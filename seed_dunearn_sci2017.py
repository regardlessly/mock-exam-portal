"""Seed Dunearn Secondary School Mid-Year (SA1) 2017 Sec 1 Express Science exam (MCQ Section A)."""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/science/2017-Sec-1-Express-Science-SA1-Dunearn-Secondary.pdf"

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

    school = db.query(School).filter(School.name == "Dunearn Secondary School").first()
    if not school:
        school = School(name="Dunearn Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(
        Exam.school_id == school.id, Exam.year == 2017,
        Exam.subject == "Science").first()
    if existing:
        print(f"Dunearn 2017 Science already seeded (id={existing.id}). Deleting and re-seeding.")
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
        source_pdf="2017-Sec-1-Express-Science-SA1-Dunearn-Secondary.pdf",
        status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)

    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=120, total_marks=100,
               date=date(2017, 5, 3),
               instructions="Section A: 30 MCQ (30 marks). Answer all questions in this "
                            "section in the OTAS provided.")
    db.add(p1); db.flush()

    def mcq(num, text, topic, topic_id, pg, top, bot, opts, ans):
        add_q(db, p1.id, exam_dir, 1, num, None,
              text + "\n\n" + opts, 1, topic, num, (pg, top, bot),
              ans, "B1", topic_id=topic_id)

    # ---- idx 1 (page_02): Q1-Q3 ----
    mcq(1, r"How can the abuse and misuse of science and technology be reduced?",
        "Introduction to Science", 101, 1, 0.07, 0.32,
        "A. by adopting positive attitudes in science like responsibility and integrity\n"
        "B. by using skills and processes to inquire about the objects in the environment\n"
        "C. by using the scientific method\nD. by working together in a team", "A")
    mcq(2, r"Which of the following is the correct order of the steps to be carried out for a scientific method of investigation? (I analysing, II experimenting, III making a conclusion, IV making a hypothesis, V observing)",
        "Introduction to Science", 101, 1, 0.31, 0.58,
        "A. I, III, II, IV, V\nB. III, IV, II, I, V\nC. V, II, I, III, IV\nD. V, IV, II, I, III", "D")
    mcq(3, r"Joan carried out an experiment to test the hypothesis that plants grow slower when rock music is played to them. She used two young identical plants of the same height and placed one of them with rock music. Both plants were left untouched for one week. She then measured the increase in height of both plants at the end of the week. Which of the following is the variable to be measured (dependent variable) in this experiment?",
        "Introduction to Science", 101, 1, 0.57, 0.92,
        "A. increase in height of each plant at the end of the week\n"
        "B. length of time that the plants were left untouched\n"
        "C. presence of rock music\nD. type of plants used", "A")

    # ---- idx 2 (page_03): Q4-Q7 ----
    mcq(4, r"The diagram below shows a safety hazard symbol displayed on a bottle. Which of the following correctly describes the chemical found in the bottle?",
        "Laboratory Safety", 101, 2, 0.07, 0.34,
        "A. explosive\nB. flammable\nC. harmful\nD. oxidising", "D")
    mcq(5, r"Which of the following differences between a luminous and a non-luminous flame is incorrect?",
        "Laboratory Apparatus", 101, 2, 0.33, 0.58,
        "A. Luminous: easy to see from far; Non-luminous: not easy to see from far\n"
        "B. Luminous: flame is orange; Non-luminous: flame is blue\n"
        "C. Luminous: obtained when air-hole is open; Non-luminous: obtained when air-hole is closed\n"
        "D. Luminous: produces a lot of soot; Non-luminous: does not produce soot", "C")
    mcq(6, r"Why is the handle of a cooking pan made of plastic?",
        "Properties of Matter", 104, 2, 0.57, 0.74,
        "A. Plastic has a high melting point.\nB. Plastic has low electrical conductivity.\n"
        "C. Plastic is a bad conductor of heat.\nD. Plastic is resistant to corrosion.", "C")
    mcq(7, r"A stack of 100 identical sheets of plain A4-sized papers has a thickness of 1.2 cm. What is the thickness of each sheet of paper?",
        "Measurement", 102, 2, 0.73, 0.96,
        "A. 0.12 mm\nB. 1.2 mm\nC. 12 mm\nD. 120 mm", "A")

    # ---- idx 3 (page_04): Q8-Q9 ----
    mcq(8, r"The diagram shows a teaspoon and a tablespoon that are made from pure iron (Tea spoon mass 20 g, Table spoon mass 50 g). Which of the following statements is correct about the densities of the two types of spoon?",
        "Density", 102, 3, 0.07, 0.42,
        "A. Both types of spoon have the same density.\n"
        r"B. The densities of the teaspoon and the tablespoon are 20 g/cm$^3$ and 50 g/cm$^3$ respectively." + "\n"
        "C. The tablespoon has a higher density than the teaspoon.\n"
        "D. The teaspoon has a higher density than the tablespoon.", "A")
    mcq(9, r"The diagram shows a pair of vernier calipers. What is a possible use of the part labelled Z?",
        "Measurement", 102, 3, 0.41, 0.78,
        "A. to measure the circumference of a coin\nB. to measure the depth of a hole\n"
        "C. to measure the inner diameter of a tube\nD. to measure the thickness of a wire", "B")

    # ---- idx 4 (page_05): Q10-Q11 ----
    mcq(10, r"The diagram shows the zero error reading on a pair of vernier calipers with closed jaws. What is the zero error?",
        "Measurement", 102, 4, 0.07, 0.42,
        "A. - 0.07 cm\nB. - 0.03 cm\nC. + 0.03 cm\nD. + 0.07 cm", "A")
    mcq(11, r"The diagrams show onion cells and human cheek cells examined under a microscope. Which of the following structures is/are seen in both cells? (I cell membrane, II cell wall, III chloroplast, IV nucleus)",
        "Cells", 107, 4, 0.41, 0.78,
        "A. I only\nB. I and IV only\nC. II and III only\nD. II and IV only", "B")

    # ---- idx 5 (page_06): Q12-Q16 ----
    mcq(12, r"Which part of the plant cell is responsible for controlling substances entering or leaving the cell?",
        "Cells", 107, 5, 0.07, 0.24,
        "A. cell membrane\nB. cell wall\nC. chloroplast\nD. vacuole", "A")
    mcq(13, r"Which of the following is an organelle?",
        "Cells", 107, 5, 0.23, 0.40,
        "A. lung\nB. muscle\nC. nucleus\nD. plant cell", "C")
    mcq(14, r"Which part of the microscope is used to focus and sharpen images?",
        "Cells", 107, 5, 0.39, 0.55,
        "A. coarse adjustment knob\nB. eyepiece\nC. fine adjustment knob\nD. objectives", "C")
    mcq(15, r"The eyepiece of a microscope has a magnification of 10X. The objective lens has a magnification of 4X. What is the total magnification of the microscope?",
        "Cells", 107, 5, 0.54, 0.74,
        "A. 4X\nB. 10X\nC. 14X\nD. 40X", "D")
    mcq(16, r"Which of the following actions will increase the rate of vibrations of particles in a piece of metal?",
        "Particulate Nature of Matter", 103, 5, 0.73, 0.92,
        "A. bending the metal\nB. heating the metal\n"
        "C. stretching the metal\nD. stroking the metal with a magnet", "B")

    # ---- idx 6 (page_07): Q17-Q21 ----
    mcq(17, r"Which of the following statements about matter are true? (I Forces of attraction hold the particles in all solid matter together. II Matter is made up of small discrete particles. III The particles in all matter are the same. IV There are no forces of attraction between gas particles.)",
        "Particulate Nature of Matter", 103, 6, 0.07, 0.30,
        "A. I and II only\nB. II and III only\nC. II and IV only\nD. I, II and III", "A")
    mcq(18, r"Pollen grains suspended in water appear to move on their own. Which of the following statements correctly explains this observation?",
        "Particulate Nature of Matter", 103, 6, 0.29, 0.50,
        "A. The pollen grains collide with dissolved gas particles from the air.\n"
        "B. The pollen grains collide with one another.\n"
        "C. The pollen grains collide with the water particles.\n"
        "D. The water particles move towards an area of low concentration.", "C")
    mcq(19, r"What happens to the particles of an object during freezing?",
        "Particulate Nature of Matter", 103, 6, 0.49, 0.66,
        "A. decrease in speed and move closer together\n"
        "B. decrease in speed and move further apart\n"
        "C. increase in speed and move closer together\n"
        "D. increase in speed and move further apart", "A")
    mcq(20, r"Which of the following substances contains particles that move the fastest at 28 $^\circ$C?",
        "Particulate Nature of Matter", 103, 6, 0.65, 0.82,
        "A. ice\nB. oxygen\nC. petrol\nD. water", "B")
    mcq(21, r"Gas particles at room temperature are able to move at very high speeds. However, when a bottle of perfume is opened at the end of a large room, it might take several minutes before its smell can be detected at the other end. Which of the following explains this phenomenon?",
        "Particulate Nature of Matter", 103, 6, 0.81, 0.99,
        "A. Perfume particles move slower than the gas particles in the air.\n"
        "B. Random collisions occur among perfume particles.\n"
        "C. Random collisions occur between perfume particles and gas particles.\n"
        "D. Strong attractive forces exist between perfume particles and gas particles.", "C")

    # ---- idx 7 (page_08): Q22-Q25 ----
    mcq(22, r"Which of the following statements about boiling water is incorrect?",
        "Particulate Nature of Matter", 103, 7, 0.07, 0.30,
        "A. The forces of attraction between water particles become weaker.\n"
        "B. The spaces between the water particles increase.\n"
        "C. The water particles changes into a state with no definite volume.\n"
        "D. The water particles expand.", "D")
    mcq(23, r"The table shows the melting points and boiling points of five different substances P, Q, R, and S. Which substance(s) would be a solid at 22 $^\circ$C but a liquid at 100 $^\circ$C? (P: mp 95, bp 280; Q: mp 24, bp 74; R: mp -26, bp 37; S: mp 31, bp 140)",
        "Particulate Nature of Matter", 103, 7, 0.29, 0.55,
        "A. P only\nB. P and Q\nC. P and S\nD. P, Q and R", "C")
    mcq(24, r"Which diagram shows the arrangement of particles inside a balloon filled with a mixture of helium and argon (helium atom = small circle, argon atom = open circle)?",
        "Particulate Nature of Matter", 103, 7, 0.54, 0.78,
        "A. diagram A\nB. diagram B\nC. diagram C\nD. diagram D", "B")
    mcq(25, r"Which of the following will expand the least in volume when its temperature rises by 5 $^\circ$C?",
        "Particulate Nature of Matter", 103, 7, 0.77, 0.95,
        r"A. 100 cm$^3$ of hydrogen" + "\n" + r"B. 100 cm$^3$ of oil" + "\n"
        r"C. 100 cm$^3$ of water" + "\n" + r"D. 100 cm$^3$ of wood", "D")

    # ---- idx 8 (page_09): Q26-Q29 ----
    mcq(26, r"A freshly baked cake is placed on a table. Which of the following describes the way the cake loses heat?",
        "Energy", 111, 8, 0.07, 0.28,
        "A. by conduction only\nB. by convection only\n"
        "C. by conduction and convection\nD. by conduction, convection and radiation", "D")
    mcq(27, r"Four spoons of different materials were used to stir an equal amount of boiling water in a pot. Which spoon will heat up most quickly (wooden, steel, plastic, glass)?",
        "Energy", 111, 8, 0.27, 0.55,
        "A. wooden spoon\nB. steel spoon\nC. plastic spoon\nD. glass spoon", "B")
    mcq(28, r"An experimental setup is shown. The glass rod and the copper rod are of equal lengths. Each pin is attached to a rod with an equal amount of wax. Which pin will drop off last (pin A, B, C, D)?",
        "Energy", 111, 8, 0.54, 0.78,
        "A. pin A\nB. pin B\nC. pin C\nD. pin D", "A")
    mcq(29, r"Which of the following statements about radiation is incorrect?",
        "Energy", 111, 8, 0.77, 0.96,
        "A. Black surfaces are good emitters of radiation.\n"
        "B. Objects with higher temperature emit radiation at a lower rate.\n"
        "C. Objects with larger surface area absorb radiation at a higher rate.\n"
        "D. Radiation can travel through a vacuum.", "B")

    # ---- idx 9 (page_10): Q30 ----
    mcq(30, r"Which of the following diagrams shows the correct direction of the convection current set up in the box (smouldering paper and candle in a box with two glass chimneys)?",
        "Energy", 111, 9, 0.07, 0.55,
        "A. diagram A\nB. diagram B\nC. diagram C\nD. diagram D", "A")

    db.commit()
    print(f"Seeded Dunearn Science MYE/SA1 2017 exam id={exam.id}: Section A {len(p1.questions)} MCQs")
    print(f"Images in {exam_dir}")
    eid = exam.id
    db.close()
    return eid


if __name__ == "__main__":
    main()
