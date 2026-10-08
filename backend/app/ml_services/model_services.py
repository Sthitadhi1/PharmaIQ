import json
import os

from app.database.config import MODEL_PATH
from app.utils.cache import RedisCache
from ml_engine.models.patient_risk_model import PatientRiskModel
from ml_engine.models.trial_dropout_model import TrialDropoutModel
from ml_engine.models.sales_forecasting import SalesForecastingModel
from ml_engine.models.doctor_segmentation import DoctorSegmentationModel

cache = RedisCache()


class ModelNotTrainedError(RuntimeError):
    """Raised when a model's saved artifacts are missing from MODEL_PATH."""


class _ModelService:
    model_class = None
    artifact = ''
    cache_prefix = ''

    def __init__(self, model_path: str = MODEL_PATH):
        self.model_path = model_path
        self.model = self.model_class(model_path=model_path)
        self._loaded = False

    def _ensure_loaded(self):
        if self._loaded:
            return
        if not os.path.exists(os.path.join(self.model_path, self.artifact)):
            raise ModelNotTrainedError(
                f'{self.cache_prefix} model is not trained. '
                'Run "python -m ml_engine.training.train_all" from the repository root.'
            )
        self.model.load_models()
        self._loaded = True

    def _cached(self, features: dict, compute) -> dict:
        cache_key = f'{self.cache_prefix}:{json.dumps(features, sort_keys=True)}'
        cached = cache.get(cache_key)
        if cached:
            return json.loads(cached)
        self._ensure_loaded()
        result = compute(features)
        cache.set(cache_key, json.dumps(result), expire=600)
        return result


class PatientRiskService(_ModelService):
    """Service for patient risk predictions."""
    model_class = PatientRiskModel
    artifact = 'patient_rf_model.pkl'
    cache_prefix = 'patient_risk'

    def predict(self, features: dict) -> dict:
        return self._cached(features, self.model.predict_risk_level)


class TrialDropoutService(_ModelService):
    """Service for trial dropout predictions."""
    model_class = TrialDropoutModel
    artifact = 'trial_rf_model.pkl'
    cache_prefix = 'trial_dropout'

    def predict(self, features: dict) -> dict:
        return self._cached(features, self.model.predict_dropout_risk)


class SalesForecasterService(_ModelService):
    """Service for sales forecasting."""
    model_class = SalesForecastingModel
    artifact = 'sales_rf_model.pkl'
    cache_prefix = 'sales_forecast'

    def forecast(self, features: dict) -> dict:
        return self._cached(features, self.model.forecast_sales)


class DoctorSegmentationService(_ModelService):
    """Service for doctor segmentation."""
    model_class = DoctorSegmentationModel
    artifact = 'doctor_kmeans_model.pkl'
    cache_prefix = 'doctor_segment'

    def segment(self, features: dict) -> dict:
        return self._cached(features, self.model.segment_doctor)
