"""Seed Bendemeer Secondary School SA2 2021 Sec 1 Express Math exam."""

import os
import shutil
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/66a8b9d3448f5_3519.pdf"
IMAGES_DIR = "/tmp/bendemeer_pages"

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

    existing = db.query(Exam).filter(Exam.school_id == school.id, Exam.year == 2021).first()
    if existing:
        print(f"Bendemeer 2021 already seeded (id={existing.id}). Deleting and re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id, title="SA2 / End of Year Examination 2021", year=2021,
        level="Secondary 1 Express", subject="Mathematics",
        source_pdf="66a8b9d3448f5_3519.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # PAPER 1 — Pages 2-13 (idx 1-12), 50 marks, 1h15m
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=75, total_marks=50,
               date=date(2021, 10, 8), instructions="Answer all questions.")
    db.add(p1); db.flush()

    # Q1 — Page 2 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 1, "a",
        r"Which of the following numbers are irrational?",
        1, "Number Classification", 3, (2, 0.05, 0.20),
        r"$\pi$, $\sqrt{2}$", "A1",
        stem=r"$1.\dot{3}$, $-1.5$, $\pi$, $\sqrt{2}$, $-4$",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 1, "b",
        r"Arrange the numbers above in ascending order.",
        1, "Number Ordering", 3, (2, 0.19, 0.34),
        r"$-4, -1.5, 1.\dot{3}, \sqrt{2}, \pi$", "A1",
        topic_id=2)

    # Q2 — Page 2 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 2, "a",
        r"Express $43\frac{1}{3}\%$ as a decimal.",
        1, "Percentage Conversion", 3, (2, 0.34, 0.50),
        r"$0.43\dot{3}$ (3 s.f.)", "A1",
        topic_id=8)

    add_q(db, p1.id, exam_dir, 1, 2, "b",
        r"Given that $\dfrac{m}{4} = \dfrac{2n}{3}$, find the ratio $m : n$.",
        2, "Ratio", 3, (2, 0.50, 0.92),
        r"$$\frac{m}{4} = \frac{2n}{3} \implies 3m = 8n \implies \frac{m}{n} = \frac{8}{3}$$" "\n" r"$m : n = 8 : 3$",
        "M1, A1",
        topic_id=9)

    # Q3 — Page 3 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 3, "a",
        r"Expand and simplify the following expression: $3c(2d - 5) - 5(c + 3)$",
        2, "Algebra — Expansion", 4, (3, 0.04, 0.22),
        r"$$3c(2d - 5) - 5(c + 3) = 6cd - 15c - 5c - 15 = 6cd - 20c - 15$$", "M1, A1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 3, "b",
        r"Factorise completely: $\pi r^2 + 2\pi rh + \pi rl$",
        1, "Algebra — Factorisation", 4, (3, 0.22, 0.42),
        r"$\pi r(r + 2h + l)$", "A1",
        topic_id=4)

    # Q4 — Page 3 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 4, "a",
        r'Write the algebraic expression for "The sum of $x$ and $y$ divided by 2 times of $x$". Give your expression in fraction form.',
        1, "Algebra — Expression", 4, (3, 0.42, 0.65),
        r"$\dfrac{x + y}{2x}$", "A1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 4, "b",
        r"Evaluate $\dfrac{n - 2x}{\sqrt[3]{5y^2}}$ when $x = -5$ and $y = 4$.",
        2, "Algebra — Substitution", 4, (3, 0.65, 0.92),
        r"$$\frac{n - 2(-5)}{\sqrt[3]{5(4)^2}} = \frac{n + 10}{\sqrt[3]{80}} \approx -1.05$$"
        "\n(When $n = -5$: answer $= -1.05$)",
        "M1, A1",
        topic_id=4)

    # Q5 — Page 4 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 5, "a",
        r"Express the following as a fraction in its simplest form: $2 + \dfrac{1}{4}(12x - 8)$",
        2, "Algebra — Simplification", 5, (4, 0.04, 0.33),
        r"$$2 + \frac{1}{4}(12x - 8) = 2 + 3x - 2 = 3x$$", "M1, A1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 5, "b",
        r"Solve the following equation: $\dfrac{5x}{3} - \dfrac{2x - 3}{2} = -1$",
        3, "Linear Equations", 5, (4, 0.33, 0.92),
        r"""$$\frac{10x}{6} - \frac{3(2x - 3)}{6} = -1$$
$$\frac{10x - 6x + 9}{6} = -1$$
$$4x + 9 = -6$$
$$x = \frac{-15}{4} = -3.75 \text{ or } -3\frac{3}{4}$$""",
        "M1 for LCD, M1 for expanding, A1",
        topic_id=5)

    # Q6 — Page 5 (idx 5)
    add_q(db, p1.id, exam_dir, 1, 6, "a",
        r"Find the value of $a$.",
        1, "Number Patterns", 6, (5, 0.04, 0.26),
        r"$a = 26$", "A1",
        stem=r"Each of the term in this sequence is found by adding the same number to the previous term: $19, a, 33, 40, \ldots$",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 6, "b",
        r"Find an expression, in terms of $n$, for the $n$th term of the sequence.",
        1, "Number Patterns — General Term", 6, (5, 0.26, 0.48),
        r"$T_n = 7n + 12$", "A1",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 6, "c",
        r"Determine if 117 is a term of this sequence. Justify your answer with working.",
        2, "Number Patterns — Reasoning", 6, (5, 0.48, 0.92),
        r"""$7n + 12 = 117$
$n = (117 - 12) \div 7 = 15$
Since $n$ is an integer, it is a term in the sequence.""",
        "M1, A1",
        topic_id=7)

    # Q7 — Page 6 (idx 6)
    add_q(db, p1.id, exam_dir, 1, 7, "a",
        r"$\sqrt{6\frac{1}{16}}$ can be expressed as the rational number $\dfrac{p}{q}$ where $p$ and $q$ are positive integers. Find the values of $p$ and $q$.",
        1, "Rational Numbers", 7, (6, 0.04, 0.26),
        r"$p = 9$, $q = 4$", "A1",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 7, "b",
        r"The number of people in a theatre is given as 500, correct to the nearest hundred. Write down the minimum number of people that could be in the theatre at this time.",
        1, "Approximation", 7, (6, 0.26, 0.45),
        r"$450$", "A1",
        topic_id=3)

    # Q8 — Page 6 (idx 6)
    add_q(db, p1.id, exam_dir, 1, 8, None,
        r"The ratio of the amount of money that Jenny has to that of Lucy is $1 : 2$ and the ratio of the amount of money that Lucy has to that of Ivy is $5 : 3$. Given that the total sum of money of the three ladies is $\$63x$, how much money does Ivy have in terms of $x$?",
        3, "Ratio — Combined", 7, (6, 0.45, 0.92),
        r"""Jenny : Lucy = 1 : 2 = 5 : 10
Lucy : Ivy = 5 : 3 = 10 : 6
Jenny : Lucy : Ivy = 5 : 10 : 6
Total = 21 units = $\$63x$
6 units $= \frac{6}{21} \times 63x = \$18x$
Ivy has $\$18x$""",
        "M1 for combined ratio, M1 for calculation, A1",
        topic_id=9)

    # Q9 — Page 7 (idx 7)
    add_q(db, p1.id, exam_dir, 1, 9, "ai",
        r"Express 168 as the product of prime factors.",
        1, "Prime Factorisation", 8, (7, 0.04, 0.22),
        r"$168 = 2^3 \times 3 \times 7$", "A1",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 9, "aii",
        r"Find the smallest integer, $k$, such that $168k$ is a perfect square.",
        1, "Perfect Square", 8, (7, 0.22, 0.43),
        r"$k = 42$", "A1",
        topic_id=1)

    add_q(db, p1.id, exam_dir, 1, 9, "b",
        r"Given that $324 = 2^2 \times 3^4$, find the largest integer which is a factor of 168 and 324.",
        1, "HCF", 8, (7, 0.43, 0.92),
        r"$\text{HCF} = 12$", "A1",
        topic_id=1)

    # Q10 — Page 8 (idx 8)
    add_q(db, p1.id, exam_dir, 1, 10, "a",
        r"Find the height of the cylinder.",
        1, "Volume — Cylinder", 9, (8, 0.04, 0.38),
        r"$$300\pi = \pi(5)^2 h \implies h = \frac{300\pi}{25\pi} = 12 \text{ cm}$$", "A1",
        stem=r"A closed cylinder with base radius 5 cm has a volume of $300\pi$ cm$^3$.",
        topic_id=13)

    add_q(db, p1.id, exam_dir, 1, 10, "b",
        r"Find the total surface area of the cylinder.",
        2, "Surface Area — Cylinder", 9, (8, 0.38, 0.92),
        r"$$\text{TSA} = 2\pi(5)(12) + 2\pi(5)^2 = 120\pi + 50\pi = 170\pi \approx 534 \text{ cm}^2 \text{ (3 s.f.)}$$",
        "M1, A1",
        topic_id=13)

    # Q11 — Page 9 (idx 9)
    add_q(db, p1.id, exam_dir, 1, 11, "a",
        r"Find $\angle x$.",
        3, "Angle Properties — Parallel Lines", 10, (9, 0.04, 0.50),
        r"""$\angle AEM = \angle EAF = 44°$ (alternate angles, $DC \parallel AG$)
$\angle DEM = 180° - 116° = 64°$ (interior angle, $DC \parallel EM$)
$\angle x = 64° + 44° = 108°$""",
        "M1 for alternate angles, M1 for interior angle, A1",
        stem=r"In the figure below, $ED \parallel BC$, $DC \parallel FABG$, $\angle EDC = 116°$ and $\angle EAF = 44°$. Stating your reasons clearly, calculate:",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 11, "b",
        r"Find $\angle y$.",
        1, "Angle Properties — Parallel Lines", 10, (9, 0.50, 0.92),
        r"$\angle y = 64°$ (corresponding angles, $ED \parallel BC$)", "A1",
        topic_id=10)

    # Q12 — Page 10 (idx 10)
    add_q(db, p1.id, exam_dir, 1, 12, "ai",
        r"Find $\angle CDE$.",
        2, "Polygon Angles — Interior", 11, (10, 0.04, 0.40),
        r"$$\angle CDE = \frac{(5 - 2) \times 180°}{5} = 108°$$", "M1, A1",
        stem=r"The diagram shows a regular pentagon $ABCDE$ and three of the sides, $GE$, $ED$ and $DF$, of a second regular polygon. Given that $\angle CDF = 96°$.",
        topic_id=11)

    add_q(db, p1.id, exam_dir, 1, 12, "aii",
        r"Find $\angle EDF$.",
        1, "Polygon Angles", 11, (10, 0.40, 0.56),
        r"$\angle EDF = 360° - 108° - 96° = 156°$", "A1",
        topic_id=11)

    add_q(db, p1.id, exam_dir, 1, 12, "b",
        r"Hence, find the number of sides in the second regular polygon.",
        2, "Polygon Angles — Exterior", 11, (10, 0.56, 0.92),
        r"""Exterior angle of second polygon $= 180° - 156° = 24°$
Number of sides $= \frac{360°}{24°} = 15$""",
        "M1, A1",
        topic_id=11)

    # Q13 — Page 11 (idx 11)
    add_q(db, p1.id, exam_dir, 1, 13, "a",
        r"An airplane leaves Country A at 09 00 local time. The distance between Country A to Country B is 5407.5 km. The average speed of the airplane is 721 km/h. The airplane arrives in Country B at 15 00 local time. Find the time difference between Country A and Country B, stating whether the time in Country B is ahead or behind the time in Country A. Show your working clearly.",
        3, "Speed, Distance, Time", 12, (11, 0.04, 0.48),
        r"""Time taken $= \frac{5407.5}{721} = 7.5$ hours
Arrival time at Country A $= 09\,00 + 7.5$ h $= 16\,30$
Arrival time at Country B $= 15\,00$
Country B is behind by 1.5 hours.""",
        "M1 for time taken, M1 for comparison, A1",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 13, "b",
        r"A car travels at 72 km/h. Convert the speed to metres per second.",
        2, "Speed Conversion", 12, (11, 0.48, 0.92),
        r"$$72 \text{ km/h} = \frac{72 \times 1000}{1 \times 3600} = 20 \text{ m/s}$$", "M1, A1",
        topic_id=9)

    # Q14 — Pages 12-13 (idx 12-13)
    add_q(db, p1.id, exam_dir, 1, 14, "a",
        r"Write down the equation of $L_2$.",
        1, "Linear Functions — Equation", 13, (12, 0.04, 0.58),
        r"$x = 3$", "A1",
        stem=r"The graph below shows two straight lines $L_1$ and $L_2$.",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 14, "b",
        r"Calculate the area enclosed by the line $L_1$, the line $L_2$ and the $x$-axis.",
        2, "Area — Triangle", 13, (12, 0.58, 0.92),
        r"$$\text{Area} = \frac{1}{2} \times 5 \times 7 = 17.5 \text{ square units}$$", "M1, A1",
        topic_id=12)

    add_q(db, p1.id, exam_dir, 1, 14, "ci",
        r"If the gradient for the line $L_1$ increases, describe how the new straight line differs from the original straight line.",
        1, "Linear Functions — Gradient", 14, (13, 0.04, 0.20),
        r"The new straight line will be steeper than the original line.", "A1",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 14, "cii",
        r"Jane wants to draw a new line with the same gradient as line $L_1$. She claimed that the new line and $L_1$ will meet at the origin. Explain whether you agree or disagree with her.",
        1, "Linear Functions — Parallel Lines", 14, (13, 0.20, 0.55),
        r"Disagree. Because if the two lines have the same gradient, then the two lines are parallel to each other so they will not meet each other. OR: Because the original line $L_1$ does not pass through the origin so it will never meet the new line at the origin.",
        "A1",
        topic_id=6)

    # ══════════════════════════════════════════════
    # PAPER 2 — Pages 15-24 (idx 14-24), 50 marks, 1h15m
    # ══════════════════════════════════════════════
    p2 = Paper(exam_id=exam.id, paper_number=2, duration_minutes=75, total_marks=50,
               date=date(2021, 10, 11), instructions="Answer all questions.")
    db.add(p2); db.flush()

    # P2 Q1 — Page 15 (idx 15)
    add_q(db, p2.id, exam_dir, 2, 1, "a",
        r"Solve the following equation: $x - [3 - 2(5x - 0.5)] = 18$",
        2, "Linear Equations", 16, (15, 0.05, 0.28),
        r"""$$x - [3 - 10x + 1] = 18$$
$$x - [4 - 10x] = 18$$
$$x - 4 + 10x = 18$$
$$11x = 22 \implies x = 2$$""",
        "M1, A1",
        topic_id=5)

    add_q(db, p2.id, exam_dir, 2, 1, "b",
        r"Simplify $\dfrac{8p + 16}{4} \times \dfrac{1}{p + 2}$.",
        2, "Algebra — Simplification", 16, (15, 0.28, 0.50),
        r"$$= \frac{8(p + 2)}{4} \times \frac{1}{p + 2} = \frac{8}{4} = 2$$"
        "\n(Accept: $= p + 2$ if not fully simplified step shown, but answer is $2$)",
        "M1, A1",
        topic_id=4)

    add_q(db, p2.id, exam_dir, 2, 1, "c",
        r"Factorise $3a(3 + b) + 5(ab + a)$.",
        2, "Algebra — Factorisation", 16, (15, 0.50, 0.92),
        r"""$$= 9a + 3ab + 5ab + 5a$$
$$= 14a + 8ab$$
$$= 2a(7 + 4b)$$""",
        "M1, A1",
        topic_id=4)

    # P2 Q2 — Page 16 (idx 16)
    add_q(db, p2.id, exam_dir, 2, 2, "a",
        r"Mr Koh borrows $\$30\,000$ from a bank on 1st January 2021 to renovate his house. The bank charges simple interest at a rate of 2.6% per annum. Calculate the amount of interest he has to pay at the end of December 2025.",
        2, "Percentage — Simple Interest", 17, (16, 0.04, 0.28),
        r"$$\text{Interest} = \frac{2.6}{100} \times 30\,000 \times 5 = \$3900$$", "M1, A1",
        topic_id=8)

    add_q(db, p2.id, exam_dir, 2, 2, "b",
        r"Mr Koh decides to travel from Singapore to Taiwan for a holiday. The exchange rate in Singapore is 1 Singapore Dollar = 20.516 Taiwan dollars. The exchange rate in Taiwan is 100 Taiwan Dollars = 4.874 Singapore dollars. Mr Koh wants to exchange 1000 Singapore dollars to Taiwan dollars. Determine how much more Taiwan dollars he will receive by changing his money in Taiwan. Give your answer to the nearest cents.",
        3, "Rate — Currency Exchange", 17, (16, 0.28, 0.92),
        r"""In Singapore: $1000 \times 20.516 = 20516$ Taiwan Dollars
In Taiwan: $1000 \div 4.874 \times 100 = 20517.03$ Taiwan Dollars
Extra $= 20517.03 - 20516 = 1.03$ Taiwan Dollars""",
        "M1 for Singapore, M1 for Taiwan, A1",
        topic_id=9)

    # P2 Q3 — Page 17 (idx 17)
    add_q(db, p2.id, exam_dir, 2, 3, "i",
        r"Find $y$.",
        2, "Angle Properties — Parallelogram", 18, (17, 0.04, 0.50),
        r"""$\angle HCB = 22°$ (vert. opp. $\angle s$)
$\angle DCB = 72°$ (opp. $\angle s$ of parallelogram)
$y = 72° - 22° = 50°$""",
        "Reasoning: M1, Answer: A1",
        stem=r"In the diagram, $ABCD$ is a parallelogram with $\angle DAB = 72°$. $DCE$, $HCF$ and $BCG$ are straight lines. $\angle GCF = 22°$, $\angle DCH = y°$ and $\angle AHC = z°$. Find, giving reasons for your workings:",
        topic_id=10)

    add_q(db, p2.id, exam_dir, 2, 3, "ii",
        r"Find $z$.",
        2, "Angle Properties — Parallel Lines", 18, (17, 0.50, 0.92),
        r"$z = 180° - 50° = 130°$ (int. $\angle s$, $DE \parallel AB$)", "Reasoning: M1, Answer: A1",
        topic_id=10)

    # P2 Q4 — Page 18 (idx 18)
    add_q(db, p2.id, exam_dir, 2, 4, "i",
        r"Find and simplify the area of the parallelogram $PQRS$ in terms of $x$.",
        2, "Area — Parallelogram", 19, (18, 0.04, 0.43),
        r"$$\text{Area} = (6)(8x) = 48x \text{ cm}^2$$"
        "\n(Note: $QU$ is perpendicular to $PS$, $QU = 8x$ cm, $PQ = (4x - 2)$ cm and $PS = 6$ cm.)",
        "M1, A1",
        stem=r"The figure below shows a parallelogram $PQRS$ and two identical semi-circles with radius 2 cm. Given that $QU$ is perpendicular to $PS$, $QU = 8x$ cm, $PQ = (4x - 2)$ cm and $PS = 6$ cm.",
        topic_id=12)

    add_q(db, p2.id, exam_dir, 2, 4, "ii",
        r"Calculate the total area of the two semi-circles and leave your answer in terms of $\pi$.",
        1, "Area — Circle", 19, (18, 0.43, 0.60),
        r"$$\text{Area of 2 semi-circles} = \pi(2)^2 = 4\pi \text{ cm}^2$$", "A1",
        topic_id=12)

    add_q(db, p2.id, exam_dir, 2, 4, "iii",
        r"Hence, find the area of the shaded region in terms of $x$ and $\pi$.",
        1, "Area — Composite", 19, (18, 0.60, 0.92),
        r"$$\text{Shaded area} = 48x - 4\pi \text{ cm}^2$$", "A1",
        topic_id=12)

    # P2 Q5 — Pages 19-20 (idx 19-20)
    add_q(db, p2.id, exam_dir, 2, 5, "a",
        r"Using a scale of 2 cm to 1 unit, draw a horizontal $x$-axis from $-4$ to $4$ and a scale of 1 cm to 1 unit, draw a vertical $y$-axis from $-2$ to $14$ on the grid. On the same axes, plot the points given in the table and join them with a straight line.",
        3, "Linear Functions — Graph", 20, (19, 0.04, 0.22),
        r"See attached graph. Scale for each axis: M2. Points and join up the points to get the straight line: M1.",
        "M2 for scale, M1 for line",
        stem=r"The table below shows some values of $x$ and the corresponding values of $y$: $(-4, 14)$, $(0, 6)$, $(4, -2)$.",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 5, "bi",
        r"Use your graph to find the gradient of the line.",
        1, "Linear Functions — Gradient", 20, (19, 0.22, 0.35),
        r"Gradient $= -2$", "A1",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 5, "bii",
        r"Find the $y$-intercept.",
        1, "Linear Functions — Intercept", 20, (19, 0.35, 0.45),
        r"$y$-intercept $= 6$", "A1",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 5, "biii",
        r"Find the equation of the line in the form of $y = mx + c$.",
        1, "Linear Functions — Equation", 20, (19, 0.45, 0.55),
        r"$y = -2x + 6$", "A1",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 5, "ci",
        r"The points $(-1.5, p)$ and $(q, 1)$ lie on the graph in (a). From your graph, find the value of $p$.",
        1, "Linear Functions — Reading Graph", 20, (19, 0.55, 0.68),
        r"$p = 9$", "A1",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 5, "cii",
        r"Find the value of $q$.",
        1, "Linear Functions — Reading Graph", 20, (19, 0.68, 0.92),
        r"$q = 2.5$", "A1",
        topic_id=6)

    # P2 Q6 — Page 21 (idx 21)
    add_q(db, p2.id, exam_dir, 2, 6, "ai",
        r"What fraction of the pile of books can Mrs Yap finish marking in 1 hour?",
        1, "Rate — Fraction of Work", 22, (21, 0.04, 0.20),
        r"$\dfrac{1}{5}$", "A1",
        stem=r"Mrs Yap and Mrs Chin estimate that they will take 5 hours and 6 hours respectively to finish marking the same pile of books individually. If they mark the same pile of books together, the estimated time taken is $x$ hours.",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 6, "aii",
        r"What fraction of the pile of books can Mrs Chin finish marking in 1 hour?",
        1, "Rate — Fraction of Work", 22, (21, 0.20, 0.33),
        r"$\dfrac{1}{6}$", "A1",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 6, "aiii",
        r"What fraction of the same pile of books can both of them finish marking in 1 hour if they mark together?",
        1, "Rate — Combined Work", 22, (21, 0.33, 0.50),
        r"$\dfrac{1}{x}$", "A1",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 6, "b",
        r"Hence, form an equation in terms of $x$ and solve for the unknown.",
        2, "Linear Equations — Work Rate", 22, (21, 0.50, 0.92),
        r"""$$\frac{1}{5} + \frac{1}{6} = \frac{1}{x}$$
$$\frac{11}{30} = \frac{1}{x}$$
$$x = \frac{30}{11} = 2\frac{8}{11} \text{ hours}$$""",
        "M1, A1",
        topic_id=5)

    # P2 Q7 — Page 22 (idx 22)
    add_q(db, p2.id, exam_dir, 2, 7, "a",
        r"Find the volume of water in the pool to the nearest cubic metre.",
        3, "Volume — Trapezium Prism", 23, (22, 0.04, 0.40),
        r"""Height $= 1.75 - 1 = 0.75$ m
Volume of water $= \frac{1}{2} \times (1 + 3 - 0.75) \times 100 \times 40$
$= \frac{1}{2}(1 + 3 - 0.75)(100)(40) = 162.5 \times 40 = 6500$ m$^3$""",
        "M1 for height, M1 for formula, A1",
        stem=r"The swimming pool is 100 m long and 40 m wide. The bottom of the pool slopes uniformly throughout the length of the pool. It is 1.75 m deep at the shallow end and 3 m deep at the deep end. The depth of water at the shallow end is 1 m.",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 7, "b",
        r"How much more water must be poured into the pool to fill it completely?",
        2, "Volume — Subtraction", 23, (22, 0.40, 0.60),
        r"""Volume of water to be poured $= 100 \times 40 \times 0.75 = 3000$ m$^3$""",
        "M1, A1",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 7, "c",
        r"It takes 30 seconds to drain 10 m$^3$ of water. Find the total time, in hours and minutes, needed to drain a fully filled pool.",
        3, "Speed, Distance, Time", 23, (22, 0.60, 0.92),
        r"""Total volume of fully filled pool $= 3000 + 6500 = 9500$ m$^3$
Time taken to drain $= \frac{9500}{10} \times 30 = 28500$ seconds
$= 7$ h $55$ min""",
        "M1 for total volume, M1 for time, A1",
        topic_id=9)

    # P2 Q8 — Pages 23-24 (idx 23-24)
    add_q(db, p2.id, exam_dir, 2, 8, "a",
        r"Calculate the percentage drop in price per kilogram from May to June 2021.",
        2, "Percentage — Decrease", 24, (23, 0.04, 0.28),
        r"$$\frac{30 - 24}{30} \times 100\% = 20\%$$", "M1, A1",
        stem=r"In June 2021, prices of durians in Singapore dropped significantly. Prices of durians were at $\$30$ per kilogram in May 2021, but it dropped to $\$24$ per kilogram in June 2021.",
        topic_id=8)

    add_q(db, p2.id, exam_dir, 2, 8, "bi",
        r"Durian vendor Mr Lim imported 1000 kg of durians from Malaysia each day. Assuming that all 1000 kg of durians were sold each day, calculate the difference in earnings per day after the drop in prices.",
        2, "Percentage — Applied", 24, (23, 0.28, 0.50),
        r"""Difference in price per kg $= \$30 - \$24 = \$6$
Difference in earning $= 1000 \times 6 = \$6000$""",
        "M1, A1",
        topic_id=8)

    add_q(db, p2.id, exam_dir, 2, 8, "bii",
        r"Find the cost price per kilogram of durians given that Mr Lim still made a profit of $\$3880$ daily after the drop in prices.",
        2, "Percentage — Cost Price", 24, (23, 0.50, 0.75),
        r"""Profit per kg $= 3880 \div 1000 = \$3.88$
Cost price per kg $= \$24 - \$3.88 = \$20.12$""",
        "M1, A1",
        topic_id=8)

    add_q(db, p2.id, exam_dir, 2, 8, "c",
        r"In July 2021, Mr Lim decided to carry out the following promotion: For every 5 kg sold at $\$24$ per kilogram, customer will get 1 kg worth of durians FREE! Determine if Mr Lim will make a loss or a profit daily if he sold 1000 kg of durians with all his customers maximising the deal and calculate the daily profit or loss with this promotion.",
        4, "Percentage — Profit/Loss", 25, (24, 0.04, 0.92),
        r"""6 kg for $\$5 \times 24 = \$120$
Only 166 customers ($166 \times 6$ kg $= 996$ kg) can get 6 kg by maximising the deal. There will be another 4 kg.
996 kg: $(996/6) \times 120 = \$19920$
Other 4 kg: $\$24 \times 4 = \$96$
Total selling price $= 19920 + 96 = \$20016$
Total cost $= 1000 \times 20.12 = \$20120$
Total daily loss $= 20120 - 20016 = \$104$
He will make a daily loss.""",
        "M1 for revenue, M1 for cost, M1 for comparison, A1",
        topic_id=8)

    db.commit()
    p1_count = len(p1.questions)
    p2_count = len(p2.questions)
    print(f"Seeded Bendemeer exam id={exam.id}: Paper 1 ({p1_count} parts), Paper 2 ({p2_count} parts)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
