from fastapi import APIRouter

router = APIRouter(prefix='/api')

@router.get('/sales')
def get_sales():
    return {'sales': []}

@router.post('/forecast/sales')
def forecast_sales(payload: dict):
    return {
        'forecast': 'Future ML Forecasting Module'
    }
