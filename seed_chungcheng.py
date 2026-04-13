"""Seed Chung Cheng High School (Yishun) EOY 2023 Sec 1 Express Math exam."""

import os
import shutil
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/Chung-Cheng-High-Yishun-EOY-2023-Sec-1-Math-Group-3.pdf"
IMAGES_DIR = "/tmp/chungcheng_pages"

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

    school = db.query(School).filter(School.name == "Chung Cheng High School (Yishun)").first()
    if not school:
        school = School(name="Chung Cheng High School (Yishun)")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(Exam.school_id == school.id, Exam.year == 2023).first()
    if existing:
        print(f"Chung Cheng 2023 already seeded (id={existing.id}). Deleting and re-seeding.")
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
        source_pdf="Chung-Cheng-High-Yishun-EOY-2023-Sec-1-Math-Group-3.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # SECTION A — Pages 2-10 (idx 1-9), 40 marks, 2 hours
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=120, total_marks=40,
               date=date(2023, 10, 2), instructions="Answer all questions.")
    db.add(p1); db.flush()

    # Q1 — Page 2 (idx 1)
    # Consider the following list of numbers: pi/3, -sqrt(2), sqrt(100/90), 1.01 (recurring)
    add_q(db, p1.id, exam_dir, 1, 1, "a",
        r"Write the numbers in order of size, starting with the smallest.",
        2, "Number Ordering", 2, (1, 0.05, 0.40),
        r"$-\sqrt{2}$, $1.\dot{0}1$, $\dfrac{\pi}{3}$, $\sqrt{\dfrac{100}{90}}$", "B2 (B1 for 2 correct)",
        stem=r"Consider the following list of numbers: $\dfrac{\pi}{3}$, $-\sqrt{2}$, $\sqrt{\dfrac{100}{90}}$, $1.\dot{0}1$.",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 1, "b",
        r"Write down all the irrational numbers.",
        1, "Number Classification", 2, (1, 0.40, 0.52),
        r"$\dfrac{\pi}{3}$, $-\sqrt{2}$", "B1",
        topic_id=2)

    # Q2 — Page 2 (idx 1)
    add_q(db, p1.id, exam_dir, 1, 2, "a",
        r"Round off 13.449 to one decimal place.",
        1, "Decimal Places", 2, (1, 0.52, 0.70),
        r"$13.4$", "B1",
        topic_id=3)

    add_q(db, p1.id, exam_dir, 1, 2, "b",
        r"Round off $\dfrac{3}{127}$ to two significant figures.",
        1, "Significant Figures", 2, (1, 0.70, 0.92),
        r"$0.024$", "B1",
        topic_id=3)

    # Q3 — Page 2 (idx 1)
    add_q(db, p1.id, exam_dir, 1, 3, None,
        r"Write down and simplify an algebraic expression for the following statement. Subtract the product of 3 and $4a$ from the sum of $2b$ and $16a$.",
        1, "Algebraic Expression", 2, (1, 0.90, 1.0),
        r"$(2b + 16a) - 3 \times 4a = 2b + 4a$", "B1",
        topic_id=4)

    # Q4 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 4, None,
        r"Given that $a = 2$, $b = -15$, and $c = 13$, find the value of $\dfrac{-b + \sqrt{b^2 - 4ac}}{2a}$.",
        2, "Algebraic Substitution", 3, (2, 0.04, 0.40),
        r"""$$= \frac{-(-15) + \sqrt{(-15)^2 - 4(2)(13)}}{2(2)}$$
$$= \frac{15 + \sqrt{225 - 104}}{4} = \frac{15 + 11}{4} = \frac{26}{4} = 6.5$$""",
        "M1 for substitution, A1",
        topic_id=4)

    # Q5 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 5, "a",
        r"Convert 78 000 cm$^2$ to m$^2$.",
        1, "Unit Conversion", 3, (2, 0.40, 0.62),
        r"$\dfrac{78\,000}{10\,000} = 7.8$ m$^2$", "B1",
        topic_id=13)

    add_q(db, p1.id, exam_dir, 1, 5, "b",
        r"By rounding each number to 1 significant figure, estimate the value of $\dfrac{\sqrt[3]{989}}{0.132 \times 472}$.",
        2, "Estimation", 3, (2, 0.60, 0.95),
        r"""$$\approx \frac{\sqrt[3]{1000}}{0.1 \times 500} = \frac{10}{50} = 0.2$$""",
        "M1 for rounding, A1",
        topic_id=3)

    # Q6 — Page 4 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 6, "a",
        r"Simplify $\dfrac{3}{2}b - \dfrac{1}{2}ha - 7b + 3ab$.",
        2, "Algebra — Simplification", 4, (3, 0.04, 0.38),
        r"$= -7b + \dfrac{3}{2}b + 3ab - \dfrac{1}{2}ha = \dfrac{5}{2}ab - \dfrac{11}{2}b$", "M1, A1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 6, "b",
        r"Factorise $-8xyz - 18yz + 6xz$ completely.",
        1, "Factorisation", 4, (3, 0.37, 0.60),
        r"$= -2z(4xy + 9y - 3x)$ or $2z(-4xy - 9y + 3x)$", "B1",
        topic_id=4)

    # Q7 — Page 4 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 7, None,
        r"Express $\dfrac{2a}{5} - \dfrac{a - 4}{3}$ as a single fraction in its simplest form.",
        2, "Algebraic Fractions", 4, (3, 0.60, 0.95),
        r"$$= \frac{6a}{15} - \frac{5(a - 4)}{15} = \frac{6a - 5a + 20}{15} = \frac{a + 20}{15}$$", "M1, A1",
        topic_id=4)

    # Q8 — Page 5 (idx 4)
    # A = 2^3 x 3^4 x 5, B = 2^6 x 3^3 x 7
    add_q(db, p1.id, exam_dir, 1, 8, "a",
        r"Find the largest integer which is a factor of both $A$ and $B$, leaving your answer as a product of its prime factors.",
        1, "HCF", 5, (4, 0.04, 0.52),
        r"$\text{HCF} = 2^3 \times 3^3$", "B1",
        stem=r"Two numbers $A$ and $B$ written as the product of their prime factors are $A = 2^3 \times 3^4 \times 5$ and $B = 2^6 \times 3^3 \times 7$.",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 8, "b",
        r"Find the smallest integer $k$ such that $A \times k$ is a multiple of $B$.",
        1, "LCM — Algebraic", 5, (4, 0.50, 0.72),
        r"All factors of $B$ must be included. $k = 2^3 \times 7 = 56$", "B1",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 8, "c",
        r"Find the smallest integer $p$ such that $A \times p$ is a perfect square.",
        1, "Perfect Square", 5, (4, 0.70, 0.95),
        r"$2^3 \times 3^4 \times 5 \times p = 2^4 \times 3^4 \times 5^2$, so $p = 2 \times 5 = 10$", "B1",
        topic_id=1)

    # Q9 — Page 6 (idx 5)
    add_q(db, p1.id, exam_dir, 1, 9, "a",
        r"If the washing machine was sold at a discount of 35%, find the original price of the washing machine.",
        2, "Reverse Percentage", 6, (5, 0.06, 0.46),
        r"""Since the washing machine was sold for $\$578.50$ at a discount of 35%,
$65\%$ rep $\$578.50$
$100\%$ rep $\dfrac{\$578.50}{65} \times 100 = \$890$""",
        "M1, A1",
        stem=r"During the Great Singapore Sale, a washing machine was sold at a discounted price of $\$578.50$.",
        topic_id=8)

    add_q(db, p1.id, exam_dir, 1, 9, "b",
        r"There is a GST of 8% on the selling price of the washing machine. A customer decided to pay the total amount over a period of 1.5 years. Find the monthly instalment of the washing machine. Leave your answer corrected to the nearest dollars.",
        2, "Percentage — GST Total", 6, (5, 0.44, 0.95),
        r"""Price after GST $= \$578.50 \times \dfrac{108}{100} = \$624.78$
Monthly instalment $= \dfrac{\$624.78}{18} = \$34.71 \approx \$35$""",
        "M1, A1",
        topic_id=8)

    # Q10 — Page 7 (idx 6)
    add_q(db, p1.id, exam_dir, 1, 10, "a",
        r"Find the length of $AE$.",
        2, "Area — Trapezium", 7, (6, 0.04, 0.62),
        r"$$\frac{1}{2} \times (5 + 13) \times AE = 108 \implies AE = 12 \text{ cm}$$", "M1, A1",
        stem=r"The diagram shows a trapezium $ABCE$ and $D$ is a point on $CE$ such that $BDE$ is an equilateral triangle. $AB = 5$ cm, $BD = 13$ cm, $CE = 28$ cm and the area of trapezium $ABDE$ is 108 cm$^2$.",
        topic_id=12)

    add_q(db, p1.id, exam_dir, 1, 10, "b",
        r"Find the area of triangle $BDC$.",
        2, "Area of Triangle", 7, (6, 0.60, 0.95),
        r"$CD = 28 - 13 = 15$ cm. Area of $\triangle BDC = \dfrac{1}{2} \times 15 \times 12 = 90$ cm$^2$", "M1, A1",
        topic_id=12)

    # Q11 — Page 8 (idx 7)
    add_q(db, p1.id, exam_dir, 1, 11, "a",
        r"A label is to be pasted to cover all of the curved surface area of the can. Find the area of the label.",
        2, "Surface Area — Cylinder", 8, (7, 0.04, 0.52),
        r"Curved Surface Area $= 2\pi(5)(16) \approx 503$ cm$^2$ (corrected to 3 s.f.)", "M1, A1",
        stem=r"A can of drink in the shape of a cylinder has radius 5 cm and height 16 cm.",
        topic_id=13)

    add_q(db, p1.id, exam_dir, 1, 11, "b",
        r"Calculate the volume of a dozen cans of drinks, giving your answer to the nearest litre.",
        3, "Volume — Cylinder", 8, (7, 0.50, 0.95),
        r"""Volume of a can $= \pi(5)^2(16)$
Volume of a dozen cans $= \pi(5)^2(16) \times 12 = 15\,079.6$ cm$^3 \approx 15.080$ l $\approx 15$ l""",
        "M1 for one can, M1 for dozen, A1",
        topic_id=13)

    # Q12 — Page 9 (idx 8)
    add_q(db, p1.id, exam_dir, 1, 12, "a",
        r"Find $\angle ABK$.",
        2, "Angle Properties — Parallel Lines", 9, (8, 0.04, 0.55),
        r"""$\angle CBK = \angle DCF = 50°$ (corr. $\angle$s, $BK \parallel CF$)
$\angle ABK = 180° - 50° = 130°$ (adj. $\angle$s on st. line)""",
        "M1, A1",
        stem=r"In the diagram below, $AD$ is parallel to $JE$ and $BK$ is parallel to $CF$. It is given that $\angle DCF = 50°$, $\angle CGH = 130°$ and $\angle KHG = 45°$.",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 12, "b",
        r"Find the reflex angle of $\angle BKH$.",
        2, "Angle Properties — Parallel Lines", 9, (8, 0.53, 0.95),
        r"""$\angle BKN = \angle KBC = 50°$ (alt. $\angle$s, $\parallel$ lines)
$\angle NKH = \angle KHG = 45°$ (alt. $\angle$s, $\parallel$ lines)
Reflex $\angle BKH = 360° - 50° - 45° = 265°$ ($\angle$s at a point)""",
        "M1, A1",
        topic_id=10)

    # Q13 — Page 10 (idx 9)
    add_q(db, p1.id, exam_dir, 1, 13, "a",
        r"Construct the quadrilateral $ABCD$, showing the construction arcs and measurements clearly. $AB$ has been drawn for you.",
        2, "Construction", 10, (9, 0.04, 0.78),
        r"Quadrilateral $ABCD$ correctly constructed with $AB = 9$ cm, $AD = 5$ cm, $BD = 8$ cm, angle $ADC = 110°$, $CD = 3$ cm.", "B1 for triangle ABD, B1 for point C",
        stem=r"A quadrilateral $ABCD$ is such that $AB = 9$ cm, $AD = 5$ cm, $BD = 8$ cm. Angle $ADC$ is $110°$ and $CD = 3$ cm.",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 13, "b",
        r"Measure the length $BC$.",
        1, "Construction — Measurement", 10, (9, 0.77, 0.87),
        r"$BC = 5.5 \pm 0.1$ cm", "B1",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 13, "c",
        r"$W$ is a point on $AD$ such that angle $ABW$ is $20°$. Mark the point $W$ on the diagram.",
        1, "Construction", 10, (9, 0.86, 0.95),
        r"Point $W$ correctly marked on $AD$.", "B1",
        topic_id=10)

    # ══════════════════════════════════════════════
    # SECTION B — Pages 12-20 (idx 11-19), 40 marks, 2 hours
    # ══════════════════════════════════════════════
    p2 = Paper(exam_id=exam.id, paper_number=2, duration_minutes=120, total_marks=40,
               date=date(2023, 10, 2), instructions="Answer all questions.")
    db.add(p2); db.flush()

    # P2 Q1 — Pages 12-13 (idx 11-12)
    add_q(db, p2.id, exam_dir, 2, 1, "a",
        r"Expand and simplify $2(5p - 3q + 4) - 6(2p - 3)$.",
        2, "Algebra — Expansion", 12, (11, 0.04, 0.42),
        r"$$2(5p - 3q + 4) - 6(2p - 3) = 10p - 6q + 8 - 12p + 18 = -2p - 6q + 26$$", "M1, A1",
        topic_id=4)

    add_q(db, p2.id, exam_dir, 2, 1, "b",
        r"Solve the equation $\dfrac{3(2 - x)}{5} = \dfrac{x - 4}{2}$.",
        2, "Solving Linear Equations", 12, (11, 0.40, 0.95),
        r"""$$\frac{6 - 3x}{5} = \frac{x - 4}{2}$$
$$2(6 - 3x) = 5(x - 4)$$
$$12 - 6x = 5x - 20$$
$$11x = 32 \implies x = \frac{32}{11} = 2\frac{10}{11}$$""",
        "M1 for cross-multiply, A1",
        topic_id=5)

    add_q(db, p2.id, exam_dir, 2, 1, "ci",
        r"Express, in terms of $x$, the price of a pair of shirt.",
        1, "Algebra — Expression", 13, (12, 0.04, 0.40),
        r"Price of a shirt $= \$\!\left(10 + \dfrac{1}{2}x\right)$ or $\$\!\dfrac{x + 20}{2}$", "B1",
        stem=r"The price of a shirt is $\$10$ more than $\dfrac{1}{2}$ of the price of a pair of shoes. Ali paid a total of $\$413$ for 2 shirts and 5 pairs of shoes. By letting the price of a pair of shoes be $\$x$:",
        topic_id=5)

    add_q(db, p2.id, exam_dir, 2, 1, "cii",
        r"Form an equation in terms of $x$ and hence find the price of a shirt.",
        3, "Linear Equations — Word Problem", 13, (12, 0.38, 0.95),
        r"""$$2\!\left(10 + \frac{1}{2}x\right) + 5x = 413$$
$$20 + x + 5x = 413$$
$$6x = 393 \implies x = 65.50$$
Price of a shirt $= \$10 + \frac{1}{2}(65.50) = \$42.75$""",
        "M1 for equation, M1 for solving, A1",
        topic_id=5)

    # P2 Q2 — Page 14 (idx 13)
    add_q(db, p2.id, exam_dir, 2, 2, "a",
        r"Find the distance, in km, Randy travelled in the first 15 minutes.",
        2, "Speed, Distance, Time", 14, (13, 0.06, 0.38),
        r"Distance $= 20 \times \dfrac{15}{60} = 5$ km", "M1, A1",
        stem=r"Randy left home at 6.30 a.m. and headed for his school, which was 10 km away. After cycling for 15 minutes at a speed of 20 km/h, the bicycle broke down and Randy spent 20 minutes to fix the bicycle. He then continued the second part of the journey at a speed of 15 km/h.",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 2, "b",
        r"Find the time taken, in minutes, to travel the remaining journey.",
        2, "Speed, Distance, Time", 14, (13, 0.36, 0.62),
        r"""Remaining distance $= 10 - 5 = 5$ km
Time taken $= \dfrac{5}{15} = \dfrac{1}{3}$ hour $= 20$ minutes""",
        "M1, A1",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 2, "c",
        r"Calculate Randy's average speed for the whole journey from home to school.",
        2, "Average Speed", 14, (13, 0.60, 0.95),
        r"""Total time taken $= 15 + 20 + 20 = 55$ min
Average speed $= 10 \div \dfrac{55}{60} = 10\dfrac{10}{11}$ km/h or $\approx 10.9$ km/h""",
        "M1, A1",
        topic_id=9)

    # P2 Q3 — Page 15 (idx 14)
    add_q(db, p2.id, exam_dir, 2, 3, "a",
        r"Write down an expression for $T_5$ and evaluate it.",
        1, "Number Patterns", 15, (14, 0.04, 0.44),
        r"$T_5 = 6^2 - 5^2 = 36 - 25 = 11$", "B1",
        stem=r"The first four terms in a sequence of numbers are given below. $T_1 = 1^2 - 0^2 = 1$, $T_2 = 2^2 - 1^2 = 3$, $T_3 = 3^2 - 2^2 = 5$, $T_4 = 4^2 - 3^2 = 7$.",
        topic_id=7)

    add_q(db, p2.id, exam_dir, 2, 3, "b",
        r"Find an expression, in terms of $n$, for the $n$th term, $T_n$, of this sequence.",
        2, "Number Patterns — General Term", 15, (14, 0.42, 0.62),
        r"$T_n = n^2 - (n-1)^2 = n^2 - n^2 + 2n - 1 = 2n - 1$", "M1, A1",
        topic_id=7)

    add_q(db, p2.id, exam_dir, 2, 3, "c",
        r"Explain, with calculations, whether 120 is a term of this sequence.",
        2, "Number Patterns — Reasoning", 15, (14, 0.60, 0.95),
        r"""If $120 = 2n - 1$, then $n = \dfrac{121}{2} = 60.5$.
Since $n$ is not an integer, 120 is not a term of this sequence.
Or: This is a sequence of odd numbers. 120 is even and cannot be a term.""",
        "M1, A1",
        topic_id=7)

    # P2 Q4 — Page 16 (idx 15)
    add_q(db, p2.id, exam_dir, 2, 4, "a",
        r"Write down the equation of line $PQ$.",
        1, "Linear Functions — Vertical Line", 16, (15, 0.04, 0.52),
        r"$x = 2$", "B1",
        stem=r"The diagram shows three points $P(2, 6)$, $Q(2, 4)$ and $R(6, 2)$.",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 4, "b",
        r"Find the gradient of line $QR$.",
        1, "Gradient", 16, (15, 0.50, 0.68),
        r"Gradient $= \dfrac{2 - 4}{6 - 2} = \dfrac{-2}{4} = -\dfrac{1}{2}$", "B1",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 4, "c",
        r"The line $PR$ has an equation $y + x = 8$. A point $(4.25, a)$ lies on the line $PR$. Find the value of $a$.",
        1, "Linear Functions — Substitution", 16, (15, 0.66, 0.95),
        r"$a + 4.25 = 8 \implies a = 3.75$", "B1",
        topic_id=6)

    # P2 Q5 — Page 17 (idx 16)
    add_q(db, p2.id, exam_dir, 2, 5, "a",
        r"Calculate the value of $x$.",
        2, "Polygon Angles", 17, (16, 0.04, 0.50),
        r"""Each interior angle of pentagon $= \dfrac{180(5 - 2)}{5} = 108°$
Each interior angle of hexagon $= \dfrac{180(6 - 2)}{6} = 120°$
Angle $x = 360° - 108° - 120° = 132°$ (angles at a point)""",
        "M1, A1",
        stem=r"The diagram shows two regular polygons (a regular pentagon and a regular hexagon).",
        topic_id=11)

    add_q(db, p2.id, exam_dir, 2, 5, "b",
        r"Determine, with calculations, whether the angle $x°$ is the interior angle of another regular polygon.",
        3, "Polygon — Number of Sides", 17, (16, 0.48, 0.95),
        r"""Each exterior angle of polygon with angle $x = 180° - 132° = 48°$ (adj. angles on st. line).
Number of sides $= \dfrac{360°}{48°} = 7.5$.
Since the number of sides is not an integer, angle $x$ is not the interior angle of another regular polygon.""",
        "M1 for exterior angle, M1 for number of sides, A1",
        topic_id=11)

    # P2 Q6 — Page 18 (idx 17)
    add_q(db, p2.id, exam_dir, 2, 6, "a",
        r"Find the area of the shaded region.",
        3, "Area — Composite Shape", 18, (17, 0.04, 0.62),
        r"""Shaded Area $= 4(3) + \dfrac{1}{2}(5 + 11)(4) - \dfrac{1}{2}\pi(4)^2$
$= 12 + 32 - 8\pi \approx 18.9$ cm$^2$ (3 s.f.)""",
        "M1 for parallelogram, M1 for trapezium, M1 for semicircle, A1",
        stem=r"The shape is made from parallelogram $EFGH$ and a trapezium $DEHA$. $GE$ is perpendicular to $EF$ and a semicircle with radius $OC$ is cut out from it. $AB = 1.5$ cm, $OC = 4$ cm, $CD = 1.5$ cm, $DE = 5$ cm, $EF = 3$ cm, $FG = 5$ cm, $GE = 4$ cm and $HA = 5$ cm.",
        topic_id=12)

    add_q(db, p2.id, exam_dir, 2, 6, "b",
        r"Find the perimeter of the shaded region.",
        2, "Perimeter — Composite", 18, (17, 0.60, 0.95),
        r"""Perimeter $= 1.5 + \dfrac{1}{2}(2\pi)(4) + 1.5 + 5 + 3 + 5 + 3 + 5 \approx 36.6$ cm (3 s.f.)""",
        "M1, A1",
        topic_id=12)

    # P2 Q7 — Pages 19-20 (idx 18-19)
    add_q(db, p2.id, exam_dir, 2, 7, "a",
        r"Calculate the value of $p$.",
        1, "Linear Functions — Table", 19, (18, 0.04, 0.22),
        r"$p = 50 - 5(4) = 30$",
        "B1",
        stem=r"The volume $V$ cm$^3$, of an ice-cream at time $t$ minutes is given by $V = 50 - 5t$ for $0 \leq t \leq 10$. Some corresponding values of $V$ and $t$ are given in the table below.",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 7, "b",
        r"Using a scale of 1 cm to represent 1 unit, draw a horizontal $t$-axis for $0 \leq t \leq 10$. Using a scale of 1 cm to represent 5 units, draw a vertical $V$-axis for $0 \leq V \leq 50$. On your axes, plot the points given in the table and draw the line $V = 50 - 5t$ for $0 \leq t \leq 10$.",
        2, "Drawing Graphs", 19, (18, 0.20, 0.95),
        r"Correct scales, correct points plotted and a straight line drawn.", "B1 for scales/points, B1 for line",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 7, "c",
        r"State the gradient of the graph.",
        1, "Linear Graph — Gradient", 20, (19, 0.04, 0.12),
        r"Gradient $= -5$", "B1",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 7, "di",
        r"Find the volume of the ice cream after 2.6 minutes.",
        1, "Graph Reading", 20, (19, 0.10, 0.28),
        r"$V = 37$ cm$^3$ (accept 36 to 38 cm$^3$)", "B1",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 7, "dii",
        r"Find the time taken for the volume of the ice cream to be 17 cm$^3$.",
        1, "Graph Reading", 20, (19, 0.26, 0.42),
        r"$t = 6.6$ min (accept 6.5 to 6.7 min)", "B1",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 7, "e",
        r"Explain the meaning of the constant term 50, in the equation $V = 50 - 5t$.",
        1, "Linear Functions — Interpretation", 20, (19, 0.40, 0.58),
        r"Initial volume of the ice-cream is 50 cm$^3$.", "B1",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 7, "f",
        r"Explain why the function $V = 50 - 5t$ is not a good representation of the volume of the ice cream after 10 minutes.",
        1, "Linear Functions — Interpretation", 20, (19, 0.56, 0.82),
        r"Volume of ice-cream will be negative after 10 mins which is not possible. Or: It shows negative volume but in actual fact, all the ice-cream has melted.", "B1",
        topic_id=6)

    db.commit()
    p1_count = len(p1.questions)
    p2_count = len(p2.questions)
    print(f"Seeded Chung Cheng exam id={exam.id}: Section A ({p1_count} parts), Section B ({p2_count} parts)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
