"""Seed Hillgrove Secondary School EOY 2017 Sec 1 Express Science exam (MCQ Section A)."""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/science/2017-Sec-1-Express-Science-SA2-Hillgrove-Secondary.pdf"
IMAGES_DIR = "/tmp/hillgrove_sci2017_pages"

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

    school = db.query(School).filter(School.name == "Hillgrove Secondary School").first()
    if not school:
        school = School(name="Hillgrove Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(
        Exam.school_id == school.id, Exam.year == 2017, Exam.subject == "Science"
    ).first()
    if existing:
        print(f"Hillgrove 2017 Science already seeded (id={existing.id}). Deleting and re-seeding.")
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
        source_pdf="2017-Sec-1-Express-Science-SA2-Hillgrove-Secondary.pdf",
        status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=105, total_marks=30,
               date=date(2017, 10, 2),
               instructions="Section A: 30 multiple-choice questions. Answer all questions.")
    db.add(p1); db.flush()

    Q = [
        (1, "A student wants to find out why a cactus is able to survive very long without water in its environment. Which attitude has he displayed?\nA curiosity\nB integrity\nC perseverance\nD responsibility",
         "Scientific Attitudes", 101, 2, (1, 0.05, 0.27), "A"),
        (2, "Which is a scientific investigation?\nA counting how many prime numbers there are between 100 to 300\nB conducting a survey to find out how many people listen to pop music\nC excavating to find out things which were used in ancient China\nD using cooking oil in cars to see whether it can be a substitute for liquid petroleum",
         "Scientific Method", 101, 2, (1, 0.27, 0.50), "D"),
        (3, "Annabelle noticed that paint on walls faded after some time. Which is a hypothesis for this observation?\nA Is the paint quality good?\nB Paint is a mixture.\nC Rain washed off the paint.\nD Samples of paint need to be analysed.",
         "Scientific Method — Hypothesis", 101, 2, (1, 0.50, 0.72), "C"),
        (4, "Which statement is inferred and not a direct observation?\nA A swan can fly.\nB Matter is made up of particles.\nC Pure ice freezes at 0 C.\nD The moon orbits around the Earth.",
         "Observation and Inference", 101, 2, (1, 0.72, 0.86), "B"),
        (5, "Which statement is correct about laboratory safety?\nA Drinking distilled water in the laboratory is allowed.\nB Entering the lab is not allowed without teacher's supervision.\nC Reporting accidents to the teacher only if someone is injured.\nD Tasting of chemicals is allowed when one is identifying them.",
         "Laboratory Safety", 101, 2, (1, 0.86, 1.0), "B"),
        (6, "Silicon carbide is a hard substance. This means that it ____.\nA can withstand weights without breaking\nB cannot be easily hammered into shapes\nC cannot be easily scratched\nD cannot go back to its original shape after being bent",
         "Physical Properties of Materials", 102, 3, (2, 0.05, 0.30), "C"),
        (7, "What is the laboratory apparatus shown (narrow-necked flask with conical body)?\nA beaker\nB conical flask\nC flat-bottomed flask\nD triangular beaker",
         "Laboratory Apparatus", 101, 3, (2, 0.30, 0.55), "B"),
        (8, "John wanted to see if sublimation will affect the density of a substance. He started with 100 g of solid iodine. After undergoing sublimation, only 80 g of solid iodine is left. What can you say about the density of solid iodine?\nA The density decreased by 20%.\nB The density decreased by 25%.\nC The density increased by 20%.\nD The density remained the same.",
         "Density", 102, 3, (2, 0.55, 0.78), "D"),
        (9, "The table shows properties of substances A, B, C and D (melting/boiling point and electrical conductivity in solid/liquid state). Which substance is most likely a metal?\nA A\nB B\nC C\nD D",
         "Properties of Metals", 104, 3, (2, 0.78, 1.0), "C"),
        (10, "The diagram shows the reading on a pair of Vernier calipers measuring the thickness of a book. The calipers has a zero error of +0.03 cm. What is the actual thickness of the book?\nA 3.42 cm\nB 3.45 cm\nC 3.48 cm\nD 3.50 cm",
         "Measurement — Vernier Calipers", 102, 4, (3, 0.05, 0.40), "A"),
        (11, "Ethanol is found in alcoholic drinks. Its chemical formula is C2H6O. This means that ethanol contains the elements ____.\nA carbon and hydrogen only\nB carbon and water only\nC copper, hydrogen and oxygen only\nD carbon, hydrogen and oxygen only",
         "Elements and Compounds", 104, 4, (3, 0.40, 0.62), "D"),
        (12, "Which diagram shows the model of a mixture of compound and element? (particle diagrams A, B, C, D)",
         "Elements, Compounds and Mixtures", 104, 4, (3, 0.62, 0.95), "D"),
        (13, "Which is the correct term to describe the mixture of sand and water?\nA emulsion\nB residue\nC solution\nD suspension",
         "Mixtures", 106, 5, (4, 0.05, 0.27), "D"),
        (14, "Which is a mixture?\nA alloy\nB mercury\nC salt\nD water",
         "Mixtures", 104, 5, (4, 0.27, 0.45), "A"),
        (15, "After separating salt solution into its components, salt and water, they ____.\nA chemically changed as the substances are chemically combined\nB chemically changed as the substances are physically mixed\nC remain chemically unchanged as the substances are chemically combined\nD remain chemically unchanged as the substances are physically mixed",
         "Separation Techniques", 105, 5, (4, 0.45, 0.67), "D"),
        (16, "Fractional distillation is best used to separate ____.\nA substances of boiling points that are far apart\nB substances of different but close boiling points\nC substances which are immiscible\nD substances with different solubilities",
         "Separation — Fractional Distillation", 105, 5, (4, 0.67, 0.82), "B"),
        (17, "When distilling a liquid, it is sometimes advisable to place porcelain chips in the distillation flask. This is because porcelain chips ____.\nA can absorb excess heat\nB can remove any impurities present\nC do not allow the liquid to boil till dryness\nD ensure smooth boiling",
         "Separation — Distillation", 105, 5, (4, 0.82, 1.0), "D"),
        (18, "The diagram shows a cross-section of a red blood cell. The red blood cell is biconcave. Which statement best explains the function of this adaptation?\nA It does not have a nucleus.\nB It has a larger surface area to absorb oxygen.\nC It has more space to contain oxygen.\nD It is easier to travel in the bloodstream.",
         "Specialised Cells — Red Blood Cell", 107, 6, (5, 0.05, 0.34), "B"),
        (19, "A scientist removed the cell wall of a unicellular organism. The cell continued to move and feed for several days. However, the cell died a few days later from an infection caused by a bacteria present in air. The experiment was repeated several times and similar results were obtained. What can be inferred from this experiment?\nA The cell wall gives the cell its regular shape.\nB The cell wall helps the cell feed better.\nC The cell wall helps to protect the cell.\nD The nucleus helps the cell to reproduce.",
         "Plant Cell Structure", 107, 6, (5, 0.34, 0.65), "C"),
        (20, "The small intestine is an organ because it is made up of ____.\nA different types of tissues working together\nB many different types of specialised cells\nC many tissues carrying out different tasks\nD same types of cells working together",
         "Cellular Organisation", 107, 6, (5, 0.65, 0.82), "A"),
        (21, "Which statement describes the behaviour of gaseous particles?\nA They are moving randomly at high speeds.\nB They are widely and equally spaced apart.\nC They settle to the bottom after some time.\nD They slide over one another.",
         "Particulate Nature of Matter", 103, 6, (5, 0.82, 1.0), "A"),
        (22, "The table shows the melting and boiling points of four substances A, B, C, D (A: mp -73, bp 60; B: mp -131, bp -1; C: mp 5, bp 5; D: mp 9, bp 103). Which substance has the weakest attractive force between its particles at 4 C?",
         "Particulate Nature of Matter — States", 103, 7, (6, 0.05, 0.27), "A"),
        (23, "Refer to the table of melting/boiling points of substances A, B, C, D. Which substance undergoes sublimation?",
         "Changes of State — Sublimation", 103, 7, (6, 0.27, 0.40), "B"),
        (24, "Which statement about particles is correct when liquid freezes to become a solid?\nA The particles decrease in size.\nB The particles stop moving.\nC The particles move further apart.\nD The speed of the particles decreases.",
         "Changes of State", 103, 7, (6, 0.40, 0.62), "D"),
        (25, "Dust particles in the air appear to move on their own in random directions. Which statement correctly explains this observation?\nA The dust particles change speed randomly.\nB The dust particles collide with gas particles in the air.\nC The dust particles collide with one another.\nD The dust particles collide with water particles.",
         "Particulate Nature of Matter — Brownian Motion", 103, 7, (6, 0.62, 0.80), "B"),
        (26, "Wei Meng found an element which contains 5 neutrons, 3 protons and 3 electrons. Which statement correctly identifies the identity of this element?\nA Beryllium, because it has 5 neutrons.\nB Lithium, because it has 3 protons.\nC Lithium, because it has 3 electrons.\nD Insufficient information was given to identify the element.",
         "Atomic Structure", 104, 7, (6, 0.80, 1.0), "B"),
        (27, "The table shows two bimetallic strips X and Y made of different metals P, Q, R (showing bending before/after heating). Which correctly arranges the worst thermal conductor to the best thermal conductor?\nA P, Q, R\nB Q, P, R\nC R, P, Q\nD R, Q, P",
         "Thermal Properties — Expansion", 102, 8, (7, 0.05, 0.40), "C"),
        (28, "The tyres of cars and bicycles deflate after some time. Which statement best explains this observation?\nA The air particles contract during cold weather and escape the tyres.\nB The tyres are made of rubber which loses elasticity and hence deflate.\nC The tyres contract during cold weather, making it look deflated.\nD There are tiny holes in the tyres which allow air particles to escape.",
         "Particulate Nature of Matter — Diffusion", 103, 8, (7, 0.40, 0.65), "D"),
        (29, "The diagram shows a saucepan. Which material is suitable to make the handles of a saucepan?\nA aluminium\nB brass\nC glass\nD plastic",
         "Thermal Properties — Conductors and Insulators", 102, 8, (7, 0.65, 0.95), "D"),
        (30, "The diagram shows a loop in a pipe that carries steam to a machine. The loop is necessary to ____.\nA allow for expansion of the pipe when hot\nB allow for contraction of the pipe when hot\nC increase the flow of steam in the pipe\nD reduce the flow of steam in the pipe",
         "Thermal Properties — Expansion", 102, 9, (8, 0.05, 0.55), "A"),
    ]

    for num, text, topic, tid, pg, crop, ans in Q:
        add_q(db, p1.id, exam_dir, 1, num, None, text, 1, topic, pg, crop,
              f"{ans}", "B1", topic_id=tid)

    db.commit()
    print(f"Seeded Hillgrove 2017 Science exam id={exam.id}: {len(p1.questions)} MCQs")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
