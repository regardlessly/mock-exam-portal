"""Seed Juying Secondary School EOY 2023 Sec 1 Express Math exam."""

import os
import shutil
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/Juying-Secondary-EOY-2023-Sec-1-Math-Group-3.pdf"
IMAGES_DIR = "/tmp/juying_pages"

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

    school = db.query(School).filter(School.name == "Juying Secondary School").first()
    if not school:
        school = School(name="Juying Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(Exam.school_id == school.id, Exam.year == 2023).first()
    if existing:
        print(f"Juying 2023 already seeded (id={existing.id}). Deleting and re-seeding.")
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
        source_pdf="Juying-Secondary-EOY-2023-Sec-1-Math-Group-3.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # PAPER 1 — Pages 1-9 (idx 0-8), 50 marks, 1h15m
    # 3 October 2023
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=75, total_marks=50,
               date=date(2023, 10, 3), instructions="Answer all questions.")
    db.add(p1); db.flush()

    # Q1 — Page 2 (idx 1)
    add_q(db, p1.id, exam_dir, 1, 1, "a",
        r"Evaluate $\dfrac{\sqrt[3]{1728} \times 2.009}{(-6.24)^2}$, giving your answer correct to 3 significant figures.",
        1, "Estimation / Calculator", 2, (1, 0.06, 0.24),
        r"$0.139\overline{8}29 = 0.140$ (3 s.f.)", "B1",
        topic_id=3)

    add_q(db, p1.id, exam_dir, 1, 1, "b",
        r"The number of people in Pioneer Stadium is given as 4200, correct to the nearest hundred. Write down the maximum number of people that could be in the stadium.",
        1, "Rounding / Approximation", 2, (1, 0.24, 0.42),
        r"$4249$", "B1",
        topic_id=3)

    # Q2 — Page 2 (idx 1)
    add_q(db, p1.id, exam_dir, 1, 2, "a",
        r"Find its height.",
        2, "Volume — Cylinder", 2, (1, 0.42, 0.64),
        r"""Radius $= 12$ cm
$$h = \frac{1188\pi}{\pi(12)^2} = 8.25 \text{ cm}$$""",
        "M1, A1",
        stem=r"A cylindrical solid with base diameter 24 cm has a volume of $1188\pi$ cm$^3$.",
        topic_id=13)

    add_q(db, p1.id, exam_dir, 1, 2, "b",
        r"Hence, find its total surface area.",
        3, "Surface Area — Cylinder", 2, (1, 0.63, 0.88),
        r"""$$\text{TSA} = 2 \times \pi(12)^2 + 2\pi(12)(8.25) = 1530 \text{ cm}^2 \text{ (3 s.f.)}$$
Exact value of $486\pi$ cm$^2$ accepted.""",
        "M1 for circles, M1/ECF for curved SA, A1",
        topic_id=13)

    # Q3 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 3, "a",
        r"Written as a product of its prime factors, $168 = 2^3 \times 3 \times 7$. Find the smallest positive integer $k$ such that $168k$ is a perfect square.",
        1, "Prime Factorisation — Perfect Square", 3, (2, 0.04, 0.26),
        r"$k = 2 \times 3 \times 7 = 42$", "B1 (accepted $k = 2 \times 3 \times 7$)",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 3, "b",
        r"$x$ is a number between 100 and 200. The highest common factor of $x$ and 168 is 42. Find the smallest possible value of $x$.",
        1, "HCF", 3, (2, 0.26, 0.55),
        r"""$168 = 2^3 \times 3 \times 7$
$x = 2 \times 3^2 \times 7 = 126$
$\text{HCF} = 42 = 2 \times 3 \times 7$""",
        "B1",
        topic_id=1)

    # Q4 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 4, None,
        r"In a museum, three antique clocks will chime at regular intervals of 10 minutes, 12 minutes and $t$ minutes. If they chime together at 6.00 a.m. and at 11.00 a.m. in the morning, find the smallest value of $t$.",
        3, "LCM", 3, (2, 0.55, 0.95),
        r"""6 am to 11 am $= 5$ hours $= 300$ min
$\text{LCM}(10, 12, t) = 300 = 2^2 \times 3 \times 5^2$
$10 = 2 \times 5$, $12 = 2^2 \times 3$
$t = 5^2 = 25$""",
        "M1 for 300 min, M1 for prime factorisation of 300, A1",
        topic_id=1)

    # Q5 — Page 4 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 5, "a",
        r"In 2021, Alfa earned a total of $\$78000$. In 2022, he earned $\$7345$ each month. Calculate the percentage increase in his earnings from 2021 to 2022.",
        2, "Percentage Increase", 4, (3, 0.04, 0.28),
        r"""$$\frac{7345 \times 12 - 78000}{78000} \times 100\% = \frac{88140 - 78000}{78000} \times 100\% = 13\%$$""",
        "M1 for finding increase, A1",
        topic_id=8)

    add_q(db, p1.id, exam_dir, 1, 5, "b",
        r"Alfa paid $\$14526$ for a watch, inclusive of 8% goods and services tax (GST). His friend commented that the watch costs $\$13363.92$ before GST. Is his comment correct? Show your calculations clearly.",
        3, "Percentage — GST", 4, (3, 0.28, 0.63),
        r"""$108\% \to \$14526$
$$100\% = \frac{14526}{108} \times 100 = \$13450$$
His comment is not correct because the price before GST should be $\$13450$, not $\$13363.92$.""",
        "M1 for 108%, M1 for working, A1 for conclusion",
        topic_id=8)

    # Q6 — Page 4 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 6, None,
        r"Bella invested $\$15000$ in a savings plan that pays simple interest at a rate of 2.5% per annum. Calculate the total amount of money she has at the end of 6 years.",
        2, "Simple Interest", 4, (3, 0.63, 0.95),
        r"""Simple interest $= \dfrac{15000 \times 2.5 \times 6}{100} = \$2250$
Total amount $= 15000 + 2250 = \$17250$""",
        "M1 for interest, A1",
        topic_id=8)

    # Q7 — Page 5 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 7, "a",
        r"Find the gradient of line $AB$.",
        2, "Gradient", 5, (4, 0.04, 0.46),
        r"""$$\text{Gradient of } AB = \frac{4 - (-1)}{-1 - (-3)} = \frac{5}{2} = 2.5$$""",
        "M1, A1",
        stem=r"Points $A(-1, 4)$, $B(-3, -1)$ and $C(3, -1)$ are plotted in the diagram below.",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 7, "bi",
        r"Plot and label the point $D(3, 4)$ in the diagram above.",
        1, "Coordinate Geometry — Plotting", 5, (4, 0.46, 0.55),
        r"Point $D(3, 4)$ plotted and labelled correctly.", "B1",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 7, "bii",
        r"State the gradient of line $BC$.",
        1, "Gradient", 5, (4, 0.55, 0.64),
        r"Gradient of $BC = 0$", "B1",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 7, "biii",
        r"Write down the name of the quadrilateral $ABCD$.",
        1, "Coordinate Geometry — Shape", 5, (4, 0.64, 0.72),
        r"Trapezium", "B1",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 7, "biv",
        r"Calculate the area of quadrilateral $ABCD$.",
        2, "Area — Trapezium", 5, (4, 0.72, 0.90),
        r"""$$\text{Area} = \frac{1}{2}(4 + 6) \times 5 = 25 \text{ units}^2$$""",
        "M1 for (4+6) or 5, A1",
        topic_id=12)

    # Q8 — Page 6 (idx 5)
    add_q(db, p1.id, exam_dir, 1, 8, "a",
        r"Simplify $2pq - 3q(5p + 4r)$.",
        2, "Algebra — Expansion", 6, (5, 0.04, 0.24),
        r"$$= 2pq - 15pq - 12qr = -13pq - 12qr$$",
        "M1 for either $-15pq$ or $-12qr$ correct, A1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 8, "b",
        r"Simplify $\dfrac{1}{3}(u + 2v) - \dfrac{1}{4}(5u - 8v)$.",
        2, "Algebra — Expansion with Fractions", 6, (5, 0.24, 0.48),
        r"""$$= \frac{u}{3} + \frac{2v}{3} - \frac{5u}{4} + 2v = \frac{4u + 8v - 15u + 24v}{12} = \frac{-11u + 32v}{12}$$""",
        "M1 for either expansion correct, A1",
        topic_id=4)

    # Q9 — Page 6 (idx 5)
    add_q(db, p1.id, exam_dir, 1, 9, "a",
        r"Express $\dfrac{5 - 3x}{2} + x$ as a single fraction in its simplest form.",
        2, "Algebraic Fractions", 6, (5, 0.48, 0.72),
        r"""$$= \frac{5 - 3x + 2x}{2} = \frac{5 - x}{2}$$""",
        "M1, A1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 9, "b",
        r"Express $\dfrac{1 + x}{4} + \dfrac{7x - 5}{6}$ as a single fraction in its simplest form.",
        3, "Algebraic Fractions", 6, (5, 0.72, 0.95),
        r"""$$= \frac{3(1+x) + 2(7x-5)}{12} = \frac{3 + 3x + 14x - 10}{12} = \frac{17x - 7}{12}$$""",
        "M1 for common denominator, M1 for expansion, A1",
        topic_id=4)

    # Q10 — Page 7 (idx 6)
    add_q(db, p1.id, exam_dir, 1, 10, "a",
        r"Solve $\dfrac{2x}{5} = 8$.",
        1, "Linear Equations", 7, (6, 0.04, 0.24),
        r"$2x = 40$, $x = 20$", "B1",
        topic_id=5)

    add_q(db, p1.id, exam_dir, 1, 10, "b",
        r"Solve $15y = 3 + 7(y - 45)$.",
        2, "Linear Equations", 7, (6, 0.24, 0.50),
        r"""$15y = 3 + 7y - 315$
$8y = -312$
$y = -39$""",
        "M1 for expanding, A1",
        topic_id=5)

    add_q(db, p1.id, exam_dir, 1, 10, "c",
        r"Solve $\dfrac{8}{5 + 7z} = \dfrac{1}{4z - 5}$.",
        3, "Linear Equations — Fractions", 7, (6, 0.50, 0.90),
        r"""$8(4z - 5) = 5 + 7z$
$32z - 40 = 5 + 7z$
$25z = 45$
$z = 1.8$ or $1\frac{4}{5}$""",
        "M1 for eliminating denominators, M1 for expanding, A1",
        topic_id=5)

    # Q11 — Page 8 (idx 7)
    add_q(db, p1.id, exam_dir, 1, 11, "a",
        r"Calculate the distance between Singapore and Malacca.",
        2, "Speed, Distance, Time", 8, (7, 0.04, 0.34),
        r"$$96 \times 2\frac{1}{2} = 240 \text{ km}$$",
        "M1, A1",
        stem=r"On his journey from Singapore to Malacca, Callum travelled at a speed of 96 km/h for 2 hours 30 minutes. He rested in Malacca for 30 minutes before driving another 145 km to Kuala Lumpur at a speed of 100 km/h.",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 11, "b",
        r"Find the time taken to travel from Malacca to Kuala Lumpur, giving your answer in hours and minutes.",
        2, "Speed, Distance, Time", 8, (7, 0.34, 0.58),
        r"$$\frac{145}{100} = 1.45 \text{ h} = 1 \text{ hr } 27 \text{ min}$$",
        "M1, A1",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 11, "c",
        r"Calculate the average speed of the entire journey from Singapore to Kuala Lumpur.",
        2, "Average Speed", 8, (7, 0.58, 0.90),
        r"""$$\text{Average speed} = \frac{240 + 145}{2.5 + 0.5 + 1.45} = \frac{385}{4.45} = 86.5 \text{ km/h (3 s.f.)}$$""",
        "M1 for total dist/total time, A1",
        topic_id=9)

    # Q12 — Page 9 (idx 8)
    add_q(db, p1.id, exam_dir, 1, 12, "a",
        r"Find the area of the parallelogram.",
        1, "Area — Parallelogram", 9, (8, 0.04, 0.62),
        r"Area $= 21 \times 15 = 315$ cm$^2$", "B1",
        stem=r"The diagram shows a parallelogram $ABCD$. The perpendicular from $A$ to $BC$ meets $BC$ at $P$. The perpendicular from $A$ to $DC$ meets $DC$ at $Q$. $AB = 21$ cm, $AP = 18$ cm and $AQ = 15$ cm.",
        topic_id=12)

    add_q(db, p1.id, exam_dir, 1, 12, "b",
        r"Find the perimeter of the parallelogram.",
        2, "Perimeter — Parallelogram", 9, (8, 0.60, 0.88),
        r"""$BC = \dfrac{315}{18} = 17.5$ cm
Perimeter $= 2(17.5 + 21) = 77$ cm""",
        "M1 for BC, A1",
        topic_id=12)

    # ══════════════════════════════════════════════
    # PAPER 2 — Pages 10-19 (idx 9-18), 50 marks, 1h15m
    # 5 October 2023
    # ══════════════════════════════════════════════
    p2 = Paper(exam_id=exam.id, paper_number=2, duration_minutes=75, total_marks=50,
               date=date(2023, 10, 5), instructions="Answer all questions.")
    db.add(p2); db.flush()

    # P2 Q1 — Page 11 (idx 10)
    add_q(db, p2.id, exam_dir, 2, 1, "a",
        r"Fill in the box: $-43 \;\square\; -34$.",
        1, "Comparing Numbers", 11, (10, 0.08, 0.18),
        r"$-43 < -34$", "B1",
        topic_id=2)

    add_q(db, p2.id, exam_dir, 2, 1, "b",
        r"Fill in the box: $0.24 \;\square\; \dfrac{6}{25}$.",
        1, "Comparing Numbers", 11, (10, 0.18, 0.28),
        r"$0.24 = \dfrac{6}{25}$", "B1",
        topic_id=2)

    add_q(db, p2.id, exam_dir, 2, 1, "c",
        r"Fill in the box: $\left(\dfrac{1}{5}\right)^4 \;\square\; \left(\dfrac{1}{3}\right)^3$.",
        1, "Comparing Numbers", 11, (10, 0.28, 0.40),
        r"$\left(\dfrac{1}{5}\right)^4 < \left(\dfrac{1}{3}\right)^3$", "B1",
        topic_id=2)

    # P2 Q2 — Page 11 (idx 10)
    add_q(db, p2.id, exam_dir, 2, 2, "a",
        r"Arrange the numbers in ascending order.",
        2, "Number Classification — Ordering", 11, (10, 0.40, 0.70),
        r"$-\dfrac{1}{3}$, $33\%$, $0.\dot{3}$, $\sqrt{3}$", "B1 for any 2 correct, B2 for all correct",
        stem=r"Consider the following numbers: $\sqrt{3}$, $33\%$, $0.\dot{3}$, $-\dfrac{1}{3}$.",
        topic_id=2)

    add_q(db, p2.id, exam_dir, 2, 2, "b",
        r"Write down the irrational number(s).",
        1, "Number Classification — Irrational", 11, (10, 0.70, 0.85),
        r"$\sqrt{3}$", "B1",
        topic_id=2)

    # P2 Q3 — Page 12 (idx 11)
    add_q(db, p2.id, exam_dir, 2, 3, "a",
        r"Write down an expression, in terms of $v$ and $x$, for the number of electric vehicles in 2023.",
        1, "Algebraic Expression", 12, (11, 0.04, 0.22),
        r"$2v + 7x$", "B1",
        stem=r"In 2021, the number of electric vehicles registered in Singapore was $v$. In 2022, the number of electric vehicles registered was twice the previous year. This number rose by another $7x$ in 2023.",
        topic_id=4)

    add_q(db, p2.id, exam_dir, 2, 3, "b",
        r"Given that $x = 188$ and that there were 4790 electric vehicles registered in 2023, find the value of $v$.",
        2, "Linear Equations — Substitution", 12, (11, 0.22, 0.40),
        r"""$2v + 7(188) = 4790$
$2v = 4790 - 1316$
$v = 1737$""",
        "M1 for equation, A1",
        topic_id=5)

    # P2 Q4 — Page 12 (idx 11)
    add_q(db, p2.id, exam_dir, 2, 4, "a",
        r"Express 945 cm$^2$ in m$^2$.",
        1, "Unit Conversion", 12, (11, 0.40, 0.55),
        r"$945 \div 100^2 = 0.0945$ m$^2$", "B1",
        topic_id=3)

    add_q(db, p2.id, exam_dir, 2, 4, "b",
        r"The total surface area of a cube is 726 cm$^2$. Find its volume.",
        3, "Volume — Cube", 12, (11, 0.55, 0.90),
        r"""Area of one surface $= 726 \div 6 = 121$ cm$^2$
Length of square $= \sqrt{121} = 11$ cm
Volume $= 11^3 = 1331$ cm$^3$""",
        "M1 for area of face, M1 for side length, A1",
        topic_id=13)

    # P2 Q5 — Page 13 (idx 12)
    add_q(db, p2.id, exam_dir, 2, 5, "a",
        r"Eight machines can spray paint 96 cars in 1 hour. Assuming all the machines work at the same rate, would four machines be able to spray paint at least 22 cars in 30 minutes? Show your calculations clearly.",
        3, "Direct Proportion / Rate", 13, (12, 0.04, 0.52),
        r"""8 machines: 96 cars in 60 min
4 machines: 48 cars in 60 min
4 machines: 24 cars in 30 min
Yes, 4 machines can spray paint 24 cars in 30 minutes, which is more than 22 cars.""",
        "M1 for halving machines, M1 for halving time, A1",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 5, "b",
        r"Given that $a : b = 2.5 : 7$ and $a : c = 3 : 1\frac{3}{5}$. Find the ratio of $b : c$.",
        3, "Ratio", 13, (12, 0.52, 0.90),
        r"""$a : b = 2.5 : 7 = 5 : 14 = 15 : 42$
$a : c = 3 : 1\frac{3}{5} = 3 : \frac{8}{5} = 15 : 8$
$b : c = 42 : 8 = 21 : 4$""",
        "M1 for each ratio, A1",
        topic_id=9)

    # P2 Q6 — Page 14 (idx 13)
    add_q(db, p2.id, exam_dir, 2, 6, "a",
        r"Write down the next two terms of the sequence.",
        2, "Number Patterns", 14, (13, 0.04, 0.20),
        r"$21, 25$", "B1, B1",
        stem=r"The first four terms of a sequence are 5, 9, 13 and 17.",
        topic_id=7)

    add_q(db, p2.id, exam_dir, 2, 6, "b",
        r"Find an expression, in terms of $n$, for the $n$th term in this sequence.",
        1, "Number Patterns — General Term", 14, (13, 0.20, 0.36),
        r"$1 + 4n$", "B1",
        topic_id=7)

    add_q(db, p2.id, exam_dir, 2, 6, "c",
        r"413 is a term in the sequence. Find the value of $n$ for this term.",
        2, "Number Patterns", 14, (13, 0.36, 0.58),
        r"""$1 + 4n = 413$
$n = 103$""",
        "M1 for equation, A1",
        topic_id=7)

    # P2 Q7 — Page 14 (idx 13)
    add_q(db, p2.id, exam_dir, 2, 7, "a",
        r"Factorise $3x - 27$.",
        1, "Factorisation", 14, (13, 0.58, 0.72),
        r"$3(x - 9)$", "B1",
        topic_id=4)

    add_q(db, p2.id, exam_dir, 2, 7, "b",
        r"Factorise $56pq - 7p + 14pr$.",
        1, "Factorisation", 14, (13, 0.72, 0.90),
        r"$7p(8q - 1 + 2r)$", "B1",
        topic_id=4)

    # P2 Q8 — Pages 15-16 (idx 14-15)
    add_q(db, p2.id, exam_dir, 2, 8, "ai",
        r"Calculate $\angle BAE$.",
        2, "Angle Properties — Isosceles Triangle", 15, (14, 0.04, 0.64),
        r"""$\angle BAE = 180 - 2(63) = 54°$ (base angles of isosceles triangle)""",
        "M1 for base angles, A1",
        stem=r"The diagram shows a quadrilateral $ABCD$. $E$ is a point on $BC$ and $F$ is a point on $AD$. $AGC$ is a straight line. $AB = AE$, $\angle ABC = 63°$, $\angle AEF = 68°$, $\angle AGF = 87°$ and $\angle EFD = 131°$.",
        topic_id=10)

    add_q(db, p2.id, exam_dir, 2, 8, "aii",
        r"Calculate $\angle AFE$.",
        2, "Angle Properties — Adjacent Angles", 15, (14, 0.64, 0.90),
        r"$\angle AFE = 180 - 131 = 49°$ (adj. angles on a str. line)", "M1, A1",
        topic_id=10)

    add_q(db, p2.id, exam_dir, 2, 8, "b",
        r"Prove that $AD$ is parallel to $BC$.",
        2, "Parallel Lines — Proof", 16, (15, 0.04, 0.38),
        r"""$\angle FEC = 180 - 68 - 63 = 49°$ (angle sum of triangle)
$\angle AFE = 180 - 131 = 49°$ (adj. angles on a str. line)
$\angle AFE = \angle FEC = 49°$
$AD$ is parallel to $BC$ (converse of alternate angles).""",
        "M1 for finding equal angles, A1 for conclusion with reason",
        topic_id=10)

    add_q(db, p2.id, exam_dir, 2, 8, "c",
        r"Hence or otherwise, calculate $\angle ACE$.",
        2, "Angle Properties", 16, (15, 0.38, 0.68),
        r"""$\angle EGC = 87°$ (vert. opp. angles)
$\angle ACE = 180 - 49 - 87 = 44°$""",
        "M1, A1",
        topic_id=10)

    # P2 Q9 — Page 17 (idx 16)
    add_q(db, p2.id, exam_dir, 2, 9, "a",
        r"Show that the volume of the prism is 36 cm$^3$.",
        2, "Volume — Prism", 17, (16, 0.04, 0.42),
        r"""$$V = \frac{1}{2} \times 3 \times 4 \times 6 = 36 \text{ cm}^3 \text{ (shown)}$$""",
        "M1 for triangle area, A1",
        stem=r"The diagram shows a prism with a triangular cross section. Dimensions: 3 cm, 4 cm, 5 cm, 6 cm.",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 9, "b",
        r"Calculate the total surface area of the prism.",
        3, "Surface Area — Prism", 17, (16, 0.42, 0.70),
        r"""$$\text{TSA} = 2\left(\frac{1}{2} \times 3 \times 4\right) + (5 \times 6) + (4 \times 6) + (3 \times 6) = 84 \text{ cm}^2$$""",
        "M1 for any 2 SA, M2 for 4 SA, A1",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 9, "c",
        r"Edna is making chocolate bars using the dimensions of the triangular prism. Find the number of chocolate bars she can make with 820 cm$^3$ of chocolate.",
        2, "Volume — Application", 17, (16, 0.70, 0.92),
        r"""$$\frac{820}{36} = 22.78 \approx 22 \text{ (round down to nearest integer)}$$""",
        "M1 for division, A1",
        topic_id=13)

    # P2 Q10 — Page 18 (idx 17)
    add_q(db, p2.id, exam_dir, 2, 10, "a",
        r"Find angle $ABC$.",
        2, "Polygon Angles — Regular Hexagon", 18, (17, 0.04, 0.52),
        r"""$$\angle ABC = \frac{(6-2) \times 180}{6} = 120°$$""",
        "M1 for formula, A1",
        stem=r"The diagram shows a regular hexagon $ABCDQR$. $PQ$, $QR$ and $RS$ are three sides of a second regular polygon. Angle $ARS = 90°$.",
        topic_id=11)

    add_q(db, p2.id, exam_dir, 2, 10, "b",
        r"Find the number of sides of the second polygon.",
        3, "Polygon Angles", 18, (17, 0.52, 0.90),
        r"""$\angle QRS = 360 - 120 - 90 = 150°$
Exterior angle of second polygon $= 180 - 150 = 30°$
No. of sides $= \dfrac{360}{30} = 12$""",
        "M1 for angle QRS, M1 for exterior angle, A1",
        topic_id=11)

    # P2 Q11 — Page 19 (idx 18)
    add_q(db, p2.id, exam_dir, 2, 11, "a",
        r"Calculate the value of $a$.",
        1, "Linear Functions — Table", 19, (18, 0.04, 0.50),
        r"$a = -3$", "B1",
        stem=r"The diagram below shows the graph of $y = -x$. The corresponding values of $x$ and $y$ for the function $y = 2x + 3$ are shown in the table below: $x = -3, 0, 1$; $y = a, 3, 5$.",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 11, "b",
        r"On the same diagram, plot and draw the graph of the function $y = 2x + 3$ for values of $x$ from $-3$ to $1$.",
        2, "Linear Functions — Graph", 19, (18, 0.50, 0.68),
        r"Straight line through $(-3, -3)$, $(0, 3)$ and $(1, 5)$.", "B1 for points, B1 for straight line through all points",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 11, "c",
        r"The point $(h, k)$ lies on both graphs. Write down the coordinates of the point.",
        1, "Linear Functions — Intersection", 19, (18, 0.68, 0.84),
        r"$(-1, 1)$", "B1",
        topic_id=6)

    db.commit()
    p1_count = len(p1.questions)
    p2_count = len(p2.questions)
    print(f"Seeded Juying exam id={exam.id}: Paper 1 ({p1_count} parts), Paper 2 ({p2_count} parts)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
