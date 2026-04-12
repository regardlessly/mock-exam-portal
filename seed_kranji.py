"""Seed Kranji Secondary School EOY 2022 Sec 1 Express Math exam."""

import os
import shutil
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/66b1f55db4548_5780.pdf"
IMAGES_DIR = "/tmp/kranji_pages"

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

    school = db.query(School).filter(School.name == "Kranji Secondary School").first()
    if not school:
        school = School(name="Kranji Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(Exam.school_id == school.id, Exam.year == 2022).first()
    if existing:
        print(f"Kranji 2022 already seeded (id={existing.id}). Deleting and re-seeding.")
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
        source_pdf="66b1f55db4548_5780.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # PAPER 1 — Pages 3-14 (idx 2-13), 50 marks, 1h15m
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=75, total_marks=50,
               date=date(2022, 9, 26), instructions="Answer all questions.")
    db.add(p1); db.flush()

    # Q1 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 1, None,
        r"The diagram is taken from an advertisement of a bicycle manufacturer. It claims that the number of bicycles produced had doubled between 2010 and 2020. Explain briefly why the advertisement might be misleading.",
        1, "Data Representation", 3, (2, 0.04, 0.35),
        r"The diagram shown should be the same size as the number of bicycles produced has doubled and not the size of the bicycle. Or 2020 should show 2 bicycles of the same size instead of a bigger bicycle. Or the number of bicycles is represented by a bicycle with no values. It is difficult to determine the number of bicycles have doubled from the size.", "B1",
        topic_id=14)

    # Q2 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 2, None,
        r"It is given that $T = \dfrac{m(n + 4)}{6 - n}$. Calculate the value of $T$ when $m = 17.348$ and $n = 2.14$. Write your answer correct to two decimal places.",
        2, "Algebraic Substitution", 3, (2, 0.35, 0.60),
        r"$$T = \frac{17.348(2.14 + 4)}{6 - 2.14} = \frac{17.348 \times 6.14}{3.86} = 27.5950 \approx 27.60$$", "M1, A1",
        topic_id=4)

    # Q3 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 3, None,
        r"By writing each number correct to 1 significant figure, estimate the value of $\dfrac{\sqrt{49.8} \times 7.9}{3.5}$.",
        2, "Estimation", 3, (2, 0.60, 0.92),
        r"$$\approx \frac{\sqrt{50} \times 8}{4} = \frac{7.07 \times 8}{4} \approx \frac{56}{4} = 14$$ Accept: $\frac{7 \times 8}{4} = 14$", "M1, A1",
        topic_id=3)

    # Q4 — Page 4 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 4, None,
        r"The Residents' Committee plans to distribute 126 pencil boxes, 252 pens and 189 books equally, without any leftover, to the needy students in the neighbourhood. Find the largest possible number of students who will receive the gifts.",
        2, "HCF", 4, (3, 0.04, 0.24),
        r"$$126 = 2 \times 3^2 \times 7, \quad 252 = 2^2 \times 3^2 \times 7, \quad 189 = 3^3 \times 7$$ $$\text{HCF} = 3^2 \times 7 = 63$$", "M1, A1",
        topic_id=1)

    # Q5 — Page 4 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 5, "a",
        r"Express $22\dfrac{3}{4}\%$ as a fraction in its simplest form.",
        1, "Percentage to Fraction", 4, (3, 0.24, 0.50),
        r"$22\dfrac{3}{4}\% = \dfrac{91}{400}$", "B1",
        topic_id=8)

    add_q(db, p1.id, exam_dir, 1, 5, "b",
        r"Express 14 g as a percentage of 8 kg.",
        2, "Percentage", 4, (3, 0.50, 0.92),
        r"$$\frac{14}{8000} \times 100\% = 0.175\%$$", "M1, A1",
        topic_id=8)

    # Q6 — Page 5 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 6, "a",
        r"In the pentagon $PQRST$, angle $QPT = 160°$ and angle $PQR = 80°$. Calculate the value of $x$.",
        3, "Polygon — Interior Angles", 5, (4, 0.04, 0.68),
        r"Sum of interior angles of a pentagon $= (5 - 2) \times 180° = 540°$ $$x + x + 28 + 2x + 160 + 80 = 540$$ $$4x = 540 - 268 = 272$$ $$x = 68$$", "M1 for angle sum, M1 for equation, A1",
        topic_id=11)

    add_q(db, p1.id, exam_dir, 1, 6, "b",
        r"Each exterior angle of a regular polygon is $18°$. Find the number of sides of the polygon.",
        1, "Polygon — Exterior Angles", 5, (4, 0.68, 0.92),
        r"Number of sides $= \dfrac{360°}{18°} = 20$", "B1",
        topic_id=11)

    # Q7 — Pages 6-7 (idx 5-6)
    add_q(db, p1.id, exam_dir, 1, 7, "a",
        r"State the coordinates of the point $A$.",
        1, "Coordinate Geometry", 6, (5, 0.04, 0.58),
        r"$A(5, 5)$", "B1",
        stem=r"The diagram shows a cartesian plane with points $A$, $B$ and $C$.",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 7, "b",
        r"Find the gradient of the straight line that joins $A$ and $B$.",
        1, "Linear Functions — Gradient", 6, (5, 0.58, 0.92),
        r"Gradient $= \dfrac{5 - 2}{5 - (-1)} = \dfrac{3}{6} = \dfrac{1}{2}$ or $0.5$", "B1",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 7, "c",
        r"Plot and label a possible point $D$ on the above grid such that $ABCD$ is a parallelogram.",
        1, "Coordinate Geometry — Parallelogram", 7, (6, 0.04, 0.35),
        r"On the diagram, $D(3, 2)$ or equivalent valid point.", "B1",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 7, "d",
        r"Hence, find the area of the parallelogram.",
        1, "Area — Parallelogram", 7, (6, 0.35, 0.60),
        r"Area $= 15$ sq units", "B1",
        topic_id=12)

    # Q8 — Page 8 (idx 7)
    add_q(db, p1.id, exam_dir, 1, 8, "a",
        r"Find the value of $x$.",
        2, "Pie Chart — Angles", 8, (7, 0.04, 0.50),
        r"$$x + 3x + 74 + 126 = 360$$ $$4x = 160$$ $$x = 40$$", "M1, A1",
        stem=r"A group of students were surveyed to determine how they travelled to school. Their choices are represented on a pie chart. Car: $x°$, Bus: $3x°$, Walk: $74°$, MRT: $126°$.",
        topic_id=14)

    add_q(db, p1.id, exam_dir, 1, 8, "b",
        r"Calculate the percentage of the students who travel to school by MRT.",
        2, "Pie Chart — Percentage", 8, (7, 0.50, 0.68),
        r"$$\frac{126}{360} \times 100\% = 35\%$$", "M1, A1",
        topic_id=14)

    add_q(db, p1.id, exam_dir, 1, 8, "c",
        r"If 204 students travel to school by bus, find the total number of students surveyed.",
        2, "Pie Chart — Total", 8, (7, 0.68, 0.92),
        r"$$\frac{204}{3x} \times 360 = \frac{204}{120} \times 360 = 612$$", "M1, A1",
        topic_id=14)

    # Q9 — Page 9 (idx 8)
    add_q(db, p1.id, exam_dir, 1, 9, "a",
        r"If the total bill was $\$1534$, write down an equation in terms of $x$.",
        1, "Linear Equations — Forming", 9, (8, 0.04, 0.38),
        r"$32x + 2x(43) = 1534$ or equivalently $32x + 86x = 1534$", "B1",
        stem=r"Ahmad bought several thumb-drives at $\$32$ each and twice as many calculators as the thumb-drives at $\$43$ each. Let $x$ be the number of thumb-drives purchased.",
        topic_id=5)

    add_q(db, p1.id, exam_dir, 1, 9, "b",
        r"Hence, find the total number of calculators purchased.",
        3, "Linear Equations — Solving", 9, (8, 0.38, 0.92),
        r"$$32x + 2x(43) = 1534$$ $$32x + 86x = 1534$$ $$118x = 1534$$ $$x = 13$$ No. of calculators $= 2x = 26$", "M1 for equation, M1 for solving, A1",
        topic_id=5)

    # Q10 — Page 10 (idx 9)
    add_q(db, p1.id, exam_dir, 1, 10, "a",
        r"Find the difference between the highest and lowest temperature.",
        2, "Negative Numbers", 10, (9, 0.04, 0.46),
        r"Highest $= 0.4$, Lowest $= -2.1$. Difference $= 0.4 - (-2.1) = 2.5°$C", "M1, A1",
        stem=r"The following readings, in $°$C, are the temperatures of several freezers recorded by health officers in a food court: $-1.6, \ -0.5, \ 0.2, \ -2.1, \ -1.5, \ -0.7, \ 0.4, \ -1.2$",
        topic_id=2)

    add_q(db, p1.id, exam_dir, 1, 10, "b",
        r"Using this information, calculate the average temperature of the freezers.",
        2, "Average / Mean", 10, (9, 0.46, 0.92),
        r"$$\text{Average} = \frac{-1.6 + (-0.5) + 0.2 + (-2.1) + (-1.5) + (-0.7) + 0.4 + (-1.2)}{8} = \frac{-7.0}{8} = -0.875°\text{C}$$", "M1, A1",
        topic_id=14)

    # Q11 — Page 11 (idx 10)
    add_q(db, p1.id, exam_dir, 1, 11, "a",
        r"Tim can paint 8 fence panels in 5 hours. Paul can paint 3 fence panels in 2 hours. Tim and Paul work together to paint a total of 18 panels. Assuming they continue to paint at the same rate, how long will it take them to paint the 18 panels? Give your answer in hours and minutes, to the nearest minute.",
        3, "Rate of Work", 11, (10, 0.04, 0.50),
        r"In 1 hour, Tim paints $\frac{8}{5}$ panels. In 1 hour, Paul paints $\frac{3}{2}$ panels. In 1 hour, both paint $\frac{8}{5} + \frac{3}{2} = \frac{31}{10}$ panels. Time taken to paint 18 panels $= \frac{18}{\frac{31}{10}} = \frac{180}{31} \approx 5$ h $48$ min", "M1 for combined rate, M1 for time, A1",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 11, "b",
        r"If $P$ is decreased by 20% and then increased by 40%, find the percentage change in $P$.",
        2, "Percentage Change", 11, (10, 0.50, 0.92),
        r"New $P = 0.8P \times 1.40 = 1.12P$. Percentage change in $P = \dfrac{1.12P - P}{P} \times 100\% = 12\%$ increase", "M1, A1",
        topic_id=8)

    # Q12 — Page 12 (idx 11)
    add_q(db, p1.id, exam_dir, 1, 12, "a",
        r"What is the average speed of the deer in m/s?",
        2, "Speed Conversion", 12, (11, 0.04, 0.46),
        r"$$78 \text{ km/h} = \frac{78 \times 1000}{60 \times 60} = \frac{78000}{3600} = 21.7 \text{ m/s (3 s.f.)}$$", "M1, A1",
        stem=r"A deer can run at an average speed of 78 km/h.",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 12, "b",
        r"How many seconds will the deer take to run a distance of 980 meters?",
        2, "Speed, Distance, Time", 12, (11, 0.46, 0.92),
        r"$$\text{Time} = \frac{980}{21.67} = 45.2 \text{ s (3 s.f.)}$$", "M1, A1",
        topic_id=9)

    # Q13 — Page 13 (idx 12)
    add_q(db, p1.id, exam_dir, 1, 13, "a",
        r"Write down the sixth line in the pattern.",
        1, "Number Patterns", 13, (12, 0.04, 0.45),
        r"$1 + 3 + 5 + 7 + 9 + 11 + 13 = 49 = 7 \times 7$", "B1",
        stem=r"Consider the number pattern: 1st line: $1 + 3 = 4 = 2 \times 2$; 2nd line: $1 + 3 + 5 = 9 = 3 \times 3$; 3rd line: $1 + 3 + 5 + 7 = 16 = 4 \times 4$; 4th line: $1 + 3 + 5 + 7 + 9 = 25 = 5 \times 5$.",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 13, "b",
        r"Find an expression, in terms of $n$, for the $n$th line.",
        1, "Number Patterns — General Term", 13, (12, 0.45, 0.63),
        r"$T_n = (n + 1)^2$", "B1",
        topic_id=7)

    add_q(db, p1.id, exam_dir, 1, 13, "c",
        r"Would there be a line with 1000 in column 2? Explain your answer.",
        2, "Number Patterns — Reasoning", 13, (12, 0.63, 0.92),
        r"No because 1000 is not a perfect square/square number. OR $(n + 1)^2 = 1000$, $n = \sqrt{1000} - 1 \approx 30.6$. Since $n$ is not a positive integer, 1000 is not a term in the pattern.", "M1, A1",
        topic_id=7)

    # Q14 — Page 14 (idx 13)
    add_q(db, p1.id, exam_dir, 1, 14, "a",
        r"Construct a quadrilateral $WXYZ$ where $XY = 7.9$ cm, $WZ = 10.2$ cm, $\angle WXY = 112°$ and $\angle ZWX = 68°$. $WX$ has already been drawn for you.",
        3, "Construction", 14, (13, 0.04, 0.65),
        r"Quadrilateral $WXYZ$ constructed with correct measurements.", "B1 for each angle, B1 for $XY$",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 14, "b",
        r"What is the special name of the quadrilateral $WXYZ$?",
        1, "Quadrilateral Properties", 14, (13, 0.65, 0.78),
        r"Trapezium", "B1",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 14, "c",
        r"Measure and write down the length of the diagonal $WY$.",
        1, "Construction — Measurement", 14, (13, 0.78, 0.92),
        r"$WY = 13.7 \pm 0.1$ cm (13.6 to 13.8)", "B1",
        topic_id=10)

    # ══════════════════════════════════════════════
    # PAPER 2 — Pages 16-26 (idx 15-25), 50 marks, 1h15m
    # ══════════════════════════════════════════════
    p2 = Paper(exam_id=exam.id, paper_number=2, duration_minutes=75, total_marks=50,
               date=date(2022, 9, 28), instructions="Answer all questions.")
    db.add(p2); db.flush()

    # P2 Q1 — Page 16 (idx 15)
    add_q(db, p2.id, exam_dir, 2, 1, "a",
        r"Write the following numbers in order of size, starting with the smallest: $0.2$, $\pi$, $\sqrt{27}$, $3\dfrac{5}{8}$, $(-0.2)^5$.",
        1, "Number Ordering", 16, (15, 0.04, 0.30),
        r"$(-0.2)^5$, $0.2$, $\pi$, $3\dfrac{5}{8}$, $\sqrt{27}$", "B1",
        topic_id=2)

    add_q(db, p2.id, exam_dir, 2, 1, "bi",
        r"Express 336 as a product of its prime factors.",
        1, "Prime Factorisation", 16, (15, 0.30, 0.53),
        r"$336 = 2^4 \times 3 \times 7$", "B1",
        stem=r"Written as the product of its prime factors $2520 = 2^3 \times 3^2 \times 5 \times 7$.",
        topic_id=1)

    add_q(db, p2.id, exam_dir, 2, 1, "bii",
        r"The number $2520k$ is a perfect square. Find the smallest positive integer value of $k$.",
        1, "Perfect Square", 16, (15, 0.53, 0.72),
        r"$2520 = 2^3 \times 3^2 \times 5 \times 7$. For perfect square, all powers must be even. $k = 2 \times 5 \times 7 = 70$", "B1",
        topic_id=1)

    add_q(db, p2.id, exam_dir, 2, 1, "biii",
        r"Find the smallest positive integer $h$ for which $336h$ is a multiple of 2520.",
        1, "LCM", 16, (15, 0.72, 0.92),
        r"$\text{LCM}(336, 2520) = 2520$. $h = \frac{2520}{336} = 7.5$, so $h = 15$ (since $336 = 2^4 \times 3 \times 7$ and $2520 = 2^3 \times 3^2 \times 5 \times 7$, need $h$ to supply $3 \times 5 = 15$).", "B1",
        topic_id=1)

    # P2 Q2 — Page 17 (idx 16)
    add_q(db, p2.id, exam_dir, 2, 2, None,
        r"In the diagram given below, $PQ$ and $RS$ are parallel and $BDE$ is a straight line. Find $x$, $y$ and $z$ giving reasons for each answer.",
        5, "Angle Properties — Parallel Lines", 17, (16, 0.04, 0.92),
        r"""$\angle FBD = 180° - 78° - 51° = 51°$ (angles in triangle $ABF$)
$y = 180° - 51° - 51° = 78°$ (angles on straight line at $B$) or alternate angles
$z = 180° - 126° = 54°$ (co-interior angles, $PQ \parallel RS$)
$x = 180° - 78° - 54° = 48°$ (angles in triangle $BDC$) or equivalent reasoning""",
        "B1 for each of $x$, $y$, $z$ with reason, M1 for method, A1",
        topic_id=10)

    # P2 Q3 — Page 18 (idx 17)
    add_q(db, p2.id, exam_dir, 2, 3, "ai",
        r"The product of $2xy$ and $5y$.",
        1, "Algebraic Expressions", 18, (17, 0.04, 0.22),
        r"$2xy \times 5y = 10xy^2$", "B1",
        stem=r"Write and simplify the algebraic expression for each of the following statements.",
        topic_id=4)

    add_q(db, p2.id, exam_dir, 2, 3, "aii",
        r"Subtract the square root of $p$ from the cube of $q$.",
        1, "Algebraic Expressions", 18, (17, 0.22, 0.37),
        r"$q^3 - \sqrt{p}$", "B1",
        topic_id=4)

    add_q(db, p2.id, exam_dir, 2, 3, "bi",
        r"Factorise completely $28x - 16y + 8$.",
        1, "Factorisation", 18, (17, 0.37, 0.57),
        r"$4(7x - 4y + 2)$", "B1",
        topic_id=4)

    add_q(db, p2.id, exam_dir, 2, 3, "bii",
        r"Factorise completely $-9p^2 - 72pq$.",
        1, "Factorisation", 18, (17, 0.57, 0.92),
        r"$-9p(p + 8q)$", "B1",
        topic_id=4)

    # P2 Q4 — Page 19 (idx 18)
    add_q(db, p2.id, exam_dir, 2, 4, "a",
        r"Express $18000 \text{ cm}^3$ in $\text{m}^3$.",
        2, "Unit Conversion", 19, (18, 0.04, 0.22),
        r"$18000 \text{ cm}^3 = \frac{18000}{100^3} = 0.018 \text{ m}^3$", "M1, A1",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 4, "b",
        r"$ABCD$ is a rectangle of length 68 cm and breadth 24 cm. $M$ is the midpoint of semicircular arc $AMD$. $BMC$ is a triangle. Find the area of the shaded region.",
        4, "Area — Composite Shapes", 19, (18, 0.22, 0.92),
        r"""Area of rectangle $= 68 \times 24 = 1632$ cm$^2$
Radius of semicircle $= \frac{24}{2} = 12$ cm
Area of semicircle $= \frac{1}{2}\pi(12)^2 = 72\pi$ cm$^2$
Area of triangle $BMC = \frac{1}{2} \times 68 \times 12 = 408$ cm$^2$
Shaded area $= 1632 - 72\pi - 408 = 1224 - 72\pi \approx 997.8$ cm$^2$ (or $= 1632 - 72\pi - 408$)""",
        "M1 for semicircle, M1 for triangle, M1 for subtraction, A1",
        topic_id=12)

    # P2 Q5 — Page 20 (idx 19)
    add_q(db, p2.id, exam_dir, 2, 5, "a",
        r"Find the ratio of blue marbles to green marbles that he has in its simplest form.",
        2, "Ratio", 20, (19, 0.04, 0.42),
        r"Red : Blue $= 3 : 4$, Red : Green $= 4 : 5$. Common red $= 12$. Blue $= 16$, Green $= 15$. Blue : Green $= 16 : 15$", "M1, A1",
        stem=r"Bill has some red marbles, blue marbles and green marbles. The ratio of red marbles to blue marbles that he has is $3 : 4$ and the ratio of red marbles to green marbles that he has is $4 : 5$.",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 5, "b",
        r"Calculate the total number of marbles that Bill has.",
        2, "Ratio — Word Problem", 20, (19, 0.42, 0.92),
        r"After exchanging 5 blue and 2 green for red: Red $= 12k + 7$, Blue $= 16k - 5$, Green $= 15k - 2$. Equal: $12k + 7 = 16k - 5 \implies k = 3$. Total $= (12 + 16 + 15) \times 3 = 129$ marbles", "M1, A1",
        stem=r"After Bill exchanged 5 blue marbles and 2 green marbles with a friend for red marbles, he will have equal number of red, blue and green marbles.",
        topic_id=9)

    # P2 Q6 — Page 21 (idx 20)
    add_q(db, p2.id, exam_dir, 2, 6, "a",
        r"Expand and simplify $5(p + 3q) - 2(3p - q)$.",
        2, "Algebra — Expansion", 21, (20, 0.04, 0.22),
        r"$$5p + 15q - 6p + 2q = -p + 17q$$", "M1, A1",
        topic_id=4)

    add_q(db, p2.id, exam_dir, 2, 6, "b",
        r"Solve the equation $3(a - 4) - 2 = 5 - a$.",
        2, "Solving Linear Equations", 21, (20, 0.22, 0.45),
        r"$$3a - 12 - 2 = 5 - a$$ $$4a = 19$$ $$a = 4.75$$", "M1, A1",
        topic_id=5)

    add_q(db, p2.id, exam_dir, 2, 6, "c",
        r"Express $\dfrac{3y - 6x}{4} + \dfrac{8x + y}{5}$ as a single fraction in its simplest form.",
        3, "Algebraic Fractions", 21, (20, 0.45, 0.92),
        r"$$= \frac{5(3y - 6x) + 4(8x + y)}{20} = \frac{15y - 30x + 32x + 4y}{20} = \frac{2x + 19y}{20}$$", "M1 for LCD, M1 for expanding, A1",
        topic_id=4)

    # P2 Q7 — Pages 22-23 (idx 21-22)
    add_q(db, p2.id, exam_dir, 2, 7, "a",
        r"Calculate the radius of the cylindrical drum.",
        2, "Volume — Cylinder", 22, (21, 0.04, 0.28),
        r"$$\pi r^2 \times 0.85 = 0.255$$ $$r^2 = \frac{0.255}{0.85\pi} = 0.09549$$ $$r \approx 0.309 \text{ m}$$", "M1, A1",
        stem=r"In a factory, liquid waste is poured into cylindrical drums. The volume of the cylindrical drum is 0.255 m$^3$ and its height is 0.85 m.",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 7, "bi",
        r"the area of trapezium $ABCD$.",
        1, "Area — Trapezium", 22, (21, 0.28, 0.92),
        r"$$\text{Area} = \frac{1}{2}(5.5 + 3.5) \times 1.8 = \frac{1}{2} \times 9 \times 1.8 = 8.1 \text{ m}^2$$", "B1",
        stem=r"When full, the drums are emptied into a tank. $DC \parallel AB$, $EF \parallel HG$, $AB = EF = 5.5$ m, $DC = HG = 3.5$ m, $AE = BF = CG = DH = 2.1$ m and the perpendicular height of the tank is 1.8 m.",
        topic_id=12)

    add_q(db, p2.id, exam_dir, 2, 7, "bii",
        r"the volume of the tank.",
        1, "Volume — Prism", 23, (22, 0.04, 0.35),
        r"$$V = \text{Area of trapezium} \times \text{length} = 8.1 \times 2.1 = 17.01 \text{ m}^3$$", "B1",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 7, "c",
        r"How many full drums of waste can be emptied into the tank?",
        2, "Volume — Division", 23, (22, 0.35, 0.70),
        r"$$\frac{17.01}{0.255} = 66.7$$ 66 full drums can be emptied into the tank.", "M1, A1",
        topic_id=13)

    # P2 Q8 — Page 24 (idx 23)
    add_q(db, p2.id, exam_dir, 2, 8, "a",
        r"Mr Heng decides to deposit $\$3000$ into a bank that pays simple interest at 1.45% per annum. After 3 years, he withdraws all the money from the bank. How much money did Mr Heng withdraw?",
        2, "Simple Interest", 24, (23, 0.04, 0.22),
        r"Interest $= \frac{3000 \times 1.45 \times 3}{100} = \$130.50$. Total withdrawn $= 3000 + 130.50 = \$3130.50$", "M1, A1",
        topic_id=8)

    add_q(db, p2.id, exam_dir, 2, 8, "bi",
        r"What is the total amount that Mr Heng pays for the laptop if he buys it on hire purchase?",
        2, "Hire Purchase", 24, (23, 0.22, 0.60),
        r"Deposit $= 0.15 \times 3198 = \$479.70$. Total $= 479.70 + 18 \times 158 = 479.70 + 2844 = \$3323.70$", "M1, A1",
        stem=r"Mr Heng saw an advertisement for a laptop. Cash Price: $\$3198.00$. Hire Purchase Terms: 15% deposit, 18 monthly payments of $\$158$.",
        topic_id=8)

    add_q(db, p2.id, exam_dir, 2, 8, "bii",
        r"Find the extra cost of buying the laptop on hire purchase as a percentage of the cash price.",
        3, "Percentage — Extra Cost", 24, (23, 0.60, 0.92),
        r"Extra cost $= 3323.70 - 3198 = \$125.70$. Percentage $= \dfrac{125.70}{3198} \times 100\% \approx 3.93\%$", "M1 for extra, M1 for percentage, A1",
        topic_id=8)

    # P2 Q9 — Pages 25-26 (idx 24-25)
    add_q(db, p2.id, exam_dir, 2, 9, "a",
        r"London is 7 hours behind Singapore and it takes 13 hours 58 minutes to reach London by air. If the aircraft leaves Singapore at 1:00 pm on Tuesday, state the time and the day it will reach London according to London's local time.",
        1, "Time Zones", 25, (24, 0.04, 0.25),
        r"Arrival Singapore time $= 1:00$ pm $+ 13$ h $58$ min $= 2:58$ am Wednesday. London time $= 2:58$ am $- 7$ h $= 7:58$ pm Tuesday", "B1",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 9, "bi",
        r"By comparing the exchange rates, explain how you can tell that the hotel in London costs more per night than the hotel in Italy.",
        2, "Currency Conversion", 25, (24, 0.25, 0.92),
        r"London: $\pounds 185 \times 1.65 = \$305.25$ per night. Italy: $\euro 185 \times 0.72$ gives $\$1 = \euro 0.72$, so $\euro 185 = \frac{185}{0.72} = \$256.94$ per night. Since $\$305.25 > \$256.94$, London costs more.", "M1, A1",
        stem=r"The exchange rate between Singapore dollars ($\$$) and euros ($\euro$) is $\$1 = \euro 0.72$. The exchange rate between pounds ($\pounds$) and Singapore dollars is $\pounds 1 = \$1.65$. London Hotel: $\pounds 185$ per night. Italy Hotel: $\euro 185$ per night.",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 9, "bii",
        r"Tom books 4 nights in a London hotel and 3 nights in the hotel in Italy. He pays using his credit card. The credit card company charges a fee of 2.8% for the currency conversion. Jerry will pay $\dfrac{2}{7}$ of the cost of the accommodation. Suggest a suitable amount for Tom to ask Jerry to pay in Singapore dollars. Justify the decision you make and show your calculations clearly.",
        4, "Currency / Percentage — Multi-step", 26, (25, 0.04, 0.75),
        r"""London: $4 \times 185 = \pounds 740 \to 740 \times 1.65 = \$1221$
Italy: $3 \times 185 = \euro 555 \to \frac{555}{0.72} = \$770.83$
Total in SGD $= 1221 + 770.83 = \$1991.83$
Credit card fee $= 1991.83 \times 1.028 = \$2047.60$
Jerry pays $= \frac{2}{7} \times 2047.60 = \$585.03$
Suggest $\$586$ (round up to nearest dollar)""",
        "M1 for London conversion, M1 for Italy conversion, M1 for credit card fee, A1",
        topic_id=9)

    db.commit()
    p1_count = len(p1.questions)
    p2_count = len(p2.questions)
    print(f"Seeded Kranji exam id={exam.id}: Paper 1 ({p1_count} parts), Paper 2 ({p2_count} parts)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
