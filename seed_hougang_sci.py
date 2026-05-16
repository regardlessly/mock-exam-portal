"""Seed Hougang Secondary School SA1 2018 Sec 1 Express Science (Paper 1 MCQ)."""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/science/2018-Sec-1-Express-Science-SA1-Hougang-Secondary.pdf"
IMAGES_DIR = "/tmp/hougang_sci_pages"

init_db()


def add_q(db, paper_id, exam_dir, paper_num, num, text, topic, topic_id,
          pdf_page, crop_region, answer_text):
    img_name = f"q{paper_num}_{num}.png"
    img_path = os.path.join(exam_dir, img_name)
    pg, top, bot = crop_region
    crop_question_image(PDF_PATH, pg, top, bot, img_path)
    q = Question(
        paper_id=paper_id, question_number=num, part=None, stem=None,
        question_text=text, marks=1, topic=topic, topic_id=topic_id,
        page_image=img_name, pdf_page=pdf_page,
    )
    db.add(q)
    db.flush()
    db.add(Answer(question_id=q.id, answer_text=answer_text, mark_scheme="B1"))
    return q


def main():
    db = SessionLocal()

    school = db.query(School).filter(School.name == "Hougang Secondary School").first()
    if not school:
        school = School(name="Hougang Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(
        Exam.school_id == school.id, Exam.year == 2018,
        Exam.subject == "Science").first()
    if existing:
        print(f"Hougang Science 2018 already seeded (id={existing.id}). Re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id, title="Semestral Assessment 1 2018", year=2018,
        level="Secondary 1 Express", subject="Science",
        source_pdf="2018-Sec-1-Express-Science-SA1-Hougang-Secondary.pdf",
        status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # PAPER 1 — Multiple Choice, 20 questions, pages 2-6 (idx 1-5)
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=45, total_marks=20,
               date=date(2018, 5, 8), instructions="Answer all questions. Each question has four options A, B, C and D. Choose the one you consider correct.")
    db.add(p1); db.flush()

    add_q(db, p1.id, exam_dir, 1, 1,
        r"Which of the following examples is not an application of Science?"
        "\n\nA. explain the preference for chicken sandwich over tuna sandwich"
        "\nB. extraction of vanilla essence from vanilla beans using different edible solvents"
        "\nC. study the effect of different amount of fertiliser applied on the mass of fruit produced by fruit trees"
        "\nD. study the effect of river water temperature on the number of plants and animals",
        "Introduction to Science", 101, 2, (1, 0.04, 0.18),
        "A — explaining a preference for a sandwich is not a scientific investigation.")

    add_q(db, p1.id, exam_dir, 1, 2,
        r"A plant placed near a window slants towards the window. A scientist made a hypothesis that plants are able to move and they respond to light. He then planned an experiment which proved that his hypothesis was correct. Which attitude of the scientist is not displayed?"
        "\n\nA. compassion\nB. curiosity\nC. objectivity\nD. open-mindedness",
        "Scientific Method / Attitudes", 101, 2, (1, 0.18, 0.32),
        "A — compassion is not a scientific attitude displayed here.")

    add_q(db, p1.id, exam_dir, 1, 3,
        r"Blood samples found in the hospital are labelled with hazard symbols. Which of the following hazard symbols are found on the blood samples?"
        "\n\nA. flammable symbol\nB. biohazard symbol\nC. harmful/irritant (cross) symbol\nD. corrosive symbol",
        "Laboratory Safety / Hazard Symbols", 101, 2, (1, 0.33, 0.95),
        "B — blood samples are a biohazard, so the biohazard symbol is used.")

    add_q(db, p1.id, exam_dir, 1, 4,
        r"Which of the following describes the function of the apparatus shown below (a tripod stand)?"
        "\n\nA. for collecting gas during experiments"
        "\nB. for evaporating the liquid in a solution over a Bunsen burner"
        "\nC. for mixing chemicals to produce a gas when heating is not required"
        "\nD. for mixing chemicals to produce a gas when heating is required",
        "Laboratory Apparatus", 101, 3, (2, 0.04, 0.20),
        "A — the tripod stand supports apparatus over a Bunsen burner. (Answer key: A)")

    add_q(db, p1.id, exam_dir, 1, 5,
        r"Which of the following describes the function of the gas jet in a Bunsen burner?"
        "\n\nA. to control rate of gas flow into the gas jet"
        "\nB. to enable gas to rush out from the gas supply"
        "\nC. to raise the flame to a suitable height for burning"
        "\nD. to support the burner so that it will not topple over",
        "Laboratory Apparatus — Bunsen burner", 101, 3, (2, 0.20, 0.33),
        "B — the gas jet allows gas to rush out from the gas supply.")

    add_q(db, p1.id, exam_dir, 1, 6,
        r"Which of the following is an example of a safe laboratory practice?"
        "\n\nA. not tying the hair when carrying out experiments"
        "\nB. pieces of paper are placed near to the Bunsen flame"
        "\nC. pointing the mouth of a heated test-tube towards your face"
        "\nD. wearing a pair of safety goggles when carrying out heating experiments",
        "Laboratory Safety", 101, 3, (2, 0.33, 0.46),
        "D — wearing safety goggles during heating is safe lab practice.")

    add_q(db, p1.id, exam_dir, 1, 7,
        r"Which of the following physical quantities is correctly matched to its S.I. units?"
        "\n\nA. length — centimeter\nB. mass — gram\nC. temperature — degree Celsius\nD. time — second",
        "Physical Quantities & Units", 102, 3, (2, 0.46, 0.95),
        "D — the SI unit of time is the second.")

    add_q(db, p1.id, exam_dir, 1, 8,
        r"Which statement about density is incorrect?"
        "\n\nA. Density is defined as the volume per unit mass."
        "\nB. Density of a denser material has a higher value than a less dense object."
        "\nC. Density of a material decreases when heated."
        "\nD. Density of the same material is constant.",
        "Density", 102, 4, (3, 0.04, 0.16),
        "A — density is mass per unit volume, not volume per unit mass.")

    add_q(db, p1.id, exam_dir, 1, 9,
        r"A piece of copper and a piece of aluminium have the same volume. Given that the density of copper is 8.9 g/cm$^3$ and the density of aluminium is 2.7 g/cm$^3$, which of the following statements is true?"
        "\n\nA. Both objects have the same mass."
        "\nB. The mass of the aluminium and copper objects cannot be compared from the given information."
        "\nC. The mass of the aluminium object is higher than that of the copper object."
        "\nD. The mass of the copper object is higher than that of the aluminium object.",
        "Density", 102, 4, (3, 0.16, 0.34),
        "D — equal volume but higher density means copper has greater mass.")

    add_q(db, p1.id, exam_dir, 1, 10,
        r"A cuboid of 5 cm by 2 cm by 1 cm has a mass of 17.6 g. Which of the following is the density of the object?"
        "\n\nA. 0.568 g/cm$^3$\nB. 0.568 kg/m$^3$\nC. 1.76 g/cm$^3$\nD. 1.76 kg/m$^3$",
        "Density Calculation", 102, 4, (3, 0.34, 0.62),
        "C — density = 17.6 / (5×2×1) = 1.76 g/cm$^3$.")

    add_q(db, p1.id, exam_dir, 1, 11,
        r"Which of the following does not belong to the category of fibres?"
        "\n\nA. aluminium foil\nB. cotton\nC. nylon\nD. rayon",
        "Materials — Fibres", 101, 4, (3, 0.62, 0.74),
        "A — aluminium foil is a metal, not a fibre.")

    add_q(db, p1.id, exam_dir, 1, 12,
        r"Which element is a colourless gas that supports life processes in living organisms?"
        "\n\nA. chlorine\nB. nitrogen\nC. oxygen\nD. sulfur",
        "Elements", 104, 4, (3, 0.74, 0.95),
        "C — oxygen is a colourless gas that supports respiration.")

    add_q(db, p1.id, exam_dir, 1, 13,
        r"Which of the following elements has similar chemical properties as fluorine?"
        "\n\nA. bromine\nB. carbon\nC. helium\nD. oxygen",
        "Elements — Periodic Table", 104, 5, (4, 0.04, 0.16),
        "A — bromine is in the same group (halogens) as fluorine.")

    add_q(db, p1.id, exam_dir, 1, 14,
        r"The chemical compound, chalk, is made up of"
        "\n\nA. calcium, carbon and oxygen.\nB. calcium, hydrogen and oxygen.\nC. carbon, chlorine and hydrogen.\nD. carbon, chlorine and oxygen.",
        "Compounds", 104, 5, (4, 0.16, 0.28),
        "A — chalk (calcium carbonate) is made of calcium, carbon and oxygen.")

    add_q(db, p1.id, exam_dir, 1, 15,
        r"Which of the following is an example of a mixture?"
        "\n\nA. blood\nB. calcium carbonate\nC. magnesium\nD. sodium hydroxide",
        "Mixtures", 104, 5, (4, 0.28, 0.40),
        "A — blood is a mixture of cells and plasma.")

    add_q(db, p1.id, exam_dir, 1, 16,
        r"Which of the following statements does not show that sugar solution is a mixture?"
        "\n\nA. Sugar and water can be mixed in any proportion."
        "\nB. Sugar and water can be separated by physical separation methods."
        "\nC. Sugar solution has properties similar to that of sugar and water."
        "\nD. Sugar solution is a clear solution that allows light to pass through.",
        "Mixtures — Solutions", 106, 5, (4, 0.40, 0.58),
        "D — being a clear solution does not by itself show it is a mixture.")

    add_q(db, p1.id, exam_dir, 1, 17,
        r"Which mixture can be separated by magnetic attraction?"
        "\n\nA. chalk and sand\nB. nickel and salt\nC. pen ink mixture\nD. sugar solution",
        "Separation Techniques", 105, 5, (4, 0.58, 0.70),
        "B — nickel is magnetic and can be separated from salt by a magnet.")

    add_q(db, p1.id, exam_dir, 1, 18,
        r"Which of the following is a practical application of evaporation to dryness?"
        "\n\nA. extraction of colouring from flower petals"
        "\nB. extraction of iron from other scrap metals"
        "\nC. extraction of salt from seawater"
        "\nD. extraction of sugar from sugar cane sap",
        "Separation Techniques — Evaporation", 105, 5, (4, 0.70, 0.95),
        "C — salt is obtained from seawater by evaporation to dryness.")

    add_q(db, p1.id, exam_dir, 1, 19,
        r"The figure shows a distillation set-up. Which of the following statements explains the direction of cold water flow into the condenser?"
        "\n\nA. to decrease the surface area for faster condensation of water vapour"
        "\nB. to increase the boiling point of water"
        "\nC. to increase the surface area for faster condensation of water vapour"
        "\nD. to lower the boiling point of water",
        "Separation Techniques — Distillation", 105, 6, (5, 0.04, 0.32),
        "C — counter-current cold water flow maximises condensation of vapour.")

    add_q(db, p1.id, exam_dir, 1, 20,
        r"Why is reverse osmosis a preferred method of desalination as compared to simple distillation?"
        "\n\nA. Reverse osmosis has the ability to extract water that is less pure."
        "\nB. Reverse osmosis has the ability to extract water that is purer."
        "\nC. Reverse osmosis requires a higher amount of heat to extract water."
        "\nD. Reverse osmosis requires a lower amount of heat to extract water.",
        "Separation Techniques — Desalination", 105, 6, (5, 0.32, 0.55),
        "D — reverse osmosis needs little/no heat, unlike distillation.")

    db.commit()
    p1_count = len(p1.questions)
    print(f"Seeded Hougang Science exam id={exam.id}: Paper 1 ({p1_count} MCQs)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
