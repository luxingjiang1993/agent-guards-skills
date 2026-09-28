---
name: enrich-tickets
description: >-
  After Matt to-tickets, add thin Agent Guards fields (Acceptance, Paths,
  Provenance when needed; auto Trust/Blast). Before before-implement.
  Does not replace to-tickets or write app code.
---

# Enrich Tickets

Keep Matt ticket body. Only add/update a thin `## Agent Guards` section.

## Matt boundary
- Do not re-split specs or rewrite Matt narrative.
- Do not run `/implement` or `/tdd`.

## Inputs
Optional ids/paths; else all open tickets (skip `done/`, `_template`).

## Required (always try to fill)
1. **ID** — filename or tracker; validate pattern  
2. **Acceptance** — ≥1 executable Given/When/Then or exact command  
3. **Paths** — file list  
4. **Provenance** — only when Paths touch existing code or adapt/port/reference: Kind + Source (path and/or URL). Never invent URLs.

## Auto-fill (human glances only on Gate)
- **Blast** — infer; default `none`  
- **Trust** — Gate if auth/db/pay; else config Default Trust  

## Optional (omit on Auto/ui when empty)
Rollback, Do-not-touch, Tests waived reason, Skills to load.

## Then
Run provenance rules → `### Provenance status`. Summarize table: ID | Trust | Blast | Prov | Acceptance?

## Do not
Implement · invent URLs · bloat every ticket with optional fields
