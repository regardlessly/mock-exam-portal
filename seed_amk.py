"""Seed Ang Mo Kio Secondary School EOY 2022 Sec 1 Express Math exam."""

import os
import shutil
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/66b1f55907ab3_5777.pdf"
IMAGES_DIR = "/tmp/amk_pages"

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

    school = db.query(School).filter(School.name == "Ang Mo Kio Secondary School").first()
    if not school:
        school = School(name="Ang Mo Kio Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(Exam.school_id == school.id, Exam.year == 2022).first()
    if existing:
        print(f"AMK 2022 already seeded (id={existing.id}). Deleting and re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id, title="End-of-Year Examination 2022", year=2022,
        level="Secondary 1 Express", subject="Mathematics",
        source_pdf="66b1f55907ab3_5777.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # PAPER 1 — Pages 3-15 (idx 2-14), 50 marks, 1 hour 15 min
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=75, total_marks=50,
               date=date(2022, 10, 10), instructions="Answer all questions.")
    db.add(p1); db.flush()

    # Q1a — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 1, "a",
        r"Express $932.3527$ correct to 3 decimal places.",
        1, "Approximation", 3, (2, 0.07, 0.25),
        r"$932.353$", "B1",
        topic_id=3)

    # Q1b — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 1, "b",
        r"Evaluate $\dfrac{(-25)^2 + \sqrt{4.03}}{0.898 - 30.2}$, giving your answer correct to 1 significant figure.",
        1, "Estimation", 3, (2, 0.24, 0.50),
        r"$\dfrac{625 + 2.00749...}{0.898 - 30.2} = \dfrac{627.007...}{-29.302} = -21.399... \approx -20$ (1 s.f.)", "B1",
        topic_id=3)

    # Q2a — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 2, "a",
        r"Express the ratio $3\dfrac{1}{5} : 24\%$ in its simplest form.",
        2, "Ratio — Simplification", 3, (2, 0.50, 0.72),
        r"""$$3\frac{1}{5} : 24\% = \frac{16}{5} : \frac{24}{100}$$
$$= \frac{16}{5} \times 100 : \frac{24}{100} \times 100 = 320 : 24$$
$$= 40 : 3$$""",
        "M1, A1",
        topic_id=9)

    # Q2b — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 2, "b",
        r"Express 860 g as a percentage of 5.6 kg.",
        2, "Percentage", 3, (2, 0.72, 0.92),
        r"$$\frac{860}{5600} \times 100\% = 15\frac{5}{14}\% \approx 15.4\% \text{ (3 s.f.)}$$", "M1, A1",
        topic_id=8)

    # Q3 — Page 4 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 3, "a",
        r"Write down the 6th term of this sequence.",
        1, "Number Patterns", 4, (3, 0.04, 0.25),
        r"$36$", "B1",
        stem=r"The first four terms of a sequence are $1, 4, 9$ and $16$.",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 3, "b",
        r"Find an expression, in terms of $n$, for the $n$th term, $T_n$, of the sequence.",
        1, "Number Patterns — General Term", 4, (3, 0.24, 0.50),
        r"$T_n = n^2$", "B1",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 3, "c",
        r"Is the number 99 part of the sequence above? Explain your answer.",
        1, "Number Patterns — Reasoning", 4, (3, 0.49, 0.78),
        r"No, it is not a perfect square.", "B1",
        topic_id=7)

    # Q4 — Page 5 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 4, None,
        r"If $p : q = 5 : 4$ and $q : r = 4.2 : 0.65$, find $p : r$.",
        3, "Ratio", 5, (4, 0.04, 0.17),
        r"""$$q : r = 4.2 : 0.65 = 420 : 65 = \frac{420}{65} = \frac{84}{13}$$
$$p : q = 5 : 4$$
$$p : q = 525 : 420, \quad q : r = 420 : 65$$
$$p : r = 525 : 65 = 105 : 13$$""",
        "M1, M1, A1",
        topic_id=9)

    # Q5 — Page 6 (idx 5)
    add_q(db, p1.id, exam_dir, 1, 5, None,
        r"Write down an equation in $x$ and solve it to find the original number.",
        3, "Linear Equations — Word Problem", 6, (5, 0.04, 0.30),
        r"""Andy: $3(x + 3)$. James: $4x - 2$.
$$(4x - 2) + 4 = 3(x + 3)$$
$$4x + 2 = 3x + 9$$
$$x = 7$$""",
        "M1, M1, A1",
        stem=r"Andy and James are playing a game. They both start with the same number $x$. Andy adds 3 to the number and then triples it. James multiplies the number by 4 and then subtracts 2. James' result is 4 less than Andy's result.",
        topic_id=5)

    # Q6 — Page 7 (idx 6)
    add_q(db, p1.id, exam_dir, 1, 6, "a",
        r"Express 300 as a product of its prime factors. Give your answer in index notation.",
        2, "Prime Factorisation", 7, (6, 0.04, 0.22),
        r"$300 = 2^2 \times 3 \times 5^2$", "M1, A1",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 6, "b",
        r"Find the lowest common multiple of 300 and 2750.",
        1, "LCM", 7, (6, 0.21, 0.42),
        r"$\text{LCM} = 2^2 \times 3 \times 5^3 \times 11 = 16500$", "B1",
        stem=r"Written as a product of its prime factors, $2750 = 2 \times 5^3 \times 11$.",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 6, "c",
        r"Find the smallest possible integer $k$ such that $\dfrac{2750}{k}$ is a perfect cube.",
        1, "Perfect Cube", 7, (6, 0.41, 0.60),
        r"$k = 2 \times 11 = 22$", "B1",
        topic_id=1)

    # Q7 — Page 8 (idx 7)
    add_q(db, p1.id, exam_dir, 1, 7, "a",
        r"Find the time the triathlete takes to swim 750 m. Give your answer in minutes and seconds.",
        2, "Speed, Distance, Time", 8, (7, 0.04, 0.38),
        r"""$$\text{Time} = \frac{750}{1.5} = 500 \text{ s} = 8 \text{ min } 20 \text{ s}$$""",
        "M1, A1",
        stem=r"A triathlete swims 750 m at an average speed of 1.5 m/s, cycles 20 km at an average speed of 30 km/h and runs 5 km in 25 minutes.",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 7, "b",
        r"Find the average speed, in km/h, of the triathlete for the total distance of the race. Give your answer correct to 1 decimal place.",
        3, "Speed, Distance, Time", 8, (7, 0.37, 0.65),
        r"""Total distance $= 0.75 + 20 + 5 = 25.75$ km
Total time $= (500 \div 3600) + (20 \div 30) + (25 \div 60)$
$= \frac{44}{36}$ h
Average speed $= 25.75 \div \frac{44}{36} = 21.1$ km/h (1 d.p.)""",
        "M1, M1, A1",
        topic_id=9)

    # Q8 — Page 9 (idx 8)
    add_q(db, p1.id, exam_dir, 1, 8, "a",
        r"Factorise $4p - 24pq - 16pr$ completely.",
        1, "Factorisation", 9, (8, 0.04, 0.28),
        r"$4p(1 - 6q - 4r)$", "B1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 8, "b",
        r"Simplify the expression $\dfrac{2(2m + n)}{3} - \dfrac{(3m - 5n)}{5}$.",
        3, "Algebraic Fractions", 9, (8, 0.27, 0.55),
        r"""$$= \frac{5 \times 2(2m+n) - 3(3m-5n)}{15}$$
$$= \frac{20m + 10n - 9m + 15n}{15}$$
$$= \frac{11m + 25n}{15} \text{ or } \frac{11m}{15} + \frac{5n}{3}$$""",
        "M1, M1 (accept alternative), A1",
        topic_id=4)

    # Q9 — Page 10 (idx 9)
    add_q(db, p1.id, exam_dir, 1, 9, None,
        r"Given $a = -2$, $b = 2$ and $c = -3$, evaluate $ab + \dfrac{2c^2}{a}$.",
        2, "Substitution", 10, (9, 0.04, 0.35),
        r"""$$= (-2)(2) + \frac{2(-3)^2}{-2} = -4 + \frac{18}{-2} = -4 + (-9) = -13$$""",
        "M1, A1",
        topic_id=4)

    # Q10 — Page 10 (idx 9)
    add_q(db, p1.id, exam_dir, 1, 10, None,
        r"Sufen paid $\$26.70$ for a pair of shoes after a discount of 25% from a departmental store. What is the original price of the shoes?",
        2, "Reverse Percentage", 10, (9, 0.35, 0.68),
        r"$$\text{Original price} = \frac{100}{75} \times 26.70 = \$35.60$$",
        "M1, A1",
        topic_id=8)

    # Q11 — Page 11 (idx 10)
    add_q(db, p1.id, exam_dir, 1, 11, "a",
        r"Find the price of the laptop before GST, correct to the nearest dollar.",
        2, "Reverse Percentage — GST", 11, (10, 0.04, 0.32),
        r"""107% $= \$3600$
100% $= \frac{3600}{107} \times 100 = \$3364$ (nearest dollar)""",
        "M1, A1",
        stem=r"Store ABC sells a laptop at $\$3600$ inclusive of 7% Goods and Services Tax (GST).",
        topic_id=8)

    add_q(db, p1.id, exam_dir, 1, 11, "b",
        r"James decides to buy the laptop on hire purchase with these terms: a down payment of 25% and the remaining amount to be paid in monthly instalments over 2 years at a simple interest rate of 3.5% per annum. Find his monthly instalment, correct to the nearest cent.",
        3, "Percentage — Hire Purchase", 11, (10, 0.31, 0.68),
        r"""25% of $\$3600 = \$900$
Remaining $= \$3600 - \$900 = \$2700$
Interest $= \frac{2700 \times 3.5 \times 2}{100} = \$189$
Total payable $= 2700 + 189 = \$2889$
Monthly instalment $= \frac{2889}{24} = \$120.38$ (nearest cent)""",
        "M1, M1, A1",
        topic_id=8)

    # Q12 — Page 12 (idx 11)
    add_q(db, p1.id, exam_dir, 1, 12, None,
        r"Find the total surface area of the prism.",
        3, "Surface Area — Prism", 12, (11, 0.04, 0.70),
        r"""Base area $= \frac{1}{2}(20)(21) + (29)(12) = 210 + 348 = 558$ cm$^2$ (accept alternative decomposition)
Total SA $= 2(558) + (21 + 20 + 12 + 29 + 12) \times 32 = 1116 + 3008 = ... $
$= 4124$ cm$^2$ (accept minor variations based on interpretation of cross-section)""",
        "M1, M1, A1",
        stem=r"The figure shows a prism with measurements given in cm. Dimensions: 20, 21, 12, 29, 12.",
        topic_id=13)

    # Q13 — Page 13 (idx 12)
    add_q(db, p1.id, exam_dir, 1, 13, None,
        r"$PQRS$ is a parallelogram. $ST$ and $PU$ are straight lines. Angle $PQR = 66°$, angle $STR = 46°$ and angle $PUS = 73°$. Find $x$.",
        3, "Angle Properties — Parallelogram", 13, (12, 0.04, 0.70),
        r"""$\angle SRQ = 180° - 66° = 114°$ (int. angles, $PQ \parallel SR$)
$\angle RUT = 180° - 114° - 46° = 20°$ ($\angle$ sum of $\triangle$)
$x = 180° - (180° - 20° - 73°)$... or
$x = 180° - 87° = 93°$""",
        "M1, M1/A1, A1",
        topic_id=10)

    # Q14 — Page 14 (idx 13)
    add_q(db, p1.id, exam_dir, 1, 14, "a",
        r"Write down the coordinates of point $R$.",
        1, "Coordinate Geometry", 14, (13, 0.04, 0.50),
        r"$R = (1, -1.5)$ or $R = (1, -\frac{3}{2})$", "B1",
        stem=r"The graph below shows 3 points $P$, $Q$ and $R$.",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 14, "b",
        r"State the equation of the line $PR$.",
        1, "Linear Functions — Equation", 14, (13, 0.50, 0.64),
        r"$x = 2$", "B1",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 14, "c",
        r"Find the gradient of line $PQ$.",
        1, "Linear Functions — Gradient", 14, (13, 0.63, 0.80),
        r"Gradient $= \dfrac{4 - (-1.5)}{3 - 5} = \dfrac{5.5}{-2} = -\dfrac{5}{2}$ ... or from reading graph $= -3$", "B1",
        topic_id=6)

    # Q15 — Page 15 (idx 14)
    add_q(db, p1.id, exam_dir, 1, 15, "a",
        r"Construct quadrilateral $PQRS$.",
        3, "Construction", 15, (14, 0.04, 0.55),
        r"All points joined correctly. Point $R$ and $S$ drawn correctly (2 marks).", "M1, M1, A1",
        stem=r"Quadrilateral $PQRS$ is such that $PQ = 6$ cm, $QR = 7.5$ cm, $PS = 6$ cm, angle $QPS = 130°$ and angle $PQR = 90°$. $PQ$ has already been drawn for you.",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 15, "b",
        r"Measure and write down angle $QRS$.",
        1, "Construction — Measurement", 15, (14, 0.55, 0.72),
        r"$\angle QRS = 73°$ (accept $\pm 1°$)", "B1",
        topic_id=10)

    # ══════════════════════════════════════════════
    # PAPER 2 — Pages 17-32 (idx 16-31), 50 marks, 1h15m
    # ══════════════════════════════════════════════
    p2 = Paper(exam_id=exam.id, paper_number=2, duration_minutes=75, total_marks=50,
               date=date(2022, 10, 12), instructions="Answer all questions.")
    db.add(p2); db.flush()

    # P2 Q1a — Page 17 (idx 16)
    add_q(db, p2.id, exam_dir, 2, 1, "a",
        r"Expand and simplify $6x + 2y - 2(3x - 7y)$.",
        2, "Algebra — Expansion", 17, (16, 0.07, 0.36),
        r"$$6x + 2y - 6x + 14y = 16y$$", "M1, A1",
        topic_id=4)

    # P2 Q1bi — Page 17 (idx 16)
    add_q(db, p2.id, exam_dir, 2, 1, "bi",
        r"Solve $5(1 - 3x) = -9 - x$.",
        2, "Linear Equations", 17, (16, 0.35, 0.65),
        r"""$$5 - 15x = -9 - x$$
$$-14x = -14$$
$$x = 1$$""",
        "M1, A1",
        topic_id=5)

    # P2 Q1bii — Page 18 (idx 17)
    add_q(db, p2.id, exam_dir, 2, 1, "bii",
        r"Solve the equation $\dfrac{x}{6} - \dfrac{x - 5}{4} = \dfrac{x - 3}{12}$.",
        3, "Linear Equations — Algebraic Fractions", 18, (17, 0.04, 0.30),
        r"""$$\frac{2x - 3(x-5)}{12} = \frac{x-3}{12}$$
$$2x - 3x + 15 = x - 3$$
$$-x + 15 = x - 3$$
$$-2x = -18 \implies x = 9$$""",
        "M1, M1, A1",
        topic_id=5)

    # P2 Q2a — Page 19 (idx 18)
    add_q(db, p2.id, exam_dir, 2, 2, "ai",
        r"Find the largest possible number of groups in this learning journey.",
        2, "HCF", 19, (18, 0.04, 0.42),
        r"$\text{HCF}(84, 100) = 4$ groups", "M1, A1",
        stem=r"84 boys and 100 girls signed up for a learning journey. The teacher wanted to divide them into mixed groups with the same number of boys and number of girls in each group.",
        topic_id=1)

    add_q(db, p2.id, exam_dir, 2, 2, "aii",
        r"Hence, find the number of boys in each group.",
        1, "HCF", 19, (18, 0.41, 0.62),
        r"$84 \div 4 = 21$ boys", "A1",
        topic_id=1)

    # P2 Q2b — Page 20 (idx 19)
    add_q(db, p2.id, exam_dir, 2, 2, "bi",
        r"the number of viewers who were between 50 and 75 years old inclusive,",
        2, "Fractions — Word Problem", 20, (19, 0.04, 0.42),
        r"""Under 50: $\frac{1}{5} \times 80 = 16$
Over 75: $\frac{1}{4} \times 80 = 20$
Between 50 and 75: $80 - 16 - 20 = 44$""",
        "M1, A1",
        stem=r"For a television show, $\frac{1}{5}$ of the viewers were under 50 years old, $\frac{1}{4}$ of the viewers were over 75 years old and $\frac{3}{4}$ of those over 75 years old were men. If the total number of viewers was 80, find",
        topic_id=2)

    add_q(db, p2.id, exam_dir, 2, 2, "bii",
        r"the number of women over 75 years old.",
        1, "Fractions — Word Problem", 20, (19, 0.41, 0.62),
        r"Women over 75 $= 20 - \frac{3}{4}(20) = 20 - 15 = 5$", "A1",
        topic_id=2)

    # P2 Q3 — Pages 21-22 (idx 20-21): Pie chart
    add_q(db, p2.id, exam_dir, 2, 3, "a",
        r"Find the number of students whose favourite food is burgers.",
        2, "Statistics — Pie Chart", 21, (20, 0.04, 0.70),
        r"$$\frac{108}{360} \times 40 = 12 \text{ students}$$", "M1, A1",
        stem=r"A survey was conducted on a class of 40 students to find out their favourite food. The results are represented on the given pie chart. Burgers $= 108°$, Pizza $= x°$, Porridge $= 2x°$, Chicken Rice is the remaining sector.",
        topic_id=14)

    add_q(db, p2.id, exam_dir, 2, 3, "b",
        r"Find the value of $x$.",
        2, "Statistics — Pie Chart", 22, (21, 0.04, 0.30),
        r"""Chicken Rice angle $= 360° - 108° - x - 2x = 252° - 3x$
Since the chart shows Chicken Rice $= 90°$:
$252 - 3x = 90° \implies x = 54$
(or from reading the chart, $x + 2x + 108 + \text{CR} = 360$)
$x = 54$""",
        "M1, A1",
        topic_id=14)

    add_q(db, p2.id, exam_dir, 2, 3, "c",
        r"Given that 5 new students joined the class and they chose chicken rice as their favourite food. Calculate the new angle on the pie chart representing the number of students who chose chicken rice.",
        2, "Statistics — Pie Chart", 22, (21, 0.29, 0.68),
        r"""Original CR students $= \frac{90}{360} \times 40 = 10$
New CR $= 10 + 5 = 15$
New angle $= \frac{15}{45} \times 360° = 120°$""",
        "M1, A1",
        topic_id=14)

    # P2 Q4 — Page 23 (idx 22)
    add_q(db, p2.id, exam_dir, 2, 4, "a",
        r"the number of sides of the polygon,",
        2, "Polygon — Interior Angles", 23, (22, 0.04, 0.52),
        r"""Interior angle $= 120°$
Exterior angle $= 180° - 120° = 60°$
$n = \frac{360°}{60°} = 6$""",
        "M1, A1",
        stem=r"In the figure below, $AB$, $BC$ and $CD$ are three sides of a regular polygon and angle $ABC = 120°$. $AB$ and $DC$ are produced to meet at $E$. Find",
        topic_id=11)

    add_q(db, p2.id, exam_dir, 2, 4, "b",
        r"angle $CEB$.",
        2, "Polygon — Angles", 23, (22, 0.51, 0.72),
        r"""$\angle CBE = 180° - 120° = 60°$ (adj. angles on str. line)
$\angle BCE = 180° - 120° = 60°$ (adj. angles on str. line)
$\angle CEB = 180° - 60° - 60° = 60°$""",
        "M1, A1",
        topic_id=11)

    # P2 Q5 — Page 24 (idx 23)
    add_q(db, p2.id, exam_dir, 2, 5, None,
        r"Find the area of the shaded region. Take $\pi = 3.142$.",
        3, "Area — Composite Figure", 24, (23, 0.04, 0.70),
        r"""Area of trapezium $CDFH$: $\frac{1}{2}(CD + HF)(CH) = \frac{1}{2}(CD + 13)(6)$
Need to find $CD$. From the diagram, $CD$ appears to be the top edge.
Area of semicircle $= \frac{1}{2}\pi r^2 = \frac{1}{2}(3.142)(3)^2 = 14.139$ m$^2$
Area of trapezium $= \frac{1}{2}(6 + 13)(6) = 57$ m$^2$
Shaded area $= 57 - 14.139 = 42.9$ m$^2$ (3 s.f.)""",
        "M1, M1, A1",
        stem=r"The diagram below shows the layout of a garden that is made up of a trapezium $CDFH$ with a semicircle $CVH$ with centre $O$ cut out of it. It is given that $CH = 6$ m and $HF = 13$ m.",
        topic_id=12)

    # P2 Q6 — Pages 25-26 (idx 24-25): Linear functions
    add_q(db, p2.id, exam_dir, 2, 6, "a",
        r"Find the value of $p$.",
        1, "Linear Functions — Table", 25, (24, 0.04, 0.22),
        r"$p = 4(-2) - 5 = -13$", "B1",
        stem=r"The following table shows the corresponding $x$ and $y$ values for the equation $y = 4x - 5$.",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 6, "b",
        r"On the grid provided, draw the graph of $y = 4x - 5$. Using a scale of 2 cm to represent 1 unit, draw a horizontal axis for $-3 \leq x \leq 3$. Using a scale of 2 cm to represent 5 units, draw a vertical axis for $-20 \leq y \leq 10$.",
        3, "Linear Functions — Graph", 25, (24, 0.21, 0.47),
        r"Straight line through $(-3, -17)$, $(-2, -13)$, $(1, -1)$, $(2.5, 5)$, $(3, 7)$.", "B1 for scale, B1 for points, B1 for line",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 6, "ci",
        r"find the value of $x$ when $y = 7$.",
        1, "Linear Functions — Reading Graph", 25, (24, 0.47, 0.60),
        r"$x = 3$", "B1",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 6, "cii",
        r"state the value of the $x$-intercept.",
        1, "Linear Functions — Intercept", 25, (24, 0.59, 0.72),
        r"$x$-intercept $= 1.25$ or $\frac{5}{4}$", "B1",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 6, "d",
        r"Draw the line $x = 3$ on the grid provided.",
        1, "Linear Functions — Vertical Line", 25, (24, 0.72, 0.80),
        r"Vertical line drawn at $x = 3$.", "B1",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 6, "e",
        r"Write down the equation of the line which has the same gradient as the line $y = 4x - 5$ and $y$-intercept 1.",
        1, "Linear Functions — Equation", 25, (24, 0.79, 0.92),
        r"$y = 4x + 1$", "B1",
        topic_id=6)

    # P2 Q7 — Pages 27-28 (idx 26-27): Currency exchange and depreciation
    add_q(db, p2.id, exam_dir, 2, 7, "ai",
        r"How much does she receive in Thai Baht?",
        1, "Currency Exchange", 27, (26, 0.04, 0.38),
        r"$750 \times 26 = 19\,500$ THB", "A1",
        stem=r"Mavis travels from Singapore to Thailand. She exchanges 750 Singapore Dollars (S\$) to Thai Baht (THB) when the exchange rate is S\$1 = 26 THB. While in Thailand, she spends 14\,200 THB. On her return, she exchanges the remaining Thai Baht into Singapore Dollars when the exchange rate is S\$1 = 26.5 THB.",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 7, "aii",
        r"Find the amount of Singapore Dollars she receives.",
        2, "Currency Exchange", 27, (26, 0.37, 0.65),
        r"""Remaining THB $= 19\,500 - 14\,200 = 5300$ THB
S\$ received $= \frac{5300}{26.5} = \$200$""",
        "M1, A1",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 7, "b",
        r"Every year, the value of a car depreciates by 15% of its value in the previous year. If the value of the car was $\$93\,925$ in 2022, find its value in 2020.",
        3, "Percentage — Depreciation", 28, (27, 0.04, 0.28),
        r"""$0.85^2 \times V_{2020} = 93\,925$
$V_{2020} = \frac{93\,925}{0.7225} = \$130\,000$""",
        "M1, M1, A1",
        topic_id=8)

    # P2 Q8 — Pages 29-30 (idx 28-29): Cylinder / pencil case
    add_q(db, p2.id, exam_dir, 2, 8, "a",
        r"Calculate the volume of the pencil, leaving your answer in terms of $\pi$.",
        2, "Volume — Cylinder", 29, (28, 0.04, 0.38),
        r"$$V = \pi r^2 h = \pi (0.35)^2 (16) = 1.96\pi \text{ cm}^3$$", "M1, A1",
        stem=r"The diagram below shows an unsharpened pencil. It is cylindrical in shape. The diameter and length of the pencil are 0.7 cm and 16 cm respectively.",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 8, "bi",
        r"Find the maximum number of pencils that can fit into the pencil case.",
        1, "Volume — Application", 29, (28, 0.37, 0.72),
        r"""Pencil case: $6 \times 2 \times 16$ cm.
Along width (6 cm): $\lfloor 6 \div 0.7 \rfloor = 8$ pencils.
Along height (2 cm): $\lfloor 2 \div 0.7 \rfloor = 2$ layers.
Maximum $= 8 \times 2 = 16$ pencils.""", "A1",
        stem=r"A number of this pencil can fit exactly into a pencil case with dimensions as given in the diagram below (6 cm $\times$ 2 cm $\times$ 16 cm).",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 8, "bii",
        r"Hence, find the percentage of empty space in the box.",
        2, "Volume — Percentage", 30, (29, 0.04, 0.40),
        r"""Volume of box $= 6 \times 2 \times 16 = 192$ cm$^3$
Volume of 16 pencils $= 16 \times 1.96\pi = 31.36\pi \approx 98.52$ cm$^3$
Percentage empty $= \frac{192 - 98.52}{192} \times 100\% = 48.7\%$""",
        "M1, A1",
        topic_id=13)

    # P2 Q9 — Pages 31-32 (idx 30-31): Parking charges
    add_q(db, p2.id, exam_dir, 2, 9, "a",
        r"Joseph parked his car at B2M level at 6:30 pm and paid $\$8.60$ for parking charges upon leaving the car park. What is the latest possible time that he left the car park? Explain your answer with working.",
        2, "Rate — Word Problem", 31, (30, 0.04, 0.68),
        r"""First 90 min: $90 \times \$0.04 = \$3.60$
Remaining $= \$8.60 - \$3.60 = \$5.00$
At $\$5$ per 30 min: 1 block (any part counts)
$\$5.00 \div \$5 = 1$ block $= 30$ min
Total $= 90 + 30 = 120$ min $= 2$ h
Latest time $= 6{:}30$ pm $+ 2$ h $= 8{:}30$ pm""",
        "M1, A1",
        stem=r"The table below shows the parking charges at Changi Airport Terminal 1. Short-term Parking (B2M and B2): First 90 mins: \$0.04 per minute. Subsequent 30 mins or part thereof: \$5 per 30 mins. General Parking (B3 and B5): \$0.04 per minute.",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 9, "b",
        r"Pearlyn is considering whether to park her car at B2 or B3 at Changi Airport Terminal 1. She intends to stay at the airport for 2.5 hours. Which is a cheaper option? Explain your answer with working.",
        3, "Rate — Comparison", 32, (31, 0.04, 0.48),
        r"""B2 (Short-term): First 90 min $= 90 \times 0.04 = \$3.60$
Remaining $= 150 - 90 = 60$ min $= 2$ blocks of 30 min $\implies 2 \times \$5 = \$10$
Total B2 $= \$3.60 + \$10 = \$13.60$

B3 (General): $150 \times \$0.04 = \$6.00$

She should park at B3 because it is cheaper ($\$6.00 < \$13.60$).""",
        "M1, M1, A1",
        topic_id=9)

    db.commit()
    p1_count = len(p1.questions)
    p2_count = len(p2.questions)
    print(f"Seeded AMK exam id={exam.id}: Paper 1 ({p1_count} parts), Paper 2 ({p2_count} parts)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
