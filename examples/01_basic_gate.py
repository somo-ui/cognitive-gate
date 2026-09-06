"""Basic Cognitive Gate example.

Run from the repository root:
    python examples/01_basic_gate.py
"""

from cognitive_gate import CognitiveGateProtocol, ConstraintStore


gate = CognitiveGateProtocol(store=ConstraintStore(":memory:"))
record = gate.decide("Tidy this room, but don't use the red approach")

print("final_action:", record.final_action)
print("constraints:", record.cognitive_request["constraints"])
print("blocked_reason:", record.audit.get("blocked_reason"))
