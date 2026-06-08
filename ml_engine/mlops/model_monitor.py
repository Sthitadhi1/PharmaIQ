from typing import Dict, Any


class ModelMonitor:
    def log_performance(self, metrics: Dict[str, float]):
        return { 'monitoring': 'logged', 'metrics': metrics }

    def alert_on_drift(self, drift_score: float, threshold: float = 0.1):
        if drift_score > threshold:
            return { 'alert': True, 'message': 'Data drift exceeds threshold' }
        return { 'alert': False, 'message': 'Model drift within expected bounds' }
