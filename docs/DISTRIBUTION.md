# Distribution

Cognitive Gate should be easy to try from three public paths: GitHub, skill directories, and hosted demos.

## GitHub

Primary install command:

```bash
python3 -m pip install "git+https://github.com/somo-ui/cognitive-gate.git@v0.1.4"
```

Smoke test:

```bash
cognitive-gate --input "Tidy this room, but don't use the red approach"
```

Expected result: `final_action` should be blocked because the deterministic mock output violates the red constraint.

Use `docs/assets/social-preview.png` as the repository social preview image in GitHub settings.

## Skill directories

Use the repository as a public reference entry before adding platform-specific packaging. A good listing should include:

- Name: Cognitive Gate
- Summary: auditable AI constraints and local decision records
- Tags: `ai-agent-guardrails`, `ai-constraints`, `auditable-ai`, `model-agnostic`, `local-first`
- Install: GitHub pip command above
- Boundary: best-effort reference implementation, not a production security boundary

Do not introduce project-private roadmap names in public directory listings.

## Hosted demos

Use `spaces/` as the starter folder for a lightweight Hugging Face Spaces demo. The hosted demo should expose one input box and return:

- final action
- extracted constraints
- route
- blocked reason
- raw local audit record

The demo should not ask for provider API keys. Keep it deterministic so users can reproduce the README examples.
