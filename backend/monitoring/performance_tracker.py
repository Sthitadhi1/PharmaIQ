from typing import Dict


class PerformanceTracker:
    def __init__(self):
        self.performance = {
            'patient-risk': {'accuracy': 91, 'precision': 88, 'recall': 86},
            'trial-dropout': {'accuracy': 89, 'precision': 85, 'recall': 82},
            'sales-forecast': {'rmse': 5.7, 'mae': 4.2}
        }

    def get_metrics(self) -> Dict[str, Dict[str, object]]:
        return self.performance
