import time
from typing import Dict

class RateLimiter:
    def __init__(self, limit: int = 60, window_seconds: int = 60):
        self.limit = limit
        self.window_seconds = window_seconds
        self.access_log: Dict[str, list[float]] = {}

    def allow(self, key: str) -> bool:
        now = time.time()
        window_start = now - self.window_seconds
        entries = self.access_log.get(key, [])
        entries = [ts for ts in entries if ts > window_start]
        if len(entries) >= self.limit:
            self.access_log[key] = entries
            return False
        entries.append(now)
        self.access_log[key] = entries
        return True
