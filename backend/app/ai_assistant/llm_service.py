import os
import re
import time
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from app.utils.logger import logger

COOLDOWN_SECONDS = 600
KNOWN_PROVIDERS = {
    'localhost:11434': 'Ollama (local)',
    '127.0.0.1:11434': 'Ollama (local)',
    'api.groq.com': 'Groq',
    'generativelanguage.googleapis.com': 'Google Gemini',
    'openrouter.ai': 'OpenRouter',
    'api.openai.com': 'OpenAI',
}
SYSTEM_PROMPT = (
    'You are PharmaIQ, a pharmaceutical analytics assistant. Answer using only the computed facts and '
    'document passages provided. Keep every number exactly as given. Be concise. If the facts do not '
    'answer the question, say so in one sentence and suggest which dataset question would help.'
)


class LLMService:
    """Optional language-model layer for any OpenAI-compatible API (OpenAI, Ollama, Groq, Gemini, OpenRouter).

    Configure with LLM_BASE_URL, LLM_API_KEY and LLM_MODEL (OPENAI_API_KEY / OPENAI_MODEL still work).
    The assistant never depends on it: answers are computed from the datasets and documents first.
    After a failure the model is skipped, so questions never wait on a request that will fail.
    """

    def __init__(self):
        self.base_url = os.getenv('LLM_BASE_URL') or None
        self.api_key = os.getenv('LLM_API_KEY') or os.getenv('OPENAI_API_KEY', '')
        if self.base_url and not self.api_key:
            self.api_key = 'not-needed'  # local servers such as Ollama ignore the key
        self.model = os.getenv('LLM_MODEL') or os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        self.timeout = float(os.getenv('LLM_TIMEOUT', '60'))
        host = urlparse(self.base_url).netloc if self.base_url else 'api.openai.com'
        self.provider = KNOWN_PROVIDERS.get(host, host)
        self._disabled_until = 0.0
        self.last_error: Optional[str] = None

    @property
    def configured(self) -> bool:
        return bool(self.api_key) and 'your_openai' not in self.api_key

    def available(self) -> bool:
        return self.configured and time.time() >= self._disabled_until

    def status(self) -> Dict[str, Any]:
        if not self.configured:
            state = 'not configured'
        elif not self.available():
            state = 'unavailable'
        else:
            state = 'ready'
        return {'provider': self.provider, 'model': self.model, 'state': state, 'last_error': self.last_error}

    def compose(self, question: str, facts: str, passages: List[str]) -> Optional[str]:
        if not self.available():
            return None
        context = facts + ('\n\nDocument passages:\n' + '\n---\n'.join(passages[:3]) if passages else '')
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key, base_url=self.base_url, timeout=self.timeout, max_retries=0)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': SYSTEM_PROMPT},
                    {'role': 'user', 'content': f'Question: {question}\n\nComputed facts:\n{context}'},
                ],
                max_tokens=300,
                temperature=0.2,
            )
            self.last_error = None
            return (response.choices[0].message.content or '').strip() or None
        except Exception as error:  # rate limit, auth, network, server down: fall back to the computed answer
            message = re.sub(r'(sk|gsk|AIza)[\w*-]+', '<redacted key>', str(error))[:120]
            self.last_error = f'{type(error).__name__}: {message}'
            # No credits or a bad key will not fix itself: stop trying until the API restarts.
            permanent = type(error).__name__ == 'AuthenticationError' or 'insufficient_quota' in str(error) \
                or 'no credits' in str(error).lower()
            self._disabled_until = float('inf') if permanent else time.time() + COOLDOWN_SECONDS
            logger.warning('%s unavailable, using computed answers: %s', self.provider, self.last_error)
            return None
