from fastapi import APIRouter

from app.services import analytics_service

router = APIRouter(prefix='/api/analytics', tags=['Analytics'])


@router.get('/overview')
def analytics_overview():
    return analytics_service.overview()


@router.get('/patients')
def analytics_patients():
    return analytics_service.patient_analytics()


@router.get('/trials')
def analytics_trials():
    return analytics_service.trial_analytics()


@router.get('/sales')
def analytics_sales():
    return analytics_service.sales_analytics()


@router.get('/doctors')
def analytics_doctors():
    return analytics_service.doctor_analytics()


@router.get('/recommendations')
def analytics_recommendations():
    return {'recommendations': analytics_service.recommendations()}


@router.get('/model-metrics')
def analytics_model_metrics():
    return analytics_service.model_metrics()
