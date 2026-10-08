from fastapi import APIRouter

from app.services import analytics_service

router = APIRouter()


@router.get('/')
def root():
    return {'message': 'PharmaIQ Life Sciences Intelligence API Running'}


@router.get('/api/dashboard/kpis')
def dashboard_kpis():
    overview = analytics_service.overview()
    return {
        'total_patients': overview['total_patients'],
        'active_trials': overview['active_trial_participants'],
        'high_risk_patients': overview['high_risk_patients'],
        'revenue_forecast': round(overview['revenue_forecast_3m'] / 1_000_000, 2),
        'last_updated': overview['last_updated'],
    }
