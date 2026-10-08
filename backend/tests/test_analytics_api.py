"""Every dashboard number must equal what the CSV datasets say (no hard-coded values)."""
import os
import shutil

import pandas as pd
import pytest
from fastapi.testclient import TestClient

from app.database.config import DATA_DIR
from app.main import app

PATIENTS = pd.read_csv(DATA_DIR / 'patients.csv')
TRIALS = pd.read_csv(DATA_DIR / 'clinical_trials.csv')
SALES = pd.read_csv(DATA_DIR / 'pharma_sales.csv')
DOCTORS = pd.read_csv(DATA_DIR / 'doctors.csv')


@pytest.fixture
def client():
    return TestClient(app)


class NoDocumentsEngine:
    """Stands in for the RAG engine so tests never load the embedding model."""
    vector_db = type('DB', (), {'metadata': []})()

    def documents(self):
        return []


@pytest.fixture
def ai_client(client, monkeypatch):
    import app.ai_assistant.chat_controller as chat_controller
    monkeypatch.setattr(chat_controller, 'engine', NoDocumentsEngine())
    monkeypatch.setattr(chat_controller.llm, 'compose', lambda *args: None)
    return client


def test_overview_matches_datasets(client):
    body = client.get('/api/analytics/overview').json()
    assert body['total_patients'] == len(PATIENTS)
    assert body['high_risk_patients'] == int((PATIENTS['risk_level'] == 'HIGH').sum())
    assert body['trial_participants'] == len(TRIALS)
    assert body['total_revenue'] == pytest.approx(SALES['revenue'].sum())
    assert body['total_doctors'] == len(DOCTORS)


def test_dashboard_kpis_are_computed(client):
    body = client.get('/api/dashboard/kpis').json()
    assert body['total_patients'] == len(PATIENTS)
    assert body['active_trials'] == int((TRIALS['dropout'] == 0).sum())
    assert body['revenue_forecast'] > 0


def test_sales_region_breakdown(client):
    body = client.get('/api/analytics/sales').json()
    expected = SALES.groupby('region')['revenue'].sum().sort_values(ascending=False)
    assert [row['region'] for row in body['by_region']] == list(expected.index)
    assert body['by_region'][0]['revenue'] == pytest.approx(expected.iloc[0])
    assert len(body['forecast']['forecast']) == 3


def test_trial_dropout_by_phase(client):
    body = client.get('/api/analytics/trials').json()
    expected = TRIALS.groupby('trial_phase')['dropout'].mean() * 100
    for row in body['by_phase']:
        phase = int(row['phase'].split()[-1])
        assert row['dropout_rate'] == pytest.approx(expected[phase], abs=0.05)


def test_doctor_segments_use_rule_thresholds(client):
    body = client.get('/api/analytics/doctors').json()
    counts = {row['segment']: row['doctors'] for row in body['segments']}
    assert counts['Segment A'] == int((DOCTORS['engagement_score'] >= 80).sum())
    assert counts['Segment C'] == int((DOCTORS['engagement_score'] < 60).sum())


def test_recommendations_are_data_driven(client):
    items = client.get('/api/analytics/recommendations').json()['recommendations']
    top_region = SALES.groupby('region')['revenue'].sum().idxmax()
    assert any(top_region in item['text'] for item in items)


def test_anomaly_endpoints_report_method_and_counts(client):
    for kind in ('sales', 'patient', 'trial'):
        body = client.get(f'/api/anomalies/{kind}').json()
        assert body['records_checked'] > 0
        assert body['count'] == len(body['items']) or body['count'] > 50
        assert body['method']


def test_dataset_changes_are_picked_up_without_restart(tmp_path, monkeypatch):
    import app.services.data_service as data_service
    shutil.copy(DATA_DIR / 'doctors.csv', tmp_path / 'doctors.csv')
    monkeypatch.setattr(data_service, 'DATA_DIR', tmp_path)
    assert len(data_service.load_dataset('doctors')) == len(DOCTORS)

    trimmed = DOCTORS.head(10)
    trimmed.to_csv(tmp_path / 'doctors.csv', index=False)
    stat = os.stat(tmp_path / 'doctors.csv')
    os.utime(tmp_path / 'doctors.csv', (stat.st_atime, stat.st_mtime + 5))
    assert len(data_service.load_dataset('doctors')) == 10
    data_service._cache.pop('doctors', None)


# ---- AI assistant (BUG-27 .. BUG-29) ----

def test_ai_status_does_not_crash(ai_client):
    # BUG-27: /api/ai/status raised AttributeError (HTTP 500).
    response = ai_client.get('/api/ai/status')
    assert response.status_code == 200
    assert {d['name'] for d in response.json()['datasets']} == {'patients.csv', 'clinical_trials.csv', 'pharma_sales.csv', 'doctors.csv'}


def test_ai_answers_sales_question_from_dataset(ai_client):
    body = ai_client.post('/api/ai/query', json={'question': 'Which region generated maximum sales?'}).json()
    top_region = SALES.groupby('region')['revenue'].sum().idxmax()
    assert body['mode'] == 'dataset'
    assert body['answer'].startswith(top_region)
    assert body['sources'] == ['pharma_sales.csv']
    assert body['table']['rows'][0][0] == top_region


def test_ai_superlative_is_not_read_as_a_filter(ai_client):
    # 'highest' must not be matched as the side-effects value 'HIGH'.
    body = ai_client.post('/api/ai/query', json={'question': 'Which trial phase has the highest dropout rate?'}).json()
    worst_phase = (TRIALS.groupby('trial_phase')['dropout'].mean()).idxmax()
    assert body['answer'].startswith(f'Phase {worst_phase}')
    assert f'{len(TRIALS):,} records' in body['answer']


def test_ai_counts_high_risk_patients(ai_client):
    body = ai_client.post('/api/ai/query', json={'question': 'How many high-risk patients are there?'}).json()
    assert f"{int((PATIENTS['risk_level'] == 'HIGH').sum()):,}" in body['answer']


def test_ai_unrelated_question_gets_help_not_garbage(ai_client):
    body = ai_client.post('/api/ai/query', json={'question': 'What is the capital of France?'}).json()
    assert body['mode'] == 'help'
    assert body['suggestions']


def test_chunking_keeps_lines():
    # BUG-28: chunks lost line breaks, so list items and answers ran together.
    from app.ai_assistant.document_loader import chunk_text
    text = '1. Which is the first step?\nA. Ignore it\nB. Define the problem\nAnswer: (B)'
    assert chunk_text(text) == [text]
    long_text = '\n'.join(f'line {i} ' + 'word ' * 50 for i in range(40))
    chunks = chunk_text(long_text, chunk_size=200, overlap=60)
    assert len(chunks) > 1 and all(len(chunk.split()) <= 260 for chunk in chunks)


def test_openai_failure_falls_back_and_stops_retrying():
    # BUG-29: with no OpenAI credits every answer was a raw "[Fallback summary]" dump.
    from app.ai_assistant.llm_service import LLMService

    class NoCredits(Exception):
        pass

    service = LLMService()
    service.api_key = 'sk-test'
    import openai

    def fail(*args, **kwargs):
        raise NoCredits("Error code: 429 - {'code': 'insufficient_quota'}")

    original = openai.OpenAI
    openai.OpenAI = lambda **kwargs: type('C', (), {'chat': type('X', (), {'completions': type('Y', (), {'create': staticmethod(fail)})()})()})()
    try:
        assert service.compose('q', 'facts', []) is None
        assert service.status()['state'] == 'unavailable'
        assert service.available() is False
    finally:
        openai.OpenAI = original


def test_llm_service_targets_any_openai_compatible_server(monkeypatch):
    # LLM_BASE_URL lets the assistant use free providers (Ollama, Groq, Gemini) instead of paid OpenAI.
    import openai
    from app.ai_assistant.llm_service import LLMService

    monkeypatch.setenv('LLM_BASE_URL', 'http://localhost:11434/v1')
    monkeypatch.setenv('LLM_MODEL', 'llama3.2')
    monkeypatch.delenv('LLM_API_KEY', raising=False)
    captured = {}

    class FakeClient:
        def __init__(self, **kwargs):
            captured.update(kwargs)
            reply = type('R', (), {'choices': [type('C', (), {'message': type('M', (), {'content': 'model answer'})()})()]})()
            self.chat = type('Chat', (), {'completions': type('Comp', (), {'create': staticmethod(lambda **kw: reply)})()})()

    monkeypatch.setattr(openai, 'OpenAI', FakeClient)
    service = LLMService()
    assert service.status()['provider'] == 'Ollama (local)'
    assert service.compose('q', 'facts', []) == 'model answer'
    assert captured['base_url'] == 'http://localhost:11434/v1'


def test_unmatched_question_goes_to_language_model_with_dataset_context(client, monkeypatch):
    import app.ai_assistant.chat_controller as chat_controller
    monkeypatch.setattr(chat_controller, 'engine', NoDocumentsEngine())
    seen = {}

    def fake_compose(question, facts, passages):
        seen['facts'] = facts
        return 'model answer'

    monkeypatch.setattr(chat_controller.llm, 'compose', fake_compose)
    body = client.post('/api/ai/query', json={'question': 'Is the business healthy overall?'}).json()
    assert body['mode'] == 'llm'
    assert body['answer'] == 'model answer'
    assert 'pharma_sales.csv: 1000 rows' in seen['facts']
