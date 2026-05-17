"""Seed Sec 1 普通华文 (Normal Chinese, G3) curriculum topics + MCQ bank.

Mirrors seed_curriculum_science.py but for Chinese. Topic IDs are 201-212.
Question modules live in chinese_bank/topic_<id>.py, each exposing
QUESTIONS = [{"q":..., "opts":[4], "ans":0-3, "explain":...}, ...]
and SUBTOPIC_RANGES = [("子主题", start_idx, end_idx), ...] (optional).

ALL text is pure CJK — no KaTeX, no `$`.
"""

import importlib.util
import os

from models import (
    SessionLocal, CurriculumTopic, CurriculumSubtopic, BankQuestion, init_db
)
from curriculum_chinese import CHINESE_TOPICS

BANK_DIR = os.path.join(os.path.dirname(__file__), "chinese_bank")

init_db()


def load_topic_questions(topic_id):
    path = os.path.join(BANK_DIR, f"topic_{topic_id}.py")
    if not os.path.exists(path):
        return [], []
    spec = importlib.util.spec_from_file_location(f"topic_{topic_id}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "QUESTIONS", []), getattr(mod, "SUBTOPIC_RANGES", [])


def main():
    db = SessionLocal()

    # Clear existing Chinese curriculum (idempotent re-seed)
    chi_topic_ids = [t[0] for t in CHINESE_TOPICS]
    db.query(BankQuestion).filter(BankQuestion.topic_id.in_(chi_topic_ids)).delete(synchronize_session=False)
    db.query(CurriculumSubtopic).filter(CurriculumSubtopic.topic_id.in_(chi_topic_ids)).delete(synchronize_session=False)
    db.query(CurriculumTopic).filter(CurriculumTopic.id.in_(chi_topic_ids)).delete(synchronize_session=False)
    db.commit()

    total_q = 0
    for tid, sem, title, desc, subtopics in CHINESE_TOPICS:
        topic = CurriculumTopic(
            id=tid, semester=sem, title=title,
            description=desc, subject="Chinese",
        )
        db.add(topic)
        db.flush()

        questions, ranges = load_topic_questions(tid)

        # Subtopics: use explicit ranges if provided, else flat list
        subtopic_rows = []
        if ranges:
            for idx, (st_title, s, e) in enumerate(ranges):
                sub = CurriculumSubtopic(
                    topic_id=tid, title=st_title,
                    question_range=f"Q{s+1}-{e}", sort_order=idx,
                )
                db.add(sub)
                db.flush()
                subtopic_rows.append((sub.id, s, e))
        else:
            for idx, st_title in enumerate(subtopics):
                sub = CurriculumSubtopic(
                    topic_id=tid, title=st_title, sort_order=idx,
                )
                db.add(sub)
                db.flush()

        for i, q in enumerate(questions):
            opts = list(q["opts"]) + [""] * (4 - len(q["opts"]))
            sub_id = None
            for sid, s, e in subtopic_rows:
                if s <= i < e:
                    sub_id = sid
                    break
            db.add(BankQuestion(
                topic_id=tid, subtopic_id=sub_id, question_number=i + 1,
                question_text=q["q"],
                option_a=opts[0], option_b=opts[1],
                option_c=opts[2], option_d=opts[3],
                correct_answer=q["ans"], explanation=q.get("explain", ""),
            ))
            total_q += 1

        print(f"Topic {tid}: {title:<20} | {len(questions):>3} Qs | {len(subtopics)} subtopics")

    db.commit()
    print(f"\nSeeded {len(CHINESE_TOPICS)} Chinese topics, {total_q} MCQs")
    db.close()


if __name__ == "__main__":
    main()
