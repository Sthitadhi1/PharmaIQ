from typing import Dict, List


class ModelRegistry:
    def __init__(self):
        self.registered_models: List[Dict[str, str]] = []

    def register_model(self, model_path: str, name: str) -> Dict[str, str]:
        entry = {'name': name, 'path': model_path, 'status': 'registered'}
        self.registered_models.append(entry)
        return entry

    def list_models(self) -> List[Dict[str, str]]:
        return self.registered_models
