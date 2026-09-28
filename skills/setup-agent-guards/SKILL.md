---
name: setup-agent-guards
description: >-
  Once per repo: Agent Guards config (ticket paths, Trust defaults, authority
  commands). Optional advanced hooks. Before enrich-tickets / before-implement.
  Does not replace Matt skills.
disable-model-invocation: true
---

# Setup Agent Guards

Per-repo config only.

## Matt boundary
- Never edit Matt skills. Chain stays: grill → to-spec → to-tickets → enrich → **before-implement** → Matt `/implement`.

## Process
### 1. Explore
AGENTS/CLAUDE, existing guards, Matt issue-tracker, `tasks/`, scripts.

### 2. Ask
A. Ticket location · B. Authority commands · C. Default Trust (Watch).  
Do **not** push hooks in the default path.

### 3. Write
1. `docs/agents/agent-guards.md` from templates.  
2. `tasks/`, `done/`, `_template.md`.  
3. AGENTS fragment `## Agent Guards` (update in place).  
4. Hooks: only if user asks — copy `templates/HOOKS.md` as `docs/agents/HOOKS.md` (**advanced / optional**).

### 4. Done
Next: `/enrich-tickets` then `/before-implement <id>` → user runs `/implement`.
