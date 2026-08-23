#!/usr/bin/env python3
"""Statistical story analysis: frequency, rhythm, dialogue, voice, emotion.

Read-only. Complements tools/check_story.py (binary rules) with descriptive
metrics. Writes tests/ANALYSIS.md and prints a console summary.

Usage:
    python tools/analyze_story.py
    python tools/analyze_story.py --report tests/ANALYSIS.md

Requires: Python 3.10+ (stdlib only).
"""

import argparse
import math
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CHAPTERS_DIR = REPO_ROOT / "src" / "04-chapters"
DEFAULT_REPORT = REPO_ROOT / "tests" / "ANALYSIS.md"

STOPWORDS = set("""
a an the and or but if then than that this these those of to in on at by for
with from as is are was were be been being am do does did have has had will
would can could shall should may might must not no nor so too very just only
even also still yet again once about above after before between during
through under over up down out off further there here when where why how all
any both each few more most other some such own same her hers his him she he
they them their it its itself i me my we our you your what which who whom
into onto upon along across behind beyond within without said says say told
ask asked asks one two three back away toward towards against because while
until since though although whether like unlike per via
""".split())

# Emotion lexicons — small, hand-picked, documented. Not exhaustive; they are
# tripwires for absence (a category with zero hits) and gross imbalance.
EMOTION_LEXICONS = {
    "fear/dread": [
        "afraid", "fear", "feared", "dread", "terror", "shudder", "shuddered",
        "tremble", "trembled", "tremor", "warning", "danger", "refusal",
        "refuse", "refused", "shook", "shake", "shaken",
    ],
    "grief": [
        "grief", "lost", "loss", "gone", "absent", "ache", "hollow", "wound",
        "weep", "wept", "cry", "cried", "mourn", "sorrow", "missing",
    ],
    "joy/warmth": [
        "laugh", "laughter", "laughed", "smile", "smiled", "grin", "grinned",
        "joy", "delight", "glad", "gentle", "comfort", "love", "loved",
    ],
    "anger": [
        "angry", "anger", "fury", "rage", "bitter", "resent", "resented",
        "snap", "snapped", "harsh", "furious",
    ],
    "awe/wonder": [
        "wonder", "wondered", "marvel", "marveled", "vast", "impossible",
        "awe", "strange",
    ],
}

SPEECH_ATTR_RE = re.compile(
    r"\b(Keji|Ari|Sera|Ira|Lio|he|she|it|the voice|a voice)\s+"
    r"(said|asked|whispered|murmured|added|answered|went on|replied|spoke)\b",
    re.IGNORECASE,
)
DIALOGUE_RE = re.compile(r'"[^"]+"')
FUNCTION_WORDS = """
i me my we our you your he him his she her it its they them their what which
who whom this that these those am is are was were be been being have has had
do does did will would can could shall should may might must not no and but
or if then than so as at by for with of to in on
""".split()


def normalize(text: str) -> str:
    return (text.replace("\u2019", "'").replace("\u2018", "'")
                .replace("\u201c", '"').replace("\u201d", '"'))


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z']+", text.lower())


def content_tokens(text: str) -> list[str]:
    return [t for t in tokens(text) if t not in STOPWORDS and len(t) > 2]


def sentences(text: str) -> list[str]:
    body = re.sub(r"^Chapter [^\n]*", "", text, flags=re.IGNORECASE)
    parts = re.split(r"(?<=[.!?])\s+", body.replace("\n", " "))
    return [s.strip() for s in parts if s.strip()]


def shannon(values: list[float]) -> float:
    if not values:
        return 0.0
    total = sum(values)
    return -sum((v / total) * math.log2(v / total) for v in values if v > 0)


def cosine(a: Counter, b: Counter) -> float:
    keys = set(a) | set(b)
    dot = sum(a[k] * b[k] for k in keys)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


def pearson(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    vx = sum((x - mx) ** 2 for x in xs) ** 0.5
    vy = sum((y - my) ** 2 for y in ys) ** 0.5
    return cov / (vx * vy) if vx and vy else 0.0


def chapter_num_safe(name: str) -> int:
    m = re.search(r"(\d+)", name)
    return int(m.group(1)) if m else 0


def main() -> int:
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Analyze story statistics.")
    parser.add_argument("--chapters-dir", type=Path, default=DEFAULT_CHAPTERS_DIR)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    if not args.report.is_absolute():
        args.report = REPO_ROOT / args.report

    files = sorted(
        f for f in args.chapters_dir.glob("*.md") if f.name.upper() != "README.MD"
    )
    texts = {f.name: normalize(f.read_text(encoding="utf-8")) for f in files}
    corpus = "\n".join(texts.values())
    total_words = len(corpus.split())
    is_story_corpus = args.chapters_dir.resolve() == DEFAULT_CHAPTERS_DIR.resolve()

    out: list[str] = [
        "# Story Analysis (generated)",
        "",
        "<!-- Generated by `python tools/analyze_story.py`. Do not edit by hand. -->",
        "",
        f"Chapters: {len(files)}   Words: {total_words}",
        "",
    ]

    # 1. Word frequency (content words)
    freq = Counter(content_tokens(corpus))
    out += ["## Content-word frequency", "",
            "| Word | Count | per 10k |", "|---|---:|---:|"]
    flagged = []
    for word, count in freq.most_common(25):
        rate = count * 10000 / total_words
        marker = " **HIGH**" if rate > 60 else ""
        if rate > 60:
            flagged.append(word)
        out.append(f"| {word} | {count} | {rate:.0f}{marker} |")
    out += ["", f"Flagged (>60/10k): {', '.join(flagged) if flagged else 'none'}", ""]

    # 2. Repeated trigrams across chapters
    tri_counts: Counter = Counter()
    tri_chapters: dict[tuple, set] = {}
    for name, text in texts.items():
        toks = tokens(text)
        for i in range(len(toks) - 2):
            tri = (toks[i], toks[i + 1], toks[i + 2])
            if any(t in STOPWORDS and t not in ("her", "his", "the", "a", "of", "to") for t in tri):
                pass
            tri_counts[tri] += 1
            tri_chapters.setdefault(tri, set()).add(name)
    multi_chapter = [
        (tri, c, len(tri_chapters[tri]))
        for tri, c in tri_counts.items()
        if c >= 4 and len(tri_chapters[tri]) >= 2
    ]
    multi_chapter.sort(key=lambda x: -x[1])
    out += ["## Repeated trigrams (count >= 4, spanning >= 2 chapters)", ""]
    if multi_chapter:
        out += ["| Trigram | Count | Chapters |", "|---|---:|---:|"]
        for (a, b, c), count, nch in multi_chapter[:15]:
            out.append(f"| {a} {b} {c} | {count} | {nch} |")
    else:
        out += ["None."]
    out.append("")

    # 3. Sentence rhythm
    all_sents = sentences(corpus)
    lens = [len(s.split()) for s in all_sents]
    mean_len = sum(lens) / len(lens)
    var = sum((x - mean_len) ** 2 for x in lens) / len(lens)
    stdev = var ** 0.5
    fragments = sum(1 for x in lens if x <= 3)
    dashes = corpus.count("\u2014") + corpus.count("--")
    out += [
        "## Sentence rhythm",
        "",
        f"- Sentences: {len(lens)}  mean length {mean_len:.1f}  stdev {stdev:.1f}",
        f"- Fragments (<=3 words): {fragments} ({fragments * 100 / len(lens):.0f}%)",
        f"- Em-dashes: {dashes} ({dashes * 10000 / total_words:.0f} per 10k)",
        "",
    ]

    # 3b. Sentence-opener dominance
    openers = Counter()
    for s in all_sents:
        first = tokens(s)
        if first:
            openers[first[0]] += 1
    top_openers = openers.most_common(10)
    out += ["## Sentence openers (top 10)", "", "| Opener | Count | Share |", "|---|---:|---:|"]
    for word, n in top_openers:
        share = n * 100 / max(len(all_sents), 1)
        marker = " **DOMINANT**" if share > 15 else ""
        out.append(f"| {word} | {n} | {share:.0f}%{marker} |")
    out.append("")

    # 3c. Abstract-noun-as-agent constructions
    ABSTRACT_AGENT_RE = re.compile(
        r"\b(?:the|its|her|his|their)?\s?"
        r"(refusal|silence|word|words|idea|memory|pressure|weight|sound|"
        r"quiet|stillness|truth|sentence|phrase|name|grief|fear)\s+"
        r"(landed|land|came|rose|sat|settle|settled|settles|pressed|presses|"
        r"hummed|hums|held|stay|stayed|remained|thrummed|pulsed|tightened|"
        r"arrived|moved|went|lodge|lodged)\b", re.IGNORECASE)
    agent_hits = ABSTRACT_AGENT_RE.findall(corpus)
    out += ["## Abstract-noun-as-agent", "",
            f"Count: {len(agent_hits)} ({len(agent_hits) * 10000 / total_words:.0f} per 10k)",
            ""]
    if agent_hits:
        combo = Counter(f"{a} {b}".lower() for a, b in agent_hits)
        out += ["| Construction | Count |", "|---|---:|"]
        for combo_text, n in combo.most_common(12):
            out.append(f"| {combo_text} | {n} |")
        out.append("")

    # 4. Dialogue share per chapter
    out += ["## Dialogue share", "", "| Chapter | Dialogue % |", "|---|---:|"]
    for name, text in texts.items():
        quoted = sum(len(m) for m in DIALOGUE_RE.findall(text))
        pct = quoted * 100 / max(len(text), 1)
        out.append(f"| {name} | {pct:.0f}% |")
    quoted_total = sum(len(m) for m in DIALOGUE_RE.findall(corpus))
    out += [f"| **corpus** | **{quoted_total * 100 / max(len(corpus), 1):.0f}%** |", ""]

    # 5. Speaker attribution counts
    speakers = Counter()
    for m in SPEECH_ATTR_RE.finditer(corpus):
        speakers[m.group(1).lower()] += 1
    out += ["## Speech attributions", ""]
    if speakers:
        out += ["| Speaker | Lines |", "|---|---:|"]
        for spk, n in speakers.most_common():
            out.append(f"| {spk} | {n} |")
    else:
        out += ["None found."]
    out.append("")

    # 6. Voice fingerprints (function-word profiles of quoted speech)
    out += ["## Voice fingerprint similarity (quoted speech)", ""]
    profiles: dict[str, Counter] = {}
    speech_by_speaker: dict[str, list[str]] = {}
    for name, text in texts.items():
        for match in DIALOGUE_RE.finditer(text):
            quote = match.group(0)
            window = text[max(0, match.start() - 80):match.end() + 80]
            am = SPEECH_ATTR_RE.search(window)
            spk = am.group(1).lower() if am else None
            if spk in ("keji", "ari", "sera", "ira"):
                profiles.setdefault(spk, Counter()).update(
                    t for t in tokens(quote) if t in FUNCTION_WORDS)
                speech_by_speaker.setdefault(spk, []).append(quote)
    named = {k: v for k, v in profiles.items() if sum(v.values()) >= 20}
    if len(named) >= 2:
        keys = sorted(named)
        out += ["| Pair | Similarity |", "|---|---:|"]
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                sim = cosine(named[keys[i]], named[keys[j]])
                flag = " **SIMILAR**" if sim > 0.85 else ""
                out.append(f"| {keys[i]} vs {keys[j]} | {sim:.2f}{flag} |")
        out += ["", "(Similarity > 0.85 suggests voices are hard to tell apart.)", ""]
    else:
        out += ["Not enough attributed dialogue for fingerprinting.", ""]

    # 6b. Dialogue music per speaker
    out += ["## Dialogue music (per speaker)", "",
            "| Speaker | Lines | Avg words | Questions % | Contractions/line |",
            "|---|---:|---:|---:|---:|"]
    for spk in sorted(speech_by_speaker):
        lines = speech_by_speaker[spk]
        if len(lines) < 4:
            continue
        word_counts = [len(tokens(q)) for q in lines]
        questions = sum(1 for q in lines if "?" in q)
        contractions = sum(q.count("'") + q.count("\u2019") for q in lines)
        avg = sum(word_counts) / len(word_counts)
        out.append(f"| {spk} | {len(lines)} | {avg:.1f} | {questions * 100 / len(lines):.0f}% | "
                   f"{contractions / len(lines):.2f} |")
    out.append("")

    # 7. Emotion lexicons
    out += ["## Emotion lexicon hits", "", "| Category | Corpus | per 10k | ch1 | ch2 | ch3 | ch4 | ch5 | ch6 | ch7 | ch8 | ch9 | ch10 | ch11 |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    empty_categories = []
    emotion_by_chapter: dict[str, dict[str, int]] = {}
    for category, words in EMOTION_LEXICONS.items():
        row = []
        total = 0
        for name, text in texts.items():
            toks = tokens(text)
            n = sum(toks.count(w) for w in words)
            total += n
            row.append(n)
            emotion_by_chapter.setdefault(name, {})[category] = n
        rate = total * 10000 / total_words
        if total == 0:
            empty_categories.append(category)
        cells = " | ".join(str(n) for n in row)
        out.append(f"| {category} | {total} | {rate:.1f} | {cells} |")
    out.append("")
    if empty_categories:
        out += [f"**Zero-hit categories:** {', '.join(empty_categories)}", ""]

    # 8. Motif tracker + co-occurrence
    motif_words = {
        "wall": ["wall", "walls"], "pulse": ["pulse", "pulsed", "pulsing", "pulses"],
        "hum": ["hum", "hums", "hummed", "humming"], "coin": ["coin"],
        "warm": ["warm", "warmed", "warmth"], "seam": ["seam", "seams"],
        "ink": ["ink"], "tide/water": ["tide", "tides", "water", "ocean", "sea", "tidepool"],
        "palimpsest-layer": ["palimpsest", "layer", "layers", "varnish", "script"],
        "limit": ["limit"],
    }
    out += ["## Motif & image tracker", "", "| Term | Count | per 10k |", "|---|---:|---:|"]
    for label, words in motif_words.items():
        n = sum(tokens(corpus).count(w) for w in words)
        out.append(f"| {label} | {n} | {n * 10000 / total_words:.0f} |")
    out.append("")

    # 8b. Motif co-occurrence (paragraph-level): catches image-family monotony —
    # pairs that ALWAYS appear together are one image, not two.
    fam_totals = {k: 0 for k in motif_words}
    cooc = {k: Counter() for k in motif_words}
    for para in re.split(r"\n\s*\n", corpus):
        para_toks = tokens(para)
        present = [k for k, ws in motif_words.items() if any(para_toks.count(w) for w in ws)]
        for k in present:
            fam_totals[k] += 1
            for other in present:
                if other != k:
                    cooc[k][other] += 1
    pairs = []
    seen = set()
    for k in motif_words:
        for other, n in cooc[k].items():
            key = tuple(sorted((k, other)))
            if key in seen:
                continue
            seen.add(key)
            denom = max(min(fam_totals[k], fam_totals[other]), 1)
            pairs.append((n / denom, n, k, other))
    pairs.sort(reverse=True)
    out += ["### Motif co-occurrence (paragraph level)", "",
            "| Pair | Together | % of rarer family |", "|---|---:|---:|"]
    for ratio, n, a, b in pairs[:10]:
        marker = " **FUSED**" if ratio > 0.6 else ""
        out.append(f"| {a} + {b} | {n} | {ratio * 100:.0f}%{marker} |")
    out += ["", "(*FUSED* = the pair appears together more than 60% of the rarer term's "
            "paragraphs — two labels, one image.)", ""]

    # 9. Staleness report — chapter similarity & information density
    out += ["## Staleness report", ""]
    names = sorted(texts.keys())
    vecs = {n: Counter(content_tokens(texts[n])) for n in names}
    trisets = {}
    for n in names:
        toks = tokens(texts[n])
        trisets[n] = {(toks[i], toks[i + 1], toks[i + 2])
                      for i in range(len(toks) - 2)}

    def chapter_num(name: str) -> int:
        m = re.search(r"(\d+)", name)
        return int(m.group(1)) if m else 0

    cos_pairs = []
    tri_pairs = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            cos_pairs.append((cosine(vecs[a], vecs[b]), a, b))
            union = trisets[a] | trisets[b]
            jac = len(trisets[a] & trisets[b]) / len(union) if union else 0.0
            tri_pairs.append((jac, a, b))

    out += ["### Lexical similarity (top pairs)", "",
            "| Pair | Cosine |", "|---|---:|"]
    for sim, a, b in sorted(cos_pairs, reverse=True)[:5]:
        marker = " **STALE?**" if sim > 0.70 else ""
        out.append(f"| ch{chapter_num(a)} ~ ch{chapter_num(b)} | {sim:.2f}{marker} |")
    out.append("")

    out += ["### Shared-trigram overlap (top pairs)", "",
            "| Pair | Jaccard |", "|---|---:|"]
    for jac, a, b in sorted(tri_pairs, reverse=True)[:5]:
        marker = " **STALE?**" if jac > 0.12 else ""
        out.append(f"| ch{chapter_num(a)} ~ ch{chapter_num(b)} | {jac:.3f}{marker} |")
    out.append("")

    # Words per unit of new information (story corpus only — needs scene ledger)
    ledger_path = REPO_ROOT / "tests" / "analysis" / "scene_ledger.yaml"
    if is_story_corpus and ledger_path.exists():
        import yaml
        ledger = yaml.safe_load(ledger_path.read_text(encoding="utf-8")) or {}
        info_per_chapter: dict[int, int] = {}
        for scene in ledger.get("scenes", []):
            ch = scene.get("chapter")
            info_per_chapter[ch] = info_per_chapter.get(ch, 0) + len(scene.get("new_info") or [])
        out += ["### Words per new-information unit", "",
                "| Chapter | Words | New info | Words/info |", "|---|---:|---:|---:|"]
        rows = []
        for n in names:
            ch = chapter_num(n)
            infos = info_per_chapter.get(ch, 0)
            w = len(texts[n].split())
            ratio = w / infos if infos else None
            rows.append((ratio if ratio is not None else 9999, ch, w, infos))
        for ratio, ch, w, infos in sorted(rows, reverse=True):
            shown = f"{ratio:.0f}" if infos else "—"
            marker = " **EXPENSIVE**" if infos and ratio > 400 else ""
            out.append(f"| ch{ch} | {w} | {infos} | {shown}{marker} |")
        out.append("")

    # Flat chapters (tension never moves inside a chapter) — story corpus only
    tension_path = REPO_ROOT / "tests" / "analysis" / "tension_ledger.yaml"
    if is_story_corpus and tension_path.exists():
        import yaml
        tdata = yaml.safe_load(tension_path.read_text(encoding="utf-8")) or {}
        by_ch: dict[int, list] = {}
        for s in tdata.get("scenes", []):
            sid = s.get("id", "")
            m = re.search(r"ch(\d+)", sid)
            if m:
                by_ch.setdefault(int(m.group(1)), []).append(s.get("tension", 0))
        flat = [ch for ch, ts in sorted(by_ch.items()) if ts and max(ts) - min(ts) <= 1]
        out += ["### Flat chapters (internal tension spread <= 1)", ""]
        out += [f"ch{', ch'.join(str(c) for c in flat)}" if flat else "None.", ""]

    # 10. Coupling: tension x emotional breadth (Dread Triangle health)
    tension_path = REPO_ROOT / "tests" / "analysis" / "tension_ledger.yaml"
    if is_story_corpus and tension_path.exists():
        import yaml
        tdata = yaml.safe_load(tension_path.read_text(encoding="utf-8")) or {}
        tens_by_ch: dict[int, list] = {}
        for s in tdata.get("scenes", []):
            m = re.search(r"ch(\d+)", s.get("id", ""))
            if m and isinstance(s.get("tension"), (int, float)):
                tens_by_ch.setdefault(int(m.group(1)), []).append(s["tension"])

        out += ["## Coupling: tension x emotional breadth", "",
                "Peak chapters running on <=2 feeling-categories are on plot, not dread.",
                "",
                "| Chapter | Avg tension | Emotion cats | Total hits | Note |",
                "|---|---:|---:|---:|---|"]
        xs, ys = [], []
        narrow_peaks = []
        for ch in sorted(tens_by_ch):
            name = next((n for n in texts if chapter_num_safe(n) == ch), None)
            if name is None:
                continue
            avg_t = sum(tens_by_ch[ch]) / len(tens_by_ch[ch])
            cats = emotion_by_chapter.get(name, {})
            n_cats = sum(1 for v in cats.values() if v > 0)
            total_hits = sum(cats.values())
            note = ""
            if avg_t >= 7 and n_cats <= 2:
                note = "**NARROW PEAK**"
                narrow_peaks.append(ch)
            xs.append(avg_t)
            ys.append(n_cats)
            out.append(f"| ch{ch} | {avg_t:.1f} | {n_cats} | {total_hits} | {note} |")
        out.append("")
        if len(xs) >= 3:
            r = pearson(xs, ys)
            out += [f"Pearson r (avg tension vs emotion categories): **{r:.2f}**", ""]
            if narrow_peaks:
                out += [f"Narrow peaks: ch{', ch'.join(str(c) for c in narrow_peaks)} "
                        "— consider seeding one non-fear feeling inside the spike.", ""]

    args.report.write_text("\n".join(out), encoding="utf-8")
    print(f"Analysis written to {args.report.relative_to(REPO_ROOT)}")
    print(f"Words: {total_words}; flagged high-freq: {', '.join(flagged) if flagged else 'none'}; "
          f"zero-hit emotion categories: {', '.join(empty_categories) if empty_categories else 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
