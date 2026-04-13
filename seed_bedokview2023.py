"""Seed Bedok View Secondary School EOY 2023 Sec 1 Express Math exam."""

import os
import shutil
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/Bedok-View-Secondary-EOY-2023-Sec-1-Math-Group-3.pdf"
IMAGES_DIR = "/tmp/bedokview2023_pages"

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

    existing = db.query(Exam).filter(Exam.school_id == school.id, Exam.year == 2023).first()
    if existing:
        print(f"Bedok View 2023 already seeded (id={existing.id}). Deleting and re-seeding.")
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
        source_pdf="Bedok-View-Secondary-EOY-2023-Sec-1-Math-Group-3.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # PAPER 1 — 4052/01, 3 Oct 2023, 50 marks, 1h15m
    # Pages BP-94 to BP-100 = PDF pages 2-8 (idx 1-7)
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=75, total_marks=50,
               date=date(2023, 10, 3), instructions="Answer all questions.")
    db.add(p1); db.flush()

    # Q1 — Page BP-94 (idx 1)
    add_q(db, p1.id, exam_dir, 1, 1, "ai",
        r"Round off $52.789$ to 3 significant figures.",
        1, "Approximation", 2, (1, 0.06, 0.19),
        r"$52.8$", "B1",
        stem=r"Round off the following numbers to 3 significant figures.",
        topic_id=3)

    add_q(db, p1.id, exam_dir, 1, 1, "aii",
        r"Round off $1.00236$ to 3 significant figures.",
        1, "Approximation", 2, (1, 0.18, 0.30),
        r"$1.00$", "B1",
        topic_id=3)

    add_q(db, p1.id, exam_dir, 1, 1, "b",
        r"List all the prime numbers between 20 to 30.",
        1, "Prime Numbers", 2, (1, 0.30, 0.40),
        r"$23, 29$", "B1",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 1, "c",
        r"Arrange the following numbers in descending order.\n$$\frac{23}{25}, \quad -0.25, \quad 2.3^2, \quad \frac{\pi}{3}, \quad -1$$",
        2, "Number Ordering", 2, (1, 0.39, 0.67),
        r"$2.3^2, \frac{\pi}{3}, \frac{23}{25}, -0.25, -1$", "B2 (deduct 1 mark for every error)",
        topic_id=2)

    # Q2 — Page BP-94 (idx 1)
    add_q(db, p1.id, exam_dir, 1, 2, None,
        r"Calculate $\dfrac{-10 - \sqrt{(-10)^2 - 4 \times 15 \times (-20)}}{3 \times 12}$, leaving your answer correct to 3 significant figures.",
        1, "Numerical Calculation", 2, (1, 0.67, 0.95),
        r"$-1.28$ (3 s.f.)", "B1",
        topic_id=3)

    # Q3 — Page BP-95 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 3, "a",
        r"Express $180$ as a product of its prime factors in index form.",
        2, "Prime Factorisation", 3, (2, 0.04, 0.35),
        r"$180 = 2 \times 2 \times 3 \times 3 \times 5$\n$180 = 2^2 \times 3^2 \times 5$", "M1 for any appropriate method, A1",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 3, "b",
        r"The number $180p$ is a perfect cube. Find the smallest value of $p$.",
        1, "Perfect Cube", 3, (2, 0.34, 0.46),
        r"$p = 2 \times 3 \times 5^2 = 150$", "B1",
        topic_id=1)

    # Q4 — Page BP-95 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 4, None,
        r"Express $-\dfrac{4(x+2)}{5} - \dfrac{x}{4}$ as a fraction in its simplest form.",
        3, "Algebraic Fractions", 3, (2, 0.46, 0.80),
        r"$$= \frac{-16(x+2) - 5x}{20} = \frac{-16x - 32 - 5x}{20} = \frac{-21x - 32}{20}$$", "M1, M1, A1",
        topic_id=4)

    # Q5 — Page BP-95 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 5, None,
        r"Factorise $-6x - 18xy$ completely.",
        2, "Factorisation", 3, (2, 0.80, 0.97),
        r"$= -(6x + 18xy) = -6x(1 + 3y)$", "M1, A1",
        topic_id=4)

    # Q6 — Page BP-96 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 6, "a",
        r"the value of $y$ when $x = -4$.",
        1, "Substitution", 4, (3, 0.04, 0.32),
        r"$y = \frac{2(-4)}{5} + 3 = 1\frac{2}{5}$", "B1 (accept 1.4)",
        stem=r"Given that $y = \dfrac{2x}{5} + 3$, find",
        topic_id=5)

    add_q(db, p1.id, exam_dir, 1, 6, "b",
        r"the value of $x$ when $y = 8$.",
        2, "Linear Equations", 4, (3, 0.31, 0.53),
        r"$8 = \frac{2x}{5} + 3$\n$5 = \frac{2x}{5}$\n$x = 12.5$", "M1, A1 (accept $12\frac{1}{2}$)",
        topic_id=5)

    # Q7 — Page BP-96 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 7, "a",
        r"Find an expression, in terms of $n$, for the $n$th term of the sequence.",
        2, "Number Patterns — General Term", 4, (3, 0.53, 0.78),
        r"$9, 16, 25, 36 = 3^2, 4^2, 5^2, 6^2$\n$T_n = (n+2)^2$", "B2",
        stem=r"The first four terms of a sequence are 9, 16, 25 and 36.",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 7, "b",
        r"One term in the sequence is 100. Find the value of $n$ for the term.",
        2, "Number Patterns", 4, (3, 0.77, 0.95),
        r"$(n+2)^2 = 100$\n$n + 2 = 10$\n$n = 8$", "M1, A1 (FT from 7a)",
        topic_id=7)

    # Q8 — Page BP-97 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 8, "a",
        r"Solve $5x + 3 = 1\dfrac{1}{2}$.",
        2, "Linear Equations", 5, (4, 0.04, 0.35),
        r"$10x + 6 = 3$\n$10x = -3$\n$x = -\frac{3}{10}$", "M1, A1 (accept $-0.3$)",
        topic_id=5)

    add_q(db, p1.id, exam_dir, 1, 8, "b",
        r"Solve $\dfrac{2x+3}{2} + 1 = \dfrac{4+x}{2}$.",
        2, "Linear Equations", 5, (4, 0.34, 0.62),
        r"$\frac{2x + 3 + 2}{2} = \frac{4 + x}{2}$\n$2x + 5 = 4 + x$\n$x = -1$", "M1, A1",
        topic_id=5)

    # Q9 — Page BP-97 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 9, None,
        r"Mr Tan borrows $\$35000$ from a bank for a business. The bank charges simple interest at a rate of 3.75% per annum. Calculate the total amount he has to repay the bank at the end of 6 years.",
        3, "Simple Interest", 5, (4, 0.62, 0.95),
        r"Interest $= \frac{35000 \times 3.75 \times 6}{100} = \$7875$\nTotal amount $= 35000 + 7875 = \$42875$", "M1, M1, A1",
        topic_id=8)

    # Q10 — Page BP-98 (idx 5)
    add_q(db, p1.id, exam_dir, 1, 10, "a",
        r"How much, in Japanese Yen, did he bring to Japan?",
        2, "Currency Conversion", 6, (5, 0.04, 0.40),
        r"$\text{S\\$}5000 = 5000 \times 103 = 515000$ yen", "M1, A1",
        stem=r"Jason just returned from a holiday in Japan. Before his trip, Jason changed $\$5000$ Singapore Dollars to Japanese Yen using the exchange rate of 1 Singapore Dollar (S$\$$) = 103 Japanese Yen. After the trip, he returned with a remainder of 45000 Japanese Yen and wants to convert his remaining Japanese Yen into Singapore Dollars using the exchange rate of 1 Singapore Dollar (S$\$$) = 110 Japanese Yen.",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 10, "b",
        r"How much Singapore Dollars would he get after his trip?",
        2, "Currency Conversion", 6, (5, 0.39, 0.56),
        r"$45000 \div 110 = \text{S\\$}409.09$ (2 d.p.)", "M1, A1",
        topic_id=9)

    # Q11 — Page BP-98 (idx 5)
    add_q(db, p1.id, exam_dir, 1, 11, "a",
        r"Find the actual lifespan of battery C.",
        1, "Negative Numbers — Application", 6, (5, 0.56, 0.78),
        r"$5 + (-0.9) = 4.1$ hours", "B1",
        stem=r"A check was conducted on 4 batteries to determine the typical lifespan of each battery when used in a toy car. Each battery is expected to last for 5 hours.\n\n| Battery | A | B | C | D |\n|---|---|---|---|---|\n| Number of hours greater or less than the expected lifespan | $-0.5$ | $+1.2$ | $-0.9$ | $+1.7$ |",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 11, "b",
        r"Find the average lifespan of the four batteries.",
        2, "Average / Mean", 6, (5, 0.77, 0.95),
        r"Average $= \frac{4.5 + 6.2 + 4.1 + 6.7}{4} = \frac{21.5}{4} = 5.375$ hours (exact)", "M1, A1 (no A1 if written as 5.38)",
        topic_id=14)

    # Q12 — Page BP-99 (idx 6)
    add_q(db, p1.id, exam_dir, 1, 12, "a",
        r"Find an expression, in terms of $x$ and $y$, for the length of the rectangle.",
        3, "Algebraic Expressions — Perimeter", 7, (6, 0.04, 0.40),
        r"Length $= \frac{5x + 11y - 8 - 2(2x + 4y - 2)}{2} = \frac{5x + 11y - 8 - 4x - 8y + 4}{2} = \frac{x + 3y - 4}{2}$", "M1, M1, A1",
        stem=r"The perimeter of a rectangular field is $(5x + 11y - 8)$ m. The breadth of the rectangular field is $(2x + 4y - 2)$ m.",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 12, "b",
        r"It is given that $x = 4$ and that the breadth of the rectangle is 14 m. Find the area of the rectangle.",
        4, "Area — Rectangle", 7, (6, 0.39, 0.65),
        r"$2(4) + 4y - 2 = 14$\n$4y + 6 = 14$\n$y = 2$\nLength $= \frac{4 + 6 - 4}{2} = 3$ m\nArea $= 14 \\times 3 = 42$ m$^2$", "M1, M1, M1, A1 (FT)",
        topic_id=12)

    add_q(db, p1.id, exam_dir, 1, 12, "c",
        r"The cost to fence the field is $\$9.50$ per metre. Find the total cost of fencing the rectangular field.",
        2, "Perimeter — Application", 7, (6, 0.64, 0.90),
        r"Perimeter $= 5(4) + 11(2) - 8 = 34$ m\nTotal Cost $= 34 \\times 9.50 = \$323$", "M1, A1 (FT)",
        topic_id=12)

    # Q13 — Page BP-100 (idx 7)
    add_q(db, p1.id, exam_dir, 1, 13, "a",
        r"Calculate the total cost of the dinner inclusive of the service charge and GST.",
        2, "Percentage — Service Charge & GST", 8, (7, 0.04, 0.35),
        r"Total Cost $= 108 \\times 1.1 \\times 1.08 = \$128.30$ (2 d.p.)", "A1 (accept M1 A1)",
        stem=r"Tom, Jane and Harry had a dinner in a restaurant. They ordered $\$108$ worth of food and decided to pay for the dinner in the ratio of $4 : 2 : 3$. The total bill of the dinner is inclusive of a 10% service charge and a Goods and Services Tax (GST) of 8%.",
        topic_id=8)

    add_q(db, p1.id, exam_dir, 1, 13, "b",
        r"Calculate how much more Harry had to pay compared to Jane.",
        2, "Ratio", 8, (7, 0.34, 0.62),
        r"Amount Harry pays more $= \frac{1}{9} \\times 128.30 = \$14.26$ (2 d.p.)", "M1, A1",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 13, "c",
        r"If the restaurant offered a 15% discount, how much less would Tom have paid?",
        2, "Percentage — Discount", 8, (7, 0.61, 0.92),
        r"Savings $= 108 \\times \frac{4}{9} \\times 0.15 \\times 1.1 \\times 1.08 = \$8.55$ (2 d.p.)", "M1, A1 (FT from a)",
        topic_id=8)

    # ══════════════════════════════════════════════
    # PAPER 2 — 4052/02, 5 Oct 2023, 50 marks, 1h30m
    # Pages BP-102 to BP-110 = PDF pages 10-18 (idx 9-17)
    # ══════════════════════════════════════════════
    p2 = Paper(exam_id=exam.id, paper_number=2, duration_minutes=90, total_marks=50,
               date=date(2023, 10, 5), instructions="Answer all questions.")
    db.add(p2); db.flush()

    # P2 Q1 — Page BP-102 (idx 9)
    add_q(db, p2.id, exam_dir, 2, 1, "a",
        r"Find the difference between the cash price and the hire purchase price.",
        2, "Hire Purchase", 10, (9, 0.06, 0.36),
        r"Hire purchase price $= 6500 \\times 20\% + 24 \\times 260 = 1300 + 6240 = 7540$\nDifference $= 7540 - 6500 = \$1040$", "M1, A1",
        stem=r"The cash price of a piano is $\$6500$. It is available on hire purchase by paying a 20% deposit of the cash price and 24 monthly payments of $\$260$.",
        topic_id=8)

    add_q(db, p2.id, exam_dir, 2, 1, "b",
        r"Express this difference as a percentage of the cash price.",
        2, "Percentage", 10, (9, 0.35, 0.54),
        r"$\frac{1040}{6500} \\times 100 = 16\%$", "M1FT, A1",
        topic_id=8)

    # P2 Q2 — Page BP-102 (idx 9)
    add_q(db, p2.id, exam_dir, 2, 2, "a",
        r"If $a : b : c = 3 : 4 : 5$ and $a + b = 84$, find the value of $a + b - c$.",
        2, "Ratio", 10, (9, 0.54, 0.74),
        r"7 units $= 84$\n1 unit $= 12$\n$a + b - c = 84 - 5(12) = 24$", "M1, A1",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 2, "b",
        r"Given that $(x - y) : (y - 2x) = 2 : 3$, find $x : y$.",
        3, "Ratio — Algebraic", 10, (9, 0.73, 0.95),
        r"$\frac{x - y}{y - 2x} = \frac{2}{3}$\n$3(x - y) = 2(y - 2x)$\n$3x - 3y = 2y - 4x$\n$7x = 5y$\n$x : y = 5 : 7$", "M1, M1, A1",
        topic_id=9)

    # P2 Q3 — Page BP-103 (idx 10)
    add_q(db, p2.id, exam_dir, 2, 3, None,
        r"Shanti Pereira won the 100-meter gold medal at the Asian Athletics Championships in July. Her blistering time of 11.20 seconds was a new national record for Singapore. Express Shanti's speed in km/h.",
        2, "Speed Conversion", 11, (10, 0.04, 0.30),
        r"Speed $= \frac{100 \div 1000}{11.20 \div 3600} = 32.1$ km/h (3 s.f.)", "M1, A1",
        topic_id=9)

    # P2 Q4 — Page BP-103 (idx 10)
    add_q(db, p2.id, exam_dir, 2, 4, "a",
        r"angle $QRT$.",
        1, "Angle Properties — Parallel Lines", 11, (10, 0.30, 0.70),
        r"$\angle QRT = \angle PQU = 56°$ (corresponding angles)", "B1",
        stem=r"In the diagram, $PR$ is parallel to $ST$, $QU$ is parallel to $RT$, angle $PQU = 56°$, angle $TSU = 120°$ and angle $QTR = 65°$. Stating your reasons clearly, calculate",
        topic_id=10)

    add_q(db, p2.id, exam_dir, 2, 4, "b",
        r"angle $QTS$.",
        2, "Angle Properties", 11, (10, 0.69, 0.82),
        r"$\angle QTS = 180° - 56° - 65° = 59°$ (interior angles)", "M1FT, A1",
        topic_id=10)

    add_q(db, p2.id, exam_dir, 2, 4, "c",
        r"angle $QUS$.",
        2, "Angle Properties", 11, (10, 0.81, 0.97),
        r"$\angle QUS = (180° - 120°) + 56° = 116°$ (interior angle and alternate angle, or angle sum of quadrilateral)", "M1, A1",
        topic_id=10)

    # P2 Q5 — Page BP-104 (idx 11)
    add_q(db, p2.id, exam_dir, 2, 5, "a",
        r"Construct triangle $ABC$ such that $AB = 6.5$ cm and $BC = 7$ cm and angle $ABC = 124°$.",
        2, "Construction", 12, (11, 0.04, 0.55),
        r"Shape of triangle with obtuse angle [B1]. All measurements are correct [B1].", "B1, B1",
        topic_id=10)

    add_q(db, p2.id, exam_dir, 2, 5, "b",
        r"Measure the length of $AC$.",
        1, "Construction — Measurement", 12, (11, 0.54, 0.65),
        r"$AC = 11.8$ / $11.9$ / $12.0$ cm", "B1",
        topic_id=10)

    add_q(db, p2.id, exam_dir, 2, 5, "c",
        r"$D$ is a point in triangle $ABC$ such that it is 5 cm from $A$ and 7.5 cm from $C$. On the same diagram, construct and measure the length of $BD$.",
        2, "Construction — Loci", 12, (11, 0.64, 0.78),
        r"Arcs with 5 cm and 7.5 cm radius centered at $A$ and $C$ respectively. $BD = 1.7$ / $1.8$ cm", "B1, B1 (deduct P if point $D$ is not labelled)",
        topic_id=10)

    # P2 Q6 — Page BP-105 (idx 12)
    add_q(db, p2.id, exam_dir, 2, 6, "a",
        r"The size of the interior angle of a regular polygon is 4 times the size of its exterior angle. Find the number of sides of the polygon.",
        2, "Polygon — Interior/Exterior Angles", 13, (12, 0.04, 0.50),
        r"$5$ units $= 180°$\n$1$ unit $= 36°$\nExterior angle $= 36°$\nNumber of sides $= 360° \div 36° = 10$", "M1, A1",
        topic_id=11)

    add_q(db, p2.id, exam_dir, 2, 6, "b",
        r"Tim claims that the exterior angle of a regular polygon cannot be $25°$. Explain why Tim is right.",
        2, "Polygon — Reasoning", 13, (12, 0.49, 0.75),
        r"If exterior angle $= 25°$, then number of sides $= 360° \div 25° = 14.4$. This cannot be true because the number of sides must be a whole number. Hence Tim is right.", "M1, A1",
        topic_id=11)

    # P2 Q7 — Page BP-106 (idx 13)
    add_q(db, p2.id, exam_dir, 2, 7, "a",
        r"the perimeter of the shaded region.",
        3, "Perimeter — Circles in Rectangle", 14, (13, 0.04, 0.55),
        r"Perimeter $= 2(14 + 4 \\times 14) + 4(2\pi)(7) = 2(14 + 56) + 56\pi = 140 + 56\pi = 316$ cm (3 s.f.)", "M1 for rectangle, M1 for circles, A1",
        stem=r"The diagram below shows 4 circles that are drawn to fit into a rectangle. The radius of each circle is 7 cm. Find",
        topic_id=12)

    add_q(db, p2.id, exam_dir, 2, 7, "b",
        r"the area of the shaded region.",
        2, "Area — Circles in Rectangle", 14, (13, 0.54, 0.90),
        r"Area $= 14(56) - 4\pi(7)^2 = 784 - 196\pi = 168$ cm$^2$ (3 s.f.)", "M1, A1",
        topic_id=12)

    # P2 Q8 — Page BP-107 (idx 14)
    add_q(db, p2.id, exam_dir, 2, 8, "a",
        r"Given that the pool is completely filled with water, find the total surface area of the pool that is **in contact** with the water.",
        3, "Surface Area — Trapezium Pool", 15, (14, 0.04, 0.58),
        r"Total SA $= 2 \\times \frac{1}{2}(1+4)(50) + 1(30) + 4(30) + 50.1(30) = 250 + 30 + 120 + 1503 = 1903$ m$^2$", "M1 for cross section, M1 for rectangular areas, A1",
        stem=r"The diagram shows a swimming pool with a trapezium as its cross section. The length and width of the pool are 50 m and 30 m respectively. The depth of the pool is 1 m at its shallow end and 4 m at its deep end.",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 8, "b",
        r"Find the volume of the water in the pool.",
        2, "Volume — Trapezoidal Prism", 15, (14, 0.57, 0.90),
        r"Volume $= \frac{1}{2}(1 + 4)(50)(30) = 3750$ m$^3$", "M1, A1",
        topic_id=13)

    # P2 Q9 — Page BP-108 (idx 15)
    add_q(db, p2.id, exam_dir, 2, 9, "a",
        r"Find the average number of friends these students have on the social media platform.",
        2, "Statistics — Mean", 16, (15, 0.04, 0.58),
        r"Average $= \frac{80 + 60 + 100 + 120}{4} = 90$", "M1, A1",
        stem=r"The bar graph shows the number of friends that four students have respectively on a social media platform.",
        topic_id=14)

    add_q(db, p2.id, exam_dir, 2, 9, "b",
        r"Find the ratio of the height of the bar representing the number of friends of Alan to that of Doris.",
        1, "Ratio", 16, (15, 0.57, 0.72),
        r"$80 : 120 = 1 : 2$ (or reading from bar heights)", "B1",
        topic_id=14)

    add_q(db, p2.id, exam_dir, 2, 9, "c",
        r"By observing the graph, Doris said that her number of friends on the social media platform was twice as many as Alan's. Explain why Doris is not correct.",
        1, "Statistics — Misleading Graphs", 16, (15, 0.71, 0.95),
        r"The vertical axis does not start from 0, so the visual comparison of bar heights is misleading. Twice as many as Alan's (80) would be 160, but Doris has only 120 friends.", "B1 (accept other reasonable explanations)",
        topic_id=14)

    # P2 Q10 — Page BP-109 (idx 16)
    add_q(db, p2.id, exam_dir, 2, 10, "a",
        r"Express, in terms of $x$, the usual time Tom takes to cycle from his house to his school.",
        1, "Speed — Expression", 17, (16, 0.04, 0.30),
        r"$\frac{x}{12}$ hours", "B1",
        stem=r"Tom cycles from his house to his school at a usual speed 12 km/h. If he increases his speed to 25 km/h, he will reach his school 8 minutes earlier. The distance between Tom's house and his school is $x$ km.",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 10, "b",
        r"Express, in terms of $x$, the time Tom takes if he cycles at the faster speed.",
        1, "Speed — Expression", 17, (16, 0.29, 0.44),
        r"$\frac{x}{25}$ hours", "B1",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 10, "c",
        r"Using your answers in parts **(a)** and **(b)**, form an equation, in terms of $x$, to describe the difference in time Tom takes to cycle from his house to his school.",
        1, "Speed — Forming Equation", 17, (16, 0.43, 0.62),
        r"$\frac{x}{12} - \frac{x}{25} = \frac{8}{60}$", "B1",
        topic_id=5)

    add_q(db, p2.id, exam_dir, 2, 10, "d",
        r"Solve the equation in part **(c)** to find the distance between Tom's house and his school.",
        3, "Linear Equations — Speed Problem", 17, (16, 0.61, 0.95),
        r"$\frac{25x - 12x}{300} = \frac{8}{60}$\n$\frac{13x}{300} = \frac{8}{60}$\n$13x = 40$\n$x = \frac{40}{13} = 3.08$ km (3 s.f.)", "M1FT, M1FT, A1 (accept $3\frac{1}{13}$ km)",
        topic_id=5)

    # P2 Q11 — Page BP-110 (idx 17)
    add_q(db, p2.id, exam_dir, 2, 11, "a",
        r"Write down the 7th term in the sequence.",
        1, "Number Patterns", 18, (17, 0.04, 0.27),
        r"$29$", "B1",
        stem=r"The first four terms in a sequence are 5, 9, 13 and 17.",
        topic_id=7)

    add_q(db, p2.id, exam_dir, 2, 11, "b",
        r"Find an expression, in terms of $n$, for the $n$th term in the sequence. Write the expression in its simplest form.",
        2, "Number Patterns — General Term", 18, (17, 0.26, 0.55),
        r"$T_n = 5 + (n-1)(4) = 5 + 4n - 4 = 4n + 1$", "M1, A1 (or B2)",
        topic_id=7)

    add_q(db, p2.id, exam_dir, 2, 11, "c",
        r"Explain why 131 is not a term in the sequence. Show your working clearly.",
        2, "Number Patterns — Reasoning", 18, (17, 0.54, 0.90),
        r"$4n + 1 = 131$\n$4n = 130$\n$n = 32.5$\n$n$ must be a whole number, so 131 is not a term in the sequence.", "M1FT, A1 (only with working)",
        topic_id=7)

    db.commit()
    p1_count = len(p1.questions)
    p2_count = len(p2.questions)
    print(f"Seeded Bedok View 2023 exam id={exam.id}: Paper 1 ({p1_count} parts), Paper 2 ({p2_count} parts)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
