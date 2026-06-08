import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import joblib
import os


class TrialDropoutModel:
    """
    Clinical Trial Dropout Prediction Model.
    Predicts probability of patient dropout from clinical trials.
    """

    def __init__(self, model_path: str = 'ml_engine/saved_models/'):
        self.model_path = model_path
        self.rf_model = None
        self.xgb_model = None
        self.scaler = StandardScaler()
        self.feature_names = [
            'patient_age', 'trial_duration', 'previous_participation',
            'side_effects_severity', 'health_score', 'visit_compliance'
        ]

    def prepare_data(self, df: pd.DataFrame):
        """Prepare and scale data for model training."""
        X = df[self.feature_names].values
        X_scaled = self.scaler.fit_transform(X)
        return X_scaled

    def train(self, X: np.ndarray, y: np.ndarray):
        """Train Random Forest and XGBoost classification models."""
        self.rf_model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
        self.rf_model.fit(X, y)

        self.xgb_model = xgb.XGBClassifier(n_estimators=100, random_state=42, max_depth=7)
        self.xgb_model.fit(X, y)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Ensemble prediction combining RF and XGBoost.
        Returns probability of dropout.
        """
        if self.rf_model is None or self.xgb_model is None:
            raise ValueError('Models not trained. Call train() first or load_models().')

        rf_proba = self.rf_model.predict_proba(X)[:, 1]
        xgb_proba = self.xgb_model.predict_proba(X)[:, 1]

        # Ensemble: average of both models
        ensemble_proba = (rf_proba + xgb_proba) / 2
        return ensemble_proba

    def predict_dropout_risk(self, features: dict) -> dict:
        """
        Predict trial dropout risk from feature dictionary.
        Returns dropout probability, risk level, and intervention recommendations.
        """
        X = np.array([[
            features.get('patient_age', 50),
            features.get('trial_duration', 6),
            features.get('previous_participation', 0),
            features.get('side_effects_severity', 2),  # 0-10 scale
            features.get('health_score', 75),  # 0-100 scale
            features.get('visit_compliance', 90)  # % compliance
        ]])

        X_scaled = self.scaler.transform(X)
        dropout_probability = self.predict(X_scaled)[0]

        if dropout_probability >= 0.7:
            risk_level = 'HIGH'
            intervention = 'Immediate patient engagement and support required'
        elif dropout_probability >= 0.4:
            risk_level = 'MEDIUM'
            intervention = 'Increased monitoring and support recommended'
        else:
            risk_level = 'LOW'
            intervention = 'Continue routine monitoring'

        return {
            'dropout_probability': round(float(dropout_probability), 3),
            'risk_level': risk_level,
            'intervention': intervention,
            'side_effects_factor': 'High' if features.get('side_effects_severity', 0) > 5 else 'Low',
            'compliance_status': 'Good' if features.get('visit_compliance', 0) >= 80 else 'At Risk'
        }

    def save_models(self):
        """Save trained models to disk."""
        os.makedirs(self.model_path, exist_ok=True)
        joblib.dump(self.rf_model, os.path.join(self.model_path, 'trial_rf_model.pkl'))
        joblib.dump(self.xgb_model, os.path.join(self.model_path, 'trial_xgb_model.pkl'))
        joblib.dump(self.scaler, os.path.join(self.model_path, 'trial_scaler.pkl'))

    def load_models(self):
        """Load trained models from disk."""
        self.rf_model = joblib.load(os.path.join(self.model_path, 'trial_rf_model.pkl'))
        self.xgb_model = joblib.load(os.path.join(self.model_path, 'trial_xgb_model.pkl'))
        self.scaler = joblib.load(os.path.join(self.model_path, 'trial_scaler.pkl'))
