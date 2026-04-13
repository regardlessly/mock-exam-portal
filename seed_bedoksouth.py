"""Seed Bedok South Secondary School EOY 2023 Sec 1 Express Math exam."""

import os
import shutil
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/Bedok-South-Secondary-EOY-2023-Sec-1-Math-Group-3.pdf"
IMAGES_DIR = "/tmp/bedoksouth_pages"

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

    school = db.query(School).filter(School.name == "Bedok South Secondary School").first()
    if not school:
        school = School(name="Bedok South Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(Exam.school_id == school.id, Exam.year == 2023).first()
    if existing:
        print(f"Bedok South 2023 already seeded (id={existing.id}). Deleting and re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id, title="End-of-Year Examination 2023", year=2023,
        level="Secondary 1 Express", subject="Mathematics",
        source_pdf="Bedok-South-Secondary-EOY-2023-Sec-1-Math-Group-3.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # PAPER 1 — Pages 2-8 (idx 1-7), 40 marks, 1 hour
    # No calculator allowed
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=60, total_marks=40,
               date=date(2023, 10, 10), instructions="Answer all questions.")
    db.add(p1); db.flush()

    # Q1 — Page 2 (idx 1)
    # Given a set of numbers: 5/2, sqrt(-2), pi, 1.2222, -5.6
    add_q(db, p1.id, exam_dir, 1, 1, "a",
        r"List all the real numbers.",
        1, "Number Classification", 2, (1, 0.05, 0.22),
        r"$\frac{5}{2}$, $\pi$, $1.2222$, $-5.6$", "B1 — award only when all are written",
        stem=r"Given a set of numbers, $\frac{5}{2}$, $\sqrt{-2}$, $\pi$, $1.2222$, $-5.6$, list all the:",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 1, "b",
        r"List all the irrational number(s).",
        1, "Number Classification", 2, (1, 0.22, 0.36),
        r"$\pi$", "B1",
        topic_id=2)

    # Q2 — Page 2 (idx 1)
    # Number line with a, b, c
    add_q(db, p1.id, exam_dir, 1, 2, "a",
        r"Determine whether $\dfrac{a}{b}$ is positive or negative. Explain your answer in words.",
        1, "Number Properties", 2, (1, 0.36, 0.66),
        r"A negative integer, because $a$ is negative but $b$ is positive. A negative number divided by a positive number gives a negative value.", "B1",
        stem=r"Observe the following numbers $a$, $b$ and $c$ on the number line below. Determine whether the following expressions are positive or negative. Explain your answer in words.",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 2, "b",
        r"Determine whether $\dfrac{a^2}{\sqrt{c}}$ is positive or negative. Explain your answer in words.",
        2, "Number Properties", 2, (1, 0.66, 0.82),
        r"A positive integer. $a$ is negative but when it is squared, $a^2$ becomes positive. $c$ is positive and when square rooted, is still positive. So positive divided by positive gives a positive integer.", "B1, B2",
        topic_id=2)

    # Q3 — Page 2 (idx 1)
    add_q(db, p1.id, exam_dir, 1, 3, None,
        r"Evaluate $\dfrac{5}{8} \times \left(-1\dfrac{1}{5}\right) \div \left(-\dfrac{5}{6}\right)$ without using calculator.",
        3, "Order of Operations", 2, (1, 0.82, 0.97),
        r"""$$\frac{5}{8} \times \left(-\frac{6}{5}\right) \times \left(-\frac{6}{5}\right)$$
$$= \frac{5}{8} \times \frac{9}{1} = \frac{45}{8} = 5\frac{5}{8}$$
Award B1 if answer is given without working.""",
        "M1, M1, A1",
        topic_id=2)

    # Q4 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 4, "a",
        r"Find the square of $7^6 \times 19^3$. Leave your answer in index notation.",
        1, "Indices", 3, (2, 0.04, 0.26),
        r"$(7^6 \times 19^3)^2 = 7^{12} \times 19^6$", "B1",
        stem=r"Find:",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 4, "b",
        r"Find the cube root of the answer in (a). Leave your answer in index notation.",
        1, "Indices", 3, (2, 0.26, 0.38),
        r"$\sqrt[3]{7^{12} \times 19^6} = 7^4 \times 19^2$", "B1",
        topic_id=1)

    # Q5 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 5, "a",
        r"Simplify $\dfrac{5(3n - 4.5)}{3} - \dfrac{-(2n + 9)}{2}$.",
        3, "Algebra — Simplification", 3, (2, 0.38, 0.68),
        r"""$$= \frac{10(3n - 4.5) + 3(2n + 9)}{6}$$
$$= \frac{30n - 45 + 6n + 27}{6} = \frac{36n - 18}{6} = 6n - 3$$""",
        "B1 either step, M1, M1, A1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 5, "b",
        r"Hence show that $\dfrac{5(3n - 4.5)}{3} - \dfrac{-(2n + 9)}{2}$ is a multiple of 3 for all positive integers $n$.",
        1, "Algebra — Proof", 3, (2, 0.68, 0.95),
        r"$6n - 3 = 3(2n - 1)$, which is a multiple of 3 for all positive integers $n$.", "B1",
        topic_id=4)

    # Q6 — Page 4 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 6, "a",
        r"Identify the steps where the errors occur and show the correct working below.",
        3, "Linear Equations — Error Analysis", 4, (3, 0.04, 0.70),
        r"""Step 3: $3(x + 1) + 2(x - a) = 6$ (sign error corrected)
Step 4: $3x + 3 + 2x - 2a = 6$ (expansion corrected)
Step 5: $5x = 3 + 2a$ (rearranged)
Step 6: $x = \frac{3 + 2a}{5}$""",
        "M1 for Step 3, M1 for Step 4/5, A1",
        stem=r"A student solved the following equation to find the value of $x$, where $a$ is a constant: $\frac{x+1}{2} - \frac{x-a}{3} = 1$.",
        topic_id=5)

    add_q(db, p1.id, exam_dir, 1, 6, "b",
        r"If the solution of the equation is $x = 2$, find the value of $a$.",
        1, "Linear Equations — Substitution", 4, (3, 0.70, 0.95),
        r"""$2 = \frac{3 + 2a}{5}$
$10 = 3 + 2a$
$a = 3.5$""",
        "M1 ref, A1 — award B1 only if answer obtained without working",
        topic_id=5)

    # Q7 — Page 5 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 7, "a",
        r"Find his average speed for the journey.",
        1, "Speed, Distance, Time", 5, (4, 0.04, 0.32),
        r"Average speed $= \frac{360}{4} = 90$ km/h", "A1 — penalise unit (U) one time for entire qns",
        stem=r"Singapore and Melaka, Malaysia are 360 km apart. A man took 2 hours to drive to a rest stop and took a 30-min break. He then took another $1\frac{1}{2}$ hours to reach Melaka. He used up 20 litres of petrol for the journey.",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 7, "b",
        r"Find the petrol consumption rate in km/$l$.",
        1, "Speed, Distance, Time", 5, (4, 0.32, 0.42),
        r"Petrol consumption $= \frac{360}{20} = 18$ km/$l$", "A1",
        topic_id=9)

    # Q8 — Page 5 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 8, "a",
        r"Write down an expression for Mrs Tan's monthly salary in terms of $x$.",
        1, "Algebra — Expression", 5, (4, 0.42, 0.72),
        r"Mrs Tan: $\$(600 + 3x)$", "B1",
        stem=r"Mr Tan's monthly salary is $\$3x$. Mrs Tan's monthly salary is $\$600$ more than Mr Tan's. Their son's monthly salary is two-thirds of Mrs Tan's.",
        topic_id=5)

    add_q(db, p1.id, exam_dir, 1, 8, "b",
        r"Express their son's monthly salary in terms of $x$.",
        1, "Algebra — Expression", 5, (4, 0.72, 0.82),
        r"Son: $\frac{2}{3}(600 + 3x)$ or $(400 + 2x)$", "B1",
        topic_id=5)

    add_q(db, p1.id, exam_dir, 1, 8, "c",
        r"If the sum of their monthly salaries is $\$10600$, find the monthly salary of Mr Tan.",
        2, "Linear Equations — Word Problem", 5, (4, 0.82, 0.97),
        r"""$$3x + 600 + 3x + \frac{2}{3}(600 + 3x) = 10600$$
$$6x + 600 + 400 + 2x = 10600$$
$$8x = 9600$$
$$x = 1200$$
Mr Tan earns $\$3600$""",
        "ecf considered, M1, A1 — penalise unit (U) one time for entire qns, penalise presentation (P) if not using whole equation to solve",
        topic_id=5)

    # Q9 — Page 6 (idx 5)
    add_q(db, p1.id, exam_dir, 1, 9, "a",
        r"Express the following as a single fraction in its simplest form: $\dfrac{3(t - 1)}{2} + \dfrac{5(t + 3)}{3}$.",
        3, "Algebraic Fractions", 6, (5, 0.04, 0.38),
        r"""$$= \frac{9(t - 1) + 10(t + 3)}{6}$$
$$= \frac{9t - 9 + 10t + 30}{6} = \frac{19t + 21}{6}$$""",
        "M1, M1, A1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 9, "bi",
        r"Factorise $3ax - 6ay + 21a$.",
        1, "Factorisation", 6, (5, 0.38, 0.62),
        r"$3a(x - 2y + 7)$", "B1",
        stem=r"Factorise the following expressions completely. Simplify the expression first if necessary.",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 9, "bii",
        r"Factorise $6(kt - 3d) - 2(2kt - 6d)$.",
        2, "Factorisation", 6, (5, 0.62, 0.95),
        r"""$$= 6(kt - 3d) - 4(kt - 3d) = 2(kt - 3d)$$""",
        "M1, A1",
        topic_id=4)

    # Q10 — Page 7 (idx 6)
    add_q(db, p1.id, exam_dir, 1, 10, None,
        r"In the diagram, $AB \parallel CD \parallel EF$ and $\angle DCF = 35°$. Find the values of $a$ and $b$. Write the mathematical statements clearly.",
        3, "Angle Properties — Parallel Lines", 7, (6, 0.04, 0.42),
        r"""$\angle DCF = \angle EFC = 35°$ (alt. $\angle$s, $EF \parallel CD$)
$\angle EFA = \angle FAB = 70°$ (alt. $\angle$s, $EF \parallel AB$)
$(a + 5b) = 70$
$35 + 5b = 70$
$5b = 35$
$b = 7$, $a = 35$""",
        "B1 penalise presentation (P) for missing maths property in entire qns, M1, A1",
        topic_id=10)

    # Q11 — Page 7 (idx 6)
    add_q(db, p1.id, exam_dir, 1, 11, "a",
        r"Find the value of $a$.",
        2, "Angle Properties — Parallelogram", 7, (6, 0.42, 0.80),
        r"""$\angle ABE = 110°$ (opp. angles of parallelogram)
$5a = (180 - 110) \div 2 = 35$ (base $\angle$s of isos. $\triangle$)
$a = 7$""",
        "M1, A1",
        stem=r"The diagram shows a parallelogram $ABCD$. Points $E$ and $F$ lie on $BC$ and $AD$ respectively such that $CF \parallel EA$, $BA = BE$, $\angle ADC = 110°$ and $\angle AEB = 5a°$.",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 11, "b",
        r"Is $ABCF$ a trapezium? Explain with reasons.",
        1, "Properties of Quadrilaterals", 7, (6, 0.80, 0.97),
        r"$ABCF$ is a trapezium because there is one pair of parallel lines $AF \parallel BC$ only in the quadrilateral.", "B1",
        topic_id=10)

    # Q12 — Page 8 (idx 7)
    add_q(db, p1.id, exam_dir, 1, 12, "a",
        r"The points $(0, a)$ and $(b, 0)$ lie on the graph. Use the graph to find the values of $a$ and $b$.",
        2, "Linear Functions — Reading Graph", 8, (7, 0.04, 0.52),
        r"$a = -3$, $b = 1$", "B1, B1",
        stem=r"The diagram shows the graph of a function $y$ against $x$.",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 12, "b",
        r"Write down the equation of the graph in the form of $y = mx + c$.",
        2, "Linear Functions — Equation", 8, (7, 0.52, 0.72),
        r"""Gradient $= \frac{0 - (-3)}{1 - 0} = 3$
$y$-intercept $= -3$
$y = 3x - 3$""",
        "M1, A1",
        topic_id=6)

    # ══════════════════════════════════════════════
    # PAPER 2 — Pages 10-20 (idx 9-19), 60 marks, 1h30m
    # Calculator allowed
    # ══════════════════════════════════════════════
    p2 = Paper(exam_id=exam.id, paper_number=2, duration_minutes=90, total_marks=60,
               date=date(2023, 10, 3), instructions="Answer all questions.")
    db.add(p2); db.flush()

    # P2 Q1 — Page 10 (idx 9)
    add_q(db, p2.id, exam_dir, 2, 1, "ai",
        r"Simplify $a : b = \frac{1}{5} : 2\frac{1}{2}$.",
        1, "Ratio", 10, (9, 0.05, 0.18),
        r"$a : b = \frac{1}{5} : \frac{5}{2} = 2 : 25$ (multiply by 10 or $\times 5$)", "B1",
        stem=r"Simplify each of the following ratios.",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 1, "aii",
        r"Simplify $b : c = 0.70 : 0.350$.",
        1, "Ratio", 10, (9, 0.18, 0.24),
        r"$b : c = 0.70 : 0.350 = 700 : 350 = 2 : 1$", "B1",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 1, "b",
        r"Hence find the ratio $a : b : c$.",
        1, "Ratio", 10, (9, 0.24, 0.36),
        r"""Make $b$ common: $a : b = 2 : 25$, $b : c = 2 : 1$ ($\times 3$, actually need common b).
$a : b = 2 : 25$; $b : c = 2 : 1$. Common $b$: not directly possible without scaling.
Correct: $a : b : c = 1 : 6 : 3$ (ecf)""",
        "ecf, B1",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 1, "c",
        r"Al, Bo and Kat share $\$590$ in the ratio $7 : 12 : 40$. Find Al's share of the money.",
        2, "Ratio — Sharing", 10, (9, 0.36, 0.50),
        r"""$59$ units $= \$590$
$1$ unit $= \frac{590}{59}$
Al $= 7$ units $= \frac{590}{59} \times 7 = \$70$""",
        "M1, A1",
        topic_id=9)

    # P2 Q2 — Page 11 (idx 10)
    add_q(db, p2.id, exam_dir, 2, 2, "a",
        r"Estimate the total mass of the five boxes by rounding off each mass to one significant figure.",
        2, "Estimation / Rounding", 11, (10, 0.04, 0.26),
        r"""$76.8 \approx 80$, $81.4 \approx 80$, $75.3 \approx 80$, $81.8 \approx 80$, $86.4 \approx 90$
Total $= 80 + 80 + 80 + 80 + 90 = 410$ kg""",
        "M1, A1",
        stem=r"The maximum load of a cargo lift is 400 kg. There are five boxes whose masses in kg are 76.8, 81.4, 75.3, 81.8 and 86.4.",
        topic_id=3)

    add_q(db, p2.id, exam_dir, 2, 2, "b",
        r"Based on the estimation in (a) and the maximum load of the lift, is it safe to transport all these boxes at the same time?",
        1, "Estimation — Reasoning", 11, (10, 0.26, 0.42),
        r"It exceeded the maximum load, so it won't be safe to transport all together.", "B1",
        topic_id=3)

    add_q(db, p2.id, exam_dir, 2, 2, "c",
        r"Verify your answer in (b) by calculating the actual total mass of all five boxes. Explain if your estimation in (a) was a good and credible method. If not, how can it be improved?",
        2, "Estimation — Evaluation", 11, (10, 0.42, 0.62),
        r"""Total $= 76.8 + 81.4 + 75.3 + 81.8 + 86.4 = 401.7$ kg
Exceeds the maximum limit by a bit.
It's a suitable method as the results is still exceeding. Or: The difference is big between actual and estimated so better to round off to 2 significant figures or nearest whole number instead, more accurate.""",
        "A1, B1",
        topic_id=3)

    # P2 Q3 — Page 12 (idx 11)
    add_q(db, p2.id, exam_dir, 2, 3, "a",
        r"By forming an equation in $n$, solve and show that $n = 7$.",
        3, "Linear Equations — Word Problem", 12, (11, 0.04, 0.32),
        r"""$1.6n + 0.8 = 0.7(n + 10) + 0.1$
$1.6n + 0.8 = 0.7n + 7 + 0.1$
$1.6n - 0.7n = 7.1 - 0.8$
$0.9n = 6.3$
$n = \frac{6.3}{0.9} = 7$ (shown)""",
        "M1 for equation, M1, A1",
        stem=r"Mrs Tan has some money to buy fruits. She can buy $n$ mangoes at $\$1.60$ each and have 80 cents left. Alternatively, she can buy $(n + 10)$ apples at $\$0.70$ each and have 10 cents left.",
        topic_id=5)

    add_q(db, p2.id, exam_dir, 2, 3, "b",
        r"How much money does Mrs Tan have for buying fruits?",
        1, "Linear Equations", 12, (11, 0.32, 0.42),
        r"Money $= 1.6(7) + 0.8 = \$12$", "A1",
        topic_id=5)

    add_q(db, p2.id, exam_dir, 2, 3, "c",
        r"If Mrs Tan buys 3 mangoes and uses the rest of the money to buy apples, how many apples can she buy?",
        2, "Linear Equations — Word Problem", 12, (11, 0.42, 0.58),
        r"""Apples amount $= 12 - (3 \times 1.6) = 7.2$
Apples $= \frac{7.2}{0.7} = 10.3 = 10$ apples""",
        "M1 ecf, A1 ecf",
        topic_id=5)

    # P2 Q4 — Page 13 (idx 12)
    add_q(db, p2.id, exam_dir, 2, 4, "a",
        r"Which stall sold the greatest number of glasses of drinks? How many glasses were sold?",
        1, "Percentage — Comparison", 13, (12, 0.04, 0.30),
        r"Stall B $= 0.85 \times 220 = 187$ glasses (answer)", "M1 or B1",
        stem=r"At a food centre, there are three drink stalls. On a certain day, Stall A sold 175 glasses out of 200 glasses of iced milo, Stall B sold 85% of its 220 glasses of iced milo and Stall C sold 180 glasses of iced milo which was 80% of its total number of glasses of iced milo.",
        topic_id=8)

    add_q(db, p2.id, exam_dir, 2, 4, "b",
        r"Which stall sold the highest percentage of its glasses of drinks? What was its percentage?",
        1, "Percentage — Comparison", 13, (12, 0.30, 0.44),
        r"Stall A $= \frac{175}{200} \times 100\% = 87.5\%$ (answer)", "M1/A1/B1",
        topic_id=8)

    add_q(db, p2.id, exam_dir, 2, 4, "c",
        r"Which stall prepared the most glasses of drinks? What was its number?",
        1, "Percentage — Reverse", 13, (12, 0.44, 0.58),
        r"Stall C $= \frac{180}{0.80} \times 100 = 225$ glasses (answer)", "M1/A1/B1",
        topic_id=8)

    # P2 Q5 — Page 14 (idx 13)
    add_q(db, p2.id, exam_dir, 2, 5, "a",
        r"In this kite, $WY = WZ$, $XY = XZ$ and $WY$ bisects $\angle XWZ$. Find the values of $x$ and $y$.",
        3, "Angle Properties — Kite", 14, (13, 0.04, 0.38),
        r"""Equation: $5y = 2y + 30$
$3y = 30$, $y = 10$
$x + 6 = 3(x - 2)$ (properties of kite)
$x + 6 = 3x - 6$
$-2x = -12$, $x = 6$""",
        "M1, M1, A1",
        topic_id=10)

    add_q(db, p2.id, exam_dir, 2, 5, "b",
        r"In the diagram, a cross-section of a camera is shown. All measurements are in centimetres. Find the area of the shaded region in square centimetres. Take $\pi = 3.142$.",
        3, "Area — Composite Shape", 14, (13, 0.38, 0.95),
        r"""Area of rectangle $= 15 \times 20 = 300$
Area of trapezium $= \frac{1}{2}(2)(6 + 9) = 15$
Area of circle not shaded $= \pi(4.5)^2 = 63.6255$
Shaded region $= 300 + 15 - 63.6255 = 251.37 \approx 251$ cm$^2$ (3 s.f.)""",
        "M1 either area of rect/trapezium, M1 circle, A1 ecf — max 2 m only if any areas are wrong",
        topic_id=12)

    # P2 Q6 — Page 15 (idx 14)
    add_q(db, p2.id, exam_dir, 2, 6, "a",
        r"Taking $\pi = 3.142$, find the volume of the bolt.",
        3, "Volume — Prism + Cylinder", 15, (14, 0.04, 0.46),
        r"""Head volume $= \text{base area} \times \text{height} = 10.4 \times 0.5 = 5.2$ cm$^3$
Cylinder volume $= \pi r^2 \times l = 3.142 \times 1^2 \times 5 = 15.71$ cm$^3$
Total volume $= 5.2 + 15.71 = 20.91 \approx 20.9$ cm$^3$""",
        "M1, M1, M1/A1 — final answer award max 2 m for any wrong area",
        stem=r"The diagram shows a bolt which has a hexagonal head and a cylindrical body. The hexagonal head is a prism of base area 10.4 cm$^2$ and thickness of 0.5 cm. The length of each side of the hexagon is 2 cm. The cylindrical body has a diameter of 2 cm and a length of 5 cm.",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 6, "b",
        r"Find the total surface area of the bolt.",
        5, "Surface Area — Composite", 15, (14, 0.46, 0.95),
        r"""Surface area of bolt (minus ring/circle):
$= \text{base area} + (\text{base area} - \pi r^2) + 6 \text{ sides}$
$= 10.4 + (10.4 - 3.142 \times 1^2 \times 1) + 6(2 \times 0.5)$
$= 10.4 + 7.258 + 6 = 23.658$ cm$^2$

Surface area of cylinder (minus one base area covered by head):
$= 1 \text{ base area} + \text{curved lateral face}$
$= \pi r^2 + 2\pi r \times l = (3.142 \times 1^2) + (2 \times 3.142 \times 1 \times 5)$
$= 3.142 + 31.42 = 34.562$ cm$^2$

Total surface area $= 23.658 + 34.562 = 58.22 \approx 58.2$ (3 s.f.) cm$^2$""",
        "M1 = curved lateral face, M1 = 6 sides, M1 = 2 base areas, M1 = sum total no. of side faces, A1 final answer — max 4 m",
        topic_id=13)

    # P2 Q7 — Page 16 (idx 15)
    add_q(db, p2.id, exam_dir, 2, 7, "a",
        r"Find $\angle CBP$.",
        2, "Polygon Angles — Hexagon/Octagon", 16, (15, 0.04, 0.36),
        r"""$\angle CBA = \frac{(6 - 2) \times 180}{6} = 120°$ (interior angle of regular hexagon)
$\angle PBA = \frac{(8 - 2) \times 180}{8} = 135°$ (interior angle of regular octagon)
$\angle CBP = 360° - 120° - 135° = 105°$ (angles at a point)""",
        "M1, A1 — penalise presentation (P) for missing maths property in entire qns",
        stem=r"The diagram shows a regular hexagon $ABCDEF$ and a regular octagon $ABPQRSTU$. Find:",
        topic_id=11)

    add_q(db, p2.id, exam_dir, 2, 7, "b",
        r"Find $\angle CAP$.",
        2, "Polygon Angles", 16, (15, 0.36, 0.56),
        r"""$\angle CAB = \frac{180 - 120}{2} = 30°$ (base angles of isos. triangle)
$\angle PAB = \frac{180 - 135}{2} = 22.5°$ (base angles of isos. triangle)
$\angle CAP = 30 + 22.5 = 52.5°$""",
        "ecf from 11(a), M1 — either angle correct, A1",
        topic_id=11)

    # P2 Q8 — Pages 16-17 (idx 15-16)
    add_q(db, p2.id, exam_dir, 2, 8, "a",
        r"Find the values for $x$, $y$ and $z$.",
        3, "Number Properties / Prime", 16, (15, 0.56, 0.95),
        r"""$x$ = odd (same as $y$ or 2)
$y = 1$
$5(x + 1) - 3(x - 2) = 21$
$5x + 5 - 3x + 6 = 21$
$2x = 10$, $x = 5$
So $z = 5$""",
        "B1, M1, B1",
        stem=r"The lengths of three sides of an isosceles $\triangle ABC$ are $x$ cm, $y$ cm and $z$ cm. Given that $x$ is an odd prime integer, $y$ is a whole number yet it is not a prime nor a composite number, and $5(x + 1) - 3(x - 2) = 21$.",
        topic_id=1)

    add_q(db, p2.id, exam_dir, 2, 8, "bi",
        r"Construct $\triangle PQR$. The point $P$ has been drawn for you.",
        3, "Construction", 17, (16, 0.04, 0.34),
        r"$\triangle PQR$ constructed with $\angle QPR = 45°$, $PR = 4$ cm, $PQ = 5.5$ cm.", "M1 for 1 arc to get point R, M1 for 1 arc to get point Q, M1 to measure angle",
        stem=r"Construct a $\triangle PQR$, in which $\angle QPR = 45°$, $PR = 4$ cm and $PQ = 5.5$ cm.",
        topic_id=10)

    add_q(db, p2.id, exam_dir, 2, 8, "bii",
        r"Measure $\angle PRQ$ and name the type of triangle $\triangle PQR$ is.",
        2, "Construction — Measurement", 17, (16, 0.34, 0.55),
        r"$\angle PRQ = 90°$ (accepted 87-90). $\triangle PQR$ is a right-angled/isosceles triangle.", "M1 must measure from drawing, A1",
        topic_id=10)

    add_q(db, p2.id, exam_dir, 2, 8, "biii",
        r"Does $\triangle PQR$ have a line of symmetry? If there is, draw and label the line of symmetry with a dashed line (-------).",
        1, "Symmetry", 17, (16, 0.55, 0.70),
        r"It has one. (Can use line bisector or angle bisector method to obtain the symmetry line accurately.) Accepted based on above 8: no line of symmetry.", "B1",
        topic_id=10)

    add_q(db, p2.id, exam_dir, 2, 8, "biv",
        r"Indicate how many rotational symmetries $\triangle PQR$ has.",
        1, "Symmetry — Rotational", 17, (16, 0.70, 0.82),
        r"None or 0", "B1",
        topic_id=10)

    # P2 Q9 — Page 18 (idx 17)
    add_q(db, p2.id, exam_dir, 2, 9, "a",
        r"The manager of branch A claims that his store had a higher percentage increase in sales compared to branch B from 2020 to 2022. Do you think his claim is correct? Explain your answer by showing calculations to support your explanation.",
        3, "Percentage — Data Interpretation", 18, (17, 0.04, 0.62),
        r"""It is not correct.
Branch A: sales went up from 50 to 60 which is rise in $\frac{10}{50} \times 100 = 20\%$
Branch B: while in B, it is $\frac{30}{90} \times 100 = 33.3\%$""",
        "B1, A1, A1",
        stem=r"Two branch managers of a fast-food chain called Super Juicy Chicken (SJC) presented the following line graphs showing the annual sales of their fried-chicken.",
        topic_id=14)

    add_q(db, p2.id, exam_dir, 2, 9, "b",
        r"Explain what could be done to the graphs to better compare the sales of both branches more effectively.",
        2, "Data Interpretation — Graphs", 18, (17, 0.62, 0.95),
        r"The 2 graphs are plotted on the same range of number or same scale along the $y$-axis, so we can see which branch has a steeper/higher sales (gradient) than the other.", "B1, B1",
        topic_id=14)

    # P2 Q10 — Pages 19-20 (idx 18-19)
    add_q(db, p2.id, exam_dir, 2, 10, "a",
        r"Find the value of $q$.",
        1, "Linear Functions — Table", 19, (18, 0.04, 0.35),
        r"$q = 12$", "B1",
        stem=r"A piece of fish is kept in a refrigerator. Its temperature, $y$ °C, at time $t$ hours is given by the equation $y = 20 - 4t$ for $0 \leq t \leq 6$. The following table of values was recorded.",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 10, "b",
        r"Using a scale of 2 cm to 1 unit on the horizontal $x$-axis and 2 cm to 2 units on the vertical $y$-axis, draw the graph of $y = 20 - 4t$ for $0 \leq t \leq 6$.",
        3, "Linear Functions — Graph", 19, (18, 0.35, 0.60),
        r"See graph. Axes drawn to the scale. Specified and labelled axes with units. All points plotted correctly. Straight line labelled with equation.", "M1 for axes to scale, M1 for specified and labelled axes with units, M1 for all points plotted correctly, M1 for straight line labelled with equation",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 10, "c",
        r"State the gradient of the graph and explain what the value of the gradient means.",
        2, "Linear Functions — Gradient Interpretation", 19, (18, 0.60, 0.78),
        r"Gradient is $-4$. It means that the temperature is dropping by 4 every hour/unit time. Negatively related to time.", "B1, B1",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 10, "d",
        r"Use the graph to find out the number of hours it takes for the temperature of the fish to reach the freezing point.",
        1, "Linear Functions — Reading Graph", 19, (18, 0.78, 0.88),
        r"It takes $t = 5$ hours.", "B1 from graph to show it",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 10, "e",
        r"What does the constant term, 20, in the equation represent?",
        1, "Linear Functions — Interpretation", 19, (18, 0.88, 0.97),
        r"20 means that the original/starting temperature of the fish/constant start value.", "B1",
        topic_id=6)

    db.commit()
    p1_count = len(p1.questions)
    p2_count = len(p2.questions)
    print(f"Seeded Bedok South exam id={exam.id}: Paper 1 ({p1_count} parts), Paper 2 ({p2_count} parts)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
