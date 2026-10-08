from fastapi import APIRouter

from app.services import analytics_service

router = APIRouter(prefix='/api/recommendations', tags=['Recommendations'])

AREAS = {'doctor': 'Doctors', 'sales': 'Sales', 'patient': 'Patients', 'trial': 'Clinical'}


def _for_area(area: str):
    return {
        'area': area,
        'recommendations': [item['text'] for item in analytics_service.recommendations() if item['area'] == area],
    }


@router.get('/doctor')
def doctor_recommendation():
    return _for_area(AREAS['doctor'])


@router.get('/sales')
def sales_recommendation():
    return _for_area(AREAS['sales'])


@router.get('/patient')
def patient_recommendation():
    return _for_area(AREAS['patient'])


@router.get('/trial')
def trial_recommendation():
    return _for_area(AREAS['trial'])
