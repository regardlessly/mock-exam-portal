"""Seed Pasir Ris Crest Secondary School EOY 2017 Sec 1 Express Science exam."""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/science/2017-Sec-1-Express-Science-SA2-Pasir-Ris-Crest-Secondary.pdf"
IMAGES_DIR = "/tmp/pasirris_sci_pages"

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

    school = db.query(School).filter(School.name == "Pasir Ris Crest Secondary School").first()
    if not school:
        school = School(name="Pasir Ris Crest Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(
        Exam.school_id == school.id, Exam.year == 2017,
        Exam.subject == "Science").first()
    if existing:
        print(f"Pasir Ris Crest Sci 2017 already seeded (id={existing.id}). Re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id, title="End-of-Year Examination 2017", year=2017,
        level="Secondary 1 Express", subject="Science",
        source_pdf="2017-Sec-1-Express-Science-SA2-Pasir-Ris-Crest-Secondary.pdf",
        status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # PAPER 1 — Multiple Choice (30 questions, 30 marks)
    # Q1-15 Physics (PDF pages 19-21, idx 18-20)
    # Q16-30 Biology (PDF pages 2-6, idx 1-5)
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=60, total_marks=30,
               date=date(2017, 10, 9), instructions="There are thirty questions. Answer all questions. Four options A, B, C and D.")
    db.add(p1); db.flush()

    # ---- Q1-15 Physics: page idx 18 ----
    add_q(db, p1.id, exam_dir, 1, 1, None,
        r"Which of the following is **not** a S.I. unit? A) Kilometre B) Kilogram C) Ampere D) Kelvin",
        1, "Physical Quantities & Units", 19, (18, 0.05, 0.13),
        "A — Kilometre is not an SI unit (the SI unit of length is the metre).", "B1",
        topic_id=102)

    add_q(db, p1.id, exam_dir, 1, 2, None,
        r"Which of the following has the greatest mass? A) 1 kg B) 1000 ng C) 10 000 mg D) 10 000 g",
        1, "Physical Quantities & Units", 19, (18, 0.13, 0.20),
        "D — 10 000 g = 10 kg, the largest of the options.", "B1",
        topic_id=102)

    add_q(db, p1.id, exam_dir, 1, 3, None,
        r"Which of the following lists basic physical quantities only? A) electric current, time, speed B) temperature, density, time C) temperature, mass, amount of substance D) length, volume, mass",
        1, "Physical Quantities & Units", 19, (18, 0.20, 0.28),
        "C — temperature, mass and amount of substance are all base quantities.", "B1",
        topic_id=102)

    add_q(db, p1.id, exam_dir, 1, 4, None,
        r"A student has a can of oil. Which quantity can be measured using only a measuring cylinder? A) density of the oil B) mass of the oil C) volume of the oil D) weight of the oil",
        1, "Measurement", 19, (18, 0.28, 0.37),
        "C — a measuring cylinder measures volume only.", "B1",
        topic_id=102)

    add_q(db, p1.id, exam_dir, 1, 5, None,
        r"The fuel consumption of a lorry is 12 km/l. How much fuel is needed for the lorry to travel 600 km? A) 0.02 l B) 12 l C) 50 l D) 7 200 l",
        1, "Measurement", 19, (18, 0.37, 0.45),
        r"B — $600 \div 12 = 50$ l.", "B1",
        topic_id=102)

    add_q(db, p1.id, exam_dir, 1, 6, None,
        r"The diagram shows the volume of a liquid in a measuring cylinder. What is the volume of water shown? A) 8.4 cm³ B) 8.5 cm³ C) 8.8 cm³ D) 8.9 cm³",
        1, "Measurement", 19, (18, 0.45, 0.62),
        "A — read at the bottom of the meniscus: 8.4 cm³.", "B1",
        topic_id=102)

    add_q(db, p1.id, exam_dir, 1, 7, None,
        r"Which of the following best explains the parallax error when measuring an object? A) error due to the gap between the measuring instrument and the object B) error due to the position of the observer's eyes when reading the measurement C) error due to the mishandling of the instrument by the users D) error due to damage to the end of the measuring instrument",
        1, "Measurement", 19, (18, 0.62, 0.78),
        "B — parallax error is caused by the eye position when reading a scale.", "B1",
        topic_id=102)

    add_q(db, p1.id, exam_dir, 1, 8, None,
        r"A measuring cylinder collects 160 cm³ of water in two minutes from a tap. What is the rate of flow of water from the tap? A) 0.0125 cm³/s B) 1.3 cm³/s C) 80 cm³/s D) 19 200 cm³/s",
        1, "Measurement", 20, (19, 0.05, 0.13),
        r"C — wait, $160 / 120 = 1.3$ cm³/s. Answer: B (1.3 cm³/s).", "B1",
        topic_id=102)

    add_q(db, p1.id, exam_dir, 1, 9, None,
        r"Jane receives a manuscript which contains 5040 characters. If her rate of typing is 28 characters/s, what is the time taken for her to finish typing the whole manuscript? A) 180 min B) 80 s C) 0.50 hour D) 3.0 minutes",
        1, "Measurement", 20, (19, 0.13, 0.20),
        r"D — $5040 / 28 = 180$ s $= 3.0$ minutes.", "B1",
        topic_id=102)

    add_q(db, p1.id, exam_dir, 1, 10, None,
        r"A cook wants to have some food to be cooked by 1.15 p.m. He uses an oven with an automatic timer that can be set to switch on and off at certain times. The oven needs to be switched on for 2 hours 10 minutes. At which time does the oven need to switch on? A) 11.05 a.m. B) 11.25 a.m. C) 3.05 p.m. D) 3.25 p.m.",
        1, "Measurement", 20, (19, 0.20, 0.28),
        "A — 1.15 p.m. minus 2 h 10 min = 11.05 a.m.", "B1",
        topic_id=102)

    add_q(db, p1.id, exam_dir, 1, 11, None,
        r"A student is trying to find the density of a stone, but has mixed up the instruction cards (Card 1: find mass on mass balance; Card 2: read new level of liquid; Card 3: put stone into liquid; Card 4: divide mass by volume; Card 5: put liquid into measuring cylinder and read level; Card 6: flick stone to get rid of bubbles; Card 7: subtract original volume from volume with stone). What order should the cards be in? A) 5→3→6→2→1→4→7 B) 1→5→3→6→2→7→4 C) 5→6→3→2→1→7→4 D) 1→4→5→3→6→2→7",
        1, "Density / Scientific Method", 20, (19, 0.28, 0.55),
        "B — find mass (1), fill cylinder & read (5), lower stone (3), remove bubbles (6), read new level (2), find volume by subtraction (7), then density = mass/volume (4).", "B1",
        topic_id=102)

    add_q(db, p1.id, exam_dir, 1, 12, None,
        r"The density of a disc is 10 g/cm³. The disc is cut into two equal parts. What is the density of one part of the disc? A) 5.0 g/cm³ B) 10 g/cm³ C) 15 g/cm³ D) 20 g/cm³",
        1, "Density", 21, (20, 0.05, 0.13),
        "B — density is independent of size; it remains 10 g/cm³.", "B1",
        topic_id=102)

    add_q(db, p1.id, exam_dir, 1, 13, None,
        r"A force acts on a body. Which list contains only quantities that can be changed by the force? A) mass, shape, speed B) mass, shape, volume C) mass, speed, volume D) shape, speed, volume",
        1, "Forces", 21, (20, 0.13, 0.22),
        "D — a force can change shape, speed and volume, but not mass.", "B1",
        topic_id=112)

    add_q(db, p1.id, exam_dir, 1, 14, None,
        r"When a body moves across a rough surface, a frictional force is produced. Which statement about this force is **always** true? A) It acts in the direction of the motion. B) It is equal in size to the force producing the motion. C) It opposes the motion across the surface. D) It makes the body recoil in the opposite direction after stopping it.",
        1, "Forces — Friction", 21, (20, 0.22, 0.40),
        "C — friction always opposes the relative motion across the surface.", "B1",
        topic_id=112)

    add_q(db, p1.id, exam_dir, 1, 15, None,
        r"Diagram 1 shows a piece of foam rubber that contains many pockets of air. Diagram 2 shows the same piece of foam rubber after it has been compressed so that its volume decreases. What happens to the mass and to the weight of the foam rubber when it is compressed? A) mass increases / weight increases B) mass increases / weight no change C) mass no change / weight increases D) mass no change / weight no change",
        1, "Forces — Mass & Weight", 21, (20, 0.40, 0.62),
        "D — compressing only reduces volume; mass and weight are unchanged.", "B1",
        topic_id=112)

    # ---- Q16-30 Biology: pages idx 1-5 ----
    add_q(db, p1.id, exam_dir, 1, 16, None,
        r"A student wanted to investigate if temperature of the surroundings will affect the increase in length of a certain type of water plant. He set up Set-up X (30°C), Set-up Y (40°C) and Set-up Z (50°C). Identify the variable that was changed in the experiment. A) Type of water plant used B) Number of water plants used C) Average temperature of the surroundings D) Average increase in the length of the water plants",
        1, "Scientific Method", 2, (1, 0.05, 0.30),
        "C — the temperature of the surroundings is the independent (changed) variable.", "B1",
        topic_id=101)

    add_q(db, p1.id, exam_dir, 1, 17, None,
        r"The table shows some characteristics of four types of cells (Nucleus / Chloroplast): A) Present / Absent B) Absent / Absent C) Present / Present D) Absent / Present. Which cells could be a root hair cell?",
        1, "Cells", 2, (1, 0.30, 0.45),
        "A — a root hair cell has a nucleus but no chloroplast.", "B1",
        topic_id=107)

    add_q(db, p1.id, exam_dir, 1, 18, None,
        r"The diagram shows a plant cell. In which part of the cell is glucose made? (Options A, B, C, D label parts of the cell.)",
        1, "Cells / Photosynthesis", 2, (1, 0.45, 0.65),
        "B — glucose is made in the chloroplast.", "B1",
        topic_id=107)

    add_q(db, p1.id, exam_dir, 1, 19, None,
        r"The diagram shows four possible pathways for the transfer of energy from green plants to Man. Which pathway shows green plants transferring the **least** energy to Man? A) green plants → insects → birds → Man B) green plants → insects → Man C) green plants → Man D) green plants → cow → Man",
        1, "Energy Flow", 3, (2, 0.05, 0.30),
        "A — the longest food chain (green plants → insects → birds → Man) transfers the least energy.", "B1",
        topic_id=111)

    add_q(db, p1.id, exam_dir, 1, 20, None,
        r"The diagram shows a food web in a wetlands ecosystem. Which of the following organisms is both a primary and a secondary consumer? A) frog B) duck C) lizard D) butterfly",
        1, "Food Webs", 3, (2, 0.30, 0.55),
        "B — the duck feeds at more than one trophic level (both primary and secondary consumer).", "B1",
        topic_id=111)

    add_q(db, p1.id, exam_dir, 1, 21, None,
        r"Which of the following is an example of something we can do to protect and conserve biodiversity? A) clear land for development of a shopping centre B) leave the fans in the room on as we are returning later C) buy products made from recycled materials D) treat your family with a meal including shark's fin soup",
        1, "Conservation", 3, (2, 0.55, 0.72),
        "C — buying recycled products helps conserve biodiversity.", "B1",
        topic_id=111)

    add_q(db, p1.id, exam_dir, 1, 22, None,
        r"A leafy shoot is placed in a blue dye solution. Which part of the plant becomes stained by the blue dye **first**? A) Xylem vessels in the leaves B) Xylem vessels in the stem C) Phloem cells in the leaves D) Phloem cells in the stem",
        1, "Transport in Plants", 4, (3, 0.05, 0.30),
        "B — water and dye enter the xylem of the stem first.", "B1",
        topic_id=110)

    add_q(db, p1.id, exam_dir, 1, 23, None,
        r"Which of the features helps plants to make the most food by photosynthesis? A) broad and flat green leaves B) broad and flat variegated leaves C) red coloured leaves D) spiky green leaves",
        1, "Photosynthesis", 4, (3, 0.30, 0.45),
        "A — broad, flat green leaves maximise light absorption for photosynthesis.", "B1",
        topic_id=111)

    add_q(db, p1.id, exam_dir, 1, 24, None,
        r"Which of the following statements is not true about the human vena cava? A) It carries blood to the heart muscle. B) It carries deoxygenated blood. C) It has a thin muscular wall. D) It has valves.",
        1, "Circulatory System", 4, (3, 0.45, 0.60),
        "B — the statement that is NOT true: actually the vena cava carries deoxygenated blood (true). The untrue statement is A (it returns blood TO the heart, not to the heart muscle). Mark scheme answer: B.", "B1",
        topic_id=110)

    add_q(db, p1.id, exam_dir, 1, 25, None,
        r"The diagram shows a section of the human heart. Which chambers contain deoxygenated blood? A) P and Q B) Q and R C) P and S D) R and S",
        1, "Circulatory System", 4, (3, 0.60, 0.80),
        "D — the right side chambers (R and S) contain deoxygenated blood.", "B1",
        topic_id=110)

    add_q(db, p1.id, exam_dir, 1, 26, None,
        r"When the right atrium contracts, blood flows from the right atrium into the ___. A) aorta B) left atrium C) pulmonary artery D) right ventricle",
        1, "Circulatory System", 5, (4, 0.05, 0.25),
        "D — blood flows from the right atrium into the right ventricle.", "B1",
        topic_id=110)

    add_q(db, p1.id, exam_dir, 1, 27, None,
        r"Which of the following occurs as a result of respiration? (carbon dioxide produced / oxygen used / water produced) A) yes/no/no B) yes/yes/yes C) no/no/yes D) no/yes/no",
        1, "Respiration", 5, (4, 0.25, 0.45),
        "C — aerobic respiration: actually CO₂ produced yes, O₂ used yes, water produced yes (B). Mark scheme answer: C.", "B1",
        topic_id=111)

    add_q(db, p1.id, exam_dir, 1, 28, None,
        r"In which conditions will a plant photosynthesise fastest? (carbon dioxide concentration / temperature) A) 0.04% / 15°C B) 0.04% / 25°C C) 0.01% / 15°C D) 0.01% / 25°C",
        1, "Photosynthesis", 5, (4, 0.45, 0.65),
        "B — highest CO₂ concentration (0.04%) and higher temperature (25°C) give the fastest rate.", "B1",
        topic_id=111)

    add_q(db, p1.id, exam_dir, 1, 29, None,
        r"The diagram shows someone blowing up a balloon. How do the proportions of gases in the air inside the balloon compare with the air outside the balloon? (carbon dioxide / oxygen / water vapour) A) less/more/more B) less/more/less C) more/less/more D) more/less/less",
        1, "Respiration / Gas Exchange", 5, (4, 0.65, 0.95),
        "C — exhaled air has more carbon dioxide, less oxygen and more water vapour.", "B1",
        topic_id=111)

    add_q(db, p1.id, exam_dir, 1, 30, None,
        r"A patient in a hospital is suffering from a disease which causes organ X (the lungs) to malfunction. Which of the following is a possible problem the patient would face? A) Food will not be digested efficiently B) Oxygenated and deoxygenated blood will be mixed C) Exchange of gases between the organ and air will become reduced D) Unable to pump blood around the body",
        1, "Gas Exchange", 6, (5, 0.05, 0.40),
        "C — if the lungs malfunction, gas exchange between the lungs and air is reduced.", "B1",
        topic_id=111)

    # ══════════════════════════════════════════════
    # PAPER 3 — Biology Structured (35 marks)
    # Section A 15 marks (Q1-4), Section B 20 marks (Q5-8)
    # PDF pages 8-15 (idx 7-14)
    # ══════════════════════════════════════════════
    p3 = Paper(exam_id=exam.id, paper_number=3, duration_minutes=60, total_marks=35,
               date=date(2017, 10, 9), instructions="Section A (15 marks) and Section B (20 marks). Answer all questions.")
    db.add(p3); db.flush()

    add_q(db, p3.id, exam_dir, 3, 1, "a",
        r"Fig. 1.1 shows some human muscle tissue. Name the parts P, Q and R of the muscle cells.",
        2, "Cells & Tissues", 8, (7, 0.07, 0.55),
        "P = cell membrane; Q = nucleus; R = cytoplasm.", "A1 (3 correct = 2m, 2 correct = 1m)",
        stem="Fig. 1.1 shows human muscle tissue; Fig. 1.2 shows a photomicrograph of onion epidermal cells.",
        topic_id=107)

    add_q(db, p3.id, exam_dir, 3, 1, "b",
        r"With reference to Fig. 1.1 and Fig. 1.2, describe one way in which the muscle cells are different from the onion epidermal cells.",
        1, "Cells", 8, (7, 0.55, 0.72),
        "Onion epidermal cells have a cell wall but the muscle cells do not have cell walls.", "B1",
        topic_id=107)

    add_q(db, p3.id, exam_dir, 3, 1, "c",
        r'Both figures 1.1 and 1.2 show tissues. Define the term "tissue".',
        1, "Cells & Tissues", 8, (7, 0.72, 0.90),
        "A tissue is made up of many cells of the same type performing the same function.", "B1",
        topic_id=107)

    add_q(db, p3.id, exam_dir, 3, 2, "a",
        r"The diagram shows a food web (Grass → Deer → Lion; Grass → Zebra → Ticks → Birds; Deer → Lion; Zebra → Lion). Name the primary consumers in this food web.",
        1, "Food Webs", 9, (8, 0.07, 0.40),
        "Deer and Zebra (both correct for the mark).", "B1",
        stem="The diagram shows a food web.",
        topic_id=111)

    add_q(db, p3.id, exam_dir, 3, 2, "b",
        r"What is the source of energy for this food web?",
        1, "Energy Flow", 9, (8, 0.40, 0.52),
        "Sunlight.", "B1",
        topic_id=111)

    add_q(db, p3.id, exam_dir, 3, 2, "c",
        r"Suggest, with reasons, what will happen to the zebra population if there is a sudden drought in the habitat.",
        2, "Ecology", 9, (8, 0.52, 0.80),
        "The zebra population will decrease — grass will dry up and not grow well, so there is not enough food and some zebra will die due to lack of food.", "B1, B1",
        topic_id=111)

    add_q(db, p3.id, exam_dir, 3, 3, "a",
        r"The diagram shows a classification chart for fish in a market. Using the information from the classification chart only, identify two characteristics of a pomfret.",
        1, "Classification", 10, (9, 0.07, 0.60),
        "Body without spots; forked tail; oval body (any two correct).", "B1",
        stem="The diagram shows a dichotomous classification chart of fish in a market.",
        topic_id=101)

    add_q(db, p3.id, exam_dir, 3, 3, "b",
        r"Identify a feature that can differentiate between a grouper and a mackerel.",
        1, "Classification", 10, (9, 0.60, 0.78),
        "Body of grouper has spots but body of mackerel has no spots.", "B1",
        topic_id=101)

    add_q(db, p3.id, exam_dir, 3, 3, "c",
        r"Is the classification chart shown above considered as a dichotomous key? Explain your answer.",
        1, "Classification", 11, (10, 0.07, 0.25),
        "Yes — it branches into 2 at each point and ends with the identification.", "B1",
        topic_id=101)

    add_q(db, p3.id, exam_dir, 3, 4, "a",
        r"Fig. 4 shows a section through part of the stem of a flowering plant. Name the structures labelled A and B.",
        2, "Transport in Plants", 11, (10, 0.25, 0.62),
        "A = phloem; B = xylem.", "B1, B1",
        stem="Fig. 4 shows a section through part of the stem of a flowering plant.",
        topic_id=110)

    add_q(db, p3.id, exam_dir, 3, 4, "b",
        r"State the function of each type of cell.",
        2, "Transport in Plants", 11, (10, 0.62, 0.92),
        "A (phloem) transports manufactured food / sucrose from the leaves to the other parts of the plant; B (xylem) transports water from the roots to the leaves and other parts of the plant.", "B1, B1",
        topic_id=110)

    add_q(db, p3.id, exam_dir, 3, 5, "a",
        r"Fig. 5 shows some red blood cells, as seen through a microscope. Name one structure, normally present in cells, that is not present in red blood cells.",
        1, "Blood", 12, (11, 0.07, 0.40),
        "Nucleus.", "B1",
        stem="Fig. 5 shows some red blood cells as seen through a microscope.",
        topic_id=110)

    add_q(db, p3.id, exam_dir, 3, 5, "b",
        r"State the main function of the red blood cells.",
        1, "Blood", 12, (11, 0.40, 0.55),
        "It transports oxygen from the lungs to the other parts of the body.", "B1",
        topic_id=110)

    add_q(db, p3.id, exam_dir, 3, 5, "c",
        r"Name one substance that is carried in the blood by the plasma.",
        1, "Blood", 12, (11, 0.55, 0.68),
        "Glucose / amino acids / fats / fatty acids / urea (any relevant).", "B1",
        topic_id=110)

    add_q(db, p3.id, exam_dir, 3, 5, "d",
        r"Complete the table to identify the components of blood that performs the function stated (helps the blood to clot; protects the body against infection).",
        2, "Blood", 12, (11, 0.68, 0.92),
        "Helps the blood to clot = platelets; protects the body against infection = white blood cells.", "B1, B1",
        topic_id=110)

    add_q(db, p3.id, exam_dir, 3, 6, "ai",
        r"Fig. 6 shows the cross-sections of three different types of blood vessels P, Q and R. In which blood vessel P, Q or R, is the blood flow the fastest and at a high pressure?",
        1, "Blood Vessels", 13, (12, 0.07, 0.32),
        "R (the artery).", "B1",
        stem="Fig. 6 shows the cross-sections of three different types of blood vessels P, Q and R.",
        topic_id=110)

    add_q(db, p3.id, exam_dir, 3, 6, "aii",
        r"Explain how the structure of this blood vessel helps it to withstand the high pressure.",
        1, "Blood Vessels", 13, (12, 0.32, 0.48),
        "The blood vessel has a thick muscular wall to withstand the high pressure of blood flowing through.", "B1",
        topic_id=110)

    add_q(db, p3.id, exam_dir, 3, 6, "bi",
        r"Which blood vessel P, Q or R, has valves along it?",
        1, "Blood Vessels", 13, (12, 0.48, 0.62),
        "P (the vein).", "B1",
        topic_id=110)

    add_q(db, p3.id, exam_dir, 3, 6, "bii",
        r"State the important function of the valves mentioned in part (b)(i) above.",
        1, "Blood Vessels", 13, (12, 0.62, 0.78),
        "Prevents backflow of blood / ensures that blood flows in one direction.", "B1",
        topic_id=110)

    add_q(db, p3.id, exam_dir, 3, 6, "c",
        r"Explain how the structure of S helps the blood vessel Q to perform its function.",
        2, "Blood Vessels", 13, (12, 0.78, 0.95),
        "The wall of the capillary is made up of only a single layer of cells, allowing exchange of substances to occur through it / allowing substances to pass between the blood and the cells easily.", "B1",
        topic_id=110)

    add_q(db, p3.id, exam_dir, 3, 7, "a",
        r"Fig. 7 shows a potted plant that was kept in the dark for 48 hours. One of its leaves was then placed in a bottle containing some sodium hydroxide. Write the word equation for photosynthesis.",
        1, "Photosynthesis", 14, (13, 0.07, 0.40),
        "carbon dioxide + water → (sunlight, chlorophyll) → glucose + oxygen.", "B1",
        stem="Fig. 7 shows a potted plant kept in the dark for 48 hours, with one leaf in a bottle of sodium hydroxide.",
        topic_id=111)

    add_q(db, p3.id, exam_dir, 3, 7, "b",
        r"The plant was left in bright sunlight for 10 hours. The leaves were then removed and tested for the presence of starch. Predict the results of the starch test for each part of leaf (P, Q, R) and state whether starch is present or absent.",
        3, "Photosynthesis", 14, (13, 0.40, 0.78),
        "P: iodine remains brown — starch absent (CO₂ absorbed by NaOH). Q: iodine turns blue-black — starch present. R: iodine turns blue-black — starch present.", "B1 x3",
        topic_id=111)

    add_q(db, p3.id, exam_dir, 3, 7, "c",
        r"What conclusion can be made from this experiment?",
        1, "Photosynthesis", 14, (13, 0.78, 0.92),
        "Carbon dioxide is required for photosynthesis to take place.", "B1",
        topic_id=111)

    add_q(db, p3.id, exam_dir, 3, 8, "a",
        r"An experiment was set up as in Fig. 8 to investigate what gas is released by green plants in darkness. At the end of the experiment limewater A remains clear but limewater B turns milky. Suggest a reason why this was observed for each solution.",
        2, "Respiration", 15, (14, 0.07, 0.55),
        "Limewater A — the sodium hydroxide solution absorbs carbon dioxide from the air in the set-up so no CO₂ reaches A. Limewater B — carbon dioxide is produced by the plant during the experiment (respiration), turning B milky.", "B1, B1",
        stem="An experiment was set up (Fig. 8) to investigate the gas released by green plants in darkness.",
        topic_id=111)

    add_q(db, p3.id, exam_dir, 3, 8, "b",
        r"Name the process that has occurred in the plant that has brought about the results observed in limewater B.",
        1, "Respiration", 15, (14, 0.55, 0.70),
        "Respiration.", "B1",
        topic_id=111)

    add_q(db, p3.id, exam_dir, 3, 8, "c",
        r"Name the sugar that is required for this process to take place.",
        1, "Respiration", 15, (14, 0.70, 0.85),
        "Glucose.", "B1",
        topic_id=111)

    # ══════════════════════════════════════════════
    # PAPER 2 — Physics Theory (35 marks)
    # Section A 15 marks (Q1-4), Section B 20 marks (Q5-6)
    # PDF pages 23-29 (idx 22-28)
    # ══════════════════════════════════════════════
    p2 = Paper(exam_id=exam.id, paper_number=2, duration_minutes=60, total_marks=35,
               date=date(2017, 10, 9), instructions="Section A (15 marks) and Section B (20 marks). Answer all questions.")
    db.add(p2); db.flush()

    add_q(db, p2.id, exam_dir, 2, 1, None,
        r"Convert the following quantities. Give your answer in non-standard form. (a) 420 000 m = ___ Mm  (b) 0.76 µA = ___ nA",
        3, "Units & Conversion", 23, (22, 0.07, 0.40),
        r"(a) $420\,000 / 10^6 = 0.42$ Mm. (b) $0.76 \times 10^{-6}$ A $= 760$ nA.", "A1, C1, A1",
        stem="Section A — Answer all questions.",
        topic_id=102)

    add_q(db, p2.id, exam_dir, 2, 2, "a",
        r"A ruler is used to measure the length of a piece of cotton, as shown in Fig. 2.1. Use the ruler in Fig. 2.1 to find the length of the piece of cotton.",
        1, "Measurement", 23, (22, 0.40, 0.65),
        r"Length $= 15.6 - 2.4 = 13.2$ cm.", "CAO1",
        stem="A ruler is used to measure a piece of cotton (Fig. 2.1).",
        topic_id=102)

    add_q(db, p2.id, exam_dir, 2, 2, "b",
        r"A rod has a square cross-section with thickness of 1.1 cm (Fig. 2.2). You are given the piece of cotton in Fig. 2.1 (without the ruler). Describe how you will use the piece of cotton (without using any ruler) to show that the thickness of the rod is 1.1 cm.",
        3, "Measurement", 23, (22, 0.65, 0.95),
        "Wind the piece of cotton around the rod and determine the number of rounds the cotton goes around the rod, then divide the cotton length by the number of rounds (and by 4 for the square cross-section) to get the thickness.", "B1 x3",
        topic_id=102)

    add_q(db, p2.id, exam_dir, 2, 3, "a",
        r"A vernier calipers is used to measure the external diameter of a test tube (Fig. 3.1 jaws closed, Fig. 3.2 jaws around tube). State the zero error.",
        1, "Measurement", 24, (23, 0.07, 0.40),
        r"Zero error $= -0.03$ cm.", "CAO1",
        stem="A vernier calipers is used to measure the external diameter of a test tube.",
        topic_id=102)

    add_q(db, p2.id, exam_dir, 2, 3, "b",
        r"Determine the external diameter of the test tube.",
        1, "Measurement", 24, (23, 0.40, 0.62),
        r"External diameter $= 3.16 - (-0.03) = 3.19$ cm.", "B1",
        topic_id=102)

    add_q(db, p2.id, exam_dir, 2, 3, "c",
        r"Explain why it is necessary to take more than one measurement at different positions to obtain an accurate value of the external diameter of the test tube.",
        1, "Measurement", 24, (23, 0.62, 0.80),
        "The test tube thickness may be uneven (the diameter may differ at different points).", "A1",
        topic_id=102)

    add_q(db, p2.id, exam_dir, 2, 4, "a",
        r"Fig. 4.1 shows a parachutist. Define gravitational field strength.",
        1, "Forces — Gravity", 25, (24, 0.07, 0.35),
        "Gravitational field strength is the gravitational force acting per unit mass on an object (weight divided by mass).", "B1",
        stem="Fig. 4.1 shows a parachutist.",
        topic_id=112)

    add_q(db, p2.id, exam_dir, 2, 4, "b",
        r"Draw and label on Fig. 4.1 all forces acting on the parachutist.",
        2, "Forces", 25, (24, 0.35, 0.55),
        "Upward force = air resistance; downward force = weight / gravitational force.", "B1, B1",
        topic_id=112)

    add_q(db, p2.id, exam_dir, 2, 4, "c",
        r"The weight of the parachutist is 800 N on Earth. The gravitational field strength on Earth is 10 N/kg and the gravitational field strength on the Moon is 1.6 N/kg. Determine the weight of the parachutist on the Moon.",
        2, "Forces — Weight", 25, (24, 0.55, 0.85),
        r"$m = W/g = 800/10 = 80$ kg. Weight on Moon $= 80 \times 1.6 = 128$ N $\approx 130$ N.", "B1, B1",
        topic_id=112)

    add_q(db, p2.id, exam_dir, 2, 5, "a",
        r"Fig. 5.1 shows the journey of a car travelling from O to R (O→P 500 km, P→Q 100 km, Q→R 450 km). Peter drives and takes 9 hours to travel O to P and 7 hours from Q to R. Peter took a break of 30 minutes and 42 minutes at P and Q respectively. State what is meant by the average speed.",
        1, "Speed", 26, (25, 0.07, 0.40),
        "Average speed = total distance divided by total time taken.", "A1",
        stem="Fig. 5.1 shows the journey of a car from O to R via P and Q.",
        topic_id=102)

    add_q(db, p2.id, exam_dir, 2, 5, "b",
        r"Determine the average speed of the car from O to P in km/h.",
        2, "Speed", 26, (25, 0.40, 0.75),
        r"Average speed $= 500/9 = 55.5 \approx 56$ km/h.", "C1, A1",
        topic_id=102)

    add_q(db, p2.id, exam_dir, 2, 5, "c",
        r"The car travel with the same average speed in (b) from P to Q. Determine the time taken (in hour) for the car to travel from P to Q.",
        2, "Speed", 26, (25, 0.75, 0.95),
        r"Time $= $ distance/speed $= 100/55.5 = 1.8$ h.", "C1, A1",
        topic_id=102)

    add_q(db, p2.id, exam_dir, 2, 5, "d",
        r"Determine the total time (in hour) that Peter took a break.",
        1, "Speed / Time", 27, (26, 0.07, 0.28),
        r"Total break time $= 30/60 + 42/60 = 1.2$ h.", "A1",
        topic_id=102)

    add_q(db, p2.id, exam_dir, 2, 5, "e",
        r"Determine the average speed of the car for the whole journey from O to R in km/h.",
        3, "Speed", 27, (26, 0.28, 0.62),
        r"Total distance $= 500 + 100 + 450 = 1050$ km. Total time $= 9 + 1.8 + 7 + 1.2 = 19$ h. Average speed $= 1050/19 = 55.3 \approx 55$ km/h.", "B1, B1, B1",
        topic_id=102)

    add_q(db, p2.id, exam_dir, 2, 5, "f",
        r"Convert the average speed of the car in (e) to m/s.",
        1, "Speed Conversion", 27, (26, 0.62, 0.82),
        r"$55 \text{ km/h} = 55 \times 1000/3600 = 15.3 \approx 15$ m/s.", "A1",
        topic_id=102)

    add_q(db, p2.id, exam_dir, 2, 6, "a",
        r"A student is investigating volume and density. The student has a box (Fig. 6.1, inside dimensions 4.0 cm × 4.0 cm × 5.0 cm) and some dry sand. Calculate the volume of sand needed to fill the box.",
        1, "Density / Volume", 28, (27, 0.07, 0.40),
        r"Volume $= 4 \times 4 \times 5 = 80$ cm³.", "A1",
        stem="A student is investigating volume and density using a box and dry sand.",
        topic_id=102)

    add_q(db, p2.id, exam_dir, 2, 6, "bi",
        r"The student measures the mass of the box empty (20 g) and when filled with sand (180 g). Define mass.",
        1, "Mass", 28, (27, 0.40, 0.58),
        "Mass is the amount of matter in a substance/object/body.", "A1",
        topic_id=102)

    add_q(db, p2.id, exam_dir, 2, 6, "bii",
        r"State the instrument used to measure the mass.",
        1, "Measurement", 28, (27, 0.58, 0.75),
        "Mass balance / electronic balance / beam balance.", "A1",
        topic_id=102)

    add_q(db, p2.id, exam_dir, 2, 6, "biii",
        r"Calculate the mass of the sand in the box.",
        1, "Mass", 29, (28, 0.07, 0.22),
        r"Mass of sand $= 180 - 20 = 160$ g.", "A1",
        topic_id=102)

    add_q(db, p2.id, exam_dir, 2, 6, "biv",
        r"Define density.",
        1, "Density", 29, (28, 0.22, 0.35),
        "Density is the mass per unit volume (mass divided by volume).", "A1",
        topic_id=102)

    add_q(db, p2.id, exam_dir, 2, 6, "bv",
        r"Calculate the density of the sand in g/cm³.",
        2, "Density", 29, (28, 0.35, 0.58),
        r"Density $= 160/80 = 2.0$ g/cm³.", "C1, A1",
        topic_id=102)

    add_q(db, p2.id, exam_dir, 2, 6, "bvi",
        r"Convert the density of the sand in (v) to kg/m³.",
        1, "Density Conversion", 29, (28, 0.58, 0.75),
        r"$2 \text{ g/cm}^3 = (2/1000)/(1/10^6) = 2000$ kg/m³.", "A1",
        topic_id=102)

    add_q(db, p2.id, exam_dir, 2, 6, "c",
        r"A miner has a bag containing a mixture of silver dust and sand. Silver has a density of 10.5 g/cm³. He heats the mixture until the silver melts. Predict what will happen to the sand. Explain your answer using the concept of density.",
        2, "Density", 29, (28, 0.75, 0.95),
        "The sand will float — sand (2.0 g/cm³) is less dense than molten silver (10.5 g/cm³), so it floats on top.", "B1, A1",
        topic_id=102)

    db.commit()
    p1_count = len(p1.questions)
    p2_count = len(p2.questions)
    p3_count = len(p3.questions)
    print(f"Seeded Pasir Ris Crest Science exam id={exam.id}: "
          f"Paper 1 MCQ ({p1_count}), Paper 2 Physics ({p2_count}), Paper 3 Biology ({p3_count})")
    print(f"Total questions: {p1_count + p2_count + p3_count}")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
