"""Seed Bedok View Secondary School SA2 2020 Sec 1 Express Math exam."""

import os
import shutil
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/66a8babe54758_3601.pdf"
IMAGES_DIR = "/tmp/bedokview_pages"

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

    school = db.query(School).filter(School.name == "Bedok View Secondary School").first()
    if not school:
        school = School(name="Bedok View Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(Exam.school_id == school.id, Exam.year == 2020).first()
    if existing:
        print(f"Bedok View 2020 already seeded (id={existing.id}). Deleting and re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id, title="SA2 / End-of-Year Examination 2020", year=2020,
        level="Secondary 1 Express", subject="Mathematics",
        source_pdf="66a8babe54758_3601.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # PAPER 1 — Pages 3-11 (idx 2-10), 50 marks, 1 hour 15 min
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=75, total_marks=50,
               date=date(2020, 10, 2), instructions="Answer all questions.")
    db.add(p1); db.flush()

    # Q1 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 1, "ai",
        r"Express the following numbers correct to 2 significant figures: $0.003928$",
        1, "Approximation / Significant Figures", 3, (2, 0.07, 0.20),
        r"$0.0039$", "B1",
        topic_id=3)

    add_q(db, p1.id, exam_dir, 1, 1, "aii",
        r"Express the following numbers correct to 2 significant figures: $5919$",
        1, "Approximation / Significant Figures", 3, (2, 0.19, 0.30),
        r"$5900$", "B1",
        topic_id=3)

    add_q(db, p1.id, exam_dir, 1, 1, "bi",
        r"Write down the greatest possible number of visitor arrivals.",
        1, "Rounding — Upper Bound", 3, (2, 0.30, 0.52),
        r"$270\,349$", "B1",
        stem=r"In 2019, there were approximately $270\,300$ visitor arrivals to Universal Studios Singapore (USS). This value has been rounded to 4 significant figures.",
        topic_id=3)

    add_q(db, p1.id, exam_dir, 1, 1, "bii",
        r"Write down the least possible number of visitor arrivals.",
        1, "Rounding — Lower Bound", 3, (2, 0.52, 0.63),
        r"$270\,250$", "B1",
        topic_id=3)

    # Q2 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 2, "a",
        r"Express $1386$ as a product of its prime factors.",
        2, "Prime Factorisation", 3, (2, 0.65, 0.82),
        r"$1386 = 2 \times 3^2 \times 7 \times 11$", "M1, A1",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 2, "b",
        r"Find the smallest positive integer $k$ such that $1386k$ is a perfect cube.",
        1, "Perfect Cube", 3, (2, 0.82, 0.91),
        r"$k = 2^2 \times 3 \times 7^2 \times 11^2 = 71\,148$", "B1",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 2, "c",
        r"Find the smallest positive integer $k$ such that $\dfrac{1386}{k}$ is a perfect square.",
        1, "Perfect Square", 3, (2, 0.91, 0.98),
        r"$k = 2 \times 7 \times 11 = 154$", "B1",
        topic_id=1)

    # Q3 — Page 4 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 3, "a",
        r"When is the next time that the bells of both schools go off at the same time?",
        2, "LCM — Word Problem", 4, (3, 0.05, 0.42),
        r"""$35 = 5 \times 7$, $40 = 2^3 \times 5$
LCM of $35$ and $40 = 2^3 \times 5 \times 7 = 280$ minutes $= 4$ hr $40$ min
$07\,25 + 4$ hr $40$ min $= 12\,05$""",
        "M1 for LCM, A1",
        stem=r"The school bell of Bedok East School goes off every 35 minutes while the school bell of Bedok West School goes off every 40 minutes. The first bell of both schools goes off at 07 25.",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 3, "b",
        r"If Bedok East School has 11 periods including recess on Monday and Bedok West School has 10 periods including recess on Monday, pupils of which school are dismissed earlier on Monday? How much earlier?",
        2, "Time Calculation", 4, (3, 0.42, 0.85),
        r"""Bedok East: $11 \times 35 = 385$ min $= 6$ hr $25$ min
Bedok West: $10 \times 40 = 400$ min $= 6$ hr $40$ min
$6$ hr $40$ min $- 6$ hr $25$ min $= 15$ min
Bedok East is earlier by 15 min.""",
        "M1 for both times, A1",
        topic_id=9)

    # Q4 — Page 5 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 4, "a",
        r"Showing your working clearly, find the value of $\left[\dfrac{5}{6} - \left(-\dfrac{2}{3}\right)\right] \div \left(\dfrac{2}{3}\right)^2$ without using a calculator.",
        2, "Order of Operations — Fractions", 5, (4, 0.05, 0.35),
        r"""$$= \left[\frac{5}{6} + \frac{2}{3}\right] \div \frac{4}{9} = \frac{3}{2} \times \frac{9}{4} = \frac{27}{8} = 3\frac{3}{8}$$""",
        "M1, A1",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 4, "bi",
        r"Represent the numbers $-\dfrac{3}{2}$, $2.7$, $-3$ and $0.5$ on a number line.",
        2, "Number Line", 5, (4, 0.35, 0.72),
        r"Number line with arrows at both ends, lines to indicate each value position for $-3$, $-\frac{3}{2}$, $0.5$, $2.7$.", "B1 for proper number line, B1 for all 4 values",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 4, "bii",
        r"Hence, arrange the numbers in part (b)(i) in descending order.",
        1, "Ordering Numbers", 5, (4, 0.72, 0.85),
        r"$2.7, 0.5, -\dfrac{3}{2}, -3$", "B1",
        topic_id=2)

    # Q5 — Page 6 (idx 5)
    add_q(db, p1.id, exam_dir, 1, 5, "a",
        r"Express the distance, in km, between Town $A$ and Town $B$ in terms of $x$.",
        1, "Speed, Distance, Time — Expression", 6, (5, 0.05, 0.28),
        r"$35x$ km", "B1",
        stem=r"Iman cycled from Town $A$ to Town $B$ in $x$ hours at an average speed of 35 km/h. On his return journey, he increased his speed by 25%. The time taken for the return journey was shorter by 30 minutes.",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 5, "b",
        r"Express the time taken, in hours, for the return journey.",
        1, "Speed, Distance, Time — Expression", 6, (5, 0.28, 0.50),
        r"$\left(x - \dfrac{1}{2}\right)$ hrs", "B1",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 5, "c",
        r"Form an equation in terms of $x$ and find the time taken for Iman to travel from Town $A$ to Town $B$.",
        3, "Speed, Distance, Time — Equation", 6, (5, 0.50, 0.90),
        r"""$$\frac{125}{100} \times 35 \times \left(x - \frac{1}{2}\right) = 35x$$
$$\frac{175}{4}\left(x - \frac{1}{2}\right) = 35x$$
$$\frac{35x}{4} = \frac{175}{8}$$
$$x = 2.5 \text{ hours}$$""",
        "M1 for equation, M1 for solving, A1",
        topic_id=9)

    # Q6 — Page 7 (idx 6)
    add_q(db, p1.id, exam_dir, 1, 6, "a",
        r"The result of a number, when increased by 40%, is 126. Find the number.",
        2, "Percentage — Reverse", 7, (6, 0.05, 0.24),
        r"$$\frac{140}{100} \times x = 126 \implies x = \frac{126 \times 100}{140} = 90$$", "M1, A1",
        topic_id=8)

    add_q(db, p1.id, exam_dir, 1, 6, "b",
        r"A fruit seller bought 200 pears for $\$80$. Upon closer examination, he discovered that some of the pears were rotten and had to be discarded. The fruit seller sold the remaining pears at 50 cents each and made a profit of $\$12$. Calculate the percentage of pears that were discarded.",
        3, "Percentage — Profit/Loss", 7, (6, 0.24, 0.62),
        r"""Let the number of pears discarded be $x$.
$0.5(200 - x) - 80 = 12$
$100 - 0.5x = 92$
$0.5x = 8$, $x = 16$
Percentage discarded $= \frac{16}{200} \times 100\% = 8\%$""",
        "M1 for equation, M1 for solving, A1",
        topic_id=8)

    add_q(db, p1.id, exam_dir, 1, 6, "c",
        r"A watch is priced at $\euro 430$ in Paris. Calculate how much Germaine needs to pay in SGD (S$\$$) if the exchange rate is S$$\$1 = \euro\,0.6368$.",
        2, "Currency Conversion", 7, (6, 0.62, 0.88),
        r"""S$$\$1 = \euro\,0.6368$
S$$\$ = \frac{430}{0.6368} = \$\$675.25$ (2 d.p.)""",
        "M1, A1",
        topic_id=8)

    # Q7 — Page 8 (idx 7)
    add_q(db, p1.id, exam_dir, 1, 7, "a",
        r"Draw and label triangle $ABC$ such that $AB = 7.9$ cm, $\angle BAC = 48°$ and $AC = 4.8$ cm.",
        2, "Construction", 8, (7, 0.05, 0.18),
        r"Triangle $ABC$ with $AB$, $AC$ and $\angle BAC$ correct (all 3). B1 for any 2 correct dimensions.", "B2 for all correct, B1 for any 2",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 7, "b",
        r"Measure and write down the length of $BC$.",
        1, "Construction — Measurement", 8, (7, 0.88, 0.93),
        r"$BC = 5.9 \pm 0.1$ cm", "B1",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 7, "c",
        r"Measure and write down the size of $\angle ACB$.",
        1, "Construction — Measurement", 8, (7, 0.93, 0.98),
        r"$\angle ACB = 84° \pm 1°$", "B1",
        topic_id=10)

    # Q8 — Page 9 (idx 8)
    add_q(db, p1.id, exam_dir, 1, 8, "ai",
        r"Find an expression, in terms of $n$, for the $n$th term, $T_n$, of the sequence.",
        2, "Number Patterns — General Term", 9, (8, 0.05, 0.23),
        r"$T_n = 53 - 6(n - 1) = 59 - 6n$", "M1, A1",
        stem=r"The first four terms in a sequence are $53, 47, 41, 35$.",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 8, "aii",
        r"Explain why it is not possible for a term in the sequence to be a multiple of 2.",
        1, "Number Patterns — Reasoning", 9, (8, 0.23, 0.38),
        r"The terms are all odd numbers and will never be a multiple of 2.", "B1",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 8, "bi",
        r"Use the formula to find $T_9$.",
        1, "Number Patterns — Substitution", 9, (8, 0.38, 0.55),
        r"$T_9 = \dfrac{3(9) + 6}{150 - 4(9)} = \dfrac{33}{114} = \dfrac{11}{38}$", "B1",
        stem=r"The $n$th term of another sequence is given by $T_n = \dfrac{3n + 6}{150 - 4n}$.",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 8, "bii",
        r"The value of $T_k$ can be simplified to $\dfrac{17}{30}$. Find the value of $k$.",
        2, "Number Patterns — Equation", 9, (8, 0.55, 0.75),
        r"""$$\frac{3k + 6}{150 - 4k} = \frac{17}{30}$$
$$30(3k + 6) = 17(150 - 4k)$$
$$90k + 180 = 2550 - 68k$$
$$158k = 2370$$
$$k = 15$$""",
        "M1, A1",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 8, "biii",
        r"Suggest a value of $n$ such that the value of $T_n$ is greater than 1.",
        1, "Number Patterns — Inequality", 9, (8, 0.75, 0.90),
        r"Accept any number 21 and above (since $\frac{3n+6}{150-4n} > 1 \implies 7n > 144 \implies n > 20.57$).", "B1",
        topic_id=7)

    # Q9 — Page 10 (idx 9)
    add_q(db, p1.id, exam_dir, 1, 9, None,
        r"Find the values of $x$, $y$ and $z$ in the following diagram, stating your reasons clearly.",
        5, "Angle Properties — Parallel Lines", 10, (9, 0.05, 0.95),
        r"""$\angle x = 180° - 130° = 50°$ (co-interior angles)
$\angle y = \angle x = 50°$ (alternate angles)
$\angle z = 24° + 50° = 74°$ (exterior angle of triangle or alternate angles)""",
        "M1 A1 for x, B1 for y, M1 A1 for z",
        stem=r"In the diagram, $PQ \parallel RS \parallel TU$. Various angles are shown including $24°$ and $130°$.",
        topic_id=10)

    # Q10 — Page 11 (idx 10)
    add_q(db, p1.id, exam_dir, 1, 10, "a",
        r"Complete the table below.",
        2, "Statistics — Tally & Frequency", 11, (10, 0.05, 0.62),
        r"""Chocolate: 6, Vanilla: 5, Strawberry: 9, Mango: 10""",
        "B2 for all 4 correct, B1 for 3 correct",
        stem=r"An ice-cream company conducted a survey on 30 people to determine the preferred ice-cream flavour. The flavours listed were Chocolate (C), Vanilla (V), Strawberry (S) and Mango (M).",
        topic_id=14)

    add_q(db, p1.id, exam_dir, 1, 10, "b",
        r"Write down the flavour that is the most popular.",
        1, "Statistics — Mode", 11, (10, 0.62, 0.73),
        r"Mango", "B1",
        topic_id=14)

    add_q(db, p1.id, exam_dir, 1, 10, "c",
        r"If the survey findings were represented using a pie chart, calculate the angle of the sector that represents the people who preferred Vanilla flavour for their ice-cream.",
        2, "Statistics — Pie Chart", 11, (10, 0.73, 0.93),
        r"$$\text{Vanilla} = \frac{5}{30} \times 360° = 60°$$", "M1, A1",
        topic_id=14)

    # ══════════════════════════════════════════════
    # PAPER 2 — Pages 3-6 (idx 12-15), 50 marks, 1h30m
    # ══════════════════════════════════════════════
    p2 = Paper(exam_id=exam.id, paper_number=2, duration_minutes=90, total_marks=50,
               date=date(2020, 10, 7), instructions="Answer all questions.")
    db.add(p2); db.flush()

    # P2 Q1 — Page 3 (idx 12)
    add_q(db, p2.id, exam_dir, 2, 1, "a",
        r"Simplify $-3[7y + 2(-3x)] - 2(x - 3y)$.",
        2, "Algebra — Expansion", 3, (12, 0.07, 0.17),
        r"""$$= -3[7y - 6x] - 2x + 6y$$
$$= -21y + 18x - 2x + 6y$$
$$= 16x - 15y$$""",
        "M1, A1",
        topic_id=4)

    add_q(db, p2.id, exam_dir, 2, 1, "b",
        r"Express $\dfrac{3(2y - x)}{9} - \dfrac{7(7x - 4y)}{45}$ as a single fraction in its simplest form.",
        3, "Algebra — Fractions", 3, (12, 0.17, 0.33),
        r"""$$= \frac{5(6y - 3x) - (49x - 28y)}{45}$$
$$= \frac{30y - 15x - 49x + 28y}{45}$$
$$= \frac{-64x + 58y}{45}$$""",
        "M1 for LCD, M1 for expanding, A1",
        topic_id=4)

    add_q(db, p2.id, exam_dir, 2, 1, "ci",
        r"$3yz - 9x$",
        2, "Algebra — Substitution", 3, (12, 0.33, 0.47),
        r"""$$= 3\left(\frac{1}{4}\right)(9) - 9(-4)$$
$$= \frac{27}{4} + 36 = 42\frac{3}{4}$$""",
        "M1, A1",
        stem=r"Given that $x = -4$, $y = \dfrac{1}{4}$ and $z = 9$, find the value of:",
        topic_id=4)

    add_q(db, p2.id, exam_dir, 2, 1, "cii",
        r"$\dfrac{x^2}{y^2} - \dfrac{1}{z}$",
        2, "Algebra — Substitution", 3, (12, 0.47, 0.65),
        r"""$$= \frac{(-4)^2}{\left(\frac{1}{4}\right)^2} - \frac{1}{9} = \frac{16}{\frac{1}{16}} - \frac{1}{9} = 256 - \frac{1}{9} = 255\frac{8}{9}$$""",
        "M1, A1",
        topic_id=4)

    # P2 Q2 — Page 3 (idx 12)
    add_q(db, p2.id, exam_dir, 2, 2, "a",
        r"Calculate $\dfrac{(-48.1)^3}{\sqrt[3]{28 \times 0.876}}$. Write down the first five digits on your calculator display.",
        1, "Calculator Usage", 3, (12, 0.66, 0.75),
        r"$869.76$ (accept first 5 digits from display)", "B1",
        topic_id=3)

    add_q(db, p2.id, exam_dir, 2, 2, "b",
        r"Write your answer to part (a) correct to 3 significant figures.",
        1, "Significant Figures", 3, (12, 0.75, 0.80),
        r"$870$ (3 s.f.)", "B1",
        topic_id=3)

    add_q(db, p2.id, exam_dir, 2, 2, "ci",
        r"Find an expression, in terms of $x$, for the perimeter of triangle $ABC$.",
        1, "Algebra — Perimeter Expression", 3, (12, 0.80, 0.90),
        r"Perimeter $= (5x - 7) + (4x + 3) + (9x - 9) = (18x - 13)$ cm", "B1",
        stem=r"Figure $ABC$ below is a triangle. $AB = (5x - 7)$ cm, $AC = (4x + 3)$ cm and $BC = (9x - 9)$ cm.",
        topic_id=4)

    add_q(db, p2.id, exam_dir, 2, 2, "cii",
        r"The perimeter of triangle $ABC$ is 41 cm. Form an equation in terms of $x$ and solve it.",
        2, "Linear Equations", 3, (12, 0.90, 0.96),
        r"""$$18x - 13 = 41$$
$$18x = 54$$
$$x = 3$$""",
        "M1, A1",
        topic_id=5)

    add_q(db, p2.id, exam_dir, 2, 2, "ciii",
        r"Find the length of the longest side of the triangle.",
        1, "Algebra — Substitution", 3, (12, 0.96, 0.99),
        r"$(4 \times 3) + 3 = 15$ cm, $(5 \times 3) - 7 = 8$ cm, $(9 \times 3) - 9 = 18$ cm. Longest side $= 18$ cm.", "B1",
        topic_id=4)

    # P2 Q3 — Page 4 (idx 13)
    add_q(db, p2.id, exam_dir, 2, 3, "a",
        r"Find the shaded cross-sectional area $ABCDHGFE$.",
        3, "Area — Composite Shape", 4, (13, 0.05, 0.65),
        r"""Area of big trapezium $ABCD = \frac{1}{2}(25 + 40) \times 28 = 910$ cm$^2$
Area of small trapezium $EFGH = \frac{1}{2}(16 + 30) \times 18 = 414$ cm$^2$
Cross-sectional area $= 910 - 414 = 496$ cm$^2$""",
        "M1 for each trapezium, A1",
        stem=r"The figure below shows a stool. $AD = 40$ cm, $EH = 30$ cm, $BC = 25$ cm and $FG = 16$ cm. The distances of $BC$ and $FG$ from the ground are 28 cm and 18 cm respectively.",
        topic_id=12)

    add_q(db, p2.id, exam_dir, 2, 3, "b",
        r"Given that the length of $BJ$ is 62 cm, find the volume of the stool, assuming the stool is a solid.",
        2, "Volume — Prism", 4, (13, 0.65, 0.82),
        r"Volume $= 496 \times 62 = 30\,752$ cm$^3$", "M1, A1",
        topic_id=13)

    # P2 Q4 — Page 5 (idx 14)
    add_q(db, p2.id, exam_dir, 2, 4, "a",
        r"Find the volume of the solid.",
        3, "Volume — Composite Solid", 5, (14, 0.05, 0.38),
        r"""Volume of cuboid $= 14 \times 6 \times \frac{2}{3} \times 9 = 504$ cm$^3$
Volume of 2 cylinders $= 2 \times \pi \times 4^2 \times 9 = 904.8$ cm$^3$
Total volume $= 504 + 904.8 \approx 1410$ cm$^3$ (3 s.f.)""",
        "M1 for cuboid, M1 for cylinders, A1",
        stem=r"A solid is formed by mounting 2 identical cylinders on a rectangular prism as shown. The cylinders have a radius of 4 cm and a height of 9 cm. The cuboid is 14 cm long, 6 cm wide and has a height that is $\frac{2}{3}$ the height of the cylinder.",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 4, "b",
        r"Find the total surface area of the solid.",
        3, "Surface Area — Composite Solid", 5, (14, 0.38, 0.56),
        r"""Surface area of 2 cylinders: $2 \times 2\pi(4)(9) + 2 \times \pi(4)^2 = 144\pi + 32\pi$... (cancelled)
Surface area of rectangular prism (adjusted)...
Total $\approx 860$ cm$^2$ (3 s.f.)""",
        "M1 for cylinders, M1 for prism, A1",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 4, "c",
        r"The solid is melted down to form a cube. Find the length of each side of the cube.",
        2, "Volume — Cube", 5, (14, 0.56, 0.68),
        r"$$x^3 = 1408.78 \implies x = \sqrt[3]{1408.78} = 11.2 \text{ cm (3 s.f.)}$$", "M1, A1",
        topic_id=13)

    # P2 Q5 — Page 5 (idx 14)
    add_q(db, p2.id, exam_dir, 2, 5, "ai",
        r"There is a service charge of 10% and GST is at 7%. Calculate the total cost of the meal.",
        2, "Percentage — GST & Service Charge", 5, (14, 0.68, 0.82),
        r"""Total $= \$11.50 + \$8.80 + \$7.90 + \$9.20 + \$6.30 = \$43.70$
With 10% service charge: $1.1 \times 43.70 = \$48.07$
With 7% GST: $1.07 \times 48.07 = \$51.43$ (2 d.p.)""",
        "M1 for service charge, A1",
        stem=r"Part of a restaurant bill is shown below: Pineapple rice $\$11.50$, Stir-fried chicken with basil $\$8.80$, Green papaya salad $\$7.90$, Green curry $\$9.20$, Thai fish cakes $\$6.30$.",
        topic_id=8)

    add_q(db, p2.id, exam_dir, 2, 5, "aii",
        r"The restaurant does not impose a service charge for takeout. Mr Ho says he could have saved 10% of the total cost obtained in part (a) if he chose to do a takeout instead. Is he correct? Explain your answer.",
        2, "Percentage — Comparison", 5, (14, 0.82, 0.94),
        r"""Total (takeout, GST only) $= 1.07 \times 43.70 = \$46.76$ (2 d.p.)
He saved $\$51.43 - \$46.76 = \$4.67$
If he saved 10%, he should have saved $0.1 \times 51.43 = \$5.14$
No, he is not correct.""",
        "M1 for comparison, A1",
        topic_id=8)

    add_q(db, p2.id, exam_dir, 2, 5, "bi",
        r"Find the total number of votes.",
        1, "Percentage — Reverse", 5, (14, 0.94, 0.97),
        r"$60\% \to 240$, Total $= \frac{240}{60} \times 100 = 400$ votes", "B1",
        stem=r"In an election for the president of the student council, Benjamin received 240 votes. This was 60% of the total number of votes.",
        topic_id=8)

    add_q(db, p2.id, exam_dir, 2, 5, "bii",
        r"Among the total votes, 18 votes were spoilt while the rest voted for Nazri. Express the number of votes Nazri received as a percentage of the votes that were not spoilt.",
        2, "Percentage", 5, (14, 0.97, 0.99),
        r"""Votes not spoilt $= 400 - 18 = 382$
Nazri received $= 382 - 240 = 142$
Percentage $= \frac{142}{382} \times 100\% = 37.2\%$ (3 s.f.)""",
        "M1, A1",
        topic_id=8)

    # P2 Q6 — Page 6 (idx 15)
    add_q(db, p2.id, exam_dir, 2, 6, "ai",
        r"Find an expression for $n$ in terms of $x$.",
        1, "Polygon — Exterior Angle", 6, (15, 0.05, 0.14),
        r"$n = \dfrac{360}{x}$", "B1",
        stem=r"A regular $n$-sided polygon has an exterior angle of $x°$.",
        topic_id=11)

    add_q(db, p2.id, exam_dir, 2, 6, "aii",
        r"If the size of the interior angle is 2 times the size of the exterior angle $x°$, find the size of the exterior angle.",
        2, "Polygon — Interior & Exterior Angles", 6, (15, 0.14, 0.26),
        r"""$2x = 180 - x$
$3x = 180$
$x = 60°$""",
        "M1, A1",
        topic_id=11)

    add_q(db, p2.id, exam_dir, 2, 6, "aiii",
        r"Hence, find $n$.",
        1, "Polygon — Number of Sides", 6, (15, 0.26, 0.33),
        r"$n = \dfrac{360}{60} = 6$", "B1",
        topic_id=11)

    add_q(db, p2.id, exam_dir, 2, 6, "b",
        r"A polygon has $n$ sides. When the number of sides is tripled, the interior angle is increased by $30°$. Find the value of $n$.",
        3, "Polygon Angles — Equation", 6, (15, 0.33, 0.50),
        r"""$$\frac{(3n - 2) \times 180}{3n} - \frac{(n - 2) \times 180}{n} = 30$$
$$\frac{540n - 360 - 540n + 1080}{3n} = 30$$
$$\frac{720}{3n} = 30$$
$$720 = 90n$$
$$n = 8$$""",
        "M1 for expressions, M1 for equation, A1",
        topic_id=11)

    # P2 Q7 — Page 6 (idx 15)
    add_q(db, p2.id, exam_dir, 2, 7, "a",
        r"Convert 6 m/s to kilometres per hour.",
        2, "Speed Conversion", 6, (15, 0.53, 0.62),
        r"$$6 \times \frac{3600}{1000} = 21.6 \text{ km/h}$$", "M1, A1",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 7, "b",
        r"Ms See borrows $\$30\,000$ from a bank to renovate her house. The bank charges simple interest at a rate of 2.9% per annum. Calculate the amount of interest she has to pay if she takes 7 years to repay the loan.",
        2, "Percentage — Simple Interest", 6, (15, 0.62, 0.74),
        r"$$\text{Interest} = \frac{30000 \times 2.9 \times 7}{100} = \$6090$$", "M1, A1",
        topic_id=8)

    add_q(db, p2.id, exam_dir, 2, 7, "ci",
        r"Calculate the parking charges if Ms Zhang parks her car for 2 hr 27 minutes.",
        2, "Rate — Word Problem", 6, (15, 0.74, 0.87),
        r"Parking charges $= \$2.40 + 3 \times \$0.70 = \$4.50$", "M1, A1",
        stem=r"The table below shows the parking charges at a certain shopping centre: 1st hour $\$2.40$, every subsequent $\frac{1}{2}$ hour or part thereof $\$0.70$.",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 7, "cii",
        r"If Ms Zhang has a cashcard value of $\$7$, what is the maximum number of complete hours she can park her car at the shopping centre?",
        2, "Rate — Word Problem", 6, (15, 0.87, 0.97),
        r"""$\$7 - \$2.40 = \$4.60$
$\frac{4.60}{0.70} = 6.57$ half hours
$= 6$ half hours (round down) $= 3$ hours
Total $= 1 + 3 = 4$ hours""",
        "M1, A1",
        topic_id=9)

    db.commit()
    p1_count = len(p1.questions)
    p2_count = len(p2.questions)
    print(f"Seeded Bedok View exam id={exam.id}: Paper 1 ({p1_count} parts), Paper 2 ({p2_count} parts)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
