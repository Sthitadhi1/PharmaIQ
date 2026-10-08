from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix='/api/mlops', tags=['MLOps'])
KNOWN_PIPELINES = {'all', 'patient', 'trial', 'sales', 'doctor'}


def get_pipeline_manager():
    try:
        from mlops.pipeline_manager import PipelineManager
    except ModuleNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f'MLOps dependency is not installed: {exc.name}'
        ) from exc

    return PipelineManager()


@router.get('/status')
def mlops_status():
    manager = get_pipeline_manager()
    return {
        'status': 'ready',
        'pipeline': 'enterprise-mlops',
        'stages': manager.stages
    }


@router.post('/run-pipeline')
def run_pipeline(pipeline: str = 'all'):
    if pipeline not in KNOWN_PIPELINES:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Unknown pipeline "{pipeline}". Expected one of: {", ".join(sorted(KNOWN_PIPELINES))}.'
        )
    try:
        manager = get_pipeline_manager()
        if pipeline == 'all':
            result = manager.run_all()
        else:
            result = manager.run_pipeline(pipeline)
        return {'status': 'completed', 'pipeline': pipeline, 'result': result}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
