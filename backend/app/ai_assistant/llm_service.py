import os
from typing import List

OPENAI_AVAILABLE = False
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    openai = None


class LLMService:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if OPENAI_AVAILABLE and self.api_key:
            openai.api_key = self.api_key
        self.use_openai = OPENAI_AVAILABLE and bool(self.api_key)

    def generate_answer(self, question: str, contexts: List[str]) -> str:
        prompt = self._build_prompt(question, contexts)
        if self.use_openai:
            try:
                response = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages=[
                        {'role': 'system', 'content': 'You are a pharmaceutical analytics assistant.'},
                        {'role': 'user', 'content': prompt}
                    ],
                    max_tokens=250,
                    temperature=0.2
                )
                return response.choices[0].message.content.strip()
            except Exception:
                return self._fallback_answer(question, contexts)
        return self._fallback_answer(question, contexts)

    def _build_prompt(self, question: str, contexts: List[str]) -> str:
        context_text = '\n\n'.join(contexts[:3])
        return f"Answer the following question based on the context below:\n\n{context_text}\n\nQuestion: {question}\n\nProvide a concise business-level answer."

    def _fallback_answer(self, question: str, contexts: List[str]) -> str:
        if not contexts:
            return 'No document context available to answer this question. Upload relevant documents first.'
        summary = ' '.join(contexts[:2])
        return f"Question: {question}\nSummary: {summary[:500]}"
