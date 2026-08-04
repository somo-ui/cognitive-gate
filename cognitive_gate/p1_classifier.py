"""P1 任务分型器：在调用任何算力之前，判断"这件事值不值得、用哪类算力"。

对应马斯克的真实痛点：太空算力（轨道数据中心）极其昂贵，
不能像地面那样随意调用模型。需要一个"任务 → 算力"的路由层。

分型结果给出：
  tier        : P1(关键/值得上太空算力) / P2(标准地面) / P3(琐碎/本地即可)
  compute     : 预估算力需求等级
  cost_tier   : 成本等级
  route       : 建议路由（space / ground / local）
  worth_it    : 是否值得执行（低价值 + 高成本 → False）
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

# 触发"值得上太空算力"的信号：大规模、长周期、跨公司、关键基础设施
SPACE_SIGNALS = ["全球", "全公司", "数天", "数月", "模拟整个", "基础设施", "轨道", "星际", "亿级"]
# 触发"琐碎/本地即可"的信号
TRIVIAL_SIGNALS = ["你好", "讲个笑话", "翻译", "算一下", "今天", "天气", "帮我写一句话"]


@dataclass
class P1Routing:
    tier: str
    compute: str
    cost_tier: str
    route: str
    worth_it: bool
    reason: str

    def to_dict(self) -> dict:
        return asdict(self)


class P1Classifier:
    def classify(self, text: str, risk_level: str = "low") -> P1Routing:
        text = text or ""
        has_space = any(s in text for s in SPACE_SIGNALS)
        has_trivial = any(s in text for s in TRIVIAL_SIGNALS)

        if has_space:
            return P1Routing(
                tier="P1", compute="high", cost_tier="high",
                route="space", worth_it=True,
                reason="长周期/跨公司/基础设施级任务，匹配轨道数据中心的稀缺算力。",
            )
        if has_trivial:
            return P1Routing(
                tier="P3", compute="low", cost_tier="low",
                route="local", worth_it=True,
                reason="低价值短任务，本地轻量模型即可，不应占用地面/太空大模型算力。",
            )
        # 标准任务：地面推理
        compute = "high" if risk_level == "high" else "medium"
        return P1Routing(
            tier="P2", compute=compute, cost_tier="medium",
            route="ground", worth_it=True,
            reason="标准任务，由地面推理集群（如特斯拉 AI4 / xAI 地面节点）处理。",
        )
