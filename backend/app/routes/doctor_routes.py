from fastapi import APIRouter

router = APIRouter(prefix='/api')

@router.get('/doctors')
def get_doctors():
    return {'doctors': []}

@router.post('/segment/doctors')
def segment_doctors(payload: dict):
    return {
        'segment': 'KMeans Model Pending'
    }
