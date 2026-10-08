import os
import re
from typing import Any, Dict, List

import numpy as np

from app.database.config import ALLOWED_UPLOAD_EXTENSIONS, MODEL_PATH, UPLOAD_DIR
from .document_loader import load_document_texts
from .vector_database import VectorDatabase

# New line, or a sentence end after a lowercase word ("... immediately. Next"), but not list labels like "A. ".
SENTENCE_SPLIT = re.compile(r'\n+|(?<=[a-z0-9)][.!?])\s+(?=[A-Z])')
MIN_RELEVANCE = 0.25


class RAGEngine:
    """Semantic search over uploaded documents, with a persistent index in MODEL_PATH.

    The embedding model loads lazily, so status checks and dataset questions stay fast.
    """

    def __init__(self, model_path: str = MODEL_PATH, upload_dir: str = str(UPLOAD_DIR)):
        self.vector_db = VectorDatabase(model_path=model_path)
        self.upload_dir = upload_dir
        self._embedder = None
        self._synced = False

    @property
    def embedder(self):
        if self._embedder is None:
            from .embedding_service import EmbeddingService
            self._embedder = EmbeddingService()
        return self._embedder

    # ---- indexing ----

    def _upload_files(self) -> Dict[str, str]:
        if not os.path.isdir(self.upload_dir):
            return {}
        return {
            name: os.path.join(self.upload_dir, name)
            for name in sorted(os.listdir(self.upload_dir))
            if os.path.splitext(name)[1].lower() in ALLOWED_UPLOAD_EXTENSIONS
        }

    def sync_upload_dir(self) -> None:
        """Index documents already in the upload folder (e.g. from before a restart); drop deleted ones."""
        if self._synced:
            return
        files = self._upload_files()
        indexed = self.vector_db.sources()
        for name in indexed:
            if name not in files:
                self.vector_db.replace_source(name, np.zeros((0, 0), dtype=np.float32), [])
        missing = [path for name, path in files.items() if name not in indexed]
        if missing:
            self.ingest_documents(missing)
        self._synced = True

    def ingest_documents(self, paths: List[str]) -> int:
        total = 0
        for path in paths:
            name = os.path.basename(path)
            texts = [chunk['text'] for chunk in load_document_texts(path) if chunk['text'].strip()]
            embeddings = self.embedder.embed_texts(texts) if texts else np.zeros((0, 0), dtype=np.float32)
            self.vector_db.replace_source(name, embeddings, [{'source': name, 'text': text} for text in texts])
            total += len(texts)
        return total

    def documents(self) -> List[Dict[str, Any]]:
        indexed = self.vector_db.sources()
        names = sorted(set(indexed) | set(self._upload_files()))
        return [{'name': name, 'chunks': indexed.get(name, 0)} for name in names]

    # ---- retrieval ----

    def search(self, question: str, top_k: int = 3) -> List[Dict[str, Any]]:
        self.sync_upload_dir()
        if not self.vector_db.metadata:
            return []
        results = self.vector_db.search(self.embedder.embed_query(question), top_k=top_k)
        return [
            {'source': item.get('source'), 'text': item.get('text', ''), 'score': round(item.get('score', 0.0), 3)}
            for item in results if item.get('score', 0.0) >= MIN_RELEVANCE
        ]

    def extractive_answer(self, question: str, passages: List[Dict[str, Any]], context_lines: int = 5) -> str:
        """Finds the sentence most similar to the question and returns it with the lines that follow it.

        Following lines matter for Q&A-style documents, where the answer comes after the matched question.
        """
        segments = []  # (text, source, position within its passage's segment list)
        per_passage = []
        for passage in passages:
            parts = [' '.join(part.split()) for part in SENTENCE_SPLIT.split(passage['text'])]
            parts = [part for part in parts if part]
            per_passage.append((parts, passage['source']))
        for passage_index, (parts, source) in enumerate(per_passage):
            for position, part in enumerate(parts):
                if len(part) >= 20:
                    segments.append((part, passage_index, position))
        if not segments:
            return passages[0]['text'][:600] if passages else ''
        segments = segments[:300]
        vectors = self.embedder.embed_texts([text for text, _, _ in segments])
        scores = vectors @ self.embedder.embed_query(question)
        _, passage_index, position = segments[int(np.argmax(scores))]
        parts, source = per_passage[passage_index]
        excerpt = ' / '.join(parts[position:position + 1 + context_lines])
        return f'{excerpt[:600]} [{source}]'

    def query(self, question: str, top_k: int = 3) -> Dict[str, Any]:
        """Document-only question answering (used by /api/rag/query)."""
        passages = self.search(question, top_k=top_k)
        answer = self.extractive_answer(question, passages) if passages else 'No relevant passage found in the uploaded documents.'
        return {'question': question, 'answer': answer, 'sources': sorted({p['source'] for p in passages}), 'passages': passages}
