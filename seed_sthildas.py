"""Seed St. Hilda's Secondary School SA2 2020 Sec 1 Express Math exam."""

import os
import shutil
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/66a8bac8ed99d_3605.pdf"
IMAGES_DIR = "/tmp/sthildas_pages"

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

    school = db.query(School).filter(School.name == "St. Hilda's Secondary School").first()
    if not school:
        school = School(name="St. Hilda's Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(Exam.school_id == school.id, Exam.year == 2020).first()
    if existing:
        print(f"St. Hilda's 2020 already seeded (id={existing.id}). Deleting and re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id, title="End-of-Year Examination 2020", year=2020,
        level="Secondary 1 Express", subject="Mathematics",
        source_pdf="66a8bac8ed99d_3605.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # Single Paper — Pages 2-17 (idx 1-17), 80 marks, 2 hours
    # Section A (Q1-15): 40 marks, Section B (Q16-24): 40 marks
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=120, total_marks=80,
               date=date(2020, 10, 6), instructions="Answer all questions.")
    db.add(p1); db.flush()

    # ── Section A ──

    # Q1 — Page 2 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 1, None,
        r"$x$ grams of beansprouts cost 60 cents. Find an expression, in terms of $x$ and $y$, for the number of grams of beansprouts that can be bought for $y$ dollars.",
        1, "Algebra — Expressions", 2, (2, 0.07, 0.28),
        r"$$\frac{100y \times x}{60} = \frac{5xy}{3} \text{ grams}$$", "B1",
        topic_id=4)

    # Q2 — Page 2 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 2, "a",
        r"$p^2 q$",
        1, "Substitution", 2, (2, 0.28, 0.48),
        r"$(-2)^2(7) = 4 \times 7 = 28$. Note: $(-2)^2 = 4$ not $-4$.", "B1",
        stem=r"Given that $p = -2$ and $q = 7$, evaluate each of the following expressions.",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 2, "b",
        r"$\dfrac{8q - p}{p + q}$",
        1, "Substitution", 2, (2, 0.47, 0.63),
        r"$$\frac{8(7) - (-2)}{(-2) + 7} = \frac{56 + 2}{5} = \frac{58}{5} = 11.6$$", "B1",
        topic_id=2)

    # Q3 — Page 2 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 3, "a",
        r"What is the highest temperature recorded in desert $A$?",
        1, "Integers — Temperature", 2, (2, 0.63, 0.82),
        r"$-7 + 45.9 = 38.9°$C", "B1",
        stem=r"The lowest temperature recorded in desert $A$ is $-7°$C. The difference between the highest and lowest temperature is $45.9°$C.",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 3, "b",
        r"The lowest temperature in desert $B$ is $6°$C less than that in desert $A$. What is the lowest temperature recorded in desert $B$?",
        1, "Integers — Temperature", 2, (2, 0.81, 0.97),
        r"$-7 - 6 = -13°$C", "B1",
        topic_id=2)

    # Q4 — Page 3 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 4, "a",
        r"Explain what a myopia rate of 40% means.",
        1, "Percentage — Interpretation", 3, (3, 0.05, 0.30),
        r"It means that for every 100 students in SHSS, there are 40 students who are myopic.", "B1",
        stem=r"All SHSS students went through a health screening exercise. It was found that the myopia rate among the students was 40%. Myopia rate is calculated by dividing the number of students who are short-sighted by the entire SHSS student population, and then expressed as a percentage.",
        topic_id=3)

    add_q(db, p1.id, exam_dir, 1, 4, "b",
        r"The myopia rate of 40% is correct to $k$ significant figure. Explain why $k$ can be 1.",
        1, "Significant Figures", 3, (3, 0.29, 0.44),
        r"The first digit 4 is a non-zero digit and it is significant. Therefore it can be 1 s.f. or 2 s.f.", "B1",
        topic_id=3)

    # Q5 — Page 3 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 5, "a",
        r"State the number of significant figures in $8.7010$.",
        1, "Significant Figures", 3, (3, 0.44, 0.57),
        r"5 s.f.", "B1",
        topic_id=3)

    add_q(db, p1.id, exam_dir, 1, 5, "b",
        r"State the number of significant figures in $0.02005$.",
        1, "Significant Figures", 3, (3, 0.56, 0.68),
        r"4 s.f.", "B1",
        topic_id=3)

    # Q6 — Page 3 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 6, "a",
        r"Factorise completely $6xyz + 2xz$.",
        1, "Factorisation", 3, (3, 0.68, 0.82),
        r"$2xz(3y + 1)$", "B1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 6, "b",
        r"Factorise completely $-9h^3 - 15h$.",
        1, "Factorisation", 3, (3, 0.81, 0.96),
        r"$-3h(3h^2 + 5)$", "B1",
        topic_id=4)

    # Q7 — Page 4 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 7, "a",
        r"Subtract $3y$ from the product of $x$ and $4z$.",
        1, "Algebraic Expressions", 4, (4, 0.05, 0.19),
        r"$4xz - 3y$", "B1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 7, "b",
        r"Divide 5 by the sum of $7a$ and 2.",
        1, "Algebraic Expressions", 4, (4, 0.18, 0.33),
        r"$\dfrac{5}{7a + 2}$", "B1",
        topic_id=4)

    # Q8 — Page 4 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 8, "a",
        r"Express 300 as a product of its prime factors.",
        1, "Prime Factorisation", 4, (4, 0.33, 0.56),
        r"$300 = 2^2 \times 3 \times 5^2$", "B1",
        stem=r"Written as a product of its prime factors $5880 = 2^3 \times 3 \times 5 \times 7^2$.",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 8, "b",
        r"Hence, write down the greatest integer that will divide both 300 and 5880 exactly.",
        1, "HCF", 4, (4, 0.55, 0.70),
        r"$\text{HCF} = 2^2 \times 3 \times 5 = 60$", "B1",
        topic_id=1)

    # Q9 — Page 4 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 9, "a",
        r"Find the smallest integer $k$ such that $kq$ is a perfect square.",
        1, "Perfect Square", 4, (4, 0.70, 0.88),
        r"$k = 2 \times 3 = 6$ (need all even powers)", "B1",
        stem=r"$p = 2^4 \times 3^2 \times 7^2 \times 11^4$, $q = 2 \times 3^3 \times 7^2$.",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 9, "b",
        r"Find the square root of $p$, leaving your answer as a product of its prime factors.",
        1, "Square Root — Prime Factors", 4, (4, 0.87, 0.98),
        r"$\sqrt{p} = 2^2 \times 3 \times 7 \times 11^2$", "B1",
        topic_id=1)

    # Q10 — Page 5 (idx 5)
    add_q(db, p1.id, exam_dir, 1, 10, "a",
        r"What fraction of the cost does Cloe pay?",
        1, "Fractions", 5, (5, 0.05, 0.28),
        r"$$1 - \frac{40}{100} - \frac{1}{3} = 1 - \frac{2}{5} - \frac{1}{3} = \frac{15 - 6 - 5}{15} = \frac{4}{15}$$", "B1",
        stem=r"Ashwin, Bennett and Cloe share the cost of a cake. Ashwin pays 40% of the cost, Bennett pays $\frac{1}{3}$ and Cloe pays the rest.",
        topic_id=8)

    add_q(db, p1.id, exam_dir, 1, 10, "b",
        r"Given that Ashwin pays $\$5.20$ more than Bennett, find the total cost of the cake.",
        2, "Percentage — Word Problem", 5, (5, 0.27, 0.45),
        r"""$$\frac{40}{100} - \frac{1}{3} = \frac{2}{5} - \frac{1}{3} = \frac{1}{15}$$
$\frac{1}{15}$ of cost $= \$5.20$
Total cost $= 15 \times 5.20 = \$78$""", "M1, A1",
        topic_id=8)

    # Q11 — Page 5 (idx 5)
    add_q(db, p1.id, exam_dir, 1, 11, "a",
        r"Arrange the following numbers in ascending order: $13$, $3$, $0.\dot{3}$, $\dfrac{3}{10}$, $30$.",
        1, "Number Ordering", 5, (5, 0.45, 0.65),
        r"$\dfrac{3}{10}, 0.\dot{3}, 3, 13, 30$", "B1",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 11, "bi",
        r"prime number(s)",
        1, "Prime Numbers", 5, (5, 0.64, 0.78),
        r"$3, 13$", "B1",
        stem=r"Using the numbers given in (a), write down the:",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 11, "bii",
        r"rational number(s)",
        1, "Rational Numbers", 5, (5, 0.77, 0.92),
        r"$3, 13, 0.\dot{3}, \dfrac{3}{10}, 30$", "B1",
        topic_id=2)

    # Q12 — Page 6 (idx 6)
    add_q(db, p1.id, exam_dir, 1, 12, "a",
        r"Complete the table of values for the graph.",
        1, "Linear Functions — Table", 6, (6, 0.05, 0.58),
        r"$x = -3 \implies y = 2$; $x = 0 \implies y = 4$; $x = 3 \implies y = 6$. So the table is: $2, 4, 6$ (or $-4, 0, 8$ depending on reading).", "B1",
        stem=r"A linear graph is shown.",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 12, "b",
        r"Find the equation of the line.",
        2, "Linear Functions — Equation", 6, (6, 0.57, 0.74),
        r"$$y = \frac{2}{3}x + 4$$", "M1, A1",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 12, "c",
        r"Does the line pass through the point $(-6, -5)$? Explain using your answer in (b).",
        1, "Linear Functions — Substitution", 6, (6, 0.73, 0.95),
        r"$y = \frac{2}{3}(-6) + 4 = -4 + 4 = 0 \neq -5$. The line does not pass through the point.", "B1",
        topic_id=6)

    # Q13 — Page 7 (idx 7)
    add_q(db, p1.id, exam_dir, 1, 13, "a",
        r"$\angle ECD$",
        1, "Angle Properties — Parallel Lines", 7, (7, 0.05, 0.36),
        r"$\angle ECD = 120°$ (corr. angles, $EC \parallel AB$)", "B1",
        stem=r"In the diagram below, not drawn to scale, $\angle ABC = 120°$ and $\angle ACD = 160°$. $AB$ is parallel to $EC$. $BCD$ is a straight line. Stating your reasons clearly, calculate:",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 13, "b",
        r"$\angle BAC$",
        1, "Angle Properties", 7, (7, 0.35, 0.52),
        r"$\angle BCA = 160° - 120° = 40°$. $\angle BAC = 40°$ (alt. angles, $EC \parallel AB$)", "B1",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 13, "c",
        r"$\angle ACB$",
        1, "Angle Properties", 7, (7, 0.51, 0.68),
        r"$\angle ACB = 180° - 160° = 20°$ (adj. angles on str. line)", "B1",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 13, "d",
        r"Reflex $\angle ABC$",
        1, "Angle Properties", 7, (7, 0.67, 0.88),
        r"Reflex $\angle ABC = 360° - 120° = 240°$ (angles at a point)", "B1",
        topic_id=10)

    # Q14 — Page 8 (idx 8)
    add_q(db, p1.id, exam_dir, 1, 14, "ai",
        r"the value of $k$",
        1, "Number Patterns", 8, (8, 0.05, 0.20),
        r"$k = 16$ (common difference is 7)", "B1",
        stem=r"In the sequence $9, k, 23, 30, 37, 44, \ldots$ find:",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 14, "aii",
        r"the expression for the $n$th term of the sequence",
        1, "Number Patterns — General Term", 8, (8, 0.19, 0.34),
        r"$T_n = 7n + 2$", "B1",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 14, "aiii",
        r"the 40th term in the sequence",
        1, "Number Patterns", 8, (8, 0.33, 0.46),
        r"$T_{40} = 7(40) + 2 = 282$", "B1",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 14, "b",
        r"Is 220 a term of the sequence shown in (a)? Explain your answer.",
        1, "Number Patterns — Reasoning", 8, (8, 0.45, 0.60),
        r"""$T_n = 7n + 2 = 220$
$7n = 218$
$n = 31\frac{1}{7}$
Since $n$ is not a whole number, 220 is not a term in the sequence.""", "B1",
        topic_id=7)

    # Q15 — Page 8 (idx 8)
    add_q(db, p1.id, exam_dir, 1, 15, "a",
        r"Expand and simplify $1 + 3(1 - 3p)$.",
        2, "Algebra — Expansion", 8, (8, 0.60, 0.76),
        r"$1 + 3 - 9p = 4 - 9p$", "M1, A1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 15, "b",
        r"Express $\dfrac{5x}{8} - \dfrac{3y + x}{2}$ as a single fraction in its simplest form.",
        3, "Algebraic Fractions", 8, (8, 0.75, 0.97),
        r"$$\frac{5x}{8} - \frac{4(3y + x)}{8} = \frac{5x - 12y - 4x}{8} = \frac{x - 12y}{8}$$", "M1, M1, A1",
        topic_id=4)

    # ── Section B ──

    # Q16 — Page 9 (idx 9)
    add_q(db, p1.id, exam_dir, 1, 16, None,
        r"Three trains arrive at platform $A$, $B$ and $C$ every 180, 150 and 120 seconds respectively. On a weekday, the three trains first arrive together at the platforms at 05 55. The platforms close at 23 59 at night. Calculate the number of times the three trains arrive at the platforms together on a weekday.",
        3, "LCM — Word Problem", 9, (9, 0.07, 0.92),
        r"""$180 = 2^2 \times 3^2 \times 5$
$150 = 2 \times 3 \times 5^2$
$120 = 2^3 \times 3 \times 5$
$\text{LCM} = 2^3 \times 3^2 \times 5^2 = 1800$ s $= 30$ min
05 55 to 23 59 $= 18$ hours $4$ min (round down to 18 hours)
$18 \times 2 = 36$ times after first
$36 + 1 = 37$ times total""", "M1 for LCM, M1 for time, A1",
        topic_id=1)

    # Q17 — Page 10 (idx 10)
    add_q(db, p1.id, exam_dir, 1, 17, "a",
        r"Write an expression, in terms of $x$, for the length of the square after the increase.",
        1, "Percentage — Expression", 10, (10, 0.05, 0.38),
        r"$1.2x$ cm", "B1",
        stem=r"The length of each side of a square is increased by 20%. Let the original length of the square be $x$ cm.",
        topic_id=8)

    add_q(db, p1.id, exam_dir, 1, 17, "b",
        r"Determine if the area of the square increases by 40% after the increase in the length. Show your workings clearly.",
        3, "Percentage — Area", 10, (10, 0.37, 0.92),
        r"""Original area $= x^2$
New area $= (1.2x)^2 = 1.44x^2$
Percentage increase $= \dfrac{1.44x^2 - x^2}{x^2} \times 100\% = \dfrac{0.44x^2}{x^2} \times 100\% = 44\%$
The area of the square increases by 44%, not 40%.""",
        "M1 for new area, M1 for percentage, A1 for conclusion",
        topic_id=8)

    # Q18 — Page 11 (idx 11)
    add_q(db, p1.id, exam_dir, 1, 18, "a",
        r"Find the sum of all the interior angles of a hexagon.",
        1, "Polygon — Interior Angle Sum", 11, (11, 0.05, 0.20),
        r"$(6 - 4) \times 180° = 720°$. Note: should be $(6-2) \times 180° = 720°$.", "B1",
        topic_id=11)

    add_q(db, p1.id, exam_dir, 1, 18, "bi",
        r"Form an equation in $x$ and solve it.",
        2, "Polygon — Angles Equation", 11, (11, 0.19, 0.70),
        r"""$720 = 90 + 158 + 172 + 39 - 2x + 166 + 14x - 7$
$720 = 618 + 12x$
$12x = 102$
$x = 8.5$""", "M1, A1",
        stem=r"The diagram shows a closed hexagon with angles $158°$, $172°$, $(39 - 2x)°$, $166°$, $(14x - 7)°$ and a right angle.",
        topic_id=11)

    add_q(db, p1.id, exam_dir, 1, 18, "bii",
        r"Hence, find the value of the acute interior angle.",
        1, "Polygon — Angles", 11, (11, 0.69, 0.92),
        r"$39 - 2(8.5) = 39 - 17 = 22°$", "B1",
        topic_id=11)

    # Q19 — Page 12 (idx 12)
    add_q(db, p1.id, exam_dir, 1, 19, "a",
        r"Find the area of the field.",
        2, "Area — Composite Shape", 12, (12, 0.05, 0.53),
        r"""Height of trapezium $= 7 - 4 = 3$
Total area $= $ area of trapezium $+$ area of rectangle
$= \frac{1}{2}(8 + 16)(3) + 4 \times 16 = 36 + 64 = 100$ km$^2$""", "M1, A1",
        stem=r"The figure below shows a field consisting of a trapezium $ABCF$ and a rectangle $CDEF$. $AB = 8$ km, $CD = FE = 4$ km, $ED = 16$ km and $AF = BC$.",
        topic_id=12)

    add_q(db, p1.id, exam_dir, 1, 19, "b",
        r"At 7 am, Jared started his training for marathon by running along the perimeter of the field at a constant speed of 7 km/h. He finished running one round around the field at 1 pm. Calculate the length $AF$.",
        3, "Speed, Distance, Time", 12, (12, 0.52, 0.95),
        r"""7 am to 1 pm $= 6$ h
Total distance $= 7 \times 6 = 42$ km
$AF = (42 - 16 - 8 - 4 - 4) \div 2 = \frac{10}{2} = 5$ km""", "M1 for distance, M1 for perimeter equation, A1",
        topic_id=9)

    # Q20 — Page 13 (idx 13)
    add_q(db, p1.id, exam_dir, 1, 20, "a",
        r"Using a pair of compasses and ruler, construct trapezium $ABCD$.",
        3, "Construction", 13, (13, 0.05, 0.65),
        r"Draw $BC = 7$ cm arc from $B$. $\angle ABC = 90°$ using perpendicular from $B$. $AB \parallel CD$ (trapezium). Measured $AB \approx 8$ cm.", "B1 for right angle, B1 for BC, B1 for parallel sides",
        stem=r"$ABCD$ is a trapezium with $BC = 7$ cm, $\angle BAD = 100°$ and $\angle ABC$ is a right angle. $AB$ has already been drawn.",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 20, "b",
        r"Calculate the area of trapezium $ABCD$.",
        2, "Area — Trapezium", 13, (13, 0.64, 0.92),
        r"$$= \frac{1}{2}(8 + 9.3)(7) = \frac{1}{2}(17.3)(7) = 60.55 \text{ cm}^2$$", "M1, A1",
        topic_id=12)

    # Q21 — Page 14 (idx 14)
    add_q(db, p1.id, exam_dir, 1, 21, "a",
        r"Write down an expression, in terms of $m$, for the cost, in dollars, of each apple.",
        1, "Algebra — Expressions", 14, (14, 0.05, 0.17),
        r"$\$\dfrac{12}{m}$", "B1",
        stem=r"A trader bought $m$ apples for $\$12$.",
        topic_id=5)

    add_q(db, p1.id, exam_dir, 1, 21, "b",
        r"It was found that 3 of the apples were bad and could not be sold. The trader sold each remaining apple at $\$1.50$. Write down an expression, in terms of $m$, for the amount of money, in dollars, received from the sales of the remaining apples.",
        1, "Algebra — Expressions", 14, (14, 0.16, 0.38),
        r"$\$1.5(m - 3)$. Accept $\$1.50(m - 3)$.", "B1",
        topic_id=5)

    add_q(db, p1.id, exam_dir, 1, 21, "c",
        r"The trader made a 25% profit from the sales of the apples. Write down an equation to represent this information and show that it reduces to $1.5m = 19.5$.",
        2, "Linear Equations — Word Problem", 14, (14, 0.37, 0.60),
        r"""$1.5(m - 3) = \frac{125}{100}(12)$
$1.5m - 4.5 = 15$
$1.5m = 15 + 4.5$
$1.5m = 19.5$ (shown)""", "M1, A1",
        topic_id=5)

    add_q(db, p1.id, exam_dir, 1, 21, "d",
        r"Solve the equation $1.5m = 19.5$.",
        1, "Linear Equations", 14, (14, 0.59, 0.72),
        r"$m = 19.5 \div 1.5 = 13$", "B1",
        topic_id=5)

    add_q(db, p1.id, exam_dir, 1, 21, "e",
        r"Find the number of remaining apples sold.",
        1, "Linear Equations — Application", 14, (14, 0.71, 0.87),
        r"$m - 3 = 13 - 3 = 10$ apples", "B1",
        topic_id=5)

    # Q22 — Page 15 (idx 15)
    add_q(db, p1.id, exam_dir, 1, 22, None,
        r"The diagram shows a kite $PQRS$. Giving your reasons clearly, explain why $w$ is $24°$.",
        2, "Angle Properties — Kite", 15, (15, 0.05, 0.48),
        r"""$\angle QPS = 180° - 66° - 66° = 48°$ (angle sum of triangle, and kite symmetry)
$\angle QPR = 48° \div 2 = 24°$ (property of kite: diagonal bisects angle)
$w = 24°$""", "M1, A1",
        topic_id=10)

    # Q23 — Page 15 (idx 15)
    add_q(db, p1.id, exam_dir, 1, 23, "a",
        r"Solve $5(q + 3) = 17$.",
        2, "Linear Equations", 15, (15, 0.48, 0.72),
        r"""$5q + 15 = 17$
$5q = 2$
$q = \frac{2}{5}$""", "M1, A1",
        topic_id=5)

    add_q(db, p1.id, exam_dir, 1, 23, "b",
        r"Solve $\dfrac{2m - 15}{7m + 1} = \dfrac{1}{3}$.",
        3, "Linear Equations — Fractions", 15, (15, 0.71, 0.97),
        r"""$3(2m - 15) = 7m + 1$
$6m - 45 = 7m + 1$
$-45 - 1 = 7m - 6m$
$m = -46$""", "M1 for cross-multiply, M1 for expanding, A1",
        topic_id=5)

    # Q24 — Pages 16-17 (idx 16-17)
    add_q(db, p1.id, exam_dir, 1, 24, "ai",
        r"calculate the base radius of the cylinder.",
        1, "Cylinder — Dimensions", 16, (16, 0.05, 0.55),
        r"Ratio of base radius to height $= 1 : 4$. Height $= 21$ cm. $r = 21 \div 4 = 5.25$ cm.", "B1",
        stem=r"A rectangular piece of thin metal sheet $ABCD$ is shown in Figure 1. The same piece of metal sheet is rolled up to form a cylinder shown in Figure 2. Points $A$ and $C$ are joined to $B$ and $D$ respectively, with no overlap. The ratio of the base radius of the cylinder to its height is $1 : 4$. Given that the height of the cylinder is 21 cm.",
        topic_id=13)

    add_q(db, p1.id, exam_dir, 1, 24, "aii",
        r"find the area of the metal sheet shown in Figure 1, leaving your answer in terms of $\pi$.",
        2, "Surface Area — Cylinder", 16, (16, 0.54, 0.82),
        r"$$\text{Area} = 2\pi r \times h = 2\pi(5.25)(21) = 220.5\pi \text{ cm}^2$$", "M1, A1",
        topic_id=13)

    add_q(db, p1.id, exam_dir, 1, 24, "b",
        r"The bottom of the cylinder is sealed with metal of negligible thickness. Water is poured into the hollow cylinder at a rate of 80 cm$^3$/s. Alex claims that the cylinder would be completely filled within 20 seconds. Justify if this is true.",
        3, "Volume — Cylinder", 17, (17, 0.05, 0.82),
        r"""Volume $= \pi r^2 h = \pi(5.25)^2(21) = \pi(27.5625)(21) = 578.8125\pi \approx 1818.4$ cm$^3$ (or $1820$ cm$^3$ to 3 s.f.)
After 20 s, water $= 80 \times 20 = 1600$ cm$^3$
$1600 < 1820$
The claim is not true. The cylinder is not completely filled after 20 s.
(OR: Time needed $= 1818.4 \div 80 = 22.7$ s $> 20$ s.)""",
        "M1 for volume, M1 for comparison, A1 for conclusion",
        topic_id=13)

    db.commit()
    q_count = len(p1.questions)
    print(f"Seeded St. Hilda's exam id={exam.id}: Paper 1 ({q_count} parts)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
