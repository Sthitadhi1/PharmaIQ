from fastapi import APIRouter

from recommendation_engine.recommender import RecommendationEngine

router = APIRouter(prefix='/api/recommendations', tags=['Recommendations'])
engine = RecommendationEngine()


@router.get('/doctor')
def doctor_recommendation():
    return engine.recommend({'type': 'doctor'})


@router.get('/sales')
def sales_recommendation():
    return engine.recommend({'type': 'sales'})


@router.get('/patient')
def patient_recommendation():
    return engine.recommend({'type': 'patient'})
