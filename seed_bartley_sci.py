"""Seed Bartley Secondary School EOY 2019 Sec 1 Express Science exam (Section A MCQ)."""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/science/2019-Sec-1-Express-Science-SA2-Bartley-Secondary.pdf"
IMAGES_DIR = "/tmp/bartley_sci_pages"

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
        Exam.school_id == school.id, Exam.year == 2019,
        Exam.subject == "Science").first()
    if existing:
        print(f"Bartley 2019 Science already seeded (id={existing.id}). Re-seeding.")
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
        source_pdf="2019-Sec-1-Express-Science-SA2-Bartley-Secondary.pdf",
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
               date=date(2019, 10, 10),
               instructions="Section A: 20 multiple-choice questions. Choose the one correct answer.")
    db.add(p1); db.flush()

    add_q(db, p1.id, exam_dir, 1, 1, None,
        r"Which row describes the colour of luminous flame and the state of the "
        r"corresponding air hole of a Bunsen burner? "
        r"A blue, closed  B blue, open  C orange, closed  D orange, open",
        1, "Bunsen Burner Flame", 2, (1, 0.18, 0.42),
        "C — a luminous flame is orange and occurs when the air hole is closed.",
        "B1", topic_id=101)

    add_q(db, p1.id, exam_dir, 1, 2, None,
        r"Vitamins A and E are soluble in fats. What does fat act as when it is used to "
        r"dissolve Vitamins A and E? "
        r"A solute  B solution  C solvent  D suspension",
        1, "Solutions & Solubility", 2, (1, 0.42, 0.62),
        "C — the fat dissolves the vitamins, so the fat is the solvent.",
        "B1", topic_id=106)

    add_q(db, p1.id, exam_dir, 1, 3, None,
        r"Which description shows the change in the movement of the particles and the "
        r"distance between each particle during freezing? "
        r"A faster, closer together  B faster, further apart  "
        r"C slower, closer together  D slower, further apart",
        1, "Particulate Nature of Matter", 2, (1, 0.62, 0.92),
        "C — on freezing (liquid → solid) particles move slower and become closer together.",
        "B1", topic_id=103)

    add_q(db, p1.id, exam_dir, 1, 4, None,
        r"Which diagrams show a mixture of two elements? (Diagrams I–IV show different "
        r"particle arrangements.) "
        r"A I and II only  B II and III only  C III and IV only  D all of the above",
        1, "Elements, Compounds & Mixtures", 3, (2, 0.05, 0.55),
        "C — III and IV only show two kinds of unbonded single atoms = mixture of two elements.",
        "B1", topic_id=104)

    add_q(db, p1.id, exam_dir, 1, 5, None,
        r"The diagram shows 200 cm³ of liquid in two different containers. Which property "
        r"of liquids is shown? "
        r"A Liquids can flow.  B Liquids cannot be compressed.  "
        r"C Liquids do not have fixed shapes.  D Liquids have high densities.",
        1, "States of Matter", 3, (2, 0.55, 0.98),
        "C — the same volume takes the shape of each container, showing liquids have no "
        "fixed shape.",
        "B1", topic_id=103)

    add_q(db, p1.id, exam_dir, 1, 6, None,
        r"The diagram shows the energy pyramid of a food chain (3 hawks; 17 snakes; "
        r"210 rats; 3000 insects; plants). What is the estimated amount of energy the "
        r"snakes will receive if the plants can provide 100 000 J of energy? "
        r"A 10 J  B 100 J  C 1 000 J  D 100 000 J",
        1, "Energy Flow / Food Chains", 4, (3, 0.05, 0.45),
        "B — about 10% of energy is passed at each level: 100 000 → 10 000 (insects) → "
        "1000 (rats) → 100 J (snakes).",
        "B1", topic_id=111)

    add_q(db, p1.id, exam_dir, 1, 7, None,
        r"The diagram shows the main parts of a hydroelectric power station. Which energy "
        r"change occurs in the generator? "
        r"A chemical to kinetic  B electrical to heat  C heat to chemical  D kinetic to electrical",
        1, "Energy Conversion", 4, (3, 0.45, 0.95),
        "D — the generator converts kinetic energy of the turbine into electrical energy.",
        "B1", topic_id=111)

    add_q(db, p1.id, exam_dir, 1, 8, None,
        r"How does a wool sweater keep a person warm? "
        r"A Air is trapped in the wool.  B Air passes easily through the wool.  "
        r"C Wool heats up easily.  D Wool is warm.",
        1, "Energy — Heat Insulation", 5, (4, 0.05, 0.42),
        "A — trapped air is a poor conductor of heat, reducing heat loss from the body.",
        "B1", topic_id=111)

    add_q(db, p1.id, exam_dir, 1, 9, None,
        r"A swimmer is suspected of consuming a banned drug. His urine sample is tested by "
        r"paper chromatography against the pure drug, using alcohol and water as solvents. "
        r"Which statement about the results is true? "
        r"A Both tests show that he consumed the banned drug. "
        r"B Both tests show that he did not consume the banned drug. "
        r"C The test using alcohol shows he consumed the drug, but not the water test. "
        r"D The test using water shows he consumed the drug, but not the alcohol test.",
        1, "Separation Techniques — Chromatography", 5, (4, 0.42, 0.98),
        "C — in alcohol the urine spot matches the drug spot (positive); in water the "
        "spots differ (no match).",
        "B1", topic_id=105)

    add_q(db, p1.id, exam_dir, 1, 10, None,
        r"Which apparatus are needed for evaporation of salt solution? "
        r"(I tripod stand, II separating funnel, III Bunsen burner) "
        r"A I and II only  B I and III only  C II and III only  D all of the above",
        1, "Separation Techniques — Evaporation", 6, (5, 0.05, 0.50),
        "B — I and III only: a tripod stand and a Bunsen burner are needed; the "
        "separating funnel is not.",
        "B1", topic_id=105)

    add_q(db, p1.id, exam_dir, 1, 11, None,
        r"Potassium permanganate is a disinfectant with chemical formula KMnO₄. How many "
        r"elements does potassium permanganate have? "
        r"A 3  B 4  C 6  D 7",
        1, "Elements & Compounds", 6, (5, 0.50, 0.72),
        "A — 3 elements: potassium (K), manganese (Mn) and oxygen (O).",
        "B1", topic_id=104)

    add_q(db, p1.id, exam_dir, 1, 12, None,
        r"Which organism is not a decomposer? "
        r"A bacteria  B earthworm  C fungi  D virus",
        1, "Ecology — Decomposers", 6, (5, 0.72, 0.95),
        "D — a virus is not a decomposer; bacteria, earthworms and fungi decompose dead "
        "matter.",
        "B1", topic_id=107)

    add_q(db, p1.id, exam_dir, 1, 13, None,
        r"Given that each small square has a side of 2 cm, what is the approximate area of "
        r"the leaf shown? "
        r"A 27 cm²  B 41 cm²  C 82 cm²  D 164 cm²",
        1, "Measurement — Area", 7, (6, 0.05, 0.55),
        "C — counting roughly 20–21 whole squares, each 2 cm × 2 cm = 4 cm², gives about "
        "82 cm².",
        "B1", topic_id=102)

    add_q(db, p1.id, exam_dir, 1, 14, None,
        r"A boy wants to measure the internal diameter of a beaker with a Vernier caliper. "
        r"What is the appropriate jaws to use and the correct reading of the Vernier caliper? "
        r"A inside jaws, 3.14 cm  B inside jaws, 3.22 cm  "
        r"C outside jaws, 3.14 cm  D outside jaws, 3.22 cm",
        1, "Measurement — Vernier Caliper", 7, (6, 0.55, 0.98),
        "B — internal diameter is measured with the inside jaws; the reading shown is "
        "3.22 cm.",
        "B1", topic_id=102)

    add_q(db, p1.id, exam_dir, 1, 15, None,
        r"Corals have a symbiotic relationship with photosynthetic algae: the algae supply "
        r"oxygen, the corals supply shelter and raw materials. What type of symbiotic "
        r"relationship do the corals have with the photosynthetic algae? "
        r"A commensalism  B mutualism  C parasitism  D predation",
        1, "Interactions Between Organisms", 8, (7, 0.05, 0.62),
        "B — mutualism: both the coral and the algae benefit from the relationship.",
        "B1", topic_id=107)

    add_q(db, p1.id, exam_dir, 1, 16, None,
        r"Increased soil erosion caused suspended particles making waters cloudy, and "
        r"warming of the sea, leading to mass destruction of coral reefs. Which abiotic "
        r"factor is responsible for the mass destruction of the coral reefs? "
        r"A air  B humidity  C soil  D water",
        1, "Abiotic Factors", 8, (7, 0.62, 0.98),
        "D — water (its temperature and turbidity) is the abiotic factor causing the "
        "destruction.",
        "B1", topic_id=107)

    add_q(db, p1.id, exam_dir, 1, 17, None,
        r"Fig. 17.1 shows a cuboid of length 2 cm by 3 cm by 4 cm placed in a measuring "
        r"cylinder initially with some water (Fig. 17.2). What will be the final water "
        r"level in the measuring cylinder after the cuboid is placed inside? "
        r"A 38 cm³  B 42 cm³  C 62 cm³  D 66 cm³",
        1, "Measurement — Volume by Displacement", 9, (8, 0.05, 0.50),
        "C — volume of cuboid = 2 × 3 × 4 = 24 cm³; final level = 38 + 24 = 62 cm³.",
        "B1", topic_id=102)

    add_q(db, p1.id, exam_dir, 1, 18, None,
        r"In a particular ecosystem, squirrels make up a large portion of the diet of "
        r"coyotes. As a result of a fatal disease, the squirrel population begins to "
        r"reduce over a period of months. Which graph best represents the expected changes "
        r"in population size of the coyotes and the squirrels? "
        r"A  B  C  D",
        1, "Population Dynamics", 9, (8, 0.50, 0.98),
        "C — as the squirrel (prey) population falls, the coyote (predator) population "
        "subsequently falls too.",
        "B1", topic_id=107)

    add_q(db, p1.id, exam_dir, 1, 19, None,
        r"Refer to the classification key for questions 19 and 20 (vertebrate split at P "
        r"into Q [myna, penguin] and R [whale, S]; S splits into bat and T [lion, cow]). "
        r"At which interval does division of vertebrates into mammals and birds occur? "
        r"A P  B Q  C S  D T",
        1, "Classification Keys", 10, (9, 0.05, 0.55),
        "A — interval P separates the birds (myna, penguin) from the mammals "
        "(whale, bat, lion, cow).",
        "B1", topic_id=107)

    add_q(db, p1.id, exam_dir, 1, 20, None,
        r"Which description shows the correct division at interval R? "
        r"A Those that are big in size and those that are small in size. "
        r"B Those that fly and those that do not fly. "
        r"C Those that lay eggs and those that give birth to their young alive. "
        r"D Those that live in water and those that live on land.",
        1, "Classification Keys", 10, (9, 0.55, 0.98),
        "D — at R the whale (lives in water) is separated from the land mammals "
        "(bat, lion, cow).",
        "B1", topic_id=107)

    db.commit()
    count = len(p1.questions)
    print(f"Seeded Bartley Secondary School 2019 Science exam id={exam.id}: "
          f"Section A ({count} MCQs)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
