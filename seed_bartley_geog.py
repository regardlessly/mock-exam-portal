"""Seed Bartley Secondary School EOY 2022 Sec 1 Express Geography exam."""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/bartley_geog.pdf"

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

    school = db.query(School).filter(School.name == "Bartley Secondary School").first()
    if not school:
        school = School(name="Bartley Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(
        Exam.school_id == school.id, Exam.year == 2022,
        Exam.subject == "Geography").first()
    if existing:
        print(f"Bartley Geography 2022 already seeded (id={existing.id}). Re-seeding.")
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
        source_pdf="bartley_geog.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)

    # Single paper. Q-paper pages 1-8 (idx 0-7).
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=75, total_marks=40,
               date=date(2022, 10, 1),
               instructions="Section A: Short-Answer Questions. "
                            "Section B: Structured Questions. Answer all questions.")
    db.add(p1); db.flush()

    # ── Section A — Q1 (topographical map of Saracenia, Fig. 1 on page 1) ──
    add_q(db, p1.id, exam_dir, 1, 1, "a",
        "Study Fig. 1, a topographical map of Saracenia. State the 4-figure "
        "grid reference of Fort Meteora.",
        1, "Maps & Map Reading", 2, (1, 0.05, 0.20),
        "2962.", "B1",
        stem="Question 1 refers to Fig. 1, a topographical map of Saracenia "
             "(shown on page 1 of the paper).",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 1, "b",
        "State the 6-figure grid reference of the northernmost settlement in "
        "grid square 2762.",
        1, "Maps & Map Reading", 2, (1, 0.17, 0.32),
        "276626 (also accept 277 or 627).", "B1",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 1, "c",
        "In what direction is the Meat Factory from the Car Park?",
        1, "Direction & Bearings", 2, (1, 0.28, 0.42),
        "Northwest.", "B1",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 1, "d",
        "Calculate the straight-line distance from the Meat Factory to Fort "
        "Meteora. Express your answer in km.",
        1, "Scale & Distance", 2, (1, 0.39, 0.55),
        "8.7 cm measured x 50 000 = 435 000 cm = 4350 m = 4.35 km.", "B1",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 1, "e",
        "According to the map, what might Rin's River be used for?",
        1, "Maps & Map Reading", 2, (1, 0.54, 0.70),
        "Water supply for the settlements / water supply for the meat factory "
        "(accept any other plausible answer).", "B1",
        topic_id=301)

    # ── Section B — Q2 (Water) ──
    add_q(db, p1.id, exam_dir, 1, 2, "a",
        "Define the term 'drought'.",
        1, "Water Resources & Management", 3, (2, 0.05, 0.20),
        "A drought is a long period of little or no rainfall in a specific "
        "area.", "B1",
        topic_id=308)

    add_q(db, p1.id, exam_dir, 1, 2, "b",
        "Explain how flash floods occur.",
        2, "Drainage Basins & Runoff", 3, (2, 0.19, 0.45),
        "Flash floods occur when there is exceptionally heavy rainfall over a "
        "short period of time, so most rainwater becomes surface runoff which "
        "floods low-lying areas.", "B1 x2",
        topic_id=306)

    add_q(db, p1.id, exam_dir, 1, 2, "c",
        "Fig. 2 shows a sketch of an area experiencing water pollution. "
        "Annotate the sketch to show three human activities that could cause "
        "pollution (an example has been done for you).",
        3, "Water Resources & Management", 3, (2, 0.44, 0.95),
        "Any three human activities, e.g.: factories discharging chemical "
        "waste into the river; households dumping rubbish/sewage; farms "
        "allowing fertiliser and pesticide runoff; oil/fuel spills from boats.",
        "B1 x3",
        topic_id=308)

    add_q(db, p1.id, exam_dir, 1, 2, "di",
        "Study Fig. 3, a pie chart on the global uses of water. Use evidence "
        "from Fig. 3 to describe the pattern of how water is used globally.",
        3, "Climate / Data Interpretation", 4, (3, 0.05, 0.60),
        "Most water is used for agriculture (65%); the least is used for "
        "domestic purposes (10%); the remaining 25% is used for industrial "
        "purposes.", "B1 x3 (cap at 1 if no data used)",
        topic_id=305)

    add_q(db, p1.id, exam_dir, 1, 2, "dii",
        "Describe two ways water is used for industrial purposes.",
        2, "Water Resources & Management", 4, (3, 0.59, 0.95),
        "Water is used to cool equipment or make products; to generate "
        "electricity through hydropower (dams); as a cleaning agent in wafer "
        "fabrication. Any two.", "B1 x2",
        topic_id=308)

    add_q(db, p1.id, exam_dir, 1, 2, "e",
        "Using examples, describe two ways by which Singapore has managed "
        "water sustainably.",
        4, "Water Resources & Management", 5, (4, 0.05, 0.95),
        "Improve water quality: water quality is monitored (temperature, "
        "dissolved oxygen, turbidity, pH) and industries cannot release "
        "wastewater into water bodies without NEA permission. Reduce water "
        "consumption: water-saving campaigns and pricing encourage households "
        "to use less. Any two with examples.",
        "B1 x4 (cap at 2 if no examples)",
        topic_id=308)

    # ── Section B — Q3 (Tropical forests & mangroves) ──
    add_q(db, p1.id, exam_dir, 1, 3, "a",
        "Study Fig. 4, a map of mangrove areas around the world. Using Fig. 4, "
        "describe the distribution of mangroves around the world.",
        2, "Mangrove & Coastal Vegetation", 6, (5, 0.05, 0.55),
        "Mangroves are located in coastal areas of continental landmasses, "
        "e.g. southwestern/southeastern coasts of North America, eastern coast "
        "of South America, western/eastern coasts of Africa, southern coast of "
        "Asia (especially Southeast Asia), and northern/southern coasts of "
        "Australia.", "B1 x2",
        topic_id=311)

    add_q(db, p1.id, exam_dir, 1, 3, "b",
        "Describe how tropical rainforests and/or mangroves can be sources of "
        "food.",
        2, "Tropical Rainforest Ecosystems", 6, (5, 0.54, 0.95),
        "Many foods (fruit, vegetables, nuts) come from rainforest plants; "
        "indigenous people hunt wild animals; some mangroves are converted to "
        "farms to rear fish and shrimp (aquaculture). Any two.", "B1 x2",
        topic_id=309)

    add_q(db, p1.id, exam_dir, 1, 3, "c",
        "Study Fig. 5, the amount of forest lost in Colombia from 2002 to "
        "2020. Use evidence from Fig. 5 to describe the changes in the amount "
        "of forest lost in Colombia from 2002 to 2020.",
        4, "Climate / Data Interpretation", 7, (6, 0.05, 0.95),
        "General trend: forest loss increased from 62 000 hectares in 2002 to "
        "165 000 hectares in 2020. Anomaly: a sudden drop in 2015 from 80 000 "
        "hectares (2014) to 49 000 hectares. Alternatively, a steep increase "
        "from 2015-2018 when loss surpassed 100 000 hectares.",
        "B1 x4 (1 mark for figure reference, 1 for general trend)",
        topic_id=305)

    add_q(db, p1.id, exam_dir, 1, 3, "d",
        "Explain how deforestation leads to the enhanced greenhouse effect.",
        3, "Variable Weather & Climate Change", 8, (7, 0.05, 0.45),
        "Burning or cutting down tropical forests releases stored carbon in "
        "plants and soil as carbon dioxide; fewer plants remain to absorb "
        "carbon dioxide through photosynthesis; so there is more carbon "
        "dioxide in the air, which traps more heat and enhances the "
        "greenhouse effect.", "B1 x3",
        topic_id=310)

    add_q(db, p1.id, exam_dir, 1, 3, "e",
        "Using examples, describe two strategies that countries can adopt to "
        "manage tropical rainforests and/or mangroves sustainably.",
        4, "Tropical Rainforest Ecosystems", 8, (7, 0.44, 0.95),
        "Establishing protected areas (e.g. Singapore's Sungei Buloh Wetland "
        "Reserve); regulating forestry/controlled logging (e.g. Malaysia, "
        "Colombia); rehabilitating disturbed areas through reforestation (e.g. "
        "replanting mangroves at Pulau Semakau/Tekong/Ubin); public education "
        "(e.g. NParks exhibitions and talks). Any two with examples.",
        "B1 x4 (cap at 2 if no examples)",
        topic_id=309)

    db.commit()
    print(f"Seeded Bartley Geography exam id={exam.id}: "
          f"Paper 1 ({len(p1.questions)} parts)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
