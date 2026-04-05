"""Seed the Northbrooks Secondary School Sec 1 Express EOY 2022 Math exam."""

import os
import shutil
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, Base, engine, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/66b1f5621f7f4_5781.pdf"

init_db()


def add_q(db, paper_id, exam_dir, paper_num, num, part, text, marks, topic,
          pdf_page, crop_region, answer_text, mark_scheme, stem=None, topic_id=None):
    """Insert a question with cropped image and its answer.

    crop_region: (page_0indexed, top_frac, bottom_frac)
    stem: shared question stem (only set on first part of a group)
    topic_id: curriculum topic ID (1-14)
    """
    # Generate cropped image
    part_suffix = part.replace("(", "").replace(")", "") if part else ""
    img_name = f"q{paper_num}_{num}{part_suffix}.png"
    img_path = os.path.join(exam_dir, img_name)
    pg, top, bot = crop_region
    crop_question_image(PDF_PATH, pg, top, bot, img_path)

    q = Question(
        paper_id=paper_id,
        question_number=num,
        part=part,
        stem=stem,
        question_text=text,
        marks=marks,
        topic=topic,
        topic_id=topic_id,
        page_image=img_name,
        pdf_page=pdf_page,
    )
    db.add(q)
    db.flush()
    a = Answer(question_id=q.id, answer_text=answer_text, mark_scheme=mark_scheme)
    db.add(a)
    return q


def main():
    db = SessionLocal()

    # Clear existing data
    from models import Answer as Ans, Question as Q, Paper as P, Exam as E, School as S
    db.query(Ans).delete()
    db.query(Q).delete()
    db.query(P).delete()
    db.query(E).delete()
    db.commit()

    school = db.query(S).filter(S.name == "Northbrooks Secondary School").first()
    if not school:
        school = S(name="Northbrooks Secondary School")
        db.add(school)
        db.flush()

    exam = Exam(
        school_id=school.id,
        title="End-of-Year Examination 2022",
        year=2022,
        level="Secondary 1 Express",
        subject="Mathematics",
        source_pdf="66b1f5621f7f4_5781.pdf",
        status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    src_dir = os.path.join(os.path.dirname(__file__), "images")
    os.makedirs(exam_dir, exist_ok=True)
    # Copy full page images too (for reference)
    copy_existing_images(src_dir, exam_dir)

    # ── Paper 1 ─────────────────────────────────────────────────

    p1 = Paper(
        exam_id=exam.id, paper_number=1, duration_minutes=75, total_marks=50,
        date=date(2022, 10, 3),
        instructions="Answer all the questions. If working is needed it must be shown with the answer.",
    )
    db.add(p1)
    db.flush()

    # NOTE: crop_region = (page_0indexed, top_frac, bottom_frac)
    # Using $ for inline math, $$ for display (standalone) equations

    # Q1 — Page 4 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 1, "a",
        r"Write down the maximum number of people that could be in the concert.",
        1, "Rounding / Approximation", 4, (3, 0.63, 0.80),
        r"$55\,499$", "B1",
        stem=r"The number of people in a concert is $55\,000$, correct to the nearest thousand.", topic_id=3)

    add_q(db, p1.id, exam_dir, 1, 1, "b",
        r"Write down the minimum number of people that could be in the concert.",
        1, "Rounding / Approximation", 5, (3, 0.78, 0.95),
        r"$54\,500$", "B1", topic_id=3)

    # Q2 — Page 5 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 2, "a",
        r"Write down the prime number(s).",
        1, "Number Sets", 5, (4, 0.12, 0.39),
        r"$5$ (since $\sqrt[3]{125} = 5$)", "B1",
        stem=r"Consider the following numbers: $\sqrt{5}$, $\pi$, $\sqrt[3]{125}$, $-0.5$, $\dfrac{\pi}{2}$, $\dfrac{22}{7}$, $\dfrac{3}{4}$.", topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 2, "b",
        r"Write down the irrational number(s).",
        1, "Number Sets", 5, (4, 0.37, 0.57),
        r"$\sqrt{5}$, $\pi$, $\dfrac{\pi}{2}$", "B1", topic_id=2)

    # Q3 — Page 5 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 3, "a",
        r"$-5$ ____ $4$",
        1, "Comparing Numbers", 5, (4, 0.55, 0.72),
        r"$<$", "B1",
        stem=r"Choose a symbol from $<$, $=$, $>$ to make a correct statement.", topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 3, "b",
        r"$\dfrac{2}{3}$ ____ $66\%$",
        1, "Comparing Numbers", 5, (4, 0.70, 0.83),
        r"$>$", "B1", topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 3, "c",
        r"$0.27$ ____ $\dfrac{3}{11}$",
        1, "Comparing Numbers", 5, (4, 0.81, 0.95),
        r"$=$ (since $\frac{3}{11} = 0.\overline{27}$)", "B1", topic_id=2)

    # Q4 — Pages 6-7 (idx 5-6) — no shared stem, each part is self-contained
    add_q(db, p1.id, exam_dir, 1, 4, "a",
        r"Express $588$ as a product of its prime factors.",
        1, "Prime Factorisation", 6, (5, 0.55, 0.73),
        r"$588 = 2^2 \times 3 \times 7^2$", "B1", topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 4, "b",
        r"Given that $504 = 2^3 \times 3^2 \times 7$, find the largest integer which is a factor of both $504$ and $588$.",
        1, "HCF", 6, (5, 0.71, 0.95),
        r"$\text{HCF} = 2^2 \times 3 \times 7 = 84$", "B1", topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 4, "c",
        r"Find the smallest positive integer $m$ such that $\sqrt{\dfrac{504}{m}}$ is a positive integer.",
        1, "Square Roots / Factors", 7, (6, 0.08, 0.28),
        r"$m = 14$", "B1", topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 4, "d",
        r"Find the smallest positive integer $n$ such that $504n$ is a multiple of $588$.",
        1, "LCM", 7, (6, 0.27, 0.51),
        r"$n = 7$", "B1", topic_id=1)

    # Q5 — Pages 7-8 (idx 6-7) — no shared stem
    add_q(db, p1.id, exam_dir, 1, 5, "a",
        r"Expand and simplify $2x - [5 - 3(7x - 1)]$.",
        3, "Algebra — Expansion", 7, (6, 0.50, 0.78),
        r"""$$2x - [5 - 3(7x - 1)]$$
$$= 2x - [5 - 21x + 3]$$
$$= 2x - [8 - 21x]$$
$$= 2x - 8 + 21x = 23x - 8$$""",
        "M1 for expanding inner bracket, M1 for removing square bracket, A1", topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 5, "b",
        r"Factorise $27a^2b - 9a$.",
        2, "Algebra — Factorisation", 7, (6, 0.76, 0.96),
        r"$9a(3ab - 1)$",
        "B1 for 9a, B1 for (3ab − 1)", topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 5, "c",
        r"Given that $3x + y = 2x + 5$, find the exact value of $\dfrac{x}{2y}$.",
        3, "Algebra — Substitution", 8, (7, 0.08, 0.49),
        r"""From $3x + y = 2x + 5y$: $x = 4y$
$$\frac{x}{2y} = \frac{4y}{2y} = 2$$""",
        "M1, M1, A1", topic_id=4)

    # Q6 — Pages 8-9 (idx 7-8)
    add_q(db, p1.id, exam_dir, 1, 6, "ai",
        r"Write in terms of $x$, the total cost of the milk tea.",
        1, "Linear Equations — Word Problem", 8, (7, 0.50, 0.75),
        r"$\$2.50x$", "B1",
        stem=r"Adrian bought 27 cups of drinks. Out of these, there were $x$ cups of milk tea that cost $\$2.50$ per cup and the rest were coffee which cost $\$3.00$ per cup. He spent a total of $\$75$.", topic_id=5)

    add_q(db, p1.id, exam_dir, 1, 6, "aii",
        r"Write in terms of $x$, the total cost of the coffee.",
        1, "Linear Equations — Word Problem", 8, (7, 0.74, 0.92),
        r"$3(27 - x)$ or $81 - 3x$", "B1", topic_id=5)

    add_q(db, p1.id, exam_dir, 1, 6, "b",
        r"By forming an equation in terms of $x$, find the number of cups of milk tea that Adrian bought.",
        3, "Linear Equations — Word Problem", 9, (8, 0.07, 0.47),
        r"""$$3(27 - x) + 2.5x = 75$$
$$81 - 3x + 2.5x = 75$$
$$-0.5x = -6 \implies x = 12$$""",
        "M1 for forming equation, M1 for simplifying, A1", topic_id=5)

    # Q7 — Pages 9-10 (idx 8-9)
    add_q(db, p1.id, exam_dir, 1, 7, "a",
        r"the profit earned in 2020.",
        2, "Percentage", 9, (8, 0.47, 0.76),
        r"$$\text{Profit}_{2020} = \frac{17\,600}{80} \times 100 = \$22\,000$$",
        "M1, A1",
        stem=r"A shopkeeper's profit in 2021 was $\$17{,}600$. This was a decrease of 20% from the profit earned in 2020. The profit earned in 2020 was an increase of 10% from the profit earned in 2019. Calculate:", topic_id=8)

    add_q(db, p1.id, exam_dir, 1, 7, "b",
        r"the profit earned in 2019.",
        2, "Percentage", 9, (8, 0.74, 0.95),
        r"$$\text{Profit}_{2019} = \frac{22\,000}{110} \times 100 = \$20\,000$$",
        "M1 ecf, A1", topic_id=8)

    add_q(db, p1.id, exam_dir, 1, 7, "c",
        r"the percentage decrease in the profit earned in 2021 as compared to 2019.",
        2, "Percentage", 10, (9, 0.07, 0.45),
        r"$$\%\text{ decrease} = \frac{20\,000 - 17\,600}{20\,000} \times 100\% = 12\%$$",
        "M1 ecf, A1", topic_id=8)

    # Q8 — Pages 10-11 (idx 9-10)
    add_q(db, p1.id, exam_dir, 1, 8, "a",
        r"Find the distance, in kilometres, between Town $X$ and Town $Y$.",
        1, "Speed, Distance, Time", 10, (9, 0.45, 0.74),
        r"$\text{Distance} = 16 \times 1.5 = 24$ km", "B1",
        stem=r"Alvin cycled at a speed of 16 km/h for 1 hour 30 minutes from Town $X$ to Town $Y$. He then stopped and rested for 45 minutes at Town $Y$. After that, he cycled from Town $Y$ to Town $X$ at 12 km/h.", topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 8, "b",
        r"Find the time taken for Alvin to cycle from Town $Y$ to Town $X$.",
        1, "Speed, Distance, Time", 10, (9, 0.73, 0.96),
        r"$\text{Time} = \frac{24}{12} = 2$ hours", "B1 ecf", topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 8, "c",
        r"Find the average speed of his entire journey.",
        3, "Speed, Distance, Time", 11, (10, 0.07, 0.40),
        r"$$\text{Average speed} = \frac{24 + 24}{1.5 + 0.75 + 2} = \frac{48}{4.25} = 11.3 \text{ km/h (3 s.f.)}$$",
        "M1 ecf for total distance and time, A1", topic_id=9)

    # Q9 — Page 12 (idx 11)
    add_q(db, p1.id, exam_dir, 1, 9, "a",
        r"Write down the coordinates of points $A$ and $B$.",
        2, "Coordinate Geometry", 12, (11, 0.07, 0.55),
        r"$A(-4,\, 0)$, $B(0,\, 2)$", "B1, B1",
        stem=r"The graph shows the line $2y = x + 4$. Points $A$ and $B$ lie on the line. Point $A$ lies on the $x$-axis and point $B$ lies on the $y$-axis.", topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 9, "b",
        r"Find the gradient of the line $2y = x + 4$.",
        1, "Coordinate Geometry", 12, (11, 0.53, 0.70),
        r"Gradient $= \frac{1}{2}$", "B1", topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 9, "c",
        r"$C$ is the point $(2,\, k)$. Point $C$ lies on the line $2y = x + 4$. Find the value of $k$.",
        2, "Coordinate Geometry", 12, (11, 0.67, 0.92),
        r"""$$2k = 2 + 4 = 6 \implies k = 3$$""",
        "M1, A1", topic_id=6)

    # Q10 — Page 13 (idx 12)
    add_q(db, p1.id, exam_dir, 1, 10, "a",
        r"Find the size of each exterior angle.",
        2, "Polygon Angles", 13, (12, 0.08, 0.55),
        r"$$\text{Exterior angle} = \frac{360°}{6} = 60°$$",
        "M1, A1",
        stem=r"The diagram below shows a regular polygon with 6 sides. One exterior angle is shown as $(2x + 40)°$.", topic_id=11)

    add_q(db, p1.id, exam_dir, 1, 10, "b",
        r"Find the value of $x$.",
        2, "Polygon Angles", 13, (12, 0.50, 0.87),
        r"""$$2x + 40 = 60 \implies 2x = 20 \implies x = 10$$""",
        "M1, A1", topic_id=11)

    # Q11 — Page 14 (idx 13)
    add_q(db, p1.id, exam_dir, 1, 11, "a",
        r"Calculate the area of the field.",
        3, "Area — Semicircle & Trapezium", 14, (13, 0.07, 0.59),
        r"""$$\text{Area} = \tfrac{1}{2}\pi(20)^2 + \tfrac{1}{2}(30 + 40)(25) = 200\pi + 875 \approx 1500 \text{ m}^2$$""",
        "M1 for semicircle area, M1 for trapezium area, A1",
        stem=r"The figure shows a field made up of a semicircle $ABC$ and a trapezium $ACDE$. $CA = 40$ m, $ED = 30$ m and the perpendicular height of the trapezium is 25 m. $AC$ is parallel to $DE$.", topic_id=12)

    add_q(db, p1.id, exam_dir, 1, 11, "b",
        r"If it costs $\$2.10$ per 1 $\text{m}^2$ of grass, find the cost of planting grass on the whole field. Give your answer correct to the nearest dollar.",
        3, "Area — Cost Calculation", 14, (13, 0.56, 0.87),
        r"$$1503.318\ldots \times 2.10 = \$3156.97\ldots \approx \$3157$$",
        "M1 for using unrounded area, M1 for cost, A1", topic_id=12)

    # ── Paper 2 ─────────────────────────────────────────────────

    p2 = Paper(
        exam_id=exam.id, paper_number=2, duration_minutes=75, total_marks=50,
        date=date(2022, 9, 30),
        instructions="Answer all the questions. If the answer is not exact, give the answer to three significant figures.",
    )
    db.add(p2)
    db.flush()

    # Q1 — Page 16 (idx 15)
    add_q(db, p2.id, exam_dir, 2, 1, "a",
        r"Calculate $\sqrt{\dfrac{-2.56 + 7.01 \times 3.45 - (-3)^2}{200.1^2}}$. Write down the first 6 digits shown on your calculator.",
        1, "Calculator Usage", 16, (15, 0.09, 0.28),
        r"$0.01175$", "B1", topic_id=3)

    add_q(db, p2.id, exam_dir, 2, 1, "b",
        r"Round off your answer to part (a) correct to two significant figures.",
        1, "Significant Figures", 16, (15, 0.25, 0.37),
        r"$0.012$", "B1", topic_id=3)

    # Q2 — Page 16 (idx 15) — no shared stem, each part independent
    add_q(db, p2.id, exam_dir, 2, 2, "a",
        r"By rounding each number correct to 1 significant figure, estimate $\dfrac{5.04 \times 19.86}{4.97}$.",
        1, "Estimation", 16, (15, 0.36, 0.57),
        r"$$\approx \frac{5 \times 20}{5} = 20$$", "B1", topic_id=3)

    add_q(db, p2.id, exam_dir, 2, 2, "b",
        r"Without using a calculator, estimate $\dfrac{\sqrt{50.4} \times \sqrt{101.5}}{\sqrt{4.1}}$.",
        2, "Surds / Estimation", 16, (15, 0.57, 0.90),
        r"$$\approx \frac{\sqrt{49} \times \sqrt{100}}{\sqrt{4}} = \frac{7 \times 10}{2} = 35$$",
        "M1, A1", topic_id=3)

    # Q3 — Page 17 (idx 16)
    add_q(db, p2.id, exam_dir, 2, 3, "a",
        r"the price of diesel per litre.",
        2, "Rate", 17, (16, 0.07, 0.38),
        r"$$\frac{43.75}{35} = 1.25 \text{ per litre}$$", "M1, A1",
        stem=r"A van travelled 322,000 m on 35 litres of diesel. The total price of the diesel used was $\$43.75$. Calculate:", topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 3, "b",
        r"the rate of diesel consumption in km per litre.",
        2, "Rate", 17, (16, 0.36, 0.63),
        r"$$\frac{322\text{ km}}{35} = 9.2 \text{ km per litre}$$", "M1, A1", topic_id=9)

    # Q4 — Page 17 (idx 16) — flat, no parts
    add_q(db, p2.id, exam_dir, 2, 4, None,
        r"If $k = \sqrt{\dfrac{2m}{q}} - n$, find the value of $k$ when $n = -3$, $q = -1$ and $m = -8$.",
        2, "Formula Substitution", 17, (16, 0.63, 0.95),
        r"$$k = \sqrt{\frac{2(-8)}{-1}} - (-3) = \sqrt{16} + 3 = 7$$", "M1, A1", topic_id=4)

    # Q5 — Page 18 (idx 17)
    add_q(db, p2.id, exam_dir, 2, 5, "a",
        r"$\dfrac{3x+1}{5} - \dfrac{x-2}{3}$",
        2, "Algebraic Fractions", 18, (17, 0.07, 0.47),
        r"$$\frac{3(3x+1) - 5(x-2)}{15} = \frac{4x + 13}{15}$$", "M1, A1",
        stem=r"Express the following expressions as a single fraction.", topic_id=4)

    add_q(db, p2.id, exam_dir, 2, 5, "b",
        r"$1 + \dfrac{2x - 4}{3}$",
        2, "Algebraic Fractions", 18, (17, 0.46, 0.92),
        r"$$\frac{3 + 2x - 4}{3} = \frac{2x - 1}{3}$$", "M1, A1", topic_id=4)

    # Q6 — Page 19 (idx 18)
    add_q(db, p2.id, exam_dir, 2, 6, "a",
        r"$7k + 11 = 12 - 3k$",
        2, "Solving Linear Equations", 19, (18, 0.07, 0.40),
        r"$$10k = 1 \implies k = \frac{1}{10}$$", "M1, A1",
        stem=r"Solve the following equations.", topic_id=5)

    add_q(db, p2.id, exam_dir, 2, 6, "b",
        r"$7 - m = \dfrac{-3m + 4}{5}$",
        3, "Solving Linear Equations", 19, (18, 0.38, 0.92),
        r"""$$5(7 - m) = -3m + 4$$
$$35 - 5m = -3m + 4$$
$$-2m = -31 \implies m = 15.5$$""",
        "M1, M1, A1", topic_id=5)

    # Q7 — Page 20 (idx 19)
    add_q(db, p2.id, exam_dir, 2, 7, "a",
        r"angle $BHF$.",
        2, "Angle Properties — Parallel Lines", 20, (19, 0.07, 0.63),
        r"""$\angle EGF = 30°$ (alternate angles)
$\angle BHF = 30° + 50° = 80°$ (exterior angle of triangle)""",
        "M1, A1",
        stem=r"In the figure, $AC$ is parallel to $GI$ and $HD$. $AF$ is parallel to $CD$ and $BG$ is parallel to $DE$. Angles of $30°$ and $50°$ are marked. Stating your reasons clearly, find:", topic_id=10)

    add_q(db, p2.id, exam_dir, 2, 7, "b",
        r"angle $CDE$.",
        3, "Angle Properties — Parallel Lines", 20, (19, 0.61, 0.92),
        r"""$\angle BAF = 50°$ (alt. angles, $AB \parallel GF$)
$\angle CDH = 50°$ (opp. angles of parallelogram)
$\angle EDH = 30°$ (alt. angles)
$\angle CDE = 50° + 30° = 80°$""",
        "M1, M1, A1", topic_id=10)

    # Q8 — Page 21 (idx 20) — flat, no parts
    add_q(db, p2.id, exam_dir, 2, 8, None,
        r"The ratio of Lionel's expenditure on food to his expenditure on clothes is $5 : 7$. The ratio of his expenditure on food to his expenditure on transport is $3 : 2$. He spends $\$132$ more on clothes than on transport. Find Lionel's total expenditure.",
        3, "Ratio", 21, (20, 0.07, 0.70),
        r"""$F : C : T = 15 : 21 : 10$
$21 - 10 = 11$ parts $= 132$, so $1$ part $= 12$
Total $= 46 \times 12 = 552$""",
        "M1, M1, A1", topic_id=9)

    # Q9 — Page 22 (idx 21)
    add_q(db, p2.id, exam_dir, 2, 9, "a",
        r"Complete the table for Figures 4 and 5.",
        2, "Number Patterns", 22, (21, 0.07, 0.39),
        r"Figure 4: $11$, Figure 5: $13$", "B1, B1",
        stem=r"The diagram below shows a sequence formed using diamonds. Figure 1 has 5 diamonds, Figure 2 has 7, Figure 3 has 9.", topic_id=7)

    add_q(db, p2.id, exam_dir, 2, 9, "b",
        r"Write down an expression, in terms of $n$, for the number of diamonds in Figure $n$.",
        1, "Number Patterns", 22, (21, 0.37, 0.56),
        r"$2n + 3$", "B1", topic_id=7)

    add_q(db, p2.id, exam_dir, 2, 9, "c",
        r"Find the number of diamonds in Figure 80.",
        1, "Number Patterns", 22, (21, 0.54, 0.69),
        r"$2(80) + 3 = 163$", "B1", topic_id=7)

    add_q(db, p2.id, exam_dir, 2, 9, "d",
        r"Is it possible for a figure to have 100 diamonds? Explain your answer.",
        2, "Number Patterns", 22, (21, 0.68, 0.92),
        r"""$2n + 3 = 100 \implies 2n = 97 \implies n = 48.5$
Since $n$ is not a positive integer, it is impossible.""",
        "M1, A1", topic_id=7)

    # Q10 — Page 23 (idx 22)
    add_q(db, p2.id, exam_dir, 2, 10, "a",
        r"Complete the table: when $x = -1, 0, 1$.",
        2, "Linear Graphs", 23, (22, 0.07, 0.22),
        r"$x = -1$: $y = 5$; $x = 0$: $y = 2$; $x = 1$: $y = -1$", "B1, B1",
        stem=r"$x$ and $y$ are related by the equation $y = 2 - 3x$.", topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 10, "b",
        r"Draw the graph of $y$ against $x$ in the grid.",
        3, "Linear Graphs", 23, (22, 0.22, 0.73),
        r"Straight line through $(-1, 5)$, $(0, 2)$, $(1, -1)$.",
        "B2 for all 3 points, B1 for straight line", topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 10, "c",
        r"State the gradient and $y$-intercept of the graph $y = 2 - 3x$.",
        2, "Linear Graphs", 23, (22, 0.72, 0.83),
        r"Gradient $= -3$, $y$-intercept $= 2$", "B1, B1", topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 10, "d",
        r"From the graph, write down the value of $x$ when $y = -4$.",
        1, "Linear Graphs", 23, (22, 0.82, 0.95),
        r"$x = 2$", "B1 (dotted lines required)", topic_id=6)

    # Q11 — Page 24 (idx 23)
    add_q(db, p2.id, exam_dir, 2, 11, "a",
        r"Construct triangle $PQR$ where $QR = 10.5$ cm and $PR = 8$ cm.",
        2, "Construction", 24, (23, 0.07, 0.57),
        r"Triangle constructed with compass arcs. $QR = 10.5$ cm, $PR = 8$ cm.",
        "B1 for QR with construction, B1 for PR with construction",
        stem=r"$PQR$ is a triangle. The side $PQ$ has already been drawn in the space below.", topic_id=10)

    add_q(db, p2.id, exam_dir, 2, 11, "b",
        r"Measure angle $QPR$.",
        1, "Construction", 24, (23, 0.55, 0.65),
        r"$\angle QPR \approx 92°$", "B1", topic_id=10)

    # Q12 — Page 25 (idx 24)
    add_q(db, p2.id, exam_dir, 2, 12, "a",
        r"Calculate the volume of the water.",
        2, "Volume — Cylinder", 25, (24, 0.07, 0.52),
        r"$$V = \pi(8)^2(12) = 768\pi \approx 2410 \text{ cm}^3 \text{ (3 s.f.)}$$",
        "M1, A1",
        stem=r"A cylindrical container of height 25 cm and radius 8 cm contains water to a depth of 12 cm.", topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 12, "b",
        r"Solid metal cubes of length 3 cm are fully submerged in the water. Find the maximum number of metal cubes that can be submerged so that the water will not flow out of the container.",
        3, "Volume — Cylinder & Cube", 25, (24, 0.49, 0.95),
        r"""Empty space $= \pi(8)^2(13) = 832\pi \approx 2613.8$ cm$^3$
Volume of 1 cube $= 3^3 = 27$ cm$^3$
$\frac{2613.8}{27} = 96.8$ → Maximum $= 96$ cubes""",
        "M1 for empty space volume, M1 for cube volume, A1", topic_id=13)

    db.commit()
    p1_count = len(p1.questions)
    p2_count = len(p2.questions)
    print(f"Seeded exam id={exam.id}: Paper 1 ({p1_count} parts), Paper 2 ({p2_count} parts)")
    print(f"Cropped images saved to {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
