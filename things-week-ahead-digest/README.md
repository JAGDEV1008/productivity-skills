# Things Week Ahead Digest Customization Guide

## What To Customize First

- Due-soon horizon (`today + 3 days` / next 72h framing).
- Planning window (`--days-ahead`, default `4`).
- Scoring weights for activity ranking.
- Number of top projects/areas included in digest.
- Suggestion generation order and wording style.
- Output length target (default guidance ~220 words).

## Personalization Points

- Time windows
  - Default: due-soon is `<= today + 3d`; week/weekend section spans `today` to `today + 4d`.
  - Why customize: users may plan in rolling 7-day, workweek-only, or monthly windows.
  - Where to change: [`SKILL.md`](./SKILL.md), [`references/suggestion-rules.md`](./references/suggestion-rules.md), and script arg `--days-ahead` in [`scripts/build_digest.py`](./scripts/build_digest.py).
- Scoring formula
  - Default: `completed_7d*3 + due_soon*2 + overdue*3 + min(open_count,10)*0.5 + checklist_hint*1.5`.
  - Why customize: different users prioritize momentum, risk, or workload differently.
  - Where to change: [`references/suggestion-rules.md`](./references/suggestion-rules.md) and `Activity.score` in [`scripts/build_digest.py`](./scripts/build_digest.py).
- Top-N inclusion rules
  - Default: top 3 projects and top 2 areas.
  - Why customize: some users prefer narrower focus or broader coverage.
  - Where to change: sorting/slicing logic in [`scripts/build_digest.py`](./scripts/build_digest.py).
- Output style constraints
  - Default: concise operational tone, fixed section order, and short digest format.
  - Why customize: some users want executive summary first or more detailed planning context.
  - Where to change: [`references/output-format.md`](./references/output-format.md), [`SKILL.md`](./SKILL.md), and `render_digest` output composition.

## Common Customization Profiles

- Ultra-concise daily triage
  - Keep only top 1-2 projects, emphasize overdue items, and cap output aggressively.
- Weekly planner
  - Use a 7-day horizon and include more tasks in `Week/Weekend Ahead`.
- Momentum-first coaching
  - Weight recent completions higher than overdue risk.
- Risk-first operational mode
  - Weight overdue and near-due items higher; force triage suggestion first.

## Example Prompts For Codex

### Adjust Defaults

- "Change this digest skill to use a 7-day planning window by default."
- "Increase the top area count from 2 to 4 in the digest output."

### Change Behavior

- "Reweight scoring so overdue items count less and recent completions count more."
- "Make suggestion generation always include a Monday prep action when Monday is within the window."

### Adapt For My Environment

- "Adapt this skill for workweek planning only (Monday-Friday) and ignore weekend deadlines."
- "Customize the output format for an executive audience: summary first, then action bullets."

### Validate My Customization

- "Review `build_digest.py` and confirm my weight changes are applied consistently to projects and areas."
- "Generate a sample digest from JSON fixtures and verify section order and length constraints."

## Validation Checklist

- Run `build_digest.py` with representative JSON and confirm output section order.
- Confirm due-soon and horizon logic match your chosen planning cadence.
- Confirm top project/area counts match customized values.
- Confirm suggestion order and style constraints reflect your intended tone.
- Confirm the digest remains readable at your target length.

## Notes And Compatibility

- Integrates with Things MCP tool outputs; quality depends on task metadata completeness.
- Script uses `python3`; ensure Python is available in target environment.
