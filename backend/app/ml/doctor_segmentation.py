from app.schemas import DoctorSegmentRequest, DoctorSegmentResponse


def segment_doctor(payload: DoctorSegmentRequest) -> DoctorSegmentResponse:
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
    return DoctorSegmentResponse(segment=segment, segment_label=label, insight=insight)
