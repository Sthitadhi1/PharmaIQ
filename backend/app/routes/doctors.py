from fastapi import APIRouter
from app.schemas import DoctorSegmentRequest, DoctorSegmentResponse

router = APIRouter()

@router.get('/doctors')
def list_doctors():
    return [
        {'doctor_id': 4001, 'name': 'Dr. Meera Joshi', 'specialization': 'Cardiology', 'region': 'West', 'prescription_volume': 980, 'patient_count': 245, 'engagement_score': 89.2},
        {'doctor_id': 4002, 'name': 'Dr. Ravi Singh', 'specialization': 'Endocrinology', 'region': 'East', 'prescription_volume': 740, 'patient_count': 180, 'engagement_score': 72.5}
    ]

@router.post('/segment/doctors', response_model=DoctorSegmentResponse)
def segment_doctors(payload: DoctorSegmentRequest):
    score = payload.engagement_score
    if score >= 80:
        segment = 'Segment A'
        label = 'High Value Doctors'
        insight = 'Strong engagement and prescription volume.'
    elif score >= 60:
        segment = 'Segment B'
        label = 'Growth Opportunity'
        insight = 'Moderate engagement; prime for targeted outreach.'
    else:
        segment = 'Segment C'
        label = 'Low Engagement'
        insight = 'Requires improved communication and incentives.'
    return {'segment': segment, 'segment_label': label, 'insight': insight}
