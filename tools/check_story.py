#!/usr/bin/env python3
"""Automated prose and structure checks for the story.

Usage:
    python tools/check_story.py
    python tools/check_story.py --report tests/STATUS.md
    python tools/check_story.py --strict

Exit codes: 0 = clean (or warnings only without --strict), 1 = errors found.
Requires: Python 3.10+, PyYAML.
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import patterns_negation

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CHAPTERS_DIR = REPO_ROOT / "src" / "04-chapters"
DEFAULT_RULES = REPO_ROOT / "tests" / "automated" / "rules.yaml"
DEFAULT_LEDGERS_DIR = REPO_ROOT / "tests" / "analysis"

CORPUS_LABEL = "(corpus)"

TITLE_RE = re.compile(r"^(Chapter \d+|Speculative Final Chapter|Epilogue)\b[^\n]*", re.IGNORECASE)
TITLE_PREFIX_RE = re.compile(r"^(chapter \d+|speculative final chapter|epilogue)\b\s*[—–-]*\s*", re.IGNORECASE)


def normalize(text: str) -> str:
    return (
        text.replace("\u2019", "'")
        .replace("\u2018", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
    )


def natural_key(path: Path):
    numbers = re.findall(r"\d+", path.stem)
    return (int(numbers[0]) if numbers else 0, path.stem)


def load_rules(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def check_line_rules(lines: list[str], rules: dict, findings: list, file_label: str) -> None:
    for lineno, raw in enumerate(lines, start=1):
        line = normalize(raw)
        low = line.lower()
        for rule in rules.get("phrase_rules", []):
            for phrase in rule.get("phrases", []):
                if phrase.lower() in low:
                    findings.append(
                        {
                            "file": file_label,
                            "line": lineno,
                            "rule": rule["id"],
                            "name": rule.get("name", ""),
                            "severity": rule.get("severity", "error"),
                            "match": phrase,
                            "context": line.strip()[:120],
                        }
                    )
        for rule in rules.get("regex_rules", []):
            if rule.get("scope", "line") != "line":
                continue
            match = re.search(rule["pattern"], line, re.IGNORECASE)
            if match:
                findings.append(
                    {
                        "file": file_label,
                        "line": lineno,
                        "rule": rule["id"],
                        "name": rule.get("name", ""),
                        "severity": rule.get("severity", "error"),
                        "match": match.group(0),
                        "context": line.strip()[:120],
                    }
                )


def check_ending_rules(text: str, rules: dict, findings: list, file_label: str) -> None:
    normalized = normalize(text)
    for rule in rules.get("regex_rules", []):
        if rule.get("scope") != "ending":
            continue
        window = normalized[-rule.get("ending_chars", 500):]
        match = re.search(rule["pattern"], window, re.IGNORECASE)
        if match:
            findings.append(
                {
                    "file": file_label,
                    "line": None,
                    "rule": rule["id"],
                    "name": rule.get("name", ""),
                    "severity": rule.get("severity", "warning"),
                    "match": match.group(0),
                    "context": "...(chapter ending)...",
                }
            )


def extract_title(text: str) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        match = TITLE_RE.match(normalize(stripped))
        return match.group(0).strip() if match else stripped
    return None


def title_key(title: str | None) -> str:
    """Reduce a heading to the story title alone so 'Chapter 3 — The Limit'
    and 'Chapter 7 — The Limit' compare equal for duplicate detection."""
    if not title:
        return ""
    normalized = normalize(title).strip().lower()
    return TITLE_PREFIX_RE.sub("", normalized)


def check_frequency(texts: dict[str, str], rules: dict, findings: list) -> None:
    """Count repeated phrases per chapter and across the corpus."""
    for rule in rules.get("frequency_rules", []):
        phrase = rule["phrase"].lower()
        max_per = rule.get("max_per_chapter")
        max_total = rule.get("max_total")
        total = 0
        for label, text in texts.items():
            count = normalize(text).lower().count(phrase)
            if not count:
                continue
            total += count
            if max_per is not None and count > max_per:
                findings.append(
                    {
                        "file": label,
                        "line": None,
                        "rule": rule["id"],
                        "name": rule.get("name", ""),
                        "severity": rule.get("severity", "warning"),
                        "match": f"{count}x {phrase!r} in one chapter (max {max_per})",
                        "context": "...(phrase frequency)...",
                    }
                )
        if max_total is not None and total > max_total:
            findings.append(
                {
                    "file": CORPUS_LABEL,
                    "line": None,
                    "rule": rule["id"],
                    "name": rule.get("name", ""),
                    "severity": rule.get("severity", "warning"),
                    "match": f"{total}x {phrase!r} across corpus (max {max_total})",
                    "context": "...(phrase frequency)...",
                }
            )


CORPUS_LABEL = "(corpus)"


def _finding(file: str, rule: str, name: str, severity: str, match: str, context: str = "", line: int | None = None) -> dict:
    return {
        "file": file,
        "line": line,
        "rule": rule,
        "name": name,
        "severity": severity,
        "match": match,
        "context": context,
    }


def check_scene_ledger(path: Path, findings: list) -> None:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    scenes = data.get("scenes", [])
    thr = data.get("thresholds", {})
    label = path.name

    for scene in scenes:
        sid = scene.get("id", "?")
        info = scene.get("new_info") or []
        flat = scene.get("value_change") == "flat"
        if not info and flat and scene.get("kind") != "transition":
            findings.append(_finding(label, "SL-01", "dead-scene",
                                     "error",
                                     f"{sid}: no new info and no value change"))

    ordered = sorted(scenes, key=lambda s: (s.get("chapter", 0), s.get("id", "")))
    for a, b in zip(ordered, ordered[1:]):
        if a.get("value_change") == "flat" and b.get("value_change") == "flat":
            findings.append(_finding(label, "SL-03", "flat-run",
                                     "warning",
                                     f"{a.get('id')} -> {b.get('id')}: consecutive flat scenes"))

    max_overlap = thr.get("max_info_overlap", 0.5)
    for i in range(len(scenes)):
        for j in range(i + 1, len(scenes)):
            si, sj = scenes[i], scenes[j]
            set_i = set(map(str, si.get("new_info") or []))
            set_j = set(map(str, sj.get("new_info") or []))
            if not set_i or not set_j:
                continue
            union = set_i | set_j
            overlap = len(set_i & set_j) / len(union)
            if overlap > max_overlap:
                findings.append(_finding(label, "SL-02", "repeated-scene-value",
                                         "error",
                                         f"{si.get('id')} ~ {sj.get('id')}: "
                                         f"{overlap:.0%} shared new-info"))

    costs = [s for s in scenes if s.get("cost_paid") not in (None, "none")]
    min_costs = thr.get("min_costs_total", 0)
    if len(costs) < min_costs:
        findings.append(_finding(label, "SL-04", "free-conflict",
                                 "error",
                                 f"{len(costs)} scenes pay a cost (min {min_costs})"))

    final_choices = [s for s in scenes if s.get("is_final_choice")]
    if len(final_choices) > 1:
        findings.append(_finding(label, "SL-07", "ambiguous-final-choice", "error",
                                 "more than one scene marked is_final_choice"))
    for scene in final_choices:
        sid = scene.get("id", "?")
        dilemma = scene.get("dilemma") or {}
        missing = [k for k in ("option_a", "option_b") if not (dilemma.get(k) or "").strip()]
        prices = dilemma.get("prices_on_page") or []
        if missing or not prices or not (scene.get("cost_to_protagonist") or "").strip():
            findings.append(_finding(label, "SL-07", "weightless-choice", "error",
                                     f"{sid}: final choice lacks both live options with "
                                     f"on-page prices, and/or a cost to the protagonist"))
    irreversible = [s for s in costs if s.get("irreversible")]
    min_irr = thr.get("min_irreversible_costs", 0)
    if len(irreversible) < min_irr:
        findings.append(_finding(label, "SL-05", "no-permanence",
                                 "error",
                                 f"{len(irreversible)} irreversible costs (min {min_irr})"))
    if thr.get("require_civic_stakes") and not any(
            s.get("stakes_scope") == "civic" for s in scenes):
        findings.append(_finding(label, "SL-06", "stakes-never-leave-home",
                                 "error",
                                 "no scene carries civic-scope stakes"))


def check_ambiguity_ledger(path: Path, findings: list) -> None:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    label = path.name
    for q in data.get("questions", []):
        qid = q.get("id", "?")
        minimum = int(q.get("min_evidence_per_reading", 1))
        for reading, evidence in (q.get("readings") or {}).items():
            n = len(evidence or [])
            if n < minimum:
                findings.append(_finding(label, "AM-01", "thin-ambiguity",
                                         "error",
                                         f"{qid} reading '{reading}' has {n} evidence items "
                                         f"(min {minimum})"))


def check_relationship_ledger(path: Path, findings: list) -> None:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    label = path.name
    for ch in data.get("characters", []):
        name = ch.get("name", "?")
        target = int(ch.get("lived_scene_target", 0))
        lived = ch.get("lived_scenes") or []
        if len(lived) < target:
            findings.append(_finding(label, "RL-01", "unwitnessed-character",
                                     "error",
                                     f"{name}: {len(lived)} lived scenes (target {target})"))


def check_promise_ledger(path: Path, findings: list) -> None:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    label = path.name
    for p in data.get("promises", []):
        claim = p.get("claim", "?")
        minimum = int(p.get("min_beats", 1))
        beats = p.get("beats") or []
        if len(beats) < minimum:
            findings.append(_finding(label, "PL-01", "broken-promise",
                                     "error",
                                     f"'{claim}': {len(beats)} delivering beats (min {minimum})"))


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def check_tension_ledger(path: Path, findings: list) -> None:
    data = load_yaml(path)
    label = path.name
    scenes = data.get("scenes", [])
    thr = data.get("thresholds", {})
    tensions = [s.get("tension") for s in scenes if isinstance(s.get("tension"), (int, float))]
    if not tensions:
        findings.append(_finding(label, "TN-00", "empty-ledger", "error", "no tension scores"))
        return
    mean = sum(tensions) / len(tensions)
    stdev = (sum((t - mean) ** 2 for t in tensions) / len(tensions)) ** 0.5
    min_stdev = thr.get("min_stdev")
    if min_stdev is not None and stdev < min_stdev:
        findings.append(_finding(label, "TN-01", "flat-curve", "error",
                                 f"tension stdev {stdev:.2f} < {min_stdev}"))
    peak = max(tensions)
    valley = min(tensions)
    if thr.get("min_peak") is not None and peak < thr["min_peak"]:
        findings.append(_finding(label, "TN-02", "no-climax", "error",
                                 f"peak tension {peak} < {thr['min_peak']}"))
    if thr.get("min_valley") is not None and valley > thr["min_valley"]:
        findings.append(_finding(label, "TN-03", "no-release", "error",
                                 f"valley tension {valley} > {thr['min_valley']}"))
    min_peak_count = thr.get("min_peak_count")
    if min_peak_count is not None:
        n_peak = sum(1 for t in tensions if t >= thr.get("min_peak", 8))
        if n_peak < min_peak_count:
            findings.append(_finding(label, "TN-06", "single-spike", "error",
                                     f"{n_peak} scenes at/above {thr.get('min_peak')} "
                                     f"(need {min_peak_count})"))
    min_valley_count = thr.get("min_valley_count")
    if min_valley_count is not None:
        n_valley = sum(1 for t in tensions if t <= thr.get("min_valley", 3))
        if n_valley < min_valley_count:
            findings.append(_finding(label, "TN-07", "thin-release", "error",
                                     f"{n_valley} scenes at/below {thr.get('min_valley')} "
                                     f"(need {min_valley_count})"))
    max_run = thr.get("max_consecutive_equal")
    if max_run is not None:
        run = 1
        for a, b in zip(tensions, tensions[1:]):
            run = run + 1 if a == b else 1
            if run > max_run:
                findings.append(_finding(label, "TN-04", "plateau", "error",
                                         f"{run} consecutive scenes at tension {a}"))
                break
    feelings = {s.get("feeling") for s in scenes if s.get("feeling")}
    min_feelings = thr.get("min_distinct_feelings")
    if min_feelings is not None and len(feelings) < min_feelings:
        findings.append(_finding(label, "TN-05", "one-note", "error",
                                 f"{len(feelings)} distinct reader feelings < {min_feelings}: "
                                 f"{sorted(feelings)}"))


def check_questions_ledger(path: Path, findings: list, last_chapter: int) -> None:
    data = load_yaml(path)
    label = path.name
    loops = data.get("loops", [])
    thr = data.get("thresholds", {})
    valid_statuses = {"answered", "held-deliberate"}
    open_by_chapter: dict[int, int] = {}
    for loop in loops:
        qid = loop.get("id", "?")
        status = loop.get("status", "")
        opened = int(loop.get("opened", 0))
        closed = loop.get("closed")
        if status not in valid_statuses:
            findings.append(_finding(label, "QL-01", "unresolved-loop", "error",
                                     f"{qid}: status '{status}' not allowed at polish stage"))
        start = opened
        end = int(closed) if closed is not None else last_chapter
        for c in range(start, end + 1):
            open_by_chapter[c] = open_by_chapter.get(c, 0) + 1
        if status == "held-deliberate":
            reminders = sorted(int(r) for r in loop.get("reminders", []))
            window = thr.get("max_open_chapters_without_reminder")
            if window is not None:
                points = [start] + reminders
                for a, b in zip(points, points[1:]):
                    if b - a > window:
                        findings.append(_finding(label, "QL-02", "forgotten-loop", "error",
                                                 f"{qid}: gap {a}->{b} exceeds {window} without reminder"))
                if last_chapter - points[-1] > window:
                    findings.append(_finding(label, "QL-02", "forgotten-loop", "error",
                                             f"{qid}: no reminder within {window} chapters of end "
                                             f"(last at {points[-1]})"))
    max_open = thr.get("max_simultaneously_open")
    if max_open is not None and open_by_chapter:
        worst = max(open_by_chapter.values())
        if worst > max_open:
            findings.append(_finding(label, "QL-03", "attention-overload", "error",
                                     f"{worst} loops simultaneously open (max {max_open})"))


def check_plantpayoff_ledger(path: Path, findings: list) -> None:
    data = load_yaml(path)
    label = path.name
    for item in data.get("items", []):
        iid = item.get("id", "?")
        status = item.get("status", "")
        payoff = (item.get("payoff") or "").strip()
        plant = (item.get("plant") or "").strip()
        if payoff and not plant:
            findings.append(_finding(label, "PP-01", "orphan-payoff", "error",
                                     f"{iid}: pays off but was never planted"))
        if plant and not payoff:
            if status != "needs-payoff":
                findings.append(_finding(label, "PP-02", "orphan-plant", "warning",
                                         f"{iid}: planted but never paid off"))
            elif status == "needs-payoff":
                findings.append(_finding(label, "PP-02", "open-plant", "warning",
                                         f"{iid}: planted (ch{item.get('planted', '?')}), "
                                         f"payoff pending — known work item"))


def check_attachment_ledger(path: Path, findings: list) -> None:
    data = load_yaml(path)
    label = path.name
    for ch in data.get("characters", []):
        name = ch.get("name", "?")
        minimum = int(ch.get("min_beats", 0))
        beats = ch.get("beats") or []
        if len(beats) < minimum:
            findings.append(_finding(label, "AT-01", "unattached-character", "error",
                                     f"{name}: {len(beats)} attachment beats (min {minimum})"))
            continue
        types = {b.get("type") for b in beats}
        if len(types) < 2:
            findings.append(_finding(label, "AT-02", "one-note-bond", "warning",
                                     f"{name}: all beats are '{next(iter(types))}'"))


def check_worldterms_ledger(path: Path, texts: dict[str, str], findings: list) -> None:
    import re
    data = load_yaml(path)
    label = path.name
    thr = data.get("thresholds", {})
    chapter_of = {i + 1: name for i, name in enumerate(sorted(texts.keys()))}
    ordered = [texts[chapter_of[c]] for c in sorted(chapter_of)]
    for entry in data.get("terms", []):
        term = entry.get("term", "")
        introduced = int(entry.get("introduced", 1))
        defined = int(entry.get("defined_by_context_in", introduced))
        needle = term.lower()
        first_seen = None
        for idx, text in enumerate(ordered, start=1):
            hay = text.lower() if needle.islower() and term != "The Limit" else text
            if term in hay or needle in hay.lower():
                first_seen = idx
                break
        if first_seen is not None and first_seen < introduced:
            findings.append(_finding(label, "WT-01", "term-drift", "error",
                                     f"'{term}' first appears in ch{first_seen}, "
                                     f"ledger says ch{introduced}"))
        lag = defined - introduced
        max_lag = thr.get("max_definition_lag")
        if max_lag is not None and lag > max_lag:
            findings.append(_finding(label, "WT-02", "late-onboarding", "error",
                                     f"'{term}': context arrives {lag} chapters after first use"))


def check_surprise_ledger(path: Path, findings: list) -> None:
    data = load_yaml(path)
    label = path.name
    turns = data.get("turns", [])
    thr = data.get("thresholds", {})
    if not turns:
        return
    n = len(turns)
    confirmed = sum(1 for t in turns if t.get("type") == "confirmed")
    moved = sum(1 for t in turns if t.get("type") in ("shifted", "subverted"))
    min_shift = thr.get("min_shift_ratio")
    if min_shift is not None and moved / n < min_shift:
        findings.append(_finding(label, "SR-01", "predictable-turns", "error",
                                 f"{moved}/{n} turns shift or subvert (min ratio {min_shift})"))
    max_conf = thr.get("max_confirmed_ratio")
    if max_conf is not None and confirmed / n > max_conf:
        findings.append(_finding(label, "SR-02", "confirmation-dominance", "error",
                                 f"{confirmed}/{n} turns pure confirmations (max ratio {max_conf})"))
    for t in turns:
        if t.get("type") == "subverted" and not (t.get("seed") or "").strip():
            findings.append(_finding(label, "SR-03", "unseeded-twist", "error",
                                     f"ch{t.get('chapter')}: subversion without a seed"))


VALID_TRIAGE = {"fixed", "explained-in-text", "embraced-deliberate"}


def check_reception_ledger(path: Path, findings: list) -> None:
    data = load_yaml(path)
    label = path.name
    acts = {a.get("act") for a in data.get("act_stakes_legibility", [])}
    for expected in (1, 2, 3):
        if expected not in acts:
            findings.append(_finding(label, "RC-01", "illegible-stakes", "error",
                                     f"act {expected} has no want/stakes statement"))
    for breaker in data.get("immersion_breakers", []):
        triage = breaker.get("triage", "")
        if triage not in VALID_TRIAGE:
            findings.append(_finding(label, "RC-02", "untriaged-breaker", "error",
                                     f"'{breaker.get('issue', '?')[:60]}' triage='{triage}'"))
    for tp in data.get("title_payoffs", []):
        if not (tp.get("pays_off_in") or "").strip():
            findings.append(_finding(label, "RC-03", "loose-title", "warning",
                                     f"ch{tp.get('chapter')} title has no paying scene"))


def check_negation_contrast(texts: dict[str, str], findings: list) -> None:
    """Adopted 2026-08-24: STRONG/MEDIUM negation-contrast frames warn;
    WEAK is a style fingerprint capped at 5% of the chapter's sentences
    (floor 3). See tools/patterns_negation.py."""
    for label, text in texts.items():
        raw = patterns_negation.normalize(text)
        sent_count = len([s for s in patterns_negation.SENT_RE.finditer(raw)])
        weak_cap = max(patterns_negation.WEAK_FLOOR,
                       round(sent_count * patterns_negation.WEAK_RATE))
        weak = 0
        for f in patterns_negation.find(raw):
            if f["severity"] in ("STRONG", "MEDIUM"):
                findings.append(_finding(label, "NC-01", "negation-contrast-frame",
                                         "warning",
                                         f"line {f['line']} ({f['reason']})",
                                         context=f["text"][:120]))
            else:
                weak += 1
        if weak > weak_cap:
            findings.append(_finding(label, "NC-02", "weak-negation-over-cap",
                                     "warning",
                                     f"{weak} WEAK frames (cap {weak_cap} = 5% of "
                                     f"{sent_count} sentences, floor {patterns_negation.WEAK_FLOOR})"))


def check_ledgers(ledgers_dir: Path, findings: list, texts: dict[str, str]) -> None:
    ledger_checks = {
        "scene_ledger.yaml": check_scene_ledger,
        "ambiguity_ledger.yaml": check_ambiguity_ledger,
        "relationship_ledger.yaml": check_relationship_ledger,
        "promise_ledger.yaml": check_promise_ledger,
        "tension_ledger.yaml": check_tension_ledger,
        "attachment_ledger.yaml": check_attachment_ledger,
        "plantpayoff_ledger.yaml": check_plantpayoff_ledger,
        "surprise_ledger.yaml": check_surprise_ledger,
        "reception_ledger.yaml": check_reception_ledger,
    }
    for filename, fn in ledger_checks.items():
        path = ledgers_dir / filename
        if path.exists():
            fn(path, findings)

    questions_path = ledgers_dir / "questions_ledger.yaml"
    if questions_path.exists():
        scene_data = load_yaml(ledgers_dir / "scene_ledger.yaml") if (ledgers_dir / "scene_ledger.yaml").exists() else {}
        chapters = [s.get("chapter", 0) for s in scene_data.get("scenes", [])]
        last_chapter = max(chapters) if chapters else 11
        check_questions_ledger(questions_path, findings, last_chapter)

    worldterms_path = ledgers_dir / "worldterms_ledger.yaml"
    if worldterms_path.exists() and texts:
        check_worldterms_ledger(worldterms_path, texts, findings)


def main() -> int:
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Run automated story checks.")
    parser.add_argument("--chapters-dir", type=Path, default=DEFAULT_CHAPTERS_DIR)
    parser.add_argument("--rules", type=Path, default=DEFAULT_RULES)
    parser.add_argument("--ledgers-dir", type=Path, default=DEFAULT_LEDGERS_DIR)
    parser.add_argument("--report", type=Path, help="Write a markdown status report to this path.")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures.")
    args = parser.parse_args()

    rules = load_rules(args.rules)
    chapter_files = sorted(args.chapters_dir.glob("*.md"), key=natural_key)
    if not chapter_files:
        print(f"No chapters found in {args.chapters_dir}", file=sys.stderr)
        return 1

    findings: list[dict] = []
    titles: dict[str, list[str]] = {}
    stats: list[dict] = []
    texts: dict[str, str] = {}

    for path in chapter_files:
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        label = path.name
        title = extract_title(text)
        if title:
            titles.setdefault(title_key(title), []).append(label)

        check_line_rules(lines, rules, findings, label)
        check_ending_rules(text, rules, findings, label)

        words = len(text.split())
        stats.append({"file": label, "title": title or "(untitled)", "words": words})
        texts[label] = text

    check_frequency(texts, rules, findings)
    check_negation_contrast(texts, findings)
    check_ledgers(args.ledgers_dir, findings, texts)

    chapter_labels = {s["file"] for s in stats}
    ledger_findings = [f for f in findings if f["file"] not in chapter_labels]

    dup_rule = next(
        (r for r in rules.get("structural_rules", []) if r.get("name") == "duplicate-chapter-title"),
        None,
    )
    if dup_rule:
        for title_text, files in sorted(titles.items()):
            if len(files) > 1:
                for label in files:
                    findings.append(
                        {
                            "file": label,
                            "line": 1,
                            "rule": dup_rule["id"],
                            "name": dup_rule.get("name", ""),
                            "severity": dup_rule.get("severity", "error"),
                            "match": f"title shared with {', '.join(f for f in files if f != label)}",
                            "context": title_text,
                        }
                    )

    errors = [f for f in findings if f["severity"] == "error"]
    warnings = [f for f in findings if f["severity"] != "error"]

    by_file: dict[str, list[dict]] = {}
    for finding in findings:
        by_file.setdefault(finding["file"], []).append(finding)

    total_words = sum(s["words"] for s in stats)
    print(f"Chapters: {len(stats)}   Words: {total_words}")
    print("-" * 72)
    for stat in stats:
        file_findings = by_file.get(stat["file"], [])
        file_errors = sum(1 for f in file_findings if f["severity"] == "error")
        file_warnings = len(file_findings) - file_errors
        if not file_findings:
            status = "PASS"
        elif file_errors:
            status = "FAIL"
        else:
            status = "WARN"
        print(f"{stat['file']:<32} {status:<5} {stat['words']:>5} words   "
              f"{file_errors} errors, {file_warnings} warnings")
        for finding in file_findings:
            loc = f"line {finding['line']}" if finding["line"] else "ending"
            print(f"    [{finding['rule']} {finding['name']}] {loc}: {finding['match']!r}")
            print(f"        {finding['context']}")
    corpus_findings = by_file.get(CORPUS_LABEL, [])
    if corpus_findings:
        print(f"{CORPUS_LABEL}:")
        for finding in corpus_findings:
            print(f"    [{finding['rule']} {finding['name']}] {finding['match']}")
    if ledger_findings:
        print("Ledgers:")
        by_ledger: dict[str, list[dict]] = {}
        for finding in ledger_findings:
            by_ledger.setdefault(finding["file"], []).append(finding)
        for ledger, lfinds in by_ledger.items():
            print(f"    {ledger}: {len(lfinds)} finding(s)")
            for finding in lfinds:
                print(f"        [{finding['rule']} {finding['name']}] {finding['match']}")
    print("-" * 72)
    print(f"Total: {len(errors)} errors, {len(warnings)} warnings")

    if args.report:
        write_report(args.report, stats, findings, total_words)
        print(f"Report written to {args.report}")

    failed = bool(errors) or (args.strict and bool(warnings))
    return 1 if failed else 0


def write_report(report_path: Path, stats: list[dict], findings: list[dict], total_words: int) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    chapter_labels = {s["file"] for s in stats}
    by_file: dict[str, list[dict]] = {}
    for finding in findings:
        by_file.setdefault(finding["file"], []).append(finding)

    lines = [
        "# Story Status (generated)",
        "",
        "<!-- This file is generated by `python tools/check_story.py --report tests/STATUS.md`. Do not edit by hand. -->",
        "",
        "| Chapter | Title | Words | Status |",
        "|---|---|---:|---|",
    ]
    for stat in stats:
        file_findings = by_file.get(stat["file"], [])
        has_error = any(f["severity"] == "error" for f in file_findings)
        status = "FAIL" if has_error else ("WARN" if file_findings else "PASS")
        title = stat["title"].replace("|", "\\|")
        lines.append(f"| {stat['file']} | {title} | {stat['words']} | {status} |")

    lines += ["", f"**Total words:** {total_words}", ""]

    if findings:
        lines += ["## Findings", ""]
        for stat in stats:
            file_findings = by_file.get(stat["file"], [])
            if not file_findings:
                continue
            lines.append(f"### {stat['file']}")
            lines.append("")
            for finding in file_findings:
                loc = f"line {finding['line']}" if finding["line"] else "ending"
                lines.append(
                    f"- **[{finding['rule']} {finding['name']}]** ({finding['severity']}) {loc}: "
                    f"`{finding['match']}` — {finding['context']}"
                )
            lines.append("")
        corpus_findings = by_file.get(CORPUS_LABEL, [])
        if corpus_findings:
            lines.append(f"### {CORPUS_LABEL}")
            lines.append("")
            for finding in corpus_findings:
                lines.append(f"- **[{finding['rule']} {finding['name']}]** ({finding['severity']}): "
                             f"`{finding['match']}`")
            lines.append("")
        ledger_by_file: dict[str, list[dict]] = {}
        for finding in findings:
            if finding["file"] not in chapter_labels and finding["file"] != CORPUS_LABEL:
                ledger_by_file.setdefault(finding["file"], []).append(finding)
        for ledger, lfinds in ledger_by_file.items():
            lines.append(f"### {ledger}")
            lines.append("")
            for finding in lfinds:
                lines.append(f"- **[{finding['rule']} {finding['name']}]** ({finding['severity']}): "
                             f"{finding['match']}")
            lines.append("")
    else:
        lines += ["No findings.", ""]

    report_path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
