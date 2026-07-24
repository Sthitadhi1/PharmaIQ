from types import SimpleNamespace

import numpy as np

from ai_engine.rag_pipeline import RAGPipeline


class DummySentenceTransformer:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def encode(self, texts, convert_to_numpy=True):
        if isinstance(texts, str):
            values = np.ones(384, dtype=np.float32)
            return values if not convert_to_numpy else values

        if isinstance(texts, list):
            return np.ones((len(texts), 384), dtype=np.float32)

        raise TypeError("Unsupported input type")


class DummyOpenAIClient:
    def __init__(self, *args, **kwargs):
        self.chat = SimpleNamespace(
            completions=SimpleNamespace(
                create=lambda *args, **kwargs: SimpleNamespace(
                    choices=[SimpleNamespace(message=SimpleNamespace(content="mocked answer"))]
                )
            )
        )


def test_rag_pipeline_ingests_and_queries(monkeypatch, tmp_path):
    monkeypatch.setattr("ai_engine.embeddings.SentenceTransformer", DummySentenceTransformer)
    monkeypatch.setattr("ai_engine.rag_pipeline.OpenAI", DummyOpenAIClient)
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    doc1 = tmp_path / "doc1.txt"
    doc2 = tmp_path / "doc2.txt"
    doc1.write_text("PharmaIQ helps detect anomalies in clinical trial data.", encoding="utf-8")
    doc2.write_text("Sales recommendations improve HCP engagement campaigns.", encoding="utf-8")

    pipeline = RAGPipeline()

    ingested_count = pipeline.ingest([str(doc1), str(doc2)])
    assert ingested_count == 2
    assert pipeline.store.count() == 2

    embeddings = pipeline.embedding.embed_texts(["alpha", "beta"])
    assert len(embeddings) == 2
    assert len(embeddings[0]) == 384
    assert len(embeddings[1]) == 384

    query_embedding = pipeline.embedding.embed_query("What does PharmaIQ do?")
    assert len(query_embedding) == 384

    response = pipeline.query("What does PharmaIQ do?", top_k=2)

    assert response["question"] == "What does PharmaIQ do?"
    assert response["answer"] == "mocked answer"
    assert response["results"]
    assert response["sources"]
    assert all(source for source in response["sources"])
