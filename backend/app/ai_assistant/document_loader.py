import os
from pathlib import Path
from typing import List, Dict

import pandas as pd
from PyPDF2 import PdfReader


def load_text_from_pdf(path: str) -> str:
    text_chunks = []
    reader = PdfReader(path)
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text_chunks.append(content)
    return "\n".join(text_chunks)


def load_text_from_csv(path: str) -> str:
    df = pd.read_csv(path)
    return df.astype(str).apply(lambda row: " ".join(row.values), axis=1).str.cat(sep="\n")


def load_text_from_txt(path: str) -> str:
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()


def load_document_texts(path: str) -> List[Dict[str, str]]:
    path_obj = Path(path)
    if not path_obj.exists():
        return []

    loader = None
    if path_obj.suffix.lower() == '.pdf':
        loader = load_text_from_pdf
    elif path_obj.suffix.lower() == '.csv':
        loader = load_text_from_csv
    elif path_obj.suffix.lower() == '.txt':
        loader = load_text_from_txt

    if loader is None:
        return []

    text = loader(str(path_obj))
    if not text:
        return []

    chunks = chunk_text(text)
    return [{"text": chunk, "source": str(path_obj)} for chunk in chunks]


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    tokens = text.split()
    chunks = []
    start = 0
    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        chunks.append(" ".join(tokens[start:end]))
        start += chunk_size - overlap
    return chunks
