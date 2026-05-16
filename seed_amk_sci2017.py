"""Seed Ang Mo Kio Secondary School SA1 2017 Sec 1 Express Science exam (MCQ Section A)."""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/science/2017-Sec-1-Express-Science-SA1-Ang-Mo-Kio-Secondary.pdf"

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

    school = db.query(School).filter(School.name == "Ang Mo Kio Secondary School").first()
    if not school:
        school = School(name="Ang Mo Kio Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(
        Exam.school_id == school.id, Exam.year == 2017,
        Exam.subject == "Science").first()
    if existing:
        print(f"AMK 2017 Science already seeded (id={existing.id}). Deleting and re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id, title="Semestral Assessment 1 (SA1) 2017", year=2017,
        level="Secondary 1 Express", subject="Science",
        source_pdf="2017-Sec-1-Express-Science-SA1-Ang-Mo-Kio-Secondary.pdf",
        status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)

    # Section A: Multiple-Choice Questions (30 marks). Single paper.
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=120, total_marks=100,
               date=date(2017, 5, 2),
               instructions="Section A: 30 MCQ (30 marks). For each question, four "
                            "suggested answers are given. Choose the most appropriate one.")
    db.add(p1); db.flush()

    def mcq(num, text, topic, topic_id, pg, top, bot, opts, ans):
        add_q(db, p1.id, exam_dir, 1, num, None,
              text + "\n\n" + opts, 1, topic, num, (pg, top, bot),
              ans, "B1", topic_id=topic_id)

    # ---- Page idx 1 (page_02): A1-A3 ----
    mcq(1, r"What does 'open-mindedness' of a good scientist refer to?",
        "Introduction to Science", 101, 1, 0.10, 0.35,
        "A. To stick to the truth until the scientist's discovery is proven.\n"
        "B. To want to know more about the unexpected results that may be observed.\n"
        "C. To be willing to accept that something could happen contrary to popular belief.\n"
        "D. To follow the facts and not be influenced by what is widely believed by others.",
        "B")
    mcq(2, r"A container of a substance displays the hazard symbols (flammable and toxic) shown in the figure. The substance could be ______.",
        "Laboratory Safety", 101, 1, 0.34, 0.62,
        "A. acid\nB. alcohol\nC. mercury\nD. uranium", "B")
    mcq(3, r"The volume of water in a measuring cylinder should be read at the ______ of the meniscus in order to prevent ______ error.",
        "Measurement", 102, 1, 0.61, 0.92,
        "A. top, zero\nB. bottom, zero\nC. top, parallax\nD. bottom, parallax", "D")

    # ---- Page idx 2 (page_03): A4-A5 ----
    mcq(4, r"The picture shows a Bunsen burner. Which one of the following alternatives given below correctly represents I, II and III?",
        "Laboratory Apparatus", 101, 2, 0.07, 0.55,
        "A. I=gas jet, II=collar, III=barrel\nB. I=collar, II=barrel, III=gas jet\n"
        "C. I=barrel, II=collar, III=gas jet\nD. I=barrel, II=gas jet, III=collar", "A")
    mcq(5, r"The air-hole of a Bunsen burner can be opened or closed to obtain two types of flame. The colours of the flame are labelled W, X (air-hole open) and Y, Z (air-hole closed). Which option correctly states the colours of W, X, Y and Z?",
        "Laboratory Apparatus", 101, 2, 0.54, 0.97,
        "A. W=dark blue, X=orange, Y=dark blue, Z=orange\n"
        "B. W=orange, X=dark blue, Y=orange, Z=dark blue\n"
        "C. W=orange, X=dark blue, Y=blue, Z=dark blue\n"
        "D. W=blue, X=dark blue, Y=orange, Z=dark blue", "D")

    # ---- Page idx 3 (page_04): A6-A9 ----
    mcq(6, r"Which of the following options correctly states the disadvantage of a technology that benefits society?",
        "Introduction to Science", 101, 3, 0.07, 0.30,
        "A. Taking X-ray photographs too often may cause cancerous tumours.\n"
        "B. Too many motor vehicles on the roads pollute the water.\n"
        "C. Antibiotics increase our bodies' resistance to superbugs.\n"
        "D. Styrofoam pollutes the environment when it decomposes naturally.", "A")
    mcq(7, r"The apparatus shown (tripod stand) is commonly found in the laboratory. What is the function of the apparatus?",
        "Laboratory Apparatus", 101, 3, 0.29, 0.52,
        "A. For isolating setups from the outside.\n"
        "B. To contain and mix chemicals and liquids.\n"
        "C. To mix and heat chemicals and liquids evenly.\n"
        "D. To collect gases released from chemical reactions.", "B")
    mcq(8, r"Which one of the following has the same value as 75 cm$^2$?",
        "Measurement", 102, 3, 0.51, 0.74,
        r"A. 0.0075 m$^2$" + "\n" + r"B. 0.075 m$^2$" + "\n" + r"C. 0.75 m$^2$" + "\n" + r"D. 75 m$^2$", "A")
    mcq(9, r"What are the smallest lengths that can be measured by a pair of vernier calipers and a micrometer screw gauge?",
        "Measurement", 102, 3, 0.73, 0.96,
        "A. Vernier 0.1 mm, Micrometer 0.01 mm\n"
        "B. Vernier 0.01 mm, Micrometer 0.001 mm\n"
        "C. Vernier 0.1 cm, Micrometer 0.01 cm\n"
        "D. Vernier 0.01 cm, Micrometer 0.001 cm", "D")

    # ---- Page idx 4 (page_05): A10-A11 ----
    mcq(10, r"What is the estimated area for the heart-shaped diagram shown (drawn on a 1 cm grid)?",
        "Measurement", 102, 4, 0.08, 0.55,
        r"A. 16 cm$^2$" + "\n" + r"B. 18 cm$^2$" + "\n" + r"C. 20 cm$^2$" + "\n" + r"D. 22 cm$^2$", "C")
    mcq(11, r"The diagram shows the reading on a micrometer screw gauge when its jaws are closed. What is the zero error of the instrument?",
        "Measurement", 102, 4, 0.54, 0.95,
        "A. + 0.02 mm\nB. - 0.02 mm\nC. - 0.20 mm\nD. + 0.48 mm", "B")

    # ---- Page idx 5 (page_06): A12-A13 ----
    mcq(12, r"The graph shows the variation of the mass, m, of an object with its volume, V. Which statement about the graph is correct?",
        "Density", 102, 5, 0.07, 0.40,
        "A. The density of the object varies as volume increases.\n"
        "B. The density of the object remains constant as volume increases.\n"
        "C. The density of the object increases as volume increases.\n"
        "D. The density of the object decreases as volume increases.", "B")
    mcq(13, r"The diagram shows an experiment to test a certain property of liquids (battery, light bulb, metal rods in liquid). Which property is being tested?",
        "Properties of Matter", 104, 5, 0.39, 0.75,
        "A. density\nB. electrical conductivity\nC. magnetism\nD. solubility", "B")

    # ---- Page idx 6 (page_07): A14-A17 ----
    mcq(14, r"Most metals such as copper and iron have high melting points. Which of the following is an advantage of this property?",
        "Properties of Matter", 104, 6, 0.07, 0.30,
        "A. It prevents machine parts made of metal from rusting.\n"
        "B. It allows metal parts to be reshaped more easily.\n"
        "C. It keeps cars from becoming too hot on sunny days.\n"
        "D. It enables people to use pots and pans made of metal to cook food.", "D")
    mcq(15, r"According to the data in the table (Lustre, Flexible, Electrical Conductivity), which sample of matter is most likely to be a plastic?",
        "Properties of Matter", 104, 6, 0.29, 0.55,
        "A. sample 1\nB. sample 2\nC. sample 3\nD. sample 4", "D")
    mcq(16, r"Elements can be classified into ______.",
        "Elements, Compounds & Mixtures", 104, 6, 0.54, 0.75,
        "A. metals and non-metals\nB. mixtures and solutions\n"
        "C. solutions and suspensions\nD. chemical formulae and symbols", "A")
    mcq(17, r"Which of the following is a mixture of elements only?",
        "Elements, Compounds & Mixtures", 104, 6, 0.74, 0.95,
        "A. air\nB. brass\nC. chalk\nD. water", "B")

    # ---- Page idx 7 (page_08): A18-A22 ----
    mcq(18, r"When sugar is heated, decomposition occurs, forming carbon and water vapour. Which statement about decomposition is true?",
        "Elements, Compounds & Mixtures", 104, 7, 0.07, 0.32,
        "A. Compounds are broken down into simpler substances.\n"
        "B. Elements are broken down into simpler substances.\n"
        "C. Compounds combine to form new compounds.\n"
        "D. Elements combine to form compounds.", "A")
    mcq(19, r"How many different types of elements are present in ammonium sulfate, $(NH_4)_2SO_4$?",
        "Elements, Compounds & Mixtures", 104, 7, 0.31, 0.50,
        "A. 3\nB. 4\nC. 10\nD. 15", "B")
    mcq(20, r"The rate of dissolving of a solute refers to ______.",
        "Solutions & Solubility", 106, 7, 0.49, 0.68,
        "A. how much a solute dissolves in a fixed volume of solvent\n"
        "B. how much a solute dissolves in any volume of solvent\n"
        "C. how fast a solute dissolves in a fixed volume of solvent\n"
        "D. how fast a solute dissolves in any volume of solvent", "C")
    mcq(21, r"Which of the following pair of substances forms a solution with water?",
        "Solutions & Solubility", 106, 7, 0.67, 0.84,
        "A. glass and carbon\nB. glass and plastic\nC. plastic and sugar\nD. sugar and common salt", "D")
    mcq(22, r"Which of the following applications does not depend on water as the solvent?",
        "Solutions & Solubility", 106, 7, 0.83, 0.99,
        "A. Making alcoholic drinks.\nB. Making cooking oil.\n"
        "C. Making detergent.\nD. Making shampoo.", "B")

    # ---- Page idx 8 (page_09): A23-A27 ----
    mcq(23, r"Which of the following will form a suspension with water?",
        "Solutions & Solubility", 106, 8, 0.07, 0.26,
        "A. ethanol\nB. bread crumbs\nC. carbon dioxide gas\nD. ribena syrup", "B")
    mcq(24, r"Which of the following mixtures can be separated by magnetic attraction?",
        "Separation Techniques", 105, 8, 0.25, 0.46,
        "A. bronze and brass buttons\nB. copper and gold coins\n"
        "C. iron and zinc pins\nD. silver and aluminium foil", "C")
    mcq(25, r"What is the correct order of steps to separate salt from a mixture of soluble salt and insoluble pepper?",
        "Separation Techniques", 105, 8, 0.45, 0.66,
        r"A. filtration $\to$ dissolving $\to$ evaporation" + "\n"
        r"B. dissolving $\to$ filtration $\to$ evaporation" + "\n"
        r"C. filtration $\to$ evaporation $\to$ dissolving" + "\n"
        r"D. evaporation $\to$ dissolving $\to$ filtration", "B")
    mcq(26, r"Which of the following can be separated by simple distillation?",
        "Separation Techniques", 105, 8, 0.65, 0.82,
        "A. alcoholic beverages\nB. pulp from orange juice\nC. pen ink\nD. seawater", "D")
    mcq(27, r"Which property of a mixture enables paper chromatography to be used as a suitable separation technique?",
        "Separation Techniques", 105, 8, 0.81, 0.99,
        "A. Different extent of solubility of the substances in the mixture.\n"
        "B. Different melting point of the substances in the mixture.\n"
        "C. Different electrical conductivity of the substances in the mixture.\n"
        "D. Different density of the substances in the mixture.", "A")

    # ---- Page idx 9 (page_10): A28-A30 ----
    mcq(28, r"The diagram shows the process of filtration. At which point, A, B, C or D, represents the residue of the filtration?",
        "Separation Techniques", 105, 9, 0.07, 0.32,
        "A. point A\nB. point B\nC. point C\nD. point D", "B")
    mcq(29, r"When a mixture undergoes evaporation, ______.",
        "Separation Techniques", 105, 9, 0.31, 0.52,
        "A. both the solvent and solute are left behind\n"
        "B. both the solvent and solute are completely evaporated\n"
        "C. the solute is completely evaporated while only the solvent is left behind\n"
        "D. the solvent is completely evaporated while only the solute is left behind", "B")
    mcq(30, r"A student mixed sand, water and an unknown substance, then filtered. The filtrate was a clear liquid with no solids; the only residue was sand. Which conclusion can the student make?",
        "Separation Techniques", 105, 9, 0.51, 0.78,
        "A. The filtrate is pure water.\n"
        "B. The filtrate contains dissolved sand.\n"
        "C. The unknown substance is soluble in water.\n"
        "D. The unknown substance is a liquid at room temperature.", "C")

    db.commit()
    print(f"Seeded AMK Science SA1 2017 exam id={exam.id}: Section A {len(p1.questions)} MCQs")
    print(f"Images in {exam_dir}")
    eid = exam.id
    db.close()
    return eid


if __name__ == "__main__":
    main()
