from typing import List


class EmbeddingGenerator:
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        return [[float(sum(ord(c) for c in text) % 100) / 100.0 for _ in range(8)] for text in texts]

    def embed_query(self, query: str) -> List[float]:
        return [float(sum(ord(c) for c in query) % 100) / 100.0 for _ in range(8)]
