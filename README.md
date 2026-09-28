# Agent Guards Skills

Thin **overlay** skills for coding agents. They sit on top of [Matt Pocock's skills](https://github.com/mattpocock/skills) and add ticket gates (acceptance, paths, provenance) **before** you run Matt's `/implement`.

They do **not** replace `grill-with-docs`, `to-spec`, `to-tickets`, `implement`, `tdd`, or `code-review`.

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

`before-implement` **stops after gates pass** and asks you to run `/implement` in a **fresh** session (one ticket per session), unless you explicitly say to continue coding in the same chat.

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

In the agent:

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

Runs skill frontmatter checks, rename guards, and deterministic provenance fixtures via `lib/check_provenance.py`.

## License

[MIT](LICENSE)

## Acknowledgments

Built to compose with [mattpocock/skills](https://github.com/mattpocock/skills). All credit for the implement/TDD/review loop belongs there.
