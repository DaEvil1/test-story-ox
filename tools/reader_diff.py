#!/usr/bin/env python3
"""Prediction-error report: frozen reader predictions vs what the next
chapter actually delivered (from the scene ledger's new_info).

Assembles side-by-side comparisons for human judgment; hit/miss/surprise
calls are recorded manually in tests/PREDICTION_DIFF.md and feed the
surprise ledger (#47).

Usage:
    python tools/reader_diff.py [--report tests/PREDICTION_DIFF.md]
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
RS_DIR = REPO_ROOT / "tests" / "reader_state"
LEDGER = REPO_ROOT / "tests" / "analysis" / "scene_ledger.yaml"
DEFAULT_REPORT = REPO_ROOT / "tests" / "PREDICTION_DIFF.md"


def main() -> int:
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = ap.parse_args()

    scenes = (yaml.safe_load(LEDGER.read_text(encoding="utf-8")) or {}).get("scenes", [])
    info_by_chapter = {}
    for s in scenes:
        c = int(s.get("chapter", 0))
        info_by_chapter.setdefault(c, []).extend(s.get("new_info") or [])

    out = [
        "# Prediction Diff (generated assembly — judgment is manual)",
        "",
        "<!-- tools/reader_diff.py — frozen reader predictions vs next-chapter delivery. -->",
        "",
        "For each boundary: what the frozen reader expected, then the chapter's",
        "registered new information. Mark each prediction **hit**, **miss**, or",
        "**surprised** (delivered something better/different than asked) in",
        "`tests/PREDICTION_DIFF.md` after review.",
        "",
    ]

    snapshots = sorted(RS_DIR.glob("after_ch*.yaml"),
                       key=lambda p: int(re.search(r"(\d+)", p.stem).group(1)))
    for snap_path in snapshots:
        n = int(re.search(r"(\d+)", snap_path.stem).group(1))
        snap = yaml.safe_load(snap_path.read_text(encoding="utf-8")) or {}
        preds = snap.get("predictions_next") or []
        if not preds or (n + 1) not in info_by_chapter:
            continue
        delivered = info_by_chapter[n + 1]
        out.append(f"## Boundary ch{n} -> ch{n + 1}")
        out.append("")
        out.append("**Reader expected:**")
        for pr in preds:
            out.append(f"- {pr}")
        out.append("")
        out.append(f"**ch{n + 1} registered:**")
        for d in delivered:
            out.append(f"- {d}")
        out.append("")

    args.report.write_text("\n".join(out), encoding="utf-8")
    print(f"Prediction diff written to {args.report.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
