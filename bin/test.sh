#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
python3 - << 'PY'
import sys, subprocess
from pathlib import Path
root = Path(".")
errors = []
required = ["setup-agent-guards", "enrich-tickets", "provenance-check", "before-implement"]
assert not (root / "skills/implement-guarded").exists(), "old implement-guarded must be removed"
for name in required:
    sm = root / "skills" / name / "SKILL.md"
    if not sm.is_file():
        errors.append(f"missing {sm}"); continue
    t = sm.read_text(encoding="utf-8")
    if not t.startswith("---"):
        errors.append(f"no frontmatter {sm}"); continue
    fm = t.split("---", 2)[1]
    if "name:" not in fm or "description:" not in fm:
        errors.append(f"bad frontmatter {sm}")
    if name == "before-implement":
        if "Gates pass" not in t or "/implement" not in t:
            errors.append("before-implement must hand off with Gates pass → /implement")
        if "fresh" not in t.lower():
            errors.append("before-implement should mention fresh session")
    if name == "enrich-tickets" and "Required" not in t:
        errors.append("enrich should label Required fields")
for script in ("bin/install-to-repo.sh", "bin/install-global.sh", "bin/test.sh"):
    if not ((root / script).stat().st_mode & 0o111):
        errors.append(f"not executable {script}")
for tmpl in ("templates/agent-guards.md", "templates/HOOKS.md", "templates/AGENTS-FRAGMENT.md", "templates/ticket-template.md"):
    if not (root / tmpl).is_file():
        errors.append(f"missing {tmpl}")
if "ADVANCED" not in (root / "templates/HOOKS.md").read_text().upper() and "OPTIONAL" not in (root / "templates/HOOKS.md").read_text().upper():
    errors.append("HOOKS.md should be ADVANCED/OPTIONAL")
checker = root / "lib/check_provenance.py"
cases = [
    ("tests/fixtures/provenance/pass-new.md", "pass"),
    ("tests/fixtures/provenance/pass-pinned.md", "pass"),
    ("tests/fixtures/provenance/warn-unpinned.md", "warn"),
    ("tests/fixtures/provenance/fail-memory.md", "fail"),
    ("tests/fixtures/provenance/fail-empty-why.md", "fail"),
]
for path, exp in cases:
    r = subprocess.run([sys.executable, str(checker), path, exp], capture_output=True, text=True)
    if r.returncode != 0:
        errors.append(f"{path}: {r.stderr or r.stdout}")
# stale name in skill/install surfaces (history docs may mention the rename)
scan_roots = [root / "skills", root / "templates", root / "bin", root / "lib", root / "tests"]
for base in scan_roots:
    if not base.exists():
        continue
    for p in base.rglob("*"):
        if not p.is_file():
            continue
        if p.resolve() == (root / "bin/test.sh").resolve():
            continue
        if p.suffix not in {".md", ".py", ".sh"}:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if "implement-guarded" in text:
            errors.append(f"stale implement-guarded in {p}")
# fixture thin ticket
thin = root / "tests/fixtures/repo/tasks/FIX-20260928-003-thin.md"
if thin.is_file() and "## Agent Guards" in thin.read_text():
    errors.append("thin fixture should lack Agent Guards")
# install script lists before-implement
inst = (root / "bin/install-to-repo.sh").read_text()
if "before-implement" not in inst or "implement-guarded" in inst:
    errors.append("install-to-repo must install before-implement only")
if errors:
    print("FAIL:")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("ALL TESTS PASSED")
PY
