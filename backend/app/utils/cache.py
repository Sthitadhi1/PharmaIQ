import os
import hashlib
from typing import Any, Optional

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    redis = None
    REDIS_AVAILABLE = False


class RedisCache:
    def __init__(self):
        self.host = os.getenv('REDIS_HOST', 'localhost')
        self.port = int(os.getenv('REDIS_PORT', 6379))
        self.db = int(os.getenv('REDIS_DB', 0))
        self._client = None
        self._local_cache = {}
        if REDIS_AVAILABLE:
            try:
                self._client = redis.Redis(
                    host=self.host,
                    port=self.port,
                    db=self.db,
                    decode_responses=True,
                    socket_connect_timeout=0.2,
                    socket_timeout=0.2
                )
                self._client.ping()
            except Exception:
                self._client = None

    def _make_key(self, key: str) -> str:
        return hashlib.sha256(key.encode('utf-8')).hexdigest()

    def get(self, key: str) -> Optional[str]:
        hashed = self._make_key(key)
        if self._client is not None:
            return self._client.get(hashed)
        return self._local_cache.get(hashed)

    def set(self, key: str, value: Any, expire: int = 300):
        hashed = self._make_key(key)
        if self._client is not None:
            self._client.set(hashed, value, ex=expire)
        else:
            self._local_cache[hashed] = str(value)

    def clear(self, key: str):
        hashed = self._make_key(key)
        if self._client is not None:
            self._client.delete(hashed)
        else:
            self._local_cache.pop(hashed, None)
