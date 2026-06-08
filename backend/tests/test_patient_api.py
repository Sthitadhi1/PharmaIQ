import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_root_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'PharmaIQ' in response.json()['message']


def test_patient_list_endpoint(client):
    response = client.get('/api/patients')
    assert response.status_code == 200
    assert 'patients' in response.json()


def test_patient_risk_prediction(client):
    payload = {'patient_id': 101}
    response = client.post('/api/predict/patient-risk', json=payload)
    assert response.status_code == 200
    data = response.json()
    assert 'risk_score' in data
    assert 'category' in data
