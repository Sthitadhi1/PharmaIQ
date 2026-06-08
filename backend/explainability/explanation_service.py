from typing import Dict

from .shap_analysis import generate_patient_explanation


class ExplanationService:
    def __init__(self):
        self.model_name = 'patient-risk-explainer'

    def explain_patient_risk(self, patient_id: int) -> Dict[str, object]:
        prediction = 'High Risk' if patient_id % 2 == 1 else 'Moderate Risk'
        explanation = generate_patient_explanation(patient_id, prediction)
        explanation['reason'] = 'Risk increased due to missed visits and low medication adherence'
        return explanation
