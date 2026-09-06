"""Audit model output against active or locked user constraints.

重要诚实声明：
  对 LLM 输出的约束合规审计，目前是 **best-effort 护栏**，不是数学保证。
  LLM 输出的语义合规是开放问题；本层用可解释的规则 + 可插拔的模型自检
  来做"最大努力拦截"，并明确标注 intercept 是概率性的、补充性的。
  它解决的是【可控性 / 可审计性 / 一致性】，不是【生存性安全】。
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Optional

from .constraint_store import ConstraintStore


@dataclass
class AuditResult:
    passed: bool
    blocked_reason: Optional[str] = None
    checks: list[dict] = field(default_factory=list)
    confidence: float = 1.0  # 本次审计本身的置信度（诚实标注不确定性）

    def to_dict(self) -> dict:
        return asdict(self)


class AuditLayer:
    def __init__(self, store: ConstraintStore):
        self.store = store

    def audit(self, model_output: str, request_constraints: list[str] | None = None) -> AuditResult:
        """检查模型输出是否违反：(a) 本次请求约束 (b) 跨任务生效约束 (c) 已锁定约束。"""
        out = (model_output or "").lower()
        checks: list[dict] = []
        violations: list[str] = []

        # (a)(b) 合并：本次约束 + 跨任务生效约束（去重，避免重复拦截提示）
        active = self.store.active_constraints()
        active_texts = [c.text for c in active]
        seen: set[str] = set()
        watch: list[str] = []
        for c in (request_constraints or []) + active_texts:
            if c not in seen:
                seen.add(c)
                watch.append(c)

        for c in watch:
            triggered = self._matches_violation(out, c)
            checks.append({"constraint": c, "violated": triggered})
            if triggered:
                violations.append(c)

        # (c) 锁定约束：即使未在本次请求中显式提及，也必须拦截
        for c in self.store.locked_constraints():
            if self._matches_violation(out, c.text):
                checks.append({"constraint": f"[LOCKED] {c.text}", "violated": True})
                violations.append(f"[已永久锁定] {c.text}")

        passed = len(violations) == 0
        reason = None
        if not passed:
            reason = "输出违反以下约束：" + "；".join(violations)
        # 诚实标注：规则匹配只能覆盖显式约束，无法保证隐含语义合规
        confidence = 0.9 if passed else 0.95
        return AuditResult(passed=passed, blocked_reason=reason, checks=checks, confidence=confidence)

    @staticmethod
    def _matches_violation(output: str, constraint: str) -> bool:
        """最小violation探测器：约束文本里抽取出被禁止/被要求的宾语，看输出是否违反它。

        例：
          约束"禁止：红色方案" → 检测输出是否出现"红色方案"（出现即违规）。
          约束"Forbidden: the red approach" → 检测输出是否出现"the red approach"。
          正向约束"要求：使用蓝色方案" → 检测输出是否【未】出现"蓝色方案"（未满足即违规）。
        这是可解释、可审计的；生产环境应叠加语义级模型自检。
        匹配对中文 / 英文约束前缀都生效。
        """
        forbid_prefixes = ["禁止：", "Forbidden: "]
        require_prefixes = ["要求：使用", "要求：", "Required: use ", "Required: "]
        for p in forbid_prefixes:
            if p in constraint:
                obj = constraint.split(p, 1)[1].strip()
                return bool(obj) and obj.lower() in output
        for p in require_prefixes:
            if p in constraint:
                obj = constraint.split(p, 1)[1].strip()
                return bool(obj) and obj.lower() not in output
        return False
