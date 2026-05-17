"""Aggregate per-exam Geography MCQ fragments into the topic bank.

Sourcing agents drop real extracted MCQs into geography_bank/_raw/<slug>.py,
each exposing:

    FRAGMENT = [
        {"q": "...", "opts": ["A","B","C","D"], "ans": 0-3,
         "explain": "...", "topic_id": 301-312},
        ...
    ]

This sequential builder (run AFTER all sourcing agents finish) groups every
fragment question by topic_id, de-duplicates by normalised question text, and
writes geography_bank/topic_<id>.py with QUESTIONS + SUBTOPIC_RANGES (the
curriculum subtopics, evenly split). No AI-generated content — authentic
extracted MCQs only.
"""

import glob
import importlib.util
import os
import re

from curriculum_geography import GEOGRAPHY_TOPICS

BANK_DIR = os.path.join(os.path.dirname(__file__), "geography_bank")
RAW_DIR = os.path.join(BANK_DIR, "_raw")

VALID_TOPIC_IDS = {t[0] for t in GEOGRAPHY_TOPICS}
SUBTOPICS = {t[0]: t[4] for t in GEOGRAPHY_TOPICS}


def _norm(s):
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def load_fragments():
    by_topic = {tid: [] for tid in VALID_TOPIC_IDS}
    seen = set()
    files = sorted(glob.glob(os.path.join(RAW_DIR, "*.py")))
    for path in files:
        name = os.path.basename(path)
        if name.startswith("_"):
            continue
        spec = importlib.util.spec_from_file_location(f"frag_{name}", path)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            print(f"  SKIP {name}: load error {e}")
            continue
        frag = getattr(mod, "FRAGMENT", [])
        kept = 0
        for q in frag:
            tid = q.get("topic_id")
            opts = list(q.get("opts", []))
            qt = q.get("q", "")
            ans = q.get("ans")
            if tid not in VALID_TOPIC_IDS:
                continue
            if len(opts) != 4 or not all(str(o).strip() for o in opts):
                continue
            if not isinstance(ans, int) or not (0 <= ans <= 3):
                continue
            if not qt or not qt.strip():
                continue
            key = _norm(qt)
            if key in seen:
                continue
            seen.add(key)
            by_topic[tid].append({
                "q": qt.strip(),
                "opts": [str(o).strip() for o in opts],
                "ans": ans,
                "explain": (q.get("explain") or "").strip(),
            })
            kept += 1
        print(f"  {name}: kept {kept}/{len(frag)}")
    return by_topic


def even_ranges(n, parts):
    """Split n items across `parts` contiguous ranges as evenly as possible."""
    if n == 0 or parts == 0:
        return []
    base, extra = divmod(n, parts)
    out, start = [], 0
    for i in range(parts):
        size = base + (1 if i < extra else 0)
        if size == 0:
            continue
        out.append((start, start + size))
        start += size
    return out


def write_topic_file(tid, questions):
    subs = SUBTOPICS[tid]
    ranges = even_ranges(len(questions), len(subs))
    lines = ["QUESTIONS = ["]
    for q in questions:
        lines.append("    " + repr(q) + ",")
    lines.append("]")
    lines.append("")
    if ranges:
        sr = [[subs[i], s, e] for i, (s, e) in enumerate(ranges)]
        lines.append("SUBTOPIC_RANGES = " + repr([tuple(x) for x in sr]))
    else:
        lines.append("SUBTOPIC_RANGES = []")
    lines.append("")
    path = os.path.join(BANK_DIR, f"topic_{tid}.py")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    by_topic = load_fragments()
    total = 0
    print()
    for tid, _, title, _, _ in GEOGRAPHY_TOPICS:
        qs = by_topic.get(tid, [])
        write_topic_file(tid, qs)
        total += len(qs)
        print(f"Topic {tid}: {title:<45} | {len(qs):>3} extracted MCQs")
    print(f"\nBuilt geography_bank from {total} extracted MCQs across "
          f"{len(GEOGRAPHY_TOPICS)} topics")


if __name__ == "__main__":
    main()
