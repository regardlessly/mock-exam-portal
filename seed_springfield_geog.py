"""Seed Springfield Secondary School EOY 2022 Sec 1 Express Geography exam.

Source PDF is the official answer scheme with the questions reproduced inline,
so question text and model answers are taken directly from it.
"""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/springfield_geog.pdf"

init_db()


def add_q(db, paper_id, exam_dir, paper_num, num, part, text, marks, topic,
          pdf_page, crop_region, answer_text, mark_scheme, stem=None, topic_id=None):
    part_suffix = part.replace("(", "").replace(")", "") if part else ""
    img_name = f"q{paper_num}_{num}{part_suffix}.png"
    img_path = os.path.join(exam_dir, img_name)
    pg, top, bot = crop_region
    crop_question_image(PDF_PATH, pg, top, bot, img_path)
    q = Question(
        paper_id=paper_id, question_number=num, part=part, stem=stem,
        question_text=text, marks=marks, topic=topic, topic_id=topic_id,
        page_image=img_name, pdf_page=pdf_page,
    )
    db.add(q)
    db.flush()
    db.add(Answer(question_id=q.id, answer_text=answer_text, mark_scheme=mark_scheme))
    return q


def main():
    db = SessionLocal()

    school = db.query(School).filter(
        School.name == "Springfield Secondary School").first()
    if not school:
        school = School(name="Springfield Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(
        Exam.school_id == school.id, Exam.year == 2022,
        Exam.subject == "Geography").first()
    if existing:
        print(f"Springfield Geography 2022 already seeded (id={existing.id}). Re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id, title="End-of-Year Examination 2022", year=2022,
        level="Secondary 1 Express", subject="Geography",
        source_pdf="springfield_geog.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)

    # Single paper: 35 marks, 1h10m. Pages of the answer-scheme PDF (idx).
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=70, total_marks=35,
               date=date(2022, 10, 4),
               instructions="Section A: Fieldwork. Section B: Data Response / "
                            "Map Work. Section C: Structured Questions. "
                            "Answer all questions.")
    db.add(p1); db.flush()

    # ── Section A: Fieldwork (5m) — Q1 ──
    add_q(db, p1.id, exam_dir, 1, 1, "a",
        "Study Fig. 1, which shows the average daily water consumption per "
        "person per day in Singapore. With reference to Fig. 1, identify the "
        "years that had the largest change in the amount of water used per "
        "person per day.",
        1, "Climate / Data Interpretation", 2, (1, 0.05, 0.55),
        "2019 - 2020.", "B1",
        stem="Section A: Fieldwork. Question 1 refers to Fig. 1 (average daily "
             "water consumption per person per day in Singapore).",
        topic_id=305)

    add_q(db, p1.id, exam_dir, 1, 1, "b",
        "With reference to Fig. 1, calculate the mean daily water usage from "
        "2015 to 2020.",
        1, "Climate / Data Interpretation", 2, (1, 0.30, 0.95),
        "146 (148.333) litres/person/day. Working: "
        "(151+148+143+141+141+154)/6 = 146.333.", "B1",
        topic_id=305)

    add_q(db, p1.id, exam_dir, 1, 1, "c",
        "Study Fig. 2, a picture of MacRitchie Reservoir in Singapore. Draw a "
        "field-sketch of Fig. 2 with two labels and annotations about the "
        "usefulness of the reservoir.",
        3, "Water Resources & Management", 3, (2, 0.05, 0.95),
        "Accurate sketch according to figure; two labels; annotations of "
        "reservoir functions (e.g. water storage, recreational activities).",
        "B1 x3",
        topic_id=308)

    # ── Section B: Data Response / Map Work (10m) — Q2 & Q3 ──
    add_q(db, p1.id, exam_dir, 1, 2, "a",
        "Study Fig. 3, a topographical map of Mount Erin Area. State the "
        "general direction of Highton from Steeltown.",
        1, "Direction & Bearings", 4, (3, 0.05, 0.62),
        "West.", "B1",
        stem="Section B. Question 2 refers to Fig. 3 (topographical map of "
             "Mount Erin Area).",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 2, "b",
        "What is the 4-figure grid reference of point 'E'?",
        1, "Maps & Map Reading", 4, (3, 0.60, 0.70),
        "3456.", "B1",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 2, "c",
        "State the infrastructure found in grid square 4051.",
        1, "Maps & Map Reading", 4, (3, 0.69, 0.80),
        "Railway Station.", "B1",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 2, "d",
        "State if the natural resource found in grid square 3451 is renewable "
        "or non-renewable. Explain why.",
        2, "Water Resources & Management", 5, (3, 0.79, 0.98),
        "It is renewable, because the water in the lake will be continually "
        "replenished via the water cycle / when it rains.", "B1 x2",
        topic_id=308)

    add_q(db, p1.id, exam_dir, 1, 3, "a",
        "Study Fig. 4, the global distribution of mangroves. Based on Fig. 4, "
        "describe where mangrove forests are located.",
        2, "Mangrove & Coastal Vegetation", 5, (4, 0.05, 0.55),
        "They are located along coastal areas, in the equatorial region.",
        "B1 x2",
        stem="Question 3 refers to Fig. 4 (global distribution of mangroves).",
        topic_id=311)

    add_q(db, p1.id, exam_dir, 1, 3, "b",
        "List two characteristics of the climate where mangrove forests are "
        "located.",
        2, "Natural Vegetation & Biomes", 5, (4, 0.50, 0.78),
        "High temperature, more than 27 degrees C; high annual rainfall, more "
        "than 1500 mm. (Answers must include data.)", "B1 x2",
        topic_id=311)

    add_q(db, p1.id, exam_dir, 1, 3, "c",
        "Give one reason mangroves require calm water conditions.",
        1, "Mangrove & Coastal Vegetation", 5, (4, 0.77, 0.98),
        "So that their seedlings can take root without being washed away, OR "
        "so that sediments can accumulate to provide nutrients for the plant.",
        "B1",
        topic_id=311)

    # ── Section C: Structured Questions (20m) — Q4 & Q5 ──
    add_q(db, p1.id, exam_dir, 1, 4, "a",
        "Fig. 5 shows a diagram of the water cycle. Based on Fig. 5, give the "
        "definition of the process that is occurring at 'A' and 'B'.",
        2, "The Water Cycle", 6, (5, 0.05, 0.62),
        "A: water falls as rain or snow if it is cold enough "
        "(precipitation). B: water that seeps into the ground may be absorbed "
        "by plants or stored as groundwater (infiltration).", "B1 x2",
        stem="Section C: Structured Questions. Question 4 refers to Fig. 5 "
             "(a diagram of the water cycle).",
        topic_id=306)

    add_q(db, p1.id, exam_dir, 1, 4, "b",
        "Explain the difference between a flash flood and a river flood.",
        4, "Drainage Basins & Runoff", 6, (5, 0.61, 0.98),
        "Flash floods are caused by exceptionally heavy rainfall over a short "
        "period; water cannot infiltrate so it becomes surface runoff that "
        "quickly floods low-lying areas. River floods are caused by sustained "
        "heavy rainfall; water flows into rivers, raising their height until "
        "they overflow their banks and flood the surrounding area.", "B1 x4",
        topic_id=306)

    add_q(db, p1.id, exam_dir, 1, 4, "c",
        "Identify one domestic and one recreational use of water.",
        2, "Water Resources & Management", 7, (6, 0.05, 0.30),
        "Domestic: bathing, cooking, flushing the toilet. Recreational: "
        "fishing, sailing, canoeing.", "B1 x2",
        topic_id=308)

    add_q(db, p1.id, exam_dir, 1, 4, "d",
        "Explain how desalination helps Singapore to manage its water "
        "resources.",
        2, "Water Resources & Management", 7, (6, 0.29, 0.60),
        "Desalination removes the salt content from seawater through advanced "
        "membrane technology; this helps Singapore manage its water resources "
        "because it increases the amount of usable water available.", "B1 x2",
        topic_id=308)

    add_q(db, p1.id, exam_dir, 1, 5, "a",
        "Study Fig. 6, a sketch of an adaptation of some plants in a tropical "
        "rainforest. Based on Fig. 6, identify the adaptation shown and "
        "explain why trees in the tropical rainforest have this adaptation.",
        2, "Tropical Rainforest Ecosystems", 7, (6, 0.59, 0.98),
        "Drip tips, so that rainwater can flow off the leaf easily, "
        "preventing the growth of fungi and bacteria.", "B1 x2",
        stem="Question 5 refers to Fig. 6 (a sketch of a plant adaptation in "
             "a tropical rainforest).",
        topic_id=309)

    add_q(db, p1.id, exam_dir, 1, 5, "b",
        "Describe two characteristics of the undergrowth layer of a tropical "
        "rainforest. Provide reasons for your observations.",
        4, "Tropical Rainforest Ecosystems", 8, (7, 0.05, 0.45),
        "It is very dark, because sunlight is blocked by the thick canopy "
        "layer; the leaves are large, so as to absorb the maximum amount of "
        "available sunlight.", "B1 x4",
        topic_id=309)

    add_q(db, p1.id, exam_dir, 1, 5, "c",
        "Describe and explain two possible measures to manage forests "
        "sustainably.",
        4, "Tropical Rainforest Ecosystems", 8, (7, 0.44, 0.85),
        "Establishing protected areas (enact laws so people do not damage "
        "forests within them); regulating forestry activities (controlled "
        "logging balances economic benefit with conservation); rehabilitating "
        "disturbed areas (reforestation replants trees and reintroduces "
        "species); public education (people who understand forests' "
        "importance are more likely to protect them). Any two.", "B1 x4",
        topic_id=309)

    db.commit()
    print(f"Seeded Springfield Geography exam id={exam.id}: "
          f"Paper 1 ({len(p1.questions)} parts)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
