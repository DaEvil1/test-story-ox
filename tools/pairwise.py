#!/usr/bin/env python3
"""Pairwise revision judging (adopted 2026-08-25).

Every nontrivial revision can go to a blind vote before it is kept:
OLD (a base git revision) vs NEW (working tree), anonymized as files A/B
with randomized assignment, judged by 3 fresh contexts. If a majority
prefers OLD, the revision reverts.

    python tools/pairwise.py start --chapter src/04-chapters/chapter_11.md --base HEAD~1
    #   -> tests/pairwise/<id>/A.md and B.md  (send each to a fresh judge)
    python tools/pairwise.py record <id> J1 B "B's restraint lands harder"
    python tools/pairwise.py tally <id>
    python tools/pairwise.py clean <id>
"""

import argparse
import random
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
PW_DIR = REPO_ROOT / "tests" / "pairwise"


def _git_meta() -> Path:
    """Shared metadata dir (works from any worktree)."""
    r = subprocess.run(
        ["git", "rev-parse", "--git-common-dir"],
        cwd=Path.cwd(), capture_output=True, text=True,
    )
    d = r.stdout.strip() or ".git"
    return Path(d).resolve() / "pairwise"


def load_meta(pid: str) -> dict:
    p = _git_meta() / f"{pid}.yaml"
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def save_meta(pid: str, meta: dict) -> None:
    d = _git_meta()
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{pid}.yaml").write_text(
        yaml.safe_dump(meta, sort_keys=False, allow_unicode=True), encoding="utf-8")


def load_meta(pid: str) -> dict:
    p = _git_meta() / f"{pid}.yaml"
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def save_meta(pid: str, meta: dict) -> None:
    d = _git_meta()
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{pid}.yaml").write_text(
        yaml.safe_dump(meta, sort_keys=False, allow_unicode=True), encoding="utf-8")


def cmd_start(args):
    import yaml as _y
    new_text = Path(args.chapter).read_text(encoding="utf-8")
    old_text = subprocess.run(
        ["git", "show", f"{args.base}:{args.chapter}"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout

    pid = args.id or random.choice("ABCDEFGH") + str(random.randint(10, 99))
    out_dir = PW_DIR / pid
    out_dir.mkdir(parents=True, exist_ok=True)

    a_is_new = random.random() < 0.5
    (out_dir / "A.md").write_text(new_text if a_is_new else old_text, encoding="utf-8")
    (out_dir / "B.md").write_text(old_text if a_is_new else new_text, encoding="utf-8")

    save_meta(pid, {
        "id": pid, "chapter": args.chapter, "base": args.base,
        "a_is": "new" if a_is_new else "old",
        "votes": {},
        "open": True,
    })
    print(f"[{pid}] started — {args.chapter}  (OLD={args.base}, NEW=working tree)")
    print(f"  Files: {out_dir / 'A.md'} and {out_dir / 'B.md'}")
    print(f"  Send each file to a fresh judge context. Collect verdicts:")
    print(f"    python tools/pairwise.py record {pid} J1 A \"reason\"")
    print(f"  Majority for the OLD side -> revert the revision.")


def cmd_record(args):
    meta = load_meta(args.id)
    if not meta.get("open"):
        print("Closed.", file=sys.stderr)
        sys.exit(1)
    choice = args.choice.upper()
    if choice not in ("A", "B"):
        print("Choice must be A or B.", file=sys.stderr)
        sys.exit(1)
    meta["votes"][args.judge] = {"choice": choice, "comment": args.comment or ""}
    save_meta(args.id, meta)
    print(f"[{args.id}] recorded {args.judge}: {choice}")


def cmd_tally(args):
    meta = load_meta(args.id)
    a_is = meta["a_is"]
    old_votes = sum(1 for v in meta["votes"].values() if v["choice"].upper() != ("A" if a_is == "new" else "B"))
    new_votes = len(meta["votes"]) - old_votes
    print(f"[{args.id}] chapter={meta['chapter']}  base={meta['base']}")
    print(f"  A was {'NEW' if a_is == 'new' else 'OLD'}   |   votes: OLD={old_votes} NEW={new_votes}")
    for judge, v in sorted(meta["votes"].items()):
        side = "OLD" if v["choice"].upper() != ("A" if a_is == "new" else "B") else "NEW"
        print(f"    {judge}: {side}  {v['comment']}")
    if len(meta["votes"]) < 2:
        print("  Need >=2 votes.")
        return
    verdict = "KEEP revision" if new_votes >= old_votes else "REVERT — majority preferred OLD"
    print(f"  VERDICT: {verdict}")


def cmd_clean(args):
    meta = load_meta(args.id)
    out_dir = PW_DIR / args.id
    if out_dir.exists():
        subprocess.run(["git", "rm", "-r", "-q", "--cached", f"tests/pairwise/{args.id}"],
                       cwd=REPO_ROOT, check=False,
                       capture_output=True, text=True)
        import shutil
        shutil.rmtree(out_dir, ignore_errors=True)
    (_git_meta() / f"{args.id}.yaml").unlink(missing_ok=True)
    print(f"[{args.id}] cleaned.")


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("start")
    s.add_argument("--chapter", required=True)
    s.add_argument("--base", default="HEAD~1")
    s.add_argument("--id", default="")
    s.set_defaults(fn=cmd_start)

    r = sub.add_parser("record")
    r.add_argument("id")
    r.add_argument("judge")
    r.add_argument("choice")
    r.add_argument("comment", nargs="?", default="")
    r.set_defaults(fn=cmd_record)

    t = sub.add_parser("tally")
    t.add_argument("id")
    t.set_defaults(fn=cmd_tally)

    c = sub.add_parser("clean")
    c.add_argument("id")
    c.set_defaults(fn=cmd_clean)

    args = ap.parse_args()
    return args.fn(args) or 0


if __name__ == "__main__":
    sys.exit(main())
