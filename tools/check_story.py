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


def main() -> int:
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Run automated story checks.")
    parser.add_argument("--chapters-dir", type=Path, default=DEFAULT_CHAPTERS_DIR)
    parser.add_argument("--rules", type=Path, default=DEFAULT_RULES)
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
    print("-" * 72)
    print(f"Total: {len(errors)} errors, {len(warnings)} warnings")

    if args.report:
        write_report(args.report, stats, findings, total_words)
        print(f"Report written to {args.report}")

    failed = bool(errors) or (args.strict and bool(warnings))
    return 1 if failed else 0


def write_report(report_path: Path, stats: list[dict], findings: list[dict], total_words: int) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
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
    else:
        lines += ["No findings.", ""]

    report_path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
