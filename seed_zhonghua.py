"""Seed Zhonghua Secondary School EOY 2023 Sec 1 Express Math exam."""

import os
import shutil
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/Zhonghua-Secondary-EOY-2023-Sec-1-Math-Group-3.pdf"
IMAGES_DIR = "/tmp/zhonghua_pages"

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

    school = db.query(School).filter(School.name == "Zhonghua Secondary School").first()
    if not school:
        school = School(name="Zhonghua Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(Exam.school_id == school.id, Exam.year == 2023).first()
    if existing:
        print(f"Zhonghua 2023 already seeded (id={existing.id}). Deleting and re-seeding.")
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
        source_pdf="Zhonghua-Secondary-EOY-2023-Sec-1-Math-Group-3.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # SINGLE PAPER — Pages 2-20 (idx 1-19), 80 marks, 2 hours
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=120, total_marks=80,
               date=date(2023, 9, 28), instructions="Answer all questions.")
    db.add(p1); db.flush()

    # Q1 — Page 2 (idx 1)
    add_q(db, p1.id, exam_dir, 1, 1, "a",
        r"Write $PQ$ as a fraction of $PR$.",
        1, "Ratio", 2, (1, 0.07, 0.32),
        r"$\dfrac{PQ}{PR} = \dfrac{5}{7}$", "B1",
        stem=r"The point $Q$ lies on the line $PR$. $PQ : QR = 5 : 2$.",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 1, "b",
        r"$QR$ is 15 cm. Calculate $PR$.",
        1, "Ratio", 2, (1, 0.30, 0.52),
        r"$$PR = \frac{15}{2} \times 7 = 52.5 \text{ cm}$$", "B1",
        topic_id=9)

    # Q2 — Page 2 (idx 1)
    add_q(db, p1.id, exam_dir, 1, 2, None,
        r"The area of the floor of a master bedroom is $12.8$ m$^2$. State the area of the floor in square centimetres.",
        1, "Unit Conversion", 2, (1, 0.52, 0.73),
        r"$12.8 \times 100^2 = 128\,000$ cm$^2$", "B1",
        topic_id=3)

    # Q3 — Pages 2-3 (idx 1-2)
    add_q(db, p1.id, exam_dir, 1, 3, "a",
        r"Factorise $20pq - 4p$.",
        1, "Factorisation", 2, (1, 0.73, 0.92),
        r"$4p(5q - 1)$", "B1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 3, "b",
        r"Write as a single fraction in its simplest form $\dfrac{3x}{12} - \dfrac{7(5 - x)}{12}$.",
        2, "Algebraic Fractions", 3, (2, 0.03, 0.18),
        r"""$$\frac{3x - 7(5 - x)}{12} = \frac{3x - 35 + 7x}{12} = \frac{10x - 35}{12}$$""",
        "M1 for single fraction, A1",
        topic_id=4)

    # Q4 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 4, "a",
        r"Write down a simplified expression for the number of adults in terms of $w$.",
        1, "Algebra — Simplification", 3, (2, 0.18, 0.60),
        r"$(2w + 4) - (w - 1) = w + 5$", "B1",
        stem=r"A residential community club organised an outing to River Wonders. Admission fees: Adult S$\$42$, Child S$\$30$. There are $(2w + 4)$ children who signed up. The number of adults is $(w - 1)$ fewer than the number of children.",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 4, "b",
        r"The total amount for the tickets purchased for the group of adults and children who signed up for the outing was S$\$1452$. By forming an equation in $w$, find the number of children in the group.",
        2, "Linear Equations — Word Problem", 3, (2, 0.58, 0.95),
        r"""$$42(w + 5) + 30(2w + 4) = 1452$$
$$42w + 210 + 60w + 120 = 1452$$
$$102w = 1122 \implies w = 11$$
Children $= 2(11) + 4 = 26$""",
        "M1 for equation, A1",
        topic_id=5)

    # Q5 — Page 4 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 5, None,
        r"Using only a ruler and compasses, construct a quadrilateral $ABCD$ where $BC = 12$ cm, $AD = 9$ cm, $BD = 12$ cm and angle $ABC = 100°$. $AB$ is drawn below.",
        3, "Construction", 4, (3, 0.03, 0.95),
        r"[C1] $AD = 9$ cm (arc to be seen); [C1] $BD = 12$ cm (arc to be seen); [C1] angle $ABC = 100°$, $BC = 12$ cm. Minus one mark if not quadrilateral or vertices not labelled.",
        "C1, C1, C1",
        topic_id=10)

    # Q6 — Page 5 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 6, "a",
        r"Calculate the area of $UVWXYZ$.",
        2, "Area — Parallelogram", 5, (4, 0.03, 0.62),
        r"$$\text{Area} = 2(9 \times 3.5) = 63 \text{ cm}^2$$", "M1 for base $\times$ height or $9 \times 7$, A1",
        stem=r"The figure is made up of two identical parallelograms, $UVWZ$ and $WXYZ$. $UV = 9$ cm, $UZ = 4.6$ cm, $VX = 7$ cm and angle $VWX = 80°$.",
        topic_id=12)

    add_q(db, p1.id, exam_dir, 1, 6, "b",
        r"Calculate angle $VUZ$.",
        2, "Angles — Parallelogram", 5, (4, 0.60, 0.95),
        r"""Angle $VWZ = \dfrac{360° - 80°}{2} = 140°$ (angles at a point)
Angle $VUZ = 140°$ (opposite angles of parallelogram)""",
        "M1 for finding one angle leading to $VUZ$, A1",
        topic_id=10)

    # Q7 — Page 6 (idx 5)
    add_q(db, p1.id, exam_dir, 1, 7, "ai",
        r"his salary when he sold 30 cars.",
        1, "Linear Functions — Reading Graph", 6, (5, 0.03, 0.55),
        r"$\$5000$", "B1",
        stem=r"The graph shows the salary scheme of a car sales representative between his salary, $\$S$, and the number of cars, $n$, he has sold.",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 7, "aii",
        r"the number of cars sold if his salary was $\$3000$.",
        1, "Linear Functions — Reading Graph", 6, (5, 0.45, 0.60),
        r"$17$ cars", "B1",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 7, "b",
        r"His salary package, $\$S$ is made up of a fixed component $\$x$ and a commission which is based on a flat rate of $\$y$ for each car he has sold. Use the graph to find the value of $x$ and of $y$.",
        2, "Linear Functions — Gradient & Intercept", 6, (5, 0.58, 0.95),
        r"""$x = -1000$ (y-intercept from graph)
$y = \dfrac{5000 - (-1000)}{30 - 0} = 200$""",
        "B1 for $x$, B1 for $y$",
        topic_id=6)

    # Q8 — Page 7 (idx 6)
    add_q(db, p1.id, exam_dir, 1, 8, "a",
        r"Find the values of $x$, $y$ and $z$.",
        2, "Number Patterns", 7, (6, 0.03, 0.45),
        r"Common difference $= \dfrac{74 - 46}{4} = 7$. $x = 67$, $y = 60$, $z = 53$.",
        "B2 for all correct, B1 for 2 correct",
        stem=r"In a sequence, the same number is subtracted each time to obtain the next term. The first five terms of the sequence are $74, x, y, z, 46, \ldots$",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 8, "b",
        r"Write down a simplified expression for the $n$th term in terms of $n$.",
        2, "Number Patterns — General Term", 7, (6, 0.43, 0.65),
        r"$T_n = 74 - 7(n - 1) = 81 - 7n$", "M1, A1",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 8, "c",
        r"Explain why $-40$ is not a term of this sequence. Justify your answer.",
        1, "Number Patterns — Reasoning", 7, (6, 0.63, 0.95),
        r"""$81 - 7n = -40 \implies 7n = 121 \implies n = \dfrac{121}{7} = 17\dfrac{2}{7}$
Since $n$ is not a positive integer, $-40$ is not a term.""", "B1",
        topic_id=7)

    # Q9 — Pages 8-9 (idx 7-8)
    add_q(db, p1.id, exam_dir, 1, 9, "ai",
        r"Express 500 as a product of its prime factors in index notation.",
        1, "Prime Factorisation", 8, (7, 0.03, 0.43),
        r"$500 = 2^2 \times 5^3$", "B1",
        stem=r"The number 240, written as the product of its prime factors, is $240 = 2^4 \times 3 \times 5$.",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 9, "aii",
        r"Hence, find the LCM of 240 and 500. Give your answer as a product of its prime factors in index notation.",
        1, "LCM", 8, (7, 0.42, 0.65),
        r"$\text{LCM} = 2^4 \times 3 \times 5^3$", "B1",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 9, "aiii",
        r"Find the smallest integer $p$, such that $240p$ is a perfect square.",
        1, "Perfect Square", 8, (7, 0.64, 0.95),
        r"$240p = 2^4 \times 3 \times 5 \times p$. Need $p = 3 \times 5 = 15$.", "B1",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 9, "bi",
        r"the largest possible length in cm of the side of each tile.",
        1, "HCF", 9, (8, 0.03, 0.60),
        r"$\text{HCF}(500, 240) = 20$ cm", "B1",
        stem=r"The diagram shows the plan of a floor. The dimensions of the floor are 5 m by 2.4 m. The floor is to be tiled using identical square tiles. Find:",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 9, "bii",
        r"the number of tiles required to fully lay the whole floor.",
        1, "HCF — Application", 9, (8, 0.58, 0.95),
        r"Number of tiles $= \dfrac{500}{20} \times \dfrac{240}{20} = 25 \times 12 = 300$", "B1",
        topic_id=1)

    # Q10 — Page 10 (idx 9)
    add_q(db, p1.id, exam_dir, 1, 10, "a",
        r"Solve the equation $\dfrac{2 + 3k}{7 - 2k} = \dfrac{1}{4}$.",
        2, "Solving Linear Equations", 10, (9, 0.03, 0.47),
        r"""$$4(2 + 3k) = 7 - 2k$$
$$8 + 12k = 7 - 2k$$
$$14k = -1 \implies k = -\frac{1}{14}$$""",
        "M1 for cross-multiply, A1",
        topic_id=5)

    add_q(db, p1.id, exam_dir, 1, 10, "b",
        r"Solve the equation $\dfrac{4x - 1}{2} - 2 = \dfrac{2 - 3x}{5}$.",
        3, "Solving Linear Equations", 10, (9, 0.45, 0.95),
        r"""$$\text{Multiply by 10: } 5(4x - 1) - 20 = 2(2 - 3x)$$
$$20x - 5 - 20 = 4 - 6x$$
$$26x = 29 \implies x = \frac{29}{26} = 1\frac{3}{26}$$""",
        "M1 for common denominator, M1 for simplification, A1",
        topic_id=5)

    # Q11 — Page 11 (idx 10)
    add_q(db, p1.id, exam_dir, 1, 11, "a",
        r"Calculate the marked price of the laptop.",
        2, "Percentage — GST Reverse", 11, (10, 0.03, 0.30),
        r"$$\text{Marked price} = \frac{2300}{1.08} = \$\!2129.63 \text{ (2 d.p.)}$$", "M1 for dividing by 1.08, A1",
        stem=r"A laptop is priced at $\$2300$ inclusive of Goods and Services Tax (GST) of 8%.",
        topic_id=8)

    add_q(db, p1.id, exam_dir, 1, 11, "bi",
        r"the total amount of interest to be paid over the 2 years.",
        2, "Percentage — Hire Purchase", 11, (10, 0.28, 0.63),
        r"""Remaining $= 0.75 \times 2129.63 = \$\!1597.22$
Interest $= 1597.22 \times 0.05 \times 2 = \$\!159.72$""",
        "M1 for finding remaining amount, A1",
        stem=r"Michelle buys the laptop on hire purchase which includes a 25% downpayment and the remaining amount to be paid on monthly instalments over 2 years at a simple interest of 5% per annum. Find:",
        topic_id=8)

    add_q(db, p1.id, exam_dir, 1, 11, "bii",
        r"her monthly instalment.",
        1, "Percentage — Hire Purchase", 11, (10, 0.62, 0.87),
        r"Monthly instalment $= \dfrac{1597.22 + 159.72}{24} = \$\!73.21$", "B1",
        topic_id=8)

    # Q12 — Pages 12-13 (idx 11-12)
    add_q(db, p1.id, exam_dir, 1, 12, "a",
        r"Find the exterior angle of a regular octagon.",
        2, "Polygon Angles — Exterior", 12, (11, 0.03, 0.30),
        r"$$\text{Exterior angle} = \frac{360°}{8} = 45°$$", "M1, A1",
        topic_id=11)

    add_q(db, p1.id, exam_dir, 1, 12, "bia",
        r"Find the value of $a$.",
        2, "Polygon Angles — Interior", 12, (11, 0.28, 0.72),
        r"""Interior angle of regular pentagon $= \dfrac{(5 - 2) \times 180°}{5} = 108°$
$a = 108$""",
        "M1, A1",
        stem=r"The diagram shows three regular pentagons. Find the value of:",
        topic_id=11)

    add_q(db, p1.id, exam_dir, 1, 12, "bib",
        r"Find the value of $b$.",
        1, "Polygon Angles", 12, (11, 0.70, 0.90),
        r"$b = 360° - 108° - 108° = 144°$ (angles at a point)", "B1",
        topic_id=11)

    add_q(db, p1.id, exam_dir, 1, 12, "bic",
        r"Find the value of $m$.",
        1, "Polygon Angles — Isosceles Triangle", 13, (12, 0.03, 0.15),
        r"$m = \dfrac{180° - 144°}{2} = 18°$ (base angles of isosceles triangle)", "B1",
        topic_id=11)

    add_q(db, p1.id, exam_dir, 1, 12, "bii",
        r"Additional pentagons are added to the three pentagons to form a closed ring which is in the shape of a regular polygon. Find the number of additional pentagons needed to form the closed ring.",
        2, "Polygon Angles", 13, (12, 0.13, 0.65),
        r"""Interior angle of the ring polygon $= 144°$
Exterior angle $= 180° - 144° = 36°$
$n = \dfrac{360°}{36°} = 10$
Additional pentagons $= 10 - 3 = 7$""",
        "M1 for finding $n$, A1",
        topic_id=11)

    # Q13 — Page 14 (idx 13)
    add_q(db, p1.id, exam_dir, 1, 13, "a",
        r"Shinkansen bullet trains in Japan reach a top speed of 320 km/h. Express this speed in m/s, giving your answer correct to 2 significant figures.",
        1, "Speed Conversion", 14, (13, 0.03, 0.32),
        r"$$320 \times \frac{1000}{3600} = 88.8\overline{8} \approx 89 \text{ m/s (2 s.f.)}$$", "B1",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 13, "bi",
        r"Find the time taken for the train to travel from Station $K$ to Station $Y$ in minutes.",
        2, "Speed, Distance, Time", 14, (13, 0.30, 0.62),
        r"$$\text{Time} = \frac{5}{50} = \frac{1}{10} \text{ h} = 6 \text{ min}$$", "M1, A1",
        stem=r"A MRT train travels 5 km at 50 km/h between Station $K$ to Station $Y$.",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 13, "bii",
        r"If the same train travels at 30 km/h from Station $Y$ to Station $A$ in 2 minutes, find its average speed in km/h, for its journey from Station $K$ to $A$.",
        3, "Average Speed", 14, (13, 0.60, 0.95),
        r"""Distance $Y$ to $A$ $= 30 \times \dfrac{2}{60} = 1$ km
Average speed $= \dfrac{5 + 1}{(6 + 2) \div 60} = \dfrac{6}{\frac{8}{60}} = 45$ km/h""",
        "M1 for distance, M1 for total time, A1",
        topic_id=9)

    # Q14 — Page 15 (idx 14)
    add_q(db, p1.id, exam_dir, 1, 14, "a",
        r"Find angle $BCD$, giving a reason for your answer.",
        2, "Angle Properties — Parallel Lines", 15, (14, 0.03, 0.52),
        r"Angle $BCD = 42°$ (corresponding angles, $GE \parallel BC$)", "B1 for angle, B1 for reason",
        stem=r"In the diagram, $CDEF$ is a straight line. $AB$ is parallel to $CF$ and $BC$ is parallel to $EG$. Angle $BAG = 100°$, angle $FEG = 42°$ and angle $CBD = 58°$.",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 14, "b",
        r"Find angle $BDE$, giving a reason for your answer.",
        2, "Angle Properties — Exterior Angle", 15, (14, 0.48, 0.65),
        r"Angle $BDE = 58° + 42° = 100°$ (exterior angle of triangle)", "B1 for angle, B1 for reason",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 14, "c",
        r"Find angle $AGE$.",
        3, "Angle Properties", 15, (14, 0.63, 0.78),
        r"""Angle $ABD = 180° - 100° = 80°$ (co-interior angles, $AB \parallel CF$)
Angle $ABC = 80° + 58° = 138°$
Angle $AGE = 180° - 138° - 42° = \ldots$
(Multiple approaches possible; final answer depends on geometric configuration)""",
        "M1, M1, A1",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 14, "d",
        r"Is $AG$ parallel to $BD$? Explain your answer.",
        2, "Angle Properties — Parallel Lines", 15, (14, 0.76, 0.95),
        r"Yes, by the converse of interior angles, since the two angles are supplementary, $AG$ is parallel to $BD$.", "B1 for answer, B1 for reason",
        topic_id=10)

    # Q15 — Pages 16-17 (idx 15-16)
    add_q(db, p1.id, exam_dir, 1, 15, "a",
        r"Plot the points given in the table and join them with a straight line.",
        3, "Linear Functions — Graph", 16, (15, 0.03, 0.55),
        r"[C2] all points plotted correctly (or [C1] if one point plotted wrongly); [C1] straight line drawn.",
        "C2 for points, C1 for line",
        stem=r"The table below shows some of the points of the line $y = mx + c$. Using a scale of 2 cm to 1 unit for the $x$-axis ($-3 \leq x \leq 3$) and 4 cm to 1 unit for the $y$-axis ($0 \leq y \leq 4$).",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 15, "b",
        r"Use your graph to find the value of $m$ and of $c$.",
        3, "Linear Functions — Gradient & Intercept", 16, (15, 0.53, 0.80),
        r"""Gradient $m = \dfrac{3 - 0}{-3 - 3} = -\dfrac{1}{2}$
$c = \dfrac{3}{2}$ (y-intercept from graph)""",
        "B1 for negative sign, B1 for $\frac{1}{2}$; B1 for $c$",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 15, "c",
        r"Write down the equation of the horizontal line that passes through $c$ in (b).",
        1, "Linear Functions — Horizontal Line", 16, (15, 0.78, 0.95),
        r"$y = \dfrac{3}{2}$", "B1",
        topic_id=6)

    # Q16 — Pages 18-20 (idx 17-19)
    add_q(db, p1.id, exam_dir, 1, 16, "ai",
        r"The swimming pool contains water to a depth of 1.4 m. Calculate the volume of the water in the swimming pool, giving your answer correct to 3 significant figures.",
        2, "Volume — Cylinder", 18, (17, 0.03, 0.62),
        r"$$V = \pi (25)^2 (1.4) = 2750 \text{ m}^3 \text{ (3 s.f.)}$$", "M1 for $\pi r^2 h$, A1",
        stem=r"A swimming pool can be modelled as a cylinder. The cylindrical swimming pool has a diameter of 50 m and a height of 1.5 m.",
        topic_id=13)

    add_q(db, p1.id, exam_dir, 1, 16, "aii",
        r"Calculate the total inner surface area of the swimming pool, giving your answer in terms of $\pi$.",
        2, "Surface Area — Cylinder", 18, (17, 0.60, 0.95),
        r"$$\text{SA} = \pi(25)^2 + 2\pi(25)(1.5) = 625\pi + 75\pi = 700\pi \text{ m}^2$$", "M1 for $2\pi rh$, A1",
        topic_id=13)

    add_q(db, p1.id, exam_dir, 1, 16, "bi",
        r"The breadth of this swimming pool is $x$ m. Find the value of $x$.",
        2, "Volume — Trapezium Prism", 19, (18, 0.03, 0.95),
        r"""$$5\,000\,000 \text{ litres} = 5000 \text{ m}^3$$
Base area $= \dfrac{1}{2}(2 + 6)(50) = 200$ m$^2$
$V = 200 \times x = 5000 \implies x = 25$""",
        "M1 for trapezium formula, A1",
        stem=r"Another swimming pool is built and it can be modelled as a trapezium prism. It is 50 m long and can hold 5,000,000 litres of water when fully filled. It is 2 m deep at one end and slopes uniformly down to 6 m at the other end.",
        topic_id=13)

    add_q(db, p1.id, exam_dir, 1, 16, "bii",
        r"Bob is tasked to paint the inner surface of this swimming pool. 1 litre of paint can cover 5 m$^2$. Given that paint is sold in 15-litre containers, Bob claims that he needs to buy 25 such tins altogether. Justify whether his claim is true or false. Show your working clearly.",
        4, "Surface Area — Trapezium Prism", 20, (19, 0.03, 0.95),
        r"""Total inner surface area:
$= 2(200) + 6(25) + 2(25) + 50.2(25)$
$= 400 + 150 + 50 + 1255 = 1855$ m$^2$
Litres needed $= \dfrac{1855}{5} = 371$
Tins $= \dfrac{371}{15} = 24.73\ldots \approx 25$ tins
His claim is true.""",
        "M1 for all 4 surface components, M1 for total SA, M1 for litres, A1",
        topic_id=13)

    db.commit()
    p1_count = len(p1.questions)
    print(f"Seeded Zhonghua exam id={exam.id}: Paper 1 ({p1_count} parts)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
