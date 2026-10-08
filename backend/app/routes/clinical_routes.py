from fastapi import APIRouter, Query

from app.ml import predict_trial_dropout as score_trial_dropout
from app.schemas import TrialDropoutRequest, TrialDropoutResponse
from app.services import get_records

router = APIRouter(prefix='/api', tags=['Clinical Trials'])


@router.get('/trials')
def get_trials(limit: int = Query(50, ge=1, le=500), offset: int = Query(0, ge=0)):
    page = get_records('trials', limit, offset)
    return {'trials': page.pop('items'), **page}


@router.post('/predict/trial-dropout', response_model=TrialDropoutResponse)
def predict_trial_dropout(payload: TrialDropoutRequest):
    return score_trial_dropout(payload)
