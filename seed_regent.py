"""Seed Regent Secondary School SA2 2020 Sec 1 Express Math exam."""

import os
import shutil
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/66a8bac6cfbab_3604.pdf"
IMAGES_DIR = "/tmp/regent_pages"

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

    existing = db.query(Exam).filter(Exam.school_id == school.id, Exam.year == 2020).first()
    if existing:
        print(f"Regent 2020 already seeded (id={existing.id}). Deleting and re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id, title="SA2 Examination 2020", year=2020,
        level="Secondary 1 Express", subject="Mathematics",
        source_pdf="66a8bac6cfbab_3604.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # PAPER 1 — Pages 2-12 (idx 1-12), 50 marks, 1 hour 15 min
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=75, total_marks=50,
               date=date(2020, 10, 5), instructions="Answer all questions.")
    db.add(p1); db.flush()

    # Q1 — Page 2 (idx 1)
    add_q(db, p1.id, exam_dir, 1, 1, None,
        r"Write the following numbers in order of size, starting with the smallest: $0.33$, $\dfrac{1}{3}$, $\left(\dfrac{1}{3}\right)^3$, $0.3$.",
        1, "Ordering Numbers", 2, (1, 0.05, 0.32),
        r"$\left(\dfrac{1}{3}\right)^3$, $0.3$, $0.33$, $\dfrac{1}{3}$", "B1",
        topic_id=2)

    # Q2 — Page 2 (idx 1)
    add_q(db, p1.id, exam_dir, 1, 2, None,
        r"The number of students in a school is given as 900, correct to the nearest hundred. Write down the minimum number of students that could be in the school at this time.",
        1, "Approximation / Rounding", 2, (1, 0.32, 0.45),
        r"$850$", "B1",
        topic_id=3)

    # Q3 — Page 2 (idx 1)
    add_q(db, p1.id, exam_dir, 1, 3, "a",
        r"Express $4320$ as a product of its prime factors.",
        1, "Prime Factorisation", 2, (1, 0.45, 0.67),
        r"$4320 = 2^5 \times 3^3 \times 5$", "B1",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 3, "b",
        r"The number $\dfrac{4320}{p}$ is a perfect cube. Given that $p$ is an integer, find the smallest value of $p$.",
        1, "Perfect Cube", 2, (1, 0.67, 0.90),
        r"$p = 2^2 \times 5 = 20$", "B1",
        topic_id=1)

    # Q4 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 4, None,
        r"By rounding each number to 2 significant figures, estimate the value of $$\dfrac{\sqrt{64.432} \times 25.12}{(19.7)^2}$$",
        2, "Estimation", 3, (2, 0.0, 0.30),
        r"$$\approx \frac{\sqrt{64} \times 25}{20^2} = \frac{8 \times 25}{400} = \frac{200}{400} = \frac{1}{2} \text{ or } 0.5$$", "M1, A1",
        topic_id=3)

    # Q5 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 5, "a",
        r"the gradient of the line.",
        1, "Linear Functions — Gradient", 3, (2, 0.30, 0.58),
        r"Gradient $= -3$", "B1",
        stem=r"The equation of a straight line is $2y = -6x + 5$. Find:",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 5, "b",
        r"the coordinates of the $y$-intercept of the line.",
        1, "Linear Functions — Intercept", 3, (2, 0.57, 0.85),
        r"$\left(0, \dfrac{5}{2}\right)$", "B1",
        topic_id=6)

    # Q6 — Page 4 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 6, None,
        r"Write as a single fraction in its simplest form $\dfrac{2+x}{3} - \dfrac{2(x-1)}{5}$.",
        3, "Algebraic Fractions", 4, (3, 0.0, 0.28),
        r"$$= \frac{5(2+x) - 6(x-1)}{15} = \frac{10 + 5x - 6x + 6}{15} = \frac{16 - x}{15}$$", "M1, M1, A1",
        topic_id=4)

    # Q7 — Page 4 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 7, "a",
        r"Construct triangle $ABC$ where angle $ABC = 100°$ and $AC = 7$ cm. $AB$ has already been drawn.",
        2, "Construction", 4, (3, 0.28, 0.76),
        r"Angle $ABC = 100° \pm 1°$ drawn; $AC = 7$ cm $\pm 0.1$ drawn.", "C1 for angle, C1 for length",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 7, "b",
        r"Write down the length of $BC$.",
        1, "Construction — Measurement", 4, (3, 0.75, 0.92),
        r"$BC = 4.1 \pm 0.1$ cm", "B1",
        topic_id=10)

    # Q8 — Page 5 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 8, "a(i)",
        r"How much butter does he use?",
        1, "Ratio", 5, (4, 0.0, 0.25),
        r"$1$ unit $= 150$ g. $3$ units $= 450$ g of butter.", "B1",
        stem=r"Tam bakes some cookies. He uses flour, sugar and butter in the ratio $5 : 2 : 3$ respectively. He uses 300 g of sugar.",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 8, "a(ii)",
        r"How much is the total mass of ingredients he used?",
        1, "Ratio", 5, (4, 0.24, 0.40),
        r"$10$ units $= 1500$ g", "B1",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 8, "b",
        r"Ng bakes some cookies using flour, oats and butter. The ratio flour : oats is $3 : 2$. The ratio oats : butter is $8 : 7$. Find the ratio of flour : oats : butter.",
        1, "Ratio — Combining", 5, (4, 0.40, 0.90),
        r"flour : oats $= 12 : 8$, oats : butter $= 8 : 7$. So flour : oats : butter $= 12 : 8 : 7$.", "B1",
        topic_id=9)

    # Q9 — Page 6 (idx 5)
    add_q(db, p1.id, exam_dir, 1, 9, None,
        r"Solve $\dfrac{x - 4}{2} - \dfrac{3x}{8} = 1$.",
        3, "Solving Linear Equations", 6, (5, 0.0, 0.35),
        r"""$$\frac{4(x-4) - 3x}{8} = 1$$
$$4x - 16 - 3x = 8$$
$$x = 24$$""",
        "M1 for common denominator, M1 for expansion, A1",
        topic_id=5)

    # Q10 — Page 6 (idx 5)
    add_q(db, p1.id, exam_dir, 1, 10, "a",
        r"Simplify $9 + 5(2x + 3)$.",
        2, "Algebra — Expansion", 6, (5, 0.35, 0.58),
        r"$$= 9 + 10x + 15 = 10x + 24$$", "M1, A1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 10, "b",
        r"Factorise completely $7ax + 21ay - 14aby$.",
        1, "Algebra — Factorisation", 6, (5, 0.58, 0.88),
        r"$7a(x + 3y - 2by)$", "B1",
        topic_id=4)

    # Q11 — Page 7 (idx 6)
    add_q(db, p1.id, exam_dir, 1, 11, "a",
        r"$x$.",
        1, "Rhombus — Angle Properties", 7, (6, 0.0, 0.55),
        r"$x = 90°$ (diagonals of rhombus bisect at right angles)", "B1",
        stem=r"In the diagram, $ABCD$ is a rhombus and angle $ABC = 75°$. Find, stating your reasons, the value of:",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 11, "b",
        r"$y$.",
        2, "Rhombus — Angle Properties", 7, (6, 0.54, 0.88),
        r"""$\angle ABC = 75°$
$y = \dfrac{180° - 75°}{2} = 52.5°$ (base angle of isosceles triangle)""",
        "M1, A1",
        topic_id=10)

    # Q12 — Page 8 (idx 7)
    add_q(db, p1.id, exam_dir, 1, 12, "a",
        r"Calculate, stating the reasons, angle $ADC$.",
        1, "Trapezium — Angle Properties", 8, (7, 0.0, 0.44),
        r"$\angle ADC = 180° - 104° = 76°$ (co-interior angles, $AB \parallel DC$)", "B1",
        stem=r"In the diagram, $ABCD$ is a trapezium where $AB$ is parallel to $DC$. $AB = 5$ cm, $DC = 8$ cm and angle $DAB = 104°$.",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 12, "b(i)",
        r"Given that the area of triangle $BDC$ is 16 cm$^2$, show that the perpendicular height of the triangle is 4 cm.",
        1, "Area of Triangle", 8, (7, 0.43, 0.64),
        r"$$\text{Area} = \frac{1}{2} \times 8 \times h = 16 \implies h = 4 \text{ cm (shown)}$$", "B1",
        topic_id=12)

    add_q(db, p1.id, exam_dir, 1, 12, "b(ii)",
        r"Hence, find the area of the trapezium $ABCD$.",
        2, "Area of Trapezium", 8, (7, 0.63, 0.92),
        r"$$\text{Area} = \frac{1}{2}(5 + 8)(4) = 26 \text{ cm}^2$$", "M1, A1",
        topic_id=12)

    # Q13 — Page 9 (idx 8)
    add_q(db, p1.id, exam_dir, 1, 13, "a",
        r"Find the values of $a$, $b$ and $c$.",
        2, "Number Patterns", 9, (8, 0.0, 0.32),
        r"Difference $= \dfrac{30 - 6}{3} = 8$. $a = -2$, $b = 14$, $c = 22$.", "B1 for 1 correct, B1 for all correct",
        stem=r"Each term in this sequence is found by adding the same number to the previous term: $a$, $6$, $b$, $c$, $30$, $\ldots$",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 13, "b",
        r"Write down an expression, in terms of $n$, for the $n$th term.",
        1, "Number Patterns — General Term", 9, (8, 0.32, 0.52),
        r"$T_n = 8n - 10$", "B1",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 13, "c",
        r"Explain why $103$ is not a term of this sequence.",
        1, "Number Patterns — Reasoning", 9, (8, 0.52, 0.88),
        r"""$8n - 10 = 103$
$8n = 113$
$n = 14\frac{1}{8}$
As $n$ is not a whole number, $103$ is not a term of the sequence.""",
        "B1",
        topic_id=7)

    # Q14 — Page 10 (idx 9)
    add_q(db, p1.id, exam_dir, 1, 14, "a",
        r"Express 20 centimetres as a percentage of 3 metres.",
        2, "Percentage", 10, (9, 0.0, 0.20),
        r"$$\frac{20}{300} \times 100\% = 6\frac{2}{3}\%$$", "M1, A1",
        topic_id=8)

    add_q(db, p1.id, exam_dir, 1, 14, "b",
        r"The price of a laptop was $\$1899$. During the Great Singapore Sales, the price was $\$1614.15$. Calculate the percentage decrease in price for the laptop.",
        2, "Percentage Decrease", 10, (9, 0.20, 0.48),
        r"$$\frac{1899 - 1614.15}{1899} \times 100\% = 15\%$$", "M1, A1",
        topic_id=8)

    # Q15 — Page 10 (idx 9)
    add_q(db, p1.id, exam_dir, 1, 15, None,
        r"Alan is drawing a triangle. Let the first angle be $x$. The second angle is $40°$ smaller than the first angle. The third angle is five times the size of the second angle. Alan claims that the smallest angle is $15°$, do you agree with him? Justify your answer by showing all workings.",
        4, "Angles in Triangle / Linear Equation", 10, (9, 0.48, 0.95),
        r"""$x + (x - 40) + 5(x - 40) = 180$
$x + x - 40 + 5x - 200 = 180$
$7x - 240 = 180$
$7x = 420$
$x = 60$
Smallest angle $= 60° - 40° = 20°$.
I do not agree with Alan as the smallest angle should be $20°$.""",
        "M1 for equation, M1 for expanding, M1 for solving, A1 for conclusion",
        topic_id=5)

    # Q16 — Page 11 (idx 10)
    add_q(db, p1.id, exam_dir, 1, 16, "a",
        r"How long did Bob spend at McDonalds?",
        1, "Speed-Time Graph — Reading", 11, (10, 0.0, 0.65),
        r"$8$ minutes", "B1",
        stem=r"The graph shows Bob's journey from home to school. He left home at 06 30 and cycled to McDonalds to get breakfast before taking a bus to school. Assume that the bus did not stop along the way.",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 16, "b",
        r"What is the distance between McDonalds and Bob's school?",
        1, "Speed-Time Graph — Reading", 11, (10, 0.64, 0.76),
        r"$10$ km", "B1",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 16, "c",
        r"Calculate the speed, in kilometres per hour, of the bus.",
        2, "Speed Calculation", 11, (10, 0.75, 0.92),
        r"$$\text{Speed} = \frac{10}{\frac{12}{60}} = \frac{10 \times 60}{12} = 50 \text{ km/h}$$", "M1, A1",
        topic_id=9)

    # Q17 — Page 12 (idx 11)
    add_q(db, p1.id, exam_dir, 1, 17, None,
        r"The cross-section of a circular badge is as shown. A ribbon-shape, consisting of two identical right-angled triangles, is removed from the badge. All measurements are in centimetres. Given that the radius of the circular badge is 2.5 cm, calculate the remaining area of the badge.",
        4, "Area — Circle minus Triangles", 12, (11, 0.0, 0.80),
        r"""Area of circle $= \pi (2.5)^2 = 6.25\pi$ cm$^2$
Area of 2 triangles $= 2 \times \frac{1}{2} \times 1.7 \times 1.4 = 2.38$ cm$^2$
Remaining area $= 6.25\pi - 2.38 = 17.3$ cm$^2$ (3 s.f.)""",
        "M1 for circle area, M1 for triangle area, M1 for subtraction, A1",
        topic_id=12)

    # ══════════════════════════════════════════════
    # PAPER 2 — Pages 14-23 (idx 13-23), 50 marks, 1h30m
    # ══════════════════════════════════════════════
    p2 = Paper(exam_id=exam.id, paper_number=2, duration_minutes=90, total_marks=50,
               date=date(2020, 10, 6), instructions="Answer all questions.")
    db.add(p2); db.flush()

    # P2 Q1 — Page 14 (idx 13)
    add_q(db, p2.id, exam_dir, 2, 1, "a",
        r"a negative integer.",
        1, "Number Classification", 14, (13, 0.0, 0.22),
        r"$-8$", "B1",
        stem=r"Study the set of numbers below: $81$, $\dfrac{1}{3}$, $\sqrt{2}$, $-0.\dot{4}\dot{3}$, $-8$, $0.09$. Write down:",
        topic_id=2)

    add_q(db, p2.id, exam_dir, 2, 1, "b",
        r"a square number.",
        1, "Number Classification", 14, (13, 0.22, 0.37),
        r"$81$", "B1",
        topic_id=2)

    add_q(db, p2.id, exam_dir, 2, 1, "c",
        r"an irrational number.",
        1, "Number Classification", 14, (13, 0.37, 0.50),
        r"$\sqrt{2}$", "B1",
        topic_id=2)

    # P2 Q2 — Page 14 (idx 13)
    add_q(db, p2.id, exam_dir, 2, 2, "a",
        r"Express $\dfrac{3}{35}$ as a percentage.",
        1, "Percentage Conversion", 14, (13, 0.50, 0.68),
        r"$\dfrac{3}{35} \times 100\% = 8\dfrac{4}{7}\%$", "B1",
        topic_id=8)

    add_q(db, p2.id, exam_dir, 2, 2, "b",
        r"Express 17.6% as a fraction in its simplest form.",
        1, "Percentage to Fraction", 14, (13, 0.68, 0.90),
        r"$\dfrac{17.6}{100} = \dfrac{176}{1000} = \dfrac{22}{125}$", "B1",
        topic_id=8)

    # P2 Q3 — Page 15 (idx 14)
    add_q(db, p2.id, exam_dir, 2, 3, "a",
        r"Convert 90 km/h to m/s.",
        1, "Speed Conversion", 15, (14, 0.0, 0.18),
        r"$$90 \times \frac{1000}{3600} = 25 \text{ m/s}$$", "A1",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 3, "b(i)",
        r"the total time, in hours, for the whole journey.",
        2, "Speed, Distance, Time", 15, (14, 0.18, 0.52),
        r"""Time for 90 km $= \frac{90}{60} = 1.5$ h
Time for 40 km $= \frac{40}{40} = 1$ h
Total time $= 1.5 + 1 = 2.5$ h""",
        "M1, A1",
        stem=r"A car travels for 90 km at 60 km/h. It then travels for 40 km at 40 km/h. Calculate:",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 3, "b(ii)",
        r"the average speed for the whole journey.",
        2, "Average Speed", 15, (14, 0.52, 0.90),
        r"$$\text{Average speed} = \frac{90 + 40}{2.5} = \frac{130}{2.5} = 52 \text{ km/h}$$", "M1, A1",
        topic_id=9)

    # P2 Q4 — Page 16 (idx 15)
    add_q(db, p2.id, exam_dir, 2, 4, "a",
        r"Convert HKD 35 000 into Singapore dollars, giving your answers correct to the nearest cent.",
        1, "Currency Conversion", 16, (15, 0.0, 0.22),
        r"HKD $100 =$ S$\$1.75$. HKD $35\,000 =$ S$\$1.75 \times 350 =$ S$\$612.50$", "B1",
        stem=r"The rate of exchange between the Hong Kong dollar (HKD), Korean won (KRW) and Singapore dollar (SGD) are HKD $100 =$ SGD $1.75$ and KRW $1000 =$ SGD $1.15$.",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 4, "b",
        r"Convert SGD 460 into Korean won, giving your answers correct to the nearest unit of the foreign currency.",
        1, "Currency Conversion", 16, (15, 0.22, 0.42),
        r"S$\$1.15 =$ KRW $1000$. S$\$1 =$ KRW $\frac{1000}{1.15}$. S$\$460 =$ KRW $\frac{1000}{1.15} \times 460 = 400\,000$", "B1",
        topic_id=9)

    # P2 Q5 — Page 16 (idx 15)
    add_q(db, p2.id, exam_dir, 2, 5, "a",
        r"the value of the cube root of $A$.",
        1, "Cube Root from Prime Factors", 16, (15, 0.42, 0.60),
        r"$\sqrt[3]{A} = \sqrt[3]{2^3 \times 5^3} = 2 \times 5 = 10$", "B1",
        stem=r"When written as product of their prime factors, $A = 2^3 \times 5^3$, $B = 2 \times 3 \times 5 \times 7$, $C = 2^2 \times 5^3 \times 7^2$. Find:",
        topic_id=1)

    add_q(db, p2.id, exam_dir, 2, 5, "b",
        r"the greatest number that will divide $A$, $B$ and $C$ exactly.",
        2, "HCF", 16, (15, 0.60, 0.78),
        r"HCF of $A$, $B$, $C = 2 \times 5 = 10$", "M1, A1",
        topic_id=1)

    add_q(db, p2.id, exam_dir, 2, 5, "c",
        r"the lowest common multiple of $A$, $B$ and $C$.",
        2, "LCM", 16, (15, 0.78, 0.95),
        r"LCM $= 2^3 \times 3 \times 5^3 \times 7^2 = 147\,000$", "M1, A1",
        topic_id=1)

    # P2 Q6 — Page 17 (idx 16)
    add_q(db, p2.id, exam_dir, 2, 6, "a",
        r"If $n$ represents the number in the top left corner of the square, write down an expression in terms of $n$, for the number in the bottom right corner of the square.",
        1, "Number Patterns — Expression", 17, (16, 0.0, 0.48),
        r"$n + 7$", "B1",
        stem=r"The diagram shows part of a number grid. A square outlining four numbers, as shown, can be placed anywhere on the grid.",
        topic_id=7)

    add_q(db, p2.id, exam_dir, 2, 6, "b",
        r"Find in its simplest form, an expression in terms of $n$, for the sum of the numbers in the square.",
        2, "Number Patterns — Simplification", 17, (16, 0.48, 0.92),
        r"$n + (n+1) + (n+6) + (n+7) = 4n + 14$", "M1, A1",
        topic_id=7)

    # P2 Q7 — Pages 18-19 (idx 17-18)
    add_q(db, p2.id, exam_dir, 2, 7, "a",
        r"Calculate the volume of water in the cylindrical tank.",
        2, "Volume — Cylinder", 18, (17, 0.0, 0.52),
        r"""$$V = \pi r^2 h = \pi \times \left(\frac{38}{2}\right)^2 \times 50 = \pi \times 19^2 \times 50 = 56\,700 \text{ cm}^3 \text{ (3 s.f.)}$$""",
        "M1, A1",
        stem=r"Diagram I shows an opened cylindrical tank of diameter 38 cm and height 50 cm and is fully filled with water. Diagram II shows an opened rectangular tank of length 70 cm, width 30 cm and height 40 cm.",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 7, "b",
        r"It takes 10 minutes to fill the cylindrical tank. Explain with working if it will take less or more time to fill the rectangular tank.",
        3, "Volume — Comparison", 18, (17, 0.52, 0.95),
        r"""Flow rate $= \frac{56\,700}{10} = 5670$ cm$^3$/min
Volume of rectangular tank $= 70 \times 30 \times 40 = 84\,000$ cm$^3$
Time $= \frac{84\,000}{5670} = 14.8$ min $> 10$ min.
It takes more time to fill the rectangular tank.""",
        "M1 for flow rate, M1 for rect volume, A1 for conclusion",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 7, "c",
        r"Calculate the area of the plastic material needed to construct 1 rectangular tank.",
        2, "Surface Area — Open Rectangular Tank", 19, (18, 0.0, 0.12),
        r"$$\text{SA} = (70 \times 30) + 2(30 \times 40) + 2(70 \times 40) = 2100 + 2400 + 5600 = 10\,100 \text{ cm}^2$$", "M1, A1",
        topic_id=13)

    # P2 Q8 — Page 19 (idx 18)
    add_q(db, p2.id, exam_dir, 2, 8, "a",
        r"Find the size of one exterior angle of a regular hexagon.",
        1, "Polygon — Exterior Angle", 19, (18, 0.12, 0.28),
        r"Exterior angle $= \dfrac{360°}{6} = 60°$", "B1",
        topic_id=11)

    add_q(db, p2.id, exam_dir, 2, 8, "b(i)",
        r"angle $BAH$.",
        2, "Polygon Angles — Octagon + Hexagon", 19, (18, 0.28, 0.65),
        r"Interior angle of octagon $= \dfrac{(8-2) \times 180°}{8} = 135°$. $\angle BAH = 135°$.", "M1, A1",
        stem=r"The figure shows a regular octagon $ABCDEFGH$ and a regular hexagon $ABWXYZ$ which shares a common side $AB$.",
        topic_id=11)

    add_q(db, p2.id, exam_dir, 2, 8, "b(ii)",
        r"angle $HAZ$.",
        2, "Polygon Angles", 19, (18, 0.65, 0.90),
        r"Interior angle of hexagon $= 120°$. $\angle HAZ = 360° - 135° - 120° = 105°$", "M1, A1",
        topic_id=11)

    # P2 Q9 — Page 20 (idx 19)
    add_q(db, p2.id, exam_dir, 2, 9, "a(i)",
        r"angle $BDF$.",
        1, "Angle Properties — Parallel Lines", 20, (19, 0.0, 0.35),
        r"$\angle BDF = \angle CBD = 56°$ (alternate angles, $AB \parallel FD$)", "B1",
        stem=r"In the diagram, $AB$ is parallel to $EDC$ and $BC$ is parallel to $FD$. Angle $CBD = 56°$, angle $FDE = 44°$ and angle $BAF = 101°$. Stating your reasons clearly, calculate:",
        topic_id=10)

    add_q(db, p2.id, exam_dir, 2, 9, "a(ii)",
        r"angle $BCD$.",
        1, "Angle Properties — Parallel Lines", 20, (19, 0.34, 0.48),
        r"$\angle BCD = \angle FDE = 44°$ (corresponding angles, $BC \parallel FD$)", "B1",
        topic_id=10)

    add_q(db, p2.id, exam_dir, 2, 9, "a(iii)",
        r"angle $ABD$.",
        2, "Angle Properties", 20, (19, 0.47, 0.65),
        r"$\angle ABD = 180° - 44° - 56° = 80°$ (co-interior angles, $AB \parallel EDC$)", "M1, A1",
        topic_id=10)

    add_q(db, p2.id, exam_dir, 2, 9, "b",
        r"State, showing your reasoning, whether $AF$ is parallel to $BD$.",
        2, "Parallel Lines — Proof", 20, (19, 0.65, 0.95),
        r"""$\angle BAF + \angle ABD = 101° + 80° = 181°$
Since the sum is not $180°$, $AF$ is not parallel to $BD$.""",
        "M1, A1",
        topic_id=10)

    # P2 Q10 — Page 21 (idx 20)
    add_q(db, p2.id, exam_dir, 2, 10, "a",
        r"Calculate the area of the parallelogram $ABCD$.",
        2, "Area — Parallelogram", 21, (20, 0.0, 0.42),
        r"Area $= 22 \times 8 = 176$ cm$^2$", "M1, A1",
        stem=r"The figure below shows a parallelogram $ABCD$. $AB$ is parallel to $DC$ and $DA$ is parallel to $CB$. $MC$ is perpendicular to $AB$ and $NC$ is perpendicular to $DA$. Given that $DC = 22$ cm, $MC = 8$ cm and $NC = 11$ cm.",
        topic_id=12)

    add_q(db, p2.id, exam_dir, 2, 10, "b",
        r"Show that the length of $AD = 16$ cm.",
        2, "Area — Parallelogram (reverse)", 21, (20, 0.42, 0.65),
        r"""Area $= AD \times NC$
$176 = AD \times 11$
$AD = 16$ cm (shown)""",
        "M1, A1",
        topic_id=12)

    add_q(db, p2.id, exam_dir, 2, 10, "c",
        r"Hence, calculate the perimeter of the parallelogram $ABCD$.",
        2, "Perimeter — Parallelogram", 21, (20, 0.65, 0.90),
        r"Perimeter $= 2(16 + 22) = 76$ cm", "M1, A1",
        topic_id=12)

    # P2 Q11 — Pages 22-23 (idx 21-22)
    add_q(db, p2.id, exam_dir, 2, 11, "a",
        r"Calculate the value of $p$ and $q$.",
        2, "Linear Functions — Table", 22, (21, 0.0, 0.35),
        r"$p = 35 + 15(1) = \$50$. $q = 35 + 15(3) = \$80$.", "B1, B1",
        stem=r"Elizabeth recorded the charges ($\$y$) she has to pay the electrician based on the number of hours ($x$ hours) the electrician worked. The variables $x$ and $y$ are connected by the equation $y = 35 + 15x$.",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 11, "b",
        r"On the grid provided on page 11, draw the graph of $y = 35 + 15x$ for $0 \leq x \leq 4$. On your axes, plot the points given in the table and join them with a straight line.",
        2, "Linear Functions — Graph", 22, (21, 0.35, 0.52),
        r"Straight line through $(0, 35)$, $(1, 50)$, $(2, 65)$, $(3, 80)$, $(4, 95)$.", "B1 for points, B1 for line",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 11, "c(i)",
        r"the amount of money he charged if he spent 2.5 hours on the job.",
        1, "Linear Functions — Reading Graph", 22, (21, 0.52, 0.68),
        r"Between $\$72$ and $\$73$", "B1",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 11, "c(ii)",
        r"the number of hours the electrician spent on the job if he charged the electrician $\$90$.",
        1, "Linear Functions — Reading Graph", 22, (21, 0.68, 0.90),
        r"Between $3.6$ h and $3.7$ h", "B1",
        topic_id=6)

    db.commit()
    p1_count = len(p1.questions)
    p2_count = len(p2.questions)
    print(f"Seeded Regent exam id={exam.id}: Paper 1 ({p1_count} parts), Paper 2 ({p2_count} parts)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
