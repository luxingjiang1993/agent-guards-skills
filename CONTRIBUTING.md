# Contributing

Thanks for improving Agent Guards.

## Principles

- Stay a **thin overlay** on [Matt Pocock skills](https://github.com/mattpocock/skills). Do not redefine `/implement`, `/tdd`, or `/code-review`.
- Keep required ticket fields minimal: **ID**, **Acceptance**, **Paths**, plus **Provenance** when adapting existing code or external URLs.
- Prefer fail-closed gates over long prose.

## Dev loop

```bash
./bin/test.sh
```

Add provenance fixtures under `tests/fixtures/provenance/` when changing `lib/check_provenance.py`.

## Skills layout

Each skill lives in `skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`). Keep descriptions trigger-focused.

## Pull requests

- One concern per PR.
- Update README install lines if skill names change.
- Use `before-implement` only; never revive the old guarded-implement skill name.
