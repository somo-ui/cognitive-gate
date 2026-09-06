# Roadmap

Cognitive Gate is a public reference implementation for auditable AI constraints. Its near-term purpose is to stay easy to install, easy to inspect, and honest about its current boundary: best-effort checks around model output.

## Current release: v0.1.2

- Installable Python package with `cognitive-gate` CLI.
- Local-only demo with no required API key.
- Constraint persistence through JSON.
- Mock model adapter for deterministic testing.
- Runnable examples for basic audit, cross-session constraints, and local records.
- Unit tests covering the early gate behavior.

## Next milestones

### v0.1.x: Public reference quality

- Keep install, tests, and demo stable across supported Python versions.
- Improve bilingual examples for Chinese and English user constraints.
- Add clearer decision records that show why a request was allowed or blocked.
- Keep README, issue templates, and contribution flow easy for first-time reviewers.

### v0.2.x: Constraint correctness

- Preserve the exact user-original text as the evidence anchor.
- Make normalized rules explicit and auditable.
- Add stronger input schema validation.
- Prove revoked rules cannot silently come back to life.
- Add fail-closed behavior for unreadable or unavailable rule storage.

### v0.3.x: Adapter boundary

- Keep the deterministic gate separate from model/provider adapters.
- Add dry-run adapters before any real provider call path.
- Record adapter decisions without leaking credentials or private prompts.

## Non-goals for this repository

- It is not an operating-system sandbox.
- It is not a mathematical guarantee that any LLM output is safe.
- It should not be marketed as a production security boundary without independent audit.

## What would make it useful to others

- Reproducible failure cases.
- Simple examples of user boundary capture.
- Comparisons with other agent guardrail and governance projects.
- Tests showing where best-effort model checks fail.
