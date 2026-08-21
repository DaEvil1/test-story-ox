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


def check_ledgers(ledgers_dir: Path, findings: list) -> None:
    ledger_checks = {
        "scene_ledger.yaml": check_scene_ledger,
        "ambiguity_ledger.yaml": check_ambiguity_ledger,
        "relationship_ledger.yaml": check_relationship_ledger,
        "promise_ledger.yaml": check_promise_ledger,
    }
    for filename, fn in ledger_checks.items():
        path = ledgers_dir / filename
        if path.exists():
            fn(path, findings)


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
    check_ledgers(args.ledgers_dir, findings)

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
