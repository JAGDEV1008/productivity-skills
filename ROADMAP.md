# Project Roadmap

## Vision

Maintain a focused set of reusable productivity skills with clear naming, deterministic workflows, direct standalone install surfaces, and cross-cutting speech output where audio delivery improves productivity.

## Product principles

- Keep skill names clear, stable, and domain-grouped.
- Keep workflow instructions deterministic and safety-forward.
- Keep docs and metadata synchronized with the active skill set.

## Milestone Progress

- [x] Milestone 0: Naming and structural refactor (completed)
- [x] Milestone 1: Docs skill consolidation and canonical maintenance entrypoints (completed)
- [x] Milestone 2: Validation hardening and maintainer-doc cleanup (completed)
- [x] Milestone 3: Standalone top-level skill recentering (completed)
- [x] Milestone 4: Speech workflow expansion (completed)

## Milestone 0: Naming and structural refactor

Scope:

- Rename skills to the current domain-grouped naming standard.
- Remove deprecated skill directories from active inventory.

Tickets:

- [x] Establish roadmap maintenance under a domain-grouped skill surface.
- [x] Rename workspace cleanup skill to `project-workspace-cleaner`.
- [x] Rename Things reminder skill to `things-reminders-manager`.
- [x] Rename Things digest skill to `things-digest-generator`.

Exit criteria:

- [x] Active skill folder names and frontmatter names match.
- [x] Deprecated names are absent from active invocation references.

## Milestone 1: Docs consolidation and canonical entrypoints

Scope:

- Consolidate docs maintenance skills into a single maintained entrypoint.
- Keep installation and invocation centered on canonical standalone skills.

Tickets:

- [x] Merge prior docs-maintenance skills into `project-docs-maintainer`.
- [x] Preserve both audit modes in the merged docs skill.
- [x] Keep roadmap maintenance under `project-docs-maintainer` through explicit modes.

Exit criteria:

- [x] Docs maintenance behavior remains available via explicit modes.
- [x] Canonical skills are directly installable and independently understandable.

## Milestone 2: Validation hardening and maintainer-doc cleanup

Scope:

- Validate metadata and reference consistency after refactor.
- Reduce repo-maintainer docs to the durable operating set.

Tickets:

- [x] Run stale-name sweeps and reference-integrity checks.
- [x] Validate each skill `agents/openai.yaml` against current SKILL intent.
- [x] Reduce maintainer docs to `AGENTS.md`, `docs/maintainers/reality-audit.md`, and `docs/maintainers/workflow-atlas.md`.
- [x] Consolidate roadmap handling under `project-docs-maintainer` with `mode=roadmap_maintenance`.
- [x] Keep roadmap guidance centered on the canonical docs-maintainer surface.

Exit criteria:

- [x] No stale skill names remain outside explicit compatibility or migration notes.
- [x] Maintainer guidance is reduced to the durable operating set.
- [x] Canonical roadmap ownership is documented under `project-docs-maintainer`.

## Milestone 3: Standalone top-level skill recentering

Scope:

- Remove the repo-level routing surface.
- Recenter docs and install guidance on direct skill invocation.

Tickets:

- [x] Remove the retired routing skill from the active inventory.
- [x] Rewrite public install guidance around standalone top-level skills.
- [x] Remove router-specific maintainer workflow documentation.

Exit criteria:

- [x] Active repo docs present only standalone skill entrypoints.
- [x] Maintainer docs describe the current post-router skill inventory.
- [x] Roadmap maintenance is presented only through the canonical docs-maintainer entrypoint.

## Milestone 4: Speech workflow expansion

Scope:

- Add a canonical speech workflow that fits the repo's standalone skill model.
- Keep repo messaging centered on productivity workflows while broadening the inventory to include audio-output use cases.

Tickets:

- [x] Migrate `speak-with-profile` into this repository as a standalone top-level skill.
- [x] Reframe the moved skill around narrated notes, spoken drafts, audio summaries, and hands-free review.
- [x] Keep profile-based accessibility options and disclosure policy as part of the canonical speech workflow.
- [x] Update public install guidance and repo inventory to include the new speech skill.

Exit criteria:

- [x] `speak-with-profile` is listed alongside the other standalone skills in repo docs.
- [x] The moved skill metadata and runtime docs describe a productivity-first speech workflow.
- [x] Repo-level docs no longer imply that productivity workflows exclude speech-output tasks.

## Risks and mitigations

- Risk: Users still invoke deprecated names.
  Mitigation: keep canonical usage guidance explicit in repo docs and skill prompts.
- Risk: Consolidated docs skill loses specificity.
  Mitigation: enforce explicit mode selection in `project-docs-maintainer`.

## Backlog candidates

- Add lightweight validation tooling for SKILL/frontmatter/openai.yaml alignment.
- Add validation checks for README layout and skill inventory consistency.
