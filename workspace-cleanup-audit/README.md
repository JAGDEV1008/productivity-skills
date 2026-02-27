# Workspace Cleanup Audit Customization Guide

## What To Customize First

- Workspace root (`--workspace`, default `~/Workspace`).
- Noise floor (`--min-mb`, default `50`).
- Staleness threshold (`--stale-days`, default `90`).
- Result cap (`--max-findings`, default `200`).
- Directory/file pattern rules and category weights in the scanner script.
- Severity scoring boundaries.

## Personalization Points

- Workspace scope
  - Default: scans repositories under `~/Workspace`.
  - Why customize: users often keep repos elsewhere or want a narrower scan target.
  - Where to change: CLI flag in [`scripts/scan_workspace_cleanup.py`](./scripts/scan_workspace_cleanup.py) or `SKILL.md` examples.
- Threshold tuning
  - Default: `--min-mb 50`, `--stale-days 90`, `--max-findings 200`.
  - Why customize: large monorepos may need higher thresholds to reduce noise.
  - Where to change: script defaults in [`scripts/scan_workspace_cleanup.py`](./scripts/scan_workspace_cleanup.py).
- Pattern coverage
  - Default: predefined build/dependency/cache directories and transient/archive file extensions.
  - Why customize: different stacks (Rust/Go/Java/mobile) generate different artifact patterns.
  - Where to change: `DIR_RULES`, `FILE_EXT_RULES` in [`scripts/scan_workspace_cleanup.py`](./scripts/scan_workspace_cleanup.py) and guidance in [`references/patterns.md`](./references/patterns.md).
- Scoring and severity
  - Default: size-based base score + category weight + age bonus; severity cutoffs at score 45/70/85.
  - Why customize: teams may prefer fewer critical alerts or stronger stale-artifact emphasis.
  - Where to change: `base_size_score`, `severity_from_score`, and weighting constants in [`scripts/scan_workspace_cleanup.py`](./scripts/scan_workspace_cleanup.py).

## Common Customization Profiles

- Strict hygiene
  - Lower `--min-mb`, lower stale days, and increase cache/dependency weights.
- Low-noise enterprise monorepo
  - Increase `--min-mb`, increase stale days, and limit findings to top high/critical.
- Language-specific tuning
  - Add stack-specific build/cache directories and extensions.
- Archive-sensitive cleanup
  - Increase archive weights and lower stale threshold for old compressed files.

## Example Prompts For Codex

### Adjust Defaults

- "Set this cleanup skill to default to `--min-mb 150` and `--stale-days 120`."
- "Change the default workspace from `~/Workspace` to `~/Code`."

### Change Behavior

- "Update severity scoring so anything under 500 MiB cannot be marked critical."
- "Reduce the weight of archive files and increase weight for stale dependency artifacts."

### Adapt For My Environment

- "Add Rust and Go artifact patterns (`.cargo`, `bin`, `pkg`, `coverage`) to the scanner rules."
- "Tune this skill for a pnpm monorepo and de-emphasize `node_modules` directories under package examples."

### Validate My Customization

- "Review `scan_workspace_cleanup.py` and confirm all new pattern rules are reachable and scored correctly."
- "Run a dry scan with JSON output and verify top findings align with my updated thresholds."

## Validation Checklist

- Run scanner with default flags and confirm expected workspace root.
- Run scanner with your tuned `--min-mb` and `--stale-days` and compare noise level.
- Confirm custom rules appear in findings (or intentionally do not).
- Confirm severity labels reflect your intended cutoff model.
- Confirm output still includes all required fields documented in [`SKILL.md`](./SKILL.md).

## Notes And Compatibility

- Skill is read-only by design; it should never delete or modify files.
- Script currently uses `python3`; ensure Python is available in the target environment.
