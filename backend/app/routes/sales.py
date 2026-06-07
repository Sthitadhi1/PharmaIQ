from fastapi import APIRouter
from app.schemas import SalesForecastRequest, SalesForecastResponse

router = APIRouter()

@router.get('/sales')
def list_sales():
    return [
        {'sales_id': 3001, 'medicine': 'Medicare A', 'region': 'North', 'units_sold': 4500, 'revenue': 180000.0, 'date': '2026-05-01'},
        {'sales_id': 3002, 'medicine': 'Medicare B', 'region': 'South', 'units_sold': 3800, 'revenue': 152000.0, 'date': '2026-05-01'}
    ]

@router.post('/forecast/sales', response_model=SalesForecastResponse)
def forecast_sales(payload: SalesForecastRequest):
    growth = 18 if payload.marketing_spend > 25000 else 10
    stock = max(15000, int(payload.sales_units * (1 + growth / 100)))
    return {
        'expected_growth': f'+{growth}%',
        'recommended_stock': stock
    }
