import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_trials_list_endpoint(client):
    response = client.get('/api/trials')
    assert response.status_code == 200
    assert 'trials' in response.json()


def test_trial_dropout_prediction(client):
    payload = {'trial_id': 201}
    response = client.post('/api/predict/trial-dropout', json=payload)
    assert response.status_code == 200
    data = response.json()
    assert 'dropout_probability' in data
    assert 'status' in data
