"""Seed Bartley Secondary School EOY 2023 Sec 1 Express Math exam."""

import os
import shutil
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/Bartley-Secondary-EOY-2023-Sec-1-Math-Group-3.pdf"
IMAGES_DIR = "/tmp/bartley_pages"

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

    school = db.query(School).filter(School.name == "Bartley Secondary School").first()
    if not school:
        school = School(name="Bartley Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(Exam.school_id == school.id, Exam.year == 2023).first()
    if existing:
        print(f"Bartley 2023 already seeded (id={existing.id}). Deleting and re-seeding.")
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
        source_pdf="Bartley-Secondary-EOY-2023-Sec-1-Math-Group-3.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # Single Paper — Pages 2-18 (idx 1-17), 80 marks, 1h45m
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=105, total_marks=80,
               date=date(2023, 10, 9), instructions="Answer all questions.")
    db.add(p1); db.flush()

    # Q1 — Page 2 (idx 1)
    # Calculate 7.6^3 / (6.14 - 0.15)
    add_q(db, p1.id, exam_dir, 1, 1, "a",
        r"Write down the first ten digits of your answer.",
        1, "Calculator Usage", 2, (1, 0.04, 0.18),
        r"$71.75741724$", "B1",
        stem=r"Calculate $\dfrac{7.6^3}{6.14 - 0.15}$.",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 1, "b",
        r"Write your answer in (a) to 4 significant figures.",
        1, "Rounding — Significant Figures", 2, (1, 0.17, 0.30),
        r"$71.76$ or their (a) to 4 s.f.", "B1 or FT",
        topic_id=3)

    # Q2 — Page 2 (idx 1)
    add_q(db, p1.id, exam_dir, 1, 2, "a",
        r"Bel wants to prepare a 300 millilitres drink. How much orange concentrate will she need?",
        1, "Ratio", 2, (1, 0.33, 0.58),
        r"$300 \div 5 = 60$ ml", "B1",
        stem=r"Bel bought a one litre bottle of orange concentrate. She uses the orange concentrate to make a drink. The recommended ratio of orange concentrate to water is $1 : 4$.",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 2, "b",
        r"Bel wants to prepare drinks for a class party of 40 students. She bought 2 bottles of orange concentrate. Caden said that it will not be enough for them if each student drinks 300 millilitres of the drink. Is Caden right? Justify your answer.",
        2, "Ratio — Word Problem", 2, (1, 0.57, 0.96),
        r"""Amount of drinks needed $= 40 \times 300 = 12000$ ml $= 12$ l
Concentrate needed $= 12 \div 5 = 2.4$ l
More than 2 l. Caden is right.
Or: $2l \times 5 = 10l$. 2 l can only make 10 l of drinks. So Caden is right.""",
        "M1, A1",
        topic_id=9)

    # Q3 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 3, "a",
        r"In triangle $ABC$, $AC = 8$ cm and $BC = 6$ cm. The line $AB$ is drawn below. Construct triangle $ABC$.",
        2, "Construction", 3, (2, 0.04, 0.65),
        r"B2 for correct arcs shown. B1 if no arc is shown but correct $AC = 8$ cm or $BC = 6$ cm.", "B2",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 3, "b",
        r"Measure angle $ACB$.",
        1, "Construction — Measurement", 3, (2, 0.64, 0.78),
        r"$90°$ (accept $89°$ to $91°$)", "B1",
        topic_id=10)

    # Q4 — Page 4 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 4, "a",
        r"Simplify $(2x + y) - 2(x - 2y)$.",
        2, "Algebra — Expansion", 4, (3, 0.04, 0.22),
        r"$$= 2x + y - 2x + 4y = 5y$$", "M1, A1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 4, "b",
        r"Simplify $\dfrac{2x}{3} + \dfrac{x}{4}$.",
        2, "Algebra — Fractions", 4, (3, 0.21, 0.38),
        r"$$= \frac{8x + 3x}{12} = \frac{11x}{12}$$", "M1, A1",
        topic_id=4)

    # Q5 — Page 4 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 5, "a",
        r"Write down one misleading feature in the chart above.",
        1, "Statistical Diagrams — Misleading", 4, (3, 0.38, 0.82),
        r"Over claiming or exaggerating title / The title gives a reader a false sense that the decrease is a lot / The vertical axis did not start from zero / The decrease will be magnified / There is missing data for some years, 2019 and 2020 / There is uncertainty — could be increase or decrease that were not known.", "B1",
        stem=r"A line chart titled 'The number of Road Accident has drastically decreased over the years' shows data for years 2018, 2021, and 2022.",
        topic_id=14)

    add_q(db, p1.id, exam_dir, 1, 5, "b",
        r"Explain why it is misleading.",
        1, "Statistical Diagrams — Reasoning", 4, (3, 0.81, 0.96),
        r"The vertical axis did not start from zero, so the decrease is magnified. OR There is missing data for years 2019 and 2020.", "B1",
        topic_id=14)

    # Q6 — Page 5 (idx 4)
    # Find a when b = -10 and c = 9
    add_q(db, p1.id, exam_dir, 1, 6, "a",
        r"Find $a$ when $b = -10$ and $c = 9$, given $a = \dfrac{b + c}{b - c}$.",
        2, "Formula Substitution", 5, (4, 0.04, 0.42),
        r"$$a = \frac{-10 + 9}{-10 - 9} = \frac{-1}{-19} = \frac{1}{19}$$", "M1, A1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 6, "b",
        r"Find $a$ when $b = -10$ and $c = 9$, given $a = \sqrt{b^2 - 4c}$.",
        2, "Formula Substitution", 5, (4, 0.41, 0.85),
        r"$$a = \sqrt{(-10)^2 - 4(9)} = \sqrt{100 - 36} = \sqrt{64} = 8$$", "M1, A1",
        topic_id=4)

    # Q7 — Page 6 (idx 5)
    add_q(db, p1.id, exam_dir, 1, 7, "a",
        r"Write down the intersection point of line $AB$ and $CD$.",
        1, "Coordinate Geometry", 6, (5, 0.04, 0.62),
        r"$(2, 3)$", "B1",
        stem=r"The graph shows two lines $AB$ and $CD$ on a Cartesian plane.",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 7, "b",
        r"Write down the equation of line $CD$.",
        1, "Linear Functions — Equation", 6, (5, 0.61, 0.76),
        r"$x = 2$", "B1",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 7, "c",
        r"Find the gradient of the line $AB$.",
        2, "Linear Functions — Gradient", 6, (5, 0.75, 0.96),
        r"$$\text{Gradient} = \frac{5 - 2}{-2 - 4} = \frac{3}{-6} = -\frac{1}{2}$$", "M1, A1",
        topic_id=6)

    # Q8 — Page 7 (idx 6)
    add_q(db, p1.id, exam_dir, 1, 8, "a",
        r"Angle $AEB = $ .......... because ..................",
        2, "Angle Properties — Parallel Lines", 7, (6, 0.04, 0.60),
        r"$\angle AEB = 77°$. Corresponding angles (or corr. $\angle$s), $DC \parallel EB$.", "B1, B1",
        stem=r"$DC$ and $EB$ are parallel lines. Angle $BAE = 63°$ and angle $ADC = 77°$. Complete these statements by finding the size of each angle. Give a reason for your answer.",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 8, "b",
        r"Angle $ACD = $ .......... because ..................",
        2, "Angle Properties — Triangle", 7, (6, 0.59, 0.80),
        r"$\angle ACD = 180° - 77° - 63° = 40°$. Angle sum of a triangle (or $\angle$ sum of $\triangle$).", "B1, B1",
        topic_id=10)

    # Q9 — Page 7 (idx 6)
    add_q(db, p1.id, exam_dir, 1, 9, None,
        r"Solve $\dfrac{2x + 1}{4} = \dfrac{x}{3}$.",
        3, "Solving Linear Equations", 7, (6, 0.80, 0.98),
        r"""$$3(2x + 1) = 4x$$
$$6x + 3 = 4x$$
$$6x - 4x = -3$$
$$2x = -3$$
$$x = -\frac{3}{2} = -1\frac{1}{2} \text{ (accept } {-1.5}\text{)}$$""",
        "M1, M1, A1",
        topic_id=5)

    # Q10 — Page 8 (idx 7)
    add_q(db, p1.id, exam_dir, 1, 10, None,
        r"$ABF$, $CGI$, $BCD$ and $EFGH$ are straight lines. Angle $ABC = 72°$ and angle $IGH = 108°$. Prove that quadrilateral $BCGF$ is a parallelogram. Give a reason for each step of your working.",
        3, "Angle Properties — Parallelogram Proof", 8, (7, 0.04, 0.96),
        r"""$\angle FBC = 180° - 72° = 108°$ (adjacent angles on a straight line)
$\angle FGC = 108°$ (vertically opposite angles)
Therefore $\angle FBC = \angle FGC$.
Opposite angles in a quadrilateral are equal, which implies $BCGF$ is a parallelogram.""",
        "M1, M1, A1",
        topic_id=10)

    # Q11 — Page 9 (idx 8)
    add_q(db, p1.id, exam_dir, 1, 11, "a",
        r"Write 2904 as a product of its prime factors.",
        1, "Prime Factorisation", 9, (8, 0.04, 0.18),
        r"$2904 = 2^3 \times 3 \times 11^2$ (accept $2 \times 2 \times 2 \times 3 \times 11 \times 11$)", "B1",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 11, "b",
        r"Find the smallest positive integer value of $k$ such that $2904k$ is a perfect cube.",
        1, "Perfect Cube", 9, (8, 0.17, 0.38),
        r"$k = 99$", "B1",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 11, "c",
        r"The highest common factor and lowest common multiple of two numbers are 10 and 120 respectively. The two numbers are not 10 and 120. Find the two numbers.",
        2, "HCF and LCM", 9, (8, 0.37, 0.68),
        r"$30$ and $40$", "B1, B1",
        topic_id=1)

    # Q12 — Page 9 (idx 8)
    add_q(db, p1.id, exam_dir, 1, 12, "a",
        r"Factorise completely $3a + 12ab - 6ac$.",
        1, "Algebra — Factorisation", 9, (8, 0.68, 0.82),
        r"$3a(1 + 4b - 2c)$", "B1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 12, "b",
        r"Factorise completely $3m(2m - 1) + 2n(1 - 2m)$.",
        2, "Algebra — Factorisation", 9, (8, 0.81, 0.98),
        r"""$$= 3m(2m - 1) - 2n(2m - 1)$$
$$= (2m - 1)(3m - 2n)$$""",
        "M1, A1",
        topic_id=4)

    # Q13 — Page 10 (idx 9)
    add_q(db, p1.id, exam_dir, 1, 13, "a",
        r"$ABCDE$ is a pentagon. Angles are $B = 132°$, $C = 88°$, $E = 123°$ and $D = x°$. Find $x$.",
        3, "Polygon Angles — Interior", 10, (9, 0.04, 0.58),
        r"""Sum of interior angles of pentagon $= (5 - 2) \times 180° = 540°$
$132° + 88° + 123° + 90° + x° = 540°$ (note: from the figure $A$ appears to be approx $107°$)
Actually: $132 + 88 + 123 + 90 + x = 540$
$x = 540 - 132 - 88 - 123 - 90 = 107°$
Otherwise sum of interior angles $= 540°$""",
        "M1, M1, A1",
        topic_id=11)

    add_q(db, p1.id, exam_dir, 1, 13, "b",
        r"The ratio of the interior angle of an $n$-sided regular polygon to its exterior angle is $8 : 1$. Find $n$.",
        2, "Polygon Angles — Exterior", 10, (9, 0.57, 0.96),
        r"""$9$ units $= 180°$
$1$ unit $= 20°$
Exterior angle $= 20°$
$n = \frac{360°}{20°} = 18$""",
        "M1, A1",
        topic_id=11)

    # Q14 — Page 11 (idx 10)
    add_q(db, p1.id, exam_dir, 1, 14, "a",
        r"Find the 5th term.",
        1, "Number Patterns", 11, (10, 0.04, 0.25),
        r"$27$", "B1",
        stem=r"The first four terms in the sequence are shown below: $11$, $15$, $19$, $23$.",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 14, "b",
        r"Find an expression, in terms of $n$, for the $n$th term of the sequence.",
        1, "Number Patterns — General Term", 11, (10, 0.24, 0.50),
        r"$7 + 4n$", "B1",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 14, "c",
        r"Explain why 101 is not a term of this sequence.",
        2, "Number Patterns — Reasoning", 11, (10, 0.49, 0.96),
        r"""$7 + 4n = 101$
$4n = 94$
$n = 23.5$
$n$ is not an integer (whole number), so $101$ is not a term.""",
        "B1",
        topic_id=7)

    # Q15 — Page 12 (idx 11)
    add_q(db, p1.id, exam_dir, 1, 15, "a",
        r"Find his speed in m/s.",
        2, "Speed Conversion", 12, (11, 0.04, 0.33),
        r"""$2.4$ km $= 2400$ m
$10$ min $= 600$ s
Speed $= \frac{2400}{600} = 4$ m/s""",
        "Either M1, A1",
        stem=r"John ran 2.4 km in 10 minutes.",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 15, "b",
        r"Sammy ran 10 km in 1 hour. Who is faster? Support your answer with numerical calculation.",
        2, "Speed — Comparison", 12, (11, 0.32, 0.62),
        r"""$10$ km $= 10000$ m, $1$ h $= 3600$ s
Sammy's speed $= \frac{10000}{3600} \approx 2.78$ m/s
John is faster.""",
        "M1, A1",
        topic_id=9)

    # Q16 — Page 12 (idx 11)
    add_q(db, p1.id, exam_dir, 1, 16, None,
        r"Express $\dfrac{3a - b}{4} - \dfrac{3a - 2b}{6}$ as a single fraction in its simplest form.",
        4, "Algebra — Algebraic Fractions", 12, (11, 0.62, 0.98),
        r"""$$= \frac{3(3a - b) - 2(3a - 2b)}{12}$$
$$= \frac{9a - 3b - 6a + 4b}{12}$$
$$= \frac{3a + b}{12}$$""",
        "M2, M1, A1",
        topic_id=4)

    # Q17 — Page 13 (idx 12)
    add_q(db, p1.id, exam_dir, 1, 17, "a",
        r"Complete the table of values for $y = \dfrac{x}{2} - 1$.",
        1, "Linear Functions — Table", 13, (12, 0.04, 0.14),
        r"$y = -3, 1, 2$", "B1",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 17, "b",
        r"On the grid, draw the graph of $y = \dfrac{x}{2} - 1$ for $-4 \leq x \leq 6$.",
        2, "Linear Functions — Graph", 13, (12, 0.13, 0.66),
        r"All points are plotted correctly. Straight line drawn.", "B1, B1",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 17, "ci",
        r"Use your graph to find the coordinates of the $x$-intercept.",
        1, "Linear Functions — Intercept", 13, (12, 0.65, 0.80),
        r"$(2, 0)$", "B1",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 17, "cii",
        r"Use your graph to find the value of $y$ when $x = 5$.",
        1, "Linear Functions — Reading Graph", 13, (12, 0.79, 0.96),
        r"$y = 1.5$", "B1",
        topic_id=6)

    # Q18 — Page 14 (idx 13)
    add_q(db, p1.id, exam_dir, 1, 18, "a",
        r"Find the sales difference between the food stall with the greatest sale and the one with the least sale.",
        1, "Statistical Diagrams — Bar Chart", 14, (13, 0.04, 0.60),
        r"$\$24000 - \$15000 = \$9000$", "B1",
        stem=r"A bar chart shows monthly sales for Food Stall A, Food Stall D, Food Stall C, and Drink Stall D.",
        topic_id=14)

    add_q(db, p1.id, exam_dir, 1, 18, "b",
        r"A pie chart is created for the same information. Find the angle of the sector that represents the monthly sale for Drink Stall D.",
        2, "Statistical Diagrams — Pie Chart", 14, (13, 0.59, 0.96),
        r"""Total $= 96000$ (approx from chart: $15000 + 25000 + 20000 + 36000$)
Angle $= \frac{36000}{96000} \times 360° = 135°$""",
        "M1, A1",
        topic_id=14)

    # Q19 — Page 15 (idx 14)
    add_q(db, p1.id, exam_dir, 1, 19, "a",
        r"Find the distance travelled by the motorist in terms of $x$.",
        1, "Speed, Distance, Time", 15, (14, 0.04, 0.20),
        r"$2x$ km", "B1",
        stem=r"A motorist travelled at the speed of $x$ km/h for 2 hours.",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 19, "b",
        r"He increased his speed by 10 km/h and travelled for another 3 hours. His average speed was 74 km/h. Form an equation and show that it reduces to $5x + 30 = 370$.",
        2, "Linear Equations — Forming", 15, (14, 0.19, 0.64),
        r"""$$\frac{2x + 3(x + 10)}{5} = 74$$
$$2x + 3x + 30 = 370$$
$$5x + 30 = 370 \text{ (shown)}$$""",
        "M1, A1",
        topic_id=5)

    add_q(db, p1.id, exam_dir, 1, 19, "c",
        r"Solve $5x + 30 = 370$.",
        1, "Linear Equations — Solving", 15, (14, 0.63, 0.96),
        r"$5x = 340$, $x = 68$", "A1",
        topic_id=5)

    # Q20 — Page 16 (idx 15)
    add_q(db, p1.id, exam_dir, 1, 20, "a",
        r"Find the area of the parallelogram.",
        2, "Area — Parallelogram", 16, (15, 0.04, 0.48),
        r"$$\text{Area} = 12 \times 5 = 60 \text{ cm}^2$$", "M1, A1",
        stem=r"A parallelogram with base 12 cm and height 5 cm (slant side 6 cm).",
        topic_id=12)

    add_q(db, p1.id, exam_dir, 1, 20, "b",
        r"The area of the trapezium is 204 cm$^2$. Find $x$.",
        2, "Area — Trapezium", 16, (15, 0.47, 0.96),
        r"""$$\frac{1}{2}(x + 22) \times 12 = 204$$
$$6(x + 22) = 204$$
$$x + 22 = 34$$
$$x = 12$$""",
        "M1, A1",
        stem=r"A trapezium with parallel sides $x$ cm and 22 cm, height 12 cm, and slant side 13 cm.",
        topic_id=12)

    # Q21 — Pages 17-18 (idx 16-17)
    add_q(db, p1.id, exam_dir, 1, 21, "a",
        r"Show that his pocket money in August 2023 is $\$210$.",
        2, "Arithmetic — Word Problem", 17, (16, 0.04, 0.52),
        r"""Number of schooling days $= 21$
Total pocket money in August $= 21 \times \$10 = \$210$ (shown)""",
        "M1, A1",
        stem=r"The pocket money for Jim is $\$10$ per day when he goes to school. The 2023 August calendar is shown, with public holidays and school holidays on 9 August and 10 August.",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 21, "b",
        r"On 8 August, due to the celebration for National Day, the school will be dismissed at 1030 and the canteen will be closed for that day. On Monday, Tuesday, Wednesday and Thursday, Jim has 2 meals in school. On Friday, he has only 1 meal in school. Find the number of meals he had in school in August.",
        2, "Arithmetic — Word Problem", 17, (16, 0.51, 0.96),
        r"""Number of days with 2 meals $= 3 + 1 + 4 + 4 + 4 = 16$
Number of days with 1 meal $= 4$
Total number of meals $= 16 \times 2 + 4 \times 1 = 36$""",
        "M1, M1 or A1",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 21, "c",
        r"Based on the food prices, would he be able to save $\$100$ in the month of August? Justify any decisions that you make and show your calculations clearly.",
        4, "Real-World Problem — Money", 18, (17, 0.04, 0.78),
        r"""Min amount of money for food $= 36 \times 3 = \$108$
$\$210 - \$108 = \$102$
Yes, he can save $\$100$.""",
        "M1, M1, M1, A1",
        stem=r"Food prices: Bowl of Noodle $\$3$, Fried Rice $\$3$, Western Food/Chicken chop/Pork Chop $\$5$, Japanese Food $\$8$, Mixed Rice $\$3$.",
        topic_id=2)

    db.commit()
    p1_count = len(p1.questions)
    print(f"Seeded Bartley exam id={exam.id}: Paper 1 ({p1_count} parts)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
