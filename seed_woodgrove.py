"""Seed Woodgrove Secondary School EOY 2020 Sec 1 Express Math exam (Paper 1 only)."""

import os
import shutil
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/Woodgrove-Secondary-End-of-Year-2020-Sec-1-Math-Only-Paper-1.pdf"
IMAGES_DIR = "/tmp/woodgrove_pages"

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

    school = db.query(School).filter(School.name == "Woodgrove Secondary School").first()
    if not school:
        school = School(name="Woodgrove Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(Exam.school_id == school.id, Exam.year == 2020).first()
    if existing:
        print(f"Woodgrove 2020 already seeded (id={existing.id}). Deleting and re-seeding.")
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
        source_pdf="Woodgrove-Secondary-End-of-Year-2020-Sec-1-Math-Only-Paper-1.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # PAPER 1 — Section A (pages 3-8, idx 1-6) + Section B (pages 9-16, idx 7-16)
    # 90 marks, 2 hours 15 minutes
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=135, total_marks=90,
               date=date(2020, 10, 6), instructions="Answer all questions. There are 2 sections in this paper (Section A: 45 marks, Section B: 45 marks).")
    db.add(p1); db.flush()

    # ──────────────────────────────────────────────
    # SECTION A — 45 marks
    # ──────────────────────────────────────────────

    # Q1 — Page 3 (idx 1)
    add_q(db, p1.id, exam_dir, 1, 1, "a",
        r"Express $360$ as a product of its prime factors.",
        2, "Prime Factorisation", 3, (1, 0.10, 0.32),
        r"$360 = 2^3 \times 3^2 \times 5$", "M1 for method, A1",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 1, "b",
        r"Find the smallest positive integer $k$ such that $360k$ is a perfect cube.",
        2, "Perfect Cube", 3, (1, 0.31, 0.48),
        r"$k = 5^2 \times 3 = 75$", "M1, A1",
        topic_id=1)

    # Q2 — Page 3 (idx 1)
    # Stem: A list of numbers: 36, -0.025, 3/7, -sqrt(7)/sqrt(7), 4pi/2, 0.71-dot
    add_q(db, p1.id, exam_dir, 1, 2, "a",
        r"a negative integer.",
        1, "Number Classification", 3, (1, 0.48, 0.72),
        r"$-\dfrac{\sqrt{7}}{\sqrt{7}} = -1$", "B1",
        stem=r"A list of numbers are shown below: $36$, $-0.025$, $\dfrac{3}{7}$, $-\dfrac{\sqrt{7}}{\sqrt{7}}$, $\dfrac{4\pi}{2}$, $0.7\dot{1}$. From the list, write down",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 2, "b",
        r"a perfect square.",
        1, "Number Classification", 3, (1, 0.71, 0.83),
        r"$36$", "B1",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 2, "c",
        r"irrational number(s).",
        1, "Number Classification", 3, (1, 0.82, 0.97),
        r"$\dfrac{4\pi}{2}$", "B1",
        topic_id=2)

    # Q3 — Page 4 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 3, "ai",
        r"Estimate $25\,956$ to 2 significant figures.",
        1, "Approximation", 4, (2, 0.05, 0.18),
        r"$26\,000$", "B1",
        stem=r"Estimate the following to 2 significant figures.",
        topic_id=3)

    add_q(db, p1.id, exam_dir, 1, 3, "aii",
        r"Estimate $4010$ to 2 significant figures.",
        1, "Approximation", 4, (2, 0.17, 0.25),
        r"$4000$", "B1",
        topic_id=3)

    add_q(db, p1.id, exam_dir, 1, 3, "aiii",
        r"Estimate $0.0502$ to 2 significant figures.",
        1, "Approximation", 4, (2, 0.24, 0.33),
        r"$0.050$", "B1",
        topic_id=3)

    add_q(db, p1.id, exam_dir, 1, 3, "b",
        r"Hence, estimate the value of $\dfrac{25\,956 + 4010}{0.0502 \times 100}$ to 1 significant figure.",
        2, "Estimation", 4, (2, 0.32, 0.52),
        r"$$\frac{25\,956 + 4010}{0.0502 \times 100} \approx \frac{26\,000 + 4000}{0.050 \times 100} = \frac{30\,000}{5} = 6000$$", "M1, A1",
        topic_id=3)

    # Q4 — Page 4 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 4, "a",
        r"Factorise $xq - yq + zq$.",
        1, "Algebra — Factorisation", 4, (2, 0.52, 0.68),
        r"$q(x - y + z)$", "B1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 4, "b",
        r"Hence, find the value of $39 \times 70 - 12 \times 70 + 73 \times 70$.",
        2, "Algebra — Factorisation Application", 4, (2, 0.67, 0.88),
        r"$$= 70(39 - 12 + 73) = 70(100) = 7000$$", "M1, A1",
        topic_id=4)

    # Q5 — Page 5 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 5, "ai",
        r"Simplify $2(m - 5) - m$.",
        2, "Algebra — Expansion", 5, (3, 0.05, 0.18),
        r"$2m - 10 - m = m - 10$", "A1, A1",
        stem=r"Simplify",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 5, "aii",
        r"Simplify $\dfrac{(a - b)}{3} + \dfrac{(a + 2b)}{4}$.",
        3, "Algebra — Algebraic Fractions", 5, (3, 0.17, 0.36),
        r"$$\frac{4(a-b) + 3(a+2b)}{12} = \frac{4a - 4b + 3a + 6b}{12} = \frac{7a + 2b}{12}$$", "M1 for LCD, A1 for expansion, A1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 5, "b",
        r"Factorise completely $3p(q - 1) + p(q - 1)$.",
        2, "Algebra — Factorisation", 5, (3, 0.35, 0.48),
        r"$(q - 1)(3p + p) = 4p(q - 1)$", "M1, A1",
        topic_id=4)

    # Q6 — Page 5 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 6, "a",
        r"Write down the next term of the sequence.",
        1, "Number Patterns", 5, (3, 0.48, 0.63),
        r"$27$", "B1",
        stem=r"The first four terms of a sequence are $7$, $12$, $17$ and $22$.",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 6, "b",
        r"Find an expression, in terms of $n$, for the $n$th term of the sequence.",
        1, "Number Patterns — General Term", 5, (3, 0.62, 0.73),
        r"$T_n = 5n + 2$", "B1",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 6, "c",
        r"One term in the sequence is $252$. Find the value of $n$ for this term.",
        2, "Number Patterns — Solving", 5, (3, 0.72, 0.84),
        r"""$T_n = 5n + 2$
$252 = 5n + 2$
$5n = 250$
$n = 50$""", "M1, A1",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 6, "d",
        r"Explain, with a reason, is $200$ in the sequence?",
        2, "Number Patterns — Reasoning", 5, (3, 0.83, 0.97),
        r"""No. $T_n = 5n + 2$
$200 = 5n + 2$
$5n = 198$
$n = 39.6$
$n$ has to be an integer. Thus not possible for $200$ to be a term.
Or: $200 = 5n + 2 \implies 5n = 198$. $198$ is not a multiple of $5$, thus it is not possible for $200$ to be a term.""", "B1, B1",
        topic_id=7)

    # Q7 — Page 6 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 7, "a",
        r"What was the total distance traveled by Joshua?",
        2, "Speed, Distance, Time", 6, (4, 0.05, 0.30),
        r"""$\frac{1}{4}$ of the journey $= (12 - 3) \times 2 = 18$ km
Total journey $= 18 \times 4 = 72$ km""", "M1, A1",
        stem=r"Joshua cycled $\frac{3}{4}$ of his journey at $12$ km/h. He then decreased his speed by $3$ km/h to complete the remaining journey in $2$ h.",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 7, "b",
        r"How long did Joshua take to travel the whole journey?",
        3, "Speed, Distance, Time", 6, (4, 0.29, 0.60),
        r"""$72 \times \frac{3}{4} = 54$ km at $12$ km/h
Time for first $\frac{3}{4}$ journey $= 54 \div 12 = 4\frac{1}{2}$ h
Total time $= 2 + 4\frac{1}{2} = 6\frac{1}{2}$ h""", "M1, M1, A1",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 7, "c",
        r"What was Joshua's average speed for the whole journey?",
        2, "Speed, Distance, Time — Average Speed", 6, (4, 0.59, 0.80),
        r"$$\text{Average speed} = \frac{\text{Total distance}}{\text{Total time}} = \frac{72}{6.5} = 11.1 \text{ km/h (3 s.f.)}$$", "M1, A1",
        topic_id=9)

    # Q8 — Page 7 (idx 5)
    add_q(db, p1.id, exam_dir, 1, 8, "a",
        r"$x$.",
        1, "Angle Properties — Parallel Lines", 7, (5, 0.04, 0.40),
        r"$x = 110$ (corresponding angles, $BE \parallel AC$)", "B1",
        stem=r"In the diagram, the straight line $AB$ is parallel to $CD$ and $AC$ is parallel to $BE$. Given $\angle CAB = 110°$ and $\angle EDC = 45°$, calculate the value of",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 8, "b",
        r"$y$.",
        1, "Angle Properties — Parallel Lines", 7, (5, 0.39, 0.55),
        r"$\angle ACD + 110° = 180°$ (co-interior angles, $AB \parallel CD$). $y = 70$", "B1",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 8, "c",
        r"$z$.",
        3, "Angle Properties — Parallel Lines", 7, (5, 0.54, 0.92),
        r"""Draw a line passing through $E$, parallel to $AB$ and $CD$.
$a° = 70°$ (alternate angles)
$b° = 45°$ (alternate angles)
$z = 70 + 45 = 115$""", "M1, M1, A1",
        topic_id=10)

    # Q9 — Page 8 (idx 6)
    add_q(db, p1.id, exam_dir, 1, 9, "a",
        r"$\angle ABC$.",
        2, "Polygon Angles", 8, (6, 0.04, 0.46),
        r"$\angle ABC = 180° - 18° - 18° = 144°$ (angle sum of triangle, since $AB = BC$ in a regular polygon)", "M1, A1",
        stem=r"$AB$, $BC$ and $CD$ are adjacent sides of a regular polygon and $\angle CAB = 18°$. Find",
        topic_id=11)

    add_q(db, p1.id, exam_dir, 1, 9, "b",
        r"the number of sides of the polygon.",
        2, "Polygon Angles — Exterior Angle", 8, (6, 0.45, 0.66),
        r"""Size of exterior angle $= 180° - 144° = 36°$
Number of sides $= \frac{360°}{36°} = 10$""", "M1, A1",
        topic_id=11)

    add_q(db, p1.id, exam_dir, 1, 9, "c",
        r"$\angle ACD$.",
        1, "Polygon Angles", 8, (6, 0.65, 0.82),
        r"$\angle ACD = 144° - 18° = 126°$", "B1",
        topic_id=11)

    # ──────────────────────────────────────────────
    # SECTION B — 45 marks
    # ──────────────────────────────────────────────

    # Q10 — Page 9 (idx 8)
    add_q(db, p1.id, exam_dir, 1, 10, "a",
        r"How many gift bags are needed?",
        2, "HCF", 9, (8, 0.05, 0.35),
        r"""HCF of $440$, $320$ and $200$:
$\text{HCF} = 10 \times 2 \times 2 = 40$
$40$ gift bags are needed.""", "M1, A1",
        stem=r"Blessed Organisation plans to donate $440$ packs of biscuits, $320$ canned food and $200$ kg of rice to the old folks' home. The maximum number of packs of biscuits, canned food and rice are to be placed equally in gift bags before the donation.",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 10, "b",
        r"How many of each items are there in each gift bag?",
        3, "HCF — Application", 9, (8, 0.34, 0.62),
        r"""Number of packs of biscuits in each bag $= 440 \div 40 = 11$
Number of canned food in each bag $= 320 \div 40 = 8$
Weight of rice in each bag $= 200 \div 40 = 5$ kg""", "B1, B1, B1",
        topic_id=1)

    # Q11 — Page 9 (idx 8)
    add_q(db, p1.id, exam_dir, 1, 11, None,
        r"Without the use of a calculator, evaluate $[(17 - 11) + 20 \div 4] \times (-2)^2$. Show your working.",
        3, "Order of Operations", 9, (8, 0.62, 0.93),
        r"""$$[(17 - 11) + 20 \div 4] \times (-2)^2$$
$$= (6 + 5) \times 4$$
$$= 11 \times 4 = 44$$""",
        "M1, M1, A1",
        topic_id=2)

    # Q12 — Page 10 (idx 9)
    add_q(db, p1.id, exam_dir, 1, 12, "ai",
        r"Simplify and factorise $3pq + 9p$.",
        1, "Algebra — Factorisation", 10, (9, 0.05, 0.18),
        r"$3p(q + 3)$", "B1",
        stem=r"Simplify and factorise completely each of the following expressions.",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 12, "aii",
        r"Simplify and factorise $3ax + 36mx - 15mx$.",
        2, "Algebra — Factorisation", 10, (9, 0.17, 0.38),
        r"$3ax + 36mx - 15mx = 3ax + 21mx = 3x(a + 7m)$", "M1, A1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 12, "b",
        r"Solve $\dfrac{5}{x+3} = \dfrac{7}{2x}$.",
        3, "Algebra — Equations with Fractions", 10, (9, 0.37, 0.70),
        r"""$5(2x) = 7(x + 3)$
$10x = 7x + 21$
$3x = 21$
$x = 7$""", "M1 for cross-multiply, M1 for expanding, A1",
        topic_id=5)

    # Q13 — Page 11 (idx 10)
    add_q(db, p1.id, exam_dir, 1, 13, "a",
        r"Danish's age.",
        1, "Algebra — Expressions", 11, (10, 0.05, 0.22),
        r"Danish's age $= (x - 6)$ years", "B1",
        stem=r"Danial is $x$ years old. His brother Danish is $6$ years younger than him. His father is $3$ times as old as Danial. Write an algebraic expression in terms of $x$ for",
        topic_id=5)

    add_q(db, p1.id, exam_dir, 1, 13, "b",
        r"his father's age.",
        1, "Algebra — Expressions", 11, (10, 0.21, 0.34),
        r"Father's age $= 3x$ years", "B1",
        topic_id=5)

    add_q(db, p1.id, exam_dir, 1, 13, "c",
        r"Write down an equation in $x$ to represent this information, and show that it reduces to $2x - 6 = 30$.",
        2, "Linear Equations — Forming", 11, (10, 0.33, 0.62),
        r"""The sum of Danial's and Danish's ages is $30$.
$x + (x - 6) = 30$
$2x - 6 = 30$ (shown)""", "M1, A1",
        stem=r"The sum of Danial's and Danish's age are $30$.",
        topic_id=5)

    add_q(db, p1.id, exam_dir, 1, 13, "d",
        r"Solve the equation $2x - 6 = 30$.",
        2, "Linear Equations — Solving", 11, (10, 0.61, 0.86),
        r"""$2x - 6 = 30$
$2x = 36$
$x = 18$""", "M1, A1",
        topic_id=5)

    # Q14 — Page 12 (idx 11), graph on page 13 (idx 12)
    add_q(db, p1.id, exam_dir, 1, 14, "a",
        r"Complete the table above for the line $y = 2x + 1$.",
        2, "Linear Functions — Table", 12, (11, 0.05, 0.30),
        r"""When $x = 0$: $y = 1$. When $x = 1$: $y = 3$. When $x = 2$: $y = 5$. When $x = 3$: $y = 7$. When $x = 4$: $y = 9$.
Any 2 right answers = 1 mark.""", "B2",
        stem=r"This is the table of values for the line $y = 2x + 1$.",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 14, "b",
        r"On the grid opposite, draw the graph of $y = 2x + 1$ for $0 \leq x \leq 4$.",
        2, "Linear Functions — Graph", 12, (11, 0.29, 0.40),
        r"Correct coordinates plotted and correct joining of points with straight line.", "B1 for points, B1 for line",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 14, "c",
        r"State the $y$-intercept of the line $y = 2x + 1$.",
        1, "Linear Functions — Intercept", 12, (11, 0.39, 0.50),
        r"$y$-intercept $= 1$", "B1",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 14, "d",
        r"Use your graph to find the value of $x$ when $y = 2$.",
        1, "Linear Functions — Reading Graph", 12, (11, 0.49, 0.60),
        r"$x = 0.5$", "B1",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 14, "e",
        r"On the same grid, draw the line $y = 3$ and label it.",
        1, "Linear Functions — Horizontal Line", 12, (11, 0.59, 0.68),
        r"Refer to graph paper.", "B1",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 14, "f",
        r"Write down the gradient of $y = 3$.",
        1, "Linear Functions — Gradient", 12, (11, 0.67, 0.80),
        r"Gradient $= 0$", "B1",
        topic_id=6)

    # Q15 — Page 14 (idx 13), continued on page 15 (idx 14)
    add_q(db, p1.id, exam_dir, 1, 15, "a",
        r"Find the area of trapezium $ABCD$.",
        2, "Area — Trapezium", 14, (13, 0.05, 0.40),
        r"$$\text{Area} = \frac{1}{2}(21.5 + 9.5) \times 10 = \frac{1}{2} \times 31 \times 10 = 155 \text{ cm}^2$$", "M1, A1",
        stem=r"The diagram shows a solid metallic prism whose cross-section is a trapezium $ABCD$. $BE = 10$ cm, $BC = 9.5$ cm, $AD = 21.5$ cm and $DJ = 35$ cm. $BC$ is parallel to $AD$.",
        topic_id=12)

    add_q(db, p1.id, exam_dir, 1, 15, "b",
        r"Hence, find the volume of the prism.",
        1, "Volume — Prism", 14, (13, 0.39, 0.50),
        r"$$V = 155 \times 35 = 5425 \text{ cm}^3$$", "B1",
        topic_id=13)

    add_q(db, p1.id, exam_dir, 1, 15, "c",
        r"If all the melted prisms could fill the tank completely, find the height of the tank.",
        4, "Volume — Cylinder", 14, (13, 0.50, 0.97),
        r"""Volume of $50$ prisms $= 50 \times 5425 = 271\,250$ cm$^3$
Radius of tank $= 0.8 \div 2 = 0.4$ m $= 40$ cm
Let the height of the tank be $h$.
$\pi \times 40^2 \times h = 271\,250$
$h = \frac{271\,250}{3.142 \times 1600} = \frac{271\,250}{5027.2} = 53.956$
$h = 54.0$ cm (3 s.f.)""",
        "M1 for total volume, M1 for radius conversion, M1 for equation, A1",
        stem=r"$50$ identical prisms were melted and poured into an open cylindrical tank with a diameter of $0.8$ m. Take $\pi = 3.142$.",
        topic_id=13)

    add_q(db, p1.id, exam_dir, 1, 15, "d",
        r"The external curved surface of the tank is coated with a protective layer. Find the area of this protective layer.",
        2, "Surface Area — Cylinder", 15, (14, 0.05, 0.18),
        r"Curved surface area $= 2\pi r h = 2 \times 3.142 \times 40 \times 54.0 = 13\,600$ cm$^2$ (3 s.f.)", "M1, A1",
        topic_id=13)

    # Q16 — Page 15 (idx 14)
    add_q(db, p1.id, exam_dir, 1, 16, None,
        r"Construct $\triangle ABC$ such that $AB = 10$ cm, $\angle BAC = 75°$ and $\angle ABC = 50°$ in the space provided. Measure and write down the length of $AC$.",
        3, "Construction", 15, (14, 0.18, 0.90),
        r"Refer to attachment. $AC$ measured from construction.", "B3 (B1 for $AB$, B1 for each angle, B1 for measurement)",
        topic_id=10)

    # Q17 — Page 16-17 (idx 15-16)
    add_q(db, p1.id, exam_dir, 1, 17, "a",
        r"The receipt shows the 7% GST amount is $\$5.04$. Show how this amount is calculated.",
        2, "Percentage — GST", 16, (15, 0.04, 0.95),
        r"""$10\%$ service charge $= \$6.55$
$100\%$ represents $\$65.50$
$7\%$ GST $= (65.50 + 6.55) \times 7\% = 72.05 \times \frac{7}{100} = 72.05 \times 0.07 = 5.0435 = \$5.04$ (2 d.p.)""",
        "M1, A1",
        stem=r"Mr Tan brought his family for lunch in a restaurant. The receipt is as shown.",
        topic_id=8)

    add_q(db, p1.id, exam_dir, 1, 17, "b",
        r"The total amount $\$77.09$ is printed on the receipt. Show how this amount is calculated.",
        2, "Percentage — GST Total", 17, (16, 0.05, 0.28),
        r"""Total amount of the bill $= 72.05 \times 107\% = 72.05 \times \frac{107}{100} = 77.0935 = \$77.09$ (2 d.p.)
OR: Total $= 72.05 + 5.04 = \$77.09$
OR: Total $= 65.50 + 6.55 + 5.04 = \$77.09$""",
        "M1, A1",
        topic_id=8)

    add_q(db, p1.id, exam_dir, 1, 17, "c",
        r"Mr Tan thinks that additional charges (service charge and GST) is 17%. Do you agree? Explain with working.",
        1, "Percentage — Reasoning", 17, (16, 0.27, 0.53),
        r"""Total amount $= 65.50 \times 1.17 = \$76.635 = \$76.64$ (2 d.p.)
$\$76.64 \neq \$77.09$
Mr Tan is incorrect.""",
        "B1",
        topic_id=8)

    db.commit()
    p1_count = len(p1.questions)
    print(f"Seeded Woodgrove exam id={exam.id}: Paper 1 ({p1_count} parts)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
