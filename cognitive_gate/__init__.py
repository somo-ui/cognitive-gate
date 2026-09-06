"""Cognitive Gate: minimal compile, route, audit, and record reference.

The model is replaceable; the control layers remain inspectable and testable.
"""

from .audit_layer import AuditLayer, AuditResult
from .compile_layer import CompileLayer, CognitiveRequest
from .constraint_store import ConstraintStore, Constraint
from .model_adapter import BaseModel, GrokAdapter, MockGrok, MockModel, ProviderAdapter, get_model
from .p1_classifier import P1Classifier, P1Routing
from .protocol import CognitiveGateProtocol, DecisionRecord

__all__ = [
    "AuditLayer", "AuditResult",
    "CompileLayer", "CognitiveRequest",
    "ConstraintStore", "Constraint",
    "BaseModel", "MockModel", "ProviderAdapter", "MockGrok", "GrokAdapter", "get_model",
    "P1Classifier", "P1Routing",
    "CognitiveGateProtocol", "DecisionRecord",
]

__version__ = "0.1.4"
