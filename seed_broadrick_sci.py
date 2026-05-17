"""Seed Broadrick Secondary School SA2 (EOY) 2019 Sec 1 Express Science exam (MCQ Section A).

Re-transcribed from /Users/timmy/Downloads/sec1-papers/science/2019-Sec-1-Express-Science-SA2-Broadrick-Secondary.pdf
Section A = 30 MCQ (printed pages 3-11 = PDF idx 0-8).
Correct options taken from the official MARKING SCHEME in the same PDF (PDF idx 25).
"""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/science/2019-Sec-1-Express-Science-SA2-Broadrick-Secondary.pdf"

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

    school = db.query(School).filter(School.name == "Broadrick Secondary School").first()
    if not school:
        school = School(name="Broadrick Secondary School")
        db.add(school)
        db.flush()

    # Idempotent re-seed scoped by school + year + subject so the 2017 and 2019
    # Broadrick Science exams stay independent and never delete each other.
    existing = db.query(Exam).filter(
        Exam.school_id == school.id, Exam.year == 2019,
        Exam.subject == "Science").first()
    if existing:
        print(f"Broadrick 2019 Science already seeded (id={existing.id}). Deleting and re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id, title="End-of-Year Examination 2019", year=2019,
        level="Secondary 1 Express", subject="Science",
        source_pdf="2019-Sec-1-Express-Science-SA2-Broadrick-Secondary.pdf",
        status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)

    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=None, total_marks=30,
               date=date(2019, 10, 1),
               instructions="Section A: 30 MCQ (30 marks). Shade your answers in the OTAS provided.")
    db.add(p1); db.flush()

    def mcq(num, text, topic, topic_id, pg, top, bot, opts, ans):
        add_q(db, p1.id, exam_dir, 1, num, None,
              text + "\n\n" + opts, 1, topic, num, (pg, top, bot),
              ans, "B1", topic_id=topic_id)

    # ---- idx 0 (printed p3): Q1-Q4 ----
    mcq(1, r"A pair of vernier calipers is used to measure the thickness of a book. "
        r"What is the thickness of the book?",
        "Physical Quantities, Units & Measurement", 102, 0, 0.08, 0.40,
        "A. 2.03 cm\nB. 2.31 cm\nC. 2.51 cm\nD. 2.62 cm",
        "C — main scale 2.5 cm plus vernier coincidence gives a reading of 2.51 cm.")
    mcq(2, r"Which instrument below can be used to measure the amount of matter in a substance?",
        "Physical Quantities, Units & Measurement", 102, 0, 0.40, 0.50,
        "A. burette\nB. spring balance\nC. beam balance\nD. displacement can",
        "C — a beam balance measures mass, which is the amount of matter in a substance.")
    mcq(3, r"The table shows information about four objects P, Q, R and S with their mass (g) "
        r"and volume (cm$^3$). Which two objects have the same density?",
        "Physical Quantities, Units & Measurement", 102, 0, 0.50, 0.72,
        r"A. P and Q\nB. P and R\nC. Q and S\nD. R and S",
        r"B — P: 30/6 = 5 g/cm$^3$ and R: 50/10 = 5 g/cm$^3$ have the same density.")
    mcq(4, r"A measuring cylinder contains 100 cm$^3$ of water. An irregularly shaped object of "
        r"mass 50 g is lowered slowly into the cylinder until it is completely immersed. Given "
        r"that the density of the object is 5.0 g/cm$^3$, what is the new reading on the "
        r"measuring cylinder?",
        "Physical Quantities, Units & Measurement", 102, 0, 0.72, 0.95,
        r"A. 105 cm$^3$\nB. 110 cm$^3$\nC. 150 cm$^3$\nD. 155 cm$^3$",
        r"B — object volume = 50/5.0 = 10 cm$^3$; new reading = 100 + 10 = 110 cm$^3$.")

    # ---- idx 1 (printed p4): Q5-Q9 ----
    mcq(5, r"The table shows the properties (density, electrical conductivity, appearance) of "
        r"four different materials. Which material is possibly a metal?",
        "Elements, Compounds & Mixtures", 104, 1, 0.05, 0.25,
        "A. low density, poor conductivity, yellow\nB. low density, good conductivity, black\n"
        "C. high density, poor conductivity, shiny\nD. high density, good conductivity, shiny",
        "D — metals typically have high density, good electrical conductivity and a shiny appearance.")
    mcq(6, r"A robotic vehicle, which has a weight of 800 N on Earth, was sent to Mars. The "
        r"gravitational field strength is 4 N/kg on Mars and 10 N/kg on Earth. What is the "
        r"robotic vehicle's weight on Mars?",
        "Forces", 112, 1, 0.25, 0.40,
        "A. 20 N\nB. 32 N\nC. 200 N\nD. 320 N",
        "D — mass = 800/10 = 80 kg; weight on Mars = 80 × 4 = 320 N.")
    mcq(7, r"In which of the following positions will a person exert the greatest pressure on the "
        r"ground?",
        "Forces", 112, 1, 0.40, 0.55,
        "A. The person stands on one foot.\nB. The person sits cross-legged on the floor.\n"
        "C. The person stands on both feet.\nD. The person lies flat on his back.",
        "A — standing on one foot gives the smallest contact area, hence the greatest pressure.")
    mcq(8, r"An object with a mass of 2.0 kg has 300 J of kinetic energy. What is the speed of "
        r"the object?",
        "Energy", 111, 1, 0.53, 0.70,
        "A. 8.7 m/s\nB. 12.8 m/s\nC. 17.3 m/s\nD. 24.5 m/s",
        r"C — KE = $\frac{1}{2}mv^2$; $v = \sqrt{2 \times 300 / 2.0} = \sqrt{300} \approx 17.3$ m/s.")
    mcq(9, r"In which of the following cases is there completely no work done?",
        "Energy", 111, 1, 0.70, 0.92,
        "A. A car slowing down when approaching a pedestrian crossing.\n"
        "B. A man holding a big shopping bag on an escalator moving upwards.\n"
        "C. A student holding her files standing at the bus stop.\n"
        "D. A delivery man holding a new TV set standing in a lift moving upwards.",
        "C — the student is stationary, so there is no displacement and no work is done.")

    # ---- idx 2 (printed p5): Q10-Q12 ----
    mcq(10, r"The total energy of a free falling object is the sum of the gravitational potential "
        r"energy and kinetic energy. Assuming air resistance is negligible, which row best "
        r"represents the changes in the different energies when the object is falling freely "
        r"under gravity (gravitational potential energy, kinetic energy, total energy)?",
        "Energy", 111, 2, 0.05, 0.30,
        "A. GPE increases, KE decreases, total remains constant\n"
        "B. GPE decreases, KE increases, total remains constant\n"
        "C. GPE decreases, KE increases, total decreases\n"
        "D. GPE increases, KE decreases, total increases",
        "B — as the object falls, GPE decreases and KE increases while total energy is conserved (constant).")
    mcq(11, r"Which of the following physical properties can be used to describe non-metals? "
        r"I They are poor conductors of electricity. II They have lower melting and boiling "
        r"points. III They are brittle.",
        "Elements, Compounds & Mixtures", 104, 2, 0.30, 0.52,
        "A. I, II\nB. II, III\nC. I, III\nD. I, II, III",
        "D — non-metals are generally poor conductors, have lower melting/boiling points and are brittle.")
    mcq(12, r"The diagram below shows the particles found in substance M (open and filled "
        r"circles representing different elements). Which of the following statements correctly "
        r"describes Substance M?",
        "Elements, Compounds & Mixtures", 104, 2, 0.52, 0.95,
        "A. Substance M is a compound.\nB. Substance M is a mixture of elements.\n"
        "C. Substance M is a mixture of compounds.\n"
        "D. Substance M is a mixture of an element and a compound.",
        "D — the diagram shows bonded two-element molecules (a compound) together with "
        "separate single-element particles, i.e. a mixture of an element and a compound.")

    # ---- idx 3 (printed p6): Q13-Q15 ----
    mcq(13, r"The set-up shows a simple distillation experiment. The boiling points of pure "
        r"water and blue ink are 100 °C and 150 °C respectively. What are the colours of the "
        r"liquids in the flask and beaker at 100 °C (flask, beaker)?",
        "Separation Techniques", 105, 3, 0.05, 0.42,
        "A. flask blue, beaker blue\nB. flask blue, beaker colourless\n"
        "C. flask colourless, beaker blue\nD. flask colourless, beaker colourless",
        "B — at 100 °C only the water boils off and condenses colourless in the beaker; the "
        "blue ink remains in the flask.")
    mcq(14, r"Sodium benzoate is a preservative. Its chemical formula is C$_6$H$_5$COONa. "
        r"How many elements are present in the formula shown?",
        "Elements, Compounds & Mixtures", 104, 3, 0.42, 0.55,
        "A. 2\nB. 3\nC. 4\nD. 5",
        "C — the elements present are carbon, hydrogen, oxygen and sodium (4 elements).")
    mcq(15, r"In the Periodic Table shown, each number represents an element. Which two "
        r"numbers represent non-metals in the same Group?",
        "Elements, Compounds & Mixtures", 104, 3, 0.55, 0.95,
        "A. 1 and 2\nB. 3 and 8\nC. 4 and 9\nD. 6 and 7",
        "D — elements 6 and 7 are non-metals in the same Group (same column on the right of "
        "the Periodic Table).")

    # ---- idx 4 (printed p7): Q16-Q18 ----
    mcq(16, r"A glass of apple juice is a solution while orange juice is considered a "
        r"suspension. Which of the following correctly identifies the difference between a "
        r"suspension and a solution?",
        "Solutions & Solubility", 106, 4, 0.05, 0.28,
        "A. The speed at which the solute dissolves in the solvent.\n"
        "B. The amount of solute that can dissolve in the solvent.\n"
        "C. When left to stand, whether particles are suspended in the liquid.\n"
        "D. Any change in colour.",
        "C — in a suspension the particles are suspended and settle on standing, whereas a "
        "solution stays uniformly mixed.")
    mcq(17, r"The effect of temperature on the solubility of two substances P and Q in the same "
        r"amount of solvent was investigated (see graph). Which statement cannot be "
        r"concluded from the graph?",
        "Solutions & Solubility", 106, 4, 0.28, 0.55,
        "A. Solubility of substance P continues to increase after 80 °C.\n"
        "B. Substance Q has reached the maximum solubility after 40 °C.\n"
        "C. At 20 °C, substance Q dissolves more than substance P.\n"
        "D. Solubility of substance P increases when temperature increases from 20 °C to 40 °C.",
        "A — the graph only goes up to about 80 °C, so behaviour after 80 °C cannot be concluded.")
    mcq(18, r"The diagram shows a specialized cell from a plant. Which function is the cell "
        r"modified for?",
        "Cells — The Basic Unit of Life", 107, 4, 0.55, 0.88,
        "A. absorption of water\nB. photosynthesis\nC. storage of food\nD. support",
        "A — the long extension (root hair cell) increases surface area for the absorption of water.")

    # ---- idx 5 (printed p8): Q19-Q21 ----
    mcq(19, r"The diagram shows some heart muscle cells. Which describes the level of "
        r"organisation of the cells and their specific function (level of organisation, "
        r"specific function)?",
        "Cells — The Basic Unit of Life", 107, 5, 0.05, 0.30,
        "A. organ, contraction\nB. organ, support\nC. tissue, support\nD. tissue, contraction",
        "D — many similar muscle cells form a tissue whose specific function is contraction.")
    mcq(20, r"An Amoeba, a unicellular organism, had its nucleus removed using a fine glass "
        r"tube but was otherwise not damaged. For seven days it continued to move and feed "
        r"but did not reproduce. An intact Amoeba used as a control reproduced twice in seven "
        r"days. What is another function of the nucleus that can be concluded from this "
        r"experiment?",
        "Cells — The Basic Unit of Life", 107, 5, 0.30, 0.55,
        "A. The nucleus controls cellular activities.\n"
        "B. The nucleus controls the movement of the cell.\n"
        "C. The nucleus is essential for cell reproduction.\n"
        "D. The nucleus is essential for the uptake of water.",
        "C — only the reproduction stopped when the nucleus was removed, so the nucleus is "
        "essential for cell reproduction.")
    mcq(21, r"The diagram shows a cell observed under a microscope. Which are the correct "
        r"labels for cell organelle 1, 2, 3 and 4 (cellulose cell wall, cell surface "
        r"membrane, chloroplast, cytoplasm)?",
        "Cells — The Basic Unit of Life", 107, 5, 0.55, 0.92,
        "A. cell wall 1, membrane 2, chloroplast 3, cytoplasm 4\n"
        "B. cell wall 1, membrane 2, chloroplast 4, cytoplasm 3\n"
        "C. cell wall 2, membrane 1, chloroplast 3, cytoplasm 4\n"
        "D. cell wall 2, membrane 1, chloroplast 4, cytoplasm 3",
        "C — the outermost layer (2) is the cellulose cell wall, (1) the cell surface membrane, "
        "(3) the chloroplast and (4) the cytoplasm.")

    # ---- idx 6 (printed p9): Q22-Q24 ----
    mcq(22, r"Four clear agar blocks A, B, C and D of different dimensions were placed in "
        r"solutions of methylene blue of the same concentration. Which agar block will be the "
        r"slowest to be completely stained blue?",
        "Movement of Substances", 108, 6, 0.05, 0.42,
        "A. block A (smallest cube)\nB. block B (largest cube)\n"
        "C. block C (small cube)\nD. block D (large cube)",
        "B — the largest block has the smallest surface area to volume ratio, so diffusion to "
        "its centre is slowest.")
    mcq(23, r"The diagram shows an experiment: a model gut (membrane bag) of white starch "
        r"suspension in yellow-brown iodine solution; after 6 hours the starch suspension "
        r"turns blue-black. Why has the starch suspension changed colour at the end of the "
        r"experiment?",
        "Movement of Substances", 108, 6, 0.42, 0.78,
        "A. Iodine has diffused in through the membrane.\n"
        "B. Iodine has diffused out through the membrane.\n"
        "C. Starch has diffused in through the membrane.\n"
        "D. Starch has diffused out through the membrane.",
        "A — small iodine molecules diffuse in through the membrane and turn the starch blue-black.")
    mcq(24, r"Which statements are true? I Plasma helps to transport dissolved substances. "
        r"II Platelets help in the clotting of blood. III White blood cells help to transport "
        r"oxygen.",
        "Transport in Living Things", 110, 6, 0.78, 0.95,
        "A. I and II only\nB. I and III only\nC. II and III only\nD. I, II and III",
        "A — I and II are true; oxygen is transported by red blood cells, not white blood cells, "
        "so III is false.")

    # ---- idx 7 (printed p10): Q25-Q26 ----
    mcq(25, r"The diagram shows red blood cells placed in solutions P, Q, R and S of different "
        r"solute concentrations. After one minute the appearance of the cells was as shown. "
        r"Which conclusion can be drawn from these observations?",
        "Movement of Substances", 108, 7, 0.05, 0.45,
        "A. Solution P has a lower water potential than the cytoplasm of the red blood cell.\n"
        "B. Solution Q has a higher water potential than the cytoplasm of the red blood cell.\n"
        "C. Solution R has a lower water potential than the cytoplasm of the red blood cell.\n"
        "D. Solution S has approximately the same solute concentration as the cytoplasm of "
        "the red blood cell.",
        "A — the cells in solution P shrank (crenated), showing solution P has a lower water "
        "potential than the cell cytoplasm.")
    mcq(26, r"The diagram shows a simplified model of blood circulation in a mammal "
        r"(Rest of Body — Heart — Lungs, vessels 1, 2, 3, 4). Which correctly shows the "
        r"identity of blood vessels 1, 2, 3 and 4 (artery, vein)?",
        "Transport in Living Things", 110, 7, 0.45, 0.78,
        "A. artery 1 and 2, vein 3 and 4\nB. artery 1 and 3, vein 2 and 4\n"
        "C. artery 1 and 4, vein 2 and 3\nD. artery 2 and 3, vein 1 and 4",
        "D — vessels 2 and 3 carry blood away from the heart (arteries); vessels 1 and 4 "
        "return blood to the heart (veins).")

    # ---- idx 8 (printed p11): Q27-Q30 ----
    mcq(27, r"The diagram shows a section through a stem (labelled tissues A, B, C, D). "
        r"Which labelled tissue transports water and mineral salts towards the leaves?",
        "Transport in Living Things", 110, 8, 0.05, 0.30,
        "A. tissue A\nB. tissue B\nC. tissue C\nD. tissue D",
        "D — the xylem (tissue D) transports water and mineral salts upward towards the leaves.")
    mcq(28, r"Which of the following secretions contains enzymes that are able to break down "
        r"carbohydrates, proteins and fats?",
        "Human Digestive System", 109, 8, 0.30, 0.45,
        "A. bile\nB. saliva\nC. gastric juice\nD. pancreatic juice",
        "D — pancreatic juice contains amylase, protease and lipase, digesting all three food groups.")
    mcq(29, r"The table shows the composition of four foods in grams per 100 g portion "
        r"(carbohydrate, fat, protein). Which food would be most useful for providing an "
        r"immediate source of energy?",
        "Human Digestive System", 109, 8, 0.45, 0.68,
        "A. food A (carbohydrate 60.2, fat 0.0, protein 0.5)\n"
        "B. food B (carbohydrate 8.6, fat 35.0, protein 32.1)\n"
        "C. food C (carbohydrate 0.0, fat 0.0, protein 45.0)\n"
        "D. food D (carbohydrate 14.8, fat 10.8, protein 0.3)",
        "A — food A has the highest carbohydrate content, which provides an immediate source of energy.")
    mcq(30, r"The diagram shows a section of the human digestive system (labelled A, B, C, D). "
        r"In which structure does the absorption of most food molecules occur?",
        "Human Digestive System", 109, 8, 0.65, 0.94,
        "A. structure A\nB. structure B\nC. structure C\nD. structure D",
        "C — most food molecules are absorbed in the small intestine (structure C).")

    db.commit()
    print(f"Seeded Broadrick Science SA2/EOY 2019 exam id={exam.id}: Section A {len(p1.questions)} MCQs")
    print(f"Images in {exam_dir}")
    eid = exam.id
    db.close()
    return eid


if __name__ == "__main__":
    main()
