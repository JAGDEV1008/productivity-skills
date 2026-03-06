# Project Roadmap

## Vision

Maintain a focused set of reusable productivity skills with clear naming, deterministic workflows, and direct standalone install surfaces.

## Product principles

- Keep skill names clear, stable, and domain-grouped.
- Keep workflow instructions deterministic and safety-forward.
- Keep docs and metadata synchronized with the active skill set.

## Milestone Progress

- [x] Milestone 0: Naming and structural refactor (completed)
- [x] Milestone 1: Docs skill consolidation and canonical maintenance entrypoints (completed)
- [x] Milestone 2: Validation hardening and maintainer-doc cleanup (completed)
- [x] Milestone 3: Standalone top-level skill recentering (completed)

## Milestone 0: Naming and structural refactor

Scope:

- Rename skills to the current domain-grouped naming standard.
- Remove deprecated skill directories from active inventory.

Tickets:

- [x] Rename roadmap skill to `project-roadmap-maintainer`.
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
- [x] Keep `project-roadmap-maintainer` as a deprecation-cycle compatibility shim.

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

## Risks and mitigations

- Risk: Users still invoke deprecated names.
  Mitigation: keep migration table in README and clear install examples.
- Risk: Consolidated docs skill loses specificity.
  Mitigation: enforce explicit mode selection in `project-docs-maintainer`.

## Backlog candidates

- Add lightweight validation tooling for SKILL/frontmatter/openai.yaml alignment.
- Add validation checks for README layout and skill inventory consistency.
