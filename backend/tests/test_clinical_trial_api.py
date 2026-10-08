import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_trials_list_endpoint(client):
    response = client.get('/api/trials')
    assert response.status_code == 200
    body = response.json()
    assert 'trials' in body
    assert body['total'] > 0


def test_trial_dropout_prediction(client):
    payload = {'trial_id': 201, 'completion_rate': 40, 'previous_missed_visits': 3, 'side_effects': 'HIGH'}
    response = client.post('/api/predict/trial-dropout', json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data['dropout_probability'] == pytest.approx(64.0)
    assert data['risk_level'] == 'HIGH'
    assert data['reason'] == 'Multiple missed visits'


def test_trial_dropout_probability_is_capped(client):
    payload = {'completion_rate': 0, 'previous_missed_visits': 50, 'side_effects': 'HIGH'}
    assert client.post('/api/predict/trial-dropout', json=payload).json()['dropout_probability'] == 92


@pytest.mark.parametrize('payload', [
    {'completion_rate': 140, 'previous_missed_visits': 0},
    {'completion_rate': 50, 'previous_missed_visits': -1},
    {'completion_rate': 50, 'previous_missed_visits': 0, 'side_effects': 'EXTREME'},
    {'trial_id': 201},
])
def test_trial_dropout_rejects_invalid_input(client, payload):
    assert client.post('/api/predict/trial-dropout', json=payload).status_code == 422
