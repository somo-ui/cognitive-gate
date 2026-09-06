"""Pluggable model adapters.

The default mock model keeps the whole repository runnable without API keys.
Production adapters can replace the mock model while keeping the compile,
route, audit, and record layers stable.
"""

from __future__ import annotations

import os
from abc import ABC, abstractmethod


class BaseModel(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        ...


class MockModel(BaseModel):
    """Demo model: echoes the prompt and intentionally violates red constraints."""

    def generate(self, prompt: str) -> str:
        # If the prompt contains a red constraint, the mock intentionally emits
        # a red output so the audit layer has a deterministic violation to catch.
        if "红色方案" in prompt:
            return "好的，我已按红色方案执行并完成整理。"
        if "red approach" in prompt.lower():
            return "Sure, I've executed it using the red approach."
        return f"[mock-model] 已处理请求：{prompt}"


class ProviderAdapter(BaseModel):
    """Example provider adapter skeleton. Requires COGNITIVE_GATE_API_KEY if used."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("COGNITIVE_GATE_API_KEY")

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("未配置 COGNITIVE_GATE_API_KEY，请使用 MockModel 或设置环境变量。")
        # TODO: call the provider API and return text.
        raise NotImplementedError("Provider adapter network call is not implemented.")


MockGrok = MockModel
GrokAdapter = ProviderAdapter


def get_model() -> BaseModel:
    """Factory: use an example provider adapter when configured, else mock."""
    if os.environ.get("COGNITIVE_GATE_API_KEY"):
        return ProviderAdapter()
    return MockModel()
