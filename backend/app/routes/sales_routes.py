from typing import Optional

from fastapi import APIRouter, Query

from app.ml import forecast_sales as compute_sales_forecast
from app.schemas import SalesForecastRequest, SalesForecastResponse
from app.services import get_records

router = APIRouter(prefix='/api', tags=['Sales'])


@router.get('/sales')
def get_sales(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    region: Optional[str] = None
):
    page = get_records('sales', limit, offset, filters={'region': region})
    return {'sales': page.pop('items'), **page}


@router.post('/forecast/sales', response_model=SalesForecastResponse)
def forecast_sales(payload: SalesForecastRequest):
    return compute_sales_forecast(payload)
