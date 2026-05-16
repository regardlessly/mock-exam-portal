"""Seed Queensway Secondary School EOY 2017 Sec 1 Express Science exam (MCQ).

This PDF is the Mid-Year/EOY 2017 Lower Sec Science paper consisting of:
  - Section 1 (Physics): 1(A) MCQ Q1-10  (PDF pages 18-21, idx 17-20)
  - Section 2 (Biology): 2(A) MCQ Q1-15  (PDF pages 1-7, idx 0-6)
Answer keys taken from the embedded mark schemes.
"""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/science/2017-Sec-1-Express-Science-SA2-Queensway-Secondary.pdf"
IMAGES_DIR = "/tmp/queensway_sci2017_lowres"

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

    school = db.query(School).filter(School.name == "Queensway Secondary School").first()
    if not school:
        school = School(name="Queensway Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(
        Exam.school_id == school.id, Exam.year == 2017, Exam.subject == "Science"
    ).first()
    if existing:
        print(f"Queensway 2017 Science already seeded (id={existing.id}). Deleting and re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id, title="End-of-Year Examination 2017", year=2017,
        level="Secondary 1 Express", subject="Science",
        source_pdf="2017-Sec-1-Express-Science-SA2-Queensway-Secondary.pdf",
        status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # PAPER 1 — Section 1 (Physics) MCQ, Q1-10 (10 marks)
    # PDF pages 18-21 (idx 17-20)
    # Key: 1C 2A 3A 4C 5C 6D 7D 8C 9A 10B
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=45, total_marks=10,
               date=date(2017, 5, 11),
               instructions="Section 1 (Physics): Multiple Choice Questions. Answer all questions. Four options A, B, C and D.")
    db.add(p1); db.flush()

    P1 = [
        (1, "Tammy wants to be a good scientist. Which of the following descriptions is appropriate for the values that a scientist should have?\nA Perseverance — To keep trying until she gets her hypothesis correct\nB Open-mindedness — To be open to ideas and suggestions only from fellow scientists\nC Objectivity — To follow the facts even when what others initially believed was different\nD Integrity — To only report observations that suit the majority belief",
         "Scientific Attitudes", 101, 17, (17, 0.05, 0.42), "C"),
        (2, "Jill was late for the lesson and missed the laboratory safety briefing. Her friends suggested a few rules from what they remember. Which of the following is not one of the laboratory safety rules?\nA There should not be any food brought into the laboratory.\nB Safety goggles must be worn at all times no matter the experiment.\nC We should not taste chemicals unless we recognize the chemical name written on the bottle.\nD The laboratory door should not be locked except when the teacher is inside with the class.",
         "Laboratory Safety", 101, 17, (17, 0.42, 0.95), "A"),
        (3, "Sammy uses a vernier caliper to measure the thickness of 10 pages of a notebook. Fig. 3.1 shows the vernier caliper reading when it is tightly clamped on the 10 pages. What is the thickness of a single page?\nA 1.06 mm\nB 1.60 mm\nC 1.06 cm\nD 1.60 cm",
         "Measurement — Vernier Calipers", 102, 18, (18, 0.05, 0.50), "A"),
        (4, "Three balls with different densities are placed into four beakers containing different liquids (W, X, Y, Z). Which of the beakers contains the second densest liquid?\nA W\nB X\nC Y\nD Z",
         "Density", 102, 18, (18, 0.50, 0.95), "C"),
        (5, "Fred wants to measure the volume of a marble. He places five similar marbles in a measuring cylinder that is partially filled with water. What is the volume of one marble?\nA 4 cm^3\nB 8 cm^3\nC 20 cm^3\nD 40 cm^3",
         "Measurement — Volume by Displacement", 102, 19, (19, 0.05, 0.45), "C"),
        (6, "Ted wants to heat up a test tube for an experiment. He is told to use a non-luminous flame. Which of the following reasons is false in explaining why he should use a non-luminous flame for heating?\nA It produces less or no soot at all.\nB It is steadier than luminous flame.\nC It is hotter and it burns more efficiently.\nD It is blue in colour, while luminous flame is yellow.",
         "Bunsen Burner / Laboratory Apparatus", 101, 19, (19, 0.45, 0.70), "D"),
        (7, "Substance A is a solid at a room temperature of 25 C. What can you tell about its melting or boiling point?\nA Substance A has a melting point of 25 C.\nB Substance A has a boiling point of 100 C.\nC Substance A has a melting point below 25 C.\nD Substance A has a boiling point above 25 C.",
         "Changes of State / Melting & Boiling Point", 103, 19, (19, 0.70, 0.95), "D"),
        (8, "Joseph wants to make a water bottle suitable for everyone to use. He is concerned about the material used to make the water bottle. Which of the following physical properties is not an important factor that he should consider?\nA The density of the material\nB The ease at which the material will corrode\nC The electrical conductivity of the material\nD Whether the material has a higher melting point than water",
         "Physical Properties of Materials", 102, 20, (20, 0.05, 0.32), "C"),
        (9, "Which of the following is not an effect of forces?\nA A wet towel being dried up under the sun.\nB A soccer ball being kicked towards a goal.\nC A basketball being deformed after being crushed.\nD A volleyball changing direction after hitting the floor.",
         "Forces", 112, 20, (20, 0.32, 0.55), "A"),
        (10, "Which of the following statements is true about mass and weight?\nA Weight is always the same regardless of location.\nB Weight can be measured by a spring balance.\nC Mass differs depending on gravity.\nD Mass can be measured using a spring balance.",
         "Mass and Weight", 112, 20, (20, 0.55, 0.85), "B"),
    ]
    for num, text, topic, tid, pg, crop, ans in P1:
        add_q(db, p1.id, exam_dir, 1, num, None, text, 1, topic, pg, crop,
              f"{ans}", "B1", topic_id=tid)

    # ══════════════════════════════════════════════
    # PAPER 2 — Section 2 (Biology) MCQ, Q1-15 (15 marks)
    # PDF pages 1-7 (idx 0-6)
    # Key: 1C 2D 3B 4D 5D 6B 7C 8A 9B 10C 11B 12B 13D 14C 15C
    # ══════════════════════════════════════════════
    p2 = Paper(exam_id=exam.id, paper_number=2, duration_minutes=45, total_marks=15,
               date=date(2017, 5, 11),
               instructions="Section 2 (Biology): Multiple Choice Questions. Answer all questions. Four options A, B, C and D.")
    db.add(p2); db.flush()

    P2 = [
        (1, "What could be a consequence of deforestation?\nA More habitats are produced for animals and plants.\nB More transpiration may increase rainfall.\nC Rainwater runs off the land causing flooding.\nD Soil erosion is less likely.",
         "Conservation / Human Impact", 111, 1, (0, 0.05, 0.30), "C"),
        (2, "The diagram shows a fish with a key to identify it (black stripe across the eye / caudal fin; black spot below dorsal fin). Use the key to identify the fish shown.\nA black stripe across the eye, go to 2\nB no black stripe across the eye\nC black spot below dorsal fin\nD no black spot below dorsal fin",
         "Classification / Dichotomous Key", 107, 1, (0, 0.30, 0.95), "D"),
        (3, "Which parts are found in both plant and animal cells?\nA cell membrane, large vacuole\nB cell membrane, cytoplasm\nC cell wall, large vacuole\nD cell wall, cytoplasm",
         "Cells — Plant and Animal", 107, 2, (1, 0.05, 0.30), "B"),
        (4, "The diagram shows some heart muscle cells. Which describes the level of organisation of these cells and their specific function?\nA organ / contraction\nB organ / support\nC tissue / support\nD tissue / contraction",
         "Cellular Organisation", 107, 2, (1, 0.30, 0.62), "D"),
        (5, "The diagram shows an apparatus used to investigate osmosis (capillary tube, water, concentrated sugar solution, partially permeable membrane). Which molecules will move across the membrane and which changes in levels will occur?\nA sugar / level 1 fall / level 2 rise\nB water / level 1 fall / level 2 rise\nC sugar / level 1 rise / level 2 fall\nD water / level 1 rise / level 2 fall",
         "Movement of Substances — Osmosis", 108, 2, (1, 0.62, 0.95), "D"),
        (6, "The diagram shows a group of body cells surrounded by tissue fluid. Which conditions cause the body cells to take in water? (water potential in tissue fluid / water potential in cytoplasm of body cells)\nA high / high\nB high / low\nC low / high\nD low / low",
         "Movement of Substances — Osmosis", 108, 3, (2, 0.05, 0.40), "B"),
        (7, "The diagram shows a bean seedling, soon after it has germinated. Where is most water absorbed?\nA region A\nB region B\nC region C\nD region D",
         "Transport in Plants — Water Uptake", 110, 3, (2, 0.40, 0.95), "C"),
        (8, "A carnation flower stalk was cut into two halves at its base. Each half was soaked in a different coloured liquid (blue ink / red ink) and placed in an airy area for three days. The stalk was cut along line X and examined. What is the expected appearance of the cut stem on the third day?\nA diagram A\nB diagram B\nC diagram C\nD diagram D",
         "Transport in Plants — Xylem", 110, 4, (3, 0.05, 0.95), "A"),
        (9, "The diagram shows a tree trunk, with a ring of bark (which includes the phloem) removed. The tree will eventually die because this action cuts off the supply of\nA mineral salts to the leaves.\nB manufactured food to the roots.\nC oxygen to the roots.\nD water to the leaves.",
         "Transport in Plants — Phloem", 110, 5, (4, 0.05, 0.42), "B"),
        (10, "The diagram shows the structure of the heart. Which structure carries deoxygenated blood from all parts of the body?\nA structure A\nB structure B\nC structure C\nD structure D",
         "Transport — The Heart", 110, 5, (4, 0.42, 0.95), "C"),
        (11, "The bar chart shows the concentration of oxygen in blood samples taken from four different blood vessels in the human circulatory system. Which blood sample is taken from the artery entering the lungs?\nA A\nB B\nC C\nD D",
         "Transport — Blood Vessels", 110, 6, (5, 0.05, 0.45), "B"),
        (12, "The diagrams show the cross-section of two types of blood vessels X and Y. What do X and Y represent?\nA X artery / Y capillary\nB X artery / Y vein\nC X capillary / Y vein\nD X vein / Y artery",
         "Transport — Blood Vessels", 110, 6, (5, 0.45, 0.95), "B"),
        (13, "Which of the following is the correct function of the oesophagus?\nA It releases bile.\nB It breaks up the food.\nC It rolls the food into small balls.\nD It pushes the food from the mouth to the stomach.",
         "Human Digestive System", 109, 7, (6, 0.05, 0.32), "D"),
        (14, "Runners sometimes eat bananas before long-distance running races because they contain\nA a large amount of water to keep the runner hydrated.\nB fats to release a lot of energy at a slow, steady rate.\nC carbohydrates which can supply energy.\nD proteins to repair muscle cells damaged while running.",
         "Human Digestive System — Nutrients", 109, 7, (6, 0.32, 0.55), "C"),
        (15, "A scientist extracted a protease from the stomach and subjected it to different pH conditions (acidic or alkaline). In which set-up will digestion take place? (acidic condition / alkaline condition / food molecule)\nA absent / present / carbohydrate\nB present / absent / carbohydrate\nC present / absent / protein\nD present / present / protein",
         "Human Digestive System — Enzymes", 109, 7, (6, 0.55, 0.85), "C"),
    ]
    for num, text, topic, tid, pg, crop, ans in P2:
        add_q(db, p2.id, exam_dir, 2, num, None, text, 1, topic, pg, crop,
              f"{ans}", "B1", topic_id=tid)

    db.commit()
    p1_count = len(p1.questions)
    p2_count = len(p2.questions)
    print(f"Seeded Queensway 2017 Science exam id={exam.id}: "
          f"Paper 1 Physics MCQ ({p1_count}), Paper 2 Biology MCQ ({p2_count})")
    print(f"Total questions: {p1_count + p2_count}")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
