"""Seed curriculum topics and 2101 MCQs from math-quest into PostgreSQL."""

import re
import os

from models import (
    SessionLocal, CurriculumTopic, CurriculumSubtopic, BankQuestion, init_db
)

TOPICS_DIR = "/tmp/math-quest/content/math/topics"

init_db()


def extract_string(text, start, quote_char='"'):
    result = []
    i = start
    while i < len(text):
        ch = text[i]
        if ch == '\\' and i + 1 < len(text):
            nc = text[i + 1]
            if nc == quote_char:
                result.append(quote_char); i += 2
            elif nc == 'n':
                result.append('\n'); i += 2
            elif nc == '\\':
                result.append('\\'); i += 2
            elif nc == "'":
                result.append("'"); i += 2
            elif nc == '"':
                result.append('"'); i += 2
            elif nc == 't':
                result.append('\t'); i += 2
            else:
                result.append(ch + nc); i += 2
        elif ch == quote_char:
            return ''.join(result), i + 1
        else:
            result.append(ch); i += 1
    return ''.join(result), i


def parse_questions(content):
    q_match = re.search(r'export const questions.*?=\s*\[(.*)\]', content, re.DOTALL)
    if not q_match:
        return []
    block = q_match.group(1)
    questions = []
    for m in re.finditer(r'\{\s*q:\s*(["\'])', block):
        quote = m.group(1)
        q_start = m.end()
        q_text, q_end = extract_string(block, q_start, quote)

        opts_m = re.search(r'opts:\s*\[', block[q_end:q_end + 50])
        if not opts_m:
            continue
        opts_start = q_end + opts_m.end()
        try:
            bracket_end = block.index(']', opts_start)
        except ValueError:
            continue
        opts_raw = block[opts_start:bracket_end]
        opts = []
        for om in re.finditer(r"""(['"])((?:(?!\1).|\\.)*)\1""", opts_raw):
            opts.append(om.group(2).replace("\\'", "'").replace('\\"', '"'))

        ans_m = re.search(r'ans:\s*(\d+)', block[bracket_end:bracket_end + 30])
        if not ans_m:
            continue

        exp_m = re.search(r'explain:\s*(["\'])', block[bracket_end:])
        if not exp_m:
            continue
        exp_quote = exp_m.group(1)
        exp_start = bracket_end + exp_m.end()
        explain, _ = extract_string(block, exp_start, exp_quote)

        questions.append({
            'q': q_text,
            'opts': opts,
            'ans': int(ans_m.group(1)),
            'explain': explain,
        })
    return questions


def main():
    db = SessionLocal()

    # Clear existing curriculum data
    db.query(BankQuestion).delete()
    db.query(CurriculumSubtopic).delete()
    db.query(CurriculumTopic).delete()
    db.commit()

    total_questions = 0

    for f in sorted(os.listdir(TOPICS_DIR)):
        if not f.endswith('.ts'):
            continue
        with open(os.path.join(TOPICS_DIR, f)) as fh:
            content = fh.read()

        id_m = re.search(r'id:\s*(\d+)', content)
        sem_m = re.search(r'sem:\s*(\d+)', content)
        title_m = re.search(r"title:\s*'([^']+)'", content)
        desc_m = re.search(r"desc:\s*'([^']+)'", content)
        subtopic_headers = re.findall(r'//\s*[═=]+[^\n]*\n\s*//\s*(.+?)\s*\n', content)

        topic_id = int(id_m.group(1))

        # Insert topic
        topic = CurriculumTopic(
            id=topic_id,
            semester=int(sem_m.group(1)),
            title=title_m.group(1),
            description=desc_m.group(1),
        )
        db.add(topic)
        db.flush()

        # Insert subtopics
        subtopic_map = {}  # (start, end) -> subtopic_id
        for idx, st in enumerate(subtopic_headers):
            range_m = re.search(r'Q(\d+)[–\-](\d+)', st)
            q_range = f"Q{range_m.group(1)}–{range_m.group(2)}" if range_m else None
            sub = CurriculumSubtopic(
                topic_id=topic_id,
                title=st,
                question_range=q_range,
                sort_order=idx,
            )
            db.add(sub)
            db.flush()
            if range_m:
                start = int(range_m.group(1)) - 1
                end = int(range_m.group(2))
                subtopic_map[(start, end)] = sub.id

        # Parse and insert questions
        questions = parse_questions(content)
        for i, q in enumerate(questions):
            opts = q['opts']
            if len(opts) < 4:
                opts.extend([''] * (4 - len(opts)))

            # Find which subtopic this question belongs to
            sub_id = None
            for (start, end), sid in subtopic_map.items():
                if start <= i < end:
                    sub_id = sid
                    break

            bq = BankQuestion(
                topic_id=topic_id,
                subtopic_id=sub_id,
                question_number=i + 1,
                question_text=q['q'],
                option_a=opts[0],
                option_b=opts[1],
                option_c=opts[2],
                option_d=opts[3],
                correct_answer=q['ans'],
                explanation=q['explain'],
            )
            db.add(bq)
            total_questions += 1

        print(f"Topic {topic_id:>2}: {title_m.group(1):<40} | {len(questions):>3} Qs | {len(subtopic_headers)} subtopics")

    db.commit()
    print(f"\nSeeded {total_questions} questions across {len(os.listdir(TOPICS_DIR))} topics")
    db.close()


if __name__ == "__main__":
    main()
