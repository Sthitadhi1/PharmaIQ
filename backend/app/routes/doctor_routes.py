from typing import Optional

from fastapi import APIRouter, Query

from app.ml import segment_doctor
from app.schemas import DoctorSegmentRequest, DoctorSegmentResponse
from app.services import get_records

router = APIRouter(prefix='/api', tags=['Doctors'])


@router.get('/doctors')
def get_doctors(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    region: Optional[str] = None
):
    page = get_records('doctors', limit, offset, filters={'region': region})
    return {'doctors': page.pop('items'), **page}


@router.post('/segment/doctors', response_model=DoctorSegmentResponse)
def segment_doctors(payload: DoctorSegmentRequest):
    return segment_doctor(payload)
