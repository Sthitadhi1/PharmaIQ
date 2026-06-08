import os
from typing import Dict, Any

import mlflow


class ExperimentTracker:
    def __init__(self, experiment_name: str = 'PharmaIQ'):
        mlflow.set_tracking_uri(os.getenv('MLFLOW_TRACKING_URI', 'file:./mlruns'))
        mlflow.set_experiment(experiment_name)

    def log_metrics(self, metrics: Dict[str, float], step: int = 0):
        with mlflow.start_run():
            for name, value in metrics.items():
                mlflow.log_metric(name, value, step=step)

    def log_params(self, params: Dict[str, Any]):
        with mlflow.start_run():
            for name, value in params.items():
                mlflow.log_param(name, value)
