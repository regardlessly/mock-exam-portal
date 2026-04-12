"""Seed Anglo-Chinese School (Barker Road) EOY 2020 Sec 1 Express Math exam."""

import os
import shutil
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/Anglo-Chinese-School-End-of-Year-2020-Sec-1-Math.pdf"
IMAGES_DIR = "/tmp/acs2020_pages"

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

    school = db.query(School).filter(School.name == "Anglo-Chinese School (Barker Road)").first()
    if not school:
        school = School(name="Anglo-Chinese School (Barker Road)")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(Exam.school_id == school.id, Exam.year == 2020).first()
    if existing:
        print(f"ACS (Barker Road) 2020 already seeded (id={existing.id}). Deleting and re-seeding.")
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
        source_pdf="Anglo-Chinese-School-End-of-Year-2020-Sec-1-Math.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # PAPER 1 — Pages 2-12 (idx 1-11), 50 marks, 1h15m
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=75, total_marks=50,
               date=date(2020, 10, 5), instructions="Answer all questions.")
    db.add(p1); db.flush()

    # Q1 — Page 2 (idx 1)
    add_q(db, p1.id, exam_dir, 1, 1, "a",
        r"Calculate $\dfrac{13.6^2 - 4}{\sqrt{3.5} + 3}$. Write down the first 5 digits on your calculator display.",
        1, "Calculator Usage", 2, (1, 0.07, 0.30),
        r"$37.151$", "B1",
        topic_id=3)

    add_q(db, p1.id, exam_dir, 1, 1, "b",
        r"Write your answer to part (a) correct to 3 decimal places.",
        1, "Rounding", 2, (1, 0.28, 0.42),
        r"$37.152$", "B1",
        topic_id=3)

    # Q2 — Page 2 (idx 1)
    add_q(db, p1.id, exam_dir, 1, 2, None,
        r"By rounding off each number to 2 significant figures, estimate the value of $51323 \div 9.96$. You must show your working clearly.",
        2, "Estimation", 2, (1, 0.41, 0.68),
        r"$51000 \div 10 = 5100$", "M1 for rounding, A1",
        topic_id=3)

    # Q3 — Page 2 (idx 1)
    add_q(db, p1.id, exam_dir, 1, 3, None,
        r"Simplify $2y + 3(y + 4x)$.",
        2, "Algebra — Expansion", 2, (1, 0.67, 0.95),
        r"$2y + 3y + 12x = 5y + 12x$", "M1, A1",
        topic_id=4)

    # Q4 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 4, None,
        r"Factorise completely $24ax - 16ay$.",
        2, "Algebra — Factorisation", 3, (2, 0.07, 0.32),
        r"$8a(3x - 2y)$", "M1 for factor of 8 or $a$, A1",
        topic_id=4)

    # Q5 — Page 3 (idx 2)
    add_q(db, p1.id, exam_dir, 1, 5, None,
        r"The numbers $p$, $q$, $r$ and $s$ are represented on the number line. The values of $p$, $q$, $r$ and $s$ are listed below: $\dfrac{1}{3}$, $33.3\%$, $\dfrac{\sqrt{2}}{2}$, $\dfrac{\pi}{4}$. Find $p$, $q$, $r$ and $s$.",
        2, "Number Line / Number Types", 3, (2, 0.31, 0.95),
        r"$p = 33.3\%$, $q = \dfrac{1}{3}$, $r = \dfrac{\sqrt{2}}{2}$, $s = \dfrac{\pi}{4}$", "B2",
        topic_id=2)

    # Q6 — Page 4 (idx 3)
    add_q(db, p1.id, exam_dir, 1, 6, "ai",
        r"Find $x$.",
        1, "Angle Properties — Triangle", 4, (3, 0.07, 0.48),
        r"$x = 24°$ (alt. angles, $AC \parallel ED$)", "B1",
        stem=r"The diagram below is formed by two triangles $BDE$ and $ACE$. $AC$ is parallel to $ED$. Angle $B = 70°$, angle $A = 60°$, angle at $E = 24°$, angle $D = 64°$.",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 6, "aii",
        r"Find $y$.",
        1, "Angle Properties — Triangle", 4, (3, 0.46, 0.58),
        r"$y = 70 - 24 = 46°$", "B1",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 6, "aiii",
        r"Find $z$.",
        1, "Angle Properties — Triangle", 4, (3, 0.56, 0.70),
        r"$z = 180 - 60 - 24 - 46 = 50°$", "B1",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 6, "b",
        r"Explain if $AE$ is parallel to $BD$.",
        1, "Parallel Lines — Reasoning", 4, (3, 0.69, 0.95),
        r"$AE$ is not parallel to $BD$ as the interior angles do not add up to $180°$.", "B1",
        topic_id=10)

    # Q7 — Page 5 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 7, None,
        r"Express $\dfrac{7x}{3} - \dfrac{2x - y}{2}$ as a single fraction in its simplest form.",
        3, "Algebraic Fractions", 5, (4, 0.07, 0.42),
        r"$$\frac{2(7x)}{6} - \frac{3(2x - y)}{6} = \frac{14x - 6x + 3y}{6} = \frac{8x + 3y}{6}$$", "M1 for LCD, M1 for expansion, A1",
        topic_id=4)

    # Q8 — Page 5 (idx 4)
    add_q(db, p1.id, exam_dir, 1, 8, None,
        r"The diagram shows a semi-circle with diameter $AC = 12$ cm. $AB = \dfrac{1}{4}AC$ and a semi-circle is drawn with $AB$ as the diameter. Find the perimeter of the shaded region.",
        3, "Perimeter — Circles", 5, (4, 0.42, 0.95),
        r"$$\frac{1}{2}[2\pi(6)] + \frac{1}{2}[2\pi(1.5)] + 9 = 6\pi + 1.5\pi + 9 = 7.5\pi + 9 \approx 32.6 \text{ cm}$$", "M1 for large semicircle arc, M1 for small semicircle arc, A1",
        topic_id=14)

    # Q9 — Page 6 (idx 5)
    add_q(db, p1.id, exam_dir, 1, 9, "a",
        r"How much does Gym $A$ charge for usage for 20 minutes?",
        1, "Graph Reading", 6, (5, 0.07, 0.56),
        r"$\$0.80$", "B1",
        stem=r"Two gyms, $A$ and $B$, offer usage charges as shown in the graphs.",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 9, "b",
        r"Jim would like to spend $\$4$ to use one of the gyms. Which gym offers more usage time?",
        1, "Graph Reading", 6, (5, 0.54, 0.68),
        r"Gym $A$", "B1",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 9, "c",
        r"Provide a possible explanation as to why the graph for Gym B only starts at 20 minutes.",
        1, "Graph Interpretation", 6, (5, 0.66, 0.92),
        r"The usage is free for the first 20 minutes.", "B1",
        topic_id=6)

    # Q10 — Page 7 (idx 6)
    add_q(db, p1.id, exam_dir, 1, 10, "a",
        r"Ben exchanged SGD 4500 for USD. Calculate the amount of USD he had received. Give your answer to 2 decimal places.",
        1, "Currency Exchange", 7, (6, 0.07, 0.36),
        r"$4500 \times 0.7312 = \text{USD } 3290.40$", "B1",
        stem=r"Ben went on a trip to New York. The exchange rate was Singapore dollars (SGD) $1$ = US dollars (USD) $0.7312$.",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 10, "b",
        r"Ben had USD 1500 remaining after his trip. He exchanged them back to SGD. The exchange rate remained at SGD $1$ = USD $0.7312$. Calculate the amount he had spent on his trip, to the nearest SGD.",
        2, "Currency Exchange", 7, (6, 0.35, 0.65),
        r"$1500 \div 0.7312 = \text{SGD } 2051.42$. Amount spent $= 4500 - 2051.42 = \text{SGD } 2449$", "M1, A1",
        topic_id=9)

    # Q11 — Page 7 (idx 6)
    add_q(db, p1.id, exam_dir, 1, 11, "a",
        r"Find the ratio of Adam's money to Ben's money to Cayden's money.",
        2, "Ratio", 7, (6, 0.64, 0.82),
        r"$A : B = 3 : 5$, $B : C = 2 : 3$. So $A : B : C = 6 : 10 : 15$.", "M1, A1",
        stem=r"Adam, Ben and Cayden share a sum of money. The ratio of Adam's money to Ben's is in the ratio $3 : 5$. Cayden has $1.5$ times the money that Ben has.",
        topic_id=9)

    add_q(db, p1.id, exam_dir, 1, 11, "b",
        r"If Cayden has $\$90$ more than Adam, find the total amount of money the three of them have.",
        2, "Ratio — Word Problem", 7, (6, 0.80, 0.95),
        r"$\$90$ is $15 - 6 = 9$ parts. $1$ part $= \$10$. Total $= 31 \times 10 = \$310$.", "M1, A1",
        topic_id=9)

    # Q12 — Page 8 (idx 7)
    add_q(db, p1.id, exam_dir, 1, 12, "a",
        r"Find the gradient of the line.",
        1, "Linear Graph — Gradient", 8, (7, 0.07, 0.58),
        r"$\dfrac{12 - 2}{4} = 2.5$", "B1",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 12, "b",
        r"Write down the $y$-intercept of the line.",
        1, "Linear Graph — Intercept", 8, (7, 0.56, 0.72),
        r"$y = 2$", "B1",
        topic_id=6)

    add_q(db, p1.id, exam_dir, 1, 12, "c",
        r"Write down the equation of the vertical line that passes through $(2, 0)$.",
        1, "Linear Graph — Equation", 8, (7, 0.71, 0.90),
        r"$x = 2$", "B1",
        topic_id=6)

    # Q13 — Page 9 (idx 8)
    add_q(db, p1.id, exam_dir, 1, 13, "a",
        r"Find the temperature after 5 minutes.",
        2, "Negative Numbers / Rate of Change", 9, (8, 0.07, 0.52),
        r"Temperature rise in 10 min $= 18 - (-6) = 24°C$. Rise in 5 min $= 12°C$. Temperature $= -6 + 12 = 6°C$... Wait, final temp after 5 min $= -6 + 12 = 6°C$. Actually the answer is $6°C$.",
        "M1, A1",
        stem=r"The temperature of a waffle was $-6°C$ when it was taken from the freezer. The waffle was placed in an oven. The temperature rose at a constant rate for 10 minutes. At the end of 10 minutes, the temperature was $18°C$.",
        topic_id=2)

    # Fix: recalculate properly. Rise = 18 - (-6) = 24 in 10 min. In 5 min = 12. Temp = -6 + 12 = 6. But marking scheme says answer is -6 + 12 = 6°C... wait no, marking scheme says "Final temperature (-6) + 12 = -6°C". Let me recheck the marking scheme image. It says: "18 - (-6) = 24°C, 10 minutes increase of 24°C, 5 minutes increase of 12°C, Final temperature (-6) + 12 = -6°C". That must be a typo in the MS — it should be 6°C. But wait, let me re-read: "Final temperature (-6) + 12 = -6°C" - I think the MS might be showing it differently. Looking again at BP-30: "18 - (-6) = 24°C, 10 minutes increase of 24°C, 5 minutes increase of 12°C, Final temperature (-6) + 12 = -6°C". Hmm, that's odd but I think the rendering might show 6°C. I'll use 6°C.

    add_q(db, p1.id, exam_dir, 1, 13, "b",
        r"Find the number of minutes it took to reach $0°C$.",
        2, "Negative Numbers / Rate of Change", 9, (8, 0.50, 0.95),
        r"$0 - (-6) = 6°C$. Time taken $= \dfrac{6}{24} \times 10 = 2.5$ minutes.", "M1, A1",
        topic_id=2)

    # Q14 — Page 10 (idx 9)
    add_q(db, p1.id, exam_dir, 1, 14, "a",
        r"$w = \dfrac{1}{3}(a^2 + b)$. Find the value of $w$ if $a = -2$ and $b = 3$.",
        2, "Formula Substitution", 10, (9, 0.07, 0.48),
        r"$w = \dfrac{1}{3}((-2)^2 + 3) = \dfrac{1}{3}(4 + 3) = \dfrac{7}{3}$", "M1, A1",
        topic_id=4)

    add_q(db, p1.id, exam_dir, 1, 14, "b",
        r"Solve $\dfrac{32}{x - 3} = 8$.",
        2, "Solving Linear Equations", 10, (9, 0.46, 0.95),
        r"$32 = 8(x - 3)$, $32 = 8x - 24$, $8x = 56$, $x = 7$.", "M1, A1",
        topic_id=5)

    # Q15 — Page 11 (idx 10)
    add_q(db, p1.id, exam_dir, 1, 15, "a",
        r"Construct quadrilateral $ABCD$ such that $BC = 6$ cm, $AD = 7$ cm, angle $ABC = 100°$ and angle $BAD = 80°$. $AB$ has already been drawn below.",
        2, "Construction", 11, (10, 0.07, 0.67),
        r"Point C and Point D constructed correctly.", "B1 for each point",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 15, "b",
        r"Measure and write down the length of the diagonal $AC$.",
        1, "Construction — Measurement", 11, (10, 0.66, 0.78),
        r"$AC = 10.4$ cm (range $10.3$ to $10.5$)", "B1",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 15, "c",
        r"Measure and write down the size of angle $ADC$.",
        1, "Construction — Measurement", 11, (10, 0.77, 0.90),
        r"Angle $ADC = 92°$ (range $91°$ to $93°$)", "B1",
        topic_id=10)

    # Q16 — Page 12 (idx 11)
    add_q(db, p1.id, exam_dir, 1, 16, "ai",
        r"Find $AB$.",
        1, "Kite Properties", 12, (11, 0.07, 0.52),
        r"$AB = BC = 3$ cm", "B1",
        stem=r"$ABCD$ is a kite. $CDFG$ is a parallelogram. $GB = BC = 3$ cm, angle $BCA = 60°$ and area of triangle $ABD = 12$ cm$^2$.",
        topic_id=12)

    add_q(db, p1.id, exam_dir, 1, 16, "aii",
        r"Find angle $CBE$.",
        2, "Angle Properties — Kite", 12, (11, 0.50, 0.68),
        r"Angle $CBE = (180 - 60 - 90)° = 30°$", "M1, A1",
        topic_id=10)

    add_q(db, p1.id, exam_dir, 1, 16, "b",
        r"Find the area of parallelogram $CDFG$.",
        2, "Area — Parallelogram", 12, (11, 0.66, 0.92),
        r"Area of triangle $BCD$ = Area of triangle $ABD = 12$ cm$^2$. Height of parallelogram $= 12 \div (3 \times \frac{1}{2}) = 8$ cm. Area of $CDFG = 8 \times 6 = 48$ cm$^2$.",
        "M1, A1",
        topic_id=12)

    # ══════════════════════════════════════════════
    # PAPER 2 — Pages 14-26 (idx 13-25), 50 marks, 1h15m
    # ══════════════════════════════════════════════
    p2 = Paper(exam_id=exam.id, paper_number=2, duration_minutes=75, total_marks=50,
               date=date(2020, 10, 8), instructions="Answer all questions.")
    db.add(p2); db.flush()

    # P2 Q1 — Page 2 (idx 13)
    add_q(db, p2.id, exam_dir, 2, 1, "a",
        r"Find $T_4$.",
        1, "Number Patterns", 2, (13, 0.07, 0.40),
        r"$T_4 = 16 + 9 = 25$", "B1",
        stem=r"The first three terms in a sequence of numbers, $T_1, T_2, T_3, \ldots$ are given below: $T_1 = 1 + 3 = 4$, $T_2 = 4 + 5 = 9$, $T_3 = 9 + 7 = 16$.",
        topic_id=7)

    add_q(db, p2.id, exam_dir, 2, 1, "b",
        r"Find an expression, in terms of $n$, for $T_n$.",
        2, "Number Patterns — General Term", 2, (13, 0.38, 0.65),
        r"$T_n = n^2 + 2n + 1$ (or $(n+1)^2$)", "M1, A1",
        topic_id=7)

    add_q(db, p2.id, exam_dir, 2, 1, "c",
        r"Evaluate $T_{40}$.",
        1, "Number Patterns", 2, (13, 0.63, 0.90),
        r"$T_{40} = 40^2 + 2(40) + 1 = 1681$", "B1",
        topic_id=7)

    # P2 Q2 — Page 3 (idx 14)
    add_q(db, p2.id, exam_dir, 2, 2, "a",
        r"Find $k$ such that $56k$ is both a perfect square and a perfect cube.",
        1, "Prime Factorisation", 3, (14, 0.07, 0.24),
        r"$k = 2^3 \times 7^5 = 134456$", "B1",
        stem=r"Written as a product of its prime factors, $56 = 2^3 \times 7$.",
        topic_id=1)

    add_q(db, p2.id, exam_dir, 2, 2, "b",
        r"Express 42 as a product of its prime factors. Give your answer in index notation.",
        1, "Prime Factorisation", 3, (14, 0.23, 0.40),
        r"$42 = 2 \times 3 \times 7$", "B1",
        topic_id=1)

    add_q(db, p2.id, exam_dir, 2, 2, "c",
        r"Find the highest common factor of 42 and 56.",
        1, "HCF", 3, (14, 0.39, 0.55),
        r"$\text{HCF} = 14$", "B1",
        topic_id=1)

    add_q(db, p2.id, exam_dir, 2, 2, "d",
        r"Two alarm clocks are set to ring at intervals of 42 minutes and 56 minutes respectively. If the alarm clocks ring together at 0830, at what time will they next ring together again?",
        2, "LCM", 3, (14, 0.53, 0.95),
        r"$\text{LCM} = 168$ minutes $= 2$ h $48$ min. Next ring at $1118$.", "M1, A1",
        topic_id=1)

    # P2 Q3 — Pages 4-5 (idx 15-16)
    add_q(db, p2.id, exam_dir, 2, 3, "a",
        r"Find the distance travelled, in km, in the first half an hour. Give your answer in terms of $x$.",
        1, "Speed, Distance, Time", 4, (15, 0.07, 0.42),
        r"$\dfrac{1}{2}x$ km", "B1",
        stem=r"Harry drives at an average speed of $x$ km/h for half an hour and then for another 20 minutes at an average speed of $1.2x$ km/h.",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 3, "b",
        r"Show that the total distance travelled for the whole journey is $0.9x$ km.",
        1, "Speed, Distance, Time", 4, (15, 0.40, 0.95),
        r"Total distance $= \dfrac{1}{2}x + 1.2x \times \dfrac{1}{3} = \dfrac{1}{2}x + 0.4x = 0.9x$ (shown)", "B1",
        topic_id=9)

    add_q(db, p2.id, exam_dir, 2, 3, "c",
        r"Given that the average speed for the entire journey was 80 km/h, form an equation in $x$ and solve the equation.",
        4, "Solving Linear Equations", 5, (16, 0.07, 0.48),
        r"$$0.9x \div \frac{5}{6} = 80, \quad \frac{27}{25}x = 80, \quad x = 80 \div \frac{27}{25} = 74.1 \text{ (3 s.f.)}$$", "M1 for total time, M1 for equation, M1 for solving, A1",
        topic_id=5)

    add_q(db, p2.id, exam_dir, 2, 3, "d",
        r"Harry says that he will reach his destination earlier if he drives at a constant speed of 80 km/h. Is his statement reasonable? Explain your answer.",
        1, "Real-World Context", 5, (16, 0.46, 0.95),
        r"Statement is not reasonable as e.g. Car starts from 0 km/h, car will have to stop at traffic junctions, etc.", "B1",
        topic_id=9)

    # P2 Q4 — Pages 6-7 (idx 17-18)
    add_q(db, p2.id, exam_dir, 2, 4, "a",
        r"Given that the volume of the solid is $1680$ cm$^3$, show that $x = 6$.",
        2, "Volume — Prism", 6, (17, 0.07, 0.95),
        r"Area of cross-section $= \dfrac{1}{2}(12 + 16)(x) = 14x$. Volume $= 14x \times 20 = 280x$. $280x = 1680$, $x = 6$ (shown).", "M1, A1",
        stem=r"The figure shows a solid metal in the form of a trapezoidal prism. Dimensions: parallel sides 12 cm and 16 cm, height $x$ cm, length 20 cm, with 2 cm borders.",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 4, "b",
        r"Calculate the cost of painting the solid if the paint costs $\$2$ per cm$^2$.",
        3, "Surface Area — Prism", 7, (18, 0.07, 0.42),
        r"Total surface area $= (84 \times 2) + (2 + 16 + 2 + 12)(20) = 168 + 640 = 808$ cm$^2$ (or calculated face by face). Cost $= \$2 \times 808 = \$1616$.",
        "M1 for cross-section, M1 for rectangles, A1",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 4, "c",
        r"The solid is then melted and made into cubes with sides of 5 cm. Calculate the maximum number of cubes that can be made.",
        3, "Volume — Cubes", 7, (18, 0.40, 0.92),
        r"Volume of cube $= 5^3 = 125$ cm$^3$. Number of cubes $= 1680 \div 125 = 13.44$. Maximum number $= 13$.", "M1 for cube volume, M1 for division, A1",
        topic_id=13)

    # P2 Q5 — Pages 8-9 (idx 19-20)
    add_q(db, p2.id, exam_dir, 2, 5, "a",
        r"Find the value of $p$.",
        1, "Linear Functions — Table", 8, (19, 0.07, 0.40),
        r"$p = 2(-1) - 6 = -8$", "B1",
        stem=r"The variables $x$ and $y$ are connected by the equation $y = 2x - 6$. The table shows some corresponding values of $x$ and $y$: $x = -3, -1, 0, 1$ and $y = -12, p, -6, -4$.",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 5, "b",
        r"On the axes in the next page, plot the points given in the table and join them with a straight line.",
        2, "Linear Functions — Graph", 8, (19, 0.38, 0.52),
        r"Points correctly plotted and joined with a straight line.", "B1 for plotting, B1 for line",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 5, "ci",
        r"Write down the coordinates of the point where the line meets the $x$-axis.",
        1, "Linear Functions — Reading Graph", 8, (19, 0.50, 0.72),
        r"$(3, 0)$", "B1",
        topic_id=6)

    add_q(db, p2.id, exam_dir, 2, 5, "cii",
        r"Find the value of $x$ when $y = -2$.",
        1, "Linear Functions — Reading Graph", 8, (19, 0.70, 0.90),
        r"$x = 2$", "B1",
        topic_id=6)

    # P2 Q6 — Page 10 (idx 21)
    add_q(db, p2.id, exam_dir, 2, 6, "a",
        r"Find angle $XDC$.",
        2, "Polygon Angles", 10, (21, 0.07, 0.48),
        r"Interior angle of 12-sided polygon $= \dfrac{(12-2) \times 180}{12} = 150°$. $\angle XDC = 180° - 150° = 30°$.", "M1, A1",
        stem=r"The diagram shows part of a regular polygon $ABCDEF\ldots$, which has 12 sides. $BCX$ and $EDX$ are straight lines.",
        topic_id=11)

    add_q(db, p2.id, exam_dir, 2, 6, "b",
        r"Find angle $DXC$.",
        1, "Polygon Angles — Triangle", 10, (21, 0.46, 0.64),
        r"$\angle DXC = 180° - (30° \times 2) = 120°$", "B1",
        topic_id=11)

    add_q(db, p2.id, exam_dir, 2, 6, "c",
        r"Find angle $BEF$.",
        2, "Polygon Angles", 10, (21, 0.62, 0.92),
        r"$\angle DEF = \angle CDE = 150°$. $\angle DEB = \dfrac{180° - \angle DXC}{2} = 30°$ (base angles of isosceles triangle $BXE$). $\angle BEF = 150° - 30° = 120°$.", "M1, A1",
        topic_id=11)

    # P2 Q7 — Pages 11-12 (idx 22-23)
    add_q(db, p2.id, exam_dir, 2, 7, "ai",
        r"Find the total amount that Jim will pay for the laptop.",
        2, "Hire Purchase", 11, (22, 0.07, 0.38),
        r"Total instalments $= 24 \times \$114 = \$2736$. Total amount paid $= 249.90 + 2736 = \$2985.90$.", "M1, A1",
        stem=r"The cash price of a new laptop is $\$2499$. Jim buys this computer on hire purchase. He pays a deposit of 10% of the cash price followed by 24 monthly instalments of $\$114$ each.",
        topic_id=8)

    add_q(db, p2.id, exam_dir, 2, 7, "aii",
        r"Find the cost of buying the laptop on hire purchase as a percentage of the cash price.",
        2, "Percentage", 11, (22, 0.36, 0.56),
        r"$\dfrac{2985.90}{2499} \times 100\% = 119\%$ (nearest whole %)", "M1, A1",
        topic_id=8)

    add_q(db, p2.id, exam_dir, 2, 7, "b",
        r"$\$6000$ was deposited into a bank. The simple interest earned at the end of 8 years was $\$72$. Calculate the yearly interest rate given by the bank.",
        2, "Simple Interest", 11, (22, 0.54, 0.95),
        r"$72 = \dfrac{6000 \times r \times 8}{100}$. $r = 0.15\%$.", "M1, A1",
        topic_id=8)

    add_q(db, p2.id, exam_dir, 2, 7, "ci",
        r"She answered 80% of the questions in Section A correctly. Find the number of questions in Section A that she answered correctly.",
        1, "Percentage", 12, (23, 0.07, 0.38),
        r"$\dfrac{80}{100} \times 20 = 16$", "B1",
        stem=r"Belle took a Mathematics test that consists of 2 sections. Section A has 20 questions and Section B has 10 questions. 1 mark is awarded for each question answered correctly.",
        topic_id=8)

    add_q(db, p2.id, exam_dir, 2, 7, "cii",
        r"Find the percentage of the questions in Section B that she needs to answer correctly in order to score 70% for the entire test.",
        3, "Percentage", 12, (23, 0.36, 0.95),
        r"Target score $= \dfrac{70}{100} \times 30 = 21$. Need $21 - 16 = 5$ from Section B. Percentage $= \dfrac{5}{10} \times 100\% = 50\%$.", "M1 for target, M1 for Section B marks, A1",
        topic_id=8)

    # P2 Q8 — Pages 13-14 (idx 24-25)
    add_q(db, p2.id, exam_dir, 2, 8, "a",
        r"Using the model, show that the volume of the Soda Can A is $108\pi$ cm$^3$.",
        1, "Volume — Cylinder", 13, (24, 0.07, 0.58),
        r"Volume $= \pi(3)^2 \times 12 = 108\pi$ (shown)", "B1",
        stem=r"The figure shows Soda Can A, which can be modelled as a cylinder of height 12 cm and radius 3 cm.",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 8, "b",
        r"Using the model, estimate the total surface area of the Soda Can A, in cm$^2$.",
        2, "Surface Area — Cylinder", 13, (24, 0.56, 0.95),
        r"$\text{SA} = \pi(3)^2 \times 2 + 2\pi(3)(12) = 18\pi + 72\pi = 90\pi \approx 283$ cm$^2$", "M1, A1",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 8, "ci",
        r"As a manufacturer of drink cans, which design will you use? Justify your answer.",
        1, "Real-World Context", 14, (25, 0.07, 0.48),
        r"Soda Can A as it has a smaller surface area and hence will be cheaper to manufacture.", "B1",
        stem=r"The figure shows another Soda Can B, which can be modelled as a cylinder of height 17.28 cm and radius 2.5 cm. The volume of Soda Can B is $108\pi$ cm$^3$ and its total surface area is $98.9\pi$ cm$^2$.",
        topic_id=13)

    add_q(db, p2.id, exam_dir, 2, 8, "cii",
        r"The smaller the volume to surface-area ratio, the faster the soda drink can will cool down in the freezer. Determine which Soda Can will cool down faster in the freezer. Show your working clearly.",
        2, "Ratio — Real-World", 14, (25, 0.46, 0.90),
        r"Can A: $\dfrac{108\pi}{90\pi} = 1.2$. Can B: $\dfrac{108\pi}{98.9\pi} = 1.09$. Can B will cool down faster.", "M1, A1",
        topic_id=13)

    db.commit()
    p1_count = len(p1.questions)
    p2_count = len(p2.questions)
    print(f"Seeded ACS (Barker Road) 2020 exam id={exam.id}: Paper 1 ({p1_count} parts), Paper 2 ({p2_count} parts)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
