"""Seed Beatty Secondary School EOY 2022 Sec 1 Express Geography exam."""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/beatty_geog.pdf"

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

    school = db.query(School).filter(School.name == "Beatty Secondary School").first()
    if not school:
        school = School(name="Beatty Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(
        Exam.school_id == school.id, Exam.year == 2022,
        Exam.subject == "Geography").first()
    if existing:
        print(f"Beatty Geography 2022 already seeded (id={existing.id}). Re-seeding.")
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
        source_pdf="beatty_geog.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)

    # Single paper: 36 marks, 1h15m. Q-paper pages 1-13 (idx 0-12).
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=75, total_marks=36,
               date=date(2022, 10, 5),
               instructions="Section A: answer Question 1. Section B: answer Question 2. "
                            "Support answers with relevant examples.")
    db.add(p1); db.flush()

    # ── Section A — Question 1 (Water; topographic map) ──
    add_q(db, p1.id, exam_dir, 1, 1, "a",
        "Study Fig. 1, which shows a topographic map. State the six-figure grid "
        "reference of Factory B.",
        1, "Maps & Map Reading", 3, (2, 0.05, 0.45),
        "285202 / 285201 / 286202 / 286201 (accept any of these).", "B1",
        stem="Section A, Question 1 refers to Fig. 1, a topographic map "
             "(shown on pages 2-3 of the paper).",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 1, "b",
        "State the contour interval of the map.",
        1, "Relief & Contours", 3, (2, 0.44, 0.62),
        "10 m.", "B1",
        topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 1, "c",
        "Describe one possible source of water pollution in the river.",
        1, "Water Resources & Management", 3, (2, 0.61, 0.95),
        "The houses dumping their waste into the river, OR waste from the rubber "
        "plantation being discarded into the river.", "B1",
        topic_id=308)

    add_q(db, p1.id, exam_dir, 1, 1, "d",
        "Explain why flash floods occur in cities.",
        2, "Drainage Basins & Runoff", 4, (3, 0.05, 0.36),
        "Flash floods occur when there is heavy rainfall over a short period of "
        "time. On roads there is no soil or vegetation to allow rainwater to "
        "infiltrate, so the rainwater becomes surface runoff which results in "
        "flooding.", "B1 x2",
        topic_id=306)

    add_q(db, p1.id, exam_dir, 1, 1, "ei",
        "Study Fig. 2, a graph of Singapore's water consumption per person "
        "between 2000 and 2018. With reference to Fig. 2, describe the changes "
        "in Singapore's daily water consumption per person from 2000 to 2018.",
        3, "Climate / Data Interpretation", 4, (3, 0.35, 0.95),
        "Daily water consumption per person decreased overall from 165 litres in "
        "2000 to 141 litres in 2018. There was a gradual decrease from 2000 to "
        "2005 (165 to 160 litres) and a steeper decrease from 2010 to 2017 "
        "(155 to 143 litres).", "B1 x3",
        topic_id=305)

    add_q(db, p1.id, exam_dir, 1, 1, "eii",
        "Describe three ways people use water.",
        3, "Water Resources & Management", 5, (4, 0.05, 0.42),
        "Domestic (showering, washing dishes, flushing); recreation (canoeing, "
        "sailing); industry (cooling equipment and power plants); agriculture "
        "(growing crops, rearing animals). Any three.", "B1 x3",
        topic_id=308)

    add_q(db, p1.id, exam_dir, 1, 1, "f",
        "Study Fig. 3, a photograph of the heavily polluted Citarum River in "
        "Indonesia. With reference to Fig. 3, explain how human actions led to "
        "water pollution and the possible impacts on people.",
        3, "Water Resources & Management", 5, (4, 0.41, 0.95),
        "Residents living close to the river dump household and plastic waste "
        "directly into it, and factories discharge untreated industrial "
        "wastewater. This pollutes the water, harming people who rely on the "
        "river for drinking and washing, causing waterborne disease and loss "
        "of clean water supply.", "B1 x3",
        topic_id=308)

    add_q(db, p1.id, exam_dir, 1, 1, "g",
        "Explain how implementing laws can improve water quality and describe "
        "an advantage and a disadvantage.",
        4, "Water Resources & Management", 6, (5, 0.05, 0.95),
        "Countries implement laws so that water can be kept clean. Industries "
        "are not allowed to release wastewater into water bodies without "
        "permission and may be fined, and laws state what wastewater must not "
        "contain (e.g. petroleum, radioactive material). Advantage: the law "
        "acts as a deterrent to illegal disposal. Disadvantage: without "
        "monitoring and enforcement, the strategy will not be successful.",
        "B1 x4",
        topic_id=308)

    # ── Section B — Question 2 (Mangroves & Tropical Forests) ──
    add_q(db, p1.id, exam_dir, 1, 2, "ai",
        "Study Fig. 4, a map of mangroves in Singapore. Describe the "
        "distribution of mangroves in Singapore as shown in Fig. 4.",
        3, "Mangrove & Coastal Vegetation", 7, (6, 0.05, 0.95),
        "Mangroves grow along the coastline near the sea, on offshore islands "
        "such as Chek Jawa and Pulau Semakau, and the northwest of Singapore "
        "(e.g. Sungei Buloh, Mandai) has a significant area of mangroves.",
        "B1 x3",
        stem="Section B, Question 2 refers to Fig. 4 (mangroves in Singapore).",
        topic_id=311)

    add_q(db, p1.id, exam_dir, 1, 2, "aii",
        "Describe the conditions for the growth of mangroves.",
        2, "Mangrove & Coastal Vegetation", 7, (6, 0.60, 0.95),
        "High salinity (high salt concentration in water/soil); high air and "
        "water temperatures of at least 20 degrees C; sheltered environments "
        "along or very close to the coast giving calm water conditions.",
        "B1 x2",
        topic_id=311)

    add_q(db, p1.id, exam_dir, 1, 2, "b",
        "Describe three environmental functions of tropical forests.",
        3, "Tropical Rainforest Ecosystems", 8, (7, 0.05, 0.55),
        "Trees release oxygen through photosynthesis; they store carbon by "
        "absorbing carbon dioxide; they provide habitats for many animals; "
        "tree cover and roots reduce soil erosion; mangrove roots trap "
        "sediment and reduce coastal erosion. Any three.", "B1 x3",
        topic_id=309)

    add_q(db, p1.id, exam_dir, 1, 2, "c",
        "Study Fig. 5, which shows the rate of deforestation in the Amazon "
        "Rainforest between 2001 and 2019. With reference to Fig. 5, describe "
        "the rate of deforestation in the Amazon Rainforest between 2001 and "
        "2019.",
        3, "Tropical Rainforest Ecosystems", 9, (8, 0.05, 0.95),
        "Overall decreasing trend from 18000 km2 in 2001 to 7500 km2 in 2019. "
        "There was an increase from 2001 to 2004 (18000 to 27500 km2), then a "
        "rapid decline from 2004 to 2007 (27500 to 11000 km2).", "B1 x3",
        topic_id=309)

    add_q(db, p1.id, exam_dir, 1, 2, "d",
        "Study Fig. 6, an infographic on the human uses of tropical forests. "
        "With reference to Fig. 6 and your own knowledge, describe the human "
        "uses of tropical forests.",
        3, "Tropical Rainforest Ecosystems", 10, (9, 0.05, 0.95),
        "A place for habitat (millions of people live in tropical forests and "
        "depend on them for basic needs); a source of food; a source of "
        "resources such as timber and medicine; a place for recreation and "
        "tourism. Any three.", "B1 x3",
        topic_id=309)

    add_q(db, p1.id, exam_dir, 1, 2, "e",
        "With the use of an example, evaluate public education as a strategy "
        "to sustainably manage tropical rainforests.",
        4, "Tropical Rainforest Ecosystems", 11, (10, 0.05, 0.70),
        "Public education raises awareness of the value of tropical forests and "
        "the threats they face. NParks in Singapore organises exhibitions, "
        "festivals and talks. Advantage: educated public can raise awareness "
        "among family and friends and reduce use of paper/wood products. "
        "Disadvantage: turning awareness into action is difficult, and people "
        "may feel their effort is insignificant; awareness-raising is harder "
        "in LDCs.", "B1 x4",
        topic_id=309)

    db.commit()
    print(f"Seeded Beatty Geography exam id={exam.id}: "
          f"Paper 1 ({len(p1.questions)} parts)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
