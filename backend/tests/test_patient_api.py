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
    body = response.json()
    assert 'patients' in body
    assert body['total'] > 0
    assert len(body['patients']) == min(50, body['total'])


def test_patient_list_pagination(client):
    first = client.get('/api/patients?limit=2&offset=0').json()['patients']
    second = client.get('/api/patients?limit=2&offset=2').json()['patients']
    assert len(first) == 2 and len(second) == 2
    assert first[0]['patient_id'] != second[0]['patient_id']


@pytest.mark.parametrize('query', ['limit=0', 'limit=501', 'offset=-1'])
def test_patient_list_rejects_invalid_paging(client, query):
    assert client.get(f'/api/patients?{query}').status_code == 422


def test_patient_risk_prediction(client):
    payload = {'patient_id': 101, 'age': 72, 'glucose_level': 190, 'previous_visits': 9}
    response = client.post('/api/predict/patient-risk', json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data['patient_id'] == 101
    assert data['risk_score'] == pytest.approx(84.3)
    assert data['category'] == 'HIGH'


def test_patient_risk_low_risk_patient(client):
    payload = {'age': 20, 'glucose_level': 80, 'previous_visits': 0}
    data = client.post('/api/predict/patient-risk', json=payload).json()
    assert data['risk_score'] == pytest.approx(20.0)
    assert data['category'] == 'LOW'


def test_patient_risk_requires_clinical_fields(client):
    response = client.post('/api/predict/patient-risk', json={'patient_id': 101})
    assert response.status_code == 422


@pytest.mark.parametrize('field,value', [('age', -5), ('age', 121), ('glucose_level', 0), ('previous_visits', -1)])
def test_patient_risk_rejects_out_of_range_values(client, field, value):
    payload = {'age': 50, 'glucose_level': 100, 'previous_visits': 1, field: value}
    assert client.post('/api/predict/patient-risk', json=payload).status_code == 422
