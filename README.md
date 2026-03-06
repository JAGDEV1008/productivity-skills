# productivity-skills

Curated Codex skills for productivity workflows, maintenance automation, and operational hygiene.

For standards and applicability guidance, see [AGENTS.md](./AGENTS.md).

## Table of Contents

- [What These Agent Skills Help With](#what-these-agent-skills-help-with)
- [Skill Guide (When To Use What)](#skill-guide-when-to-use-what)
- [Quick Start (Vercel Skills CLI)](#quick-start-vercel-skills-cli)
- [Install individually by Skill or Skill Pack](#install-individually-by-skill-or-skill-pack)
- [Update Skills](#update-skills)
- [More resources for similar Skills](#more-resources-for-similar-skills)
- [Repository Layout](#repository-layout)
- [Notes](#notes)
- [Keywords](#keywords)
- [License](#license)

## What These Agent Skills Help With

This repository packages reusable Codex skills for canonical docs maintenance, read-only workspace hygiene, and Things planning/reminder workflows.

## Skill Guide (When To Use What)

- `project-docs-maintainer`
  - Canonical maintainer for `*-skills` README drift and checklist roadmap maintenance through explicit modes.
- `project-workspace-cleaner`
  - Read-only workspace hygiene scanner that ranks cleanup chores.
- `things-reminders-manager`
  - Deterministic Things reminder create/update workflow with duplicate and date safeguards.
- `things-digest-generator`
  - Weekly Things digest generator with prioritized next-step suggestions.

Compatibility only:

- `project-roadmap-maintainer`
  - Thin redirect shim for legacy roadmap-maintainer prompts. Prefer `project-docs-maintainer` for all new work.

## Quick Start (Vercel Skills CLI)

Use the Vercel `skills` CLI to install from this repository.

```bash
# Install from this repository (interactive picker)
npx skills add gaelic-ghost/productivity-skills
```

Install all skills from this repository:

```bash
npx skills add gaelic-ghost/productivity-skills --all
```

## Install individually by Skill or Skill Pack

```bash
npx skills add gaelic-ghost/productivity-skills --skill project-docs-maintainer
npx skills add gaelic-ghost/productivity-skills --skill project-workspace-cleaner
npx skills add gaelic-ghost/productivity-skills --skill things-reminders-manager
npx skills add gaelic-ghost/productivity-skills --skill things-digest-generator
```

Compatibility note:

- Install `project-roadmap-maintainer` only when you must preserve a legacy prompt or install surface.

## Update Skills

```bash
npx skills check
npx skills update
```

## More resources for similar Skills

### Find Skills like these with the `skills` CLI by Vercel — [vercel-labs/skills](https://github.com/vercel-labs/skills)

```bash
npx skills find "skills readme maintenance"
npx skills find "workspace cleanup automation"
npx skills find "things productivity automation"
```

### Find Skills like these with the `Find Skills` Agent Skill by Vercel — [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)

```bash
# `Find Skills` is a part of Vercel's `agent-skills` repo
npx skills add vercel-labs/agent-skills --skill find-skills
```

Then ask your Agent for help finding a skill for "" or ""

### Leaderboard

- Skills catalog: [skills.sh](https://skills.sh/)

## Repository Layout

```text
.
├── README.md
├── AGENTS.md
├── docs/
│   └── maintainers/
├── project-docs-maintainer/
├── project-roadmap-maintainer/
├── project-workspace-cleaner/
├── things-digest-generator/
└── things-reminders-manager/
```

## Notes

- Install and use skills individually; do not assume access to repo-level maintainer docs.
- Prefer canonical skills over compatibility shims for new prompts.

## Keywords

Codex skills, skills README maintenance, roadmap maintenance, workspace cleanup, Things reminders, Things digest, productivity automation.

## License

Apache License 2.0. See [LICENSE](./LICENSE).
