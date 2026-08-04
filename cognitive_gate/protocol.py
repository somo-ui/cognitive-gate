"""统一 AI 决策审计协议（Cognitive Gate Protocol）。

这是跨所有公司（Tesla / xAI / SpaceX / X）的统一审计层：
无论 Grok 在哪家公司被调用，输出都经过同一套「编译 → 分型 → 生成 → 审计」。
它是一个**协议**，不是集成——可在任意调用点前置插入。

编排一次完整决策：
  1. 编译：人类指令 → CognitiveRequest（确定性结构）
  2. 分型：P1 路由（值不值得、用哪类算力）
  3. 生成：调用模型（默认 MockGrok，可换真 Grok）
  4. 审计：输出 vs 生效/锁定约束 → 通过或拦截
  5. 留痕：写出决策档案(decision record) + 追加决策病历(decision history)
"""

from __future__ import annotations

import json
import os
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone

from .audit_layer import AuditLayer, AuditResult
from .compile_layer import CompileLayer, CognitiveRequest
from .constraint_store import ConstraintStore
from .model_adapter import BaseModel, get_model
from .p1_classifier import P1Classifier, P1Routing


@dataclass
class DecisionRecord:
    request_id: str
    timestamp: str
    cognitive_request: dict
    p1_routing: dict
    model_output: str
    audit: dict
    final_action: str  # allow / blocked
    notes: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


class CognitiveGateProtocol:
    def __init__(self, store: ConstraintStore | None = None,
                 model: BaseModel | None = None,
                 history_path: str = "decision_history.jsonl"):
        self.store = store or ConstraintStore()
        self.compile = CompileLayer(self.store)
        self.p1 = P1Classifier()
        self.audit = AuditLayer(self.store)
        self.model = model or get_model()
        self.history_path = history_path

    def decide(self, user_text: str, *, model_input_override: str | None = None) -> DecisionRecord:
        req: CognitiveRequest = self.compile.compile(user_text)
        routing: P1Routing = self.p1.classify(user_text, req.risk_level)

        # 在调用算力之前先判断值不值得（P1 分型器的价值）
        if not routing.worth_it:
            rec = DecisionRecord(
                request_id=str(uuid.uuid4())[:8],
                timestamp=self._now(),
                cognitive_request=req.to_dict(),
                p1_routing=routing.to_dict(),
                model_output="",
                audit=AuditResult(passed=True, confidence=1.0).to_dict(),
                final_action="skipped",
                notes="P1 分型判定不值得调用大模型算力。",
            )
            self._append_history(rec)
            return rec

        # 调用模型（编译层已把模糊指令变成结构化请求喂给它）
        prompt = model_input_override or req.reconstructed_text or user_text
        output = self.model.generate(prompt)

        # 输出后审计
        result: AuditResult = self.audit.audit(output, req.constraints)
        final = "blocked" if not result.passed else "allow"

        rec = DecisionRecord(
            request_id=str(uuid.uuid4())[:8],
            timestamp=self._now(),
            cognitive_request=req.to_dict(),
            p1_routing=routing.to_dict(),
            model_output=output,
            audit=result.to_dict(),
            final_action=final,
            notes=result.blocked_reason or "通过审计。",
        )
        self._append_history(rec)
        return rec

    # 交互：用户拒绝某条约束建议
    def reject_constraint(self, key: str, text: str | None = None) -> dict:
        return self.store.reject(key, text)

    def _append_history(self, rec: DecisionRecord) -> None:
        """决策病历：追加式、不可变日志，每一笔决策都留痕可审计。"""
        with open(self.history_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec.to_dict(), ensure_ascii=False) + "\n")

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()
