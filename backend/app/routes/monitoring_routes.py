from fastapi import APIRouter
from monitoring.model_monitor import MonitoringRegistry
from monitoring.drift_detection import DriftDetector

router = APIRouter(prefix='/api/model-monitoring', tags=['Model Monitoring'])
monitor_registry = MonitoringRegistry()
drift_detector = DriftDetector()


def _display(model: dict) -> str:
    value = model['value']
    if value is None:
        return '—'
    return f"{value * 100:.1f}%" if model['metric'] == 'accuracy' else f'{value:.3f}'


@router.get('/status')
def monitoring_status():
    drift = drift_detector.detect()
    return {
        'models': [
            {
                'name': model['model'],
                'metric': model['metric'],
                'accuracy': _display(model),
                'value': model['value'],
                'status': model['status'],
                'trained_at': model['trained_at'],
                'drift': drift['drift'] if model['model'] == 'sales_forecast' else 'n/a',
            }
            for model in monitor_registry.get_models()
        ],
        'data_drift': drift,
    }


@router.get('/metrics')
def monitoring_metrics():
    return {
        'summary': monitor_registry.get_models(),
        'drift_analysis': drift_detector.detect()
    }
