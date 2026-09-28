---
name: provenance-check
description: >-
  Validate ticket Provenance before coding when adapting existing code or
  external URLs. Use after enrich-tickets or inside before-implement.
  Do not modify application source.
---

# Provenance Check

## Read
Ticket + `docs/agents/agent-guards.md`. Optional: `lib/check_provenance.py`.

## Rules (when required)
1. Required if Paths touch existing files OR Kind ∈ {adapt, port} OR external ref.  
2. Kind ∈ {new, adapt, port, generated}.  
3. Kind ≠ new → Source path and/or URL (not memory).  
4. URL → pin SHA/tag or `warn`.  
5. adapt|port → What changed + Why not copy as-is.  
6. External URL → License note.

## Output
`### Provenance status` → pass | warn | fail

## Matt boundary
Gates **whether** coding may start; Matt `/implement` decides **how**.
