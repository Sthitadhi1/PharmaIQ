"""Regression tests: one or more per defect in docs/TESTING_AND_BUG_REPORT.md (BUG-xx)."""
import os

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database.config import MODEL_PATH

ARTIFACTS_PRESENT = os.path.exists(os.path.join(MODEL_PATH, 'patient_rf_model.pkl'))


@pytest.fixture
def client():
    return TestClient(app)


class DummyEngine:
    def __init__(self):
        self.ingested = []

    def ingest_documents(self, paths):
        self.ingested.extend(paths)
        return len(paths)


@pytest.fixture
def upload_dir(tmp_path, monkeypatch):
    """Point uploads at a temp dir and stub the RAG engine (avoids downloading models)."""
    import app.ai_assistant.chat_controller as chat_controller
    import app.utils.uploads as uploads

    target = tmp_path / 'uploads'
    monkeypatch.setattr(uploads, 'UPLOAD_DIR', target)
    monkeypatch.setattr(chat_controller, 'engine', DummyEngine())
    return target


# BUG-06: CORS reflected any origin with credentials
def test_cors_rejects_unknown_origin(client):
    response = client.get('/health', headers={'Origin': 'http://evil.example'})
    assert 'access-control-allow-origin' not in response.headers


def test_cors_allows_configured_frontend(client):
    response = client.get('/health', headers={'Origin': 'http://localhost:5173'})
    assert response.headers['access-control-allow-origin'] == 'http://localhost:5173'


# BUG-07: path traversal / unrestricted upload
@pytest.mark.parametrize('filename', ['../../evil.txt', '..\\..\\evil.txt', '/etc/evil.txt'])
def test_upload_cannot_escape_upload_dir(client, upload_dir, filename):
    response = client.post('/api/ai/upload', files={'file': (filename, b'hello', 'text/plain')})
    assert response.status_code == 200
    assert response.json()['filename'] == 'evil.txt'
    assert (upload_dir / 'evil.txt').exists()
    assert not (upload_dir.parent / 'evil.txt').exists()


def test_upload_rejects_disallowed_extension(client, upload_dir):
    response = client.post('/api/ai/upload', files={'file': ('payload.exe', b'MZ', 'application/octet-stream')})
    assert response.status_code == 415


def test_upload_rejects_empty_file(client, upload_dir):
    assert client.post('/api/ai/upload', files={'file': ('empty.txt', b'', 'text/plain')}).status_code == 400


def test_upload_rejects_oversized_file(client, upload_dir, monkeypatch):
    import app.utils.uploads as uploads
    monkeypatch.setattr(uploads, 'MAX_UPLOAD_BYTES', 10)
    response = client.post('/api/ai/upload', files={'file': ('big.txt', b'x' * 11, 'text/plain')})
    assert response.status_code == 413


# BUG-08: RAG router existed but was never mounted
def test_rag_router_is_mounted(client):
    assert client.get('/api/rag/status').status_code == 200


# BUG-16: empty question loaded the (slow, network-bound) RAG engine before validating
def test_empty_ai_question_rejected_without_loading_engine(client, monkeypatch):
    import app.ai_assistant.chat_controller as chat_controller
    monkeypatch.setattr(chat_controller, 'engine', None)
    monkeypatch.setattr(chat_controller, 'get_engine', lambda: pytest.fail('engine loaded'))
    assert client.post('/api/ai/query', json={'question': '   '}).status_code == 400


# BUG-11 / BUG-20: auth hardening
def _login(client, username='admin', password='AdminPass123!'):
    return client.post('/api/auth/token', json={'username': username, 'password': password})


def test_refresh_token_is_rotated_and_old_one_revoked(client):
    tokens = _login(client).json()
    first = client.post('/api/auth/refresh', json={'refresh_token': tokens['refresh_token']})
    assert first.status_code == 200
    assert first.json()['refresh_token'] != tokens['refresh_token']
    replay = client.post('/api/auth/refresh', json={'refresh_token': tokens['refresh_token']})
    assert replay.status_code == 401


def test_access_token_cannot_be_used_as_refresh_token(client):
    tokens = _login(client).json()
    assert client.post('/api/auth/refresh', json={'refresh_token': tokens['access_token']}).status_code == 401


def test_login_rate_limit_returns_429(client):
    from app.routes import auth_routes
    auth_routes.limiter.access_log.clear()
    statuses = [_login(client, 'business_user', 'wrong').status_code for _ in range(11)]
    assert statuses[:10] == [401] * 10
    assert statuses[10] == 429
    auth_routes.limiter.access_log.clear()


# BUG-10: logged-in roles had no permissions entry
def test_every_user_role_has_permissions():
    from app.utils.security import fake_users_db
    from security import ROLE_PERMISSIONS, ROLES
    for user in fake_users_db.values():
        assert user['role'] in ROLES
        assert ROLE_PERMISSIONS[user['role']]


# BUG-12: unknown pipelines reported success
def test_unknown_mlops_pipeline_returns_404(client):
    assert client.post('/api/mlops/run-pipeline?pipeline=bogus').status_code == 404


# BUG-13: explainability accepted invalid ids (dataset ids start at 0, so only negatives are invalid)
@pytest.mark.parametrize('patient_id', [-1, -3])
def test_explainability_rejects_negative_ids(client, patient_id):
    assert client.get(f'/api/explainability/patient/{patient_id}').status_code == 422


# Doctor segmentation boundary values (rule-based endpoint)
@pytest.mark.parametrize('score,segment', [(100, 'Segment A'), (80, 'Segment A'), (79.9, 'Segment B'),
                                           (60, 'Segment B'), (59.9, 'Segment C'), (0, 'Segment C')])
def test_doctor_segment_boundaries(client, score, segment):
    response = client.post('/api/segment/doctors', json={'engagement_score': score})
    assert response.json()['segment'] == segment


# BUG-03 / BUG-04: ML errors were hidden behind HTTP 200
def test_untrained_model_returns_503(tmp_path):
    from app.ml_services.model_services import ModelNotTrainedError, PatientRiskService
    service = PatientRiskService(model_path=str(tmp_path))
    with pytest.raises(ModelNotTrainedError):
        service.predict({'age': 99999})


def test_ml_endpoint_rejects_out_of_range_input(client):
    payload = {'age': -500, 'previous_visits': -1, 'treatment_duration': 0, 'glucose_level': -1,
               'blood_pressure_systolic': 0, 'blood_pressure_diastolic': 0}
    assert client.post('/api/ml/patient-risk', json=payload).status_code == 422


@pytest.mark.skipif(not ARTIFACTS_PRESENT, reason='run python -m ml_engine.training.train_all first')
def test_ml_patient_risk_with_trained_model(client):
    payload = {'age': 72, 'previous_visits': 9, 'treatment_duration': 12, 'glucose_level': 190,
               'blood_pressure_systolic': 160, 'blood_pressure_diastolic': 100}
    response = client.post('/api/ml/patient-risk', json=payload)
    assert response.status_code == 200
    assert response.json()['risk_category'] == 'HIGH'
    assert 'error' not in response.json()
