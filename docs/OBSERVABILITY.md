# Observability

Cognitive Gate should be judged by visible user behavior, not by whether the repository looks complete.

## Weekly metrics

Record these once a week after every public update:

| Signal | Why it matters | How to check |
|---|---|---|
| Stars | People understood enough to save it | GitHub repository header |
| Forks | People may try modifying or reusing it | GitHub repository header |
| Watchers | People want future updates | GitHub repository header |
| Views | The public entry is being seen | GitHub Insights -> Traffic |
| Unique visitors | Exposure is not only repeat self-visits | GitHub Insights -> Traffic |
| Clones | Users tried installing or inspecting locally | GitHub Insights -> Traffic |
| Referrers | Shows which channel is actually working | GitHub Insights -> Traffic |
| Search terms | Shows whether the wording matches real demand | Manual GitHub search |
| Release views/downloads | Shows whether versioned publishing helps | GitHub Releases |

## GitHub CLI checks

Repository state:

```bash
gh repo view somo-ui/cognitive-gate --json description,repositoryTopics,latestRelease,url
```

Traffic views:

```bash
gh api repos/somo-ui/cognitive-gate/traffic/views
```

Traffic clones:

```bash
gh api repos/somo-ui/cognitive-gate/traffic/clones
```

Top referrers:

```bash
gh api repos/somo-ui/cognitive-gate/traffic/popular/referrers
```

Top paths:

```bash
gh api repos/somo-ui/cognitive-gate/traffic/popular/paths
```

These APIs only return recent traffic windows. Keep dated snapshots in a private notes file if trend history matters.

## Manual search checks

Search GitHub while logged out or in a private browser window:

- `cognitive-gate`
- `"cognitive gate" ai`
- `ai agent guardrails constraints`
- `auditable ai constraints`
- `model agnostic audit ai`
- `cross session constraints ai`

Useful exposure means the repository appears for its exact name first, then gradually appears for category phrases.

## Baseline snapshot template

```markdown
## YYYY-MM-DD

- Version:
- Stars:
- Forks:
- Watchers:
- Views / uniques:
- Clones / uniques:
- Top referrers:
- Top paths:
- Search result notes:
- Next action:
```

## Current baseline

Snapshot captured on 2026-09-07 Asia/Shanghai through GitHub traffic APIs.

- Version: v0.1.5 candidate
- Views / uniques: 5 / 2
- Clones / uniques: 30 / 13
- Top referrer: `github.com` with 3 views and 1 unique visitor
- Top paths: `/somo-ui/cognitive-gate` and `/somo-ui/cognitive-gate/watchers`
- Interpretation: baseline traffic exists, but category-level public discovery is not proven yet.
- Next action: publish v0.1.5, upload the social preview image manually in GitHub settings, then recheck exact-name and category searches after indexing.

## Interpretation

Low traffic after a new release is normal. First optimize exact-name discovery, then category discovery, then external referrers.

Do not treat stars as the only success metric. For an installable reference project, clone attempts and referrers are often more useful than stars in the first stage.
