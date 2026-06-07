from fastapi import APIRouter

router = APIRouter(prefix='/api')

@router.get('/trials')
def get_trials():
    return {'trials': []}

@router.post('/predict/trial-dropout')
def predict_trial_dropout(payload: dict):
    return {
        'dropout_probability': 0,
        'status': 'Model Integration Pending'
    }
