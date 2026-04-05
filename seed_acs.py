"""Seed Anglo-Chinese School (Barker Road) EOY 2021 Sec 1 Express Math exam."""

import os
import shutil
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/Anglo-Chinese-School-SA2-2021-Sec-1-Math.pdf"
IMAGES_DIR = "/tmp/acs_pages"

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

    school = db.query(School).filter(School.name == "Anglo-Chinese School (Barker Road)").first()
    if not school:
        school = School(name="Anglo-Chinese School (Barker Road)")
        db.add(school)
        db.flush()

    # Check if already seeded
    existing = db.query(Exam).filter(Exam.school_id == school.id, Exam.year == 2021).first()
    if existing:
        print(f"ACS 2021 already seeded (id={existing.id}). Deleting and re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id,
        title="End-of-Year Examination 2021",
        year=2021,
        level="Secondary 1 Express",
        subject="Mathematics",
        source_pdf="Anglo-Chinese-School-SA2-2021-Sec-1-Math.pdf",
        status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════════════════════
    # PAPER 1 — Pages 2-10
    # ══════════════════════════════════════════════════════════════

    p1 = Paper(
        exam_id=exam.id, paper_number=1, duration_minutes=75, total_marks=50,
        date=date(2021, 10, 1),
        instructions="Answer all questions. If working is needed it must be shown with the answer.",
    )
    db.add(p1)
    db.flush()

    # Q1 — Page 2 (idx 1)
    add_q(db, p1.id, exam_dir, 1, 1, "a",
        r"Calculate $\dfrac{\sqrt{3.41}}{18.5 - 2.81^2}$. Write down the first 5 digits on your calculator display.",
        1, "Calculator Usage", 2, (1, 0.09, 0.24),
        r"$0.14190\ldots$ → $0.1419$", "B1",
        stem=r"", topic_id=3)

    add_q(db, p1.id, exam_dir, 1, 1, "b",
        r"Write your answer to part (a) correct to 3 decimal places.",
        1, "Decimal Places", 2, (1, 0.23, 0.30),
        r"$0.142$", "B1", topic_id=3)

    # Q2 — Page 2 (idx 1)
    add_q(db, p1.id, exam_dir, 1, 2, None,
        r"By rounding each number to 1 significant figure, estimate the value of $\dfrac{62.89 \times 8.93}{3.12}$. You must show your working.",
        2, "Estimation", 2, (1, 0.30, 0.56),
        r"$$\approx \frac{60 \times 9}{3} = 180$$", "M1, A1", topic_id=3)

    # Q3 — Page 2 (idx 1)
    add_q(db, p1.id, exam_dir, 1, 3, None,
        r"Simplify $4y - (13y - 5x)$.",
        2, "Simplifying Expressions", 2, (1, 0.56, 0.72),
        r"$5x - 9y$", "M1, A1", topic_id=4)

    # Q4 — Page 2 (idx 1)
    add_q(db, p1.id, exam_dir, 1, 4, None,
        r"Factorise completely $7a - 21ay$.",
        2, "Factorisation", 2, (1, 0.72, 0.92),
        r"$7a(1 - 3y)$", "M1, A1", topic_id=4)

    # Q5 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 5, None,
        r"Write these numbers in order of size, starting with the smallest: $\dfrac{3}{5}$, $0.75\%$, $\dfrac{\sqrt{3}}{2}$, $\dfrac{\pi}{4}$, $0.57$.",
        2, "Ordering Numbers", 3, (2, 0.05, 0.28),
        r"$0.75\%$, $0.57$, $\frac{3}{5}$, $\frac{\pi}{4}$, $\frac{\sqrt{3}}{2}$", "M1, A1", topic_id=2)

    # Q6 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 6, "a",
        r"all the prime numbers.",
        1, "Prime Numbers", 3, (2, 0.28, 0.41),
        r"$2, 5$", "B1",
        stem=r"From the list: $1$, $5$, $\pi$, $\dfrac{22}{7}$, $2$. List down:", topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 6, "b",
        r"all the rational numbers.",
        1, "Number Classification", 3, (2, 0.39, 0.48),
        r"$1, 2, 5, \frac{22}{7}$", "B1", topic_id=2)

    # Q7 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 7, None,
        r"In the diagram, $AB = 5$ cm, $BC = 7$ cm, $BE = 4$ cm. $BE$ is perpendicular to $AD$ and $BF$ is perpendicular to $DC$. Find $BF$.",
        2, "Area of Triangle", 3, (2, 0.47, 0.92),
        r"""Area of triangle $BCD = \frac{1}{2} \times 7 \times 4 = 28$ cm$^2$
$$BF = \frac{28 \times 2}{5} = \frac{28}{5} = 5.6 \text{ cm}$$""",
        "M1, A1", topic_id=12)

    # Q8 — Page 4 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 8, None,
        r"Express $\dfrac{5x}{3} - \dfrac{2x + y}{4}$ as a single fraction in its simplest form.",
        3, "Algebraic Fractions", 4, (3, 0.06, 0.44),
        r"$$\frac{20x - 3(2x + y)}{12} = \frac{20x - 6x - 3y}{12} = \frac{14x - 3y}{12}$$",
        "M1 for common denominator, M1 for expanding, A1", topic_id=4)

    # Q9 — Page 4 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 9, None,
        r"The price of a house at the end of 2019 was 9% higher than at the end of 2018. The price of the house at the end of 2020 was 9% lower than at the end of 2019. Jim says that the price of the house at the end of 2020 will be the same as that in 2018. Is he correct? Show your working to support your answer.",
        3, "Percentage", 4, (3, 0.43, 0.90),
        r"""Let $x$ be the price in 2018.
Price in 2019 $= 1.09x$
Price in 2020 $= 0.91(1.09x) = 0.9919x$
Jim is wrong — the price is lower.""",
        "M1 for 1.09x, M1 for 0.91(1.09x), A1", topic_id=8)

    # Q10 — Page 5 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 10, "a",
        r"Convert 72 km/h to m/s.",
        2, "Speed Conversion", 5, (4, 0.05, 0.22),
        r"$$72 \times \frac{1000}{3600} = 20 \text{ m/s}$$", "M1, A1", topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 10, "b",
        r"50 g of meat costs $x$ dollars. Find an expression, in dollars, for the cost of $y$ kg of meat.",
        2, "Algebraic Expression", 5, (4, 0.21, 0.43),
        r"""50 g $= 0.05$ kg costs $\$x$.
$y$ kg costs $\$\frac{xy}{0.05} = \$20xy$""",
        "M1, A1", topic_id=4)

    # Q11 — Page 5 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 11, None,
        r"Amy and Ben each have a savings account. The ratio of Amy's savings to Ben's savings $= 7 : 9$. They each spend $\$50$ from their savings. The new ratio of Amy's savings to Ben's savings $= 3 : 4$. Find how much money they have in total at the beginning.",
        4, "Ratio", 5, (4, 0.43, 0.90),
        r"""Original ratio $7 : 9$, New ratio $3 : 4 = 6 : 8$
Both spent 1 unit from original → 1 unit $= \$50$
Total $= (7 + 9) \times 50 = 16 \times 50 = \$800$""",
        "M1 for equivalent ratio, M1 for 1 unit, M1 for working, A1", topic_id=9)

    # Q12 — Page 6 (idx 5)
    add_q(db, p1.id, exam_dir, 1, 12, None,
        r"The figure below shows a large square $ABCD$ and a small square in the centre. There are 4 semi-circles and 4 quadrants each with a radius of 7 cm. Find the area of the shaded part as a percentage of the unshaded part. (Use $\pi = \frac{22}{7}$)",
        4, "Area — Composite Shapes", 6, (5, 0.06, 0.90),
        r"""Area of $ABCD = 28 \times 28 = 784$ cm$^2$
Small square $= 14 \times 14 = 196$ cm$^2$
Circles $= 3 \times \frac{22}{7} \times 7 \times 7 = 462$ cm$^2$
Shaded $= 784 - 196 - 462 = 126$ cm$^2$
Unshaded $= 784 - 126 = 658$ cm$^2$
Percentage $= \frac{126}{658} \times 100\% \approx 19\frac{1}{47}\%$""",
        "M1 for areas, M1 for shaded, M1 for percentage, A1", topic_id=12)

    # Q13 — Page 7 (idx 6)
    add_q(db, p1.id, exam_dir, 1, 13, "a",
        r"$r = q^2\left(\dfrac{1}{4} - p\right)$. Find the value of $r$ when $q = -2$ and $p = 3$.",
        1, "Substitution", 7, (6, 0.05, 0.34),
        r"$$r = (-2)^2\left(\frac{1}{4} - 3\right) = 4 \times \left(-\frac{11}{4}\right) = -11$$", "B1", topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 13, "b",
        r"I am thinking of a number $n$. 32 divided by the sum of $n$ and 3 gives me 8. What is the number?",
        3, "Linear Equation — Word Problem", 7, (6, 0.33, 0.88),
        r"""$$\frac{32}{n + 3} = 8$$
$$n + 3 = 4$$
$$n = 1$$""",
        "M1 for equation, M1 for solving, A1", topic_id=5)

    # Q14 — Page 8 (idx 7)
    add_q(db, p1.id, exam_dir, 1, 14, "a",
        r"Construct quadrilateral $ABCD$ such that $BC = 7$ cm, $AD = 6$ cm, angle $ABC = 80°$ and angle $BAD = 100°$. $AB$ has already been drawn below.",
        2, "Construction", 8, (7, 0.06, 0.56),
        r"Construction with compass arcs shown. $90° \pm 3°$, diagonal $BD = 9.6 \pm 0.2$ cm.",
        "B1 for correct angles, B1 for correct lengths", topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 14, "b",
        r"Measure and write down the length of the diagonal $BD$.",
        1, "Measurement", 8, (7, 0.56, 0.64),
        r"$BD = 9.6$ cm $(\pm 0.2$ cm$)$", "B1", topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 14, "c",
        r"Measure and write down the size of angle $ADC$.",
        1, "Measurement", 8, (7, 0.63, 0.72),
        r"Angle $ADC \approx 90° \pm 3°$", "B1", topic_id=10)

    # Q15 — Page 9 (idx 8)
    add_q(db, p1.id, exam_dir, 1, 15, "a",
        r"Complete these statements by calculating the size of each angle. Give a reason for each statement. Angle $BCD = $ ____°. Angle $BDF = $ ____°.",
        2, "Angle Properties — Parallel Lines", 9, (8, 0.06, 0.53),
        r"""Angle $BCD = 43°$ (corresponding angles, $BC \parallel FD$)
Angle $BDF = 57°$ (alternate angles, $BC \parallel FD$)""",
        "B1 with reason, B1 with reason",
        stem=r"In the diagram, $AB$ is parallel to $EDC$ and $BC$ is parallel to $FD$. Angle $CBD = 57°$, angle $EDF = 43°$ and angle $FAB = 99°$.", topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 15, "b",
        r"Calculate angle $AFD$.",
        2, "Angle Properties", 9, (8, 0.50, 0.68),
        r"""Angle $ABD = 180° - (43° + 57°) = 80°$
Angle $AFD = 360° - 99° - 57° - 80° = 124°$""",
        "M1, A1", topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 15, "c",
        r"John says that $AF$ is parallel to $BD$. Do you agree or disagree? You must show your calculations.",
        1, "Angle Properties", 9, (8, 0.67, 0.90),
        r"Disagree. Angle $FAB$ + angle $ABD = 99° + 80° = 179° \neq 180°$ (co-interior angles). So $AF$ is not parallel to $BD$.",
        "B1", topic_id=10)

    # Q16 — Page 10 (idx 9)
    add_q(db, p1.id, exam_dir, 1, 16, "a",
        r"How much does the company charge for rental of an electric bike for 35 hours?",
        1, "Reading Graphs", 10, (9, 0.50, 0.64),
        r"$\$80$", "B1",
        stem=r"The graph shows the charge imposed by a company for the rental of an electric bike. The charge depends on the number of hours of rental.", topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 16, "b",
        "Complete these sentences: The company charges a fixed cost of &#36;______ for rental of an electric bike up to ______ hours. Each additional hour costs &#36;______.",
        2, "Interpreting Graphs", 10, (9, 0.63, 0.79),
        r"Fixed cost $= \$40$, up to $15$ hours. Each additional hour costs $\$2$.", "B1, B1", topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 16, "c",
        r"Another company charges a rate of $\$4$ per hour, without any fixed cost. Draw on the same grid the graph representing this company's charging model.",
        1, "Drawing Graphs", 10, (9, 0.78, 0.86),
        r"Straight line through origin with gradient 4.", "B1", topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 16, "d",
        r"Both companies charge the same amount to rent an electric bike for ______ hours.",
        1, "Interpreting Graphs", 10, (9, 0.85, 0.92),
        r"$10$ hours", "B1", topic_id=6)

    # ══════════════════════════════════════════════════════════════
    # PAPER 2 — Pages 12-24
    # ══════════════════════════════════════════════════════════════

    p2 = Paper(
        exam_id=exam.id, paper_number=2, duration_minutes=75, total_marks=50,
        date=date(2021, 10, 1),
        instructions="Answer all questions. If the answer is not exact, give the answer to three significant figures.",
    )
    db.add(p2)
    db.flush()

    # P2 Q1 — Page 12 (idx 11)
    add_q(db, p2.id, exam_dir, 2, 1, "a",
        r"Express 90 as a product of its prime factors.",
        1, "Prime Factorisation", 12, (11, 0.10, 0.31),
        r"$90 = 2 \times 3^2 \times 5$", "B1",
        stem=r"Expressed as a product of its prime factors, $156 = 2^2 \times 3 \times 13$.", topic_id=1)

    add_q(db, p2.id, exam_dir, 2, 1, "b",
        r"Find the lowest common multiple of 90 and 156.",
        1, "LCM", 12, (11, 0.30, 0.49),
        r"$\text{LCM} = 2^2 \times 3^2 \times 5 \times 13 = 2340$", "B1", topic_id=1)

    add_q(db, p2.id, exam_dir, 2, 1, "c",
        r"The number $\sqrt{\dfrac{156}{k}}$ is a perfect square. Find $k$.",
        1, "Square Roots / Factors", 12, (11, 0.48, 0.66),
        r"""$$\frac{156}{k} = \frac{2^2 \times 3 \times 13}{k}$$
For perfect square: $k = 3 \times 13 = 39$""",
        "B1", topic_id=1)

    add_q(db, p2.id, exam_dir, 2, 1, "d",
        r"The highest common factor of 156 and $x$ is 26. $x$ is between 100 and 200. Find the smallest possible value of $x$.",
        2, "HCF", 12, (11, 0.64, 0.93),
        r"""$156 = 2^2 \times 3 \times 13$, $26 = 2 \times 13$
$x$ must be a multiple of 26 but NOT contain factor 3 or $2^2$.
$x = 2 \times 13 \times 5 = 130$""",
        "M1, A1", topic_id=1)

    # P2 Q2 — Page 13 (idx 12)
    add_q(db, p2.id, exam_dir, 2, 2, "a",
        r"Find the value of $p$.",
        1, "Linear Functions — Table", 13, (12, 0.07, 0.29),
        r"$p = 2$", "B1",
        stem=r"The variables $x$ and $y$ are connected by the equation $y + 2x = 4$. The table shows some corresponding values of $x$ and $y$: when $x = -1$, $y = 6$; when $x = 1$, $y = p$; when $x = 3$, $y = -2$.", topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 2, "b",
        r"On the axes, draw the graph of $y + 2x = 4$ for values of $x$ from $-1$ to $3$.",
        2, "Linear Functions — Graph", 13, (12, 0.28, 0.72),
        r"Straight line through $(-1, 6)$, $(1, 2)$, $(3, -2)$.", "B1 for points, B1 for line", topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 2, "ci",
        r"Write down the coordinates of the point where the line meets the $x$-axis.",
        1, "Linear Functions — Intercept", 13, (12, 0.72, 0.83),
        r"$(2, 0)$", "B1", topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 2, "cii",
        r"Find the value of $x$ when $y = -1$.",
        1, "Linear Functions — Reading Graph", 13, (12, 0.82, 0.92),
        r"$x = 2.5$", "B1", topic_id=6)

    # P2 Q3 — Page 14 (idx 13)
    add_q(db, p2.id, exam_dir, 2, 3, "a",
        r"Complete the table for Pattern 5: number of circles and number of unshaded circles.",
        1, "Number Patterns — Table", 14, (13, 0.07, 0.52),
        r"Number of circles: $1 + 4 + 4 + 4 + 4 + 4 = 21$. Number of unshaded circles: $17$.", "B1",
        stem=r"The diagram below shows a series of patterns made using shaded and unshaded circles.", topic_id=7)

    add_q(db, p2.id, exam_dir, 2, 3, "b",
        r"Write down an expression, in terms of $n$, for the number of circles in Pattern $n$.",
        1, "Number Patterns — General Term", 14, (13, 0.51, 0.65),
        r"$1 + 4n$", "B1", topic_id=7)

    add_q(db, p2.id, exam_dir, 2, 3, "c",
        r"Explain why the number of circles in the sequence is always odd.",
        1, "Number Patterns — Reasoning", 14, (13, 0.63, 0.78),
        r"For any value of $n$, $4n$ is always even. Adding 1 to an even number always gives an odd number. Hence the number of circles is always odd.",
        "B1", topic_id=7)

    add_q(db, p2.id, exam_dir, 2, 3, "d",
        r"Would there be a pattern where there are 178 unshaded circles? Show your working clearly.",
        2, "Number Patterns — Reasoning", 14, (13, 0.77, 0.93),
        r"""$(1 + 4n) - 4 = 178$
$4n = 181$
$n = 45.25$
No, there will not be a pattern with 178 unshaded circles since $n$ is not a whole number.""",
        "M1, A1", topic_id=7)

    # P2 Q4 — Page 15 (idx 14)
    add_q(db, p2.id, exam_dir, 2, 4, "ai",
        r"angle $ABC$.",
        2, "Polygon Angles — Interior", 15, (14, 0.06, 0.49),
        r"$$\text{Interior angle} = \frac{(10 - 2) \times 180°}{10} = 144°$$", "M1, A1",
        stem=r"$JABCD$ shows part of a regular ten-sided polygon. $O$ is the centre of the polygon. Find:", topic_id=11)

    add_q(db, p2.id, exam_dir, 2, 4, "aii",
        r"angle $AOJ$.",
        1, "Polygon Angles — Central", 15, (14, 0.48, 0.64),
        r"$$\frac{360°}{10} = 36°$$", "B1", topic_id=11)

    add_q(db, p2.id, exam_dir, 2, 4, "aiii",
        r"angle $CAJ$.",
        2, "Polygon Angles", 15, (14, 0.62, 0.88),
        r"""Angle $BAC = \frac{180° - 144°}{2} = 18°$
Angle $CAJ = 144° - 18° = 126°$""",
        "M1, A1", topic_id=11)

    # P2 Q5 — Pages 16-17 (idx 15-16)
    add_q(db, p2.id, exam_dir, 2, 5, "a",
        r"Show that the area of the cross-section $ABCD$ is 24 cm$^2$.",
        1, "Area — Trapezium", 16, (15, 0.06, 0.60),
        r"$$\text{Area} = \frac{1}{2}(3 + 9)(4) = 24 \text{ cm}^2$$", "B1",
        stem=r"The figure shows a solid prism with a uniform cross-section $ABCD$ in the shape of a trapezium. $AB = 3$ cm, $BC = 5$ cm, $AD = 5$ cm, $CD = 9$ cm, length $= 7$ cm.", topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 5, "b",
        r"Calculate the volume of the prism.",
        1, "Volume — Prism", 16, (15, 0.58, 0.92),
        r"$$V = 24 \times 7 = 168 \text{ cm}^3$$", "B1", topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 5, "c",
        r"Calculate the total surface area of the prism.",
        3, "Surface Area — Prism", 17, (16, 0.05, 0.88),
        r"""$$\text{Two trapeziums} = 2 \times 24 = 48 \text{ cm}^2$$
$$\text{Rectangles} = (3 + 5 + 9 + 5) \times 7 = 154 \text{ cm}^2$$
$$\text{Total} = 48 + 154 = 202 \text{ cm}^2$$""",
        "M1 for trapezium faces, M1 for rectangles, A1", topic_id=13)

    # P2 Q6 — Page 18 (idx 17)
    add_q(db, p2.id, exam_dir, 2, 6, "a",
        r"Train $A$ had travelled $x$ km when it reached Junction $X$. Write down, in terms of $x$, the time taken for Train $A$ to travel from its station to Junction $X$.",
        1, "Speed — Expression", 18, (17, 0.06, 0.38),
        r"$\dfrac{x}{70}$ hours", "B1",
        stem=r"Two trains, $A$ and $B$, left their respective stations and travelled at a constant speed in opposite directions, on parallel tracks. Train $A$ travelled at 70 km/h while Train $B$ travelled at 85 km/h. At a certain point in time, both trains pass each other at Junction $X$.", topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 6, "b",
        r"Train $B$ had travelled 45 km more than Train $A$ when it reached Junction $X$. Write down, in terms of $x$, the time taken for Train $B$ to travel from its station to Junction $X$.",
        1, "Speed — Expression", 18, (17, 0.37, 0.52),
        r"$\dfrac{x + 45}{85}$ hours", "B1", topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 6, "c",
        r"Hence or otherwise, form an equation in $x$ and solve it.",
        3, "Speed — Equation", 18, (17, 0.50, 0.77),
        r"""$$\frac{x}{70} = \frac{x + 45}{85}$$
$$85x = 70(x + 45)$$
$$85x = 70x + 3150$$
$$15x = 3150 \implies x = 210$$""",
        "M1 for equation, M1 for cross-multiply, A1", topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 6, "d",
        r"Find the distance between the two stations.",
        1, "Speed — Distance", 18, (17, 0.76, 0.92),
        r"Total distance $= 210 + (210 + 45) = 465$ km", "B1", topic_id=9)

    # P2 Q7 — Pages 19-20 (idx 18-19)
    add_q(db, p2.id, exam_dir, 2, 7, "ai",
        r"Jenny bought a handbag in Hong Kong for HKD 350. Calculate the cost in SGD.",
        2, "Foreign Exchange", 19, (18, 0.28, 0.55),
        r"""HKD 1 $= \frac{1}{100} \times 17.1850 =$ SGD $0.171850$
HKD 350 $= 350 \times 0.171850 =$ SGD $60.15$""",
        "M1, A1",
        stem=r"The following table shows various foreign exchange rates, against the Singapore Dollar (SGD). 1 USD = 1.3409 SGD, 1 AUD = 0.9848 SGD, 100 JPY = 1.2175 SGD, 100 HKD = 17.1850 SGD.", topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 7, "aii",
        r"A tourist from Australia bought a bag for SGD $\$294.35$. The amount paid included a commission of 1.5% because the tourist paid in AUD. What was the price of the bag in AUD, excluding the commission, correct to the nearest dollar?",
        2, "Foreign Exchange + Percentage", 19, (18, 0.55, 0.92),
        r"""SGD $290$ (before commission)
Cost in AUD $= \frac{290}{0.9848} = 294.48 \approx$ AUD $294$""",
        "M1, A1", topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 7, "b",
        r"Jim puts a certain amount of money into a savings account paying simple interest of 2% per annum. At the end of 2 years, the total amount of money in his account is $\$3120$. Find the amount of money that Jim put into the account.",
        2, "Simple Interest", 20, (19, 0.06, 0.66),
        r"""$$3120 = P + \frac{P \times 2 \times 2}{100}$$
$$3120 = P + 0.04P = 1.04P$$
$$P = \$3000$$""",
        "M1, A1", topic_id=8)

    # P2 Q8 — Pages 21-22 (idx 20-21)
    add_q(db, p2.id, exam_dir, 2, 8, "ai",
        r"Write down the coordinates of point $D$.",
        1, "Coordinate Geometry — Symmetry", 21, (20, 0.06, 0.62),
        r"$(6, 3)$", "B1",
        stem=r"The diagram shows a triangle $ABC$. $A$, $B$ and $C$ are the points $(3, 7)$, $(0, 3)$ and $(3, 1)$ respectively. The quadrilateral $ABCD$ is symmetrical about the line $AC$.", topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 8, "aii",
        r"Find the area of the quadrilateral $ABCD$.",
        2, "Area — Coordinate Geometry", 21, (20, 0.60, 0.88),
        r"""$$\text{Area of } \triangle ABC = \frac{1}{2} \times 6 \times 3 = 9$$
$$\text{Area of } ABCD = 9 \times 2 = 18 \text{ unit}^2$$""",
        "M1, A1", topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 8, "aiii",
        r"What is the special name given to this quadrilateral?",
        1, "Quadrilateral Properties", 22, (21, 0.06, 0.19),
        r"Kite", "B1", topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 8, "bi",
        r"Find the gradient of the line $AB$.",
        1, "Gradient", 22, (21, 0.19, 0.38),
        r"Gradient $= \dfrac{7 - 3}{3 - 0} = \dfrac{4}{3}$", "B1", topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 8, "bii",
        r"Write down the equation of the line $AB$.",
        2, "Linear Equation of Line", 22, (21, 0.37, 0.74),
        r"$y = \dfrac{4}{3}x + 3$", "M1, A1", topic_id=6)

    # P2 Q9 — Pages 23-24 (idx 22-23)
    add_q(db, p2.id, exam_dir, 2, 9, "a",
        r"Calculate the amount that Jeremy pays for petrol in a year.",
        2, "Rate — Cost Calculation", 23, (22, 0.06, 0.70),
        r"""Litres per year $= \frac{11\,000}{11} = 1000$ L
Cost $= 1000 \times \$2.49 = \$2490$""",
        "M1, A1",
        stem=r"Jeremy owns a car of engine capacity 1599 cc. He drives on average about 11,000 km per year. His car travels 11 km on every litre of petrol. Cost: cc < 1000 → $\$2.47$/L, $1000 \le$ cc $< 1600$ → $\$2.49$/L, cc $> 1600$ → $\$2.58$/L.", topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 9, "b",
        r"Jeremy estimates additional yearly costs: Car Insurance $\$1650$ (before 40% NCD), ERP $\$920$, Servicing + Road Tax $\$2000$, Parking $\$2640$. Without a car, monthly costs: MRT $\$50$, Bus $\$55$, Taxis $\$375$. Would it be cheaper for Jeremy to use other transport instead of his car? Show working to support your answer.",
        4, "Rate — Comparison", 24, (23, 0.06, 0.90),
        r"""Car costs per year:
Petrol $= \$2490$
Insurance $= 1650 \times 0.6 = \$990$
ERP $= \$920$, Servicing $= \$2000$, Parking $= \$2640$
Total car $= 2490 + 990 + 920 + 2000 + 2640 = \$9040$

Public transport per year:
$(50 + 55 + 375) \times 12 = 480 \times 12 = \$5760$

Yes, it would be cheaper to use other transport ($\$5760 < \$9040$).""",
        "M1 for insurance, M1 for car total, M1 for transport total, A1", topic_id=9)

    db.commit()
    p1_count = len(p1.questions)
    p2_count = len(p2.questions)
    print(f"Seeded ACS exam id={exam.id}: Paper 1 ({p1_count} parts), Paper 2 ({p2_count} parts)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
