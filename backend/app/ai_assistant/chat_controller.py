import os
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, UploadFile, File, status
from pydantic import BaseModel, Field

from app.services.data_service import DATASETS, dataset_path, load_dataset
from app.utils.logger import logger
from app.utils.uploads import save_upload
from .analytics_agent import EXAMPLE_QUESTIONS, DatasetAnalyst
from .llm_service import LLMService

router = APIRouter(prefix='/api/ai', tags=['AI Assistant'])
analyst = DatasetAnalyst()
llm = LLMService()
engine = None


class AIQueryRequest(BaseModel):
    question: str = Field(..., max_length=2000)
    top_k: int = Field(3, ge=1, le=10)


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


def warm_up() -> None:
    """Load the embedding model and index the upload folder so the first question is fast."""
    try:
        rag_engine = get_engine()
        rag_engine.sync_upload_dir()
        rag_engine.embedder
        logger.info('AI assistant ready: %d document chunks indexed', len(rag_engine.vector_db.metadata))
    except Exception as error:
        logger.warning('AI assistant warm-up failed (it will retry on the first question): %s', error)


@router.post('/upload')
async def upload_document(file: UploadFile = File(...)):
    target_path = await save_upload(file)
    rag_engine = get_engine()
    count = rag_engine.ingest_documents([target_path])
    return {'filename': os.path.basename(target_path), 'chunks_indexed': count, 'status': 'uploaded'}


def _facts_text(result: Dict[str, Any]) -> str:
    text = result['answer']
    table = result.get('table')
    if table:
        text += '\n' + ' | '.join(table['columns'])
        text += ''.join('\n' + ' | '.join(str(cell) for cell in row) for row in table['rows'][:15])
    return text


def _dataset_context() -> str:
    """Columns plus key aggregates of every dataset, for questions the rule-based analyst did not match."""
    lines = []
    for key, file_name in DATASETS.items():
        if dataset_path(key).exists():
            df = load_dataset(key)
            lines.append(f'{file_name}: {len(df)} rows; columns: {", ".join(df.columns)}')
    for example in ('Give me a summary of the business', 'Which region generated maximum sales?',
                    'Which trial phase has the highest dropout rate?', 'High-risk share by age group',
                    'Which specialization has the highest doctor engagement?'):
        result = analyst.answer(example)
        if result:
            lines.append(_facts_text(result))
    return '\n'.join(lines)


@router.post('/query')
def query_ai(request: AIQueryRequest):
    # Validate before get_engine(): loading the engine can download an embedding model.
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail='Question text is required.')

    data_result = analyst.answer(question)
    passages: List[Dict[str, Any]] = []
    rag_engine = get_engine()
    if rag_engine.documents():
        passages = rag_engine.search(question, top_k=request.top_k)

    if data_result:
        answer, mode = data_result['answer'], 'dataset'
        sources = list(data_result['sources'])
    elif passages:
        answer, mode = rag_engine.extractive_answer(question, passages), 'documents'
        sources = []
    else:
        answer = ("I couldn't match that to the datasets or to any uploaded document. "
                  'Ask about sales, patients, clinical trials or doctors, or upload a PDF, TXT or CSV document first.')
        mode, sources = 'help', []
    sources += sorted({passage['source'] for passage in passages} - set(sources))

    if mode == 'help':
        # No rule matched: let the language model try, grounded in a summary of every dataset.
        phrased = llm.compose(question, _dataset_context(), [])
        if phrased:
            answer, mode = phrased, 'llm'
            sources = list(DATASETS.values())
    else:
        facts = _facts_text(data_result) if data_result else answer
        phrased = llm.compose(question, facts, [passage['text'] for passage in passages])
        if phrased:
            answer, mode = phrased, f'{mode}+llm'

    return {
        'question': question,
        'answer': answer,
        'mode': mode,
        'table': data_result.get('table') if data_result else None,
        'sources': sources,
        'passages': [{**passage, 'text': passage['text'][:400]} for passage in passages],
        'llm': llm.status(),
        'suggestions': EXAMPLE_QUESTIONS if mode == 'help' else [],
    }


@router.get('/status')
def ai_status():
    try:
        documents = get_engine().documents()
        state = 'ready'
    except HTTPException as exc:
        documents, state = [], f'unavailable: {exc.detail}'
    datasets = [
        {'name': file_name, 'rows': int(len(load_dataset(key)))}
        for key, file_name in DATASETS.items() if dataset_path(key).exists()
    ]
    return {
        'status': state,
        'datasets': datasets,
        'documents': documents,
        'source_count': sum(doc['chunks'] for doc in documents),
        'llm': llm.status(),
        'examples': EXAMPLE_QUESTIONS,
    }
