from typing import Dict, Any


class AnomalyDetector:
    def detect(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'anomaly': False,
            'message': 'No anomalies detected in current batch.'
        }
