# Agent Guards Skills

Thin **overlay** skills for coding agents. They sit on top of [Matt Pocock's skills](https://github.com/mattpocock/skills) and add ticket gates (acceptance, paths, provenance) **before** you run Matt's `/implement`.

They do **not** replace `grill-with-docs`, `to-spec`, `to-tickets`, `implement`, `tdd`, or `code-review`.

They also do **not** replace a slim `AGENTS.md` or per-ticket files — see [docs/repo-templates/HOW-TO.md](docs/repo-templates/HOW-TO.md).

## Daily flow

```text
grill-with-docs → to-spec → to-tickets → enrich-tickets → before-implement → /implement
                 (Matt)                   (Agent Guards)   (gate + handoff)   (Matt)
```

| Step | Skill | What it does |
|------|--------|----------------|
| Clarify | Matt `/grill-with-docs` | Align the ask with docs/reality |
| Spec | Matt `/to-spec` | Write the spec and test seams |
| Split | Matt `/to-tickets` | Cut thin tickets |
| Enrich | `/enrich-tickets` | Fill thin Agent Guards fields (batch OK) |
| Gate | `/before-implement <id>` | Check one ticket; hand off to Matt |
| Build | Matt `/implement` | TDD → typecheck/tests → `/code-review` → commit |

## AGENTS.md + TASK (still required, keep thin)

| Artifact | Purpose |
|----------|---------|
| [`docs/repo-templates/AGENTS.md`](docs/repo-templates/AGENTS.md) | Always-on rules: Done, stop, Trust, authority commands, Agent Guards pointer |
| [`docs/repo-templates/TASK.md`](docs/repo-templates/TASK.md) | One-slice ticket template (ID / Acceptance / Paths + Guards) |
| [`docs/repo-templates/HOW-TO.md`](docs/repo-templates/HOW-TO.md) | How the three layers fit together |

Copy those into your app repo (or let `/setup-agent-guards` seed them). Skills = **how to run**; AGENTS = **standing rules**; tickets = **this slice**.

## Install

### A. skills CLI (recommended)

```bash
npx skills@latest add luxingjiang1993/agent-guards-skills
```

Select: `setup-agent-guards`, `enrich-tickets`, `provenance-check`, `before-implement`.

Also install Matt's pack (at least `implement`, `tdd`, `code-review`):

```bash
npx skills add mattpocock/skills
```

### B. Copy into one repo

```bash
./bin/install-to-repo.sh /path/to/your/repo
```

### C. User-global copy

```bash
./bin/install-global.sh
```

### Once per repo

```text
/setup-agent-guards
```

Writes `docs/agents/agent-guards.md` and an `## Agent Guards` block on `AGENTS.md` / `CLAUDE.md`.

## Skills

| Skill | When |
|-------|------|
| [`setup-agent-guards`](skills/setup-agent-guards/SKILL.md) | Once per repo |
| [`enrich-tickets`](skills/enrich-tickets/SKILL.md) | After Matt `/to-tickets` |
| [`provenance-check`](skills/provenance-check/SKILL.md) | Before coding when adapting code/URLs |
| [`before-implement`](skills/before-implement/SKILL.md) | Gate one ticket, then Matt `/implement` |

### Thin required fields

Always: **ID**, **Acceptance** (≥1 executable check), **Paths**.  
When adapting existing code or external refs: **Provenance** (Kind + Source; pin remote URLs).  
**Trust** / **Blast** are auto-filled; humans confirm on Gate tickets.

### Evidence (after Matt `/implement`)

Keep it to three lines: typecheck exit · tests exit · paths ok|drift.

Hooks (`templates/HOOKS.md`) are **advanced / optional** and never replace Matt `/code-review`.

## Tests

```bash
./bin/test.sh
```

## License

[MIT](LICENSE)

## Acknowledgments

Built to compose with [mattpocock/skills](https://github.com/mattpocock/skills).
