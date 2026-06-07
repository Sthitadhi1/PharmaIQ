from fastapi import APIRouter
from app.schemas import AnalyticsOverview

router = APIRouter()

@router.get('/overview', response_model=AnalyticsOverview)
def overview():
    return {
        'total_patients': 1920,
        'active_trials': 28,
        'high_risk_patients': 314,
        'revenue_forecast': '$4.8M',
        'average_risk_score': 68.4
    }
