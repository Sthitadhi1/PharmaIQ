from app.schemas import DoctorSegmentRequest, DoctorSegmentResponse


def segment_doctor(payload: DoctorSegmentRequest) -> DoctorSegmentResponse:
    score = payload.engagement_score
    if score >= 80:
        return DoctorSegmentResponse(segment='Segment A', segment_label='High Value Doctors', insight='Strong engagement and prescription volume.')
    if score >= 60:
        return DoctorSegmentResponse(segment='Segment B', segment_label='Growth Opportunity', insight='Moderate engagement; prime for targeted outreach.')
    return DoctorSegmentResponse(segment='Segment C', segment_label='Low Engagement', insight='Requires improved communication and incentives.')
