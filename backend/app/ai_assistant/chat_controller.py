import os
import shutil
import json

from fastapi import APIRouter, HTTPException, UploadFile, File, status
from pydantic import BaseModel

from app.utils.cache import RedisCache

router = APIRouter(prefix='/api/ai', tags=['AI Assistant'])
cache = RedisCache()
engine = None


class AIQueryRequest(BaseModel):
    question: str
    top_k: int = 3


def get_engine():
    global engine
    if engine is not None:
        return engine

    try:
        from .rag_engine import RAGEngine
    except ModuleNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f'AI assistant dependency is not installed: {exc.name}'
        ) from exc

    engine = RAGEngine()
    return engine


@router.post('/upload')
async def upload_document(file: UploadFile = File(...)):
    rag_engine = get_engine()
    if not file.filename:
        raise HTTPException(status_code=400, detail='File field is required.')

    uploads_dir = os.path.abspath('documents')
    os.makedirs(uploads_dir, exist_ok=True)
    target_path = os.path.join(uploads_dir, file.filename)

    try:
        contents = await file.read()
        with open(target_path, 'wb') as buffer:
            buffer.write(contents)
    except Exception as error:
        raise HTTPException(status_code=500, detail=f'Upload failed: {error}')
    finally:
        await file.close()

    count = rag_engine.ingest_documents([target_path])
    return {'filename': file.filename, 'chunks_indexed': count, 'status': 'uploaded'}


@router.post('/query')
def query_ai(request: AIQueryRequest):
    rag_engine = get_engine()
    if not request.question.strip():
        raise HTTPException(status_code=400, detail='Question text is required.')

    cache_key = f'ai_response:{request.question.strip().lower()}:{request.top_k}'
    cached = cache.get(cache_key)
    if cached:
        return json.loads(cached)

    result = rag_engine.query(request.question, top_k=request.top_k)
    cache.set(cache_key, json.dumps(result), expire=600)
    return result


@router.get('/status')
def ai_status():
    try:
        rag_engine = get_engine()
    except HTTPException as exc:
        return {'status': 'unavailable', 'detail': exc.detail, 'source_count': 0}

    return {'status': 'ready', 'source_count': len(rag_engine.vector_db.metadata)}
