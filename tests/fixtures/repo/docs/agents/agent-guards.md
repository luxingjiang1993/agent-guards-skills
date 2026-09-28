# Agent Guards (per-repo)

## Ticket location
- **Mode**: local-markdown | github | other
- **Local glob**: `tasks/**/*.md` (exclude `tasks/done/**`, `tasks/_template.md`)
- **Done folder**: `tasks/done/`

## Defaults
- **Default Trust**: Watch
- **Auto allowed when**: Blast is only `ui` or `none`, and Provenance kind is `new`
- **Gate when**: Blast includes `auth` or `db` or `pay`, or ticket says production
- **Ticket ID pattern**: `(?i)^(feat|fix|refactor|chore|spike)-[0-9]{8}-[0-9]{3}$` OR `^[A-Z]+-[0-9]+(\.[0-9]+)?$`

## Thin required fields
- Always: ID, Acceptance (≥1 executable), Paths
- Provenance when Paths touch existing code or Kind is adapt|port
- Trust/Blast: auto from rules; human confirms on Gate

## Evidence (after Matt /implement)
Three lines only: typecheck exit · tests exit · paths ok|drift

## Matt Pocock
```text
grill-with-docs → to-spec → to-tickets → enrich-tickets → before-implement → /implement
```
Install separately: `npx skills add mattpocock/skills`

## Hooks
Advanced/optional — see `docs/agents/HOOKS.md` only if you opted in during setup.

## Authority commands
- typecheck: `pnpm typecheck`
- test: `pnpm test`
