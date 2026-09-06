# Publishing checklist

Use this checklist when turning a release into a public entry point.

## GitHub repository

- Confirm README first screen says what the project is, who it is for, and how to run it.
- Confirm install command points to the latest release tag.
- Confirm `CHANGELOG.md` includes the latest version.
- Confirm GitHub topics include category phrases, not only project-specific names.
- Upload `docs/assets/social-preview.png` in GitHub Settings -> Social preview.
- Confirm release notes are short and user-facing.

## Skill directories

- Use the standalone name: `Cognitive Gate`.
- Use the short summary: `Auditable AI constraints and local decision records.`
- Use tags: `ai-agent-guardrails`, `ai-constraints`, `auditable-ai`, `model-agnostic`, `local-first`.
- Link to the GitHub release, not a moving branch, when possible.
- State clearly that this is a best-effort reference implementation.

## Hosted demo

- Start from `spaces/`.
- Keep the demo deterministic and provider-key-free.
- Show final action, extracted constraints, route, blocked reason, and raw audit record.
- Link back to the GitHub release.

## Post-publish monitoring

- Record a baseline snapshot from `docs/OBSERVABILITY.md`.
- Check exact-name GitHub search first.
- Check category phrase search after indexing has had time to update.
- Watch referrers to decide which external channel is worth more work.

## Do not do yet

- Do not introduce private roadmap names into the public entry.
- Do not claim production security.
- Do not claim mathematical safety guarantees.
- Do not add real provider calls before the adapter boundary has separate tests.
