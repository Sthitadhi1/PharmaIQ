from datetime import datetime
from typing import Dict, Any


class ExperimentTracker:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.experiments = []

    def log_experiment(self, name: str, metrics: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, Any]:
        experiment = {
            'name': name,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'metrics': metrics,
            'metadata': metadata
        }
        self.experiments.append(experiment)
        return experiment

    def list_experiments(self):
        return self.experiments
