import json
import os
from datetime import datetime, timezone

# Absolute so training writes to the same place regardless of the current directory.
SAVED_MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'saved_models')


def save_metrics(model_name: str, metrics: dict, model_path: str = SAVED_MODELS_DIR) -> None:
    """Record a model's evaluation metrics in metrics.json (read by the monitoring API)."""
    os.makedirs(model_path, exist_ok=True)
    path = os.path.join(model_path, 'metrics.json')
    existing = {}
    if os.path.exists(path):
        with open(path, encoding='utf-8') as handle:
            existing = json.load(handle)
    existing[model_name] = {
        **{key: value if isinstance(value, int) else round(float(value), 4) for key, value in metrics.items()},
        'trained_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
    }
    with open(path, 'w', encoding='utf-8') as handle:
        json.dump(existing, handle, indent=2)
