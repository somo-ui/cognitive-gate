# Roadmap

Cognitive Gate is the early public reference for ORIGIN. Its near-term purpose is not to claim a complete safety product, but to make the core idea installable, inspectable, and testable: user boundaries should become deterministic control checks around probabilistic AI output.

## Current release: v0.1.1

- Installable Python package with `cognitive-gate` CLI.
- Local-only demo with no required API key.
- Constraint persistence through JSON.
- Mock model adapter for deterministic testing.
- Unit tests covering the early gate behavior.

## Next milestones

### v0.1.x: Public reference quality

- Keep install, tests, and demo stable across supported Python versions.
- Improve bilingual examples for Chinese and English user constraints.
- Add clearer decision records that show why a request was allowed or blocked.
- Keep README, issue templates, and contribution flow easy for first-time reviewers.

### v0.2.x: ORIGIN alignment

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

- It is not the full modern ORIGIN safety core.
- It is not an operating-system sandbox.
- It is not a mathematical guarantee that any LLM output is safe.
- It should not be marketed as a production security boundary without independent audit.

## What would make it useful to others

- Reproducible failure cases.
- Simple examples of user boundary capture.
- Comparisons with other agent guardrail and governance projects.
- Tests showing where best-effort model checks fail.
