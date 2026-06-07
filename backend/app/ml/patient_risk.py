from app.schemas import PatientRiskRequest, RiskPrediction


def predict_patient_risk(payload: PatientRiskRequest) -> RiskPrediction:
    score = 0.4 * (payload.age / 100) + 0.3 * (payload.glucose_level / 200) + 0.3 * (payload.previous_visits / 10)
    risk_score = round(min(max(score * 100, 15), 95), 1)
    category = 'HIGH' if risk_score >= 70 else 'MEDIUM' if risk_score >= 40 else 'LOW'
    return RiskPrediction(
        risk_score=risk_score,
        risk_category=category,
        recommended_action='Immediate follow-up required' if category == 'HIGH' else 'Monitor progress regularly'
    )
