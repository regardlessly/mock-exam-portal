"""Seed Outram Secondary School EOY 2022 Sec 1 Express Math exam."""

import os
import shutil
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/66b1f56285f50_5782.pdf"
IMAGES_DIR = "/tmp/outram_pages"

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

    school = db.query(School).filter(School.name == "Outram Secondary School").first()
    if not school:
        school = School(name="Outram Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(Exam.school_id == school.id, Exam.year == 2022).first()
    if existing:
        print(f"Outram 2022 already seeded (id={existing.id}). Deleting and re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id, title="End-of-Year Examination 2022", year=2022,
        level="Secondary 1 Express", subject="Mathematics",
        source_pdf="66b1f56285f50_5782.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # PAPER 1 — Pages 3-11 (idx 2-10), 50 marks, 1 hour
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=60, total_marks=50,
               date=date(2022, 10, 10), instructions="Answer all questions.")
    db.add(p1); db.flush()

    # Q1 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 1, "ai",
        r"Identify and write down the negative integer.",
        1, "Number Classification", 3, (2, 0.04, 0.22),
        r"$-\sqrt[3]{1000} = -10$", "B1",
        stem=r"Consider the following numbers: $(-6)^2$, $19$, $-\sqrt[3]{1000}$, $\pi$, $\dfrac{3}{7}$.",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 1, "aii",
        r"Identify and write down the irrational number.",
        1, "Number Classification", 3, (2, 0.22, 0.33),
        r"$\pi$", "B1",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 1, "b",
        r"Arrange the following numbers in descending order: $$\sqrt[3]{-343} \;,\; 5.4 \;,\; -3\tfrac{1}{2} \;,\; (-4)^2$$",
        2, "Ordering Numbers", 3, (2, 0.33, 0.55),
        r"$(-4)^2 = 16$, $5.4$, $-3\tfrac{1}{2} = -3.5$, $\sqrt[3]{-343} = -7$. Descending order: $16,\; 5.4,\; -3.5,\; -7$",
        "B1 for correct values, B1 for correct order",
        topic_id=2)

    # Q2 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 2, "a",
        r"Find the value of the cube root of $p$.",
        1, "Prime Factorisation / Cube Root", 3, (2, 0.55, 0.78),
        r"$\sqrt[3]{p} = \sqrt[3]{3^6 \times 5^3} = 3^2 \times 5 = 45$", "B1",
        stem=r"When written as the product of their prime factors, $p$ is $3^6 \times 5^3$, $q$ is $2^2 \times 3^3 \times 5$, $r$ is $2 \times 3^2$.",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 2, "b",
        r"Find the HCF of $p$, $q$ and $r$, giving your answer as the product of its prime factors.",
        1, "HCF", 3, (2, 0.78, 0.95),
        r"$\text{HCF} = 3^2$", "B1",
        topic_id=1)

    # Q3 — Page 4 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 3, "a",
        r"Express $9261$ in terms of its prime factors.",
        2, "Prime Factorisation", 4, (3, 0.04, 0.30),
        r"$9261 = 3^3 \times 7^3$", "M1, A1",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 3, "b",
        r"Explain why $9261$ is a perfect cube.",
        1, "Perfect Cube", 4, (3, 0.30, 0.47),
        r"The powers of all the prime factors are multiples of 3.", "B1",
        topic_id=1)

    # Q4 — Page 4 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 4, None,
        r"Three bells chime every 12 minutes, 15 minutes, and 21 minutes respectively. Given that they chime together at 08 00, at what time will they next chime together again?",
        2, "LCM", 4, (3, 0.47, 0.95),
        r"$\text{LCM}(12, 15, 21) = 2^2 \times 3 \times 5 \times 7 = 420$ minutes $= 7$ hours. Next chime at $15\!:\!00$ (3 p.m.)",
        "M1 for LCM, A1",
        topic_id=1)

    # Q5 — Page 5 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 5, None,
        r"Given that $a = 4$, $b = -3$ and $c = 2$, evaluate $b^2 - 3c + 2a$. Show your substitution step clearly.",
        2, "Algebraic Substitution", 5, (4, 0.04, 0.28),
        r"$(-3)^2 - 3(2) + 2(4) = 9 - 6 + 8 = 11$", "M1, A1",
        topic_id=4)

    # Q6 — Page 5 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 6, "a",
        r"Expand and simplify $4 + 5(3x - 2)$.",
        1, "Algebra — Expansion", 5, (4, 0.28, 0.55),
        r"$4 + 15x - 10 = 15x - 6$", "B1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 6, "b",
        r"Factorise $6ab - 2ac$.",
        1, "Algebra — Factorisation", 5, (4, 0.55, 0.95),
        r"$2a(3b - c)$", "B1",
        topic_id=4)

    # Q7 — Page 6 (idx 5)
    add_q(db, p1.id, exam_dir, 1, 7, "a",
        r"Solve $5x + 3(4 - x) = 8x$.",
        2, "Solving Linear Equations", 6, (5, 0.04, 0.33),
        r"$5x + 12 - 3x = 8x \implies 12 = 6x \implies x = 2$", "M1, A1",
        stem=r"Solve the following equations:",
        topic_id=5)

    add_q(db, p1.id, exam_dir, 1, 7, "b",
        r"Solve $\dfrac{7x + 5}{3} = \dfrac{4x + 3}{2}$.",
        2, "Solving Linear Equations", 6, (5, 0.33, 0.62),
        r"$2(7x + 5) = 3(4x + 3) \implies 14x + 10 = 12x + 9 \implies 2x = -1 \implies x = -\dfrac{1}{2}$",
        "M1, A1",
        topic_id=5)

    # Q8 — Page 6 (idx 5)
    add_q(db, p1.id, exam_dir, 1, 8, None,
        r"Express $\dfrac{3(x+2)}{4} - \dfrac{2(x-1)}{2}$ as a single fraction in its simplest form.",
        3, "Algebraic Fractions", 6, (5, 0.62, 0.95),
        r"$$\frac{3(x+2) - 4(x-1)}{4} = \frac{3x + 6 - 4x + 4}{4} = \frac{-x + 10}{4}$$",
        "M1 for LCD, M1 for expansion, A1",
        topic_id=4)

    # Q9 — Page 7 (idx 6)
    add_q(db, p1.id, exam_dir, 1, 9, "a",
        r"Find the value of $x$ such that $15 : 2x = 5 : 4$.",
        2, "Ratio", 7, (6, 0.04, 0.22),
        r"$15 \times 4 = 2x \times 5 \implies 60 = 10x \implies x = 6$", "M1, A1",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 9, "b",
        r"The lengths of a triangle $XYZ$ are such that $XY : YZ : ZX = 2 : 3 : 3$. Given that $XY = 15$ cm, find the perimeter of triangle $XYZ$.",
        2, "Ratio", 7, (6, 0.22, 0.50),
        r"$2$ units $\to 15$ cm, $1$ unit $= 7.5$ cm. Perimeter $= (2+3+3) \times 7.5 = 60$ cm",
        "M1, A1",
        topic_id=9)

    # Q10 — Page 7 (idx 6)
    add_q(db, p1.id, exam_dir, 1, 10, "a",
        r"Convert $65.5\%$ to a fraction in its simplest form.",
        1, "Percentage to Fraction", 7, (6, 0.50, 0.63),
        r"$\dfrac{131}{200}$", "B1",
        topic_id=8)

    add_q(db, p1.id, exam_dir, 1, 10, "b",
        r"Given that $35\%$ of $y$ is $175$. Find the value of $y$.",
        1, "Percentage", 7, (6, 0.63, 0.76),
        r"$y = \dfrac{100}{35} \times 175 = 500$", "B1",
        topic_id=8)

    add_q(db, p1.id, exam_dir, 1, 10, "c",
        r"Jia Jun got 8 out of 10 marks in Test $A$, 56 out of 65 in Test $B$. Assuming Test $A$ and Test $B$ are of similar difficulty, which test did Jia Jun perform better? Justify your answer.",
        2, "Percentage — Comparison", 7, (6, 0.76, 0.95),
        r"Test A: $\frac{8}{10} \times 100\% = 80\%$. Test B: $\frac{56}{65} \times 100\% \approx 86.2\%$. Jia Jun did better in Test B because the percentage is higher.",
        "M1, A1",
        topic_id=8)

    # Q11 — Page 8 (idx 7)
    add_q(db, p1.id, exam_dir, 1, 11, None,
        r"Jaden bought 120 handphones that cost &#36;500 each. He sold 60% of them at &#36;600 each and the remainder at a loss of 20%. Did Jaden make a profit or a loss? Calculate the amount of profit / loss.",
        4, "Percentage — Profit and Loss", 8, (7, 0.04, 0.70),
        r"""60% of 120 $= 72$ phones sold at $\$600$ each $= \$43\,200$
Remaining $= 48$ phones at 20% loss: $\$500 \times 0.8 = \$400$ each $= \$19\,200$
Total revenue $= 43\,200 + 19\,200 = \$62\,400$
Total cost $= 120 \times 500 = \$60\,000$
Jaden made a profit of $\$2\,400$.""",
        "M1 for revenue from 60%, M1 for loss price, M1 for total, A1",
        topic_id=8)

    # Q12 — Page 9 (idx 8)
    add_q(db, p1.id, exam_dir, 1, 12, "a",
        r"Find the value of $a$.",
        2, "Kite Properties — Algebra", 9, (8, 0.04, 0.55),
        r"Adjacent sides of a kite are equal: $2a + 3 = 3(2a - 1) \implies 2a + 3 = 6a - 3 \implies 4a = 6 \implies a = 1.5$",
        "M1, A1",
        stem=r"Figure $WXYZ$ is a kite with $WX = (2a + 3)$ cm, $XY = 3(2a - 1)$ cm.",
        topic_id=11)

    add_q(db, p1.id, exam_dir, 1, 12, "b",
        r"Find the value of $b$.",
        2, "Kite Properties — Angles", 9, (8, 0.55, 0.95),
        r"Diagonals of a kite bisect at $90°$: $3b + 2b + 90 = 180 \implies 5b = 90 \implies b = ...$. From marking: $9b + 90 = 180 \implies 9b = 90 \implies b = 10$",
        "M1, A1",
        topic_id=11)

    # Q13 — Page 10 (idx 9)
    add_q(db, p1.id, exam_dir, 1, 13, None,
        r"The following diagram shows part of a regular polygon. How many sides does the polygon have?",
        2, "Polygon — Number of Sides", 10, (9, 0.04, 0.32),
        r"Exterior angle $= 180° - 156° = 24°$. Number of sides $= \frac{360°}{24°} = 15$",
        "M1, A1",
        topic_id=11)

    # Q14 — Page 10 (idx 9)
    add_q(db, p1.id, exam_dir, 1, 14, "a",
        r"Use the formula to find $T_2$ and $T_8$.",
        2, "Number Patterns", 10, (9, 0.32, 0.62),
        r"$T_2 = 2(2) + 3 = 7$, $T_8 = 2(8) + 3 = 19$", "B1, B1",
        stem=r"The $n$th term of a sequence is given by $T_n = 2n + 3$.",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 14, "b",
        r"Is '$28$' a term in this sequence? Show your working and give a reason to support your answer.",
        2, "Number Patterns — Reasoning", 10, (9, 0.62, 0.88),
        r"$28 = 2n + 3 \implies 25 = 2n \implies n = 12.5$. Since $n$ is not an integer, $28$ is not a term in the sequence.",
        "M1, A1",
        topic_id=7)

    # Q15 — Page 11 (idx 10)
    add_q(db, p1.id, exam_dir, 1, 15, None,
        r"The following diagram shows a rectangular tank containing some water. Find the surface area of the tank that is in contact with the water.",
        2, "Surface Area — Rectangular Tank", 11, (10, 0.04, 0.47),
        r"""Surface area in contact $= [(25 \times 20 + 32 \times 28) \times 2] + (32 \times 20) = 3296$ m$^2$""",
        "M1, A1",
        stem=r"Rectangular tank: length $= 32$ m, width $= 28$ m, height $= 25$ m, water level $= 20$ m.",
        topic_id=13)

    # Q16 — Page 11 (idx 10)
    add_q(db, p1.id, exam_dir, 1, 16, "a",
        r"Find the value of $x$.",
        2, "Angle Properties — Parallel Lines", 11, (10, 0.47, 0.80),
        r"$x = 180° - 138° = 42°$ (co-interior angles, $AB \parallel CD$)", "M1, A1",
        stem=r"In the following diagram, $AB \parallel CD$.",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 16, "b",
        r"Find the value of $y$.",
        2, "Angle Properties — Parallel Lines", 11, (10, 0.80, 0.95),
        r"$y = 180° - 42° - 76° = 62°$", "M1, A1",
        topic_id=10)

    # ══════════════════════════════════════════════
    # PAPER 2 — Pages 12-22 (idx 11-21), 50 marks, 1h30m
    # ══════════════════════════════════════════════
    p2 = Paper(exam_id=exam.id, paper_number=2, duration_minutes=90, total_marks=50,
               date=date(2022, 10, 13), instructions="Answer all questions.")
    db.add(p2); db.flush()

    # P2 Q1 — Page 13 (idx 12)
    add_q(db, p2.id, exam_dir, 2, 1, "a",
        r"What is Mrs Tan's age in 3 years' time in terms of $x$?",
        1, "Algebra — Expression", 13, (12, 0.04, 0.38),
        r"$5x + 3$", "B1",
        stem=r"Mrs Tan is 5 times as old as her daughter now. In 3 years' time, the sum of their ages will be 48 years. If her daughter is $x$ years old now,",
        topic_id=4)

    add_q(db, p2.id, exam_dir, 2, 1, "b",
        r"How old is Mrs Tan now?",
        2, "Linear Equations — Word Problem", 13, (12, 0.38, 0.60),
        r"$(x + 3) + (5x + 3) = 48 \implies 6x + 6 = 48 \implies x = 7$. Mrs Tan $= 5 \times 7 = 35$ years old.",
        "M1, A1",
        topic_id=5)

    # P2 Q2 — Page 13 (idx 12)
    add_q(db, p2.id, exam_dir, 2, 2, None,
        r"Expand and simplify $3(x + 2y) - 4(y - x)$.",
        2, "Algebra — Expansion", 13, (12, 0.60, 0.95),
        r"$3x + 6y - 4y + 4x = 7x + 2y$", "M1, A1",
        topic_id=4)

    # P2 Q3 — Page 14 (idx 13)
    add_q(db, p2.id, exam_dir, 2, 3, None,
        r"Solve $\dfrac{2(1 - 3r)}{3} + \dfrac{3r + 5}{2} = 3$.",
        3, "Solving Linear Equations", 14, (13, 0.04, 0.40),
        r"""$$\frac{4(1-3r) + 3(3r+5)}{6} = 3$$
$$4 - 12r + 9r + 15 = 18$$
$$-3r + 19 = 18 \implies r = \frac{1}{3}$$""",
        "M1 for LCD, M1 for expanding, A1",
        topic_id=5)

    # P2 Q4 — Page 14 (idx 13)
    add_q(db, p2.id, exam_dir, 2, 4, "a",
        r"Without using a calculator, estimate the value of $\dfrac{13.4 \times 4.8}{5.49}$ by rounding off each number in the expression to 1 significant figure.",
        2, "Estimation", 14, (13, 0.40, 0.72),
        r"$$\approx \frac{10 \times 5}{5} = \frac{50}{5} = 10$$", "M1, A1",
        topic_id=3)

    add_q(db, p2.id, exam_dir, 2, 4, "b",
        r"Using a calculator, work out the value of $\sqrt{\dfrac{10.5 \times 7.89}{3.46}}$. Leave your answer to 2 decimal places.",
        1, "Calculator Use", 14, (13, 0.72, 0.95),
        r"$= 1.41$ (2 d.p.)", "A1",
        topic_id=3)

    # P2 Q5 — Page 15 (idx 14)
    add_q(db, p2.id, exam_dir, 2, 5, "a",
        r"Find the number of crosses in Pattern 4.",
        1, "Number Patterns", 15, (14, 0.04, 0.37),
        r"$20$", "B1",
        stem=r"The diagram shows a sequence of patterns made of crosses.",
        topic_id=7)

    add_q(db, p2.id, exam_dir, 2, 5, "b",
        r"Find an expression, in terms of $n$, for the total number of crosses in the $n$th figure.",
        1, "Number Patterns — General Term", 15, (14, 0.37, 0.58),
        r"$n(n + 1)$", "B1",
        topic_id=7)

    add_q(db, p2.id, exam_dir, 2, 5, "c",
        r"Which figure has 11130 crosses?",
        1, "Number Patterns", 15, (14, 0.58, 0.80),
        r"$n(n+1) = 11130$, $n = 105$ since $105 \times 106 = 11130$. Figure $105$.", "B1",
        topic_id=7)

    # P2 Q6 — Page 16 (idx 15)
    add_q(db, p2.id, exam_dir, 2, 6, "a",
        r"Find angle $CDB$.",
        2, "Angle Properties — Parallel Lines", 16, (15, 0.04, 0.56),
        r"""$\angle EFA = 104° - 46° = 58°$ (corr. $\angle$s)
$\angle CDB = 58°$ (alt. $\angle$s)""",
        "M1, A1",
        stem=r"In the figure, $EC \parallel GB$, $AF \parallel BC$. Angle $CEF = 60°$, angle $GAF = 104°$ and angle $CBD = 46°$.",
        topic_id=10)

    add_q(db, p2.id, exam_dir, 2, 6, "b",
        r"Find reflex angle $EFA$.",
        3, "Angle Properties — Parallel Lines", 16, (15, 0.56, 0.95),
        r"""$\angle EFA = 60° + 76° = 136°$ (alt. $\angle$s, int. $\angle$s)
Reflex $\angle EFA = 360° - 136° = 224°$""",
        "M1 for $\\angle EFA$, M1 for reflex, A1",
        topic_id=10)

    # P2 Q7 — Page 17 (idx 16)
    add_q(db, p2.id, exam_dir, 2, 7, "a",
        r"Find the number of cars in the town in 2020.",
        1, "Pictogram — Reading", 17, (16, 0.04, 0.36),
        r"$3.5 \times 6000 = 21\,000$", "B1",
        stem=r"The pictogram represents the number of cars in a town across the years. Each car symbol represents 6000 cars.",
        topic_id=14)

    add_q(db, p2.id, exam_dir, 2, 7, "b",
        r"Calculate the percentage decrease in the number of cars in the town between 2018 and 2021.",
        2, "Percentage Decrease", 17, (16, 0.36, 0.54),
        r"2018: $24\,000$, 2021: $12\,000$. Decrease $= \frac{24000 - 12000}{24000} \times 100\% = 50\%$",
        "M1, A1",
        topic_id=14)

    add_q(db, p2.id, exam_dir, 2, 7, "c",
        r"What is one disadvantage of representing the above data using a pictogram?",
        1, "Statistics — Representation", 17, (16, 0.54, 0.68),
        r"It is difficult to represent values using partial icons.", "B1",
        topic_id=14)

    add_q(db, p2.id, exam_dir, 2, 7, "d",
        r"The above data can also be represented using a pie chart. Calculate the angle that represents the number of cars in the town in 2019.",
        2, "Pie Chart Angle", 17, (16, 0.68, 0.95),
        r"Angle $= \frac{7}{16.5} \times 360° \approx 152.7°$",
        "M1, A1",
        topic_id=14)

    # P2 Q8 — Page 18 (idx 17)
    add_q(db, p2.id, exam_dir, 2, 8, None,
        r"A car travels the first 48 km of its journey at an average speed of 96 km/h. The car took 20 minutes to complete the remaining 15 km of its journey. Find the average speed of the car for its entire journey in km/h.",
        3, "Speed, Distance, Time", 18, (17, 0.04, 0.30),
        r"""Total distance $= 48 + 15 = 63$ km
Time for first part $= \frac{48}{96} = 0.5$ h
Total time $= \frac{1}{2} + \frac{1}{3} = \frac{5}{6}$ h
Average speed $= \frac{63}{\frac{5}{6}} = 75.6$ km/h""",
        "M1 for time, M1 for total, A1",
        topic_id=9)

    # P2 Q9 — Page 18 (idx 17)
    add_q(db, p2.id, exam_dir, 2, 9, "a",
        r"Find the equation of the straight line.",
        2, "Linear Functions — Equation", 18, (17, 0.30, 0.82),
        r"$y = -2x + 1$", "B1 for gradient, B1 for intercept",
        stem=r"The diagram shows a straight line $l$.",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 9, "b",
        r"On the graph above, draw the line $x = 2$.",
        1, "Linear Functions — Vertical Line", 18, (17, 0.82, 0.95),
        r"Vertical line through $x = 2$.", "B1",
        topic_id=6)

    # P2 Q10 — Page 19 (idx 18)
    add_q(db, p2.id, exam_dir, 2, 10, "ai",
        r"Find the area of region $EADCB$.",
        3, "Area — Composite Figure", 19, (18, 0.04, 0.50),
        r"""Area of semicircle $= \frac{\pi(2.1)^2}{2}$
Area of trapezium $= \frac{1}{2}(3.5)(4.2 + 5.6)$
Area $= \frac{\pi(2.1)^2}{2} + \frac{1}{2}(3.5)(4.2 + 5.6) = 13.85 + 17.15 = 31.0$ m$^2$ (3 s.f.)""",
        "M1 for semicircle, M1 for trapezium, A1",
        stem=r"A basketball court is shown. Region $EADCB$ is made up of a semicircle of radius 2.1 m with centre $O$, and a trapezium $ABCD$. All lengths in metres.",
        topic_id=12)

    add_q(db, p2.id, exam_dir, 2, 10, "aii",
        r"Find the perimeter of region $EADCB$.",
        3, "Perimeter — Composite Figure", 19, (18, 0.50, 0.95),
        r"""Semicircle arc $= \frac{2\pi(2.1)}{2} = 2.1\pi$
Perimeter $= 2.1\pi + 3.6 + 5.6 + 3.6 = 19.4$ m""",
        "M1 for semicircle arc, M1 for sides, A1",
        topic_id=12)

    # P2 Q11 — Page 20 (idx 19)
    add_q(db, p2.id, exam_dir, 2, 11, "a",
        r"Find the volume of the cylinder, leaving your answer to 2 decimal places.",
        2, "Volume — Cylinder", 20, (19, 0.04, 0.42),
        r"$V = \pi(8)^2(10) = 640\pi = 2010.62$ cm$^3$", "M1, A1",
        stem=r"Bella fills a cylinder completely with water. She then transfers all the water into a cuboid and the water level reaches a height $h$ cm. Cylinder: radius $= 8$ cm, height $= 10$ cm. Cuboid: $30$ cm $\times$ $8$ cm $\times$ $9$ cm.",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 11, "b",
        r"Find the value of $h$.",
        2, "Volume — Cuboid", 20, (19, 0.42, 0.62),
        r"$h = \frac{2010.62}{30 \times 8} = 8.38$ cm (3 s.f.)", "M1, A1",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 11, "c",
        r"Find the total surface area of the cuboid.",
        2, "Surface Area — Cuboid", 20, (19, 0.62, 0.95),
        r"TSA $= (2 \times 30 \times 8) + (30 + 30 + 8 + 8) \times 9 = 480 + 684 = 1164$ cm$^2$", "M1, A1",
        topic_id=13)

    # P2 Q12 — Pages 21-22 (idx 20-21)
    add_q(db, p2.id, exam_dir, 2, 12, "a",
        r"Plot the points from the table and join them with a straight line.",
        3, "Linear Functions — Graph", 21, (20, 0.04, 0.62),
        r"Correct axes (1m), correctly plotted points (1m), correct line drawn through plotted points (1m).", "M1 for axes, M1 for points, M1 for line",
        stem=r"Tammy pours out water from a jug into cups of equal volume. She records the volume of water remaining ($V$ ml) after $x$ cups are filled. Table: $x = 0, 5, 10, 15, 20$; $V = 5000, 4100, 3200, 2300, 1400$.",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 12, "b",
        r"Find the gradient of the line.",
        1, "Linear Functions — Gradient", 21, (20, 0.62, 0.80),
        r"Gradient $= \frac{4100 - 5000}{5 - 0} = -180$", "B1",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 12, "c",
        r"What is the volume of each cup?",
        1, "Linear Functions — Interpretation", 21, (20, 0.80, 0.92),
        r"$180$ ml", "A1",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 12, "di",
        r"From your graph, find the volume of water remaining in the jug after Tammy fills 16 cups.",
        1, "Linear Functions — Reading Graph", 22, (21, 0.04, 0.30),
        r"$V = 5000 - 180 \times 16 = 2120$ ml. From graph: $\approx 2100$ ml", "B1",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 12, "dii",
        r"From your graph, find the maximum number of full cups of water the jug can fill.",
        1, "Linear Functions — Reading Graph", 22, (21, 0.30, 0.55),
        r"$27$ (round down from $27.5$)", "B1",
        topic_id=6)

    db.commit()
    p1_count = len(p1.questions)
    p2_count = len(p2.questions)
    print(f"Seeded Outram exam id={exam.id}: Paper 1 ({p1_count} parts), Paper 2 ({p2_count} parts)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
