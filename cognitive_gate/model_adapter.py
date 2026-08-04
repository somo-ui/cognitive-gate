"""可插拔模型适配器。

默认提供一个 MockGrok，让整套系统在没有 API key 时也能端到端跑通、
3 分钟内验证。生产环境把它替换成真正的 xAI Grok 调用即可——
这正是"编译层在前、审计层在后"架构的价值：模型是可替换的引擎，
控制层（方向盘/刹车）保持不变。
"""

from __future__ import annotations

import os
from abc import ABC, abstractmethod


class BaseModel(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        ...


class MockGrok(BaseModel):
    """演示用：把 prompt 原样回声，并故意在部分场景里"犯错"以便演示审计拦截。"""

    def generate(self, prompt: str) -> str:
        # 演示副作用：如果 prompt 提到"红色方案"或 "red approach"，mock 故意
        # 产出包含它的输出，触发审计层拦截 —— 证明中英双语约束审计都能拦住违规。
        if "红色方案" in prompt:
            return "好的，我已按红色方案执行并完成整理。"
        if "red approach" in prompt.lower():
            return "Sure, I've executed it using the red approach."
        return f"[mock-grok] 已处理请求：{prompt}"


class GrokAdapter(BaseModel):
    """真实 xAI Grok 适配器骨架（需要 XAI_API_KEY）。

    接口已对齐，仅留 TODO：实际请求 https://api.x.ai/v1 即可。
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("XAI_API_KEY")

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("未配置 XAI_API_KEY，请使用 MockGrok 或设置环境变量。")
        # TODO: 调用 xAI Grok 接口并返回文本
        raise NotImplementedError("GrokAdapter 的真实网络调用待接入；架构已预留。")


def get_model() -> BaseModel:
    """工厂：有 key 用真模型，没有用 mock —— 保证零配置可跑。"""
    if os.environ.get("XAI_API_KEY"):
        return GrokAdapter()
    return MockGrok()
