import os
import mlflow


class ModelRegistry:
    def __init__(self, registry_uri: str = None):
        if registry_uri:
            mlflow.set_registry_uri(registry_uri)

    def register_model(self, model_uri: str, name: str, description: str = None):
        return mlflow.register_model(model_uri, name)

    def transition_model(self, name: str, version: str, stage: str):
        client = mlflow.tracking.MlflowClient()
        client.transition_model_version_stage(name, version, stage)
