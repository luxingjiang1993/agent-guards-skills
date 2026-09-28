#!/usr/bin/env python3
"""Deterministic provenance rules for Agent Guards (no LLM). Exit 0 always; prints JSON summary."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

KIND_RE = re.compile(r"(?im)^\s*[-*]?\s*\*?\*?Kind\*?\*?\s*:\s*(\w+)")
SOURCE_RE = re.compile(r"(?im)^\s*[-*]?\s*\*?\*?Source\*?\*?\s*:\s*(.+)$")
PIN_RE = re.compile(r"(?im)^\s*[-*]?\s*\*?\*?Pin\*?\*?\s*:\s*(.+)$")
WHAT_RE = re.compile(r"(?im)^\s*[-*]?\s*\*?\*?What changed\*?\*?\s*:\s*(.+)$")
WHY_RE = re.compile(r"(?im)^\s*[-*]?\s*\*?\*?Why not copy as-is\*?\*?\s*:\s*(.+)$")
LICENSE_RE = re.compile(r"(?im)^\s*[-*]?\s*\*?\*?License(?: note)?\*?\*?\s*:\s*(.+)$")
PATHS_HINT = re.compile(r"(?im)(Paths?\s*:|src/|lib/|\.ts|\.tsx|\.py)")
URL_RE = re.compile(r"https?://\S+")
SHA_OR_TAG = re.compile(
    r"(/commit/[0-9a-f]{7,40}|[?&](?:ref|rev)=|@v?\d|/tree/v\d|/blob/[0-9a-f]{7,40}/|"
    r"\bPin:\s*(?!missing|\(missing|none|n/a)\S)",
    re.I,
)
MEMORY_ONLY = re.compile(r"(?i)\b(from memory|similar to what i saw|as i recall|vague)\b")


def parse(text: str) -> dict:
    kind_m = KIND_RE.search(text)
    source_m = SOURCE_RE.search(text)
    pin_m = PIN_RE.search(text)
    what_m = WHAT_RE.search(text)
    why_m = WHY_RE.search(text)
    lic_m = LICENSE_RE.search(text)
    kind = (kind_m.group(1).lower() if kind_m else "").strip()
    source = (source_m.group(1).strip() if source_m else "")
    pin = (pin_m.group(1).strip() if pin_m else "")
    return {
        "kind": kind,
        "source": source,
        "pin": pin,
        "what": (what_m.group(1).strip() if what_m else ""),
        "why": (why_m.group(1).strip() if why_m else ""),
        "license": (lic_m.group(1).strip() if lic_m else ""),
        "paths_hint": bool(PATHS_HINT.search(text)),
        "has_url": bool(URL_RE.search(source) or URL_RE.search(text)),
    }


def evaluate(text: str) -> dict:
    p = parse(text)
    notes: list[str] = []
    required = p["kind"] in {"adapt", "port"} or (
        p["paths_hint"] and p["kind"] not in {"new", "generated", ""}
    )
    # also required if adapt-like language without kind new
    if re.search(r"(?i)\b(adapt|port|reference:|based on)\b", text) and p["kind"] != "new":
        required = True
    if p["kind"] == "new" and not re.search(r"(?i)\b(adapt|port)\b", text):
        required = False

    if not required and p["kind"] in {"", "unknown"}:
        if re.search(r"(?i)Provenance|Kind:", text) is None and p["paths_hint"]:
            return {"result": "fail", "notes": "Provenance required (paths touch existing code) but missing", **p}

    if not required:
        return {"result": "pass", "notes": "Provenance not required", **p}

    if p["kind"] not in {"new", "adapt", "port", "generated"}:
        return {"result": "fail", "notes": f"Invalid or missing Kind: {p['kind']!r}", **p}

    if p["kind"] == "new":
        return {"result": "pass", "notes": "Kind new", **p}

    if not p["source"] or MEMORY_ONLY.search(p["source"]) or MEMORY_ONLY.search(text):
        return {"result": "fail", "notes": "Source missing or memory-only", **p}

    if p["kind"] in {"adapt", "port"}:
        if not p["what"] or p["what"].lower() in {"", "tbd", "..."}:
            notes.append("What changed empty")
        if not p["why"] or p["why"].lower() in {"", "tbd", "..."}:
            notes.append("Why not copy as-is empty")

    urls = URL_RE.findall(p["source"]) + URL_RE.findall(text)
    if urls:
        pinned = False
        blob = p["source"] + "\n" + p["pin"] + "\n" + text
        if SHA_OR_TAG.search(blob) and not re.search(r"(?i)Pin:\s*(\(missing|missing|none|n/a)", blob):
            # unpinned main blob URLs without pin field
            if re.search(r"(?i)Pin:\s*(\(missing|missing)", text) or (
                "/blob/main/" in blob and not re.search(r"(?i)Pin:\s*[0-9a-f]{7,}|Pin:\s*v?\d", text)
            ):
                pinned = False
            elif SHA_OR_TAG.search(p["source"] + " " + p["pin"]) and not re.search(
                r"(?i)\(missing|missing — warn\)", p["pin"]
            ):
                pinned = True
            else:
                pinned = bool(re.search(r"/commit/[0-9a-f]{7,40}|/blob/[0-9a-f]{7,40}/", blob, re.I))
        if not pinned:
            notes.append("URL has no SHA/tag pin")
        if not p["license"]:
            notes.append("License note missing for external URL")

    if any("empty" in n or "missing" in n.lower() and "URL" not in n for n in notes if "URL" not in n and "License" not in n):
        hard = [n for n in notes if n.startswith("What") or n.startswith("Why") or "memory" in n.lower()]
        if hard:
            return {"result": "fail", "notes": "; ".join(notes), **p}

    if notes:
        # URL pin / license → warn; empty what/why → fail
        if any(n.startswith("What") or n.startswith("Why") for n in notes):
            return {"result": "fail", "notes": "; ".join(notes), **p}
        return {"result": "warn", "notes": "; ".join(notes), **p}

    return {"result": "pass", "notes": "ok", **p}


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: check_provenance.py <ticket.md> [expected:pass|warn|fail]", file=sys.stderr)
        return 2
    path = Path(argv[1])
    text = path.read_text(encoding="utf-8")
    out = evaluate(text)
    out["file"] = str(path)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if len(argv) >= 3:
        expected = argv[2].strip().lower()
        if out["result"] != expected:
            print(f"EXPECTED {expected} got {out['result']}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
