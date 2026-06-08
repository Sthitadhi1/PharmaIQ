import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import joblib
import os


class PatientRiskModel:
    """
    Patient Risk Prediction Model using ensemble methods.
    Combines Random Forest, Logistic Regression, and XGBoost for robust predictions.
    """

    def __init__(self, model_path: str = 'ml_engine/saved_models/'):
        self.model_path = model_path
        self.rf_model = None
        self.lr_model = None
        self.xgb_model = None
        self.scaler = StandardScaler()
        self.feature_names = [
            'age', 'previous_visits', 'treatment_duration',
            'glucose_level', 'blood_pressure_systolic', 'blood_pressure_diastolic'
        ]

    def prepare_data(self, df: pd.DataFrame):
        """Prepare and scale data for model training."""
        X = df[self.feature_names].values
        X_scaled = self.scaler.fit_transform(X)
        return X_scaled

    def train(self, X: np.ndarray, y: np.ndarray):
        """Train all three models."""
        self.rf_model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
        self.rf_model.fit(X, y)

        self.lr_model = LogisticRegression(random_state=42, max_iter=1000)
        self.lr_model.fit(X, y)

        self.xgb_model = xgb.XGBClassifier(n_estimators=100, random_state=42, max_depth=6)
        self.xgb_model.fit(X, y)

    def predict(self, X: np.ndarray) -> dict:
        """
        Ensemble prediction combining all three models.
        Returns average probability across models.
        """
        if self.rf_model is None or self.lr_model is None or self.xgb_model is None:
            raise ValueError('Models not trained. Call train() first or load_models().')

        rf_proba = self.rf_model.predict_proba(X)[:, 1]
        lr_proba = self.lr_model.predict_proba(X)[:, 1]
        xgb_proba = self.xgb_model.predict_proba(X)[:, 1]

        # Ensemble: average of all three models
        ensemble_proba = (rf_proba + lr_proba + xgb_proba) / 3

        return ensemble_proba

    def predict_risk_level(self, features: dict) -> dict:
        """
        Predict patient risk level from feature dictionary.
        Returns risk score, category, and recommendation.
        """
        X = np.array([[
            features.get('age', 50),
            features.get('previous_visits', 0),
            features.get('treatment_duration', 0),
            features.get('glucose_level', 100),
            features.get('blood_pressure_systolic', 120),
            features.get('blood_pressure_diastolic', 80)
        ]])

        X_scaled = self.scaler.transform(X)
        risk_probability = self.predict(X_scaled)[0]

        if risk_probability >= 0.7:
            risk_category = 'HIGH'
            recommendation = 'Immediate medical attention recommended'
        elif risk_probability >= 0.4:
            risk_category = 'MEDIUM'
            recommendation = 'Regular monitoring and follow-up required'
        else:
            risk_category = 'LOW'
            recommendation = 'Continue routine care'

        return {
            'risk_probability': round(float(risk_probability), 3),
            'risk_category': risk_category,
            'recommendation': recommendation
        }

    def save_models(self):
        """Save trained models to disk."""
        os.makedirs(self.model_path, exist_ok=True)
        joblib.dump(self.rf_model, os.path.join(self.model_path, 'patient_rf_model.pkl'))
        joblib.dump(self.lr_model, os.path.join(self.model_path, 'patient_lr_model.pkl'))
        joblib.dump(self.xgb_model, os.path.join(self.model_path, 'patient_xgb_model.pkl'))
        joblib.dump(self.scaler, os.path.join(self.model_path, 'patient_scaler.pkl'))

    def load_models(self):
        """Load trained models from disk."""
        self.rf_model = joblib.load(os.path.join(self.model_path, 'patient_rf_model.pkl'))
        self.lr_model = joblib.load(os.path.join(self.model_path, 'patient_lr_model.pkl'))
        self.xgb_model = joblib.load(os.path.join(self.model_path, 'patient_xgb_model.pkl'))
        self.scaler = joblib.load(os.path.join(self.model_path, 'patient_scaler.pkl'))
