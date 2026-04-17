"""Rate limiting.

- Uses Redis when `REDIS_URL` is set (stateless across instances).
- Falls back to in-memory sliding window if Redis is unavailable.

Default algorithm for Redis: fixed window counter with TTL (60s).
"""

from __future__ import annotations

import time
from collections import defaultdict, deque

from fastapi import HTTPException


class RateLimiter:
    def __init__(
        self,
        max_requests: int,
        window_seconds: int = 60,
        redis_client=None,
        key_prefix: str = "rate",
    ):
        self.max_requests = int(max_requests)
        self.window_seconds = int(window_seconds)
        self.redis = redis_client
        self.key_prefix = key_prefix

        self._windows: dict[str, deque] = defaultdict(deque)

    def check(self, bucket: str) -> dict:
        if self.redis is not None:
            return self._check_redis(bucket)
        return self._check_memory(bucket)

    def _check_memory(self, bucket: str) -> dict:
        now = time.time()
        window = self._windows[bucket]
        while window and window[0] < now - self.window_seconds:
            window.popleft()

        reset_at = int(now) + self.window_seconds
        if len(window) >= self.max_requests:
            oldest = window[0]
            retry_after = int(oldest + self.window_seconds - now) + 1
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded: {self.max_requests} req/{self.window_seconds}s",
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Limit": str(self.max_requests),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(reset_at),
                },
            )

        window.append(now)
        remaining = max(0, self.max_requests - len(window))
        return {"limit": self.max_requests, "remaining": remaining, "reset_at": reset_at}

    def _check_redis(self, bucket: str) -> dict:
        now = int(time.time())
        window_id = now // self.window_seconds
        key = f"{self.key_prefix}:{bucket}:{window_id}"

        pipe = self.redis.pipeline()
        pipe.incr(key, amount=1)
        pipe.ttl(key)
        current, ttl = pipe.execute()

        if ttl == -1:
            self.redis.expire(key, self.window_seconds)
            ttl = self.window_seconds

        reset_at = now + max(0, int(ttl))
        remaining = max(0, self.max_requests - int(current))

        if int(current) > self.max_requests:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded: {self.max_requests} req/{self.window_seconds}s",
                headers={
                    "Retry-After": str(max(1, int(ttl))),
                    "X-RateLimit-Limit": str(self.max_requests),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(reset_at),
                },
            )

        return {"limit": self.max_requests, "remaining": remaining, "reset_at": reset_at}
