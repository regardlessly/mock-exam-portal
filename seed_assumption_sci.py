"""Seed Assumption English School EOY 2019 Sec 1 Express Science exam (Booklet A MCQ)."""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/science/2019-Sec-1-Express-Science-SA2-Assumption-English.pdf"
IMAGES_DIR = "/tmp/assumption_sci_pages"

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

    school = db.query(School).filter(School.name == "Assumption English School").first()
    if not school:
        school = School(name="Assumption English School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(
        Exam.school_id == school.id, Exam.year == 2019,
        Exam.subject == "Science").first()
    if existing:
        print(f"Assumption 2019 Science already seeded (id={existing.id}). Re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id, title="End-of-Year Examination 2019", year=2019,
        level="Secondary 1 Express", subject="Science",
        source_pdf="2019-Sec-1-Express-Science-SA2-Assumption-English.pdf",
        status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # BOOKLET A — Section A: Multiple-Choice (30 marks)
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=120, total_marks=30,
               date=date(2019, 10, 8),
               instructions="Section A: 30 multiple-choice questions. Choose the one correct answer.")
    db.add(p1); db.flush()

    add_q(db, p1.id, exam_dir, 1, 1, None,
        r"Which statement(s) is / are true? "
        r"I Advancements in science are always beneficial to society. "
        r"II Science is the study of our physical world. "
        r"III Scientific knowledge is derived from observations. "
        r"IV We use instruments to help us make accurate measurements. "
        r"A I and II only  B III and IV only  C II, III and IV only  D all of the above",
        1, "Introduction to Science", 2, (1, 0.10, 0.42),
        "A — I and II only. Advancements in science are not always beneficial; "
        "scientific knowledge from observation and instruments aid measurement.",
        "B1", topic_id=101)

    add_q(db, p1.id, exam_dir, 1, 2, None,
        r"The following symbols were found on a bottle of reagent (corrosive / harmful "
        r"and toxic hazard symbols). Which of the following does / do not show the "
        r"safety precaution(s) that should be taken when using this reagent? "
        r"I Do not have it near open flame. "
        r"II Using a stopper to seal the reagent after use to prevent vapours from escaping in to the surrounding. "
        r"III Use special protective gear during handling. "
        r"A I only  B I and III only  C II and III only  D III only",
        1, "Laboratory Safety", 2, (1, 0.42, 0.95),
        "C — II and III only. The symbols are corrosive/toxic, not flammable; "
        "the stated precautions about flame and gear do not match these symbols.",
        "B1", topic_id=101)

    add_q(db, p1.id, exam_dir, 1, 3, None,
        r"Jordan noticed that after several rounds of washing, some of his T-shirts shrank "
        r"in size. He then conducted a scientific investigation. "
        r"I Jordan measured the size of the T-shirts after the wash and recorded them in a table. "
        r"II Jordan concluded that cotton results in greater shrinkage. "
        r"III Jordan chose two T-shirts, made up of cotton and polyester respectively, and washed them under the same conditions. "
        r"IV Jordan predicted that the materials of the T-shirts affect whether they would shrink in size after washing. "
        r"Which correctly corresponds with the key elements of the scientific method "
        r"(formulating hypothesis, collecting data, carrying out experiment, interpreting data)? "
        r"A II, III, I, IV  B III, I, IV, II  C IV, III, I, II  D IV, I, III, II",
        1, "Scientific Method", 3, (2, 0.05, 0.62),
        "D — hypothesis IV, collect data I, carry out experiment III, interpret data II.",
        "B1", topic_id=101)

    add_q(db, p1.id, exam_dir, 1, 4, None,
        r"The diagram shows the reading for the length of an object measured by a vernier "
        r"caliper, with its vernier scale V placed against the main scale S. What is the reading shown? "
        r"A 7.23 cm  B 7.26 cm  C 7.33 cm  D 7.36 cm",
        1, "Measurement — Vernier", 3, (2, 0.62, 0.98),
        "C — 7.33 cm (main scale 7.3 cm + vernier 0.03 cm).",
        "B1", topic_id=102)

    add_q(db, p1.id, exam_dir, 1, 5, None,
        r"Which diagram is the correct scientific drawing for a conical flask? "
        r"A (open V shape)  B (round-bottom flask)  C (conical flask outline)  D (stool shape)",
        1, "Laboratory Apparatus", 4, (3, 0.05, 0.40),
        "C — the conical (Erlenmeyer) flask outline.",
        "B1", topic_id=101)

    add_q(db, p1.id, exam_dir, 1, 6, None,
        r"The air-hole of a Bunsen burner can be opened or closed to obtain two types of "
        r"flame. W is the outer flame with the air-hole opened; X is the outer flame with "
        r"the air-hole closed. Which option correctly states the colours of W and X? "
        r"A W blue, X blue  B W blue, X orange  C W orange, X blue  D W orange, X orange",
        1, "Bunsen Burner Flame", 4, (3, 0.40, 0.98),
        "B — air-hole open gives a blue (non-luminous) flame; air-hole closed gives an "
        "orange (luminous) flame.",
        "B1", topic_id=101)

    add_q(db, p1.id, exam_dir, 1, 7, None,
        r"The table shows a scratch test for bronze, zinc, iron and titanium. If substance "
        r"X scratches substance Y leaving a mark, a tick is placed; otherwise a cross. "
        r"Arrange the substances according to increasing hardness. "
        r"A titanium, iron, bronze, zinc  B titanium, zinc, iron, bronze  "
        r"C zinc, bronze, iron, titanium  D zinc, iron, bronze, titanium",
        1, "Properties of Materials", 5, (4, 0.05, 0.55),
        "C — zinc (softest), bronze, iron, titanium (hardest), based on which substance "
        "scratches which.",
        "B1", topic_id=104)

    add_q(db, p1.id, exam_dir, 1, 8, None,
        r"The diagram shows some liquid in a measuring cylinder. What is the volume of the liquid? "
        r"A 55.8 cm³  B 55.9 cm³  C 56.0 cm³  D 56.1 cm³",
        1, "Measurement — Volume", 5, (4, 0.55, 0.98),
        "B — read the bottom of the meniscus: 55.9 cm³.",
        "B1", topic_id=102)

    add_q(db, p1.id, exam_dir, 1, 9, None,
        r"A student has to find the volume of a cork using a measuring cylinder. The cork "
        r"floats, so a stone is used to keep it under the water. Water = 20 cm³, "
        r"water + cork = 23.5 cm³, water + cork + stone = 48.5 cm³, water + stone = 41.5 cm³. "
        r"What is the volume of the cork? "
        r"A 3.5 cm³  B 7.0 cm³  C 18.0 cm³  D 21.5 cm³",
        1, "Measurement — Volume by Displacement", 6, (5, 0.05, 0.55),
        "B — volume of cork = (water+cork+stone) − (water+stone) = 48.5 − 41.5 = 7.0 cm³.",
        "B1", topic_id=102)

    add_q(db, p1.id, exam_dir, 1, 10, None,
        r"A student drops six identical aluminium balls, each of mass 27 g, into a "
        r"measuring cylinder containing water. Water level rises from 50 cm³ to 110 cm³. "
        r"What is the density of the aluminium balls? "
        r"A 0.4 g/cm³  B 2.7 g/cm³  C 60 g/cm³  D 162 g/cm³",
        1, "Density", 6, (5, 0.55, 0.98),
        "B — total mass = 6 × 27 = 162 g; volume = 110 − 50 = 60 cm³; "
        "density = 162 ÷ 60 = 2.7 g/cm³.",
        "B1", topic_id=102)

    add_q(db, p1.id, exam_dir, 1, 11, None,
        r"At which position should the student be taking the reading so as to avoid "
        r"parallax error? (Eye positions A, B/C, D shown above a ruler under a block.) "
        r"A  B  C  D",
        1, "Measurement — Parallax", 7, (6, 0.05, 0.55),
        "C — the line of sight must be directly perpendicular (straight down) to the scale.",
        "B1", topic_id=102)

    add_q(db, p1.id, exam_dir, 1, 12, None,
        r"Which property is the reason why tungsten is a suitable material for a filament "
        r"in a light bulb? "
        r"A flexibility  B hardness  C melting point  D strength",
        1, "Properties of Materials", 7, (6, 0.55, 0.80),
        "C — tungsten has a very high melting point, so the filament does not melt when hot.",
        "B1", topic_id=104)

    add_q(db, p1.id, exam_dir, 1, 13, None,
        r"Tyres are made of …… as it is …… and can withstand high temperature and friction. "
        r"A plastic, less dense than water  B metal, malleable  C rubber, elastic  D metal, malleable",
        1, "Properties of Materials", 7, (6, 0.80, 0.98),
        "C — rubber, elastic; rubber is elastic and withstands heat and friction.",
        "B1", topic_id=104)

    add_q(db, p1.id, exam_dir, 1, 14, None,
        r"Which diagram shows a mixture of two different elements? (Diagrams I–IV show "
        r"different particle arrangements.) "
        r"A I only  B I and II only  C III and IV only  D all of the above",
        1, "Elements, Compounds & Mixtures", 8, (7, 0.05, 0.55),
        "C — III and IV only: both contain two kinds of single (un-bonded) atoms = "
        "mixture of two elements.",
        "B1", topic_id=104)

    add_q(db, p1.id, exam_dir, 1, 15, None,
        r"Decomposition occurs when sugar is heated to form carbon and water vapour. "
        r"Which statement about decomposition is true? "
        r"A Compounds are broken down into simpler substances. "
        r"B Compounds combine to form new compounds. "
        r"C Elements are broken down into simpler substances. "
        r"D Elements combine to form compounds.",
        1, "Chemical Change", 8, (7, 0.55, 0.98),
        "A — decomposition breaks a compound down into simpler substances.",
        "B1", topic_id=104)

    add_q(db, p1.id, exam_dir, 1, 16, None,
        r"A mixture containing two types of sugar is analysed using chromatography and "
        r"compared against four other types of sugar. Which two sugars does the mixture contain? "
        r"A 1 and 2  B 1 and 4  C 2 and 4  D 3 and 4",
        1, "Separation Techniques", 9, (8, 0.05, 0.55),
        "C — the mixture's two spots align with the spots of sugar 2 and sugar 4.",
        "B1", topic_id=105)

    add_q(db, p1.id, exam_dir, 1, 17, None,
        r"Rice supplies the body with the nutrient carbohydrate. There are many types of "
        r"rice and the existence of this variety is important. Which is not one of the "
        r"reasons why a variety in rice is important? "
        r"A Different rice crops can be grown in different climates. "
        r"B Different rice crops can be grown in different types of soil. "
        r"C Some rice crops are pest-resistant and help prevent the rice species from being wiped out. "
        r"D Humans can pick the type of nutrients they want.",
        1, "Variation & Nutrition", 9, (8, 0.55, 0.98),
        "D — variety does not let humans pick nutrients; rice supplies carbohydrate "
        "regardless of variety.",
        "B1", topic_id=109)

    add_q(db, p1.id, exam_dir, 1, 18, None,
        r"A student wants to construct a dichotomous key to classify different plants in a "
        r"garden. Which question(s) should he ask when classifying them? "
        r"I Are there organisms living on each plant? "
        r"II Do the leaves have smooth or jagged edge? "
        r"III How many leaves does each plant have? "
        r"IV How many types of plants are there in the garden? "
        r"A I and II only  B II and III only  C I, II and III only  D II, III and IV only",
        1, "Classification", 10, (9, 0.05, 0.55),
        "D — II, III and IV only. A dichotomous key uses observable distinguishing "
        "features of the plants.",
        "B1", topic_id=107)

    add_q(db, p1.id, exam_dir, 1, 19, None,
        r"Use the dichotomous key to answer questions 19 and 20. Ezekiel studies a black "
        r"organism that has a long, tubular and segmented body. This organism moves using "
        r"its multiple legs attached to each segment of its body. What is the identity of "
        r"this organism? "
        r"A centipede  B leech  C slug  D spider",
        1, "Classification — Dichotomous Key", 11, (10, 0.05, 0.62),
        "A — centipede: long segmented tubular body with multiple legs per segment.",
        "B1", topic_id=107)

    add_q(db, p1.id, exam_dir, 1, 20, None,
        r"Which statement is correct about both spiders and ticks? "
        r"A They both have spinnerets.  B They both have tails.  "
        r"C They are arachnids.  D They are insects.",
        1, "Classification", 11, (10, 0.62, 0.98),
        "C — both spiders and ticks are arachnids.",
        "B1", topic_id=107)

    add_q(db, p1.id, exam_dir, 1, 21, None,
        r"A tiger invaded a village near a forest. Which are possible causes of this incident? "
        r"I The tigers were over-hunted. "
        r"II The tigers no longer had a source of food. "
        r"III The natural habitat of the tigers was destroyed. "
        r"IV The tigers were infected by a type of bacteria. "
        r"A I and II only  B II and III only  C III and IV only  D all of the above",
        1, "Interactions & Habitats", 12, (11, 0.05, 0.30),
        "B — II and III only: loss of food source and habitat destruction drive tigers "
        "into villages.",
        "B1", topic_id=107)

    add_q(db, p1.id, exam_dir, 1, 22, None,
        r"The brain is an organ because ……… "
        r"A it has different tissues working together. "
        r"B it has different organelles working together. "
        r"C it has different types of cells working together. "
        r"D it is part of the nervous system.",
        1, "Cells & Organisation", 12, (11, 0.30, 0.52),
        "A — an organ is made of different tissues working together.",
        "B1", topic_id=107)

    add_q(db, p1.id, exam_dir, 1, 23, None,
        r"Division of labour in an organism is important because ……… "
        r"A cells in multicellular organisms have specific functions. "
        r"B cells performing similar functions group together to form tissues. "
        r"C the nucleus controls the activities in the cell. "
        r"D work is broken down into specific tasks for maximum efficiency.",
        1, "Cells & Organisation", 12, (11, 0.52, 0.75),
        "D — division of labour breaks work into specific tasks for maximum efficiency.",
        "B1", topic_id=107)

    add_q(db, p1.id, exam_dir, 1, 24, None,
        r"An amoeba had its nucleus removed. For several days, it continued to move and "
        r"feed but it did not reproduce. A normal amoeba reproduced twice in that time. "
        r"What conclusion can be drawn using the information given? "
        r"A The nucleus is necessary for cell growth. "
        r"B The nucleus is necessary for reproduction. "
        r"C The nucleus is necessary for the release of energy. "
        r"D The nucleus is the site for chemical reactions in the cell.",
        1, "Cells — Nucleus", 12, (11, 0.75, 0.98),
        "B — without the nucleus the amoeba could not reproduce, so the nucleus is "
        "necessary for reproduction.",
        "B1", topic_id=107)

    add_q(db, p1.id, exam_dir, 1, 25, None,
        r"Scientists discovered a new organism, A, living in the depth of a pond. The "
        r"labelled image shows organism A with a flagellum, chloroplast, cytoplasm and "
        r"nucleus. Which statement is correct about organism A? "
        r"A Organism A is an animal cell as it does not have a cell wall. "
        r"B Organism A is a plant cell as it possesses chloroplast only. "
        r"C Organism A is a plant cell as it possesses cytoplasm and a nucleus. "
        r"D Organism A is an animal cell because it has a flagellum.",
        1, "Plant & Animal Cells", 13, (12, 0.05, 0.55),
        "A — it has no cell wall (and is mobile via flagellum), so it behaves like an "
        "animal cell despite the chloroplast.",
        "B1", topic_id=107)

    add_q(db, p1.id, exam_dir, 1, 26, None,
        r"Which part of organism A is the site of many chemical reactions? "
        r"A chloroplast  B cytoplasm  C flagellum  D nucleus",
        1, "Cell Structure — Function", 13, (12, 0.55, 0.98),
        "B — the cytoplasm is the site of many chemical reactions in the cell.",
        "B1", topic_id=107)

    add_q(db, p1.id, exam_dir, 1, 27, None,
        r"Which diagram represents the arrangement of particles during the process of "
        r"condensation? (A: spread → packed; B: packed → spread; C: closely packed → "
        r"spread; D: closely packed → spread.) "
        r"A  B  C  D",
        1, "Particulate Nature of Matter", 14, (13, 0.05, 0.55),
        "A — condensation is gas → liquid: widely spaced particles become closer together.",
        "B1", topic_id=103)

    add_q(db, p1.id, exam_dir, 1, 28, None,
        r"Which row shows the correct relative charges of the sub-atomic particles of an atom? "
        r"A proton −1, neutron 0, electron +1  B proton 0, neutron +1, electron −1  "
        r"C proton +1, neutron 0, electron −1  D proton +1, neutron −1, electron 0",
        1, "Atomic Structure", 14, (13, 0.55, 0.98),
        "C — proton +1, neutron 0, electron −1.",
        "B1", topic_id=104)

    add_q(db, p1.id, exam_dir, 1, 29, None,
        r"Alice looks through a U-shaped hollow tube while David looks through a straight "
        r"hollow tube. Both tubes are the same short distance from a candle flame. Which "
        r"statement about the set-up is correct? "
        r"A Both Alice and David can see the candle flame. "
        r"B Both Alice and David cannot see the candle flame. "
        r"C Only Alice can see the candle flame. "
        r"D Only David can see the candle flame.",
        1, "Light — Rectilinear Propagation", 15, (14, 0.05, 0.55),
        "D — light travels in straight lines, so only David (straight tube) can see the "
        "flame; the U-shaped tube blocks it.",
        "B1", topic_id=114)

    add_q(db, p1.id, exam_dir, 1, 30, None,
        r"When a green object is illuminated by a coloured light it appears black. Which "
        r"colour could the light be? "
        r"A cyan  B green  C yellow  D red",
        1, "Light — Colour", 15, (14, 0.55, 0.95),
        "D — red. A green object reflects only green; under red light there is no green "
        "to reflect, so it appears black.",
        "B1", topic_id=114)

    db.commit()
    count = len(p1.questions)
    print(f"Seeded Assumption English School 2019 Science exam id={exam.id}: "
          f"Booklet A ({count} MCQs)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
