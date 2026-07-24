import os
from typing import List, Dict

from dotenv import load_dotenv
from openai import OpenAI

from .document_processor import DocumentProcessor
from .embeddings import EmbeddingGenerator
from .vector_store import VectorStore

load_dotenv()


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

        if not results:
            answer = "No relevant context was found in the indexed documents."
        else:
            context_chunks = [item['metadata'].get('text', '') for item in results if item.get('metadata', {}).get('text')]
            context = "\n\n".join(context_chunks)
            api_key = os.getenv("OPENAI_API_KEY")

            if api_key:
                client = OpenAI(api_key=api_key)
                prompt = (
                    "You are a helpful assistant answering from the provided context only. "
                    "Use the context below to answer the user's question. "
                    "If the context does not contain enough information, say so clearly.\n\n"
                    f"Context:\n{context}\n\n"
                    f"Question: {question}"
                )
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "You answer using only the provided context."},
                            {"role": "user", "content": prompt},
                        ],
                        temperature=0.2,
                    )
                    answer = response.choices[0].message.content.strip()
                except Exception:
                    top_text = context_chunks[0] if context_chunks else ""
                    answer = f"[Fallback summary] {top_text[:800]}"
            else:
                top_text = context_chunks[0] if context_chunks else ""
                answer = f"[No OpenAI API key] Extractive summary of top retrieved chunk: {top_text[:800]}"

        return {
            'question': question,
            'answer': answer,
            'recommendation': 'Increase HCP engagement campaign',
            'sources': [item['metadata']['source'] for item in results],
            'results': results
        }
