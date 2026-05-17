"""Seed Zhenghua Secondary School Mid-Year Examination 2013 Sec 1 Express Geography.

Source: smiletutor.sg Sec 1 Geography 2013 compilation PDF, Zhenghua section
(question paper idx 123-130, End of Paper idx 130; mark scheme idx 131-136).
Subject = Geography. topic_id Geography range 301-312. Plain English, no LaTeX.
Model answers taken from the paper's own mark scheme.
This paper is structured/mapwork-only (no MCQ section), so the bank fragment
is empty.
"""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/smiletutor_sec1geog_2013.pdf"

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

    school = (
        db.query(School)
        .filter(School.name == "Zhenghua Secondary School")
        .first()
    )
    if not school:
        school = School(name="Zhenghua Secondary School")
        db.add(school)
        db.flush()

    existing = (
        db.query(Exam)
        .filter(Exam.school_id == school.id, Exam.year == 2013,
                Exam.subject == "Geography")
        .first()
    )
    if existing:
        print(f"Zhenghua Geography 2013 already seeded (id={existing.id}). "
              f"Re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id,
        title="Mid-Year Examination 2013 (Geography)",
        year=2013, level="Secondary 1 Express", subject="Geography",
        source_pdf="smiletutor_sec1geog_2013.pdf (Zhenghua section)",
        status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)

    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=90,
               total_marks=70, date=date(2013, 5, 1),
               instructions="Section A Mapwork (20 marks), Section B Basic "
                            "Techniques & Short Answer (15 marks), Section C "
                            "Structured Questions (45 marks). Answer all "
                            "questions.")
    db.add(p1)
    db.flush()

    # ── Section A: Mapwork [20 marks] ──
    add_q(db, p1.id, exam_dir, 1, 1, None,
          "Refer to the Treasure Bay Map. Study the map and answer questions "
          "1a to 1j. (a) Name the table of the map which shows the list of "
          "symbols (X). (b) State the contour interval of the contour lines. "
          "(c) State the four-figure grid reference of Lake Diamond. (d) State "
          "the six-figure grid reference of the school. (e) State the direction "
          "of the church from Lake Diamond. (f) State the bearing from the "
          "school to the Post Office. (g) Calculate the straight-line distance "
          "between the Police Station and the school. Show your workings; "
          "express your answer in metres. (h) Measure and calculate the length "
          "of the major road. Show your workings; express your answer in metres. "
          "(i) State the 4-figure grid reference of the grid with the steepest "
          "slope on the map and explain your answer. (j) State the highest "
          "physical feature on the map and give its height.",
          20, "Maps & Map Reading", 125, (124, 0.0, 1.0),
          "(a) The Legend / Key. (b) Contour interval read from the map. "
          "(c) Four-figure GR of Lake Diamond. (d) 0603 (six-figure GR of the "
          "school). (e) North-east. (f) Bearing from school to Post Office "
          "measured with a protractor. (g) Multiply the measured map distance by "
          "the 1:50 000 scale; show working; answer in metres. (h) Measure the "
          "road length with thread/ruler, convert using the scale, show working "
          "in metres. (i) The grid with the most closely-spaced contour lines is "
          "the steepest; give its 4-figure GR and cite the close contour "
          "spacing as evidence. (j) The highest point/hill with its stated "
          "height in metres. (Per the paper's mark scheme.)",
          "B1/B2 per part; M1 for scale workings",
          stem="Treasure Bay topographical map, scale 1:50 000, with legend "
               "(major road, minor road, contour lines in metres, lake, "
               "seasonal river, swamp, sand & mud, flat rock, scrub, sea, sugar "
               "cane plantation, church, building, school).",
          topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 2, None,
          "Fig.1 shows an annual rainfall map of Singapore. (a) Which area "
          "experiences the lowest average annual rainfall? (b) Which three areas "
          "receive an annual rainfall between 2200 mm and 2300 mm? (c) State the "
          "area that experiences the highest average annual rainfall and give "
          "one example of how Singapore uses it for its water needs.",
          6, "Climate Graphs & Data Interpretation", 126, (125, 0.0, 1.0),
          "(a) The area with the lowest rainfall band on Fig.1. (b) The three "
          "areas falling in the 2200-2300 mm class on the legend. (c) The area "
          "with the highest rainfall — Singapore uses it by collecting the "
          "rainwater in reservoirs/catchment areas (e.g. as part of the local "
          "catchment water tap).",
          "B1 per correct reading",
          stem="Fig.1: annual rainfall map of Singapore with a rainfall-band "
               "legend and labelled areas.",
          topic_id=305)

    # ── Section B: Basic Techniques & Short Answer [15 marks] ──
    add_q(db, p1.id, exam_dir, 1, 3, "a",
          "Explain the difference between weather and climate.",
          2, "Weather & Climate", 127, (126, 0.0, 0.30),
          "Weather is the condition of the atmosphere over a short period of "
          "time, whereas climate is the weather pattern over a long period of "
          "time. (1 mark per comparison.)",
          "B2 (1 mark per comparison)",
          topic_id=303)

    add_q(db, p1.id, exam_dir, 1, 3, "b",
          "Fig.2 shows a Stevenson Screen. Explain 2 characteristics of a "
          "Stevenson Screen.",
          2, "Weather & Climate: Instruments", 127, (126, 0.28, 0.78),
          "Any two with explanation: painted white to reflect heat; has louvres "
          "to allow free air circulation; raised on stilts about 1.2 m above "
          "the ground so that heat from the ground does not affect the readings. "
          "(1 mark for characteristic, 1 mark for explanation.)",
          "B1 characteristic + B1 explanation",
          stem="Fig.2: diagram of a Stevenson Screen.",
          topic_id=303)

    add_q(db, p1.id, exam_dir, 1, 4, "a",
          "State the three types of crustal movement.",
          3, "Crustal Movements", 127, (126, 0.0, 0.55),
          "Convergent, Divergent and Transform. (1 mark each.)",
          "B1 per type",
          topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 4, "b",
          "Explain folding.",
          2, "Crustal Movements", 127, (126, 0.53, 1.0),
          "Folding occurs when two plates collide with each other; some layers "
          "of the rock from the Earth's crust buckle and form folds.",
          "B2",
          topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 5, "a",
          "Fig.3 shows a photo of a type of environment. Identify the change to "
          "the environment.",
          1, "Environments", 128, (127, 0.0, 0.45),
          "The natural environment has been changed/built up (forest cleared "
          "and replaced with human structures).",
          "B1",
          stem="Fig.3: photograph of a type of environment.",
          topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 5, "b",
          "Identify the type of environment and explain 1 possible impact on "
          "humans from the change.",
          3, "Environments", 128, (127, 0.43, 0.78),
          "It is a human (built) environment. Possible impact: pollution from "
          "the development can affect human health; or loss of natural land "
          "affects resources available to humans.",
          "B-marks for identification + impact",
          topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 5, "c",
          "Explain the difference between physical and human environments.",
          2, "Environments", 128, (127, 0.76, 1.0),
          "A physical environment consists of natural features not made by "
          "people (e.g. rivers, forests), whereas a human environment consists "
          "of features built or created by people (e.g. houses, roads).",
          "B2",
          topic_id=301)

    # ── Section C: Structured Questions [45 marks] ──
    add_q(db, p1.id, exam_dir, 1, 6, "a",
          "Fig.4 shows the climograph of Country X. Describe the rainfall and "
          "temperature patterns of the entire year shown in Fig.4.",
          4, "Climate Graphs & Data Interpretation", 131, (130, 0.0, 1.0),
          "Rainfall: highest in May with evidence from the graph; describe the "
          "pattern through the year with figures. Temperature: rises from "
          "around -10 C in January to about 17 C in May and decreases to about "
          "-8 C in December. (Use values read from Fig.4.)",
          "Levelled marking with evidence from the graph",
          stem="Fig.4: climograph of Country X (rainfall bars and temperature "
               "line by month).",
          topic_id=305)

    add_q(db, p1.id, exam_dir, 1, 6, "b",
          "Calculate the mean annual temperature for Country X. Show your "
          "working.",
          2, "Climate Graphs & Data Interpretation", 131, (130, 0.0, 1.0),
          "Mean annual temperature = (sum of the 12 monthly temperatures) / 12. "
          "Show the working with the values read from Fig.4.",
          "M1 for working, A1 for answer",
          topic_id=305)

    add_q(db, p1.id, exam_dir, 1, 6, "c",
          "Calculate the annual temperature range. Show your working.",
          2, "Climate Graphs & Data Interpretation", 131, (130, 0.0, 1.0),
          "Annual temperature range = maximum temperature minus minimum "
          "temperature; e.g. 17 C - (-10) C = 27 C (using the values from "
          "Fig.4).",
          "M1 for working, A1",
          topic_id=305)

    add_q(db, p1.id, exam_dir, 1, 6, "d",
          "Calculate the total annual rainfall for Country X. Show your "
          "working.",
          2, "Climate Graphs & Data Interpretation", 131, (130, 0.0, 1.0),
          "Total annual rainfall = sum of all 12 monthly rainfall values read "
          "from Fig.4; show the addition.",
          "M1 for working, A1",
          topic_id=305)

    add_q(db, p1.id, exam_dir, 1, 6, "e",
          "Based on your answers above, state the climate of Country X.",
          1, "Factors Affecting Temperature & Rainfall", 131, (130, 0.0, 1.0),
          "Temperate climate.",
          "B1",
          topic_id=304)

    add_q(db, p1.id, exam_dir, 1, 6, "f",
          "Identify the instrument used for collecting rainwater.",
          1, "Weather & Climate: Instruments", 131, (130, 0.0, 1.0),
          "Rain gauge.",
          "B1",
          topic_id=303)

    add_q(db, p1.id, exam_dir, 1, 6, "g",
          "State 3 requirements for the use of a rain gauge.",
          3, "Weather & Climate: Instruments", 131, (130, 0.0, 1.0),
          "Place it in an open area away from buildings/trees so there are no "
          "obstructions to block the rain; place it away from concrete surfaces "
          "to prevent additional water from splashing into the rain gauge; sink "
          "the soil for partial burial to make the rain gauge more stable.",
          "B1 per requirement",
          topic_id=303)

    add_q(db, p1.id, exam_dir, 1, 7, "a",
          "Fig.5 shows a diagram of a tropical rainforest. Explain 2 "
          "characteristics for all three layers of a tropical rainforest.",
          6, "Tropical Rainforest Ecosystems", 131, (130, 0.0, 1.0),
          "Emergent layer: tallest trees that grow very tall (45-50 m); buttress "
          "roots to support the trees. Canopy layer: forms a continuous layer "
          "of leaves that blocks out 70-100% of sunlight; lianas and epiphytes "
          "common. Undergrowth: receives little sunlight, so few plants; cool "
          "and moist interior. (1 mark per characteristic.)",
          "B1 per characteristic",
          stem="Fig.5: diagram of a tropical rainforest with emergent, canopy "
               "and undergrowth layers.",
          topic_id=309)

    add_q(db, p1.id, exam_dir, 1, 7, "b",
          "Describe how the leaves of the trees in tropical rainforests adapt "
          "to the tropical climate.",
          3, "Tropical Rainforest Ecosystems", 131, (130, 0.0, 1.0),
          "Leaves have waxy drip-tips to allow excess water to flow off quickly "
          "as the rainfall is abundant; thin leaves to lose moisture and reduce "
          "weight; broad leaves to absorb as much sunlight as there is "
          "competition for sunlight.",
          "B1 per adaptation",
          topic_id=309)

    add_q(db, p1.id, exam_dir, 1, 7, "c",
          "Explain, using examples, three benefits of natural vegetation.",
          6, "Natural Vegetation & Biomes", 131, (130, 0.0, 1.0),
          "Natural resource — e.g. wood/timber for construction. Medicinal "
          "purpose — e.g. raw material for medicines. Recreation — e.g. leisure "
          "activities/ecotourism. Oxygen production — trees release oxygen for "
          "all living creatures. Formation of rain — transpiration contributes "
          "to cloud formation. Prevent soil erosion — roots hold soil together. "
          "Natural habitats — provides homes for animals. (Any three with "
          "examples; per the mark scheme.)",
          "B1 per benefit with example",
          topic_id=311)

    add_q(db, p1.id, exam_dir, 1, 8, "a",
          "State where most volcanoes and fold mountains are found and provide "
          "one example of a fold mountain.",
          2, "Crustal Movements", 131, (130, 0.0, 0.30),
          "Most volcanoes and fold mountains are found along plate boundaries "
          "(e.g. the Pacific Ring of Fire / where plates collide). Example of a "
          "fold mountain: the Himalayas (accept other reasonable examples such "
          "as Mount Everest).",
          "B1 + B1",
          topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 8, "b",
          "Explain the 2 differences between an active volcano and an extinct "
          "volcano.",
          2, "Crustal Movements", 131, (130, 0.0, 0.45),
          "An active volcano is one that is erupting recently/now and is "
          "expected to erupt again; an extinct volcano is one which has not "
          "erupted in a long time and is not expected to erupt again in the "
          "future.",
          "B1 per difference",
          topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 8, "c",
          "State 3 risks and 3 benefits of living close to a volcano.",
          6, "Variable Weather & Climate Change", 131, (130, 0.0, 0.65),
          "Risks: ash in the air can cause breathing difficulties, skin disease "
          "and serious eye infections; eruption may result in the destruction "
          "of land used for farming and loss of livelihood; lava flows can "
          "destroy homes; death by pyroclastic bombs. Benefits: volcanic ash is "
          "very fertile, good for farming; valuable gems and minerals on the "
          "surface; tourism brings income; geothermal energy. (Per the mark "
          "scheme.)",
          "B1 per risk/benefit",
          topic_id=310)

    add_q(db, p1.id, exam_dir, 1, 8, "d",
          "Identify 3 adaptations people make to survive living close to a "
          "volcano.",
          3, "Variable Weather & Climate Change", 131, (130, 0.0, 0.80),
          "Evacuation plans and drills to ensure people can get out safely; "
          "volcanic hazard maps to guide people in placing their homes; "
          "distribution of masks and survival kits to protect people; regular "
          "inspection/monitoring of volcanoes.",
          "B1 per adaptation",
          topic_id=310)

    add_q(db, p1.id, exam_dir, 1, 8, "e",
          "State the 2 characteristics of a plateau.",
          2, "Relief, Photographs & GIS", 131, (130, 0.0, 1.0),
          "A plateau is a raised area of land with a flat broad top (1m) and "
          "steep slopes (1m).",
          "B1 per characteristic",
          topic_id=302)

    db.commit()
    print(f"Seeded Zhenghua Geography 2013 exam id={exam.id}: "
          f"{len(p1.questions)} question rows.")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
