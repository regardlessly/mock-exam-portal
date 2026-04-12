"""Seed North Vista Secondary School EOY 2020 Sec 1 Express Math exam."""

import os
import shutil
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/North-Vista-Secondary-End-of-Year-2020-Sec-1-Math.pdf"
IMAGES_DIR = "/tmp/northvista_pages"

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

    school = db.query(School).filter(School.name == "North Vista Secondary School").first()
    if not school:
        school = School(name="North Vista Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(Exam.school_id == school.id, Exam.year == 2020).first()
    if existing:
        print(f"North Vista 2020 already seeded (id={existing.id}). Deleting and re-seeding.")
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
        source_pdf="North-Vista-Secondary-End-of-Year-2020-Sec-1-Math.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # Single Paper — Pages 2-19 (idx 1-18), 80 marks, 2 hours
    # Section 1: Q1-13 (short answer)
    # Section 2: Q14-21 (structured)
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=120, total_marks=80,
               date=date(2020, 9, 30), instructions="Answer all questions.")
    db.add(p1); db.flush()

    # ── Section 1 ──

    # Q1 — Page 2 (idx 1)
    add_q(db, p1.id, exam_dir, 1, 1, "a",
        r"the integer(s).",
        1, "Number Classification", 2, (1, 0.08, 0.30),
        r"$1$, $\sqrt[3]{-27}$, $5$", "B1",
        stem=r"Consider the following numbers: $1$, $\dfrac{22}{7}$, $\sqrt[3]{-27}$, $-5\dfrac{1}{8}$, $\pi$, $0.\dot{3}$, $\sqrt{3}$, $5$. Write down",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 1, "b",
        r"the irrational number(s).",
        1, "Number Classification", 2, (1, 0.30, 0.42),
        r"$\pi$, $\sqrt{3}$", "B1",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 1, "c",
        r"the prime number(s).",
        1, "Number Classification", 2, (1, 0.42, 0.53),
        r"$5$", "B1",
        topic_id=2)

    # Q2 — Page 2 (idx 1)
    add_q(db, p1.id, exam_dir, 1, 2, "a",
        r"Calculate $\dfrac{\pi - 6.2^2}{\sqrt[4]{20} - 3\dfrac{2}{7}}$, write down the first six digits shown on your calculator display.",
        1, "Calculator Usage", 2, (1, 0.53, 0.82),
        r"$30.8896$", "B1",
        topic_id=3)

    add_q(db, p1.id, exam_dir, 1, 2, "b",
        r"Give your answer to part (a) correct to 4 significant figures.",
        1, "Significant Figures", 2, (1, 0.82, 0.95),
        r"$30.89$", "B1",
        topic_id=3)

    # Q3 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 3, None,
        r"The diagram shows a prism whose cross-section is an isosceles triangle. All dimensions are given in metres. Calculate the volume of the prism and leave your answers in cm$^3$.",
        2, "Volume — Prism", 3, (2, 0.04, 0.55),
        r"$$\text{Area} = \frac{1}{2} \times 3.6 \times 2.4 = 86.4 \text{ m}^2$$\n$$V = 86.4 \times 20 = 84\,400\,000 \text{ cm}^3$$",
        "M1, A1",
        topic_id=13)

    # Q4 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 4, None,
        r"A cylindrical pipe with diameter 3.2 cm discharges water at a rate of 360 cm/s. Find the volume of water discharged in 30 seconds, giving your answer to the nearest cm$^3$.",
        2, "Volume — Cylinder", 3, (2, 0.55, 0.78),
        r"$$V = \pi \times 1.6^2 \times 360 \times 30 = 86\,858 \text{ cm}^3$$", "M1, A1",
        topic_id=13)

    # Q5 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 5, None,
        r"Mr Yee sold his private property and earned a 30% profit. If the profit earned is $\$350\,400$, find the cost price of the property.",
        2, "Percentage — Reverse", 3, (2, 0.78, 0.97),
        r"$$\text{Cost price} = \frac{350\,400}{30} \times 100 = \$1\,168\,000$$", "M1, A1",
        topic_id=8)

    # Q6 — Page 4 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 6, None,
        r"Three of the interior angles of an $n$-sided polygon are $156°$, $117°$ and $135°$, and the remaining interior angles are $123°$ each. Find the value of $n$.",
        3, "Polygon Angles", 4, (3, 0.04, 0.46),
        r"""$(n - 2) \times 180 = 156 + 117 + 135 + 123(n - 3)$
$180n - 360 = 408 + 123n - 369$
$57n = 399$
$n = 7$""",
        "M1, M1, A1",
        topic_id=11)

    # Q7 — Page 4 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 7, None,
        r"Mrs Eliza is $(15x - 6)$ years old. She is thrice as old as her daughter, Beth. Find the age of Mrs Eliza, in terms of $x$, when she gave birth to Beth.",
        3, "Linear Expressions", 4, (3, 0.46, 0.97),
        r"""Beth's age $= \dfrac{15x - 6}{3} = 5x - 2$
Age at birth $= (15x - 6) - (5x - 2) = 10x - 4$ years old""",
        "M1, M1, A1",
        topic_id=4)

    # Q8 — Page 5 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 8, "a",
        r"The interior angle of a regular polygon is $162°$. Calculate the number of sides that the polygon has.",
        2, "Polygon Angles — Interior", 5, (4, 0.04, 0.48),
        r"Exterior angle $= 180° - 162° = 18°$. Number of sides $= \dfrac{360°}{18°} = 20$", "M1, A1",
        topic_id=11)

    add_q(db, p1.id, exam_dir, 1, 8, "b",
        r"Calculate the exterior angle of a regular pentagon.",
        1, "Polygon Angles — Exterior", 5, (4, 0.48, 0.80),
        r"$\dfrac{360°}{5} = 72°$", "B1",
        topic_id=11)

    # Q9 — Page 6 (idx 5)
    add_q(db, p1.id, exam_dir, 1, 9, "a",
        r"Given the perimeter of the field is 400 m, find in terms of $\pi$, the radius, $r$, of the semi-circle.",
        2, "Perimeter — Composite", 6, (5, 0.04, 0.55),
        r"""$2\pi r + 200 = 400$
$r = \dfrac{100}{\pi}$ m""",
        "M1, A1",
        stem=r"The diagram below shows a school field made up of a rectangle and two semi-circles.",
        topic_id=12)

    add_q(db, p1.id, exam_dir, 1, 9, "b",
        r"Hence, find the area of the field leaving your answers correct to the nearest m$^2$.",
        2, "Area — Composite", 6, (5, 0.55, 0.97),
        r"""$$A = \pi\left(\frac{100}{\pi}\right)^2 + 100 \times 2 \times \frac{100}{\pi} = \frac{10\,000}{\pi} + \frac{20\,000}{\pi} = \frac{30\,000}{\pi} \approx 9549 \text{ m}^2$$""",
        "M1 (ECF), A1",
        topic_id=12)

    # Q10 — Page 7 (idx 6)
    add_q(db, p1.id, exam_dir, 1, 10, "a",
        r"angle $ABC$.",
        1, "Angle Properties — Parallelogram", 7, (6, 0.04, 0.53),
        r"$\angle ABC = 180° - 51° = 129°$ (int. angles, $AB \parallel FC$)", "B1",
        stem=r"$ABCE$ is a parallelogram, angle $a$ = angle $b$ = angle $c$ and angle $BCD$ is $51°$. Stating your reasons clearly, find",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 10, "b",
        r"angle $AEF$.",
        1, "Angle Properties — Corresponding", 7, (6, 0.53, 0.70),
        r"$\angle AEF = 51°$ (corr. angles, $BC \parallel AE$)", "B1",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 10, "c",
        r"angle $ADE$.",
        2, "Angle Properties — Exterior", 7, (6, 0.70, 0.95),
        r"""Angle $c = 17°$
Angle $ADE = 51° - 17° = 34°$ (ext angle of triangle)""",
        "M1, A1",
        topic_id=10)

    # Q11 — Page 8 (idx 7)
    add_q(db, p1.id, exam_dir, 1, 11, "ai",
        r"the greatest whole number that will divide both $p$ and $q$ exactly.",
        1, "HCF", 8, (7, 0.04, 0.35),
        r"$\text{HCF} = 2^2 \times 7 = 28$", "B1",
        stem=r"The numbers $p$ and $q$, written as the products of their prime factors are $p = 2^4 \times 3^3 \times 7$ and $q = 2^2 \times 7^2 \times 11^6$. Find",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 11, "aii",
        r"their LCM, leaving your answer as a product of its prime factors.",
        1, "LCM", 8, (7, 0.35, 0.55),
        r"$\text{LCM} = 2^4 \times 3^3 \times 7^2 \times 11^6$", "B1",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 11, "b",
        r"Explain with working, if $pq$ is a perfect cube.",
        2, "Perfect Cube", 8, (7, 0.55, 0.95),
        r"$pq = 2^6 \times 3^3 \times 7^3 \times 11^6$. Since all the indices of its prime factors are multiples of 3, $pq$ is a perfect cube.", "A1",
        topic_id=1)

    # Q12 — Page 9 (idx 8)
    add_q(db, p1.id, exam_dir, 1, 12, "a",
        r"If it took her 16 h 10 min to reach Geneva from Singapore, how long did Hannah wait for her next flight at Dubai airport?",
        1, "Time Calculation", 9, (8, 0.04, 0.48),
        r"$16 \text{ h } 10 \text{ min} - 7 \text{ h } 30 \text{ min} - 7 \text{ h } 5 \text{ min} = 1 \text{ h } 35 \text{ min}$ or $95$ min", "B1",
        stem=r"Hannah took a flight at 0935 from Singapore to Dubai, then took the next available flight from Dubai to Geneva. Singapore to Dubai: 7 h 30 min, 5842 km. Dubai to Geneva: 7 h 5 min, 4924 km.",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 12, "b",
        r"Hannah reached Geneva on the same day at 1845 local time. Determine the time difference between Singapore and Geneva.",
        1, "Time Zones", 9, (8, 0.48, 0.72),
        r"$7$ hours", "B1",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 12, "c",
        r"Calculate the average speed for the entire flight journey. Leave your answer to the nearest km/h.",
        2, "Average Speed", 9, (8, 0.72, 0.97),
        r"$$\frac{5842 + 4924}{16\frac{10}{60}} = \frac{10\,766}{16.1\overline{6}} \approx 666 \text{ km/h}$$", "M1, A1",
        topic_id=9)

    # Q13 — Page 10 (idx 9)
    add_q(db, p1.id, exam_dir, 1, 13, "a",
        r"$3.5x - 0.7 = 2x + 9.8$",
        2, "Linear Equations", 10, (9, 0.04, 0.45),
        r"$1.5x = 10.5 \implies x = 7$", "M1, A1",
        stem=r"Solve the following equations.",
        topic_id=5)

    add_q(db, p1.id, exam_dir, 1, 13, "b",
        r"$\dfrac{7y - 3}{9y - 5} = \dfrac{2}{3}$",
        2, "Linear Equations — Fractions", 10, (9, 0.45, 0.95),
        r"""$3(7y - 3) = 2(9y - 5)$
$21y - 9 = 18y - 10$
$3y = -1$
$y = -\dfrac{1}{3}$""",
        "M1, A1",
        topic_id=5)

    # ── Section 2 ──

    # Q14 — Page 11 (idx 10)
    add_q(db, p1.id, exam_dir, 1, 14, "a",
        r"Complete the table.",
        1, "Number Patterns — Table", 11, (10, 0.04, 0.55),
        r"Figure 4: 4 squares, 10 circles. Figure 5: 5 squares, 12 circles.", "B1",
        stem=r"The first three figures of a sequence are as shown.",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 14, "b",
        r"Find an expression, in terms of $n$, for the number of circles in Figure $n$.",
        1, "Number Patterns — General Term", 11, (10, 0.55, 0.72),
        r"$2n + 2$", "B1",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 14, "c",
        r"Find the number of circles in Figure 78.",
        1, "Number Patterns", 11, (10, 0.72, 0.84),
        r"$2(78) + 2 = 158$", "B1",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 14, "d",
        r"Will there be a pattern with a total of 601 circles? Explain your answer.",
        1, "Number Patterns — Reasoning", 11, (10, 0.84, 0.97),
        r"No. $2n + 2 = 601 \implies n = 299.5$. Since $n$ must be a positive integer, 601 circles is not possible. The number of circles will always be even numbers whereas 601 is an odd number.", "B1",
        topic_id=7)

    # Q15 — Page 12 (idx 11)
    add_q(db, p1.id, exam_dir, 1, 15, None,
        r"Stating your reasons clearly, find the value of the unknown in the following figure.",
        4, "Angle Properties — Parallel Lines", 12, (11, 0.04, 0.95),
        r"""$a1 = 2a - 10$ (alt. angles, $\parallel$ lines)
$a2 = a + 7$ (alt. angles, $\parallel$ lines)
$2a - 10 + a + 7 + 276 = 360$ (angles at a point)
$3a + 273 = 360$
$a = 29$""",
        "M1, M1, M1, A1",
        topic_id=10)

    # Q16 — Page 13 (idx 12)
    add_q(db, p1.id, exam_dir, 1, 16, "a",
        r"State one feature of the graph that may be misleading.",
        1, "Data Handling — Misleading Graphs", 13, (12, 0.04, 0.50),
        r"It is not clear if the height or the area of each picture is to be used in comparing the number of pets. Legend / Key is not given for comparison.", "B1",
        stem=r"The number of pets each of the three friends Rei, Ian and Luke owns, is shown in the pictogram below.",
        topic_id=14)

    add_q(db, p1.id, exam_dir, 1, 16, "b",
        r"Would it be better to present the above information with a line graph? Explain your answer.",
        1, "Data Handling — Graph Types", 13, (12, 0.50, 0.72),
        r"No. Line graph is used to observe the rising or falling of a trend. The line graph is used to plot the data over time.", "B1",
        topic_id=14)

    add_q(db, p1.id, exam_dir, 1, 16, "c",
        r"Rei decided to represent the above information using a pie chart. If each animal represent 3 pets owned by a friend, find the angle of the sector that represent Rei's number of pets.",
        2, "Data Handling — Pie Chart", 13, (12, 0.72, 0.97),
        r"$\dfrac{2}{9} \times 360° = 80°$", "M1, A1",
        topic_id=14)

    # Q17 — Page 14 (idx 13)
    add_q(db, p1.id, exam_dir, 1, 17, "a",
        r"Construct a quadrilateral $JKLM$ such that $KL = 7$ cm, $JM = 10$ cm, angle $JKL = 110°$ and angle $MJK = 80°$. $JK$ has already been drawn.",
        3, "Construction", 14, (13, 0.04, 0.82),
        r"B1 for $JM$ with correct angle and length, B1 for $KL$ with correct angle and length, B1 for joining $M$ to $L$ to form quadrilateral $JKLM$ with correct labelling.", "B3",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 17, "b",
        r"Measure and write down the length of $LM$.",
        1, "Construction — Measurement", 14, (13, 0.82, 0.97),
        r"$LM = 10.1 \pm 0.1$ cm", "B1",
        topic_id=10)

    # Q18 — Page 15 (idx 14)
    add_q(db, p1.id, exam_dir, 1, 18, "a",
        r"Calculate his monthly instalment if he choose Option 2.",
        3, "Percentage — Hire Purchase", 15, (14, 0.04, 0.62),
        r"""Deposit $= 3580 \times 0.85 = \$3043$
Interest $= 3043 \times \dfrac{8}{100} \times 2 = \$486.88$
Monthly instalment $= \dfrac{3043 + 486.88}{24} = \$147.08$""",
        "M1, M1, A1",
        stem=r"Wei Kang wanted to buy a 55-inch OLED TV for his new house. Option 1: Cash $\$3580$. Option 2: Hire Purchase — deposit of 15% of cash price plus 2 years of monthly payment at an interest of 8% per annum.",
        topic_id=8)

    add_q(db, p1.id, exam_dir, 1, 18, "b",
        r"How much would he save if he choose Option 1 instead?",
        1, "Percentage — Savings", 15, (14, 0.62, 0.97),
        r"$\$486.88$", "B1",
        topic_id=8)

    # Q19 — Page 16 (idx 15)
    add_q(db, p1.id, exam_dir, 1, 19, "a",
        r"Find the amount he targeted to save.",
        2, "Ratio — Word Problem", 16, (15, 0.04, 0.38),
        r"""Monday : rest of week $= 1 : 5$
$\dfrac{3}{10} \div \dfrac{6}{15} \text{ rep } \$8.20$
Total amount $= 8.2 \div 2 \times 15 = \$61.50$""",
        "M1, A1",
        stem=r"Lucas planned to save a certain amount of money in one week to buy a toy figurine. He saved some money every day, starting Monday. The ratio of the amount of money he saved on Monday to the amount he saved for the rest of the days (Tuesday to Sunday) is $1 : 5$. After he saved another $\$8.20$ on Tuesday, he was 70% away from his targeted amount. For the rest of the week, he saved the same amount of money every day.",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 19, "b",
        r"Calculate the amount of money he saved every day for the rest of the week.",
        2, "Ratio — Word Problem", 16, (15, 0.38, 0.62),
        r"""$\dfrac{1}{5} \times 61.50 = 10.25$ (ECF)
$(61.5 - 10.25 - 8.2) \div 5 = \$8.61$""",
        "M1 (ECF), A1",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 19, "c",
        r"After a week, he happily took the saved amount of money to buy the toy figurine. But the price of the toy figurine had changed. The cashier showed him a balance of $-\$3.40$ after he had paid the amount using all his savings. Find the price of the toy figurine.",
        2, "Negative Numbers — Context", 16, (15, 0.62, 0.97),
        r"$\$61.50 - (-\$3.40) = \$64.90$", "M1 (ECF), A1",
        topic_id=2)

    # Q20 — Page 17 (idx 16)
    add_q(db, p1.id, exam_dir, 1, 20, "a",
        r"Factorise $-11ax - 33ay - 22az$ completely.",
        1, "Algebra — Factorisation", 17, (16, 0.04, 0.18),
        r"$-11a(x + 3y + 2z)$", "B1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 20, "b",
        r"It is given that $s = ut + \dfrac{1}{2}at^2$. Find $s$ when $u = \dfrac{1}{2}$, $a = 0.25$ and $t = 16$.",
        1, "Formula Substitution", 17, (16, 0.18, 0.40),
        r"$s = \dfrac{1}{2}(16) + \dfrac{1}{2}(0.25)(16^2) = 8 + 32 = 35.2$ or $35\dfrac{1}{5}$", "B1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 20, "ci",
        r"$3(9x - 5y) - 7(-2y + x)$.",
        2, "Algebra — Expansion", 17, (16, 0.40, 0.62),
        r"$27x - 15y + 14y - 7x = 20x - y$", "M1, A1",
        stem=r"Simplify the following expressions.",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 20, "cii",
        r"$\dfrac{13x + 1}{6} + \dfrac{4 - 8x}{9}$.",
        2, "Algebra — Fractions", 17, (16, 0.62, 0.95),
        r"""$$= \frac{3(13x + 1) + 2(4 - 8x)}{18} = \frac{39x + 3 + 8 - 16x}{18} = \frac{23x + 11}{18}$$""",
        "M1, A1",
        topic_id=4)

    # Q21 — Pages 18-19 (idx 17-18)
    add_q(db, p1.id, exam_dir, 1, 21, "ai",
        r"Stool A.",
        3, "Surface Area — Prism", 18, (17, 0.04, 0.58),
        r"""$$\text{SA} = 2\left(\frac{1}{2} \times (45 + 55) \times 45\right) - (35 \times 35) + 45(45 + 45.3 + 55 + 45.3 + 35 + 35)$$
$= 13\,777 \text{ cm}^2$""",
        "M1 for cross-sectional area, M1 for lateral area, A1",
        stem=r"Samuel plans to purchase and paint the surface of the wooden stools shown below. Stool A has a uniform cross-sectional area and Stool B is made up of one cylindrical seat and four identical cylindrical legs.",
        topic_id=13)

    add_q(db, p1.id, exam_dir, 1, 21, "aii",
        r"Stool B.",
        3, "Surface Area — Cylinder", 18, (17, 0.58, 0.97),
        r"""$$\text{SA} = 2\pi\left(\frac{45}{2}\right)^2 + 2\pi\left(\frac{45}{2}\right)(10) + 2\pi\left(\frac{5}{2}\right)(35) \times 4$$
$= 6794 \text{ cm}^2$""",
        "M1 for cross-sectional area, M1 for lateral area, A1",
        topic_id=13)

    add_q(db, p1.id, exam_dir, 1, 21, "b",
        r"A can of paint cost $\$2.33$. Each can of paint covers an area of 600 cm$^2$. Will he have enough money to paint both stools if he has $\$80$? Justify your answer with working.",
        2, "Surface Area — Application", 19, (18, 0.04, 0.30),
        r"""Total SA $= 13\,777 + 6794 = 20\,571$ cm$^2$ (approx.)
Cans needed $= \lceil 20\,571 \div 600 \rceil = 35$ cans
Cost $= 35 \times 2.33 = \$81.55$
He will not have enough money for the paint.""",
        "M1 (ECF), A1 (Dependent)",
        topic_id=13)

    db.commit()
    p1_count = len(p1.questions)
    print(f"Seeded North Vista exam id={exam.id}: Paper 1 ({p1_count} parts)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
