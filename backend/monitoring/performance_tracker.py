from typing import Dict

from app.services.analytics_service import model_metrics


class PerformanceTracker:
    """Evaluation metrics recorded by the training scripts (ml_engine/saved_models/metrics.json)."""

    def get_metrics(self) -> Dict[str, Dict[str, object]]:
        return model_metrics()
