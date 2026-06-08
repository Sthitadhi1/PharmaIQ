from typing import List, Dict

from .document_processor import DocumentProcessor
from .embeddings import EmbeddingGenerator
from .vector_store import VectorStore


class RAGPipeline:
    def __init__(self):
        self.processor = DocumentProcessor()
        self.embedding = EmbeddingGenerator()
        self.store = VectorStore()

    def ingest(self, paths: List[str]) -> int:
        total = 0
        for path in paths:
            documents = self.processor.extract_text(path)
            for doc in documents:
                embedding = self.embedding.embed_texts([doc['text']])[0]
                self.store.add(embedding, {'source': doc['source'], 'text': doc['text']})
                total += 1
        return total

    def query(self, question: str, top_k: int = 3) -> Dict[str, object]:
        query_embedding = self.embedding.embed_query(question)
        results = self.store.search(query_embedding, top_k=top_k)
        answer = 'Generated answer based on semantic similarity and domain context.'
        return {
            'question': question,
            'answer': answer,
            'recommendation': 'Increase HCP engagement campaign',
            'sources': [item['metadata']['source'] for item in results],
            'results': results
        }
