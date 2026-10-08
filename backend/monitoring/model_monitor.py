from typing import Dict, List

from app.services.analytics_service import model_metrics

MODELS = ['patient_risk', 'trial_dropout', 'sales_forecast', 'doctor_segmentation']
# Primary metric per model and the minimum value considered healthy.
PRIMARY_METRIC = {
    'patient_risk': ('accuracy', 0.8),
    'trial_dropout': ('accuracy', 0.8),
    'sales_forecast': ('r2_score', 0.8),
    'doctor_segmentation': ('silhouette', 0.25),
}


class ModelMonitor:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def summary(self) -> Dict[str, object]:
        metrics = model_metrics().get(self.model_name)
        metric_name, healthy_min = PRIMARY_METRIC[self.model_name]
        if not metrics:
            return {'model': self.model_name, 'metric': metric_name, 'value': None, 'status': 'Not trained', 'trained_at': None}
        value = metrics.get(metric_name)
        return {
            'model': self.model_name,
            'metric': metric_name,
            'value': value,
            'status': 'Healthy' if value is not None and value >= healthy_min else 'Degraded',
            'trained_at': metrics.get('trained_at'),
            'samples': metrics.get('samples'),
        }

    def metrics_report(self) -> Dict[str, object]:
        return model_metrics().get(self.model_name, {})


class MonitoringRegistry:
    def __init__(self):
        self.models = [ModelMonitor(name) for name in MODELS]

    def get_models(self) -> List[Dict[str, object]]:
        return [model.summary() for model in self.models]
