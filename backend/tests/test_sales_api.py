import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_sales_list_endpoint(client):
    response = client.get('/api/sales')
    assert response.status_code == 200
    assert 'sales' in response.json()


def test_sales_forecast_endpoint(client):
    payload = {'sales_id': 301}
    response = client.post('/api/forecast/sales', json=payload)
    assert response.status_code == 200
    data = response.json()
    assert 'forecast' in data
