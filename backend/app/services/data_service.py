import os
from datetime import datetime, timezone
from threading import Lock
from typing import Any, Dict, Optional, Tuple

import pandas as pd
from fastapi import HTTPException, status

from app.database.config import DATA_DIR

DATASETS = {
    'patients': 'patients.csv',
    'trials': 'clinical_trials.csv',
    'sales': 'pharma_sales.csv',
    'doctors': 'doctors.csv',
}

# Cache keyed by file modification time: editing or replacing a CSV is picked up on
# the next request, without restarting the API.
_cache: Dict[str, Tuple[float, pd.DataFrame]] = {}
_lock = Lock()


def dataset_path(dataset: str):
    return DATA_DIR / DATASETS[dataset]


def load_dataset(dataset: str) -> pd.DataFrame:
    path = dataset_path(dataset)
    if not path.exists():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f'Dataset not found: {DATASETS[dataset]}'
        )
    mtime = os.path.getmtime(path)
    with _lock:
        cached = _cache.get(dataset)
        if cached is None or cached[0] != mtime:
            _cache[dataset] = (mtime, pd.read_csv(path))
        return _cache[dataset][1].copy()


def datasets_last_updated() -> str:
    mtimes = [os.path.getmtime(dataset_path(name)) for name in DATASETS if dataset_path(name).exists()]
    if not mtimes:
        return ''
    return datetime.fromtimestamp(max(mtimes), tz=timezone.utc).isoformat(timespec='seconds')


def get_records(
    dataset: str,
    limit: int,
    offset: int,
    filters: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    df = load_dataset(dataset)
    for column, value in (filters or {}).items():
        if value is not None:
            df = df[df[column].astype(str).str.lower() == value.lower()]
    page = df.iloc[offset:offset + limit]
    return {'total': int(len(df)), 'limit': limit, 'offset': offset, 'items': page.to_dict(orient='records')}
