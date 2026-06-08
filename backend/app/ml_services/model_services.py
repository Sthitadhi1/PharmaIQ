import json
import os
from app.utils.cache import RedisCache
from ml_engine.models.patient_risk_model import PatientRiskModel
from ml_engine.models.trial_dropout_model import TrialDropoutModel
from ml_engine.models.sales_forecasting import SalesForecastingModel
from ml_engine.models.doctor_segmentation import DoctorSegmentationModel

cache = RedisCache()


class PatientRiskService:
    """Service for patient risk predictions."""

    def __init__(self, model_path='ml_engine/saved_models/'):
        self.model = PatientRiskModel(model_path=model_path)
        self.model_path = model_path

    def predict(self, features: dict) -> dict:
        """Predict patient risk level."""
        cache_key = f'patient_risk:{json.dumps(features, sort_keys=True)}'
        cached = cache.get(cache_key)
        if cached:
            return json.loads(cached)
        try:
            if os.path.exists(os.path.join(self.model_path, 'patient_rf_model.pkl')):
                self.model.load_models()
            result = self.model.predict_risk_level(features)
            cache.set(cache_key, json.dumps(result), expire=600)
            return result
        except Exception as e:
            return {'error': str(e), 'risk_probability': 0, 'risk_category': 'UNKNOWN'}


class TrialDropoutService:
    """Service for trial dropout predictions."""

    def __init__(self, model_path='ml_engine/saved_models/'):
        self.model = TrialDropoutModel(model_path=model_path)
        self.model_path = model_path

    def predict(self, features: dict) -> dict:
        """Predict trial dropout risk."""
        cache_key = f'trial_dropout:{json.dumps(features, sort_keys=True)}'
        cached = cache.get(cache_key)
        if cached:
            return json.loads(cached)
        try:
            if os.path.exists(os.path.join(self.model_path, 'trial_rf_model.pkl')):
                self.model.load_models()
            result = self.model.predict_dropout_risk(features)
            cache.set(cache_key, json.dumps(result), expire=600)
            return result
        except Exception as e:
            return {'error': str(e), 'dropout_probability': 0, 'risk_level': 'UNKNOWN'}


class SalesForecasterService:
    """Service for sales forecasting."""

    def __init__(self, model_path='ml_engine/saved_models/'):
        self.model = SalesForecastingModel(model_path=model_path)
        self.model_path = model_path

    def forecast(self, features: dict) -> dict:
        """Forecast sales."""
        cache_key = f'sales_forecast:{json.dumps(features, sort_keys=True)}'
        cached = cache.get(cache_key)
        if cached:
            return json.loads(cached)
        try:
            if os.path.exists(os.path.join(self.model_path, 'sales_rf_model.pkl')):
                self.model.load_models()
            result = self.model.forecast_sales(features)
            cache.set(cache_key, json.dumps(result), expire=600)
            return result
        except Exception as e:
            return {'error': str(e), 'forecast_sales': 0, 'growth_percentage': 0}


class DoctorSegmentationService:
    """Service for doctor segmentation."""

    def __init__(self, model_path='ml_engine/saved_models/'):
        self.model = DoctorSegmentationModel(model_path=model_path)
        self.model_path = model_path

    def segment(self, features: dict) -> dict:
        """Segment doctor."""
        cache_key = f'doctor_segment:{json.dumps(features, sort_keys=True)}'
        cached = cache.get(cache_key)
        if cached:
            return json.loads(cached)
        try:
            if os.path.exists(os.path.join(self.model_path, 'doctor_kmeans_model.pkl')):
                self.model.load_models()
            result = self.model.segment_doctor(features)
            cache.set(cache_key, json.dumps(result), expire=600)
            return result
        except Exception as e:
            return {'error': str(e), 'segment': 'UNKNOWN', 'engagement_score': 0}
