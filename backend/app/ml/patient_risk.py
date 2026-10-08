from app.schemas import PatientRiskRequest, PatientRiskResponse

HIGH_RISK_THRESHOLD = 70
MEDIUM_RISK_THRESHOLD = 40


def _normalise(value: float, ceiling: float) -> float:
    """Scale a feature to 0..1 so one extreme input cannot dominate the score."""
    return min(max(value / ceiling, 0.0), 1.0)


def risk_category(risk_score: float) -> str:
    if risk_score >= HIGH_RISK_THRESHOLD:
        return 'HIGH'
    if risk_score >= MEDIUM_RISK_THRESHOLD:
        return 'MEDIUM'
    return 'LOW'


def predict_patient_risk(payload: PatientRiskRequest) -> PatientRiskResponse:
    score = (
        0.4 * _normalise(payload.age, 100)
        + 0.3 * _normalise(payload.glucose_level, 200)
        + 0.3 * _normalise(payload.previous_visits, 10)
    )
    risk_score = round(score * 100, 1)
    category = risk_category(risk_score)
    return PatientRiskResponse(
        patient_id=payload.patient_id,
        risk_score=risk_score,
        category=category,
        recommended_action='Immediate follow-up required' if category == 'HIGH' else 'Monitor progress regularly'
    )
