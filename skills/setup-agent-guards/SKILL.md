---
name: setup-agent-guards
description: >-
  Once per repo: Agent Guards config (ticket paths, Trust defaults, authority
  commands). Optional slim AGENTS/TASK templates. Before enrich-tickets /
  before-implement. Does not replace Matt skills.
disable-model-invocation: true
---

# Setup Agent Guards

Per-repo config only.

## Matt boundary
Never edit Matt skills. Chain: grill → to-spec → to-tickets → enrich → before-implement → Matt `/implement`.

## Process
### 1. Explore
AGENTS/CLAUDE, existing guards, Matt issue-tracker, `tasks/`, scripts.

### 2. Ask
A. Ticket location · B. Authority commands · C. Default Trust (Watch).  
Do **not** push hooks in the default path.

### 3. Write
1. `docs/agents/agent-guards.md` from templates.  
2. `tasks/`, `done/`, `_template.md` (from thin TASK template).  
3. If root `AGENTS.md` / `CLAUDE.md` is missing or has no Agent Guards section: offer slim starter from pack `docs/repo-templates/AGENTS.md`, then append `## Agent Guards` from [templates/AGENTS-FRAGMENT.md](../../templates/AGENTS-FRAGMENT.md) — update in place, never duplicate.  
4. Point user at `docs/repo-templates/HOW-TO.md` in the Agent Guards repo/pack for the AGENTS+ticket story.  
5. Hooks: only if user asks — copy `templates/HOOKS.md` (**advanced / optional**).

### 4. Done
Next: `/enrich-tickets` then `/before-implement <id>` → user `/implement`.
