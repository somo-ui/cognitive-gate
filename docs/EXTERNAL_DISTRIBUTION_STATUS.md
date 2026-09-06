# External distribution status

Snapshot captured on 2026-09-07 Asia/Shanghai.

## GitHub social preview

Status: prepared, manual upload required.

GitHub documents social preview upload through repository Settings -> Social preview. No public REST or GraphQL API is available for this setting, so the prepared image must be uploaded through the GitHub web UI.

Prepared asset:

```text
docs/assets/social-preview.png
```

Recommended manual action:

1. Open `https://github.com/somo-ui/cognitive-gate/settings`.
2. Find `Social preview`.
3. Upload `docs/assets/social-preview.png`.
4. Save and verify the preview renders.

## Hugging Face Space

Status: prepared, blocked by missing Hugging Face token.

The Space starter exists under:

```text
spaces/
```

Hugging Face's API supports creating Spaces with `create_repo(..., repo_type="space", space_sdk="gradio")` and uploading a folder with `upload_folder(...)`, but the local environment has no Hugging Face token configured.

Verified blocker:

```text
LocalTokenNotFoundError: Token is required to call the /whoami-v2 endpoint
```

After login, publish with:

```bash
python3 -m pip install huggingface_hub
hf auth login
python3 - <<'PY'
from huggingface_hub import HfApi

repo_id = "somo-ui/cognitive-gate"
api = HfApi()
api.create_repo(repo_id=repo_id, repo_type="space", space_sdk="gradio", exist_ok=True)
api.upload_folder(repo_id=repo_id, repo_type="space", folder_path="spaces")
print(f"https://huggingface.co/spaces/{repo_id}")
PY
```

## ClawHub

Status: dry-run passed, publishing paused after user denied CLI authorization.

Prepared skill package:

```text
skill/cognitive-gate/
```

Verified dry-run:

```text
status: would-publish
slug: cognitive-gate
displayName: Cognitive Gate
version: 0.1.6
fileCount: 1
```

Latest CLI authorization result:

```text
Authorization denied by user.
Error: Authorization denied by user.
```

Publish only after the user explicitly chooses to authorize ClawHub CLI access:

```bash
npx -y clawhub@0.23.3 skill publish skill/cognitive-gate \
  --slug cognitive-gate \
  --name "Cognitive Gate" \
  --version 0.1.6 \
  --tags ai-agent-guardrails,ai-constraints,auditable-ai,model-agnostic,local-first \
  --topics ai-agent-guardrails,ai-constraints,auditable-ai,local-first,model-agnostic \
  --source-repo somo-ui/cognitive-gate \
  --source-commit "$(git rev-parse HEAD)" \
  --source-ref v0.1.6 \
  --source-path skill/cognitive-gate \
  --changelog "Initial public skill listing for Cognitive Gate v0.1.6."
```

## SkillHub

Status: prepared, submission route not verified.

The SkillHub site was reachable through search snippets, but direct fetches for the install page timed out in this environment. Use the same `skill/cognitive-gate/` package and listing text from `docs/DISTRIBUTION.md` once the submission route is available.

## Current priority

1. Manually upload GitHub social preview.
2. Log in to Hugging Face and publish the Space from `spaces/`.
3. Re-authorize ClawHub only if the user decides the registry listing is worth publishing now.
4. Recheck GitHub traffic and exact-name search after indexing.
