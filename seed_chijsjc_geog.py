"""Seed CHIJ St Joseph's Convent Semestral Assessment 1 (2012)
Secondary 1 Express Geography exam."""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/chijsjc_geog.pdf"

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

    school = (db.query(School)
              .filter(School.name == "CHIJ St Joseph's Convent").first())
    if not school:
        school = School(name="CHIJ St Joseph's Convent")
        db.add(school)
        db.flush()

    existing = (db.query(Exam)
                .filter(Exam.school_id == school.id, Exam.year == 2012,
                        Exam.subject == "Geography")
                .first())
    if existing:
        print(f"CHIJ SJC Geography 2012 already seeded (id={existing.id}). "
              f"Re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id, title="Semestral Assessment 1 (2012)", year=2012,
        level="Secondary 1 Express", subject="Geography",
        source_pdf="Sec-1-Geography-2013.pdf (CHIJ St Joseph's Convent SA1 2012)",
        status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)

    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=105,
               total_marks=60, date=date(2012, 5, 2),
               instructions="Answer all questions. Section A: Mapwork [10]. "
                            "Section B: Basic Techniques [5]. "
                            "Section C: Structured Questions [45].")
    db.add(p1); db.flush()

    # ── SECTION A — MAPWORK [10] ──
    # Q1 page 3 (idx 1) — world map
    map_stem = "Figure 1 shows a world map with features labelled A to E."
    add_q(db, p1.id, exam_dir, 1, 1, "a",
        "Identify the continent labelled A.",
        1, "World Map - Continents", 3, (1, 0.05, 0.78),
        "South America", "B1", stem=map_stem, topic_id=301)
    add_q(db, p1.id, exam_dir, 1, 1, "b",
        "Identify the latitude labelled B.",
        1, "Lines of Latitude", 3, (1, 0.62, 0.70),
        "Equator", "B1", topic_id=301)
    add_q(db, p1.id, exam_dir, 1, 1, "c",
        "Identify the latitude labelled C.",
        1, "Lines of Latitude", 3, (1, 0.70, 0.76),
        "Tropic of Capricorn", "B1", topic_id=301)
    add_q(db, p1.id, exam_dir, 1, 1, "d",
        "Identify the longitude labelled D.",
        1, "Lines of Longitude", 3, (1, 0.76, 0.82),
        "Greenwich / Prime Meridian", "B1", topic_id=301)
    add_q(db, p1.id, exam_dir, 1, 1, "e",
        "Identify the ocean labelled E.",
        1, "World Map - Oceans", 3, (1, 0.82, 0.90),
        "Indian Ocean", "B1", topic_id=301)

    # Q2 page 4 (idx 2) — coastal area map
    coast_stem = ("Figure 2 shows a coastal area with a topographical map "
                  "(jetties P and Q, Capuccino Head, Big Mocca Island, "
                  "grid squares).")
    add_q(db, p1.id, exam_dir, 1, 2, "a",
        "Name the physical feature located in grid square 2741.",
        1, "Mapwork - Grid Squares", 4, (2, 0.06, 0.70),
        "An island / ridge / hill", "B1", stem=coast_stem, topic_id=301)
    add_q(db, p1.id, exam_dir, 1, 2, "b",
        "What is the 6-figure grid reference of Y at Capuccino Head?",
        1, "Mapwork - 6-Figure Grid Reference", 4, (2, 0.70, 0.76),
        "256424", "B1", topic_id=301)
    add_q(db, p1.id, exam_dir, 1, 2, "c",
        "Indicate the direction of Capuccino Head from Big Mocca Island.",
        1, "Mapwork - Direction", 4, (2, 0.76, 0.82),
        "West", "B1", topic_id=301)
    add_q(db, p1.id, exam_dir, 1, 2, "d",
        "Measure the bearing of jetty Q from jetty P.",
        1, "Mapwork - Bearings", 4, (2, 0.82, 0.88),
        "139 deg (accept 139 deg +/- 2 deg)", "B1", topic_id=301)
    add_q(db, p1.id, exam_dir, 1, 2, "e",
        "Calculate the distance between jetty Q and jetty P in kilometres. "
        "Round up your answer to TWO decimal places.",
        1, "Mapwork - Measuring Distance", 4, (2, 0.88, 0.96),
        "2.94 to 3.13 km", "B1", topic_id=301)

    # ── SECTION B — BASIC TECHNIQUES [5] ──
    # Q3 page 5 (idx 3) — climograph
    climo_stem = ("Figure 3 shows the climograph of Country X (mean monthly "
                  "precipitation as bars and mean temperature as a line).")
    add_q(db, p1.id, exam_dir, 1, 3, "a",
        "What is the lowest temperature for Country X?",
        1, "Climograph Reading", 5, (3, 0.05, 0.62),
        "24.5 deg C / about 25 deg C", "B1", stem=climo_stem, topic_id=305)
    add_q(db, p1.id, exam_dir, 1, 3, "b",
        "What is the highest temperature for Country X?",
        1, "Climograph Reading", 5, (3, 0.62, 0.70),
        "27.8 deg C / about 28 deg C", "B1", topic_id=305)
    add_q(db, p1.id, exam_dir, 1, 3, "c",
        "Calculate the temperature range for Country X.",
        1, "Temperature Range", 5, (3, 0.70, 0.76),
        "About 3.2 to 3.4 deg C", "B1", topic_id=305)
    add_q(db, p1.id, exam_dir, 1, 3, "d",
        "In which month did Country X experience the highest rainfall?",
        1, "Climograph Reading", 5, (3, 0.76, 0.82),
        "October", "B1", topic_id=305)
    add_q(db, p1.id, exam_dir, 1, 3, "e",
        "What type of climate does Country X have?",
        1, "Climate Types", 5, (3, 0.82, 0.90),
        "Tropical climate (hot and wet)", "B1", topic_id=305)

    # ── SECTION C — STRUCTURED QUESTIONS [45] ──
    # Q4 page 6 (idx 4)
    env_stem = ("Figure 4 and Figure 5 show different environments (a natural "
                "desert/dryland scene and a built/man-made scene).")
    add_q(db, p1.id, exam_dir, 1, 4, "ai",
        "Identify the different environments shown in Figure 4 and Figure 5.",
        2, "Environments", 6, (4, 0.05, 0.55),
        "Figure 4: a natural / physical environment. Figure 5: a built / "
        "man-made (human) environment.", "B1 x 2", stem=env_stem,
        topic_id=302)
    add_q(db, p1.id, exam_dir, 1, 4, "aii",
        "Use evidence from Figure 4 and Figure 5 to support your answer.",
        4, "Environments - Evidence", 6, (4, 0.45, 0.62),
        "Figure 4 shows natural features (no buildings, natural vegetation / "
        "bare ground). Figure 5 shows man-made features (buildings, roads "
        "built by people).", "B1 x 4", topic_id=302)
    add_q(db, p1.id, exam_dir, 1, 4, "b",
        "Name THREE ways in which humans can destroy the fragile Earth.",
        3, "Human Impact on Earth", 6, (4, 0.62, 0.72),
        "Mining; deforestation; burning of forest/fossil fuels; pollution; "
        "global warming; littering (any three).", "B1 x 3", topic_id=309)
    add_q(db, p1.id, exam_dir, 1, 4, "c",
        "If you were lost in the Kalahari Desert and need to live with the "
        "!Kung Bushmen, how would you adapt your lifestyle to obtain the "
        "basic needs of food and shelter?",
        6, "Adapting to the Environment", 6, (4, 0.72, 0.92),
        "Learn to hunt animals and gather wild plants for food; find and "
        "store water; build simple shelters from natural materials; wear "
        "suitable clothing; move to places where water and food can be "
        "found; collect/store rainwater.", "B1 x 6", topic_id=311)

    # Q5 page 7 (idx 5) — weather instruments
    add_q(db, p1.id, exam_dir, 1, 5, "ai",
        "Figure 6 shows a weather instrument (a louvred box on a stand). "
        "Identify the weather instrument shown in Figure 6.",
        1, "Weather Instruments", 7, (5, 0.05, 0.55),
        "Stevenson screen", "B1", topic_id=303)
    add_q(db, p1.id, exam_dir, 1, 5, "aii",
        "List the instruments placed inside this weather instrument.",
        2, "Weather Instruments", 7, (5, 0.55, 0.62),
        "Maximum thermometer; minimum thermometer; wet-bulb thermometer; "
        "dry-bulb thermometer; barometer (any relevant).", "B1 x 2",
        topic_id=303)
    add_q(db, p1.id, exam_dir, 1, 5, "aiii",
        "Explain the function of the louvres.",
        2, "Stevenson Screen", 7, (5, 0.62, 0.70),
        "The louvres allow free flow of air around the instruments while "
        "blocking direct sunlight, so air temperature is measured "
        "accurately.", "B1 x 2", topic_id=303)
    add_q(db, p1.id, exam_dir, 1, 5, "bi",
        "Figure 7 shows another instrument. Identify the instrument shown in "
        "Figure 7.",
        1, "Weather Instruments", 7, (5, 0.70, 0.80),
        "Rain gauge", "B1", topic_id=303)
    add_q(db, p1.id, exam_dir, 1, 5, "bii",
        "Explain why the instrument should NOT be placed near buildings and "
        "trees.",
        6, "Weather Instruments - Siting", 7, (5, 0.80, 0.92),
        "Buildings and trees can shelter the gauge so it collects less rain "
        "than actually falls; they can also cause water to drip in from "
        "leaves/roofs, giving an inaccurate (too high or too low) reading. It "
        "should be placed in an open area away from obstructions.",
        "B1 x 6", topic_id=303)
    add_q(db, p1.id, exam_dir, 1, 5, "c",
        "Where should a wind vane be placed? Explain your answer.",
        3, "Weather Instruments - Siting", 7, (5, 0.05, 0.55),
        "In an open, exposed area away from buildings and trees so that wind "
        "direction is not blocked or deflected and an accurate reading is "
        "obtained.", "B1 x 3", topic_id=303)

    # Q6 page 8 (idx 6) — leaves / forests
    leaf_stem = ("Figures 8 and 9 show two different types of leaves "
                 "(a needle-like leaf and a broad leaf).")
    add_q(db, p1.id, exam_dir, 1, 6, "ai",
        "Identify the types of forest in which the leaves in Figures 8 and 9 "
        "can be found.",
        2, "Forest Types", 8, (6, 0.05, 0.55),
        "Figure 8 (needle leaf): coniferous forest. Figure 9 (broad leaf): "
        "tropical rainforest.", "B1 x 2", stem=leaf_stem, topic_id=311)
    add_q(db, p1.id, exam_dir, 1, 6, "aii",
        "Describe the differences between the two types of leaves shown in "
        "Figures 8 and 9.",
        4, "Leaf Adaptations", 8, (6, 0.55, 0.65),
        "Coniferous (needle) leaves are small, thin and waxy to reduce water "
        "loss and shed snow. Rainforest leaves are broad with drip tips and "
        "a large surface area for photosynthesis and to drain heavy rain.",
        "B1 x 4", topic_id=311)
    add_q(db, p1.id, exam_dir, 1, 6, "aiii",
        "Compare how the trees in the forests identified in a(i) adapt to "
        "their surrounding.",
        6, "Forest Adaptations", 8, (6, 0.65, 0.78),
        "Tropical rainforest trees are evergreen with broad leaves, drip "
        "tips, buttress roots and tall straight trunks reaching for sunlight. "
        "Coniferous trees are evergreen with a conical shape, needle leaves "
        "and a thick bark to survive cold and reduce water loss.",
        "B1 x 6", topic_id=309)
    add_q(db, p1.id, exam_dir, 1, 6, "b",
        "Explain why the tropical rainforest is always dark and moist.",
        3, "Rainforest Conditions", 8, (6, 0.78, 0.90),
        "The dense, layered canopy blocks most sunlight, so the forest floor "
        "is dark. High temperature and heavy rainfall with high humidity, "
        "plus transpiration from the many trees, keep it moist.",
        "B1 x 3", topic_id=309)

    db.commit()
    cnt = db.query(Question).filter(Question.paper_id == p1.id).count()
    print(f"Seeded CHIJ St Joseph's Convent Geography 2012 exam id={exam.id}: "
          f"{cnt} questions")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
