from app.schemas import TrialDropoutRequest, TrialDropoutResponse

SIDE_EFFECT_PENALTY = {'NONE': 0, 'LOW': 3, 'MEDIUM': 6, 'HIGH': 10}


def predict_trial_dropout(payload: TrialDropoutRequest) -> TrialDropoutResponse:
    raw = (
        payload.previous_missed_visits * 8
        + (100 - payload.completion_rate) * 0.5
        + SIDE_EFFECT_PENALTY[payload.side_effects]
    )
    probability = round(min(max(raw, 5), 92), 1)
    risk_level = 'HIGH' if probability >= 60 else 'MEDIUM' if probability >= 30 else 'LOW'

    if payload.previous_missed_visits >= 2:
        reason = 'Multiple missed visits'
    elif payload.side_effects == 'HIGH':
        reason = 'Severe side effects reported'
    else:
        reason = 'Engagement and adherence risk'

    return TrialDropoutResponse(
        trial_id=payload.trial_id,
        dropout_probability=probability,
        risk_level=risk_level,
        reason=reason,
        recommended_action='Patient engagement needed' if risk_level != 'LOW' else 'Continue standard follow-up'
    )
