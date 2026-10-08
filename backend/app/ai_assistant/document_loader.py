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
    # Keep column names next to values ("region: North") so rows stay meaningful once chunked.
    df = pd.read_csv(path)
    return df.astype(str).apply(
        lambda row: "; ".join(f"{column}: {value}" for column, value in row.items()) + ".", axis=1
    ).str.cat(sep="\n")


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
    """Chunks of about `chunk_size` words that keep line breaks (lists and Q&A layouts stay readable)."""
    lines = [" ".join(line.split()) for line in text.splitlines()]
    lines = [line for line in lines if line]
    chunks, start = [], 0
    while start < len(lines):
        words, end = 0, start
        while end < len(lines) and (words == 0 or words + len(lines[end].split()) <= chunk_size):
            words += len(lines[end].split())
            end += 1
        chunks.append("\n".join(lines[start:end]))
        if end >= len(lines):
            break
        # Step back over roughly `overlap` words of lines so context carries into the next chunk.
        back, carried = end, 0
        while back > start + 1 and carried < overlap:
            back -= 1
            carried += len(lines[back].split())
        start = back
    return chunks
