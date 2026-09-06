"""Cross-session constraint example.

Run from the repository root:
    python examples/02_cross_session_constraint.py
"""

import os
import tempfile

from cognitive_gate import CognitiveGateProtocol, ConstraintStore


tmpdir = tempfile.mkdtemp()
store_path = os.path.join(tmpdir, "constraints.json")

first_gate = CognitiveGateProtocol(store=ConstraintStore(store_path))
first_record = first_gate.decide("帮我整理房间，但别用红色方案")
constraint_key = first_record.cognitive_request["constraint_keys"][0]
constraint_text = first_record.cognitive_request["constraints"][0]

for _ in range(3):
    first_gate.reject_constraint(constraint_key, constraint_text)

second_gate = CognitiveGateProtocol(store=ConstraintStore(store_path))
second_record = second_gate.decide("再整理一次，用红色方案")

print("store_path:", store_path)
print("locked_constraint:", constraint_key)
print("final_action:", second_record.final_action)
print("blocked_reason:", second_record.audit.get("blocked_reason"))
