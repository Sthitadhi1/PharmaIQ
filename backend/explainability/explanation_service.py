import os
from typing import Dict, Optional, Tuple

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from app.services.analytics_service import patients_frame
from app.services.data_service import dataset_path

FEATURES = {
    'age': 'Age',
    'blood_pressure': 'Blood pressure',
    'cholesterol': 'Cholesterol',
    'diabetes': 'Diabetes',
    'previous_admissions': 'Previous admissions',
    'medication_adherence': 'Medication adherence',
}


class PatientNotFoundError(LookupError):
    pass


class ExplanationService:
    """Explains patient risk with a logistic regression fitted on patients.csv.

    For a linear model, coefficient x standardised value is the exact contribution of each
    feature to the log-odds (equivalent to SHAP values for a linear model with independent features).
    """

    def __init__(self):
        self.model_name = 'patient-risk-logistic-explainer'
        self._fitted: Optional[Tuple[float, StandardScaler, LogisticRegression, float]] = None

    def _model(self):
        mtime = os.path.getmtime(dataset_path('patients'))
        if self._fitted is None or self._fitted[0] != mtime:
            df = patients_frame()
            X = df[list(FEATURES)].to_numpy(dtype=float)
            scaler = StandardScaler().fit(X)
            model = LogisticRegression(max_iter=1000).fit(scaler.transform(X), df['is_high_risk'])
            accuracy = float(model.score(scaler.transform(X), df['is_high_risk']))
            self._fitted = (mtime, scaler, model, accuracy)
        return self._fitted[1], self._fitted[2], self._fitted[3]

    def explain_patient_risk(self, patient_id: int) -> Dict[str, object]:
        df = patients_frame()
        match = df[df['patient_id'] == patient_id]
        if match.empty:
            raise PatientNotFoundError(patient_id)
        row = match.iloc[0]
        scaler, model, accuracy = self._model()

        values = row[list(FEATURES)].to_numpy(dtype=float).reshape(1, -1)
        contributions = model.coef_[0] * scaler.transform(values)[0]
        probability = float(model.predict_proba(scaler.transform(values))[0, 1])
        high_risk = probability >= 0.5

        # Factors pushing toward the predicted class, strongest first.
        direction = 1 if high_risk else -1
        order = np.argsort(-direction * contributions)
        total = float(np.abs(contributions).sum()) or 1.0
        averages = df[list(FEATURES)].mean()
        factors = []
        for index in order[:3]:
            feature = list(FEATURES)[index]
            if direction * contributions[index] <= 0:
                continue
            factors.append({
                'feature': FEATURES[feature],
                'impact': f'{abs(contributions[index]) / total * 100:.0f}%',
                'value': float(row[feature]),
                'dataset_average': round(float(averages[feature]), 1),
            })

        def describe(factor):
            side = 'above' if factor['value'] > factor['dataset_average'] else 'below'
            return f"{factor['feature'].lower()} {factor['value']:g} ({side} the average of {factor['dataset_average']:g})"

        verb = 'increased' if high_risk else 'kept low'
        if factors:
            reason = f'Risk {verb} mainly by ' + '; '.join(describe(factor) for factor in factors)
        else:
            reason = 'No single factor dominates this prediction.'

        return {
            'patient_id': int(patient_id),
            'prediction': 'High Risk' if high_risk else 'Low Risk',
            'risk_score': round(probability * 100, 1),
            'recorded_risk_level': row['risk_level'],
            'top_risk_factors': factors,
            'reason': reason,
            'model': {'name': self.model_name, 'training_accuracy': round(accuracy, 3), 'trained_on': 'patients.csv'},
        }
