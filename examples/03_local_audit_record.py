"""Local audit record example.

Run from the repository root:
    python examples/03_local_audit_record.py
"""

import os
import tempfile

from cognitive_gate import CognitiveGateProtocol, ConstraintStore


tmpdir = tempfile.mkdtemp()
history_path = os.path.join(tmpdir, "decision_history.jsonl")

gate = CognitiveGateProtocol(
    store=ConstraintStore(os.path.join(tmpdir, "constraints.json")),
    history_path=history_path,
)
record = gate.decide("Write a Python function to read a CSV file")

print("history_path:", history_path)
print("request_id:", record.request_id)
print("final_action:", record.final_action)

with open(history_path, "r", encoding="utf-8") as history_file:
    print("history_lines:", len(history_file.readlines()))
