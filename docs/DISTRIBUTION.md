# Distribution

Cognitive Gate should be easy to try from three public paths: GitHub, skill directories, and hosted demos.

## GitHub

Primary install command:

```bash
python3 -m pip install "git+https://github.com/somo-ui/cognitive-gate.git@v0.1.6"
```

Smoke test:

```bash
cognitive-gate --input "Tidy this room, but don't use the red approach"
```

Expected result: `final_action` should be blocked because the deterministic mock output violates the red constraint.

Use `docs/assets/social-preview.png` as the repository social preview image in GitHub settings.

## Skill directories

Use `skill/cognitive-gate/` as the public skill package. A good listing should include:

- Name: Cognitive Gate
- Summary: auditable AI constraints and local decision records
- Tags: `ai-agent-guardrails`, `ai-constraints`, `auditable-ai`, `model-agnostic`, `local-first`
- Install: GitHub pip command above
- Skill path: `skill/cognitive-gate/`
- Boundary: best-effort reference implementation, not a production security boundary

Do not introduce project-private roadmap names in public directory listings.

ClawHub publish command after logging in:

```bash
clawhub skill publish skill/cognitive-gate \
  --slug cognitive-gate \
  --name "Cognitive Gate" \
  --version 0.1.6 \
  --tags ai-agent-guardrails,ai-constraints,auditable-ai,model-agnostic,local-first \
  --changelog "Initial public skill listing for Cognitive Gate v0.1.6."
```

## Hosted demos

Use `spaces/` as the starter folder for a lightweight Hugging Face Spaces demo. The hosted demo should expose one input box and return:

- final action
- extracted constraints
- route
- blocked reason
- raw local audit record

The demo should not ask for provider API keys. Keep it deterministic so users can reproduce the README examples.
