from typing import List

try:
    from ai_engine.rag_pipeline import RAGPipeline
except ModuleNotFoundError:
    from .document_loader import load_document_texts
    from .embedding_service import EmbeddingService
    from .vector_database import VectorDatabase
    from .llm_service import LLMService
    RAGPipeline = None


class RAGEngine:
    def __init__(self, model_path: str = 'ml_engine/saved_models/'):
        if RAGPipeline is not None:
            self.pipeline = RAGPipeline()
        else:
            self.embedding_service = EmbeddingService()
            self.vector_db = VectorDatabase(model_path=model_path)
            self.llm_service = LLMService()
            self.pipeline = None

    def ingest_documents(self, paths: List[str]) -> int:
        if self.pipeline is not None:
            return self.pipeline.ingest(paths)

        all_metadata = []
        texts = []
        for path in paths:
            chunks = load_document_texts(path)
            for chunk in chunks:
                if chunk['text'].strip():
                    texts.append(chunk['text'])
                    all_metadata.append({'source': chunk['source'], 'text': chunk['text']})
        if not texts:
            return 0
        embeddings = self.embedding_service.embed_texts(texts)
        self.vector_db.add_embeddings(embeddings, all_metadata)
        return len(texts)

    def query(self, question: str, top_k: int = 3) -> dict:
        if self.pipeline is not None:
            return self.pipeline.query(question, top_k=top_k)

        query_embedding = self.embedding_service.embed_query(question)
        results = self.vector_db.search(query_embedding, top_k=top_k)
        contexts = [item.get('text', item.get('source', '')) for item in results]
        answer = self.llm_service.generate_answer(question, contexts)
        return {
            'question': question,
            'answer': answer,
            'sources': [item.get('source') for item in results],
            'results': results
        }
