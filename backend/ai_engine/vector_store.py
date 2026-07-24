from typing import Any, Dict, List

import faiss
import numpy as np


class VectorStore:
    def __init__(self):
        self.index = faiss.IndexFlatL2(384)
        self.metadata: List[Dict[str, str]] = []

    def add(self, embedding: List[float], metadata: Dict[str, str]) -> None:
        vector = np.asarray(embedding, dtype="float32").reshape(1, -1)
        self.index.add(vector)
        self.metadata.append(metadata)

    def search(self, query_embedding: List[float], top_k: int = 3) -> List[Dict[str, Any]]:
        query_vector = np.asarray(query_embedding, dtype="float32").reshape(1, -1)
        distances, indices = self.index.search(query_vector, min(top_k, self.index.ntotal))

        results: List[Dict[str, Any]] = []
        for distance, index in zip(distances[0], indices[0]):
            if index < 0:
                continue
            metadata = self.metadata[int(index)]
            results.append({"metadata": metadata, "distance": float(distance)})

        return results

    def count(self) -> int:
        return int(self.index.ntotal)
