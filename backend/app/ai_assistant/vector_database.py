import os
import pickle
from typing import List, Dict, Any

import numpy as np

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False


class VectorDatabase:
    def __init__(self, model_path: str = 'ml_engine/saved_models/', index_name: str = 'doc_index'):
        self.model_path = model_path
        self.index_name = index_name
        self.index = None
        self.metadata: List[Dict[str, Any]] = []
        self.embeddings = []
        self.dim = 0
        self.index_file = os.path.join(self.model_path, f'{self.index_name}.pkl')
        self._load_index()

    def _load_index(self):
        if os.path.exists(self.index_file):
            with open(self.index_file, 'rb') as f:
                payload = pickle.load(f)
                self.embeddings = payload.get('embeddings', [])
                self.metadata = payload.get('metadata', [])
                self.dim = payload.get('dim', 0)
                if FAISS_AVAILABLE and self.embeddings:
                    self.index = faiss.IndexFlatIP(self.dim)
                    self.index.add(np.vstack(self.embeddings))

    def _save_index(self):
        os.makedirs(self.model_path, exist_ok=True)
        with open(self.index_file, 'wb') as f:
            pickle.dump({'embeddings': self.embeddings, 'metadata': self.metadata, 'dim': self.dim}, f)

    def add_embeddings(self, embeddings: np.ndarray, metadata: List[Dict[str, Any]]):
        if embeddings.size == 0 or not metadata:
            return
        if self.dim == 0:
            self.dim = embeddings.shape[1]
        if FAISS_AVAILABLE:
            if self.index is None:
                self.index = faiss.IndexFlatIP(self.dim)
            self.index.add(embeddings)
        self.embeddings.extend([emb for emb in embeddings])
        self.metadata.extend(metadata)
        self._save_index()

    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> List[Dict[str, Any]]:
        if self.dim == 0 or query_embedding.size == 0:
            return []
        if FAISS_AVAILABLE and self.index is not None:
            query_vector = np.array([query_embedding], dtype=np.float32)
            scores, ids = self.index.search(query_vector, top_k)
            results = []
            for score, idx in zip(scores[0], ids[0]):
                if idx < 0 or idx >= len(self.metadata):
                    continue
                item = self.metadata[idx].copy()
                item['score'] = float(score)
                results.append(item)
            return results

        # Fallback similarity search
        vectors = np.vstack(self.embeddings) if self.embeddings else np.zeros((0, self.dim), dtype=np.float32)
        if vectors.size == 0:
            return []
        normalized_vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
        normalized_query = query_embedding / np.linalg.norm(query_embedding)
        scores = np.dot(normalized_vectors, normalized_query)
        top_indices = list(np.argsort(scores)[::-1][:top_k])
        return [
            {**self.metadata[idx], 'score': float(scores[idx])}
            for idx in top_indices if idx < len(self.metadata)
        ]
