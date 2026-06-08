import json
from fastapi import APIRouter
from app.utils.cache import RedisCache

router = APIRouter()
cache = RedisCache()

@router.get('/')
def root():
    return {'message': 'PharmaIQ Life Sciences Intelligence API Running'}

@router.get('/api/dashboard/kpis')
def dashboard_kpis():
    cache_key = 'dashboard_kpis'
    cached = cache.get(cache_key)
    if cached:
        return json.loads(cached)

    payload = {
        'total_patients': 1920,
        'active_trials': 28,
        'high_risk_patients': 314,
        'revenue_forecast': 4.8,
        'last_updated': '2026-06-07T00:00:00Z'
    }
    cache.set(cache_key, json.dumps(payload), expire=300)
    return payload
