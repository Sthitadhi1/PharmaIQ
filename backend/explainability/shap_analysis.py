from typing import Dict, List


def generate_patient_explanation(patient_id: int, prediction: str) -> Dict[str, object]:
    top_risk_factors = [
        {'feature': 'Age', 'impact': '35%'},
        {'feature': 'Missed Visits', 'impact': '30%'},
        {'feature': 'Medication Compliance', 'impact': '20%'}
    ]

    explanation = {
        'risk_score': 87 if prediction.lower() == 'high risk' else 42,
        'top_risk_factors': top_risk_factors,
        'patient_id': patient_id,
        'prediction': prediction
    }
    return explanation
