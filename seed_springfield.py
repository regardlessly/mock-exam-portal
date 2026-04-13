"""Seed Springfield Secondary School EOY 2023 Sec 1 Express Math exam."""

import os
import shutil
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/Springfield-Secondary-EOY-2023-Sec-1-Math-Group-3.pdf"
IMAGES_DIR = "/tmp/springfield_pages"

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

    school = db.query(School).filter(School.name == "Springfield Secondary School").first()
    if not school:
        school = School(name="Springfield Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(Exam.school_id == school.id, Exam.year == 2023).first()
    if existing:
        print(f"Springfield 2023 already seeded (id={existing.id}). Deleting and re-seeding.")
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
        source_pdf="Springfield-Secondary-EOY-2023-Sec-1-Math-Group-3.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # Single paper — Pages 2-17 (idx 1-16), 80 marks, 2 hours
    # Section A (40 marks) + Section B (40 marks)
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=120, total_marks=80,
               date=date(2023, 10, 2), instructions="Answer all questions.")
    db.add(p1); db.flush()

    # ── SECTION A (40 Marks) ──────────────────────

    # Q1 — Page 2 (idx 1)
    add_q(db, p1.id, exam_dir, 1, 1, None,
        r"Write the following numbers in order of size, starting with the smallest: $\sqrt[3]{\dfrac{1}{17}}$, $\sqrt{0.15}$, $0.\dot{7}$, $37\%$.",
        1, "Ordering Real Numbers", 2, (1, 0.07, 0.24),
        r"$0.\dot{7}$, $37\%$, $\sqrt{0.15}$, $\sqrt[3]{\dfrac{1}{17}}$", "B1",
        topic_id=2)

    # Q2 — Page 2 (idx 1)
    add_q(db, p1.id, exam_dir, 1, 2, None,
        r"The number of Instagram users in early 2023 was $2\,700\,000$, correct to 2 significant figures. Write down the largest possible number of Instagram users.",
        1, "Approximation / Significant Figures", 2, (1, 0.25, 0.40),
        r"$2\,749\,999$", "B1",
        topic_id=3)

    # Q3 — Page 2 (idx 1)
    add_q(db, p1.id, exam_dir, 1, 3, "a",
        r"Calculate $\dfrac{0.43}{2.75^2 - \pi}$. Write down the first five digits on your calculator display.",
        1, "Calculator Usage", 2, (1, 0.40, 0.62),
        r"$0.0972$", "B1",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 3, "b",
        r"Write your answer to part (a) correct to 2 decimal places.",
        1, "Rounding", 2, (1, 0.62, 0.74),
        r"$0.10$", "B1",
        topic_id=3)

    # Q4 — Page 2 (idx 1)
    add_q(db, p1.id, exam_dir, 1, 4, None,
        r"It is given that $A = \dfrac{uv}{u - v}$. Find $A$ when $u = 2$ and $v = -3$.",
        1, "Formula Substitution", 2, (1, 0.74, 0.95),
        r"$$A = \frac{2 \times (-3)}{2 - (-3)} = \frac{-6}{5} = -1.2$$", "B1",
        topic_id=4)

    # Q5 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 5, "a",
        r"Find the amount Winston has to pay every month.",
        3, "Hire Purchase / Simple Interest", 3, (2, 0.0, 0.38),
        r"""Downpayment $= 20\% \times 1350 = \$270$
Remaining $= 1350 - 270 = \$1080$
Interest $= \dfrac{1080 \times 8 \times 2}{100} = \$172.80$
Monthly payment $= \dfrac{1080 + 172.80}{24} = \$52.20$""",
        "M1 for interest, M1 for total, A1",
        stem=r"A camera is priced at $\$1350$. Winston bought the camera on hire purchase according to these terms: A downpayment of 20% and the remaining to be paid in monthly instalments over 2 years at a simple interest rate of 8% per annum.",
        topic_id=8)

    add_q(db, p1.id, exam_dir, 1, 5, "b",
        r"Winston pays $x\%$ more on hire purchase for the camera. Find the value of $x$.",
        1, "Percentage Increase", 3, (2, 0.38, 0.55),
        r"$$x = \frac{172.80}{1350} \times 100 = 12.8$$", "B1",
        topic_id=8)

    # Q6 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 6, "a",
        r"Simplify $7p - 4(2p - 3)$.",
        1, "Algebra — Expansion", 3, (2, 0.55, 0.72),
        r"$7p - 8p + 12 = -p + 12$", "B1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 6, "b",
        r"Factorise completely $3 - 9p + 4q - 12pq$.",
        2, "Algebra — Factorisation", 3, (2, 0.72, 0.95),
        r"$3(1 - 3p) + 4q(1 - 3p) = (1 + 4q)(1 - 3p)$ (accept $(3 + 4q)(1 - 3p)$ — but grouping gives $(1+4q)(1-3p)$)", "M1, A1",
        topic_id=4)

    # Q7 — Page 4 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 7, "a",
        r"Find the value of $x$.",
        1, "Angle Properties — Parallel Lines", 4, (3, 0.0, 0.52),
        r"$x = 28$ (alternate angles, $CE \parallel FG$)", "B1",
        stem=r"A rectangular piece of paper $ABCD$ is folded along $CE$. Line $FG$ is drawn such that $CE$ is parallel to $FG$. Angle $CFG = 28°$. Give a reason for each step of your answer.",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 7, "b",
        r"Find the value of $y$.",
        1, "Angle Properties", 4, (3, 0.52, 0.70),
        r"$y = 180 - 90 - 28 = 62$ (angle sum of a triangle, interior angles, $CE \parallel FG$)", "B1",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 7, "c",
        r"Find the value of $z$.",
        1, "Angle Properties", 4, (3, 0.70, 0.95),
        r"$z = 180 - 2 \times 62 = 56$ (adjacent angles on a straight line)", "B1",
        topic_id=10)

    # Q8 — Page 5 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 8, "a",
        r"Express $864$ as a product of its prime factors. Leave your answer in index notation.",
        2, "Prime Factorisation", 5, (4, 0.0, 0.25),
        r"$864 = 2^5 \times 3^3$", "M1, A1",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 8, "b",
        r"Using your answer to part (a), explain why $864$ is not a perfect cube.",
        1, "Perfect Cube", 5, (4, 0.25, 0.40),
        r"The power of its prime factor 2 is 5 which is not a multiple of 3. Hence, 864 is not a perfect cube.", "B1",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 8, "c",
        r"Find the smallest positive integer $k$ such that $864k$ is a perfect square.",
        1, "Perfect Square", 5, (4, 0.40, 0.58),
        r"$k = 2 \times 3 = 6$", "B1",
        topic_id=1)

    # Q9 — Page 5 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 9, None,
        r"Solve $7 - 4x = 3(1 - 2x)$.",
        2, "Solving Linear Equations", 5, (4, 0.58, 0.90),
        r"""$7 - 4x = 3 - 6x$
$2x = -4$
$x = -2$""",
        "M1 for expansion, A1",
        topic_id=5)

    # Q10 — Page 6 (idx 5)
    add_q(db, p1.id, exam_dir, 1, 10, "a",
        r"Write down the largest possible value of $p + q$.",
        1, "Percentage", 6, (5, 0.0, 0.38),
        r"$200$", "B1",
        stem=r"Two classes, A and B, of 40 students each were given two papers in a Mathematics examination. The table shows the percentage passes in the two classes for both papers. Class A: $p\%$, $q\%$. Class B: $20\%$, $r\%$.",
        topic_id=8)

    add_q(db, p1.id, exam_dir, 1, 10, "b",
        r"For Class B, 12 more students passed Paper 2 than Paper 1. Find the value of $r$.",
        2, "Percentage", 6, (5, 0.38, 0.63),
        r"""No. of students who passed Paper 2 $= 20\% \times 40 + 12 = 20$
$r = \dfrac{20}{40} \times 100 = 50$""",
        "M1, A1",
        topic_id=8)

    # Q11 — Page 6 (idx 5)
    add_q(db, p1.id, exam_dir, 1, 11, None,
        r"Write as a single fraction in its simplest form $\dfrac{3x - 1}{4} - \dfrac{2x + 1}{3}$.",
        3, "Algebraic Fractions", 6, (5, 0.63, 0.95),
        r"""$$= \frac{3(3x - 1) - 4(2x + 1)}{12}$$
$$= \frac{9x - 3 - 8x - 4}{12} = \frac{x - 7}{12}$$""",
        "M1 for common denominator, M1 for expansion, A1",
        topic_id=4)

    # Q12 — Page 7 (idx 6)
    add_q(db, p1.id, exam_dir, 1, 12, "a",
        r"Show that the ratio of the number of red marbles : blue marbles : yellow marbles is $7 : 12 : 9$.",
        2, "Ratio", 7, (6, 0.0, 0.48),
        r"""Red $= \dfrac{1}{4}$. Remaining $= \dfrac{3}{4}$.
Blue $= \dfrac{4}{7} \times \dfrac{3}{4} = \dfrac{3}{7}$.
Yellow $= \dfrac{3}{4} - \dfrac{3}{7} = \dfrac{9}{28}$.
Red : Blue : Yellow $= \dfrac{1}{4} : \dfrac{3}{7} : \dfrac{9}{28} = 7 : 12 : 9$ (Shown)""",
        "M1 for combined ratio, A1",
        stem=r"A bag contains marbles of three different colours. 25% of the marbles are red. $\dfrac{4}{7}$ of the remaining marbles are blue and the rest are yellow.",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 12, "b",
        r"If there are 18 more yellow marbles than red marbles, how many marbles are in the bag altogether?",
        2, "Ratio — Word Problem", 7, (6, 0.48, 0.90),
        r"""$2$ units $\to 18$
$7 + 12 + 9 = 28$ units
$28$ units $\to \dfrac{18}{2} \times 28 = 252$""",
        "M1, A1",
        topic_id=9)

    # Q13 — Page 8 (idx 7)
    add_q(db, p1.id, exam_dir, 1, 13, None,
        r"Two L-shaped planks were used to form a T-shaped plank as shown. The edges of the plank meet each other at right angles. The perimeter of the T-shaped plank is 27 m. Write down an equation in $x$ to represent this information, and find the value of $x$.",
        4, "Algebra — Perimeter Word Problem", 8, (7, 0.0, 0.95),
        r"""Perimeter $= 4(7 - 3x) + 2(4x + 1)$
$= 28 - 12x + 8x + 2 = 27$
$30 - 4x = 27$
$4x = 3$
$x = \dfrac{3}{4}$""",
        "M1 for expression, M1 for expansion, M1 for isolating x, A1",
        topic_id=5)

    # Q14 — Page 9 (idx 8)
    add_q(db, p1.id, exam_dir, 1, 14, "a",
        r"Find the values of $a$, $b$ and $c$.",
        2, "Number Patterns", 9, (8, 0.0, 0.38),
        r"$a = 13$, $b = 19$, $c = 31$", "B2 (1m for any two correct values)",
        stem=r"Each term in this sequence is found by adding the same number to the previous term: $7, a, b, 25, c, \ldots$",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 14, "b",
        r"Write down an expression, in terms of $n$, for the $n$th term.",
        1, "Number Patterns — General Term", 9, (8, 0.38, 0.55),
        r"$6n + 1$", "B1",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 14, "c",
        r"Explain why $101$ is not a term of this sequence.",
        2, "Number Patterns — Reasoning", 9, (8, 0.55, 0.95),
        r"""$6n + 1 = 101$
$6n = 100$
$n = \dfrac{100}{6} = \dfrac{50}{3}$
Since $n$ is not a positive integer, 101 is not a term of this sequence.""",
        "M1, A1",
        topic_id=7)

    # ── SECTION B (40 Marks) ──────────────────────

    # Q15 — Page 10 (idx 9)
    add_q(db, p1.id, exam_dir, 1, 15, "a",
        r"Show that $h = 10$.",
        2, "Area of Triangle / Trapezium", 10, (9, 0.0, 0.60),
        r"""$\dfrac{1}{2} \times 6 \times h = 30$
$3h = 30$
$h = 10$ (Shown)""",
        "M1, A1",
        stem=r"$ABCD$ is a trapezium with $AB$ parallel to $DC$. $E$ is a point on $DC$ such that the area of triangle $BCE$ is 30 cm$^2$. $AB = 23$ cm, $DE = 8.5$ cm, $EC = 6$ cm.",
        topic_id=12)

    add_q(db, p1.id, exam_dir, 1, 15, "b",
        r"What fraction of trapezium $ABCD$ is shaded?",
        2, "Area — Fraction", 10, (9, 0.60, 0.95),
        r"""Area of trapezium $ABCD = \dfrac{1}{2} \times (14.5 + 23) \times 10 = 187.5$ cm$^2$
Shaded fraction $= \dfrac{30}{187.5} = \dfrac{4}{25}$""",
        "M1, A1",
        topic_id=12)

    # Q16 — Page 11 (idx 10)
    add_q(db, p1.id, exam_dir, 1, 16, "a",
        r"The diagram shows a regular pentagon. Find the sum of the angles $p$, $q$, $r$, $s$ and $t$.",
        3, "Polygon Angles", 11, (10, 0.0, 0.52),
        r"""Sum of interior angles of pentagon $= (5 - 2) \times 180° = 540°$
Sum of $p + q + r + s + t = 5 \times 360° - 540° = 1260°$""",
        "M1 for interior angles, M1 for exterior calculation, A1",
        topic_id=11)

    add_q(db, p1.id, exam_dir, 1, 16, "b",
        r"An $n$-sided polygon has an equal number of exterior angles of size $10°$ and $30°$. Find the value of $n$.",
        2, "Polygon Angles — Exterior", 11, (10, 0.52, 0.90),
        r"""$\dfrac{n}{2} \times 10 + \dfrac{n}{2} \times 30 = 360$
$20n = 360$
$n = 18$""",
        "M1, A1",
        topic_id=11)

    # Q17 — Page 12 (idx 11)
    add_q(db, p1.id, exam_dir, 1, 17, "a",
        r"Convert 90 km/h into m/s.",
        1, "Speed Conversion", 12, (11, 0.0, 0.18),
        r"$90 \times \dfrac{1000}{3600} = 25$ m/s", "B1",
        stem=r"Ash and Ben drove towards each other from opposite ends of a highway. They began their journey at the same time. Ash and Ben drove at a constant speed of 75 km/h and 90 km/h respectively.",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 17, "b",
        r"At the instant when Ash travelled 120 km, he passed Ben along the highway. Show that the length of the highway is 264 km.",
        3, "Speed, Distance, Time", 12, (11, 0.18, 0.57),
        r"""Length of time travelled by Ben $= \dfrac{120}{75} = 1.6$ hours
Distance travelled by Ben $= 90 \times 1.6 = 144$ km
Length of highway $= 120 + 144 = 264$ km (Shown)""",
        "M1 for time, M1 for Ben's distance, A1",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 17, "c",
        r"After passing Ben, Ash travelled at 110 km/h until he reached the other end of the highway. Calculate Ash's average speed, in km/h, for the whole journey.",
        3, "Average Speed", 12, (11, 0.57, 0.95),
        r"""Time after passing Ben $= \dfrac{144}{110} = 1.3091$ hours (3 s.f.)
Ash's average speed $= \dfrac{\text{Total Distance}}{\text{Total Time}} = \dfrac{264}{1.6 + 1.3091} = \dfrac{264}{2.9091} = 90.7$ km/h (3 s.f.)""",
        "M1 for remaining time, M1 for formula, A1",
        topic_id=9)

    # Q18 — Page 13 (idx 12)
    add_q(db, p1.id, exam_dir, 1, 18, "a",
        r"What is the maximum volume of drink Model $B$ holds?",
        2, "Volume — Cylinder", 13, (12, 0.0, 0.47),
        r"$$V = \pi \times 3^2 \times 20 = 180\pi \approx 565 \text{ cm}^3 \text{ (3 s.f.)}$$", "M1, A1",
        stem=r"A manufacturer came up with two possible models, $A$ and $B$, to package its drinks. Both models $A$ and $B$ are closed at the top. All dimensions are given in centimetres. Model $A$: rectangular prism $6 \times 4.5 \times 20$. Model $B$: cylinder diameter $6$, height $20$.",
        topic_id=13)

    add_q(db, p1.id, exam_dir, 1, 18, "b",
        r"Metal is used to coat the external surface of the model. The cost depends on the amount of metal used. The thickness of the surface coat on both models is negligible. Which of the two models, $A$ or $B$, should the manufacturer choose to lower its cost? Justify your decision.",
        5, "Surface Area Comparison", 13, (12, 0.47, 0.95),
        r"""Surface area of Model $A = 2(6 \times 4.5) + 2(6 \times 20) + 2(4.5 \times 20) = 54 + 240 + 180 = 474$ cm$^2$
Surface area of Model $B = 2\pi(3)^2 + 2\pi(3)(20) = 18\pi + 120\pi = 138\pi \approx 434$ cm$^2$ (3 s.f.)
Choice: Model $B$.
Reason: Model $B$ has a smaller surface area compared to Model $A$.""",
        "M1 for SA of A, M1 for SA of B circles, M1 for SA of B curved, M1 for comparison, A1",
        topic_id=13)

    # Q19 — Page 14 (idx 13)
    add_q(db, p1.id, exam_dir, 1, 19, "a",
        r"Calculate the percentage increase in the amount she earned from 2021 to 2022.",
        2, "Percentage Increase", 14, (13, 0.0, 0.40),
        r"$$\frac{35\,000 - 25\,000}{25\,000} \times 100\% = 40\%$$", "M1, A1",
        stem=r"In 2021, Eve earned a total of $\$25\,000$. In 2022, she earned $\$35\,000$.",
        topic_id=8)

    add_q(db, p1.id, exam_dir, 1, 19, "b",
        r"Chloe wants to buy a dress that is sold on two online sites, $A$ and $B$. Site $A$: \texteuro100. Site $B$: \textsterling100. The exchange rate is $\$1 = \texteuro 0.68$ and $\$1 = \textsterling 0.58$. Explain why Chloe saves more by purchasing the dress via site $A$. Show your calculations.",
        3, "Currency Exchange", 14, (13, 0.40, 0.95),
        r"""Site $A$: $\dfrac{100}{0.68} = \$147.06$ (2 d.p.)
Site $B$: $\dfrac{100}{0.58} = \$172.41$ (2 d.p.)
In Singapore dollars, the dress on site $A$ costs less than site $B$. Hence, Chloe saves more by purchasing the dress via site $A$.""",
        "M1 for both conversions, M1 for comparison, A1",
        topic_id=8)

    # Q20 — Pages 15-16 (idx 14-15)
    add_q(db, p1.id, exam_dir, 1, 20, "a",
        r"Find the value of $p$.",
        1, "Linear Functions — Table", 15, (14, 0.0, 0.22),
        r"$p = 4.5$", "B1",
        stem=r"The variables $x$ and $y$ are connected by the equation $2y = 6 - 3x$. The table shows some corresponding values of $x$ and $y$.",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 20, "b",
        r"Write down the gradient of $2y = 6 - 3x$.",
        1, "Linear Functions — Gradient", 15, (14, 0.22, 0.35),
        r"$-1.5$ (accept $-\dfrac{3}{2}$)", "B1",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 20, "c",
        r"On the grid on Page 17, draw the graph of $2y = 6 - 3x$ for $-2.5 \leq x \leq 3$.",
        2, "Linear Functions — Graph", 15, (14, 0.35, 0.47),
        r"At least 2 points plotted accurately. Line drawn to pass through all plotted points.", "B1 for points, B1 for line",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 20, "di",
        r"Use your graph to find the coordinates of the $x$-intercept.",
        1, "Linear Functions — Intercept", 15, (14, 0.47, 0.60),
        r"$(2, 0)$", "B1",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 20, "dii",
        r"Use your graph to find the value of $y$ when $x = 0.4$.",
        1, "Linear Functions — Reading Graph", 15, (14, 0.60, 0.72),
        r"$y = 2.4$", "B1",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 20, "e",
        r"Does the line $2y = 6 - 3x$ pass through the point $(7, -7)$? Explain your answer.",
        2, "Linear Functions — Verification", 15, (14, 0.72, 0.95),
        r"""$2(-7) = -14$
$6 - 3(7) = -15$
Since $-14 \neq -15$ (LHS $\neq$ RHS), the line does not pass through the point $(7, -7)$.""",
        "M1 for LHS & RHS, A1 for conclusion",
        topic_id=6)

    # Q21 — Page 17 (idx 16)
    add_q(db, p1.id, exam_dir, 1, 21, "a",
        r"Construct triangle $ABC$ such that $AC = 9.3$ cm and angle $ABC = 115°$. The side $AB$ has been drawn for you.",
        2, "Construction", 17, (16, 0.0, 0.48),
        r"Length of $AC$ with arc drawn. Angle $ABC = 115°$ and completed triangle $ABC$ drawn.", "B1 for AC, B1 for angle",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 21, "b",
        r"Measure and write the length of $BC$.",
        1, "Construction — Measurement", 17, (16, 0.48, 0.62),
        r"$BC = (5 \pm 0.1)$ cm", "B1",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 21, "c",
        r"Measure and write the size of angle $BAC$.",
        1, "Construction — Measurement", 17, (16, 0.62, 0.76),
        r"Angle $BAC = (29.5 \pm 1)°$", "B1",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 21, "d",
        r"Mark a point with an 'x' within the triangle $ABC$ such that it is 1.5 cm away from $B$ and 4 cm away from $C$. Label this point $P$.",
        1, "Construction — Locus", 17, (16, 0.76, 0.92),
        r"Refer to construction in part (a).", "B1",
        topic_id=10)

    db.commit()
    q_count = len(p1.questions)
    print(f"Seeded Springfield exam id={exam.id}: Paper 1 ({q_count} parts)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
