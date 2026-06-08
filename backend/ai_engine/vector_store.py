from typing import Any, Dict, List


class VectorStore:
    def __init__(self):
        self.index: List[Dict[str, Any]] = []

    def add(self, embedding: List[float], metadata: Dict[str, str]) -> None:
        self.index.append({'embedding': embedding, 'metadata': metadata})

    def search(self, query_embedding: List[float], top_k: int = 3) -> List[Dict[str, Any]]:
        def score(item):
            return sum(min(q, e) for q, e in zip(query_embedding, item['embedding']))

        ranked = sorted(self.index, key=score, reverse=True)
        return ranked[:top_k]

    def count(self) -> int:
        return len(self.index)
