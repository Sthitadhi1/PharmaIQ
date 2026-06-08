from typing import Dict, List


class ModelMonitor:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.metrics = {
            'accuracy': 91,
            'precision': 88,
            'recall': 86,
            'prediction_count': 12500,
            'last_training_date': '2026-06-01'
        }

    def summary(self) -> Dict[str, object]:
        return {
            'model': self.model_name,
            'accuracy': self.metrics['accuracy'],
            'status': 'Healthy' if self.metrics['accuracy'] >= 85 else 'Degraded',
            'prediction_count': self.metrics['prediction_count'],
            'last_training_date': self.metrics['last_training_date']
        }

    def metrics_report(self) -> Dict[str, object]:
        return self.metrics


class MonitoringRegistry:
    def __init__(self):
        self.models = [
            ModelMonitor('patient-risk'),
            ModelMonitor('trial-dropout'),
            ModelMonitor('sales-forecast'),
            ModelMonitor('doctor-segmentation')
        ]

    def get_models(self) -> List[Dict[str, object]]:
        return [model.summary() for model in self.models]
