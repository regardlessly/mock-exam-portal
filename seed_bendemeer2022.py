"""Seed Bendemeer Secondary School EOY 2022 Sec 1 Express Math exam."""

import os
import shutil
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/66b1f55957476_5778.pdf"
IMAGES_DIR = "/tmp/bendemeer2022_pages"

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

    school = db.query(School).filter(School.name == "Bendemeer Secondary School").first()
    if not school:
        school = School(name="Bendemeer Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(Exam.school_id == school.id, Exam.year == 2022).first()
    if existing:
        print(f"Bendemeer 2022 already seeded (id={existing.id}). Deleting and re-seeding.")
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
        source_pdf="66b1f55957476_5778.pdf", status="ready",
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
               date=date(2022, 10, 10), instructions="Answer all questions.")
    db.add(p1); db.flush()

    # Q1 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 1, "a",
        r"a prime number,",
        1, "Number Classification", 3, (2, 0.06, 0.32),
        r"$\sqrt{4} = 2$", "A1",
        stem=r"From numbers given below, write down: $\sqrt{4}$, $\pi$, $\dfrac{22}{7}$, $\sqrt{5}$, $9$, $-6$.",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 1, "b",
        r"an irrational number,",
        1, "Number Classification", 3, (2, 0.31, 0.44),
        r"$\pi$ or $\sqrt{5}$. Any one of the answers.", "A1",
        topic_id=2)

    # Q2 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 2, "a",
        r"Without the use of calculator, evaluate $\left[\dfrac{2}{3} + \left(-\dfrac{1}{6}\right)\right] \div \dfrac{6}{7} \times \left(\dfrac{4}{5} - \dfrac{3}{10}\right)$ with necessary workings.",
        2, "Order of Operations", 3, (2, 0.44, 0.78),
        r"""$$= \left[\frac{4}{6} - \frac{1}{6}\right] \div \frac{6}{7} \times \left(\frac{8}{10} - \frac{3}{10}\right)$$
$$= \frac{1}{2} \div \frac{6}{7} \times \frac{1}{2} = \frac{1}{2} \times \frac{7}{6} \times \frac{1}{2} = \frac{7}{24}$$""",
        "M0.5, M0.5, M0.5, A0.5",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 2, "b",
        r"Using a calculator, evaluate the following, leaving your answer in 3 significant figures. $\dfrac{3.25 \times \sqrt{1.22}}{11 - 2.8^3}$",
        2, "Calculator Use / Sig Figs", 3, (2, 0.78, 0.97),
        r"$= -0.33777\ldots \approx -0.338$", "M1, A1",
        topic_id=3)

    # Q3 — Page 4 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 3, "ai",
        r"Write 360 as a product of its prime numbers.",
        1, "Prime Factorisation", 4, (3, 0.04, 0.20),
        r"$360 = 2^3 \times 3^2 \times 5$", "A1",
        stem=r"The number 240, written as a product of its prime factors, is $2^4 \times 3 \times 5$.",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 3, "aii",
        r"Find the HCF of both 240 and 360.",
        1, "HCF", 4, (3, 0.20, 0.36),
        r"$\text{HCF} = 2^3 \times 3 \times 5 = 120$", "A1",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 3, "aiii",
        r"Find the smallest non-zero whole number $m$ for which $\dfrac{360}{m}$ is a factor of 240.",
        1, "Factors / HCF", 4, (3, 0.36, 0.60),
        r"$m = 3$", "A1",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 3, "b",
        r"Given that $A = xyz$, $B = xy^3$ and $C = x^3yz^2$, find the lowest common multiple of $A$, $B$ and $C$.",
        1, "LCM — Algebraic", 4, (3, 0.60, 0.88),
        r"$\text{LCM} = x^3 y^3 z^2$", "A1",
        topic_id=1)

    # Q4 — Page 5 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 4, "a",
        r"$\dfrac{3}{10} : \dfrac{5}{6}$",
        1, "Ratio", 5, (4, 0.04, 0.22),
        r"$9 : 25$", "B1",
        stem=r"Express each ratio in its simplest form.",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 4, "b",
        r"$0.5 \text{ km} : 8\dfrac{1}{10} \text{ m} : 20 \text{ cm}$",
        2, "Ratio — Unit Conversion", 5, (4, 0.22, 0.42),
        r"""$0.5 \text{ km} = 50\,000 \text{ cm}$, $8\frac{1}{10} \text{ m} = 810 \text{ cm}$
$50\,000 : 810 : 20 = 5000 : 81 : 2$""",
        "M1, A1",
        topic_id=9)

    # Q5 — Page 5 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 5, "a",
        r"$-4(-2x + y) - 3(x - 6y)$.",
        2, "Algebra — Expansion", 5, (4, 0.42, 0.64),
        r"$8x - 4y - 3x + 18y = 5x + 14y$", "M1, A1",
        stem=r"Expand and simplify the following.",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 5, "b",
        r"$\dfrac{5x}{7} + 7\!\left(\dfrac{2}{7}x - x + 2x\right)$.",
        2, "Algebra — Expansion", 5, (4, 0.64, 0.90),
        r"""$$= \frac{5x}{7} + 7 \times \frac{9x}{7} = \frac{5x}{7} + 9x = \frac{5x + 63x}{7} = \frac{68x}{7}$$""",
        "M1, A1",
        topic_id=4)

    # Q6 — Page 6 (idx 5)
    add_q(db, p1.id, exam_dir, 1, 6, "a",
        r"$\dfrac{-5x + 3y}{3} - \dfrac{y + 3x}{8}$",
        2, "Algebraic Fractions", 6, (5, 0.04, 0.48),
        r"""$$= \frac{8(-5x + 3y) - 3(y + 3x)}{24} = \frac{-40x + 24y - 3y - 9x}{24} = \frac{-49x + 21y}{24}$$""",
        "M1, A1",
        stem=r"Express the following as a single fraction in its simplest form.",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 6, "b",
        r"$\dfrac{3(x+1)}{2} + \dfrac{4(x-1)}{5}$",
        2, "Algebraic Fractions", 6, (5, 0.48, 0.92),
        r"""$$= \frac{15(x+1) + 8(x-1)}{10} = \frac{15x + 15 + 8x - 8}{10} = \frac{23x + 7}{10}$$""",
        "M0.5, M0.5, A1",
        topic_id=4)

    # Q7 — Page 7 (idx 6)
    add_q(db, p1.id, exam_dir, 1, 7, "a",
        r"Factorise $64x^2y + 16xyz - 24xy$ completely.",
        1, "Algebra — Factorisation", 7, (6, 0.04, 0.16),
        r"$8xy(8x + 2z - 3)$", "A1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 7, "bi",
        r"Expand $a(x - y)$.",
        1, "Algebra — Expansion", 7, (6, 0.16, 0.28),
        r"$ax - ay$", "A1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 7, "bii",
        r"Hence use the answer in (b)(i) to evaluate $28 \times 165 - 28 \times 65$.",
        2, "Algebra — Application", 7, (6, 0.28, 0.44),
        r"$= 28(165 - 65) = 28(100) = 2800$", "M1, A1",
        topic_id=4)

    # Q8 — Page 7 (idx 6)
    add_q(db, p1.id, exam_dir, 1, 8, "a",
        r"A new car costs $\$120\,000$. After one year, it is worth $\$108\,000$. Find the percentage decrease in the value of the car.",
        2, "Percentage Decrease", 7, (6, 0.44, 0.70),
        r"""Decrease $= \$12\,000$
Percentage decrease $= \frac{12\,000}{120\,000} \times 100\% = 10\%$""",
        "M1, A1",
        topic_id=8)

    add_q(db, p1.id, exam_dir, 1, 8, "b",
        r"Chery invested $\$6000$ in a bank that gave interest of 2% per annum. Find the simple interest Chery received after a period of 9 months.",
        2, "Simple Interest", 7, (6, 0.70, 0.92),
        r"Interest $= 6000 \times 2\% \times \frac{9}{12} = \$90$", "M1, A1",
        topic_id=8)

    # Q9 — Page 8 (idx 7)
    add_q(db, p1.id, exam_dir, 1, 9, None,
        r"Given that the exterior angle of regular polygon is $15°$, how many angles does this polygon have?",
        2, "Polygon Angles", 8, (7, 0.04, 0.16),
        r"$n = \frac{360°}{15°} = 24$", "M1, A1",
        topic_id=11)

    # Q10 — Page 8 (idx 7)
    add_q(db, p1.id, exam_dir, 1, 10, "a",
        r"Write down, in terms of $x$, the area of $ABCD$.",
        1, "Algebra — Area", 8, (7, 0.16, 0.58),
        r"Area $= 5(2x - 7)$ cm$^2$", "A1",
        stem=r"The diagram below shows a rectangle $PQRS$ and a parallelogram $ABCD$ where $PQ = AB$ and both shapes share the same height. Dimensions: $(x - 3)$ cm, $(2x - 7)$ cm, $5$ cm.",
        topic_id=12)

    add_q(db, p1.id, exam_dir, 1, 10, "b",
        r"It is given that the area of the rectangle is 55 cm$^2$, form an equation in $x$ and solve it.",
        3, "Linear Equations", 8, (7, 0.58, 0.76),
        r"""$$5(2x - 7) = 55$$
$$2x - 7 = 11$$
$$2x = 18, \quad x = 9$$""",
        "M1 for equation, M1 for solving, A1",
        topic_id=5)

    add_q(db, p1.id, exam_dir, 1, 10, "c",
        r"Hence, find the length of $AD$.",
        1, "Substitution", 8, (7, 0.76, 0.84),
        r"$AD = x - 3 = 9 - 3 = 6$ cm", "A1",
        topic_id=5)

    add_q(db, p1.id, exam_dir, 1, 10, "d",
        r"Find the perimeter of the parallelogram $ABCD$.",
        2, "Perimeter", 8, (7, 0.84, 0.96),
        r"Perimeter $= 2(6 + 11) = 34$ cm", "M1, A1",
        topic_id=12)

    # Q11 — Page 9 (idx 8)
    add_q(db, p1.id, exam_dir, 1, 11, "a",
        r"Find the gradient of $AB$.",
        2, "Linear Functions — Gradient", 9, (8, 0.04, 0.56),
        r"""$$\text{Gradient} = \frac{3 - (-1)}{4 - (-4)} = \frac{4}{8} = 0.5$$""",
        "M1, A1",
        stem=r"The points $A(-4, -1)$ and $B(4, 3)$ are shown in the diagram below.",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 11, "b",
        r"What is the value of the $y$-intercept?",
        1, "Linear Functions — Intercept", 9, (8, 0.56, 0.72),
        r"$y$-intercept $= 1$", "A1",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 11, "c",
        r"Write down the equation of the line $AB$.",
        1, "Linear Functions — Equation", 9, (8, 0.72, 0.88),
        r"$y = 0.5x + 1$", "A1",
        topic_id=6)

    # Q12 — Page 10 (idx 9)
    add_q(db, p1.id, exam_dir, 1, 12, "a",
        r"$\dfrac{2x - 5}{3x + 2} = \dfrac{1}{4}$",
        2, "Solving Linear Equations", 10, (9, 0.04, 0.50),
        r"""$$4(2x - 5) = 3x + 2$$
$$8x - 20 = 3x + 2$$
$$5x = 22, \quad x = 4.4$$""",
        "M1, A1",
        stem=r"Solve the following equations.",
        topic_id=5)

    add_q(db, p1.id, exam_dir, 1, 12, "b",
        r"$0.3x - 1.7 = 4.3 - 0.9x$",
        2, "Solving Linear Equations", 10, (9, 0.50, 0.96),
        r"""$$1.2x = 6$$
$$x = 5$$""",
        "M1, A1",
        topic_id=5)

    # Q13 — Page 11 (idx 10)
    add_q(db, p1.id, exam_dir, 1, 13, None,
        r"In the figure below, find the values of $x$ and $y$, stating your reasons clearly.",
        4, "Angle Properties — Parallel Lines", 11, (10, 0.04, 0.90),
        r"""$\angle ADF = 68°$ (alt. angles, $AB \parallel EC$)
$\angle PDE = 72°$ (alt. angles, $PQ \parallel EC$)
$x + 10 + 68 + 72 = 360° \implies x + 10 = 140° \implies x = 130$
$\angle BQD = 68°$ (corr. angles, $AD \parallel BC$)
$\angle DBC = 180° - 2(68°) = 44°$ (sum of angles of isos. triangle)
$y = 44$""",
        "M0.5 for alt angles (68), M0.5 for alt angles (72), A1 for x = 130, M1 for corr angles, A1 for y = 44",
        topic_id=10)

    # ══════════════════════════════════════════════
    # PAPER 2 — Pages 13-22 (idx 12-21), 50 marks, 1h15m
    # ══════════════════════════════════════════════
    p2 = Paper(exam_id=exam.id, paper_number=2, duration_minutes=75, total_marks=50,
               date=date(2022, 10, 11), instructions="Answer all questions.")
    db.add(p2); db.flush()

    # P2 Q1 — Pages 13-14 (idx 12-13)
    add_q(db, p2.id, exam_dir, 2, 1, "a",
        r"If the TV cost $\$800$, calculate the total amount of money she need to pay if she paid using PayPay.",
        2, "Percentage — Discount", 14, (13, 0.04, 0.24),
        r"""Shop Voucher $= \$30$ (min. spend $\$500$).
Price after voucher $= 800 - 30 = \$770$.
PayPay 25% off: $770 \times 0.75 = \$577.50$.
Delivery $\$20$: Total $= \$577.50 + \$20 = \$597.50$""",
        "M1 for working, A1",
        stem=r"Emily signed up with an online shopping app called Shopi and bought a TV during the 9.9 Super Shoppers Sale. TV Shop Voucher: $\$30$ off (min. spend $\$500$), $\$60$ off (min. spend $\$1000$). Shopi Member's Discount Voucher: 20% off Final Bill. Shopi Discount Voucher: 25% off for payment using PayPay. $\$20$ delivery fee applies; free delivery for items more than $\$1000$.",
        topic_id=8)

    add_q(db, p2.id, exam_dir, 2, 1, "bi",
        r"her downpayment,",
        2, "Hire Purchase", 14, (13, 0.24, 0.52),
        r"Downpayment $= 10\% \times 2000 = \$200$", "M1, A1",
        stem=r"Emily changed her mind and bought a $\$2000$ smart TV using the Hire and Purchase plan. 10% downpayment and 5% per annum interest rate for 2 years plan. Vouchers cannot be used. Delivery fee is waived.",
        topic_id=8)

    add_q(db, p2.id, exam_dir, 2, 1, "bii",
        r"the monthly instalments she needed to pay.",
        3, "Hire Purchase — Instalments", 14, (13, 0.52, 0.92),
        r"""Interest $= 5\% \times 1800 \times 2 = \$180$
Monthly instalment $= (1800 + 180) / 24 = \$82.50$""",
        "M1 for interest, M1 for total, A1",
        topic_id=8)

    # P2 Q2 — Page 15 (idx 14)
    add_q(db, p2.id, exam_dir, 2, 2, "a",
        r"Find shaded area of the cross-section.",
        2, "Area — Composite (Annulus)", 15, (14, 0.04, 0.48),
        r"""Area of big circle $= \pi(17.5)^2 = 306.25\pi$ mm$^2$
Area of small circle $= \pi(12.5)^2 = 156.25\pi$ mm$^2$
Shaded area $= 150\pi \approx 471$ mm$^2$ (3 s.f.)""",
        "M1 for each area, A1",
        stem=r"Tuck Lee Ice was established in Singapore in 1935. They make food grade ice tube in the form of hollow cylindrical shape. Outer diameter $= 35$ mm, inner diameter $= 25$ mm, length $= 40$ mm.",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 2, "b",
        r"Find volume of the ice tube.",
        2, "Volume — Hollow Cylinder", 15, (14, 0.48, 0.68),
        r"Volume $= 471.23\ldots \times 40 \approx 18\,800$ mm$^3$ (3 s.f.)", "M1, A1",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 2, "c",
        r"Given that a packet of ice tubes weighs 1kg and the density of ice is 1 g/cm$^3$, find the number of ice tubes that can be contained in a packet. [density $= \frac{\text{mass}}{\text{volume}}$]",
        3, "Volume — Application", 15, (14, 0.68, 0.92),
        r"""$18\,849.6 \text{ mm}^3 = 18.8496 \text{ cm}^3$
Mass of 1 tube $= 18.8496$ g
Number $= 1000 / 18.8496 \approx 53.05 \approx 53$""",
        "M1 for conversion, M1 for calculation, A1",
        topic_id=13)

    # P2 Q3 — Page 16 (idx 15)
    add_q(db, p2.id, exam_dir, 2, 3, "a",
        r"How many sides does this polygon have?",
        2, "Polygon — Sides", 16, (15, 0.04, 0.44),
        r"""Ext. angle $= 180° - 156° = 24°$
$n = 360° / 24° = 15$""",
        "M1, A1",
        stem=r"The diagram shows part of a regular polygon. Interior angle $= 156°$.",
        topic_id=11)

    add_q(db, p2.id, exam_dir, 2, 3, "b",
        r"Given that $O$ is the centre of the polygon, find the value of $\angle AOC$.",
        2, "Polygon — Central Angle", 16, (15, 0.44, 0.66),
        r"$\angle AOC = \frac{360°}{15} \times 2 = 48°$", "M1, A1",
        topic_id=11)

    add_q(db, p2.id, exam_dir, 2, 3, "c",
        r"If $AC = 8$ cm and $OB = 12.5$ cm, find the area of the above polygon.",
        2, "Polygon — Area", 16, (15, 0.66, 0.88),
        r"""Area of triangle $= \frac{1}{2} \times 8 \times 12.5 = 50$ cm$^2$
Area of polygon $= 50 \times 15 = 750$ cm$^2$""",
        "M1, A1",
        topic_id=11)

    # P2 Q4 — Page 17 (idx 16)
    add_q(db, p2.id, exam_dir, 2, 4, "a",
        r"the distance between Town A and Town M, leaving your answer in km.",
        2, "Speed, Distance, Time", 17, (16, 0.04, 0.36),
        r"""Distance $= 16 \times 30 \times 60 = 28\,800$ m $= 28.8$ km""",
        "M1, A1",
        stem=r"Towns A and B are 60 km apart. Town M is between Town A and B. Chandra drove from Town A to Town M at an average speed of 16 m/s in 30 minutes and then from Town M to Town B at an average speed of 25 m/s.",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 4, "b",
        r"the average speed of Chandra's car for the entire journey from Town A to Town B.",
        3, "Average Speed", 17, (16, 0.36, 0.58),
        r"""Distance M to B $= 60 - 28.8 = 31.2$ km $= 31\,200$ m
Time M to B $= 31\,200 / 25 = 1248$ s $= 20.8$ min
Total time $= 30 + 20.8 = 50.8$ min $= 127/150$ h
Average speed $= 60 / (50.8/60) \approx 70.9$ km/h (3 s.f.)""",
        "M1 for time, M1 for working, A1",
        topic_id=9)

    # P2 Q5 — Page 17 (idx 16)
    add_q(db, p2.id, exam_dir, 2, 5, "ai",
        r"Rovaniemi",
        1, "Time Zones", 17, (16, 0.58, 0.76),
        r"$6 - 5 = 1$ a.m.", "A1",
        stem=r"Countries in the world follow different time zones. The local time in Rovaniemi is $-5$ hours relative to the local time in Singapore. The local time in Christchurch is $+4$ hours relative to the local time in Singapore. When the time in Singapore is 6 am, find the local time in:",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 5, "aii",
        r"Christchurch",
        1, "Time Zones", 17, (16, 0.76, 0.84),
        r"$6 + 4 = 10$ a.m.", "A1",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 5, "b",
        r"When the local time in Rovaniemi on 2 September is 10 pm, what is the time and date in Singapore?",
        1, "Time Zones", 17, (16, 0.84, 0.96),
        r"$10 + 5 = 3$ a.m., 3 September", "A1",
        topic_id=9)

    # P2 Q6 — Page 18 (idx 17)
    add_q(db, p2.id, exam_dir, 2, 6, "a",
        r"What would be the largest possible area he could have?",
        1, "Area — Rectangle / Perimeter", 18, (17, 0.04, 0.30),
        r"$13 \times 13 = 169$ m$^2$ or $12 \times 14 = 168$ m$^2$", "A1",
        stem=r"Mr Singh used a tape of 52 m to cordon off a rectangular plot of land to plant vegetables. (Dimensions are integers.)",
        topic_id=12)

    add_q(db, p2.id, exam_dir, 2, 6, "b",
        r"State the dimensions of this largest possible area.",
        1, "Area — Dimensions", 18, (17, 0.30, 0.50),
        r"$14$ m $\times$ $12$ m, or $13$ m $\times$ $13$ m", "A1",
        topic_id=12)

    add_q(db, p2.id, exam_dir, 2, 6, "c",
        r"Mrs Tan bought more tapes and the shape of the plot of land was later altered from a rectangle to a circle. With the area of the plot remaining the same, find the radius of the circle?",
        2, "Area — Circle", 18, (17, 0.50, 0.90),
        r"""Radius $= \sqrt{\frac{169}{\pi}} \approx 7.33$ m (3 s.f.)""",
        "M1, A1",
        topic_id=13)

    # P2 Q7 — Page 19 (idx 18)
    add_q(db, p2.id, exam_dir, 2, 7, "a",
        r"Use the information from the bar chart to find the value of $p$ and $q$ in the table below.",
        2, "Statistics — Bar Chart", 19, (18, 0.04, 0.58),
        r"$p = 12$, $q = 1$", "A1, A1",
        stem=r"The following table and bar graph show the number of students who owned at least one laptop at home. Classes: 1C1 ($8$), 1C2 ($15$), 1C3 ($7$), 1C4 ($p$), 1C5 ($q$).",
        topic_id=14)

    add_q(db, p2.id, exam_dir, 2, 7, "b",
        r"Find the total number of students who had at least one laptop at home.",
        1, "Statistics — Total", 19, (18, 0.58, 0.72),
        r"Total $= 8 + 15 + 7 + 12 + 1 = 43$", "A1",
        topic_id=14)

    add_q(db, p2.id, exam_dir, 2, 7, "c",
        r"If the number of students in Class 1C1 was increased to 10, find the percentage increase in the total number of students.",
        2, "Percentage Increase", 19, (18, 0.72, 0.92),
        r"""New total $= 45$. Increase $= 2$.
Percentage increase $= \frac{2}{43} \times 100\% \approx 4.65\%$ (3 s.f.)""",
        "M1, A1",
        topic_id=14)

    # P2 Q8 — Page 20 (idx 19)
    add_q(db, p2.id, exam_dir, 2, 8, "a",
        r"Write down the 7th term of the pattern.",
        1, "Number Patterns", 20, (19, 0.04, 0.22),
        r"$T_7 = 28$", "A1",
        stem=r"The first four terms of a number sequence are $-8, -2, 4, 10$.",
        topic_id=7)

    add_q(db, p2.id, exam_dir, 2, 8, "b",
        r"Find an expression for the nth term of the sequence.",
        1, "Number Patterns — General Term", 20, (19, 0.22, 0.36),
        r"$T_n = 6n - 14$", "A1",
        topic_id=7)

    add_q(db, p2.id, exam_dir, 2, 8, "c",
        r"Find the term in the sequence when the number is 118.",
        1, "Number Patterns", 20, (19, 0.36, 0.50),
        r"$6n - 14 = 118 \implies 6n = 132 \implies n = 22$", "A1",
        topic_id=7)

    add_q(db, p2.id, exam_dir, 2, 8, "d",
        r"Will there be a number pattern where the number is 89? Explain your answer.",
        2, "Number Patterns — Reasoning", 20, (19, 0.50, 0.90),
        r"""$6n - 14 = 89 \implies 6n = 103 \implies n = 17.2$
Since $n$ is not a whole number, there will not be a number pattern where the number is 89.
OR: Since $6n - 14 = 2(3n - 7)$, the numbers in the sequence will always be even. 89 is an odd number so there will not be a term equal to 89.""",
        "M1 for working, A1",
        topic_id=7)

    # P2 Q9 — Pages 21-22 (idx 20-21)
    add_q(db, p2.id, exam_dir, 2, 9, "a",
        r"Given that $y = -2x - 4$, find the values of $p$ and $q$ in the following table.",
        2, "Linear Functions — Table", 21, (20, 0.04, 0.22),
        r"$p = 8$, $q = -12$", "A1, A1",
        stem=r"Table: $x = -6, -4, 0, 2, 4$ and $y = p, 4, -4, -8, q$.",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 9, "b",
        r"Using a scale of 2 cm to represent 1 unit on the $x$-axis and 1 cm to represent 1 unit on the $y$-axis, draw the graph of $y = -2x - 4$ for values of $x$ from $-6$ to $4$.",
        3, "Linear Functions — Graph", 21, (20, 0.22, 0.44),
        r"Straight line through $(-6, 8)$, $(-4, 4)$, $(0, -4)$, $(2, -8)$, $(4, -12)$.", "B1 for correct points, B1 for line, B1 for correct scale/labels",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 9, "c",
        r"Using your graph, find the value of $y$ when $x = -1.5$.",
        1, "Linear Functions — Reading Graph", 21, (20, 0.44, 0.56),
        r"$y = -1$", "A1",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 9, "d",
        r"Find the gradient of the graph.",
        1, "Linear Functions — Gradient", 21, (20, 0.56, 0.68),
        r"Gradient $= -2$", "A1",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 9, "e",
        r"A line parallel to the graph $y = -2x - 4$, cuts the $y$-axis at $y = 3$. Write down the equation to this parallel line.",
        1, "Linear Functions — Parallel", 21, (20, 0.68, 0.86),
        r"$y = -2x + 3$", "A1",
        topic_id=6)

    db.commit()
    p1_count = len(p1.questions)
    p2_count = len(p2.questions)
    print(f"Seeded Bendemeer 2022 exam id={exam.id}: Paper 1 ({p1_count} parts), Paper 2 ({p2_count} parts)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
