"""Seed Manjusri Secondary School Mid-Year 2017 Sec 1 Express Science exam."""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/science/2017-Sec-1-Express-Science-SA1-Manjusri-Secodary.pdf"
IMAGES_DIR = "/tmp/manjusri_sci_pages"

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

    school = db.query(School).filter(School.name == "Manjusri Secondary School").first()
    if not school:
        school = School(name="Manjusri Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(
        Exam.school_id == school.id, Exam.year == 2017,
        Exam.subject == "Science").first()
    if existing:
        print(f"Manjusri 2017 Science already seeded (id={existing.id}). Re-seeding.")
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
        source_pdf="2017-Sec-1-Express-Science-SA1-Manjusri-Secodary.pdf",
        status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # PAPER 1 — Section A: 40 MCQs (pages 2-15, idx 1-14)
    # Physics & Chemistry. Verified key A21-A40 from marking scheme
    # (idx 28). A1-A20 inferred from subject knowledge.
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=120, total_marks=100,
               date=date(2017, 5, 8), instructions="Answer all questions. Section A: 40 MCQ (40 marks). Section B: 40 marks. Section C: 20 marks.")
    db.add(p1); db.flush()

    # A1 — idx 1 (top)
    add_q(db, p1.id, exam_dir, 1, 1, None,
        r"The scientific method usually involves the following skills. "
        r"I: making meaning of information and evidence. II: communicating. III: engaging with an event. IV: collecting and presenting evidence. "
        r"What is the correct sequence in which the four skills are applied in the scientific method? "
        r"A: I, IV, III, II. B: III, IV, I, II. C: I, II, III, IV. D: IV, III, II, I.",
        1, "Scientific Method", 2, (1, 0.10, 0.45),
        r"B — III (engage with an event), IV (collect/present evidence), I (make meaning), II (communicate).", "B1",
        topic_id=101)

    # A2 — idx 1
    add_q(db, p1.id, exam_dir, 1, 2, None,
        r"Objectivity is an attitude of scientific enquiry. What do you understand by this term? "
        r"A: influenced by what is widely believed by others. "
        r"B: not influenced by what is widely believed by others. "
        r"C: follow the facts and be influenced by what is widely believed by others. "
        r"D: follow the facts and not be influenced by what is widely believed by others.",
        1, "Scientific Attitudes", 2, (1, 0.45, 0.70),
        r"D — objectivity means following the facts and not being influenced by popular belief.", "B1",
        topic_id=101)

    # A3 — idx 1
    add_q(db, p1.id, exam_dir, 1, 3, None,
        r"Which property of a substance indicates whether it is a liquid or solid at room temperature? "
        r"A: flexibility. B: solubility. C: melting point. D: heat conductivity.",
        1, "Properties of Matter", 2, (1, 0.70, 0.92),
        r"C — the melting point determines whether a substance is solid or liquid at room temperature.", "B1",
        topic_id=103)

    # A4 — idx 2 (top)
    add_q(db, p1.id, exam_dir, 1, 4, None,
        r"Marie carried out an experiment involving falling objects (table: mass of falling object, height released, time to reach ground). "
        r"Which of the statements below could be the hypothesis/hypotheses Marie tested? "
        r"I: The greater the mass, the longer the time to fall. II: The larger the volume, the longer the time to fall. III: The greater the mass, the greater the distance it falls before reaching the ground. "
        r"A: I only. B: I and II. C: II and III. D: none of the above.",
        1, "Scientific Method — Hypothesis", 3, (2, 0.06, 0.42),
        r"A — only I (relating mass to time) matches the variables measured in the table.", "B1",
        topic_id=101)

    # A5 — idx 2
    add_q(db, p1.id, exam_dir, 1, 5, None,
        r"To improve the experiment, Marie's teacher told her she should ask herself some questions before carrying it out. Which question should Marie ask? "
        r"A: How does the shape of the falling object affect the time taken? "
        r"B: Should the release height be measured in centimetres instead of metres? "
        r"C: Should the mass of the object be measured again after it reaches the ground? "
        r"D: Should the mass of the object be measured using a beam balance or spring balance?",
        1, "Scientific Method — Variables", 3, (2, 0.42, 0.66),
        r"A — controlling the shape of the object (a variable that could affect the result) improves the fair test.", "B1",
        topic_id=101)

    # A6 — idx 2
    add_q(db, p1.id, exam_dir, 1, 6, None,
        r"As a supplement to some diets, iron is consumed in tablet form. The mass of iron in these tablets is often measured in ______. "
        r"A: grams. B: calories. C: millilitres. D: milligrams.",
        1, "Units of Measurement", 3, (2, 0.66, 0.88),
        r"D — milligrams (the mass of iron in a tablet is very small).", "B1",
        topic_id=102)

    # A7 — idx 3 (top)
    add_q(db, p1.id, exam_dir, 1, 7, None,
        r"The diagram shows an experiment to test a certain property of liquids (light bulb, wire, battery, metal rods in a liquid). Which property is being tested? "
        r"A: density. B: solubility. C: magnetism. D: electrical conductivity.",
        1, "Properties of Matter — Conductivity", 4, (3, 0.06, 0.45),
        r"D — electrical conductivity (the bulb lights if the liquid conducts electricity).", "B1",
        topic_id=113)

    # A8 — idx 3
    add_q(db, p1.id, exam_dir, 1, 8, None,
        r"Gold, silver, platinum and copper are metals (table of melting points and densities). Which statement describes the relationship between melting point and density? "
        r"A: The densest material has the lowest melting point. "
        r"B: The melting point of a material is 100 times its density. "
        r"C: The melting point of a material is independent of density. "
        r"D: The melting point of a material decreases as density decreases.",
        1, "Properties of Matter", 4, (3, 0.45, 0.92),
        r"C — there is no consistent relationship; melting point is independent of density (from the table values).", "B1",
        topic_id=102)

    # A9 — idx 4 (top)
    add_q(db, p1.id, exam_dir, 1, 9, None,
        r"A stone of mass 60 g is lowered into a measuring cylinder. The water level rises from 50 cm³ to 100 cm³. What is the density of the stone? "
        r"A: 0.6 g/cm³. B: 1.2 g/cm³. C: 2.0 g/cm³. D: 3.0 g/cm³.",
        1, "Density", 5, (4, 0.06, 0.45),
        r"B — volume = 100 − 50 = 50 cm³; density = 60 ÷ 50 = 1.2 g/cm³.", "B1",
        topic_id=102)

    # A10 — idx 4
    add_q(db, p1.id, exam_dir, 1, 10, None,
        r"Which of the following is not an effect of a force? "
        r"A: It changes the size of an object. "
        r"B: It changes the mass of an object. "
        r"C: It changes the speed of a moving object. "
        r"D: It changes the direction of a moving object.",
        1, "Effects of Forces", 5, (4, 0.45, 0.68),
        r"B — a force does not change the mass of an object.", "B1",
        topic_id=112)

    # A11 — idx 4
    add_q(db, p1.id, exam_dir, 1, 11, None,
        r"What is the resultant force acting on the box shown (3 N to the left and 5 N to the right)? "
        r"A: 2 N to the left. B: 2 N to the right. C: 8 N to the left. D: 8 N to the right.",
        1, "Resultant Force", 5, (4, 0.68, 0.92),
        r"B — 5 N − 3 N = 2 N to the right.", "B1",
        topic_id=112)

    # A12 — idx 5 (top)
    add_q(db, p1.id, exam_dir, 1, 12, None,
        r"Which of the following is a contact force? "
        r"A: magnetic force. B: frictional force. C: electrostatic force. D: gravitational force.",
        1, "Types of Forces", 6, (5, 0.06, 0.30),
        r"B — frictional force is a contact force; the others act at a distance.", "B1",
        topic_id=112)

    # A13 — idx 5
    add_q(db, p1.id, exam_dir, 1, 13, None,
        r"Two metal balls P and Q each hang from a nylon thread. A negatively charged rod is placed between them. P is repelled by the rod while Q is attracted to it. What are the charges of P and Q? "
        r"A: P positive, Q positive. B: P positive, Q negative. C: P negative, Q positive. D: P negative, Q negative.",
        1, "Electrostatics", 6, (5, 0.30, 0.68),
        r"C — P is repelled by the negative rod so P is negative; Q is attracted so Q is positive.", "B1",
        topic_id=113)

    # A14 — idx 5
    add_q(db, p1.id, exam_dir, 1, 14, None,
        r"Which material is magnetic? "
        r"A: wood. B: brass. C: steel. D: aluminium.",
        1, "Magnetism", 6, (5, 0.68, 0.92),
        r"C — steel is a magnetic material.", "B1",
        topic_id=112)

    # A15 — idx 6 (top)
    add_q(db, p1.id, exam_dir, 1, 15, None,
        r"A metal rod XY is placed near a magnet. End X is attracted when placed near the north pole, and also when placed near the south pole. How does end Y behave when placed near the two poles? "
        r"A: Y near N attraction, Y near S attraction. B: Y near N attraction, Y near S repulsion. "
        r"C: Y near N repulsion, Y near S attraction. D: Y near N repulsion, Y near S repulsion.",
        1, "Magnetism", 7, (6, 0.06, 0.45),
        r"A — XY is an unmagnetised magnetic material (induced magnetism), so Y is attracted to both poles.", "B1",
        topic_id=112)

    # A16 — idx 6
    add_q(db, p1.id, exam_dir, 1, 16, None,
        r"Which of the following is the most likely to exert the greatest amount of pressure on the ground? "
        r"A: a loaded lorry with four identical wheels. "
        r"B: a loaded lorry with six identical wheels. "
        r"C: an empty lorry with four identical wheels. "
        r"D: an empty lorry with six identical wheels.",
        1, "Pressure", 7, (6, 0.45, 0.68),
        r"A — greatest force (loaded) over the smallest total contact area (four wheels) gives the greatest pressure.", "B1",
        topic_id=112)

    # A17 — idx 6
    add_q(db, p1.id, exam_dir, 1, 17, None,
        r"Four methods of lifting a heavy box using a lever are shown. Which method would lift the box most easily? (Diagrams A-D show different effort positions/pivots.)",
        1, "Levers / Moments", 7, (6, 0.68, 0.95),
        r"D — the method with the longest effort arm relative to the load arm requires the least effort.", "B1",
        topic_id=112)

    # A18 — idx 7 (top)
    add_q(db, p1.id, exam_dir, 1, 18, None,
        r"Which of the following shows the weight of objects in increasing order? (P, Q, R shown on balance beams.) "
        r"A: P, R, Q. B: R, P, Q. C: Q, R, P. D: R, Q, P.",
        1, "Mass and Weight", 8, (7, 0.06, 0.42),
        r"B — R, P, Q (lightest to heaviest, as indicated by the balance tilt).", "B1",
        topic_id=112)

    # A19 — idx 7
    add_q(db, p1.id, exam_dir, 1, 19, None,
        r"Which of the following does not use chemical potential energy? "
        r"A: car. B: blender. C: torchlight. D: handphone.",
        1, "Energy — Forms", 8, (7, 0.42, 0.62),
        r"B — a blender runs on mains electrical energy, not chemical (battery) energy.", "B1",
        topic_id=111)

    # A20 — idx 7
    add_q(db, p1.id, exam_dir, 1, 20, None,
        r"The arrow in each picture shows the direction of force exerted by a person. Which picture shows work being done? "
        r"A: standing holding a bag. B: lifting up a box. C: holding a ladder. D: sitting on a chair.",
        1, "Work Done", 8, (7, 0.62, 0.95),
        r"B — work is done when a force moves an object through a distance (lifting up a box).", "B1",
        topic_id=111)

    # A21 — idx 8 (top)
    add_q(db, p1.id, exam_dir, 1, 21, None,
        r"During an experiment in a school laboratory, Klein accidentally spilled a chemical with a hazard symbol (toxic/cross) on his arm. What should Klein do first? "
        r"A: call the ambulance. B: raise his hand to inform the teacher. C: wipe his arm with a clean piece of cloth. D: wash his arm thoroughly under running water.",
        1, "Lab Safety", 9, (8, 0.06, 0.40),
        r"D — wash the affected area thoroughly under running water first.", "B1",
        topic_id=101)

    # A22 — idx 8
    add_q(db, p1.id, exam_dir, 1, 22, None,
        r"Which of the following apparatus should Ryan use to measure exactly 31.4 cm³ of a liquid? "
        r"A: beaker. B: burette. C: pipette. D: test-tube.",
        1, "Measuring Apparatus", 9, (8, 0.40, 0.62),
        r"B — a burette can measure a precise, non-standard volume such as 31.4 cm³.", "B1",
        topic_id=101)

    # A23 — idx 8
    add_q(db, p1.id, exam_dir, 1, 23, None,
        r"The steps to lighting up a Bunsen burner: I: Turn on the gas tap. II: Open the air-hole. III: Light it up with a lighter. IV: Close the air-hole. "
        r"Which is the correct order to obtain a non-luminous flame? "
        r"A: I, II, III, IV. B: II, I, III, IV. C: IV, I, III, II. D: IV, III, II, I.",
        1, "Bunsen Burner", 9, (8, 0.62, 0.92),
        r"C — close the air-hole, turn on gas, light it (luminous flame), then open the air-hole for a non-luminous flame.", "B1",
        topic_id=101)

    # A24 — idx 9 (top)
    add_q(db, p1.id, exam_dir, 1, 24, None,
        r"Which one of the following diagrams shows the correct way of heating a liquid in a test-tube? (Diagrams A-D show different test-tube angles/positions over a flame.)",
        1, "Lab Safety — Heating", 10, (9, 0.06, 0.55),
        r"A — the test tube is held at an angle, pointed away from people, and heated correctly.", "B1",
        topic_id=101)

    # A25 — idx 9
    add_q(db, p1.id, exam_dir, 1, 25, None,
        r"After outdoor cooking, Jing Han realised that the bottom of his cooking pot was covered with soot. Which statement correctly describes his observation? "
        r"A: The flame was too hot. B: The food in the pot was burnt. C: The camp fire was a luminous flame. D: The camp fire was a non-luminous flame.",
        1, "Combustion / Flames", 10, (9, 0.55, 0.78),
        r"C — a luminous (yellow, incomplete combustion) flame deposits soot.", "B1",
        topic_id=101)

    # A26 — idx 9
    add_q(db, p1.id, exam_dir, 1, 26, None,
        r"Gina accidentally poured salt into a bowl of rice grains. To prevent wastage, she uses separation techniques. "
        r"Steps: I: Pour the mixture down a filter funnel fitted with filter paper. II: Add water to the mixture and stir. III: Heat the mixture until all the water has evaporated. "
        r"Which is the correct order? A: I, II, III. B: I, III, II. C: II, I, III. D: II, III, I.",
        1, "Separation Techniques", 10, (9, 0.78, 0.97),
        r"C — add water and stir to dissolve the salt (II), filter to remove rice (I), then evaporate the water to recover salt (III).", "B1",
        topic_id=105)

    # A27 — idx 10 (top)
    add_q(db, p1.id, exam_dir, 1, 27, None,
        r"Pure copper(II) sulfate crystals can be obtained from an impure mixture of copper(II) sulfate and sand. Stages I-IV shown (heating/evaporation, filtration, crystals, dissolving). In which order should these stages be? "
        r"A: I, IV, II, III. B: II, I, IV, III. C: II, I, III, IV. D: IV, I, II, III.",
        1, "Separation Techniques", 11, (10, 0.06, 0.62),
        r"B — dissolve (II), filter out sand (I), evaporate solution (IV), obtain crystals (III).", "B1",
        topic_id=105)

    # A28 — idx 10
    add_q(db, p1.id, exam_dir, 1, 28, None,
        r"Which statement must be true in order for two substances to be separated by chromatography? "
        r"A: They have different colours. B: They have different densities. C: They have different boiling points. D: They are soluble in the same solvent.",
        1, "Chromatography", 11, (10, 0.62, 0.90),
        r"D — both substances must be soluble in the same solvent so they can move with it.", "B1",
        topic_id=105)

    # A29 — idx 11 (top)
    add_q(db, p1.id, exam_dir, 1, 29, None,
        r"The diagram shows a separation technique used to obtain tea (boiling water, tea leaves, filter paper, filter jug). Which statement is correct? "
        r"A: The tea leaves dissolve in water to make tea. "
        r"B: The boiling water cannot pass through the filter paper. "
        r"C: The tea is the filtrate and the tea leaves are the residue. "
        r"D: The tea leaves are the filtrate and the tea is the residue.",
        1, "Filtration", 12, (11, 0.06, 0.45),
        r"C — the tea (liquid that passes through) is the filtrate; the tea leaves retained are the residue.", "B1",
        topic_id=105)

    # A30 — idx 11
    add_q(db, p1.id, exam_dir, 1, 30, None,
        r"Which of the following diagrams represent an element? (Diagrams A-D show different particle arrangements.)",
        1, "Elements & Compounds", 12, (11, 0.45, 0.95),
        r"A — an element contains only one type of atom (single identical particles).", "B1",
        topic_id=104)

    # A31 — idx 12 (top)
    add_q(db, p1.id, exam_dir, 1, 31, None,
        r"Henry Cavendish showed that hydrogen burns with oxygen in air to form water. Which statement(s) can be inferred from this observation alone? "
        r"I: Air is an element. II: Water is an element. III: Water is a compound. IV: Water is formed from the reaction between hydrogen and oxygen. "
        r"A: I only. B: II and III. C: II and IV. D: III and IV.",
        1, "Elements & Compounds", 13, (12, 0.06, 0.42),
        r"D — III and IV (water is a compound formed from hydrogen and oxygen reacting).", "B1",
        topic_id=104)

    # A32 — idx 12
    add_q(db, p1.id, exam_dir, 1, 32, None,
        r"Which of the following shows an element, a compound and a mixture? "
        r"A: carbon monoxide / magnesium oxide / sugar solution. "
        r"B: mercury / Milo / sodium chloride. "
        r"C: nitrogen / carbon dioxide / air. "
        r"D: steel / mud / tin.",
        1, "Elements, Compounds & Mixtures", 13, (12, 0.42, 0.78),
        r"C — nitrogen (element), carbon dioxide (compound), air (mixture).", "B1",
        topic_id=104)

    # A33 — idx 12
    add_q(db, p1.id, exam_dir, 1, 33, None,
        r"In 2004 a new element nihonium (proton number 113) was discovered, with 3 electrons in its outermost shell. Which statement is true? "
        r"A: Its chemical symbol is Ni. "
        r"B: It belongs to Group I of the Periodic Table. "
        r"C: It belongs to Period 4 of the Periodic Table. "
        r"D: It is predicted to be between copernicium and flerovium in the Periodic Table.",
        1, "Periodic Table", 13, (12, 0.78, 0.97),
        r"D — by proton number 113 it lies between copernicium (112) and flerovium (114).", "B1",
        topic_id=104)

    # A34 — idx 13 (top)
    add_q(db, p1.id, exam_dir, 1, 34, None,
        r"Which statement is true for all metals? "
        r"A: They have a silvery appearance. "
        r"B: They can be attracted by magnets. "
        r"C: They can conduct electricity in the solid state. "
        r"D: They are solids at room temperature and pressure.",
        1, "Properties of Metals", 14, (13, 0.06, 0.32),
        r"C — all metals conduct electricity in the solid state (not all are silvery, magnetic, or solid e.g. mercury).", "B1",
        topic_id=104)

    # A35 — idx 13
    add_q(db, p1.id, exam_dir, 1, 35, None,
        r"Letters T, U, V, W, X, Y, Z represent elements on the Periodic Table diagram. Which pair of elements are highly unreactive? "
        r"A: T and U. B: V and Y. C: W and Z. D: X and Y.",
        1, "Periodic Table — Noble Gases", 14, (13, 0.32, 0.55),
        r"D — X and Y are in Group 0 (noble gases), which are highly unreactive.", "B1",
        topic_id=104)

    # A36 — idx 13
    add_q(db, p1.id, exam_dir, 1, 36, None,
        r"Using the Periodic Table diagram, which pair of elements react violently in water? "
        r"A: T and U. B: V and Y. C: W and Z. D: X and Y.",
        1, "Periodic Table — Group I", 14, (13, 0.55, 0.78),
        r"C — W and Z are Group I (alkali) metals, which react violently with water.", "B1",
        topic_id=104)

    # A37 — idx 13
    add_q(db, p1.id, exam_dir, 1, 37, None,
        r"Using the Periodic Table diagram, which pair of elements have the same number of electron shells? "
        r"A: T and U. B: V and Y. C: W and Z. D: X and Y.",
        1, "Periodic Table — Periods", 14, (13, 0.78, 0.97),
        r"A — T and U are in the same period, so they have the same number of electron shells.", "B1",
        topic_id=104)

    # A38 — idx 14 (top)
    add_q(db, p1.id, exam_dir, 1, 38, None,
        r"Which of the following is a chemical reaction between elements only? "
        r"A: magnesium + oxygen → magnesium oxide. "
        r"B: methane + oxygen → carbon dioxide + water. "
        r"C: oxygen + nitrogen monoxide → nitrogen dioxide. "
        r"D: potassium + water → potassium hydroxide + hydrogen.",
        1, "Chemical Reactions", 15, (14, 0.06, 0.40),
        r"A — magnesium and oxygen are both elements reacting together.", "B1",
        topic_id=104)

    # A39 — idx 14
    add_q(db, p1.id, exam_dir, 1, 39, None,
        r"Which of the following substances is a compound? "
        r"A: C60. B: HF. C: O2. D: S8.",
        1, "Elements & Compounds", 15, (14, 0.40, 0.62),
        r"B — HF (hydrogen fluoride) contains two different elements chemically combined.", "B1",
        topic_id=104)

    # A40 — idx 14
    add_q(db, p1.id, exam_dir, 1, 40, None,
        r"Which of the following statements is true? "
        r"A: A compound has the properties of the elements it is made up of. "
        r"B: A compound can be formed by chemical processes such as combustion. "
        r"C: A compound can be broken down into simpler substances by physical methods. "
        r"D: A compound is made up of two or more different elements with different composition by mass.",
        1, "Compounds", 15, (14, 0.62, 0.92),
        r"B — a compound can be formed by chemical processes such as combustion.", "B1",
        topic_id=104)

    db.commit()
    p1_count = len(p1.questions)
    print(f"Seeded Manjusri Science exam id={exam.id}: Paper 1 ({p1_count} MCQs)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
