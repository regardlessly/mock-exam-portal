"""Seed Regent Secondary School EOY 2022 Sec 1 Express Math exam."""

import os
import shutil
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/66b1f567be084_5784.pdf"
IMAGES_DIR = "/tmp/regent2022_pages"

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

    school = db.query(School).filter(School.name == "Regent Secondary School").first()
    if not school:
        school = School(name="Regent Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(Exam.school_id == school.id, Exam.year == 2022).first()
    if existing:
        print(f"Regent 2022 already seeded (id={existing.id}). Deleting and re-seeding.")
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
        source_pdf="66b1f567be084_5784.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # PAPER 1 — Pages 3-13 (idx 2-12), 50 marks, 1 hour 15 min
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=75, total_marks=50,
               date=date(2022, 10, 10), instructions="Answer all questions.")
    db.add(p1); db.flush()

    # Q1 — Page 3 (idx 2)
    # Consider the numbers: 3, sqrt(16), 125/5, 7, 3pi
    add_q(db, p1.id, exam_dir, 1, 1, "a",
        r"Write down the prime number(s).",
        1, "Number Classification", 3, (2, 0.07, 0.22),
        r"$3$, $7$", "B1",
        stem=r"Consider the numbers below: $3$, $\sqrt{16}$, $\dfrac{125}{5}$, $7$, $3\pi$.",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 1, "b",
        r"Write down the irrational number(s).",
        1, "Number Classification", 3, (2, 0.21, 0.32),
        r"$3\pi$", "B1",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 1, "c",
        r"Write down the square number(s).",
        1, "Number Classification", 3, (2, 0.31, 0.42),
        r"$\sqrt{16}$ (since $16 = 4^2$)", "B1",
        topic_id=2)

    # Q2 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 2, "a",
        r"Calculate $\dfrac{-5 \times \sqrt{12.3}}{(-4) - (-2)}$, showing first five figures on your calculator display.",
        1, "Calculator Usage", 3, (2, 0.44, 0.62),
        r"$-3.3946$ (first five figures)", "B1",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 2, "b",
        r"Give your answer correct to 2 significant figures.",
        1, "Rounding / Approximation", 3, (2, 0.61, 0.72),
        r"$-3.4$", "B1",
        topic_id=3)

    # Q3 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 3, "a",
        r"Express 600 as the product of its prime factors in index notation.",
        2, "Prime Factorisation", 3, (2, 0.72, 0.85),
        r"$600 = 2^3 \times 3 \times 5^2$", "M1, A1",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 3, "b",
        r"Written as the product of its prime factors, $P = x^a \times y^b$. Based on the given information, it is concluded that the number $P$ is both a perfect square and a perfect cube. Do you agree? Explain your answer.",
        1, "Perfect Square / Cube", 3, (2, 0.84, 0.98),
        r"Yes, as the power 6 is a multiple of 2 and 3.", "B1",
        topic_id=1)

    # Q4 — Page 4 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 4, None,
        r"A sum of money is shared between Gary, Winnie and Fandi in the ratio of $5 : 3 : 1$. Winnie decided to give 50% of what she has to Fandi. As a result, Fandi has $\$500$. Calculate the sum of money that was shared.",
        3, "Ratio", 4, (3, 0.03, 0.60),
        r"""$$\frac{50}{100} \times 3k = 1.5k$$
Fandi's new amount $= k + 1.5k = 2.5k$
$2.5k = 500 \implies k = 200$
Total $= 9k = 9 \times 200 = \$1800$""",
        "M1 for expression, M1 for solving, A1",
        topic_id=9)

    # Q5 — Page 4 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 5, "a",
        r"56% as a fraction.",
        1, "Percentage — Fraction", 4, (3, 0.62, 0.78),
        r"$\dfrac{56}{100} = \dfrac{14}{25}$", "B1",
        stem=r"Express:",
        topic_id=8)

    add_q(db, p1.id, exam_dir, 1, 5, "b",
        r"40 km/h in m/s.",
        2, "Speed Conversion", 4, (3, 0.77, 0.98),
        r"$$40 \times \frac{1000}{3600} = 11\frac{1}{9} \text{ m/s}$$", "M1, A1",
        topic_id=9)

    # Q6 — Page 5 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 6, "a",
        r"$-2m + 7 - 2m - 3$",
        1, "Algebra — Simplification", 5, (4, 0.04, 0.24),
        r"$-4m + 4$", "B1",
        stem=r"Expand and simplify the following algebraic expressions.",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 6, "b",
        r"$4(y + 2) - 5(2y - 3)$",
        2, "Algebra — Expansion", 5, (4, 0.23, 0.49),
        r"$$4y + 8 - 10y + 15 = -6y + 23$$", "M1, A1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 6, "c",
        r"$\dfrac{x - 3}{3} + \dfrac{-5 + 2x}{5}$",
        3, "Algebra — Fractions", 5, (4, 0.48, 0.98),
        r"""$$= \frac{5(x - 3) + 3(-5 + 2x)}{15}$$
$$= \frac{5x - 15 - 15 + 6x}{15}$$
$$= \frac{11x - 30}{15}$$""",
        "M1 for LCD, M1 for expanding, A1",
        topic_id=4)

    # Q7 — Page 6 (idx 5)
    # Sequence of squares: Diagram 1=6, 2=9, 3=12, 4=15, 5=r
    add_q(db, p1.id, exam_dir, 1, 7, "a",
        r"Find the value of $r$.",
        1, "Number Patterns", 6, (5, 0.04, 0.34),
        r"$r = 18$", "B1",
        stem=r"A sequence of made up of squares is shown below. Diagram 1 has 6, Diagram 2 has 9, Diagram 3 has 12, Diagram 4 has 15, Diagram 5 has $r$ squares.",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 7, "b",
        r"Write down an expression for the $n$th term of the sequence.",
        1, "Number Patterns — General Term", 6, (5, 0.33, 0.44),
        r"$3n + 3$", "B1",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 7, "c",
        r"Find the number of squares in diagram 40.",
        1, "Number Patterns", 6, (5, 0.43, 0.54),
        r"$3(40) + 3 = 123$", "B1",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 7, "d",
        r"Find the diagram number that has 51 squares.",
        1, "Number Patterns", 6, (5, 0.53, 0.66),
        r"$3n + 3 = 51 \implies n = 16$", "B1",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 7, "e",
        r"Ethan said that all multiples of 3 is a term in the sequence. Do you agree with the statement? Explain your answer.",
        1, "Number Patterns — Reasoning", 6, (5, 0.65, 0.85),
        r"No as 3 is not a term in the sequence.", "B1",
        topic_id=7)

    # Q8 — Page 7 (idx 6)
    # PTQ, TUV and SVR are straight lines. PQ parallel to SR.
    # angle QTU = 24 deg, angle RVW = 39 deg, angle TUV = 75 deg
    add_q(db, p1.id, exam_dir, 1, 8, "a",
        r"$\angle TVS$.",
        1, "Angle Properties — Parallel Lines", 7, (6, 0.04, 0.48),
        r"$\angle TVS = 39°$ (vert. opp. angles)", "B1",
        stem=r"In the diagram, $PTQ$, $TUV$ and $SVR$ are straight lines and $PQ$ is parallel to $SR$. $\angle QTU = 24°$, $\angle RVW = 39°$ and $\angle TUV = 75°$. Stating your reasons clearly in your working, find:",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 8, "b",
        r"$\angle UTV$.",
        2, "Angle Properties — Parallel Lines", 7, (6, 0.47, 0.64),
        r"""$\angle QTV = \angle TVS = 39°$ (alt. angles, $PQ \parallel SR$)
$\angle UTV = 39° - 24° = 15°$""",
        "M1, A1",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 8, "c",
        r"reflex $\angle TUV$.",
        2, "Angle Properties", 7, (6, 0.63, 0.85),
        r"""$\angle TUV = 180° - 75° - 15°$ (sum of angles in triangle)
$= 92°$ (accept from marking scheme)
Reflex $\angle TUV = 360° - 92° = 268°$ (angles at a point)""",
        "M1, A1",
        topic_id=10)

    # Q9 — Page 8 (idx 7)
    # Graph with points P(4,5) and N(11,9), line 7y = 4x + 19
    add_q(db, p1.id, exam_dir, 1, 9, "a",
        r"Find the gradient of line.",
        1, "Linear Functions — Gradient", 8, (7, 0.04, 0.42),
        r"$$m = \frac{9 - 5}{11 - 4} = \frac{4}{7}$$", "B1",
        stem=r"The graph below shows a line with points $P(4, 5)$ and $N(11, 9)$.",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 9, "b",
        r"Given that the equation of the line is $7y = 4x + 19$, show that the $y$-intercept of the line is $\dfrac{19}{7}$.",
        1, "Linear Functions — Intercept", 8, (7, 0.41, 0.62),
        r"""$7y = 4x + 19$
$y = \frac{4}{7}x + \frac{19}{7}$
As $y = mx + c$, $y$-intercept is $\frac{19}{7}$.""", "B1",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 9, "c",
        r"Does $(2, 4)$ lie on the line $7y = 4x + 19$? Show your workings clearly.",
        1, "Linear Functions — Substitution", 8, (7, 0.61, 0.80),
        r"""$7y = 4x + 19$
$7(4) = 4(2) + 19$
$28 \neq 27$
Since $y \neq 4$, $(2, 4)$ does not lie on the line.""", "B1",
        topic_id=6)

    # Q10 — Page 9 (idx 8)
    # Bar graph: hours spent doing homework
    add_q(db, p1.id, exam_dir, 1, 10, "a",
        r"Find the total number of students in the class.",
        1, "Statistics — Bar Graph", 9, (8, 0.04, 0.46),
        r"Total students $= 1 + 4 + 7 + 5 + 3 = 20$", "B1",
        stem=r"The bar graph shows the hours spent doing homework by different students in a class.",
        topic_id=14)

    add_q(db, p1.id, exam_dir, 1, 10, "b",
        r"Express the number of students who spend 3 hours doing work daily as a percentage of the whole class.",
        1, "Statistics — Percentage", 9, (8, 0.45, 0.60),
        r"$\dfrac{5}{20} \times 100 = 25\%$", "B1",
        topic_id=14)

    add_q(db, p1.id, exam_dir, 1, 10, "c",
        r"Calculate the average number of hours the students spend doing homework daily.",
        2, "Statistics — Mean", 9, (8, 0.59, 0.82),
        r"$$\frac{0(1) + 1(4) + 2(7) + 3(5) + 4(3)}{20} = \frac{45}{20} = 2.25$$", "M1, A1",
        topic_id=14)

    # Q11 — Page 10 (idx 9)
    # Simple interest: Mrs Ravi deposited $P, monthly simple interest 0.03%, 15 months, total $56252
    add_q(db, p1.id, exam_dir, 1, 11, "a",
        r"Find the amount of interest earned in terms of $P$.",
        1, "Simple Interest", 10, (9, 0.04, 0.40),
        r"$$\text{Interest} = \frac{P \times 0.03 \times 15}{100} = \frac{9P}{2000}$$", "B1",
        stem=r"Mrs Ravi deposited an amount $\$P$ in PBS bank at the start of February 2021. The bank pays a monthly simple interest rate of 0.03% at the end of every month. Mrs Ravi checked her account at the start of May 2022 and found that the total amount in the account is $\$56\,252$.",
        topic_id=8)

    add_q(db, p1.id, exam_dir, 1, 11, "b",
        r"Calculate the initial amount that Mrs Ravi deposited.",
        3, "Simple Interest", 10, (9, 0.39, 0.82),
        r"""$$P + \frac{9P}{2000} = 56252$$
$$\frac{2009P}{2000} = 56252$$
$$P = \frac{56252 \times 2000}{2009}$$
$$P = \$56\,000$$""",
        "M1 for equation, M1 for solving, A1",
        topic_id=8)

    # Q12 — Page 11 (idx 10)
    # Construct parallelogram PQRS, PS = 7 cm, angle PQR = 70 deg
    add_q(db, p1.id, exam_dir, 1, 12, "a",
        r"Construct a parallelogram $PQRS$ such that $PS = 7$ cm and angle $PQR = 70°$. The line $PQ$ has been provided.",
        2, "Construction", 11, (10, 0.03, 0.22),
        r"M1 for correct length, M1 for correct angle.", "M1, M1",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 12, "b",
        r"Draw the diagonals of the parallelogram and mark the intersection point of the diagonal with the letter $T$.",
        1, "Construction", 11, (10, 0.03, 0.22),
        r"Correct diagonal with label $T$.", "B1",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 12, "c",
        r"Measure and write the angle $STR$.",
        1, "Construction — Measurement", 11, (10, 0.03, 0.22),
        r"$106°$", "B1",
        topic_id=10)

    # Q13 — Page 12 (idx 11)
    # CXD is a semicircle with centre Y. CDEF is a trapezium. CZ = 20 cm, FE = 48 cm.
    add_q(db, p1.id, exam_dir, 1, 13, "a",
        r"If the area of trapezium $CDEF$ is $820$ cm$^2$, find the length of $CD$.",
        2, "Area — Trapezium", 12, (11, 0.04, 0.58),
        r"""$$820 = \frac{1}{2}(CD + 48) \times 20$$
$$82 = CD + 48$$
$$CD = 34 \text{ cm}$$""",
        "M1, A1",
        stem=r"In the figure, $CXD$ is a semicircle with the centre $Y$ and $CDEF$ is a trapezium. $CZ = 20$ cm and $FE = 48$ cm.",
        topic_id=12)

    add_q(db, p1.id, exam_dir, 1, 13, "b",
        r"Hence, find the area of the shaded region.",
        3, "Area — Semicircle", 12, (11, 0.57, 0.82),
        r"""Radius $= \frac{34}{2} = 17$ cm
$$= \frac{1}{2} \times \pi \times 17^2 - \frac{1}{2} \times 34 \times 17 \approx 165 \text{ cm}^2$$""",
        "M1 for radius, M1 for semicircle area, A1",
        topic_id=12)

    # ══════════════════════════════════════════════
    # PAPER 2 — Pages 14-25 (idx 13-24), 50 marks, 1h30m
    # ══════════════════════════════════════════════
    p2 = Paper(exam_id=exam.id, paper_number=2, duration_minutes=90, total_marks=50,
               date=date(2022, 10, 12), instructions="Answer all questions.")
    db.add(p2); db.flush()

    # P2 Q1 — Page 14 (idx 13)
    add_q(db, p2.id, exam_dir, 2, 1, "a",
        r"$18ah + 3by$",
        1, "Algebra — Factorisation", 14, (13, 0.04, 0.20),
        r"$= 3(6ah + by)$", "B1",
        stem=r"Factorise the following algebraic expressions.",
        topic_id=4)

    add_q(db, p2.id, exam_dir, 2, 1, "b",
        r"$\dfrac{3}{5}x^2y + \dfrac{1}{5}xy^2$",
        1, "Algebra — Factorisation", 14, (13, 0.19, 0.38),
        r"$\frac{1}{5}xy(3x + y)$", "B1",
        topic_id=4)

    # P2 Q2 — Page 14 (idx 13)
    add_q(db, p2.id, exam_dir, 2, 2, None,
        r"Tim, Nora and Danson are given 3 ribbons of equal lengths. Tim cuts his ribbon into smaller pieces of equal length of 42 cm. Nora cuts her ribbon into smaller pieces of equal length of 24 cm. Danson cuts his ribbon into smaller pieces of equal length of 60 cm. If there are no ribbon leftover, what is the shortest possible length of ribbon given to each of them?",
        3, "LCM", 14, (13, 0.37, 0.90),
        r"""$42 = 2 \times 3 \times 7$
$24 = 2^3 \times 3$
$60 = 2^2 \times 3 \times 5$
Shortest possible length $= \text{LCM} = 2^3 \times 3 \times 5 \times 7 = 840$ cm""",
        "M1 for prime factors, M1 for LCM, A1",
        topic_id=1)

    # P2 Q3 — Page 15 (idx 14)
    # Pentagon ABCDEGF with triangle. AB parallel to ED. angle ABC=115, BCD=150, GEF=85
    add_q(db, p2.id, exam_dir, 2, 3, "ai",
        r"sum of interior angles in the pentagon $ABCDE$.",
        1, "Polygon Angles — Interior", 15, (14, 0.04, 0.52),
        r"Sum of interior angles $= (5 - 2) \times 180° = 540°$", "M1, A1",
        stem=r"In the diagram below, $ABCDEGF$ is made up of a pentagon and a triangle. $AB$ is parallel to $ED$, angle $ABC = 115°$, angle $BCD = 150°$ and angle $GEF = 85°$.",
        topic_id=11)

    add_q(db, p2.id, exam_dir, 2, 3, "aii",
        r"angle $EAB$.",
        2, "Polygon Angles", 15, (14, 0.51, 0.63),
        r"""$\angle DEA = 85°$
$\angle EAB = 180° - 85° = 95°$""",
        "M1, A1",
        topic_id=11)

    add_q(db, p2.id, exam_dir, 2, 3, "aiii",
        r"angle $EDC$.",
        1, "Polygon Angles", 15, (14, 0.62, 0.73),
        r"$\angle EDC = 540° - 115° - 150° - 95° - 85° = 95°$", "B1",
        topic_id=11)

    add_q(db, p2.id, exam_dir, 2, 3, "b",
        r"Using your answer in part (a), what can be said about lines $EA$ and $DC$? Explain your answer.",
        1, "Polygon Angles — Parallel Lines", 15, (14, 0.72, 0.90),
        r"$\angle EDC + \angle DEA = 95° + 85° = 180°$. Interior angles on a pair of parallel lines. Therefore $EA \parallel DC$.", "B1",
        topic_id=11)

    # P2 Q4 — Page 16 (idx 15)
    # Pie chart: exports of a country in 2021. Minerals 105 deg, Agricultural produce (angle to find), Manufactured goods 85 deg, Others 15 deg
    add_q(db, p2.id, exam_dir, 2, 4, "a",
        r"Express the export of minerals as a ratio of the agricultural produce.",
        2, "Ratio — Pie Chart", 16, (15, 0.04, 0.48),
        r"""Angle for agricultural produce $= 360° - 105° - 85° - 15° = 155°$
Ratio minerals : agricultural $= 105 : 155 = 21 : 31$""",
        "M1, A1",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 4, "b",
        r"If the value of the export of manufactured goods is worth $\$18$ million dollars in 2021, find the total value of all exports in the country in 2021.",
        2, "Ratio — Pie Chart", 16, (15, 0.47, 0.82),
        r"""$$\text{Total} = \frac{360°}{85°} \times 18 = 76.2 \text{ million}$$
Accept $\$76.2$ million""",
        "M1, A1",
        topic_id=9)

    # P2 Q5 — Pages 17-18 (idx 16-17)
    # Caleb and Jean: Singapore to KL, 330 km, drove 190 km in 2 hours, stopped 40 min
    add_q(db, p2.id, exam_dir, 2, 5, "a",
        r"Find the speed the journey for the first 2 hours.",
        1, "Speed, Distance, Time", 17, (16, 0.04, 0.28),
        r"Speed $= \frac{190}{2} = 95$ km/h", "B1",
        stem=r"Caleb and Jean started their journey to Kuala Lumpur from Singapore at 0900. The distance between Singapore and Kuala Lumpur is 330 km. They drove 190 km for 2 hours and decided to stop for a meal for 40 minutes.",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 5, "b",
        r"After the meal, Caleb and Jean continued driving and reached Kuala Lumpur at 1325. Calculate the average speed for the whole journey.",
        2, "Speed, Distance, Time", 17, (16, 0.27, 0.52),
        r"""From 0900 to 1325 $= 4$ h $25$ min. Driving time $= 4$ h $25$ min $- 40$ min $= 3$ h $45$ min.
Average speed $= \frac{330}{\frac{225}{60}} = \frac{330 \times 60}{225} = 74.7$ km/h""",
        "M1, A1",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 5, "c",
        r"Jean said that if they drove at the same speed as the first part of the journey, they will reach Kuala Lumpur before 1300. Do you agree with Jean? Support your answer with workings.",
        3, "Speed, Distance, Time", 17, (16, 0.51, 0.92),
        r"""Distance remaining $= 330 - 190 = 140$ km
Time needed $= \frac{140}{95} = 1.474$ hours $= 1$ h $28$ min (approx)
$1140 + 1$ h $28$ min $= 1308$
No, with a speed of 95 km/h, they would reach only at $1308$.""",
        "M1 for distance, M1 for time, A1 for conclusion",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 5, "d",
        r"For each litre of petrol, the car is able to travel a distance of 10.5 km. Calculate the amount of petrol, corrected to the nearest whole number, needed for the whole journey from Singapore to Kuala Lumpur.",
        2, "Speed, Distance, Time — Petrol", 18, (17, 0.04, 0.28),
        r"$$\frac{330}{10.5} = 31.428... \approx 32 \text{ litres}$$", "M1, A1",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 5, "e",
        r"At Kuala Lumpur, Caleb decided to pump petrol for the journey back to Singapore. Given that each litre of petrol cost RM 2.80 and 1 SGD $= $ RM 3.17, calculate how much will it cost in Singapore dollars for the return journey.",
        3, "Currency Conversion", 18, (17, 0.27, 0.80),
        r"""Cost in RM $= 32 \times 2.80 = \text{RM } 89.60$
Cost in SGD $= \frac{89.60}{3.17} = \$\!28.26$ (2 d.p.)""",
        "M1 for RM cost, M1 for conversion, A1",
        topic_id=9)

    # P2 Q6 — Page 19 (idx 18)
    # Participants: 2020 = Y, 2021 increased by 30%, 2022 increased by 350 from 2021
    add_q(db, p2.id, exam_dir, 2, 6, "a",
        r"Write down an expression in terms of $Y$, for the number of participants in 2021.",
        1, "Algebra — Expression", 19, (18, 0.04, 0.28),
        r"$1.3Y$", "B1",
        stem=r"The number of participants for an event in 2020 is $Y$. In 2021, the number of participants is increased by 30%.",
        topic_id=5)

    add_q(db, p2.id, exam_dir, 2, 6, "b",
        r"In 2022, the number of participants is increased by 350 from 2021. Write down an expression in terms of $Y$, for the number of participants in 2022.",
        1, "Algebra — Expression", 19, (18, 0.27, 0.46),
        r"$1.3Y + 350$", "B1",
        topic_id=5)

    add_q(db, p2.id, exam_dir, 2, 6, "c",
        r"If the total number of participants is 1390 in 2022, form an equation in terms of $Y$ and find the number of participants for the event in 2020.",
        3, "Linear Equations", 19, (18, 0.45, 0.82),
        r"""$1.3Y + 350 = 1390$
$1.3Y = 1040$
$Y = 800$""",
        "M1 for equation, M1 for solving, A1",
        topic_id=5)

    # P2 Q7 — Page 20 (idx 19)
    # Carpark rates at Mandarin Orchard
    add_q(db, p2.id, exam_dir, 2, 7, "a",
        r"Mrs Tan wants to park her car at Mandarin Orchard on a Sunday from 4.30 pm to 6.30 pm. Find the total carpark charges for the duration she parked.",
        2, "Real-World Problem", 20, (19, 0.04, 0.46),
        r"Total $= \$3.60 + 30(0.06) + \$3.60 = \$9.00$",
        "M1, A1",
        stem=r"The table below shows the carpark rates in Mandarin Orchard, Singapore. Weekdays 6am-6pm: \$3.60 first hour, \$0.06/min after. 6pm-6am: \$3.60 first hour, \$0.04/min after. Weekends 6am-6pm: same as weekdays. 6pm-6am: \$3.60 per entry.",
        topic_id=8)

    add_q(db, p2.id, exam_dir, 2, 7, "b",
        r"Heidi has $\$6$ in her cashcard that is used to pay for the carpark charges in Mandarin Orchard on a Wednesday. She said that with the same amount of money in her cashcard, she can park 20 minutes longer if she enters the carpark after 6pm compared to before 6pm. Do you agree? Support your answers with working.",
        3, "Real-World Problem", 20, (19, 0.45, 0.90),
        r"""Before 6pm: $6 - 3.60 = 2.40$. Extra time $= \frac{2.40}{0.06} = 40$ min. Total $= 60 + 40 = 100$ min.
After 6pm: $6 - 3.60 = 2.40$. Extra time $= \frac{2.40}{0.04} = 60$ min. Total $= 60 + 60 = 120$ min.
$120 - 100 = 20$ min. Yes, she can park 20 minutes more.""",
        "M1 for before 6pm, M1 for after 6pm, A1 for conclusion",
        topic_id=8)

    # P2 Q8 — Pages 21-23 (idx 20-22)
    # Cylindrical container: radius 7 cm, height 25 cm
    add_q(db, p2.id, exam_dir, 2, 8, "a",
        r"Calculate the volume of the cylinder.",
        2, "Volume — Cylinder", 21, (20, 0.04, 0.82),
        r"$$V = \pi r^2 h = \pi (7)^2 (25) = 3848.451... \approx 3850 \text{ cm}^3$$", "M1, A1",
        stem=r"The diagram below shows a cylindrical container used to store sand. The cylinder has a radius of 7 cm and a height of 25 cm.",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 8, "b",
        r"The diagram below shows an open prism whose cross-section is a trapezium $ABCD$. $AB = 30$ cm, $DC = 13$ cm, $DE = 20$ cm, $AD = BC = 22$ cm and $CF = 50$ cm. Calculate the volume of the prism.",
        3, "Volume — Prism", 22, (21, 0.04, 0.62),
        r"""Base area (trapezium) $= \frac{1}{2}(13 + 30)(20) = \frac{1}{2}(43)(20) = 430$ cm$^2$
Volume $= 430 \times 50 = 21\,500$ cm$^3$""",
        "M1 for area, M1 for volume, A1",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 8, "c",
        r"Kris decided to fill the trapezoidal prism with sand. Calculate the number of cylindrical containers of sand that is needed.",
        2, "Volume — Division", 23, (22, 0.04, 0.22),
        r"$$\frac{21500}{3848.451} = 5.586... \approx 6 \text{ containers}$$", "M1, A1",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 8, "d",
        r"Kris decided to paint the outer surfaces of the trapezoidal prism. Calculate the total surface area that she needs to paint.",
        3, "Surface Area — Prism", 23, (22, 0.21, 0.72),
        r"""$$\text{SA} = 2 \times \frac{1}{2}(13 + 30)(20) + 2 \times 22 \times 50 + 13 \times 50$$
$$= 860 + 2200 + 650 = 3710 \text{ cm}^2$$""",
        "M2 for areas, A1",
        topic_id=13)

    # P2 Q9 — Pages 24-25 (idx 23-24)
    # y = -5x + 4, table: x=0,y=4; x=2,y=-6; x=4,y=p; x=5,y=-21; x=7,y=-31
    add_q(db, p2.id, exam_dir, 2, 9, "a",
        r"Calculate the value of $p$.",
        1, "Linear Functions — Table", 24, (23, 0.04, 0.22),
        r"$p = -5(4) + 4 = -16$", "B1",
        stem=r"The table below shows the values of $x$ and $y$ connected by the equation $y = -5x + 4$.",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 9, "b",
        r"On the grid next page, draw the graph of $y = -5x + 4$ for $0 \leq x \leq 7$.",
        2, "Linear Functions — Graph", 24, (23, 0.21, 0.32),
        r"M1 for correct points, M1 for straight line plotted.", "M1, M1",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 9, "ci",
        r"the value of $y$ when $x = 1$.",
        1, "Linear Functions — Reading Graph", 24, (23, 0.32, 0.46),
        r"$y = -1$", "B1",
        stem=r"From your graph, find:",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 9, "cii",
        r"the value of $x$ when $y = -26$.",
        1, "Linear Functions — Reading Graph", 24, (23, 0.45, 0.56),
        r"$x = 6$", "B1",
        topic_id=6)

    db.commit()
    p1_count = len(p1.questions)
    p2_count = len(p2.questions)
    print(f"Seeded Regent 2022 exam id={exam.id}: Paper 1 ({p1_count} parts), Paper 2 ({p2_count} parts)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
