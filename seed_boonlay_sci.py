"""Seed Boon Lay Secondary School EOY 2019 Sec 1 Express Science exam (Section A MCQ)."""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/science/2019-Sec-1-Express-Science-SA2-Boon-Lay-Secondary.pdf"
IMAGES_DIR = "/tmp/boonlay_sci_pages"

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

    school = db.query(School).filter(School.name == "Boon Lay Secondary School").first()
    if not school:
        school = School(name="Boon Lay Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(
        Exam.school_id == school.id, Exam.year == 2019,
        Exam.subject == "Science").first()
    if existing:
        print(f"Boon Lay 2019 Science already seeded (id={existing.id}). Re-seeding.")
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
        source_pdf="2019-Sec-1-Express-Science-SA2-Boon-Lay-Secondary.pdf",
        status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # SECTION A — Multiple-Choice (20 marks)
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=90, total_marks=20,
               date=date(2019, 10, 7),
               instructions="Section A: 20 multiple-choice questions. Choose the one correct answer.")
    db.add(p1); db.flush()

    add_q(db, p1.id, exam_dir, 1, 1, None,
        r"The diagram shows a girl conducting an experiment. Which of the following "
        r"statements are safety hazards shown in the diagram? "
        r"1 Not wearing eye protection. "
        r"2 Long hair that is not tied up. "
        r"3 Looking into the test tube of liquid while heating it. "
        r"4 Not closing the air hole before lighting up the Bunsen burner. "
        r"5 Placing ethanol, a flammable substance, near the Bunsen burner. "
        r"A 2 and 3 only  B 1, 2 and 5 only  C 1, 2, 3 and 5 only  D 1, 2, 3, 4 and 5",
        1, "Laboratory Safety", 2, (1, 0.05, 0.55),
        "C — 1, 2, 3 and 5 are clearly hazards; 4 (closing the air hole before lighting) "
        "is not observable / not a hazard here.",
        "B1", topic_id=101)

    add_q(db, p1.id, exam_dir, 1, 2, None,
        r"The following shows steps a scientist performs in answering a question. "
        r"1 The scientist notices that there are fewer soil microorganisms near "
        r"underground gas tanks. "
        r"2 The scientist suspects that a gasoline leakage has reduced the population of "
        r"soil microorganisms. "
        r"3 The scientist varies the amount of gas added to a fixed amount of different "
        r"samples of soil. "
        r"4 The scientist counts the number of microorganisms that survived in the samples "
        r"of soil. "
        r"5 From the results the scientist finds that there is significant reduction of "
        r"microorganisms due to the gas. "
        r"Which of the following about the above steps is correct? "
        r"A step 1 = Hypothesis  B step 2 = Experimentation  "
        r"C step 3 = Interpretation  D step 4 = Data collection",
        1, "Scientific Method", 2, (1, 0.55, 0.98),
        "D — step 4 (counting surviving microorganisms) is data collection.",
        "B1", topic_id=101)

    add_q(db, p1.id, exam_dir, 1, 3, None,
        r"A measuring cylinder shows oil (density 0.85 g/ml) on top, water "
        r"(density 1.00 g/ml) in the middle and corn syrup (density 1.02 g/ml) at the "
        r"bottom. Unknown liquids: Sample P 1.02, Sample Q 0.96, Sample R 1.15, "
        r"Sample S 0.82 g/ml. Which liquid sample would sink in oil and float in water? "
        r"A P  B Q  C R  D S",
        1, "Density & Floating", 3, (2, 0.05, 0.50),
        "B — to sink in oil and float in water the density must be between 0.85 and "
        "1.00 g/ml: Sample Q (0.96 g/ml).",
        "B1", topic_id=102)

    add_q(db, p1.id, exam_dir, 1, 4, None,
        r"The chart shows the melting points of some substances found in the kitchen "
        r"(olive oil, water, lard, butter, chocolate, beeswax, sugar). The temperature in "
        r"the kitchen is 25°C. How many substances in the chart are liquids at this "
        r"temperature? "
        r"A 2  B 3  C 4  D 5",
        1, "States of Matter — Melting Point", 3, (2, 0.50, 0.98),
        "A — 2. Only substances with a melting point below 25°C (olive oil and water) "
        "are liquid at 25°C.",
        "B1", topic_id=103)

    add_q(db, p1.id, exam_dir, 1, 5, None,
        r"Which of the following is / are factor(s) that affect(s) the rate of dissolving? "
        r"1 Whether the mixture is stirred. "
        r"2 Size of solid solute particles. "
        r"3 Temperature of solvent. "
        r"A 1 only  B 1 and 2 only  C 1, 2 and 3  D None of the above",
        1, "Solutions & Solubility", 4, (3, 0.05, 0.30),
        "C — all three (stirring, particle size and solvent temperature) affect the rate "
        "of dissolving.",
        "B1", topic_id=106)

    add_q(db, p1.id, exam_dir, 1, 6, None,
        r"Sugar is added to black coffee to make sweetened coffee. Which of the following "
        r"is correct (solute / solvent / solution)? "
        r"A sugar / black coffee / sweetened coffee  "
        r"B black coffee / sugar / sweetened coffee  "
        r"C sweetened coffee / black coffee / sugar  "
        r"D sugar / sweetened coffee / black coffee",
        1, "Solutions — Solute & Solvent", 4, (3, 0.30, 0.55),
        "A — sugar is the solute, black coffee the solvent and sweetened coffee the solution.",
        "B1", topic_id=106)

    add_q(db, p1.id, exam_dir, 1, 7, None,
        r"The diagram is an example of simple distillation (watch-glass, flask, solution, "
        r"beaker). Which of the following processes occur in distillation? "
        r"A Boiling and melting  B Freezing and melting  "
        r"C Boiling and condensation  D Melting and condensation",
        1, "Separation Techniques — Distillation", 4, (3, 0.55, 0.98),
        "C — distillation involves boiling the liquid then condensing the vapour.",
        "B1", topic_id=105)

    add_q(db, p1.id, exam_dir, 1, 8, None,
        r"A colourless solution of sodium chloride is added to a colourless solution of "
        r"silver nitrate. A white precipitate (insoluble solid compound) of silver "
        r"chloride forms, suspended in a solution of sodium nitrate. The mixture of "
        r"silver chloride and sodium nitrate solution is filtered. Which of the following "
        r"is correct (residue / filtrate)? "
        r"A sodium chloride / silver nitrate  B silver nitrate / sodium chloride  "
        r"C silver chloride / sodium nitrate  D sodium nitrate / silver chloride",
        1, "Separation Techniques — Filtration", 5, (4, 0.05, 0.55),
        "D (per official mark scheme). Scientifically the insoluble silver chloride is "
        "the residue and the sodium nitrate solution is the filtrate, which matches "
        "option C; the school answer key records D.",
        "B1", topic_id=105)

    add_q(db, p1.id, exam_dir, 1, 9, None,
        r"Which of the following statements explain why classification of living things is "
        r"important? "
        r"1 To keep track of number of species. "
        r"2 To study and conserve species. "
        r"3 To give a big picture of all life forms at a glance. "
        r"4 To understand the relationship among different groups of organisms. "
        r"A 1  B 2  C 3  D 4",
        1, "Classification", 5, (4, 0.55, 0.78),
        "D — 4. Classification helps us understand the relationships among different "
        "groups of organisms (it groups organisms by characteristics).",
        "B1", topic_id=107)

    add_q(db, p1.id, exam_dir, 1, 10, None,
        r"The Venn diagram shows the characteristics of three marine organisms: whales, "
        r"fish and shrimp. Which of the following characteristics can X be (the region "
        r"common to all three)? "
        r"A lay eggs  B have fins  C can swim  D have scales",
        1, "Classification — Venn Diagram", 5, (4, 0.78, 0.98),
        "C — can swim is the characteristic shared by whales, fish and shrimp.",
        "B1", topic_id=107)

    add_q(db, p1.id, exam_dir, 1, 11, None,
        r"A team of students made a model of a plant cell. They took a length of tubing "
        r"made from a substance that allows only water molecules to pass through, and "
        r"enclosed it in a permeable membrane, with beads, a marble and dilute sugar "
        r"solution inside. Which of the following best represents the items used "
        r"(the marble / the beads / the tubing)? "
        r"A vacuoles / cell wall / nucleus  B cell wall / nucleus / vacuoles  "
        r"C nucleus / vacuoles / cell membrane  D nucleus / cell membrane / vacuoles",
        1, "Cell Structure & Function", 6, (5, 0.05, 0.55),
        "C — the marble = nucleus, the beads = vacuoles, the partially permeable tubing = "
        "cell membrane.",
        "B1", topic_id=107)

    add_q(db, p1.id, exam_dir, 1, 12, None,
        r"Which of the following organs are parts of the respiratory system? "
        r"A Heart and blood vessels  B Trachea and bronchi  "
        r"C Oesophagus and mouth  D Stomach and small intestine",
        1, "Human Organ Systems", 6, (5, 0.55, 0.78),
        "B — the trachea and bronchi are parts of the respiratory system.",
        "B1", topic_id=107)

    add_q(db, p1.id, exam_dir, 1, 13, None,
        r"Which of the following statements about cell and organism is true? "
        r"A A cell is the basic unit for animals only. "
        r"B A multicellular organism has more than one cell in its body. "
        r"C Plant cells and animal cells only differ in terms of cell wall. "
        r"D A unicellular organism does not need a nucleus to function.",
        1, "Cells & Organisation", 6, (5, 0.78, 0.98),
        "B — a multicellular organism is always made of more than one cell.",
        "B1", topic_id=107)

    add_q(db, p1.id, exam_dir, 1, 14, None,
        r"The chart lists the changes of state of matter (gas, liquid, solid with "
        r"condensation, freezing, boiling, melting, sublimation, deposition). How many "
        r"changes of state in the diagram involve the gain of heat by the substance from "
        r"its surroundings? "
        r"A 3  B 4  C 5  D 6",
        1, "Particulate Nature of Matter", 7, (6, 0.05, 0.50),
        "A — 3: melting, boiling and sublimation are processes that happen because of a "
        "gain in heat.",
        "B1", topic_id=103)

    add_q(db, p1.id, exam_dir, 1, 15, None,
        r"The diagram shows the change in the arrangement of particles as matter is heated "
        r"from the solid state to gaseous state (solid → solid/liquid → liquid → "
        r"gas/liquid → gas). Which of the following decreases as the substance is heated "
        r"from solid to gas? "
        r"A The speed of particles. "
        r"B The distance between particles. "
        r"C The temperature of the substance. "
        r"D The number of particles per unit volume.",
        1, "Particulate Nature of Matter", 7, (6, 0.50, 0.98),
        "D — as a substance becomes a gas, the number of particles per unit volume "
        "decreases (particles spread out).",
        "B1", topic_id=103)

    add_q(db, p1.id, exam_dir, 1, 16, None,
        r"An element X is written as ᴬzX where A is the mass number and Z is the atomic "
        r"number. The atomic structure of X has 4 electrons and 4 protons and 5 neutrons. "
        r"Which of the following shows the values of A and Z correctly? "
        r"A Z=5, A=4  B Z=4, A=5  C Z=9, A=4  D Z=4, A=9",
        1, "Atomic Structure", 8, (7, 0.05, 0.55),
        "D — the atom has 4 protons and 5 neutrons, so Z (atomic number) = 4 and A "
        "(mass number) = 4 + 5 = 9.",
        "B1", topic_id=104)

    add_q(db, p1.id, exam_dir, 1, 17, None,
        r"An unknown atom which is electrically neutral has 10 electrons more than a "
        r"calcium atom. What could be the possible chemical name of this element? "
        r"A Zinc  B Nitrogen  C Aluminium  D Cobalt",
        1, "Atomic Structure — Elements", 8, (7, 0.55, 0.78),
        "A — calcium has atomic number 20; 10 more electrons gives atomic number 30, "
        "which is zinc.",
        "B1", topic_id=104)

    add_q(db, p1.id, exam_dir, 1, 18, None,
        r"The diagram shows the label on a bottle containing a chemical (MgSO₄). Which of "
        r"the following is correct about the chemical in the bottle "
        r"(total type of elements / total number of atoms)? "
        r"A 2 / 5  B 5 / 3  C 3 / 3  D 3 / 6",
        1, "Elements & Compounds", 8, (7, 0.78, 0.98),
        "D — MgSO₄ has 3 types of elements (Mg, S, O) and a total of 6 atoms "
        "(1 Mg + 1 S + 4 O).",
        "B1", topic_id=104)

    add_q(db, p1.id, exam_dir, 1, 19, None,
        r"Mr Loh's car is behind Mr Lim's car at a traffic light. The number plate of Mr "
        r"Loh's car reads 'SBC 2569 F'. How would Mr Lim see Mr Loh's car number plate in "
        r"his rear view mirror? "
        r"A (laterally inverted SBC 2569 F)  B SBC 2569 F  "
        r"C F 2569 SBC  D (laterally inverted F 2569 SBC)",
        1, "Light — Reflection in Mirrors", 9, (8, 0.05, 0.55),
        "A — a plane mirror produces a laterally inverted image of the number plate.",
        "B1", topic_id=114)

    add_q(db, p1.id, exam_dir, 1, 20, None,
        r"The diagram shows two prisms and a screen. White light enters the first prism, "
        r"is split into a spectrum, then passes through a second (inverted) prism before "
        r"reaching the screen. Which of the following colours of light would be seen on "
        r"the screen? "
        r"A Red  B Blue  C White  D Yellow",
        1, "Light — Dispersion", 9, (8, 0.55, 0.98),
        "C — the first prism disperses white light and the second prism recombines the "
        "colours back to white light (reverse refraction).",
        "B1", topic_id=114)

    db.commit()
    count = len(p1.questions)
    print(f"Seeded Boon Lay Secondary School 2019 Science exam id={exam.id}: "
          f"Section A ({count} MCQs)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
