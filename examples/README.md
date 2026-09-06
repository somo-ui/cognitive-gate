# Examples

Run these examples from the repository root after installing the package or from a local checkout.

```bash
python examples/01_basic_gate.py
python examples/02_cross_session_constraint.py
python examples/03_local_audit_record.py
```

## What each example shows

- `01_basic_gate.py`: English constraint extraction and output blocking.
- `02_cross_session_constraint.py`: local JSON constraint reuse across gate instances.
- `03_local_audit_record.py`: decision history written to a local JSONL file.

The examples use temporary files or in-memory stores, so they do not require provider accounts or external services.
