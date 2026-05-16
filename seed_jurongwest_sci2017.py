"""Seed Jurong West Secondary School Mid-Year 2017 Sec 1 Express Science exam."""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/science/2017-Sec-1-Express-Science-SA1-Jurong-West-Secondary.pdf"
IMAGES_DIR = "/tmp/jurongwest_sci_pages"

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

    school = db.query(School).filter(School.name == "Jurong West Secondary School").first()
    if not school:
        school = School(name="Jurong West Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(
        Exam.school_id == school.id, Exam.year == 2017,
        Exam.subject == "Science").first()
    if existing:
        print(f"Jurong West 2017 Science already seeded (id={existing.id}). Re-seeding.")
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
        source_pdf="2017-Sec-1-Express-Science-SA1-Jurong-West-Secondary.pdf",
        status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # PAPER 1 — Section A: 20 MCQs (pages 2-8, idx 1-7)
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=90, total_marks=75,
               date=date(2017, 5, 5), instructions="Answer all questions. Section A: 20 MCQ (20 marks). Section B: 35 marks. Section C: 20 marks.")
    db.add(p1); db.flush()

    # Q1 — page idx 1 (top)
    add_q(db, p1.id, exam_dir, 1, 1, None,
        r"A container with the labels X and Y pasted on it. Which of the following correctly identifies X and Y? "
        r"(X = exclamation/harmful symbol, Y = corrosive symbol). "
        r"A: X corrosive, Y irritant. "
        r"B: X irritant, Y corrosive. "
        r"C: X explosive, Y irritant. "
        r"D: X irritant, Y acutely toxic.",
        1, "Lab Safety / Hazard Symbols", 2, (1, 0.13, 0.45),
        r"B — X is the irritant/harmful symbol, Y is the corrosive symbol.", "B1",
        topic_id=101)

    # Q2 — page idx 1
    add_q(db, p1.id, exam_dir, 1, 2, None,
        r"Which of the following statements about scientific method is incorrect? "
        r"A: After an experiment, results are recorded and analysed. "
        r"B: An experiment is created to test the hypothesis. "
        r"C: Scientist shares the results of the experiment with others. "
        r"D: Scientist can change his hypothesis after the experiment.",
        1, "Scientific Method", 2, (1, 0.45, 0.62),
        r"D — A hypothesis is formulated before the experiment; the conclusion (not the hypothesis) follows from results.", "B1",
        topic_id=101)

    # Q3 — page idx 1
    add_q(db, p1.id, exam_dir, 1, 3, None,
        r"A student discovered a new type of plant on his way back home. He did some research to find out more about the plant. Which scientific attitude does this student show? "
        r"A: curiosity. B: integrity. C: open-mindedness. D: perseverance.",
        1, "Scientific Attitudes", 2, (1, 0.62, 0.90),
        r"A — curiosity (wanting to find out more).", "B1",
        topic_id=101)

    # Q4 — page idx 2 (top)
    add_q(db, p1.id, exam_dir, 1, 4, None,
        r"Which of the following safety precautions should be taken when heating liquids in a test tube over a Bunsen flame? "
        r"I: Wear safety goggles. II: Wear gloves to hold the test tube. III: Point the test tube towards people. IV: Point the test tube away from people. "
        r"A: I and III only. B: I and IV only. C: II and III only. D: II and IV only.",
        1, "Lab Safety", 3, (2, 0.06, 0.42),
        r"B — I and IV only (wear goggles, point test tube away from people).", "B1",
        topic_id=101)

    # Q5 — page idx 2
    add_q(db, p1.id, exam_dir, 1, 5, None,
        r"A teacher would like to conduct an experiment to investigate the rate to dissolve sugar in water at different temperatures. Which of the following apparatus are needed? "
        r"I: thermometer. II: stopwatch. III: glass rod. IV: Bunsen burner. V: micrometer. "
        r"A: I, II, III and IV only. B: I, III, IV and V only. C: I, III and V only. D: I, IV and V only.",
        1, "Apparatus Selection", 3, (2, 0.42, 0.78),
        r"A — I, II, III and IV only (thermometer, stopwatch, glass rod, Bunsen burner; micrometer not needed).", "B1",
        topic_id=101)

    # Q6 — page idx 3 (top)
    add_q(db, p1.id, exam_dir, 1, 6, None,
        r"Which of the instruments would you use for the following measurements? "
        r"(i) Diameter of a football. (ii) Mass of a bag of sand. "
        r"A: (i) vernier calipers, (ii) electronic mass balance. "
        r"B: (i) micrometer, (ii) weighing scale. "
        r"C: (i) metre rule, (ii) electronic mass balance. "
        r"D: (i) metre rule, (ii) weighing scale.",
        1, "Measurement Instruments", 4, (3, 0.06, 0.40),
        r"D — metre rule for football diameter (large object); weighing scale for the mass of a bag of sand (large mass).", "B1",
        topic_id=102)

    # Q7 — page idx 3
    add_q(db, p1.id, exam_dir, 1, 7, None,
        r"A stone is lowered into a measuring cylinder containing some water. Water level before the stone is added = 17 cm³ region; after = higher. What is the volume of the stone? "
        r"A: 5 cm³. B: 12 cm³. C: 17 cm³. D: 29 cm³.",
        1, "Volume by Displacement", 4, (3, 0.40, 0.80),
        r"B — 12 cm³ (final water level minus initial water level).", "B1",
        topic_id=102)

    # Q8 — page idx 4 (top)
    add_q(db, p1.id, exam_dir, 1, 8, None,
        r"A metal block has a density of 2.7 g/cm³ and it is then cut into two equal pieces. The density of the two smaller pieces will ______. "
        r"A: be 2.7 g/cm³. B: be 1.35 g/cm³. C: less than 2.7 g/cm³ and more than 1.35 g/cm³. D: less than 2.7 g/cm³ and less than 1.35 g/cm³.",
        1, "Density", 5, (4, 0.06, 0.40),
        r"A — be 2.7 g/cm³. Density is a property of the material and does not change when the block is cut.", "B1",
        topic_id=102)

    # Q9 — page idx 4
    add_q(db, p1.id, exam_dir, 1, 9, None,
        r"The diagram below shows a cell. Which of the following correctly identifies the organelle where aerobic respiration takes place? (Options A-D point to structures on the cell diagram.)",
        1, "Cell Structure — Mitochondria", 5, (4, 0.40, 0.66),
        r"D — the mitochondrion is the site of aerobic respiration.", "B1",
        topic_id=107)

    # Q10 — page idx 4
    add_q(db, p1.id, exam_dir, 1, 10, None,
        r"Why is it important to have division of labour in an organism? "
        r"A: It improves the appearance of the organism. "
        r"B: It improves the efficiency of the organism. "
        r"C: It improves the relationship between two organisms. "
        r"D: It improves the structure of the organism.",
        1, "Division of Labour", 5, (4, 0.66, 0.92),
        r"B — it improves the efficiency of the organism (specialised cells perform specific functions).", "B1",
        topic_id=107)

    # Q11 — page idx 5 (top)
    add_q(db, p1.id, exam_dir, 1, 11, None,
        r"Which of the following describes an organ? "
        r"A: different organs working together. "
        r"B: different systems working together. "
        r"C: different tissues working together. "
        r"D: similar cells working together.",
        1, "Levels of Organisation", 6, (5, 0.06, 0.32),
        r"C — different tissues working together form an organ.", "B1",
        topic_id=107)

    # Q12 — page idx 5
    add_q(db, p1.id, exam_dir, 1, 12, None,
        r"Which row in the table lists the structure from the simplest to the most complex? "
        r"A: Cells, Organs, Organ systems, Tissues. "
        r"B: Cells, Tissues, Organs, Organ systems. "
        r"C: Organ systems, Organs, Tissues, Cells. "
        r"D: Tissues, Cells, Organs, Organ systems.",
        1, "Levels of Organisation", 6, (5, 0.32, 0.58),
        r"B — Cells → Tissues → Organs → Organ systems.", "B1",
        topic_id=107)

    # Q13 — page idx 5
    add_q(db, p1.id, exam_dir, 1, 13, None,
        r"Which of the following represents the physical state of a material just below its melting point? "
        r"A: solid. B: liquid. C: gas. D: solid and liquid.",
        1, "States of Matter", 6, (5, 0.58, 0.76),
        r"A — solid. Just below the melting point the substance is still a solid.", "B1",
        topic_id=103)

    # Q14 — page idx 5
    add_q(db, p1.id, exam_dir, 1, 14, None,
        r"When a substance is heated, the particles in the substance ______. "
        r"A: move slowly. B: move at the same speed. C: move faster. D: do not move.",
        1, "Kinetic Particle Theory", 6, (5, 0.76, 0.94),
        r"C — move faster (gain kinetic energy on heating).", "B1",
        topic_id=103)

    # Q15 — page idx 6 (top)
    add_q(db, p1.id, exam_dir, 1, 15, None,
        r"Which diagram shows the arrangement of atoms inside a gas jar containing helium gas? (O = helium atom) "
        r"A: closely packed regular array. B: closely packed cluster. C: widely spaced single atoms. D: widely spaced pairs of atoms.",
        1, "Particle Arrangement — Gases", 7, (6, 0.06, 0.55),
        r"C — helium is a monatomic gas, so widely spaced single atoms in a random arrangement.", "B1",
        topic_id=104)

    # Q16 — page idx 6
    add_q(db, p1.id, exam_dir, 1, 16, None,
        r"Which of the following involves a change of state from liquid to gas? "
        r"A: freezing. B: condensation. C: melting. D: evaporation.",
        1, "Changes of State", 7, (6, 0.55, 0.72),
        r"D — evaporation is the change from liquid to gas.", "B1",
        topic_id=103)

    # Q17 — page idx 6
    add_q(db, p1.id, exam_dir, 1, 17, None,
        r"Which of the following represents an element? "
        r"A: two identical atoms (one type). B: one atom of two different types bonded. C: a molecule of three atoms of two types. D: a molecule with three different atoms.",
        1, "Elements, Compounds & Molecules", 7, (6, 0.72, 0.95),
        r"A — an element consists of only one type of atom (two identical atoms).", "B1",
        topic_id=104)

    # Q18 — page idx 7 (top)
    add_q(db, p1.id, exam_dir, 1, 18, None,
        r"In a chemical reaction, element X combines with element Y to form compound Z. Which statement is not true about compound Z? "
        r"A: Elements X and Y can be separated from compound Z by physical means. "
        r"B: It has properties that are different from elements X and Y. "
        r"C: It is made up of two elements. "
        r"D: It has fixed composition by mass.",
        1, "Compounds", 8, (7, 0.06, 0.36),
        r"A — a compound cannot be separated into its elements by physical means (only chemical means).", "B1",
        topic_id=104)

    # Q19 — page idx 7
    add_q(db, p1.id, exam_dir, 1, 19, None,
        r"Which of the following statements about a suspension is not true? "
        r"A: Cloudiness or insoluble particles are observed. "
        r"B: Light can pass through a suspension easily. "
        r"C: Particles settle at the bottom when a suspension is left to stand. "
        r"D: Residue is obtained when a suspension is filtered.",
        1, "Suspensions / Mixtures", 8, (7, 0.36, 0.62),
        r"B — light cannot pass through a suspension easily because it is cloudy/opaque.", "B1",
        topic_id=106)

    # Q20 — page idx 7
    add_q(db, p1.id, exam_dir, 1, 20, None,
        r"A student wants to dissolve some sugar in water to make a drink. Which of the following actions will slow down the rate of dissolving? "
        r"A: using powdered sugar instead of sugar cubes. "
        r"B: using hot water instead of cold water. "
        r"C: stirring the water after sugar is added. "
        r"D: adding ice to the mixture to make it cold.",
        1, "Solubility / Rate of Dissolving", 8, (7, 0.62, 0.88),
        r"D — using cold water (adding ice) decreases the temperature and slows the rate of dissolving.", "B1",
        topic_id=106)

    db.commit()
    p1_count = len(p1.questions)
    print(f"Seeded Jurong West Science exam id={exam.id}: Paper 1 ({p1_count} MCQs)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
