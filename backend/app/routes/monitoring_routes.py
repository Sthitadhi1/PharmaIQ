from fastapi import APIRouter
from monitoring.model_monitor import MonitoringRegistry
from monitoring.drift_detection import DriftDetector

router = APIRouter(prefix='/api/model-monitoring', tags=['Model Monitoring'])
monitor_registry = MonitoringRegistry()
drift_detector = DriftDetector()


@router.get('/status')
def monitoring_status():
    return {
        'models': [
            {
                'name': model['model'],
                'accuracy': f"{model['accuracy']}%",
                'drift': drift_detector.detect()['drift'],
                'status': model['status']
            }
            for model in monitor_registry.get_models()
        ]
    }


@router.get('/metrics')
def monitoring_metrics():
    return {
        'summary': monitor_registry.get_models(),
        'drift_analysis': drift_detector.detect()
    }
