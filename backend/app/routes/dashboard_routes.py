from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def root():
    return {'message': 'PharmaIQ Life Sciences Intelligence API Running'}
