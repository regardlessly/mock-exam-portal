"""Seed Canberra Secondary School EOY 2022 Sec 1 Express Math exam."""

import os
import shutil
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/66b1f55d7d973_5779.pdf"
IMAGES_DIR = "/tmp/canberra_pages"

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

    school = db.query(School).filter(School.name == "Canberra Secondary School").first()
    if not school:
        school = School(name="Canberra Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(Exam.school_id == school.id, Exam.year == 2022).first()
    if existing:
        print(f"Canberra 2022 already seeded (id={existing.id}). Deleting and re-seeding.")
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
        source_pdf="66b1f55d7d973_5779.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # PAPER 1 — Pages 3-12 (idx 2-11), 50 marks, 1 hour 15 min
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=75, total_marks=50,
               date=date(2022, 10, 7), instructions="Answer all questions.")
    db.add(p1); db.flush()

    # Q1 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 1, "a",
        r"Express $540$ as a product of its prime factors, giving your answer in index notation.",
        1, "Prime Factorisation", 3, (2, 0.07, 0.22),
        r"$540 = 2^2 \times 3^3 \times 5$", "B1",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 1, "b",
        r"Hence find the smallest integer $m$ such that $540m$ is a perfect cube.",
        1, "Perfect Cube", 3, (2, 0.22, 0.40),
        r"$m = 50$", "B1",
        topic_id=1)

    # Q2 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 2, "a",
        r"Factorise the following expressions: $2bc - 4b^2 + 2b$.",
        1, "Algebra — Factorisation", 3, (2, 0.40, 0.58),
        r"$2b(c - 2b + 1)$", "B1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 2, "b",
        r"Factorise $n(m + 3) - 6(m + 3)$.",
        1, "Algebra — Factorisation", 3, (2, 0.58, 0.78),
        r"$(m + 3)(n - 6)$", "B1",
        topic_id=4)

    # Q3 — Page 4 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 3, "ai",
        r"Round off $1.952$ correct to 2 significant figures.",
        1, "Approximation", 4, (3, 0.07, 0.22),
        r"$2.0$", "B1",
        stem=r"Round off the following numbers correct to 2 significant figures.",
        topic_id=3)

    add_q(db, p1.id, exam_dir, 1, 3, "aii",
        r"Round off $3.015$ correct to 2 significant figures.",
        1, "Approximation", 4, (3, 0.22, 0.37),
        r"$3.0$", "B1",
        topic_id=3)

    add_q(db, p1.id, exam_dir, 1, 3, "b",
        r"Hence, estimate the value of $\dfrac{1.952 + 3.015}{0.126}$.",
        2, "Estimation", 4, (3, 0.37, 0.65),
        r"$$\frac{2.0 + 3.0}{\sqrt[3]{0.125}} = \frac{5.0}{0.5} = 10$$", "M1, A1",
        topic_id=3)

    # Q4 — Page 5 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 4, "a",
        r"Simplify $\dfrac{1}{2}a + \dfrac{1}{2}b - \dfrac{1}{4}a + \dfrac{1}{4}b$.",
        2, "Algebra — Simplification", 5, (4, 0.07, 0.42),
        r"$$\frac{1}{2}a - \frac{1}{4}a + \frac{1}{2}b + \frac{1}{4}b = \frac{1}{4}a + \frac{3}{4}b$$", "M1, A1",
        stem=r"Simplify the following expressions.",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 4, "b",
        r"Simplify $2(3p - 5q) - (2p - 4q)$.",
        2, "Algebra — Expansion", 5, (4, 0.42, 0.78),
        r"$$6p - 10q - 2p + 4q = 4p - 6q$$", "M1, A1",
        topic_id=4)

    # Q5 — Page 6 (idx 5)
    add_q(db, p1.id, exam_dir, 1, 5, "a",
        r"Liquid $A$ was heated so that its temperature rose by $23°\\text{C}$. Write down its new temperature.",
        1, "Integers — Temperature", 6, (5, 0.07, 0.24),
        r"$-5 + 23 = 18°\\text{C}$", "B1",
        stem=r"The temperature of both liquid $A$ and liquid $B$ in a Science Laboratory were at $-5°\\text{C}$.",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 5, "b",
        r"Liquid $B$ was cooled so that its temperature fell by $8°\\text{C}$. Write down its new temperature.",
        1, "Integers — Temperature", 6, (5, 0.24, 0.40),
        r"$-5 - 8 = -13°\\text{C}$", "B1",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 5, "c",
        r"Find the average of the final temperatures of the two liquids.",
        2, "Integers — Average", 6, (5, 0.40, 0.58),
        r"$$\\frac{18 + (-13)}{2} = \\frac{5}{2} = 2.5°\\text{C}$$", "M1, A1",
        topic_id=2)

    # Q6 — Page 6 (idx 5)
    add_q(db, p1.id, exam_dir, 1, 6, "a",
        r"Solve the equation $4x + 8 = 2x - 20$.",
        2, "Linear Equations", 6, (5, 0.58, 0.73),
        r"$$4x - 2x = -20 - 8$$ $$2x = -28$$ $$x = -14$$", "M1, A1",
        topic_id=5)

    add_q(db, p1.id, exam_dir, 1, 6, "b",
        r"Evaluate $-3(5 - 2) + \left[2 - (3 \times 5)\right]$, showing your working clearly.",
        3, "Order of Operations", 6, (5, 0.73, 0.93),
        r"$$-3(3) + [2 - 15]$$ $$= -9 + [-13]$$ $$= -22$$", "M1, M1, A1",
        topic_id=2)

    # Q7 — Page 7 (idx 6)
    add_q(db, p1.id, exam_dir, 1, 7, "a",
        r"If there are $x$ red pens, write down in terms of $x$, the number of blue pens.",
        1, "Algebra — Expression", 7, (6, 0.07, 0.22),
        r"$30 - x$", "B1",
        stem=r"John bought 30 red and blue pens.",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 7, "bi",
        r"Write down an expression in $x$ for the cost of the red pens.",
        1, "Algebra — Expression", 7, (6, 0.22, 0.42),
        r"$\\$0.5x$", "B1",
        stem=r"The red pens are sold at 50c each and the blue pens are sold at 40c each. The total bill for the pens was $\\$13.00$.",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 7, "bii",
        r"Write down an expression in $x$ for the cost of the blue pens.",
        1, "Algebra — Expression", 7, (6, 0.42, 0.58),
        r"$0.4(30 - x)$", "B1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 7, "c",
        r"Form an equation in $x$ and solve it to find the number of blue pens.",
        3, "Linear Equations — Word Problem", 7, (6, 0.58, 0.82),
        r"$$0.5x + 0.4(30 - x) = 13$$ $$0.5x + 12 - 0.4x = 13$$ $$0.1x = 1$$ $$x = 10$$ Blue pens $= 30 - 10 = 20$", "M1, M1, A1",
        topic_id=5)

    # Q8 — Page 8 (idx 7)
    add_q(db, p1.id, exam_dir, 1, 8, "a",
        r"Find the value of $y$.",
        2, "Angle Properties — Isosceles Triangle", 8, (7, 0.07, 0.47),
        r"$$180 - 2(60) = 60°$$ $$y = 180 - 60 = 120°$$ (angles on straight line, or: $\\angle BDC = 180 - 105 - 60 = 15°$, etc.)", "M1, A1",
        stem=r"Triangle $BCD$ is an isosceles triangle and $AB$ is parallel to $DC$. Given that $\\angle BCD = 60°$, $\\angle AED = 105°$ and $\\angle EAB$ is a right angle. Find the values of:",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 8, "b",
        r"Find the value of $x$.",
        2, "Angle Properties — Parallel Lines", 8, (7, 0.47, 0.70),
        r"$$360 - 90 - 105 - 60 = 105°$$ (angles in quadrilateral)", "M1, A1",
        topic_id=10)

    # Q9 — Page 9 (idx 8)
    add_q(db, p1.id, exam_dir, 1, 9, "a",
        r"Find $\\angle RST$, stating your reasons clearly.",
        2, "Angle Properties — Parallel Lines", 9, (8, 0.07, 0.42),
        r"$$\\angle RST = 67 + 23 = 90°$$ (alt. angles, $AB \\parallel CD$)", "M1, A1",
        stem=r"In the diagram, $AB$ is parallel to $CD$ and $PR$ is parallel to $ST$. Given that $\\angle PQR = 66°$, $\\angle DRS = 23°$ and $\\angle PTS = 113°$.",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 9, "b",
        r"Find $\\angle PRS$.",
        1, "Angle Properties — Parallel Lines", 9, (8, 0.42, 0.57),
        r"$\\angle PRS = 90°$ (int. angles, $PR \\parallel ST$)", "B1",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 9, "c",
        r"Find $\\angle QPR$.",
        2, "Angle Properties — Triangle", 9, (8, 0.57, 0.78),
        r"$$\\angle QRP = 180 - 90 - 23 = 67°$$ $$\\angle QPR = 180 - 66 - 67 = 47°$$ (sum of angles in $\\triangle$)", "M1, A1",
        topic_id=10)

    # Q10 — Page 10 (idx 9)
    add_q(db, p1.id, exam_dir, 1, 10, "a",
        r"Write down the next term in the sequence.",
        1, "Number Patterns", 10, (9, 0.07, 0.22),
        r"$8$", "B1",
        stem=r"The first four terms of a sequence are $-4, -1, 2, 5, \\ldots$",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 10, "b",
        r"Write down an expression for the $n$th term.",
        2, "Number Patterns — General Term", 10, (9, 0.22, 0.42),
        r"$T_n = 3n - 7$", "B1 (for $3n$), B1 (for $-7$)",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 10, "c",
        r"Hence, find the $25$th term in the sequence.",
        1, "Number Patterns", 10, (9, 0.42, 0.57),
        r"$T_{25} = 3(25) - 7 = 68$", "B1",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 10, "d",
        r"Explain why $255$ is not a term of the sequence.",
        2, "Number Patterns — Reasoning", 10, (9, 0.57, 0.80),
        r"$$3n - 7 = 255$$ $$3n = 262$$ $$n = 87.\\overline{3}$$ Since $n$ is not a positive integer, $255$ is not a term.", "M1, A1",
        topic_id=7)

    # Q11 — Pages 11-12 (idx 10-11)
    add_q(db, p1.id, exam_dir, 1, 11, "a",
        r"The perimeter of this trapezium is given by the expression $(20x - 3)$ cm. Show that the length of $EC$ is $(8x - 9)$ cm.",
        2, "Algebra — Perimeter", 11, (10, 0.07, 0.65),
        r"$$(20x - 3) - (3x + 3) - (5x - 3) - 4x = EC$$ $$EC = 20x - 3 - 3x - 3 - 5x + 3 - 4x = 8x - 9$$ (SHOWN)", "M1, A1",
        stem=r"The composite figure below shows a trapezium $ABCE$ and a semicircle $CDE$. Expressions for the lengths of three sides of a trapezium are shown on the diagram. All lengths are given in centimetres. $AB = 5x - 3$, $AE = 3x + 3$, $BC = 4x$.",
        topic_id=12)

    add_q(db, p1.id, exam_dir, 1, 11, "b",
        r"Given that $AE = BC$, find the value of $x$ and hence, calculate the perimeter of the trapezium.",
        2, "Linear Equations — Perimeter", 11, (10, 0.65, 0.90),
        r"$$3x + 3 = 4x$$ $$x = 3$$ Perimeter $= 20(3) - 3 = 57$ cm", "M1, A1",
        topic_id=12)

    add_q(db, p1.id, exam_dir, 1, 11, "ci",
        r"Given that the area of the trapezium is $264$ cm$^2$, find the height, $h$, of the trapezium.",
        2, "Area — Trapezium", 12, (11, 0.07, 0.40),
        r"$$\\frac{1}{2}(15 + 18)h = 264$$ $$\\frac{33h}{2} = 264$$ $$h = 16$$ cm", "M1, A1",
        topic_id=12)

    add_q(db, p1.id, exam_dir, 1, 11, "cii",
        r"Find the area of the composite figure.",
        2, "Area — Composite (Trapezium + Semicircle)", 12, (11, 0.40, 0.75),
        r"$$\\text{Radius} = \\frac{15}{2} = 7.5$$ $$\\text{Area} = 264 + \\frac{1}{2}\\pi\\left(\\frac{15}{2}\\right)^2 = 264 + \\frac{225\\pi}{8} \\approx 264 + 88.36 = 352$$ cm$^2$", "M1, A1",
        topic_id=12)

    # ══════════════════════════════════════════════
    # PAPER 2 — Pages 14-24 (idx 13-23), 50 marks, 1 hour 15 min
    # ══════════════════════════════════════════════
    p2 = Paper(exam_id=exam.id, paper_number=2, duration_minutes=75, total_marks=50,
               date=date(2022, 10, 12), instructions="Answer all questions.")
    db.add(p2); db.flush()

    # P2 Q1 — Page 14 (idx 13)
    add_q(db, p2.id, exam_dir, 2, 1, "a",
        r"Express $58.6\%$ as a decimal.",
        1, "Percentage to Decimal", 14, (13, 0.07, 0.18),
        r"$\\frac{58.6}{100} = 0.586$", "A1",
        topic_id=8)

    add_q(db, p2.id, exam_dir, 2, 1, "b",
        r"Express 55 seconds as a percentage of 4 minutes.",
        1, "Percentage", 14, (13, 0.18, 0.32),
        r"$\\frac{55}{240} \\times 100\\% = 22.9\\%$", "A1",
        topic_id=8)

    # P2 Q2 — Page 14 (idx 13)
    add_q(db, p2.id, exam_dir, 2, 2, "a",
        r"Calculate the cost per 100 g of peaches in a small tin.",
        1, "Rate — Unit Price", 14, (13, 0.32, 0.62),
        r"$\\frac{\\$2.65}{420} \\times 100 = \\$0.63$ / 100g", "A1",
        stem=r"Peaches are sold in either small or large tins. Small: 420g, $\\$2.65$. Large: 825g, $\\$4.20$.",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 2, "b",
        r"State which tin gives you a better value. Explain.",
        1, "Rate — Comparison", 14, (13, 0.62, 0.82),
        r"Large tin: $\\frac{\\$4.20}{825} \\times 100 = \\$0.51$ / 100g. The large tin is a better deal as the cost per 100g is cheaper.", "A1",
        topic_id=9)

    # P2 Q3 — Page 15 (idx 14)
    add_q(db, p2.id, exam_dir, 2, 3, "a",
        r"Find the HCF of $2^4 \\times 3 \\times 5^3$ and $2^6 \\times 3^3 \\times 5 \\times 7$.",
        1, "HCF", 15, (14, 0.07, 0.18),
        r"$\\text{HCF} = 2^4 \\times 3 \\times 5 = 240$", "A1",
        topic_id=1)

    add_q(db, p2.id, exam_dir, 2, 3, "b",
        r"If $A : B = 3 : 4$ and $B : C = 3 : 5$, find the ratio $A : B : C$.",
        2, "Ratio", 15, (14, 0.18, 0.38),
        r"$$A : B = 3 : 4 = 9 : 12$$ $$B : C = 3 : 5 = 12 : 20$$ $$A : B : C = 9 : 12 : 20$$", "A1, A1",
        topic_id=9)

    # P2 Q4 — Page 15 (idx 14)
    add_q(db, p2.id, exam_dir, 2, 4, None,
        r"Three shuttle bus services leave from a terminal station. For a complete loop, the first service takes 15 minutes, the second takes 21 minutes and the third takes 25 minutes. All three services leave the terminal station together at 0800. Find the time when the three services next leave the terminal station together.",
        3, "LCM — Word Problem", 15, (14, 0.38, 0.70),
        r"$$15 = 3 \\times 5$$ $$21 = 3 \\times 7$$ $$25 = 5^2$$ $$\\text{LCM} = 3 \\times 5^2 \\times 7 = 525 \\text{ min} = 8 \\text{ h } 45 \\text{ min}$$ Required Time $= 4{:}45$ p.m.", "M1, M1, A1",
        topic_id=1)

    # P2 Q5 — Page 15 (idx 14)
    add_q(db, p2.id, exam_dir, 2, 5, None,
        r"A polygon has $n$ sides. Three of its exterior angles are $21°$, $43°$ and $56°$. The other $(n - 3)$ exterior angles are $12°$ each. Find the value of $n$.",
        3, "Polygon — Exterior Angles", 15, (14, 0.70, 0.93),
        r"$$\\text{Remaining angles} = 360° - 21° - 43° - 56° = 240°$$ $$(n - 3) \\times 12 = 240$$ $$n - 3 = 20$$ $$n = 23$$", "M1, M1, A1",
        topic_id=11)

    # P2 Q6 — Page 16 (idx 15)
    add_q(db, p2.id, exam_dir, 2, 6, "a",
        r"Find the time taken for the journey from $A$ to $C$, in hours.",
        1, "Speed, Distance, Time", 16, (15, 0.07, 0.22),
        r"$2 \\text{ h } 12 \\text{ min} + 15 \\text{ min} + 1 \\text{ h} = 3.45 \\text{ h} = 3$ h $27$ min", "A1",
        stem=r"A train started a journey from $A$ and travelled for 2 hours 12 minutes to $B$. It stopped for 15 minutes and then continued its journey to $C$ for another 1 hour. The distance between $A$ and $C$ is 280 km.",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 6, "b",
        r"Find the average speed of the whole journey in km/h.",
        1, "Average Speed", 16, (15, 0.22, 0.37),
        r"$$\\text{Average speed} = \\frac{280}{3.45} = 81.2 \\text{ km/h}$$", "A1",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 6, "ci",
        r"Convert 110 km/h to m/s.",
        1, "Speed Conversion", 16, (15, 0.37, 0.57),
        r"$$110 \\times \\frac{1000}{3600} = 30.6 \\text{ m/s}$$", "A1",
        stem=r"After resting at $C$ for 15 minutes, the train continued its journey to $D$, at an average speed of 110 km/h for 50 minutes.",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 6, "cii",
        r"Find the distance between $C$ and $D$, in km.",
        1, "Speed, Distance, Time", 16, (15, 0.57, 0.75),
        r"$$\\text{Distance} = 110 \\times \\frac{50}{60} = 91.7 \\text{ km}$$", "A1",
        topic_id=9)

    # P2 Q7 — Page 17 (idx 16)
    add_q(db, p2.id, exam_dir, 2, 7, "a",
        r"Calculate the amount she paid for the Cotton cloth.",
        1, "Ratio — Amount", 17, (16, 0.07, 0.32),
        r"$$\\frac{6}{25} \\times \\$800 = \\$192$$", "A1",
        stem=r"During a warehouse sale, cloths are being sold at a flat rate regardless of the type. A tailor bought 100 m$^2$ of Cotton, Dry-fit and Stretchy cloth in the ratio of $6 : 15 : 4$ respectively. She paid a total sum of $\\$800$ for the cloths. The tailor proceeded to create shirts using the cloth purchased. Each shirt requires 0.5 m$^2$ of cloth.",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 7, "b",
        r"Calculate the amount of Cotton cloth bought, in m$^2$.",
        1, "Ratio — Quantity", 17, (16, 0.32, 0.52),
        r"$$\\frac{6}{25} \\times 100 = 24 \\text{ m}^2$$", "A1",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 7, "c",
        r"Calculate the selling price for each Cotton shirt, given that the tailor intends to make a profit of 30% on all the Cotton shirts.",
        2, "Percentage — Profit", 17, (16, 0.52, 0.82),
        r"$$\\text{Number of Cotton shirts} = \\frac{24}{0.5} = 48$$ $$\\text{Selling price per shirt} = \\frac{192 \\times 1.3}{48} = \\$5.20$$", "M1, A1",
        topic_id=8)

    # P2 Q8 — Page 18 (idx 17)
    add_q(db, p2.id, exam_dir, 2, 8, "a",
        r"Find the fraction of cars that were white.",
        1, "Statistics — Pie Chart", 18, (17, 0.07, 0.32),
        r"$$\\frac{140}{360} = \\frac{7}{18}$$", "A1",
        stem=r"Nicolette recorded the colour of cars travelling through Sun Plaza taxi stand one day. Her results are shown on a pie chart. Blue: $133°$, White: $140°$.",
        topic_id=14)

    add_q(db, p2.id, exam_dir, 2, 8, "b",
        r"Calculate the percentage of cars that were blue.",
        1, "Statistics — Pie Chart", 18, (17, 0.32, 0.47),
        r"$$\\frac{133}{360} \\times 100\\% = 36.9\\%$$", "A1",
        topic_id=14)

    add_q(db, p2.id, exam_dir, 2, 8, "c",
        r"There were twice as many black cars as red cars. Find the angle representing red cars.",
        1, "Statistics — Pie Chart", 18, (17, 0.47, 0.65),
        r"$$\\text{Red + Black} = 360 - 140 - 133 = 87°$$ $$\\text{Black} = 2 \\times \\text{Red}$$ $$3 \\times \\text{Red} = 87°$$ $$\\text{Red} = 29°$$", "A1",
        topic_id=14)

    add_q(db, p2.id, exam_dir, 2, 8, "d",
        r"Given that there were 145 red cars, find the total number of cars in the survey.",
        1, "Statistics — Pie Chart", 18, (17, 0.65, 0.82),
        r"$$\\frac{29}{360} \\times \\text{Total} = 145$$ $$\\text{Total} = \\frac{145 \\times 360}{29} = 1800$$", "A1",
        topic_id=14)

    # P2 Q9 — Page 19 (idx 18)
    add_q(db, p2.id, exam_dir, 2, 9, "a",
        r"Construct the triangle $ABC$. Line $AB$ has already been drawn in the answer space provided.",
        1, "Construction", 19, (18, 0.07, 0.45),
        r"Triangle $ABC$ constructed with $AB = 9$ cm, $BC = 7$ cm, $AC = 6$ cm.", "A1",
        stem=r"In triangle $ABC$, $AB = 9$ cm, $BC = 7$ cm and $AC = 6$ cm.",
        topic_id=10)

    add_q(db, p2.id, exam_dir, 2, 9, "b",
        r"Find the value of $\\angle ABC$.",
        1, "Construction — Measurement", 19, (18, 0.45, 0.60),
        r"$\\angle ABC = 42° \\pm 1°$", "A1",
        topic_id=10)

    add_q(db, p2.id, exam_dir, 2, 9, "c",
        r"Using a compass, construct the perpendicular bisector of $AB$.",
        1, "Construction — Perpendicular Bisector", 19, (18, 0.60, 0.70),
        r"Perpendicular bisector of $AB$ drawn with arcs shown.", "A1",
        topic_id=10)

    add_q(db, p2.id, exam_dir, 2, 9, "d",
        r"Construct the angle bisector of $\\angle BAC$.",
        1, "Construction — Angle Bisector", 19, (18, 0.70, 0.80),
        r"Angle bisector of $\\angle BAC$ drawn with arcs shown.", "A1",
        topic_id=10)

    add_q(db, p2.id, exam_dir, 2, 9, "e",
        r"The perpendicular bisector of $AB$ intersects the angle bisector of $\\angle BAC$ at point $P$. Measure and write down the value of $PA$.",
        1, "Construction — Measurement", 19, (18, 0.80, 0.93),
        r"$PA = 5$ cm $\\pm 0.1$ cm", "A1",
        topic_id=10)

    # P2 Q10 — Pages 20-21 (idx 19-20)
    add_q(db, p2.id, exam_dir, 2, 10, "a",
        r"Calculate the value of $m$.",
        1, "Linear Functions — Table", 20, (19, 0.07, 0.22),
        r"$m = 4(2) + 8 = 16$", "B1",
        stem=r"The following table shows some corresponding values of $x$ and $y$ for the equation $y = 4x + 8$.",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 10, "b",
        r"Using a scale of 2 cm to 1 unit for the $x$-axis and 1 cm to 2 units for the $y$-axis, plot the graph of $y = 4x + 8$ for $-4 \\leq x \\leq 2$.",
        2, "Linear Functions — Graph", 20, (19, 0.22, 0.93),
        r"Straight line through $(-4, -8)$, $(-2, 0)$, $(0, 8)$, $(2, 16)$.", "B1 for points, B1 for line",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 10, "ci",
        r"From the graph, find the value of $x$ when $y = 2$.",
        1, "Linear Functions — Reading Graph", 21, (20, 0.07, 0.20),
        r"$x = -1.5$", "A1",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 10, "cii",
        r"From the graph, find the value of $y$ when $x = -1$.",
        1, "Linear Functions — Reading Graph", 21, (20, 0.20, 0.37),
        r"$y = 4$", "A1",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 10, "d",
        r"On the same axes in (b), draw the line of $y = 6$.",
        1, "Linear Functions — Horizontal Line", 21, (20, 0.37, 0.50),
        r"Horizontal line $y = 6$ drawn.", "B1",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 10, "e",
        r"Hence, write down the coordinates of the point of intersection where the line $y = 4x + 8$ meets the line $y = 6$.",
        1, "Linear Functions — Intersection", 21, (20, 0.50, 0.70),
        r"$(-0.5, 6)$", "A1",
        topic_id=6)

    # P2 Q11 — Page 22 (idx 21)
    add_q(db, p2.id, exam_dir, 2, 11, "a",
        r"Calculate the area of triangle $PQR$.",
        1, "Area — Triangle", 22, (21, 0.07, 0.42),
        r"$$\\frac{1}{2}(8)(6.93) = 27.72 \\text{ cm}^2$$", "A1",
        stem=r"The diagram shows a solid hexagonal prism. The cross-section of the prism is a regular hexagon made up of six equilateral triangles, with sides of length 8 cm and height 6.93 cm. The length of the prism is 40 cm.",
        topic_id=12)

    add_q(db, p2.id, exam_dir, 2, 11, "b",
        r"Calculate the volume of the prism.",
        2, "Volume — Prism", 22, (21, 0.42, 0.62),
        r"$$\\text{Area of hexagon} = 6 \\times 27.72 = 166.32 \\text{ cm}^2$$ $$\\text{Volume} = 166.32 \\times 40 = 6652.8 \\text{ cm}^3$$", "M1, A1",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 11, "c",
        r"Calculate the total surface area of the prism.",
        2, "Surface Area — Prism", 22, (21, 0.62, 0.85),
        r"$$\\text{Curved surface area} = (8 \\times 6) \\times 40 = 1920 \\text{ cm}^2$$ $$\\text{Total SA} = 1920 + 2(166.32) = 2252.64 \\text{ cm}^2$$", "M1, A1",
        topic_id=13)

    # P2 Q12 — Page 23 (idx 22)
    add_q(db, p2.id, exam_dir, 2, 12, "a",
        r"Solve the equation $\\dfrac{x - 7}{4} = 9$.",
        2, "Linear Equations", 23, (22, 0.07, 0.30),
        r"$$x - 7 = 36$$ $$x = 43$$", "M1, A1",
        stem=r"Solve the following equations.",
        topic_id=5)

    add_q(db, p2.id, exam_dir, 2, 12, "b",
        r"Solve the equation $\\dfrac{y}{2} - \\dfrac{3y + 1}{4} = 5$.",
        3, "Linear Equations — Fractions", 23, (22, 0.30, 0.58),
        r"$$\\frac{2y - (3y + 1)}{4} = 5$$ $$2y - 3y - 1 = 20$$ $$-y = 21$$ $$y = -21$$", "M1, M1, A1",
        topic_id=5)

    add_q(db, p2.id, exam_dir, 2, 12, "c",
        r"Solve the equation $6(z + 3) - 7(2z - 5) = 3(5z - 4) - 4$.",
        3, "Linear Equations — Expansion", 23, (22, 0.58, 0.82),
        r"$$6z + 18 - 14z + 35 = 15z - 12 - 4$$ $$-8z + 53 = 15z - 16$$ $$-23z = -69$$ $$z = 3$$", "M1, M1, A1",
        topic_id=5)

    db.commit()
    p1_count = len(p1.questions)
    p2_count = len(p2.questions)
    print(f"Seeded Canberra exam id={exam.id}: Paper 1 ({p1_count} parts), Paper 2 ({p2_count} parts)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
