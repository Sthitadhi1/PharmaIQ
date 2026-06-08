import os
from typing import List, Dict


class DocumentProcessor:
    def extract_text(self, filepath: str) -> List[Dict[str, str]]:
        if not os.path.exists(filepath):
            return []

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            text = file.read()

        chunks = []
        for idx, block in enumerate(text.split('\n\n')):
            if block.strip():
                chunks.append({'source': f'{os.path.basename(filepath)}#{idx}', 'text': block.strip()})
        return chunks
