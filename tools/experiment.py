#!/usr/bin/env python3
"""Experiment lifecycle manager — git-as-search-space for story exploration.

Implements the branching architecture adopted 2026-08-25 (see
docs/pipeline.md, "Experiment Lifecycle"):

    python tools/experiment.py start dive ch06 impossible-game ^
        --trigger curiosity --question "What game would this city invent?"
    python tools/experiment.py status
    python tools/experiment.py stage impossible-game incubate
    python tools/experiment.py close impossible-game harvest ^
        --found "culturally embedded controller/masses game" ^
        --reason "interrogation rewrite overengineered"
    python tools/experiment.py close impossible-game accept   # squash-merge
    python tools/experiment.py close impossible-game reject
    python tools/experiment.py close impossible-game defer
    python tools/experiment.py list --all

Design:
- main is sacred: the currently believed story.
- Experiments run on local branch exp/<type>/<slug> checked out via git
  worktree at ../test-story-ox-exp-<slug> so canon cannot be mutated
  accidentally.
- Metadata lives under .git/experiments/ (shared across worktrees, never in
  the manuscript tree).
- Every closed experiment is tagged experiment/<YYYYMMDD>/<slug> so dead
  universes stay reachable; branches/worktrees are removed.
- ACCEPT squash-merges into main (one clean mainline commit).
- HARVEST appends discovered items to drafts/discovery_buffer.md on main.
"""

import argparse
import subprocess
import sys
from datetime import date
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
BUFFER_PATH = REPO_ROOT / "drafts" / "discovery_buffer.md"
OUTCOMES = ("accept", "reject", "harvest", "defer")
STAGES = ("probe", "incubate", "candidate")


def git(*args, cwd=REPO_ROOT, check=True):
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"git {' '.join(args)} failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


def meta_path() -> Path:
    """Shared metadata lives under the MAIN .git (works from any worktree)."""
    d = Path(git("rev-parse", "--git-common-dir")).resolve()
    return d / "experiments" / "experiments.yaml"


META_PATH = None  # resolved lazily via meta_path()


def load_meta() -> dict:
    p = meta_path()
    if p.exists():
        return yaml.safe_load(p.read_text(encoding="utf-8")) or {"experiments": []}
    return {"experiments": []}


def save_meta(meta: dict) -> None:
    p = meta_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(yaml.safe_dump(meta, sort_keys=False, allow_unicode=True), encoding="utf-8")


def get_exp(meta: dict, slug: str, require_active: bool = False):
    matches = [e for e in meta["experiments"] if e["slug"] == slug]
    if require_active:
        matches = [e for e in matches if e.get("active")] or matches
    for e in matches:
        return e
    print(f"No experiment named '{slug}'.", file=sys.stderr)
    sys.exit(1)


def sanitize(slug: str) -> str:
    out = re.sub(r"[^a-z0-9-]+", "-", slug.lower()).strip("-")
    if not out:
        print("Slug must contain letters/numbers.", file=sys.stderr)
        sys.exit(1)
    return out


import re  # noqa: E402


def require_main_clean():
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    if branch != "main":
        print(f"Must run from main (currently on '{branch}').", file=sys.stderr)
        sys.exit(1)
    if git("status", "--porcelain"):
        print("Working tree not clean — commit or stash first.", file=sys.stderr)
        sys.exit(1)


def cmd_start(args):
    meta = load_meta()
    slug = sanitize(args.slug)
    branch = f"exp/{args.type}/{slug}"
    worktree = REPO_ROOT.parent / f"test-story-ox-exp-{slug}"
    if any(e["slug"] == slug and e.get("active") for e in meta["experiments"]):
        print(f"'{slug}' already exists and is active.", file=sys.stderr)
        sys.exit(1)

    base = git("rev-parse", "HEAD")
    git("worktree", "add", str(worktree), "-b", branch, "main")

    ids = [e.get("id", "") for e in meta["experiments"]]
    n = 1
    today = date.today().strftime("%Y%m%d")
    while f"{today}-{n:03d}" in ids:
        n += 1
    exp_id = f"{today}-{n:03d}"

    meta["experiments"].append({
        "id": exp_id,
        "slug": slug,
        "type": args.type,
        "scope": args.scope or "",
        "branch": branch,
        "worktree": str(worktree),
        "base": base,
        "created": str(date.today()),
        "trigger": args.trigger,
        "question": args.question or "",
        "stage": "probe",
        "active": True,
    })
    save_meta(meta)
    print(f"[{exp_id}] started {branch}")
    print(f"  worktree: {worktree}")
    print(f"  stage: probe — follow the thought; QA machinery waits for CANDIDATE.")
    print(f"  When done: python tools/experiment.py close {slug} <accept|reject|harvest|defer>")


def cmd_status(_args):
    meta = load_meta()
    active = [e for e in meta["experiments"] if e.get("active")]
    if not active:
        print("No active experiments.")
        return
    for e in active:
        dirty = ""
        wt = Path(e["worktree"])
        if wt.exists():
            r = subprocess.run(["git", "status", "--porcelain"], cwd=wt,
                               capture_output=True, text=True)
            dirty = " [uncommitted changes]" if r.stdout.strip() else " [clean]"
        print(f"[{e['id']}] {e['slug']}  type={e['type']}  stage={e['stage']}{dirty}")
        print(f"    Q: {e.get('question') or '(no question recorded)'}")
        print(f"    {e['worktree']}")


def cmd_stage(args):
    meta = load_meta()
    e = get_exp(meta, sanitize(args.slug), require_active=True)
    if args.stage not in STAGES:
        print(f"Stage must be one of {STAGES}", file=sys.stderr)
        sys.exit(1)
    e["stage"] = args.stage
    save_meta(meta)
    print(f"[{e['id']}] {e['slug']} -> {args.stage}")


def _teardown(e: dict):
    wt = Path(e["worktree"])
    if wt.exists():
        subprocess.run(["git", "worktree", "remove", str(wt), "--force"], cwd=REPO_ROOT,
                       capture_output=True, text=True)
    git("branch", "-D", e["branch"], check=False)


def _tag(e: dict, suffix: str = ""):
    tag = f"experiment/{e['id']}/{e['slug']}{suffix}"
    r = subprocess.run(["git", "rev-parse", "-q", "--verify", tag],
                       cwd=REPO_ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        git("tag", "-a", tag, e["branch"],
            "-m", f"experiment {e['id']} type={e['type']} trigger={e['trigger']} "
                  f"question: {e.get('question', '')}")
    return tag


def cmd_close(args):
    meta = load_meta()
    e = get_exp(meta, sanitize(args.slug), require_active=True)
    if args.outcome not in OUTCOMES:
        print(f"Outcome must be one of {OUTCOMES}", file=sys.stderr)
        sys.exit(1)
    if args.outcome == "accept":
        # Only ACCEPT writes to main; other outcomes just tag & tear down.
        require_main_clean()

    tag = _tag(e)

    if args.outcome == "accept":
        git("merge", "--squash", e["branch"])
        msg = f"EXPERIMENT ACCEPT [{e['id']}] {e['type']}: {e['slug']}\n\nQuestion: {e.get('question', '')}"
        subprocess.run(["git", "commit", "-m", msg], cwd=REPO_ROOT, check=True,
                       capture_output=True, text=True)
    elif args.outcome == "harvest":
        found = args.found or []
        BUFFER_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not BUFFER_PATH.exists():
            BUFFER_PATH.write_text(
                "# Discovery Buffer\n\n"
                "Things that appeared while writing and feel alive. Un-scored,\n"
                "no justification required. Harvested from experiments; some will\n"
                "grow into the story, most will sleep here.\n",
                encoding="utf-8")
        with BUFFER_PATH.open("a", encoding="utf-8") as fh:
            fh.write(f"\n## {date.today()} — harvested from [{e['id']}] {e['slug']} ({e['type']})\n")
            fh.write(f"question: {e.get('question', '')}\n")
            for item in found:
                fh.write(f"- {item}\n")

    e["active"] = False
    e["outcome"] = args.outcome
    e["closed"] = str(date.today())
    e["tag"] = tag
    if args.distance:
        e["distance"] = args.distance
    if args.found:
        e["discovered"] = args.found
    if args.reason:
        e["reason"] = args.reason
    _teardown(e)
    save_meta(meta)
    print(f"[{e['id']}] {e['slug']} closed: {args.outcome.upper()}  (tag {tag})")
    if args.outcome == "accept":
        print("Squash-merged into main — review, then commit is already done.")


def cmd_list(args):
    meta = load_meta()
    exps = meta["experiments"]
    if not args.all:
        exps = [e for e in exps if e.get("active")]
    if not exps:
        print("(none)")
        return
    for e in exps:
        state = "active/" + e.get("stage", "?") if e.get("active") else e.get("outcome", "closed")
        print(f"[{e['id']}] {e['slug']:32} {e['type']:10} {state:16} {e.get('tag', '')}")
        if e.get("reason"):
            print(f"    reason: {e['reason']}")
        for d in e.get("discovered", []) or []:
            print(f"    discovered: {d}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Story experiment lifecycle (git-as-search-space)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("start")
    s.add_argument("type", help="dive|fork|rewrite|veto|mutation|zero-base|wild")
    s.add_argument("slug")
    s.add_argument("--scope", default="", help="what area the experiment touches (e.g. ch06, ending)")
    s.add_argument("--trigger", default="curiosity", choices=["curiosity", "stuck", "creative-itch"])
    s.add_argument("--question", default="")
    s.set_defaults(fn=cmd_start)

    st = sub.add_parser("status")
    st.set_defaults(fn=cmd_status)

    sg = sub.add_parser("stage")
    sg.add_argument("slug")
    sg.add_argument("stage")
    sg.set_defaults(fn=cmd_stage)

    c = sub.add_parser("close")
    c.add_argument("slug")
    c.add_argument("outcome", choices=OUTCOMES)
    c.add_argument("--found", action="append", help="discovered item (repeatable)")
    c.add_argument("--reason", default="")
    c.add_argument("--distance", default="",
                   help="creative distance traveled: low | medium | high | very-high "
                        "(qualitative by design - how far from the incumbent's "
                        "assumptions did this excursion reach?)")
    c.set_defaults(fn=cmd_close)

    l = sub.add_parser("list")
    l.add_argument("--all", action="store_true")
    l.set_defaults(fn=cmd_list)

    args = ap.parse_args()
    return args.fn(args) or 0


if __name__ == "__main__":
    sys.exit(main())
