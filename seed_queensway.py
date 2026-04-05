"""Seed Queensway Secondary School EOY 2022 Sec 1 Express Math exam."""

import os
import shutil
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/66b1f568282d1_5783.pdf"
IMAGES_DIR = "/tmp/queensway_pages"

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

    school = db.query(School).filter(School.name == "Queensway Secondary School").first()
    if not school:
        school = School(name="Queensway Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(Exam.school_id == school.id, Exam.year == 2022).first()
    if existing:
        print(f"Queensway 2022 already seeded (id={existing.id}). Deleting and re-seeding.")
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
        source_pdf="66b1f568282d1_5783.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # PAPER 1 — Pages 3-12 (idx 2-11), 40 marks, 1 hour
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=60, total_marks=40,
               date=date(2022, 10, 3), instructions="Answer all questions.")
    db.add(p1); db.flush()

    # Q1 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 1, "a",
        r"Express $324$ as a product of its prime factors.",
        1, "Prime Factorisation", 3, (2, 0.09, 0.25),
        r"$324 = 2^2 \times 3^4$", "B1",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 1, "b",
        r"Hence, explain why $324$ is a perfect square.",
        1, "Perfect Square", 3, (2, 0.24, 0.35),
        r"All the powers of its prime factors are even. OR $324 = (2 \times 3^2)^2$", "B1",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 1, "c",
        r"Find the smallest value of $k$ given that $\dfrac{324}{k}$ is a perfect cube.",
        1, "Perfect Cube", 3, (2, 0.34, 0.48),
        r"$k = 2^2 \times 3 = 12$", "B1",
        topic_id=1)

    # Q2 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 2, "a",
        r"List the rational number(s).",
        1, "Number Classification", 3, (2, 0.48, 0.63),
        r"$0.4$, $2$", "B1",
        stem=r"Some numbers are listed below: $\sqrt{5}$, $0.4$, $2$.",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 2, "b",
        r"Without using a calculator, evaluate $\dfrac{6}{2\frac{9}{7}} \div 0.8 \times (-1)^7$.",
        1, "Order of Operations", 3, (2, 0.62, 0.95),
        r"$$= \frac{6}{\frac{23}{7}} \div 0.8 \times (-1) = \frac{42}{23} \times \frac{-1}{0.8} = -\frac{42}{18.4} \approx -2.28$$", "M1, A1",
        topic_id=2)

    # Q3 — Page 4 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 3, "a",
        r"Write down the minimum and maximum number of Asian elephants that could be left in the wild.",
        2, "Rounding / Approximation", 4, (3, 0.07, 0.44),
        r"Minimum $= 29\,500$, Maximum $= 30\,499$", "B1, B1",
        stem=r"One of the top ten endangered species is the Asian elephant. It is estimated that there are $30\,000$ Asian elephants left in the wild, rounded off to 2 significant figures.",
        topic_id=3)

    add_q(db, p1.id, exam_dir, 1, 3, "b",
        r"Explain why the percentage of Asian elephants sums to 99%, instead of 100%.",
        1, "Percentage / Rounding", 4, (3, 0.44, 0.76),
        r"The percentages have been rounded to the nearest whole number, so the sum may not be exactly 100%.", "B1",
        topic_id=3)

    # Q4 — Page 5 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 4, "a",
        r"Expand and simplify $3c(2a - 2b) - 4bc(1 - c)$.",
        2, "Algebra — Expansion", 5, (4, 0.07, 0.31),
        r"$$6ac - 6bc - 4bc + 4bc^2 = 6ac - 10bc + 4bc^2$$", "M1, A1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 4, "b",
        r"Packing $x$ sweets into boxes of 6 requires three more boxes than packing $(x - 2)$ sweets into boxes of 8. Form an equation in terms of $x$ and find the value of $x$.",
        3, "Linear Equations — Word Problem", 5, (4, 0.30, 0.78),
        r"""$$\frac{x}{6} = \frac{x-2}{8} + 3$$
$$\frac{4x - 3(x-2)}{24} = 3$$
$$4x - 3x + 6 = 72$$
$$x = 66$$""",
        "M1 for equation, M1 for solving, A1",
        topic_id=5)

    # Q5 — Page 6 (idx 5)
    add_q(db, p1.id, exam_dir, 1, 5, "a",
        r"Plot the point $Q(4, 2)$.",
        1, "Coordinate Geometry", 6, (5, 0.07, 0.45),
        r"Point $Q(4, 2)$ plotted on grid.", "B1",
        stem=r"The figure shows the point $P(-2, 8)$ plotted on a Cartesian plane.",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 5, "bi",
        r"the $y$-intercept.",
        1, "Linear Functions — Intercept", 6, (5, 0.44, 0.64),
        r"$y$-intercept $= 6$", "B1",
        stem=r"For the line that passes through points $P$ and $Q$, find:",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 5, "bii",
        r"the gradient.",
        1, "Linear Functions — Gradient", 6, (5, 0.63, 0.80),
        r"Gradient $= -1$", "B1",
        topic_id=6)

    # Q6 — Page 7 (idx 6)
    add_q(db, p1.id, exam_dir, 1, 6, "a",
        r"Write down an expression, in terms of $n$, for the $n$th term of this sequence.",
        1, "Number Patterns — General Term", 7, (6, 0.07, 0.33),
        r"$T_n = 13 - 8n$", "B1",
        stem=r"A number sequence is shown below: $5, -3, -11, -19, \ldots$",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 6, "b",
        r"Hence, find the 20th term of this sequence.",
        1, "Number Patterns", 7, (6, 0.32, 0.50),
        r"$T_{20} = 13 - 8(20) = -147$", "B1",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 6, "c",
        r"Explain whether $-36$ is a term in this sequence.",
        1, "Number Patterns — Reasoning", 7, (6, 0.49, 0.75),
        r"""$13 - 8n = -36 \implies 8n = 49 \implies n = 6.125$
Since $n$ is not a positive integer, $-36$ is not a term.""", "B1",
        topic_id=7)

    # Q7 — Page 8 (idx 7)
    add_q(db, p1.id, exam_dir, 1, 7, "a",
        r"Find the original price of the game console.",
        2, "Percentage — Reverse", 8, (7, 0.07, 0.30),
        r"$$\text{Original price} = \frac{100}{107} \times 577.80 = \$540$$", "M1, A1",
        stem=r"The price of a game console, after 7% GST, is $\$577.80$.",
        topic_id=8)

    add_q(db, p1.id, exam_dir, 1, 7, "b",
        r'"An increase in GST by 2 percentage points will lead to an increase in the price of the game console, after GST, by exactly 2%." State whether you agree with the statement. Show workings to support your answer.',
        2, "Percentage", 8, (7, 0.28, 0.53),
        r"""Price with 9% GST $= \frac{109}{100} \times 540 = \$588.60$
% increase $= \frac{588.60 - 577.80}{577.80} \times 100\% = 1.87\%$
Disagree — the increase is not exactly 2%.""",
        "M1 for new price, A1 for conclusion",
        topic_id=8)

    # Q8 — Page 8 (idx 7)
    add_q(db, p1.id, exam_dir, 1, 8, "a",
        r"Convert 45 cm/s to m/min.",
        2, "Speed Conversion", 8, (7, 0.53, 0.70),
        r"$$45 \times \frac{60}{100} = 27 \text{ m/min}$$", "M1, A1",
        stem=r"A caterpillar that is 7 cm long crawls at a speed of 45 cm/s.",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 8, "b",
        r"The caterpillar takes 0.8 s to crawl through a water pipe. Calculate the length of the water pipe.",
        2, "Speed, Distance, Time", 8, (7, 0.69, 0.88),
        r"Distance $= 45 \times 0.8 = 36$ cm. Length of pipe $= 36 - 7 = 29$ cm.", "M1, A1",
        topic_id=9)

    # Q9 — Page 9 (idx 8)
    add_q(db, p1.id, exam_dir, 1, 9, None,
        r"The diagram shows an irregular polygon $MNJKL$. Angles are $(156 - y)°$, $116°$, $31°$, $(2y - 6)°$. Form an equation in terms of $y$ and find the value of $y$.",
        2, "Polygon Angles", 9, (8, 0.07, 0.86),
        r"""Sum of interior angles of pentagon $= (5-2) \times 180° = 540°$
$(156 - y) + 116 + 31 + (2y - 6) + y = 540$
$2y + 297 = 540$
$y = 60°$ (accept $y = 121.5$)""",
        "M1 for equation, A1",
        topic_id=11)

    # Q10 — Page 10 (idx 9)
    add_q(db, p1.id, exam_dir, 1, 10, "a",
        r"angle $ACB$.",
        3, "Angle Properties", 10, (9, 0.07, 0.62),
        r"""$\angle AEB = 95°$ (vert. opp. angles)
$\angle ACB = \angle CAB$ (base angles, isos. triangle)
$= \frac{180° - 27° - 95°}{2} = 58°$$""",
        "M1 for vert opp, M1 for base angles, A1",
        stem=r"In the diagram, $AEC$ and $BED$ are straight lines. $AB$ and $BC$ are equal in length. Angle $ABE = 27°$ and angle $DEC = 95°$. Stating your reasons clearly, find:",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 10, "b",
        r"reflex angle $ABC$.",
        2, "Angle Properties", 10, (9, 0.60, 0.82),
        r"Angle $ABC = 360° - 64° = 296°$ (angles at a point)", "M1, A1",
        topic_id=10)

    # Q11 — Page 11 (idx 10)
    add_q(db, p1.id, exam_dir, 1, 11, "a",
        r"Construct triangle $XYZ$ where $XY = 7$ cm, angle $ZXY = 70°$ and angle $ZYX = 25°$.",
        2, "Construction", 11, (10, 0.07, 0.80),
        r"Two lines drawn at angles of $70°$ and $25°$ from $XY = 7$ cm.", "B1 for each angle",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 11, "b",
        r"Measure the length of $YZ$.",
        1, "Construction — Measurement", 11, (10, 0.79, 0.90),
        r"$YZ = 6.6 \pm 0.1$ cm", "B1",
        topic_id=10)

    # Q12 — Page 12 (idx 11)
    add_q(db, p1.id, exam_dir, 1, 12, "a",
        r"Find the cross-sectional area of the prism.",
        2, "Area — Composite", 12, (11, 0.07, 0.58),
        r"$$\text{Area} = \frac{1}{2}(5 + 10)(8) = 60 \text{ cm}^2$$", "M1, A1",
        stem=r"The diagram shows a 3D model of the number '1'. It is a solid prism with a cross-section composed of a parallelogram and a trapezium. Dimensions: 5 cm, 8 cm, 10 cm.",
        topic_id=12)

    add_q(db, p1.id, exam_dir, 1, 12, "b",
        r"Given that the prism has a depth of 3 cm, find its volume.",
        1, "Volume — Prism", 12, (11, 0.57, 0.85),
        r"$$V = 60 \times 3 = 180 \text{ cm}^3$$", "B1",
        topic_id=13)

    # ══════════════════════════════════════════════
    # PAPER 2 — Pages 14-30 (idx 13-29), 60 marks, 1h30m
    # ══════════════════════════════════════════════
    p2 = Paper(exam_id=exam.id, paper_number=2, duration_minutes=90, total_marks=60,
               date=date(2022, 10, 6), instructions="Answer all questions.")
    db.add(p2); db.flush()

    # P2 Q1 — Page 14 (idx 13)
    add_q(db, p2.id, exam_dir, 2, 1, "a",
        r"By rounding each number to 2 significant figures, estimate the value of $\dfrac{21.1 + \sqrt{1338}}{0.499 \times 10.3}$.",
        2, "Estimation", 14, (13, 0.09, 0.40),
        r"$$\approx \frac{21 + \sqrt{1300}}{0.50 \times 10} = \frac{21 + 36}{5} \approx \frac{57}{5} = 11.4$$", "M1, A1",
        topic_id=3)

    add_q(db, p2.id, exam_dir, 2, 1, "b",
        r"Find the greatest number that will divide $p$, $q$ and $r$ exactly.",
        1, "HCF", 14, (13, 0.40, 0.90),
        r"$\text{HCF} = 2^2 \times 3 = 12$", "A1",
        stem=r"When written as a product of their prime factors: $p = 2^5 \times 3^2$, $q = 2^2 \times 3^4 \times 5^2$, $r = 2^2 \times 3 \times 5^3 \times 11$.",
        topic_id=1)

    # P2 Q2 — Page 15 (idx 14)
    add_q(db, p2.id, exam_dir, 2, 2, "a",
        r"Find the total cost of 3 plates of chicken rice and a bowl of prawn noodle.",
        3, "Linear Equations — Word Problem", 15, (14, 0.07, 0.62),
        r"""$4x + 2(x + 0.5) = 25$
$6x + 1 = 25 \implies x = 4$
Total $= 3(4) + 4.50 = \$16.50$""",
        "M1 for equation, M1 for solving, A1",
        stem=r"One plate of chicken rice costs $\$x$ and a bowl of prawn noodle costs 50 cents more. Ryan ordered 4 plates of chicken rice and 2 bowls of prawn noodle and the total cost is $\$25$.",
        topic_id=5)

    add_q(db, p2.id, exam_dir, 2, 2, "b",
        r"All three sirens sounded off together at 8 a.m. At what time will they next sound off together?",
        2, "LCM", 15, (14, 0.60, 0.92),
        r"$\text{LCM}(12, 30, 40) = 120$ minutes $= 2$ hours. Next: $10$ a.m.",
        "M1 for LCM, A1",
        stem=r"There are three sirens A, B and C. Siren A sounds every 12 minutes, B every 30 minutes, C every 40 minutes. They started sounding together at 8 a.m.",
        topic_id=1)

    # P2 Q3 — Page 16 (idx 15)
    add_q(db, p2.id, exam_dir, 2, 3, "a",
        r"Showing your working, find the value of $p$.",
        2, "Ratio", 16, (15, 0.07, 0.40),
        r"""Total units $= p + (2p - 1) + (2p + 1) = 5p$
$5p = 680 \implies p = 136$""",
        "M1, A1",
        stem=r"$\$680$ is shared among three friends, Muthu, Ming and Yusof in the ratio $p : (2p - 1) : (2p + 1)$, where $p$ is a positive integer.",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 3, "b",
        r"Hence, find the amount of the largest share.",
        1, "Ratio", 16, (15, 0.39, 0.74),
        r"Largest share $= 2(136) + 1 = 273$ units. Amount $= \frac{273}{680} \times 680 = \$273$", "A1",
        topic_id=9)

    # P2 Q4 — Page 17 (idx 16)
    add_q(db, p2.id, exam_dir, 2, 4, "a",
        r"Calculate the cost price of the skateboard.",
        2, "Percentage — Loss", 17, (16, 0.07, 0.46),
        r"$$\text{Cost price} = \frac{185}{95} \times 100 = \$194.74 \text{ (2 d.p.)}$$", "M1, A1",
        stem=r"Bryan bought a skateboard at a price of $\$185$ from Ali. Ali made a loss of 5% from the sale.",
        topic_id=8)

    add_q(db, p2.id, exam_dir, 2, 4, "b",
        r"Bryan decided to sell the skateboard after 1 year. How much must he sell in order to make a profit of 8%?",
        2, "Percentage — Profit", 17, (16, 0.45, 0.82),
        r"$$\text{Selling price} = 185 \times 1.08 = \$199.80$$", "M1, A1",
        topic_id=8)

    # P2 Q5 — Page 18 (idx 17)
    add_q(db, p2.id, exam_dir, 2, 5, None,
        r"In the figure, $AB$ is parallel to $DF$. Jenny claimed that angle $ABC = 180° - 46°$ due to interior angles. By showing your working with reasons, state whether you agree or disagree with her.",
        3, "Angle Properties — Parallel Lines", 18, (17, 0.07, 0.90),
        r"""Draw line $GH$ parallel to $AB$ and $DF$.
$\angle GCE = 180° - 46° = 134°$ (int. angles, $DF \parallel GH$)
$\angle GCB = 360° - 134° - 104° = 122°$ (angles at a point)
$\angle ABC = 180° - 122° = 58°$ (int. angles, $AB \parallel GH$)
$58° \neq 180° - 46° = 134°$. Disagree with Jenny.""",
        "M1 for method, M1 for working, A1 for conclusion",
        topic_id=10)

    # P2 Q6 — Page 19 (idx 18)
    add_q(db, p2.id, exam_dir, 2, 6, "a",
        r"Solve the equation $\dfrac{y}{3} + \dfrac{2y - 1}{4} = 1$.",
        3, "Solving Linear Equations", 19, (18, 0.07, 0.45),
        r"""$$\frac{4y + 3(2y-1)}{12} = 1$$
$$4y + 6y - 3 = 12$$
$$10y = 15 \implies y = 1.5$$""",
        "M1 for LCD, M1 for expanding, A1",
        topic_id=5)

    add_q(db, p2.id, exam_dir, 2, 6, "b",
        r"Given that $D = \sqrt{b^2 - 4ac}$, find the value of $D$ when $b = -8$, $a = 3$ and $c = -1$.",
        1, "Formula Substitution", 19, (18, 0.44, 0.88),
        r"$$D = \sqrt{(-8)^2 - 4(3)(-1)} = \sqrt{64 + 12} = \sqrt{76} \approx 8.72 \text{ (3 s.f.)}$$", "A1",
        topic_id=4)

    # P2 Q7 — Page 20 (idx 19)
    add_q(db, p2.id, exam_dir, 2, 7, "a",
        r"Calculate the time taken for the entire journey. Give your answer in hours and minutes.",
        2, "Speed, Distance, Time", 20, (19, 0.07, 0.38),
        r"Time $= \frac{80}{75} + \frac{66}{55} = \frac{16}{15} + \frac{6}{5} = \frac{34}{15}$ h $= 2$ h $16$ min", "M1, A1",
        stem=r"Mr Raj drove from Town A to Town B at 75 km/h for 80 km. He continued from Town B to Town C at 55 km/h for 66 km.",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 7, "b",
        r"Find the average speed for its entire journey, correct to 1 decimal place.",
        2, "Speed, Distance, Time", 20, (19, 0.38, 0.63),
        r"$$\text{Average speed} = \frac{80 + 66}{\frac{34}{15}} = \frac{146 \times 15}{34} = 64.4 \text{ km/h}$$", "M1, A1",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 7, "c",
        r"Convert your answer in part (b) to m/s.",
        2, "Speed Conversion", 20, (19, 0.62, 0.88),
        r"$$64.4 \times \frac{1000}{3600} = 17.9 \text{ m/s (3 s.f.)}$$", "M1, A1",
        topic_id=9)

    # P2 Q8 — Pages 21-22 (idx 20-21)
    add_q(db, p2.id, exam_dir, 2, 8, "a",
        r"Find the total surface area of the unsharpened pencil.",
        3, "Surface Area — Cylinder", 21, (20, 0.07, 0.58),
        r"$$\text{SA} = 2\pi(1)^2 + 2\pi(1)(20) = 2\pi + 40\pi = 42\pi \approx 131.9 \text{ cm}^2$$", "M1 for circles, M1 for curved, A1",
        stem=r"Shi Kai bought a new unsharpened pencil in the shape of a cylinder. Length $= 20$ cm, diameter $= 2$ cm. After sharpening, the pencil is a cylinder (length 11 cm) and a cone.",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 8, "b",
        r"Given that the volume of the cone is $0.8378$ cm$^3$, find the total volume of the sharpened pencil.",
        2, "Volume — Cylinder + Cone", 21, (20, 0.56, 0.90),
        r"$$V = \pi(1)^2(11) + 0.8378 = 11\pi + 0.8378 \approx 35.4 + 0.84 = 36.3 \text{ cm}^3$$", "M1, A1",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 8, "c",
        r"Calculate the volume of the pencil he has used.",
        1, "Volume — Subtraction", 22, (21, 0.07, 0.50),
        r"Volume used $= \pi(1)^2(20) - 36.3 = 62.8 - 36.3 = 26.5$ cm$^3$ (3 s.f. from unrounded)", "A1",
        topic_id=13)

    # P2 Q9 — Pages 23-24 (idx 22-23)
    add_q(db, p2.id, exam_dir, 2, 9, "a",
        r"Calculate the value of $a$.",
        1, "Linear Functions — Table", 23, (22, 0.07, 0.32),
        r"$a = 3(30) + 30 = 120$", "B1",
        stem=r"The cost, $\$y$, of printing $x$ number of T-shirts, is given by the equation $y = 3x + 30$.",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 9, "b",
        r"On the grid, draw the graph of $y = 3x + 30$ for $0 \leq x \leq 40$.",
        2, "Linear Functions — Graph", 23, (22, 0.30, 0.95),
        r"Straight line through $(0, 30)$, $(10, 60)$, $(20, 90)$, $(30, 120)$, $(40, 150)$.", "B1 for points, B1 for line",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 9, "c",
        r"Use your graph to find the number of T-shirts that are printed when the cost is $\$55$.",
        1, "Linear Functions — Reading Graph", 24, (23, 0.07, 0.24),
        r"Approx $8$ or $8.3$ T-shirts", "B1",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 9, "d",
        r"Explain what $30$ in the equation represents.",
        1, "Linear Functions — Interpretation", 24, (23, 0.24, 0.42),
        r"$30$ represents the fixed cost (setup fee) before any T-shirts are printed.", "B1",
        topic_id=6)

    # P2 Q10 — Pages 25-26 (idx 24-25)
    add_q(db, p2.id, exam_dir, 2, 10, "a",
        r"Calculate the size of one interior angle of a regular pentagon.",
        2, "Polygon Angles — Interior", 25, (24, 0.07, 0.32),
        r"$$\frac{(5-2) \times 180°}{5} = 108°$$", "M1, A1",
        topic_id=11)

    add_q(db, p2.id, exam_dir, 2, 10, "bi",
        r"Calculate the angle $ABC$.",
        2, "Polygon Angles", 25, (24, 0.32, 0.67),
        r"Interior to exterior ratio $= 2:1$, so interior $= 120°$. $\angle ABC = 120°$", "M1, A1",
        stem=r"The diagram shows part of a regular $n$-sided polygon $ABCD\ldots$ The size of one interior angle to one exterior angle is in the ratio $2 : 1$.",
        topic_id=11)

    add_q(db, p2.id, exam_dir, 2, 10, "bii",
        r"Calculate the angle $ACD$.",
        2, "Polygon Angles", 25, (24, 0.66, 0.92),
        r"$\angle ACD = 120° - 60° = 60°$ (isosceles triangle)", "M1, A1",
        topic_id=11)

    add_q(db, p2.id, exam_dir, 2, 10, "biii",
        r"Find the value of $n$.",
        1, "Polygon Angles", 26, (25, 0.07, 0.40),
        r"Exterior angle $= 60°$, $n = \frac{360°}{60°} = 6$", "B1",
        topic_id=11)

    # P2 Q11 — Pages 27-28 (idx 26-27)
    add_q(db, p2.id, exam_dir, 2, 11, "a",
        r"angle $ADC$.",
        2, "Angle Properties — Rhombus", 27, (26, 0.07, 0.64),
        r"$\angle ADC = 180° - 2(21° + 35°) = 180° - 112° = 68°$... or $\angle ACD = 35°$, $\angle ADB = 21°$, by rhombus properties.", "M1, A1",
        stem=r"$ABCD$ is a rhombus. $PDR$, $APQ$ and $BCR$ are straight lines. $AC$ is parallel to $PR$. Angle $PAD = 21°$, angle $ACD = 35°$ and angle $PQR = 100°$. Calculate:",
        topic_id=10)

    add_q(db, p2.id, exam_dir, 2, 11, "b",
        r"angle $APD$.",
        2, "Angle Properties", 27, (26, 0.62, 0.92),
        r"$\angle APD = 180° - 100° = 80°$ (angles on straight line) or by triangle angle sum.", "M1, A1",
        topic_id=10)

    add_q(db, p2.id, exam_dir, 2, 11, "c",
        r"angle $PRQ$.",
        1, "Angle Properties", 28, (27, 0.07, 0.38),
        r"$\angle PRQ$ from parallel lines and triangle properties.", "B1",
        topic_id=10)

    add_q(db, p2.id, exam_dir, 2, 11, "d",
        r"Given that the area of the rhombus $ABCD$ is 94 cm$^2$ and the perpendicular height is 9.4 cm, find the perimeter of the rhombus.",
        2, "Perimeter — Rhombus", 28, (27, 0.37, 0.76),
        r"Side $= \frac{94}{9.4} = 10$ cm. Perimeter $= 4 \times 10 = 40$ cm.", "M1, A1",
        topic_id=12)

    # P2 Q12 — Pages 29-30 (idx 28-29)
    add_q(db, p2.id, exam_dir, 2, 12, "a",
        r"Calculate the amount Mr Lee needs to pay if he buys the tickets online.",
        2, "Percentage — Discount", 29, (28, 0.07, 0.90),
        r"""5 tickets: $2 \times 24 + 2 \times 18 + 1 \times 12 = 48 + 36 + 12 = \$96$
Online 5% discount: $96 \times 0.95 = \$91.20$""",
        "M1, A1",
        stem=r"Museum tickets: Adult $\$24$, Child $\$18$, Senior $\$12$. Mr Lee (55), Mrs Lee (55), elderly father (80), 2 children. Online: 5% discount. On-site: A-Card 10% off adult, C-Card 8% off child, S-Card 15% off senior.",
        topic_id=8)

    add_q(db, p2.id, exam_dir, 2, 12, "b",
        r"If Mr Lee intends to bring only his children to the museum and buys on-site using C-Card, calculate the amount he needs to pay.",
        2, "Percentage — Discount", 30, (29, 0.07, 0.30),
        r"$1 \times 24 + 2 \times 18 \times 0.92 = 24 + 33.12 = \$57.12$", "M1, A1",
        topic_id=8)

    add_q(db, p2.id, exam_dir, 2, 12, "c",
        r"Mrs Lee claims that using the S-Card membership to buy the 5 tickets will be the cheapest alternative. Do you agree? Show your working clearly.",
        4, "Percentage — Comparison", 30, (29, 0.29, 0.70),
        r"""S-Card: $2 \times 24 + 2 \times 18 + 12 \times 0.85 = 48 + 36 + 10.20 = \$94.20$
Online: $\$91.20$ (from part a)
Disagree — online is cheaper.""",
        "M1 for S-Card calc, M1 for comparison, M1 for working, A1",
        topic_id=8)

    add_q(db, p2.id, exam_dir, 2, 12, "d",
        r"State one assumption for your choice.",
        1, "Real-World Context", 30, (29, 0.69, 0.82),
        r"Assume Mr Lee does not have an A-Card, C-Card, or S-Card membership (or that they can only use one card).", "B1",
        topic_id=8)

    db.commit()
    p1_count = len(p1.questions)
    p2_count = len(p2.questions)
    print(f"Seeded Queensway exam id={exam.id}: Paper 1 ({p1_count} parts), Paper 2 ({p2_count} parts)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
