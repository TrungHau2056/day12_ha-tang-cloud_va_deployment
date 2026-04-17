"""Cost guard / budget protection.

Stores usage in Redis when available (stateless across instances). Falls back to memory.

All costs stored in micro-USD (1e-6 USD) to avoid float issues in Redis.
"""

from __future__ import annotations

import time

from fastapi import HTTPException


PRICE_PER_1K_INPUT_TOKENS = 0.00015
PRICE_PER_1K_OUTPUT_TOKENS = 0.0006


def estimate_cost_micro_usd(input_tokens: int, output_tokens: int) -> int:
    cost = (input_tokens / 1000) * PRICE_PER_1K_INPUT_TOKENS + (output_tokens / 1000) * PRICE_PER_1K_OUTPUT_TOKENS
    return int(round(cost * 1_000_000))


class CostGuard:
    def __init__(
        self,
        daily_budget_usd: float,
        redis_client=None,
        key_prefix: str = "cost",
    ):
        self.daily_budget_micro_usd = int(round(float(daily_budget_usd) * 1_000_000))
        self.redis = redis_client
        self.key_prefix = key_prefix

        self._day = time.strftime("%Y-%m-%d")
        self._daily_cost_micro_usd = 0

    def _day_key(self) -> str:
        return time.strftime("%Y-%m-%d")

    def check_available(self) -> None:
        if self.redis is not None:
            self._check_available_redis()
        else:
            self._check_available_memory()

    def record_usage(self, input_tokens: int, output_tokens: int) -> int:
        if self.redis is not None:
            return self._record_usage_redis(input_tokens, output_tokens)
        return self._record_usage_memory(input_tokens, output_tokens)

    def get_daily_cost_usd(self) -> float:
        if self.redis is not None:
            key = f"{self.key_prefix}:{self._day_key()}"
            val = self.redis.get(key)
            return (int(val) / 1_000_000) if val else 0.0
        self._rollover_if_needed()
        return self._daily_cost_micro_usd / 1_000_000

    def _rollover_if_needed(self) -> None:
        today = self._day_key()
        if today != self._day:
            self._day = today
            self._daily_cost_micro_usd = 0

    def _check_available_memory(self) -> None:
        self._rollover_if_needed()
        if self._daily_cost_micro_usd >= self.daily_budget_micro_usd:
            raise HTTPException(status_code=503, detail="Daily budget exhausted. Try tomorrow.")

    def _record_usage_memory(self, input_tokens: int, output_tokens: int) -> int:
        self._rollover_if_needed()
        delta = estimate_cost_micro_usd(input_tokens, output_tokens)
        self._daily_cost_micro_usd += delta
        return delta

    def _check_available_redis(self) -> None:
        key = f"{self.key_prefix}:{self._day_key()}"
        current = self.redis.get(key)
        current_micro = int(current) if current else 0
        if current_micro >= self.daily_budget_micro_usd:
            raise HTTPException(status_code=503, detail="Daily budget exhausted. Try tomorrow.")

    def _record_usage_redis(self, input_tokens: int, output_tokens: int) -> int:
        day = self._day_key()
        key = f"{self.key_prefix}:{day}"
        delta = estimate_cost_micro_usd(input_tokens, output_tokens)

        pipe = self.redis.pipeline()
        pipe.incrby(key, delta)
        pipe.ttl(key)
        new_val, ttl = pipe.execute()

        if ttl == -1:
            self.redis.expire(key, 60 * 60 * 48)

        return int(delta)
