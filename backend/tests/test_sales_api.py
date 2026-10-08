import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_sales_list_endpoint(client):
    response = client.get('/api/sales')
    assert response.status_code == 200
    assert response.json()['total'] > 0


def test_sales_list_region_filter_is_case_insensitive(client):
    body = client.get('/api/sales?region=north&limit=500').json()
    assert body['total'] > 0
    assert all(row['region'] == 'North' for row in body['sales'])


def test_sales_forecast_endpoint(client):
    payload = {'sales_units': 1000, 'marketing_spend': 30000}
    response = client.post('/api/forecast/sales', json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data['expected_growth'] == '+18%'
    assert data['recommended_stock'] == 1180


def test_sales_forecast_does_not_overstock_small_products(client):
    # Regression: stock used to be floored at 15,000 units regardless of demand.
    data = client.post('/api/forecast/sales', json={'sales_units': 100, 'marketing_spend': 1000}).json()
    assert data['recommended_stock'] == 110


def test_sales_forecast_spend_threshold_boundary(client):
    at_threshold = client.post('/api/forecast/sales', json={'sales_units': 100, 'marketing_spend': 25000}).json()
    above = client.post('/api/forecast/sales', json={'sales_units': 100, 'marketing_spend': 25001}).json()
    assert at_threshold['growth_percentage'] == 10
    assert above['growth_percentage'] == 18


def test_sales_forecast_rejects_negative_units(client):
    assert client.post('/api/forecast/sales', json={'sales_units': -1, 'marketing_spend': 0}).status_code == 422
