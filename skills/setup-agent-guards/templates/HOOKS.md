# Agent Guards — hooks (ADVANCED / OPTIONAL)

Default setup **skips** this file. Real gates are: failing tests + Matt `/code-review`.

If your host supports Stop/PreToolUse hooks, you may:
- Block Done when Acceptance missing or Provenance status is `fail`
- Block `git reset --hard` / force-push

Do not block Matt's normal test/typecheck/commit flow. Do not auto-invoke `/implement`.
