"""Cognitive Gate —— 大模型前的编译层 / 后的审计层（最小可运行参考实现）。

设计哲学：模型是引擎，控制层是方向盘和刹车。本仓库提供控制层，
可插拔任意大模型（默认 MockGrok，可换 xAI Grok）。
"""

from .audit_layer import AuditLayer, AuditResult
from .compile_layer import CompileLayer, CognitiveRequest
from .constraint_store import ConstraintStore, Constraint
from .model_adapter import BaseModel, MockGrok, GrokAdapter, get_model
from .p1_classifier import P1Classifier, P1Routing
from .protocol import CognitiveGateProtocol, DecisionRecord

__all__ = [
    "AuditLayer", "AuditResult",
    "CompileLayer", "CognitiveRequest",
    "ConstraintStore", "Constraint",
    "BaseModel", "MockGrok", "GrokAdapter", "get_model",
    "P1Classifier", "P1Routing",
    "CognitiveGateProtocol", "DecisionRecord",
]

__version__ = "0.1.0"
