---
name: before-implement
description: >-
  Check one ticket's gates (Acceptance, Paths, Provenance, Trust) then hand off
  to Matt Pocock /implement in a fresh session. Use after enrich-tickets when
  guards matter. Not a replacement for implement, tdd, or code-review.
disable-model-invocation: true
---

# Before Implement

Thin pre-gate. **Does not write app code.** Coding starts only when the user runs Matt `/implement`.

## Matt boundary (hard)
- Never redefine `/tdd`, seams, or `/code-review`.
- Never present this skill as a substitute for `/implement`.
- If Matt `implement` is missing: tell user to install it; do not invent a fallback coding loop (except user-explicit Auto/ui micro-fixes via authority commands).

## Preconditions
1. Exactly one ticket id/path.
2. `docs/agents/agent-guards.md` exists (else `/setup-agent-guards`).
3. Prefer a fresh session for the later `/implement`.

## Steps (gate only)
1. Load ticket + config.
2. Missing required Guards → run **enrich-tickets** on this ticket only; if Trust is Watch/Gate, pause for a glance.
3. **provenance-check**. `fail` → stop. `warn` → ask once.
4. Required fields present: **Acceptance** (≥1 executable), **Paths**, and Provenance when rules say so. Trust/Blast may be auto-filled.
5. Announce Trust, Blast, Provenance status in one short line.

## Hand-off (two-step — default)
Print exactly (fill the id):

> Gates pass for `<ID>`. Open a **fresh** session and run `/implement` on this ticket.

Then **stop**. Do not continue into coding unless the user explicitly says to keep going in this session (e.g. 「门过了继续开写」).

## After Matt implement (user or later turn)
Append a **short** Evidence block (3 lines max):

```markdown
### Evidence
- typecheck: `<cmd>` → `<exit>`
- tests: `<cmd>` → `<exit>`
- paths: ok | drift: …
```

Commit message should include Ticket ID. Move to Done only with user OK. Never `git reset --hard` / force-push.

## Never
- Multiple tickets · skip provenance fail · claim Gate merge-ready without human · rewrite Matt skills
