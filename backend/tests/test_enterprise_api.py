import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_explainability_patient_endpoint(client):
    response = client.get('/api/explainability/patient/1001')
    assert response.status_code == 200
    body = response.json()
    assert body['prediction'] == 'High Risk'
    assert 'reason' in body
    assert 'details' in body
    assert body['details']['risk_score'] == 87


def test_model_monitoring_status(client):
    response = client.get('/api/model-monitoring/status')
    assert response.status_code == 200
    body = response.json()
    assert 'models' in body
    assert isinstance(body['models'], list)
    assert body['models'][0]['status'] in ('Healthy', 'Degraded')


def test_security_roles_endpoint(client):
    response = client.get('/api/auth/roles')
    assert response.status_code == 200
    body = response.json()
    assert 'roles' in body
    assert 'ADMIN' in body['roles']
    assert 'permissions' in body


def test_executive_strategy_endpoint(client):
    payload = {'trial_dropout': 'High', 'region': 'Chennai'}
    response = client.post('/api/executive/strategy', json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body['business_problem'] == 'Clinical trial retention risk detected'
    assert 'Increase patient follow-up frequency' in body['recommendations']
