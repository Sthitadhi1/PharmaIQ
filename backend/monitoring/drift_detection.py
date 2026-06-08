from typing import Dict


class DriftDetector:
    def __init__(self):
        self.summary = {
            'distribution_change': '2%',
            'accuracy_drop': '1.5%',
            'prediction_pattern_change': 'stable',
            'drift_score': 2
        }

    def detect(self) -> Dict[str, str]:
        return {
            'drift': self.summary['distribution_change'],
            'accuracy_drop': self.summary['accuracy_drop'],
            'prediction_pattern_change': self.summary['prediction_pattern_change'],
            'status': 'Healthy' if float(self.summary['drift_score']) < 5 else 'Monitor'
        }
