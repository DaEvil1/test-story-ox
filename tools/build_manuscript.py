#!/usr/bin/env python3
"""Assemble the manuscript from the chapter order defined in book.yaml.

Usage:
    python tools/build_manuscript.py

Writes output/manuscript.md and prints word-count progress against
book.yaml's target_word_count. Chapters with `include: false` are skipped.
Requires: Python 3.10+, PyYAML.
"""

import re
import sys
from datetime import date
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
BOOK_YAML = REPO_ROOT / "book.yaml"
OUTPUT_PATH = REPO_ROOT / "output" / "manuscript.md"

HEADING_RE = re.compile(r"^(Chapter \d+|Speculative Final Chapter|Epilogue)\b[^\n]*", re.IGNORECASE)


def main() -> int:
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
        sys.stdout.reconfigure(encoding="utf-8")

    book = yaml.safe_load(BOOK_YAML.read_text(encoding="utf-8"))
    title = book.get("title", "Untitled")
    floor = int(book.get("target_word_count", 0))
    ceiling = int(book.get("max_word_count", 0))

    parts: list[str] = [f"# {title}", ""]
    total_words = 0
    included = 0
    skipped: list[str] = []

    for entry in book.get("chapters", []):
        path = REPO_ROOT / entry["file"]
        if not entry.get("include", True):
            skipped.append(path.name)
            continue
        if not path.exists():
            print(f"ERROR: missing chapter file {path}", file=sys.stderr)
            return 1

        text = path.read_text(encoding="utf-8").strip()
        lines = text.splitlines()
        heading = None
        body_start = 0
        for i, line in enumerate(lines):
            if line.strip():
                match = HEADING_RE.match(line.strip())
                heading = match.group(0).strip() if match else line.strip()
                body_start = i + 1
                break

        words = len(text.split())
        total_words += words
        included += 1

        body = lines[body_start:]
        while body and not body[0].strip():
            body.pop(0)

        parts += [f"## {heading}", ""]
        parts += body
        # Trim trailing blank lines between chapters, keep one separator.
        while parts and not parts[-1].strip():
            parts.pop()
        parts += ["", ""]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")

    print(f"Assembled {included} chapters -> {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    band = ""
    if floor and ceiling:
        if total_words < floor:
            band = f" (below floor {floor} by {floor - total_words})"
        elif ceiling and total_words > ceiling:
            band = f" (above ceiling {ceiling} by {total_words - ceiling})"
        else:
            band = f" (within band {floor}-{ceiling})"
    elif floor:
        band = f" / target {floor} ({total_words - floor:+d})"
    print(f"Words: {total_words}{band}")
    if skipped:
        print("Excluded: " + ", ".join(skipped))
    return 0


if __name__ == "__main__":
    sys.exit(main())
