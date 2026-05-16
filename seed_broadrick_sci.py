"""Seed Broadrick Secondary School 2019 Sec 1 Express Science (Section A MCQ)."""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/science/2019-Sec-1-Express-Science-SA2-Broadrick-Secondary.pdf"
IMAGES_DIR = "/tmp/broadrick_sci_pages"

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

    school = db.query(School).filter(School.name == "Broadrick Secondary School").first()
    if not school:
        school = School(name="Broadrick Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(
        Exam.school_id == school.id, Exam.year == 2019,
        Exam.subject == "Science").first()
    if existing:
        print(f"Broadrick Science 2019 already seeded (id={existing.id}). Re-seeding.")
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
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # SECTION A — Multiple Choice, 30 questions, pages 3-13 (idx 0-12)
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=60, total_marks=30,
               date=date(2019, 10, 1),
               instructions="Section A. Answer all questions. Shade your answers in the OTAS provided.")
    db.add(p1); db.flush()

    add_q(db, p1.id, exam_dir, 1, 1,
        r"Which of the symbols should be printed on a bottle of alcohol?"
        "\n\nA. flammable symbol\nB. harmful/irritant symbol\nC. toxic (cross) symbol\nD. explosive symbol",
        "Laboratory Safety / Hazard Symbols", 101, 3, (0, 0.06, 0.24),
        "A — alcohol is flammable, so the flammable hazard symbol is used.")

    add_q(db, p1.id, exam_dir, 1, 2,
        r"Which of the following is a property of a luminous flame?"
        "\n\nA. It is invisible at a distance."
        "\nB. It does not produce soot."
        "\nC. It is produced when the air-hole is closed."
        "\nD. It is hotter than the non-luminous flame.",
        "Laboratory Apparatus — Bunsen flame", 101, 3, (0, 0.24, 0.36),
        "C — a luminous flame is produced when the air-hole is closed.")

    add_q(db, p1.id, exam_dir, 1, 3,
        r"Justin wants to find the volume of a cork by using a measuring cylinder. He uses a stone to keep the cork under water. The results of each stage of the experiment are shown. What is the volume of the cork?"
        "\n\nA. 2 cm$^3$\nB. 6 cm$^3$\nC. 22 cm$^3$\nD. 28 cm$^3$",
        "Measurement — Volume by displacement", 102, 3, (0, 0.36, 0.95),
        "B — cork volume = (water+cork+stone) − (water+stone) reading = 6 cm$^3$.")

    add_q(db, p1.id, exam_dir, 1, 4,
        r"Which of the following SI units are correctly matched?"
        "\n\nI. length — metre (m)\nII. time — minutes (min)\nIII. temperature — Kelvin (K)"
        "\n\nA. I and II only\nB. I and III only\nC. II and III only\nD. I, II and III",
        "Physical Quantities & Units", 102, 4, (1, 0.04, 0.20),
        "B — length is in metres and temperature in Kelvin; the SI unit of time is the second, not minutes.")

    add_q(db, p1.id, exam_dir, 1, 5,
        r"Huimin used a pair of vernier calipers to measure the diameter of a test tube. How large is the diameter of the test tube?"
        "\n\nA. 2.14 cm\nB. 2.15 cm\nC. 2.45 cm\nD. 2.54 cm",
        "Measurement — Vernier calipers", 102, 4, (1, 0.20, 0.46),
        "A — main scale 2 cm + vernier reading gives 2.14 cm.")

    add_q(db, p1.id, exam_dir, 1, 6,
        r"A student aims to investigate how an egg of the same density will behave in liquids of different densities. List the liquids P to S from the densest to the least dense."
        "\n\nA. P, Q, R, S\nB. S, R, Q, P\nC. R, Q, P, S\nD. S, P, Q, R",
        "Density — Floating and Sinking", 102, 4, (1, 0.46, 0.70),
        "B — the egg floats highest in the densest liquid; order densest to least is S, R, Q, P.")

    add_q(db, p1.id, exam_dir, 1, 7,
        r"An object is placed 5 m in front of a mirror. A boy sits between the object and the mirror and viewed that the image of the object is 7 m away from him. What is the distance between the boy and the object?"
        "\n\nA. 2 m\nB. 3 m\nC. 4 m\nD. 5 m",
        "Ray Model of Light — Reflection", 114, 4, (1, 0.70, 0.95),
        "B — image is 5 m behind mirror; boy is 7−5 = 2 m from mirror, so 5−2 = 3 m from the object.")

    add_q(db, p1.id, exam_dir, 1, 8,
        r"The diagram shows a ray of light entering a block of glass. Which numbered angles are the angles of incidence and of refraction?"
        "\n\nA. incidence 1, refraction 3\nB. incidence 1, refraction 4\nC. incidence 2, refraction 3\nD. incidence 2, refraction 4",
        "Ray Model of Light — Refraction", 114, 5, (2, 0.04, 0.40),
        "D — angle of incidence (2) and angle of refraction (4) are both measured from the normal.")

    add_q(db, p1.id, exam_dir, 1, 9,
        r"The following diagram shows the path of light as it passes through four substances. Which of the following options ranks the four substances in increasing order of density?"
        "\n\nA. glass, plastic, neon, hydrogen"
        "\nB. hydrogen, neon, glass, plastic"
        "\nC. hydrogen, neon, plastic, glass"
        "\nD. plastic, glass, neon, hydrogen",
        "Ray Model of Light — Refraction & Density", 114, 5, (2, 0.40, 0.95),
        "C — greater bending towards the normal indicates higher optical density: hydrogen, neon, plastic, glass.")

    add_q(db, p1.id, exam_dir, 1, 10,
        r"A student shines a narrow beam of white light into a prism. He sees a spectrum of colours emerging from the prism. Which three colours does he see at X, at Y and at Z?"
        "\n\nA. X violet, Y yellow, Z red"
        "\nB. X red, Y violet, Z yellow"
        "\nC. X red, Y yellow, Z violet"
        "\nD. X yellow, Y red, Z violet",
        "Ray Model of Light — Dispersion", 114, 6, (3, 0.04, 0.30),
        "A — violet is refracted most (X, top), then yellow (Y), then red least (Z).")

    add_q(db, p1.id, exam_dir, 1, 11,
        r"Which of the following statements is true?"
        "\n\nA. A magenta object appears red in blue light."
        "\nB. A blue object appears blue only in blue light."
        "\nC. A green object appears yellow in white light."
        "\nD. A black object appears black in light of any colour.",
        "Ray Model of Light — Colour", 114, 6, (3, 0.30, 0.50),
        "D — a black object absorbs all colours, so it appears black under any colour of light.")

    add_q(db, p1.id, exam_dir, 1, 12,
        r"A car is travelling at an average speed of 60 km/h. Calculate how far it would travel if the motorist starts at 0800 h and ends his journey at 0940 h."
        "\n\nA. 84 km\nB. 100 km\nC. 140 km\nD. 600 km",
        "Speed, Distance, Time", 112, 6, (3, 0.50, 0.70),
        "B — time = 1 h 40 min = 5/3 h; distance = 60 × 5/3 = 100 km.")

    add_q(db, p1.id, exam_dir, 1, 13,
        r"Mountain bike tires are specially designed to provide good grip on the ground. Four methods are suggested: add tread pattern on the tires; apply lubricating oil on tires; increase the width of tires; use a smooth material to make tires. How many method(s) will effectively improve the grip of mountain bike tires?"
        "\n\nA. 1\nB. 2\nC. 3\nD. 4",
        "Forces — Friction", 112, 6, (3, 0.70, 0.95),
        "B — adding a tread pattern and increasing tyre width both improve grip (2 methods).")

    add_q(db, p1.id, exam_dir, 1, 14,
        r"A brick with flat rectangular sides rests on a table. The brick is then turned so that it rests on the table on its smallest surface. Which row correctly shows how the force and pressure exerted by the brick on the table changed?"
        "\n\nA. force increased, pressure increased"
        "\nB. force increased, pressure unchanged"
        "\nC. force unchanged, pressure increased"
        "\nD. force unchanged, pressure unchanged",
        "Forces — Pressure", 112, 7, (4, 0.04, 0.28),
        "C — weight (force) is unchanged, but smaller contact area increases the pressure.")

    add_q(db, p1.id, exam_dir, 1, 15,
        r"Which are the correct units for friction, weight and pressure?"
        "\n\nA. friction N, weight N, pressure Pa"
        "\nB. friction kg, weight kg, pressure Pa"
        "\nC. friction kg, weight g, pressure kg/m$^2$"
        "\nD. friction N, weight N, pressure kg/m$^2$",
        "Forces — Units", 112, 7, (4, 0.28, 0.46),
        "A — friction and weight are forces measured in newtons (N); pressure is measured in pascals (Pa).")

    add_q(db, p1.id, exam_dir, 1, 16,
        r"A boy holds a 40-newton dumbbell at arm's length for 10 seconds. His arm is 1.5 metres above the ground. What is the work done by the force of the boy on the 40-newton dumbbell when he is holding it?"
        "\n\nA. 0 J\nB. 40 J\nC. 60 J\nD. 400 J",
        "Energy / Work", 111, 7, (4, 0.46, 0.66),
        "A — there is no movement in the direction of the force, so work done = 0 J.")

    add_q(db, p1.id, exam_dir, 1, 17,
        r"A ball rolls down a ramp. Assuming there is no friction, what is the highest possible position the ball can reach?"
        "\n\nA. position A\nB. position B\nC. position C\nD. position D",
        "Energy — Conservation", 111, 7, (4, 0.66, 0.95),
        "B — without friction, the ball can rise only to a height equal to its starting height (position B).")

    add_q(db, p1.id, exam_dir, 1, 18,
        r"Which of the following is a correct classification of an organelle, a cell, a tissue or an organ?"
        "\n\nA. cell — chloroplast\nB. organ — nucleus\nC. organelle — kidney\nD. tissue — blood",
        "Cells — Organisation", 107, 8, (5, 0.04, 0.24),
        "D — blood is a tissue (the others are mismatched).")

    add_q(db, p1.id, exam_dir, 1, 19,
        r"The table shows the composition of four foods in grams per 100 g portion. Which food would be most useful for providing an immediate source of energy?"
        "\n\nA. carbohydrate 69.2, fat 0.0, protein 0.5"
        "\nB. carbohydrate 8.6, fat 49.0, protein 28.1"
        "\nC. carbohydrate 0.0, fat 0.9, protein 18.0"
        "\nD. carbohydrate 4.8, fat 3.8, protein 3.3",
        "Human Digestive System — Nutrients", 109, 8, (5, 0.24, 0.46),
        "A — highest carbohydrate content provides the most immediate source of energy.")

    add_q(db, p1.id, exam_dir, 1, 20,
        r"The diagram represents stages in the breakdown of starch to maltose by the enzyme amylase. Which line is correct?"
        "\n\nA. starch P, maltose R, amylase Q"
        "\nB. starch Q, maltose R, amylase P"
        "\nC. starch Q, maltose P, amylase R"
        "\nD. starch R, maltose Q, amylase P",
        "Human Digestive System — Enzymes", 109, 8, (5, 0.46, 0.95),
        "B — substrate (starch) Q, products (maltose) R, enzyme amylase P.")

    add_q(db, p1.id, exam_dir, 1, 21,
        r"The diagram shows the human digestive system. Where is bile made, where is it stored and where does it act?"
        "\n\nA. made P, stored Q, acts R"
        "\nB. made P, stored R, acts T"
        "\nC. made Q, stored S, acts P"
        "\nD. made Q, stored T, acts S",
        "Human Digestive System — Bile", 109, 9, (6, 0.04, 0.46),
        "B — bile is made in the liver (P), stored in the gall bladder (R) and acts in the small intestine (T).")

    add_q(db, p1.id, exam_dir, 1, 22,
        r"In the outline of the Periodic Table shown below some elements are represented by numbers. Which two of these are non-metals in the same Period?"
        "\n\nA. 1 and 3\nB. 2 and 6\nC. 4 and 5\nD. 5 and 6",
        "Elements — Periodic Table", 104, 9, (6, 0.46, 0.95),
        "C — elements 4 and 5 are non-metals located in the same Period.")

    add_q(db, p1.id, exam_dir, 1, 23,
        r"The table gives the melting points, densities and electrical conductivities of four elements. Which element is copper?"
        "\n\nA. m.p. −38.9 °C, density 13.6 g/cm$^3$, good conductivity"
        "\nB. m.p. −7.2 °C, density 3.12 g/cm$^3$, poor conductivity"
        "\nC. m.p. 97.8 °C, density 0.97 g/cm$^3$, good conductivity"
        "\nD. m.p. 1083 °C, density 8.96 g/cm$^3$, good conductivity",
        "Elements — Properties of Metals", 104, 10, (7, 0.04, 0.30),
        "D — copper has a high melting point (1083 °C), density 8.96 g/cm$^3$ and good conductivity.")

    add_q(db, p1.id, exam_dir, 1, 24,
        r"The symbols (open and filled circles) represent particles of different elements. Which diagram shows a mixture of an element and a compound?"
        "\n\nA. diagram A\nB. diagram B\nC. diagram C\nD. diagram D",
        "Elements, Compounds & Mixtures", 104, 10, (7, 0.30, 0.95),
        "D — diagram D shows separate single-element particles together with bonded compound particles.")

    add_q(db, p1.id, exam_dir, 1, 25,
        r"Cobalt chloride has a chemical formula of CoCl$_2$. Four statements are made: "
        r"(1) Cobalt chloride is a mixture of elements. "
        r"(2) Cobalt chloride can be broken down by chemical methods. "
        r"(3) The constituent elements of cobalt chloride are carbon, oxygen and chlorine. "
        r"(4) There are two chlorine particles in cobalt chloride. Which of the statements are correct?"
        "\n\nA. 1 and 2 only\nB. 2 and 3 only\nC. 2 and 4 only\nD. 2, 3 and 4",
        "Elements, Compounds & Mixtures", 104, 11, (8, 0.04, 0.36),
        "C — statements 2 and 4 are correct: a compound can be broken down chemically and CoCl$_2$ has two chlorine atoms.")

    add_q(db, p1.id, exam_dir, 1, 26,
        r"A mixture can be classified as a solution or a suspension. Which of the following methods will not allow you to distinguish between a solution and a suspension?"
        "\n\nA. allow the mixture to stand for a period of time"
        "\nB. shine a beam of light through the mixture"
        "\nC. filter the mixture"
        "\nD. heat the mixture strongly",
        "Solutions & Solubility", 106, 11, (8, 0.36, 0.56),
        "D — heating the mixture strongly does not distinguish a solution from a suspension.")

    add_q(db, p1.id, exam_dir, 1, 27,
        r"A very old painting has been vandalised with new paint. The solubilities of the old and new paints in different solvents A, B, C and D are shown. Which solvent could be used to remove the vandalism without damaging the original paint?"
        "\n\nA. old paint insoluble, new paint insoluble"
        "\nB. old paint insoluble, new paint soluble"
        "\nC. old paint soluble, new paint insoluble"
        "\nD. old paint soluble, new paint soluble",
        "Solutions & Solubility", 106, 11, (8, 0.56, 0.95),
        "B — a solvent in which the old paint is insoluble but the new paint is soluble removes the vandalism safely.")

    add_q(db, p1.id, exam_dir, 1, 28,
        r"Singapore uses reverse osmosis as one of the separation techniques in the process of producing NEWater. Which one of the following best describes the process of reverse osmosis?"
        "\n\nA. A high pressure is used to push a solvent through a partially permeable membrane."
        "\nB. A low pressure is used to push a solvent through a partially permeable membrane."
        "\nC. A high pressure is used to force bacteria and viruses through a partially permeable membrane so that they are removed from the solution."
        "\nD. A low pressure is used to force bacteria and viruses through a partially permeable membrane for removal from the solution.",
        "Separation Techniques — Reverse osmosis", 105, 12, (9, 0.04, 0.42),
        "A — reverse osmosis uses high pressure to push the solvent (water) through a partially permeable membrane.")

    add_q(db, p1.id, exam_dir, 1, 29,
        r"The table shows steps that are used to separate a mixture containing iron filings, chalk powder and table salt. The steps are not in correct sequence: "
        r"(1) heating to dryness; (2) using a bar magnet; (3) dissolving in water; (4) filtering. "
        r"Which of the following shows the correct sequence to obtain these substances separately?"
        "\n\nA. 1 → 2 → 3 → 4\nB. 4 → 1 → 2 → 3\nC. 2 → 3 → 4 → 1\nD. 3 → 2 → 1 → 4",
        "Separation Techniques", 105, 12, (9, 0.42, 0.80),
        "C — remove iron with magnet (2), dissolve salt (3), filter out chalk (4), then evaporate to dryness for salt (1).")

    add_q(db, p1.id, exam_dir, 1, 30,
        r"The key shows one way to classify flowers according to the animals that they attract. Which animal would be attracted by a large, brightly coloured flower?"
        "\n\nA. bat\nB. bee\nC. bird\nD. moth",
        "Classification — Dichotomous Key", 107, 13, (10, 0.04, 0.55),
        "C — following the key, a large flower that is red or yellow (brightly coloured) attracts a bird.")

    db.commit()
    p1_count = len(p1.questions)
    print(f"Seeded Broadrick Science exam id={exam.id}: Section A ({p1_count} MCQs)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
