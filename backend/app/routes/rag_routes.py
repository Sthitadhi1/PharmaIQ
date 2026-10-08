from typing import List

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel, Field

from app.ai_assistant.chat_controller import get_engine
from app.utils.uploads import save_upload

router = APIRouter(prefix='/api/rag', tags=['RAG'])


class RAGQueryRequest(BaseModel):
    question: str = Field(..., max_length=2000)
    top_k: int = Field(3, ge=1, le=10)


@router.post('/ingest')
async def ingest_rag_documents(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail='At least one file is required.')

    saved_paths = [await save_upload(upload_file) for upload_file in files]
    rag_engine = get_engine()
    chunks_indexed = rag_engine.ingest_documents(saved_paths)
    return {'chunks_indexed': chunks_indexed, 'status': 'uploaded'}


@router.post('/query')
def query_rag_documents(request: RAGQueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail='Question text is required.')

    rag_engine = get_engine()
    return rag_engine.query(request.question, top_k=request.top_k)


@router.get('/status')
def rag_status():
    return {'status': 'ready'}
