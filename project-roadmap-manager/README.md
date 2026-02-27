# Project Roadmap Manager Customization Guide

## What To Customize First

- Roadmap template sections and table columns in `SKILL.md`.
- Milestone naming style (`M1` vs `Phase 1` vs quarter-based labels).
- Status vocabulary (`Planned`, `In Progress`, `Completed`, `Blocked`, `De-scoped`).
- Change log detail level and plan history verbosity.
- Target version/date conventions (semantic versions, quarters, or calendar dates).

## Personalization Points

- Template shape and required sections
  - Default: skill creates/maintains `ROADMAP.md` with `Current Milestone`, `Milestones`, `Plan History`, and `Change Log`.
  - Why customize: teams often need owners, risk tracking, dependencies, or OKR fields.
  - Where to change: [`SKILL.md`](./SKILL.md) template and event handling rules.
- Milestone IDs and naming
  - Default: `M1` style IDs and semantic version examples like `v0.1.0`.
  - Why customize: some teams track by quarter (`2026-Q1`) or phase (`Phase 1`).
  - Where to change: [`SKILL.md`](./SKILL.md) template + rules under milestone updates.
- Status model
  - Default: planned set includes `Completed`, `In Progress`, `Blocked`, `De-scoped`, `Planned`.
  - Why customize: organizations may enforce a simpler or stricter status workflow.
  - Where to change: [`SKILL.md`](./SKILL.md) event handling rules.
- Change tracking granularity
  - Default: every mutation gets a dated `Change Log` note and accepted plans are captured in `Plan History`.
  - Why customize: reduce noise for fast-moving projects or increase audit detail for regulated teams.
  - Where to change: [`SKILL.md`](./SKILL.md) workflow and quality bar.

## Common Customization Profiles

- Lightweight solo roadmap
  - Keep the default structure, shorten `Plan History` entries, and keep only one active + one next milestone.
- Team delivery roadmap
  - Add owner and dependency columns, require explicit acceptance criteria and risk notes.
- Quarterly planning roadmap
  - Replace milestone IDs with quarter IDs and use quarter-based target dates.
- Compliance-heavy roadmap
  - Require dense `Change Log` entries including reason, owner, and rollout note.

## Example Prompts For Codex

### Adjust Defaults

- "Update this skill so new `ROADMAP.md` files include an `Owner` field in `Current Milestone`."
- "Change milestone IDs from `M1/M2` to `Phase 1/Phase 2` everywhere in the template and rules."

### Change Behavior

- "Make `Plan History` concise: only include scope and acceptance criteria, omit risks unless explicitly provided."
- "Require `Blocked` milestones to include a `Blocker` note in the `Milestones` table."

### Adapt For My Environment

- "Adapt this skill to a quarterly roadmap style (`YYYY-Qn`) with target quarter instead of target version."
- "Modify the roadmap conventions to match a startup release cadence with weekly milestone updates."

### Validate My Customization

- "Review `SKILL.md` and confirm there are no conflicting milestone statuses across sections."
- "Dry-run a sample `ROADMAP.md` output from this skill and verify it follows the customized status model."

## Validation Checklist

- Confirm the template in [`SKILL.md`](./SKILL.md) matches your desired roadmap sections.
- Confirm milestone ID examples reflect your preferred naming convention.
- Confirm status values are consistent across event rules and quality bar.
- Confirm `Plan History` and `Change Log` rules match your intended verbosity.
- Run a sample roadmap update request and verify generated `ROADMAP.md` structure.

## Notes And Compatibility

- This skill is documentation/rule driven and does not require platform-specific tooling.
- Customization is primarily in [`SKILL.md`](./SKILL.md); no script changes are required.
