from app.schemas import ClinicalDropoutRequest, DropoutPrediction


def predict_trial_dropout(payload: ClinicalDropoutRequest) -> DropoutPrediction:
    probability = min(max(payload.previous_missed_visits * 8 + (100 - payload.completion_rate) * 0.5, 5), 92)
    return DropoutPrediction(
        dropout_probability=round(probability, 1),
        reason='Multiple missed visits' if payload.previous_missed_visits >= 2 else 'Engagement and adherence risk',
        recommended_action='Patient engagement needed'
    )
