"""Seed New Town Secondary School Mid-Year 2017 Sec 1 Express Science exam.

The PDF combines Part 2 (Biology, 10 MCQs) and Part 1 (Chemistry, 10 MCQs).
Stored as one Paper 1 with questions 1-10 (Biology) and 11-20 (Chemistry).
Answer keys verified from the marking schemes in the same PDF:
  Biology Section A (idx 12):  D C C B D C B D D A
  Chemistry Section A (idx 23): B A C D B A D C B A
"""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/science/2017-Sec-1-Express-Science-SA1-New-Town-Secondary.pdf"
IMAGES_DIR = "/tmp/newtown_sci_pages"

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

    school = db.query(School).filter(School.name == "New Town Secondary School").first()
    if not school:
        school = School(name="New Town Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(
        Exam.school_id == school.id, Exam.year == 2017,
        Exam.subject == "Science").first()
    if existing:
        print(f"New Town 2017 Science already seeded (id={existing.id}). Re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id, title="Mid-Year Examination 2017", year=2017,
        level="Secondary 1 Express", subject="Science",
        source_pdf="2017-Sec-1-Express-Science-SA1-New-Town-Secondary.pdf",
        status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=90, total_marks=80,
               date=date(2017, 5, 8),
               instructions="Answer both Part 1 (Chemistry) and Part 2 (Biology). Q1-10 are Part 2 Biology MCQs; Q11-20 are Part 1 Chemistry MCQs.")
    db.add(p1); db.flush()

    # ══════════════════════════════════════════════
    # PART 2 (BIOLOGY) — Section A: Q1-10 (pages 2-6, idx 1-5)
    # Verified key: D C C B D C B D D A
    # ══════════════════════════════════════════════

    # Bio Q1 — idx 1 (top)
    add_q(db, p1.id, exam_dir, 1, 1, None,
        r"[Part 2 Biology Q1] Which of the following represents an adaptation of a mangrove plant to oxygen-deficient soil? "
        r"A: They photosynthesise at low tide. B: They secrete salt through the leaves. "
        r"C: They have needle-like leaves. D: They have aerial roots that stick out of the soil.",
        1, "Adaptations / Environment", 2, (1, 0.10, 0.32),
        r"D — aerial (breathing) roots that stick out of the soil are an adaptation to oxygen-deficient soil.", "B1",
        topic_id=110)

    # Bio Q2 — idx 1
    add_q(db, p1.id, exam_dir, 1, 2, None,
        r"[Part 2 Biology Q2] The population sizes of four different species of insect were monitored over 40 years (graph A-D shown). "
        r"Which species is in the greatest danger of extinction?",
        1, "Populations / Ecology", 2, (1, 0.32, 0.92),
        r"C — the species whose population shows a steady decline towards zero is in the greatest danger of extinction.", "B1",
        topic_id=110)

    # Bio Q3 — idx 2
    add_q(db, p1.id, exam_dir, 1, 3, None,
        r"[Part 2 Biology Q3] The diagram shows part of a food web (eagle, fox, badger, thrush, hedgehog, ladybird, aphid, caterpillar, snail, slug, tree). "
        r"Which is a pyramid of energy based on this food web? (Diagrams A-D shown.)",
        1, "Food Webs / Pyramids", 3, (2, 0.06, 0.95),
        r"C — a pyramid of energy always narrows at each higher trophic level (broad producer base, narrow apex).", "B1",
        topic_id=110)

    # Bio Q4 — idx 3 (top)
    add_q(db, p1.id, exam_dir, 1, 4, None,
        r"[Part 2 Biology Q4] Humans affect the environment: 1 felling of tropical forest, 2 harvesting of marine algae, 3 reforestation, 4 combustion of fuel, 5 overuse of nitrate fertilizer. "
        r"Which human activities lead to an increase in the level of carbon dioxide in the atmosphere? "
        r"A: 1, 2 and 3. B: 1, 2 and 4. C: 2, 3 and 4. D: 2, 3 and 5.",
        1, "Human Impact / Carbon Cycle", 4, (3, 0.06, 0.40),
        r"B — felling of forest (1), harvesting of marine algae (2) and combustion of fuel (4) increase atmospheric CO2.", "B1",
        topic_id=110)

    # Bio Q5 — idx 3
    add_q(db, p1.id, exam_dir, 1, 5, None,
        r"[Part 2 Biology Q5] The diagram shows a flowering plant with parts P, Q and R. Which correctly identifies P, Q and R? "
        r"A: P organ, Q organ, R tissue. B: P organ, Q organ system, R organ. "
        r"C: P organ system, Q organ, R tissue. D: P organ system, Q organ system, R organ.",
        1, "Levels of Organisation", 4, (3, 0.40, 0.95),
        r"C — the leaf/shoot system (P) is an organ system, the root (Q) is an organ, R is a tissue.", "B1",
        topic_id=107)

    # Bio Q6 — idx 4 (top)
    add_q(db, p1.id, exam_dir, 1, 6, None,
        r"[Part 2 Biology Q6] Which of the following represents the overall magnification of a microscope with an eyepiece magnification of 10X and an objective magnification of 40X? "
        r"A: 10X. B: 40X. C: 400X. D: 1000X.",
        1, "Microscope Magnification", 5, (4, 0.06, 0.32),
        r"C — overall magnification = 10 × 40 = 400X.", "B1",
        topic_id=107)

    # Bio Q7 — idx 4
    add_q(db, p1.id, exam_dir, 1, 7, None,
        r"[Part 2 Biology Q7] Which of the following is true for both a xylem vessel and a red blood cell? "
        r"A: large surface area to volume ratio. B: no nucleus. C: no cytoplasm. D: thickened cell wall.",
        1, "Specialised Cells", 5, (4, 0.32, 0.55),
        r"B — both a mature xylem vessel and a red blood cell have no nucleus.", "B1",
        topic_id=107)

    # Bio Q8 — idx 4
    add_q(db, p1.id, exam_dir, 1, 8, None,
        r"[Part 2 Biology Q8] Which chemical element forms part of all protein molecules? "
        r"A: calcium. B: iron. C: magnesium. D: nitrogen.",
        1, "Nutrients — Proteins", 5, (4, 0.55, 0.74),
        r"D — nitrogen is present in all protein molecules (amino groups).", "B1",
        topic_id=109)

    # Bio Q9 — idx 4
    add_q(db, p1.id, exam_dir, 1, 9, None,
        r"[Part 2 Biology Q9] The diagram shows the human alimentary canal. In which part do simpler food substances enter the blood stream? (Labels A-D on the diagram.)",
        1, "Digestion — Absorption", 5, (4, 0.74, 0.95),
        r"D — absorption of digested food into the blood occurs in the small intestine (label D).", "B1",
        topic_id=109)

    # Bio Q10 — idx 5 (top)
    add_q(db, p1.id, exam_dir, 1, 10, None,
        r"[Part 2 Biology Q10] The graph shows the effect of temperature on the time taken for the complete digestion of starch. At which temperature is the rate of digestion of starch the greatest? "
        r"A: 10 °C. B: 30 °C. C: 40 °C. D: 50 °C.",
        1, "Enzymes — Temperature", 6, (5, 0.06, 0.40),
        r"C — the rate is greatest where the time for complete digestion is shortest (about 40 °C).", "B1",
        topic_id=109)

    # ══════════════════════════════════════════════
    # PART 1 (CHEMISTRY) — Section A: Q1-10 (pages 16-18, idx 15-17)
    # Stored here as Q11-20. Verified key: B A C D B A D C B A
    # ══════════════════════════════════════════════

    # Chem Q1 -> Q11 — idx 15 (top)
    add_q(db, p1.id, exam_dir, 1, 11, None,
        r"[Part 1 Chemistry Q1] A magnesium ribbon is dropped into hydrochloric acid and the gas produced is collected. "
        r"Which statement is not an observation made during the experiment? "
        r"A: The magnesium ribbon became smaller. B: Hydrogen gas is produced. C: Bubbles are produced. D: 28 cm³ of gas is produced.",
        1, "Chemical Reactions — Observations", 16, (15, 0.06, 0.42),
        r"B — 'hydrogen gas is produced' is an inference (identity of gas), not a direct observation.", "B1",
        topic_id=101)

    # Chem Q2 -> Q12 — idx 15
    add_q(db, p1.id, exam_dir, 1, 12, None,
        r"[Part 1 Chemistry Q2] Kelly performed an experiment (250/500/1000 cm³ beakers over a burning candle, timed). Which hypothesis could Kelly be testing? "
        r"A: More oxygen leads to a candle burning longer. B: The bigger the candle, the longer it burns. "
        r"C: A candle stops burning when all the oxygen has been used up. D: The bigger the beaker, the hotter the temperature of the flame.",
        1, "Scientific Method — Hypothesis", 16, (15, 0.42, 0.78),
        r"A — varying the beaker size varies the amount of air (oxygen), testing whether more oxygen lets the candle burn longer.", "B1",
        topic_id=101)

    # Chem Q3 -> Q13 — idx 15
    add_q(db, p1.id, exam_dir, 1, 13, None,
        r"[Part 1 Chemistry Q3] Leonard saw a colourless chemical labelled with a hazard symbol (corrosive). "
        r"What special precaution should he take when using this chemical? "
        r"A: He should heat the liquid before using it. B: He should wear safety goggles when heating the liquid. "
        r"C: He should use a water bath to heat the liquid. D: He should wear gloves when handling the liquid.",
        1, "Lab Safety — Corrosive", 16, (15, 0.78, 0.97),
        r"D — a corrosive chemical requires protective gloves when handling.", "B1",
        topic_id=101)

    # Chem Q4 -> Q14 — idx 16 (top)
    add_q(db, p1.id, exam_dir, 1, 14, None,
        r"[Part 1 Chemistry Q4] Hip joint implants used to be made of stainless steel but are now made of titanium alloys "
        r"(table compares strength, density, resistance to corrosion, thermal expansion, cost, magnetism). "
        r"Why are titanium alloys used instead of stainless steel? "
        r"A: The hip implants are heavier. B: The hip implants are more expensive to manufacture. "
        r"C: The hip implants do not rust or corrode after a long time. D: The hip implants do not change lengths at different temperatures.",
        1, "Properties of Materials", 17, (16, 0.06, 0.42),
        r"C — titanium alloy has high resistance to corrosion, so the implant does not corrode in the body.", "B1",
        topic_id=102)

    # Chem Q5 -> Q15 — idx 16
    add_q(db, p1.id, exam_dir, 1, 15, None,
        r"[Part 1 Chemistry Q5] Which of these materials is correctly classified? "
        r"A: wood — ceramic. B: cotton — fibre. C: diamond — metal. D: steel — plastic.",
        1, "Classification of Materials", 17, (16, 0.42, 0.62),
        r"B — cotton is correctly classified as a fibre.", "B1",
        topic_id=102)

    # Chem Q6 -> Q16 — idx 16
    add_q(db, p1.id, exam_dir, 1, 16, None,
        r"[Part 1 Chemistry Q6] Tony set up the apparatus (material hung from a retort stand with weights added until it breaks) "
        r"and recorded the maximum weight before it breaks. Which physical property is he investigating? "
        r"A: Strength. B: Hardness. C: Flexibility. D: Malleability.",
        1, "Properties of Materials — Strength", 17, (16, 0.62, 0.95),
        r"A — the maximum weight a material supports before breaking measures its strength.", "B1",
        topic_id=102)

    # Chem Q7 -> Q17 — idx 17 (top)
    add_q(db, p1.id, exam_dir, 1, 17, None,
        r"[Part 1 Chemistry Q7] A diagram shows benefits of recycling 1000 kg of paper "
        r"(17 trees, 2 barrels of oil, 3.2 km² of landfill, 60 kg of air pollution, 4100 kW of energy). "
        r"Which statement is not true about recycling paper? "
        r"A: Recycling paper results in fewer forests being cleared. B: Recycling paper reduces waste. "
        r"C: Recycling paper protects the environment. D: Recycling paper uses up energy.",
        1, "Recycling / Environment", 18, (17, 0.06, 0.42),
        r"D — recycling paper saves energy; it does not 'use up' energy (statement is not true).", "B1",
        topic_id=104)

    # Chem Q8 -> Q18 — idx 17
    add_q(db, p1.id, exam_dir, 1, 18, None,
        r"[Part 1 Chemistry Q8] Which statement is true about compounds? "
        r"A: They are colourless solutions. B: They can be separated by physical methods. "
        r"C: They have fixed proportion of elements. D: They become a gas at 100 °C.",
        1, "Compounds", 18, (17, 0.42, 0.62),
        r"C — a compound has a fixed proportion (by mass) of its constituent elements.", "B1",
        topic_id=104)

    # Chem Q9 -> Q19 — idx 17
    add_q(db, p1.id, exam_dir, 1, 19, None,
        r"[Part 1 Chemistry Q9] Which of the following is not true about a suspension? "
        r"A: It is a mixture. B: It has the same colour throughout. "
        r"C: It contains both solid and liquid particles. D: It is formed when substances cannot dissolve.",
        1, "Suspensions / Mixtures", 18, (17, 0.62, 0.82),
        r"B — a suspension is cloudy and not uniform; it does not have the same colour/appearance throughout.", "B1",
        topic_id=106)

    # Chem Q10 -> Q20 — idx 17
    add_q(db, p1.id, exam_dir, 1, 20, None,
        r"[Part 1 Chemistry Q10] What is the chemical symbol for potassium? "
        r"A: K. B: Km. C: P. D: Po.",
        1, "Chemical Symbols", 18, (17, 0.82, 0.97),
        r"A — the chemical symbol for potassium is K.", "B1",
        topic_id=104)

    db.commit()
    p1_count = len(p1.questions)
    print(f"Seeded New Town Science exam id={exam.id}: Paper 1 ({p1_count} MCQs: 10 Biology + 10 Chemistry)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
