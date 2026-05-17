"""Seed Broadrick Secondary School SA1 (EOY) 2017 Sec 1 Express Science exam (MCQ Section A).

Re-transcribed from /Users/timmy/Downloads/sec1-papers/science/2017-Sec-1-Express-Science-SA1-Broadrick-Secondary.pdf
Section A = 30 MCQ (printed pages 3-13 = PDF idx 0-10).
Correct options taken from the marked Answer Scheme in the same PDF (PDF idx 23-33).
"""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/science/2017-Sec-1-Express-Science-SA1-Broadrick-Secondary.pdf"

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
        Exam.school_id == school.id, Exam.year == 2017,
        Exam.subject == "Science").first()
    if existing:
        print(f"Broadrick 2017 Science already seeded (id={existing.id}). Deleting and re-seeding.")
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
        source_pdf="2017-Sec-1-Express-Science-SA1-Broadrick-Secondary.pdf",
        status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)

    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=None, total_marks=30,
               date=date(2017, 10, 1),
               instructions="Section A: 30 MCQ (30 marks). Shade your answers in the OTAS provided.")
    db.add(p1); db.flush()

    def mcq(num, text, topic, topic_id, pg, top, bot, opts, ans):
        add_q(db, p1.id, exam_dir, 1, num, None,
              text + "\n\n" + opts, 1, topic, num, (pg, top, bot),
              ans, "B1", topic_id=topic_id)

    # ---- idx 0 (printed p3): Q1-Q3 ----
    mcq(1, r"Which of the symbols should be printed on a bottle of alcohol?",
        "Introduction to Science & the Laboratory", 101, 0, 0.12, 0.33,
        "A. flammable symbol\nB. corrosive symbol\nC. toxic symbol\nD. explosive symbol",
        "A — alcohol is flammable, so the flammable hazard symbol is used.")
    mcq(2, r"Which of the following is a property of a luminous flame?",
        "Introduction to Science & the Laboratory", 101, 0, 0.32, 0.50,
        "A. It is invisible at a distance.\nB. It does not produce soot.\n"
        "C. It is produced when the air-hole is closed.\nD. It is hotter than the non-luminous flame.",
        "C — a luminous (yellow) flame is produced when the air-hole of the Bunsen burner is closed.")
    mcq(3, r"Justin wants to find the volume of a cork by using a measuring cylinder. He uses a "
        r"stone to keep the cork under water. The results of each stage of the experiment "
        r"(water; water and cork; water, cork and stone; water and stone) are shown. "
        r"What is the volume of the cork?",
        "Physical Quantities, Units & Measurement", 102, 0, 0.50, 0.92,
        r"A. 2 cm$^3$" + "\n" + r"B. 6 cm$^3$" + "\n" + r"C. 22 cm$^3$" + "\n" + r"D. 28 cm$^3$",
        r"B — cork volume = (water+cork) reading minus water reading = 6 cm$^3$.")

    # ---- idx 1 (printed p4): Q4-Q7 ----
    mcq(4, r"Which of the following SI units are correctly matched? "
        r"(I length — metre (m); II time — minutes (min); III temperature — Kelvin (K))",
        "Physical Quantities, Units & Measurement", 102, 1, 0.05, 0.27,
        "A. I and II only\nB. I and III only\nC. II and III only\nD. I, II and III",
        "B — length (m) and temperature (K) are correct SI units; the SI unit of time is the second, not the minute.")
    mcq(5, r"Huimin used a pair of vernier calipers to measure the diameter of a test tube. "
        r"How large is the diameter of the test tube?",
        "Physical Quantities, Units & Measurement", 102, 1, 0.27, 0.50,
        "A. 2.14 cm\nB. 2.15 cm\nC. 2.45 cm\nD. 2.54 cm",
        "A — main scale reading plus vernier coincidence gives 2.14 cm.")
    mcq(6, r"A student aims to investigate how an egg of the same density will behave in liquids "
        r"of different densities P, Q, R and S. List the liquids P to S from the densest to the "
        r"least dense (based on how the egg floats/sinks in each).",
        "Physical Quantities, Units & Measurement", 102, 1, 0.50, 0.73,
        "A. P, Q, R, S\nB. S, R, Q, P\nC. R, Q, P, S\nD. S, P, Q, R",
        "A — the egg floats highest in the densest liquid; order from densest to least dense is P, Q, R, S.")
    mcq(7, r"An object is placed 5 m in front of a mirror. A boy sits between the object and the "
        r"mirror and views that the image of the object is 7 m away from him. What is the "
        r"distance between the boy and the object?",
        "Ray Model of Light", 114, 1, 0.73, 0.95,
        "A. 2 m\nB. 3 m\nC. 4 m\nD. 5 m",
        "B — image distance behind mirror equals object distance (5 m). Boy to image = 7 m, "
        "so boy to mirror = 7 − 5 = 2 m, hence boy to object = 5 − 2 = 3 m.")

    # ---- idx 2 (printed p5): Q8-Q9 ----
    mcq(8, r"The diagram shows a ray of light entering a block of glass (numbered angles 1, 2, 3, 4). "
        r"Which numbered angles are the angles of incidence and of refraction?",
        "Ray Model of Light", 114, 2, 0.05, 0.52,
        "A. incidence 1, refraction 3\nB. incidence 1, refraction 4\n"
        "C. incidence 2, refraction 3\nD. incidence 2, refraction 4",
        "D — angle of incidence (2) and angle of refraction (4) are both measured from the normal.")
    mcq(9, r"The diagram shows the path of light as it passes through four substances "
        r"(hydrogen, neon, glass, plastic). Which option ranks the four substances in "
        r"increasing order of density?",
        "Physical Quantities, Units & Measurement", 102, 2, 0.52, 0.92,
        "A. glass, plastic, neon, hydrogen\nB. hydrogen, neon, glass, plastic\n"
        "C. hydrogen, neon, plastic, glass\nD. plastic, glass, neon, hydrogen",
        "C — light bends more towards the normal in denser media; increasing density is "
        "hydrogen, neon, plastic, glass.")

    # ---- idx 3 (printed p6): Q10-Q13 ----
    mcq(10, r"A student shines a narrow beam of white light into a prism. He sees a spectrum of "
        r"colours emerging from the prism. Which three colours does he see at X, Y and Z?",
        "Ray Model of Light", 114, 3, 0.05, 0.40,
        "A. X = violet, Y = yellow, Z = red\nB. X = red, Y = violet, Z = yellow\n"
        "C. X = red, Y = yellow, Z = violet\nD. X = yellow, Y = red, Z = violet",
        "C — red is deviated least and violet most, so X = red, Y = yellow, Z = violet.")
    mcq(11, r"Which of the following statements is true?",
        "Ray Model of Light", 114, 3, 0.40, 0.58,
        "A. A magenta object appears red in blue light.\n"
        "B. A blue object appears blue only in blue light.\n"
        "C. A green object appears yellow in white light.\n"
        "D. A black object appears black in light of any colour.",
        "D — a black object absorbs all wavelengths and so appears black in light of any colour.")
    mcq(12, r"A car is travelling at an average speed of 60 km/h. Calculate how far it would "
        r"travel if the motorist starts at 0800 h and ends his journey at 0940 h.",
        "Physical Quantities, Units & Measurement", 102, 3, 0.58, 0.74,
        "A. 84 km\nB. 100 km\nC. 140 km\nD. 600 km",
        "B — time = 1 h 40 min = 5/3 h; distance = 60 × 5/3 = 100 km.")
    mcq(13, r"Mountain bike tyres are specially designed to provide good grip on the ground. "
        r"Four methods are suggested: add tread pattern; apply lubricating oil; increase the "
        r"width of the tyres; use a smooth material. How many method(s) will effectively "
        r"improve the grip of mountain bike tyres?",
        "Forces", 112, 3, 0.71, 0.99,
        "A. 1\nB. 2\nC. 3\nD. 4",
        "B — adding a tread pattern and increasing the tyre width both increase friction/grip "
        "(2 methods); oil and a smooth material reduce grip.")

    # ---- idx 4 (printed p7): Q14-Q17 ----
    mcq(14, r"A brick with flat rectangular sides rests on a table. The brick is then turned so "
        r"that it rests on the table on its smallest surface. Which row correctly shows how the "
        r"force and pressure exerted by the brick on the table changed?",
        "Forces", 112, 4, 0.05, 0.40,
        "A. force increased, pressure increased\nB. force increased, pressure unchanged\n"
        "C. force unchanged, pressure increased\nD. force unchanged, pressure unchanged",
        "C — the weight (force) is unchanged but the smaller contact area increases the pressure.")
    mcq(15, r"Which are the correct units for friction, weight and pressure?",
        "Forces", 112, 4, 0.40, 0.58,
        r"A. friction N, weight N, pressure Pa" + "\n"
        r"B. friction kg, weight kg, pressure Pa" + "\n"
        r"C. friction kg, weight g, pressure kg/m$^2$" + "\n"
        r"D. friction N, weight N, pressure kg/m$^2$",
        "A — friction and weight are forces measured in newtons (N); pressure is measured in pascals (Pa).")
    mcq(16, r"A boy holds a 40-newton dumbbell at arm's length for 10 seconds. His arm is 1.5 "
        r"metres above the ground. What is the work done by the force of the boy on the "
        r"40-newton dumbbell when he is holding it?",
        "Energy", 111, 4, 0.58, 0.74,
        "A. 0 J\nB. 40 J\nC. 60 J\nD. 400 J",
        "A — the dumbbell does not move (no displacement in the direction of force), so work done = 0 J.")
    mcq(17, r"A ball rolls down a ramp. Assuming there is no friction, what is the highest "
        r"possible position the ball can reach (positions A, B, C, D along the curve)?",
        "Energy", 111, 4, 0.74, 0.97,
        "A. position A\nB. position B\nC. position C\nD. position D",
        "B — by conservation of energy with no friction, the ball can rise to the same height "
        "as its starting point (position B).")

    # ---- idx 5 (printed p8): Q18-Q20 ----
    mcq(18, r"Which of the following is a correct classification of an organelle, a cell, a tissue "
        r"or an organ (classification — example)?",
        "Cells — The Basic Unit of Life", 107, 5, 0.05, 0.32,
        "A. cell — chloroplast\nB. organ — nucleus\nC. organelle — kidney\nD. tissue — blood",
        "D — blood is a tissue. (Chloroplast/nucleus are organelles; the kidney is an organ.)")
    mcq(19, r"The table shows the composition of four foods A, B, C and D in grams per 100 g "
        r"portion. Which food would be most useful for providing an immediate source of energy?",
        "Human Digestive System", 109, 5, 0.32, 0.55,
        "A. food A (carbohydrate 69.2, fat 0.0, protein 0.5)\n"
        "B. food B (carbohydrate 8.6, fat 49.0, protein 28.1)\n"
        "C. food C (carbohydrate 0.0, fat 0.9, protein 18.0)\n"
        "D. food D (carbohydrate 4.8, fat 3.8, protein 3.3)",
        "A — food A has the highest carbohydrate content, which provides an immediate source of energy.")
    mcq(20, r"The diagram represents stages in the breakdown of starch to maltose by the enzyme "
        r"amylase. Which line (starch / maltose / amylase) is correct?",
        "Human Digestive System", 109, 5, 0.55, 0.97,
        "A. starch P, maltose R, amylase Q\nB. starch Q, maltose R, amylase P\n"
        "C. starch Q, maltose P, amylase R\nD. starch R, maltose Q, amylase P",
        "B — substrate starch = Q, products maltose = R, enzyme amylase = P (the enzyme is "
        "unchanged and reused).")

    # ---- idx 6 (printed p9): Q21-Q22 ----
    mcq(21, r"The diagram shows the human digestive system (labels P, Q, R, S, T). "
        r"Where is bile made, where is it stored and where does it act?",
        "Human Digestive System", 109, 6, 0.05, 0.52,
        "A. made P, stored Q, acts R\nB. made P, stored R, acts T\n"
        "C. made Q, stored S, acts P\nD. made Q, stored T, acts S",
        "B — bile is made in the liver (P), stored in the gall bladder (R) and acts in the small intestine (T).")
    mcq(22, r"In the outline of the Periodic Table shown, some elements are represented by "
        r"numbers. Which two of these are non-metals in the same Period?",
        "Elements, Compounds & Mixtures", 104, 6, 0.52, 0.95,
        "A. 1 and 3\nB. 2 and 6\nC. 4 and 5\nD. 5 and 6",
        "C — elements 4 and 5 are both non-metals lying in the same Period (right-hand side, same row).")

    # ---- idx 7 (printed p10): Q23-Q24 ----
    mcq(23, r"The table gives the melting points, densities and electrical conductivities of four "
        r"elements. Which element is copper?",
        "Elements, Compounds & Mixtures", 104, 7, 0.05, 0.34,
        "A. melting point −38.9 °C, density 13.6, good\n"
        "B. melting point −7.2 °C, density 3.12, poor\n"
        "C. melting point 97.8 °C, density 0.97, good\n"
        "D. melting point 1083 °C, density 8.96, good",
        "D — copper has a high melting point (1083 °C), density 8.96 g/cm³ and is a good "
        "conductor of electricity.")
    mcq(24, r"The symbols (open circle and filled circle) represent particles of different "
        r"elements. Which diagram shows a mixture of an element and a compound?",
        "Elements, Compounds & Mixtures", 104, 7, 0.34, 0.97,
        "A. diagram A\nB. diagram B\nC. diagram C\nD. diagram D",
        "C — diagram C shows separate single-element particles together with bonded "
        "two-element (compound) particles, i.e. a mixture of an element and a compound.")

    # ---- idx 8 (printed p11): Q25-Q27 ----
    mcq(25, r"Cobalt chloride has a chemical formula of CoCl$_2$. Four statements are made: "
        r"(1) Cobalt chloride is a mixture of elements. (2) Cobalt chloride can only be broken "
        r"down by chemical methods. (3) The constituent elements of cobalt chloride are carbon, "
        r"oxygen and chlorine. (4) There are two chlorine particles in cobalt chloride. "
        r"Which of the statements are correct?",
        "Elements, Compounds & Mixtures", 104, 8, 0.05, 0.38,
        "A. 1 and 2 only\nB. 2 and 3 only\nC. 2 and 4 only\nD. 2, 3 and 4",
        "C — statements 2 and 4 are correct: a compound is broken down only by chemical means, "
        "and CoCl₂ contains two chlorine atoms.")
    mcq(26, r"A mixture can be classified as a solution or a suspension. Which of the following "
        r"methods will not allow you to distinguish between a solution and a suspension?",
        "Solutions & Solubility", 106, 8, 0.38, 0.56,
        "A. allow the mixture to stand for a period of time\n"
        "B. shine a beam of light through the mixture\n"
        "C. filter the mixture\nD. heat the mixture strongly",
        "D — strong heating evaporates the solvent in both cases and does not distinguish a "
        "solution from a suspension.")
    mcq(27, r"A very old painting has been vandalised with new paint. The solubilities of the old "
        r"and new paints in different solvents A, B, C and D are shown in the table. Which "
        r"solvent could be used to remove the vandalism without damaging the original paint?",
        "Solutions & Solubility", 106, 8, 0.56, 0.97,
        "A. old insoluble, new insoluble\nB. old insoluble, new soluble\n"
        "C. old soluble, new insoluble\nD. old soluble, new soluble",
        "B — solvent B dissolves the new (vandal) paint but not the old original paint.")

    # ---- idx 9 (printed p12): Q28-Q29 ----
    mcq(28, r"Singapore uses reverse osmosis as one of the separation techniques in the process "
        r"of producing NEWater. Which one of the following best describes the process of "
        r"reverse osmosis?",
        "Separation Techniques", 105, 9, 0.05, 0.40,
        "A. A high pressure is used to push a solvent through a partially permeable membrane.\n"
        "B. A low pressure is used to push a solvent through a partially permeable membrane.\n"
        "C. A high pressure is used to force bacteria and viruses through a partially "
        "permeable membrane so that they are removed from the solution.\n"
        "D. A low pressure is used to force bacteria and viruses through a partially permeable "
        "membrane for removal from the solution.",
        "A — reverse osmosis uses a high pressure to push the solvent (water) through a "
        "partially permeable membrane.")
    mcq(29, r"The table shows steps used to separate a mixture containing iron filings, chalk "
        r"powder and table salt. The steps are not in correct sequence: 1 heating to dryness; "
        r"2 using a bar magnet; 3 dissolving in water; 4 filtering. Which option shows the "
        r"correct sequence to obtain these substances separately?",
        "Separation Techniques", 105, 9, 0.40, 0.72,
        r"A. 1 $\to$ 2 $\to$ 3 $\to$ 4" + "\n" + r"B. 4 $\to$ 1 $\to$ 2 $\to$ 3" + "\n"
        r"C. 2 $\to$ 3 $\to$ 4 $\to$ 1" + "\n" + r"D. 3 $\to$ 2 $\to$ 1 $\to$ 4",
        r"C — use a magnet to remove iron filings (2), dissolve in water (3), filter off chalk "
        r"(4), then heat to dryness to recover the salt (1).")

    # ---- idx 10 (printed p13): Q30 ----
    mcq(30, r"The key shows one way to classify flowers according to the animals that they "
        r"attract. Which animal would be attracted by a large, brightly coloured (red or "
        r"yellow) flower?",
        "Cells — The Basic Unit of Life", 107, 10, 0.10, 0.62,
        "A. bat\nB. bee\nC. bird\nD. moth",
        "C — following the key, large + red or yellow colour leads to bird.")

    db.commit()
    print(f"Seeded Broadrick Science SA1/EOY 2017 exam id={exam.id}: Section A {len(p1.questions)} MCQs")
    print(f"Images in {exam_dir}")
    eid = exam.id
    db.close()
    return eid


if __name__ == "__main__":
    main()
