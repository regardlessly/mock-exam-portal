"""Seed Riverside Secondary School Mid-Year Examination 2013 Sec 1 Express Geography.

Source: smiletutor.sg Sec 1 Geography 2013 compilation PDF, Riverside section
(footer 2013/MYE/Humanities/Geography/1E, paper idx 137-144, End of Paper idx 144).
Subject = Geography. topic_id Geography range 301-312. Plain English, no LaTeX.
This paper is structured-only (no MCQ section), so the bank fragment is empty.
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
        .filter(School.name == "Riverside Secondary School")
        .first()
    )
    if not school:
        school = School(name="Riverside Secondary School")
        db.add(school)
        db.flush()

    existing = (
        db.query(Exam)
        .filter(Exam.school_id == school.id, Exam.year == 2013,
                Exam.subject == "Geography")
        .first()
    )
    if existing:
        print(f"Riverside Geography 2013 already seeded (id={existing.id}). "
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
        source_pdf="smiletutor_sec1geog_2013.pdf (Riverside section)",
        status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)

    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=90,
               total_marks=50, date=date(2013, 5, 1),
               instructions="Section A Basic Technique, Section B Atlas & Map "
                            "Reading, Section C Structured Essay. Answer all "
                            "questions.")
    db.add(p1)
    db.flush()

    # ── Section A: Basic Technique ──
    add_q(db, p1.id, exam_dir, 1, 1, None,
          "Study Figure A (table of the planets: distance from the Sun, number of "
          "moons, diameter in km — Mercury, Venus, Earth, Mars, Jupiter, Saturn, "
          "Uranus, Neptune). (a) Which planet is the third largest in diameter? "
          "(b) Calculate the difference in diameter between the largest and "
          "smallest planets. (c) Calculate the distance between Jupiter and the "
          "Sun. (d) Identify the planet which has the larger number of moons "
          "between Jupiter and Mercury.",
          5, "Basic Technique", 139, (138, 0.0, 0.55),
          "(a) Read from the table — the planet with the third largest diameter "
          "(e.g. Uranus). (b) Largest diameter (Jupiter) minus smallest diameter "
          "(Mercury), using the figures in the table. (c) Read the distance from "
          "the Sun column for Jupiter. (d) Jupiter has far more moons than "
          "Mercury.",
          "B1 per correct reading/calculation",
          stem="Figure A: table of planet data (distance from the Sun, number of "
               "moons, diameter in km).",
          topic_id=303)

    # ── Section B Part 1: Atlas [10 marks] ──
    add_q(db, p1.id, exam_dir, 1, 2, None,
          "Study Figure B (world map with labelled A, B, C, D and lines). "
          "(a) What is the latitude 23.5 S known as? (b) What are the names of "
          "continents A and B? (c) What is the name of ocean C? (d) What is the "
          "name of the mountain range in continent D? (e) Name the land mass "
          "found at 90 S of the equator.",
          6, "Atlas / Maps", 139, (138, 0.53, 1.0),
          "(a) Tropic of Capricorn. (b) Continents A and B as labelled on the "
          "world map. (c) Ocean C as labelled. (d) The major mountain range in "
          "continent D. (e) Antarctica.",
          "B1 per correct answer",
          stem="Figure B: world map with labelled continents A and B, ocean C, "
               "continent D and lines of latitude.",
          topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 3, None,
          "Study the map extract (world map with points W, X, Y and Z). Find the "
          "latitudes and longitudes of W, X, Y and Z.",
          4, "Atlas / Maps", 140, (139, 0.30, 1.0),
          "Give the latitude and longitude pair for each point W, X, Y and Z "
          "read off the gridded world map.",
          "B1 per correct coordinate pair",
          stem="World map extract with four marked points W, X, Y and Z on a "
               "latitude-longitude grid.",
          topic_id=301)

    # ── Section B Part 2: Map Reading [15 marks] ──
    add_q(db, p1.id, exam_dir, 1, 4, None,
          "Study the topographical map (scale 1:50 000, with legend: contour "
          "lines in metres, houses, rubber tree plantation, mangrove swamp, road, "
          "bridge, embankment, trigonometrical station). Answer: (a) Find the "
          "four-figure grid reference of Factory B. (b) Find the six-figure grid "
          "reference of the school. (c) Find the six-figure grid reference of the "
          "sawmill. (d) What is the contour interval of the map? (e) What is the "
          "direction of the school from the police station? (f) Find the distance "
          "travelled by road from the school to the police station (to the "
          "nearest 0.1 km). (g) Identify the landform found in grid reference "
          "2919 and justify your answer with evidence from the map. (h) Find the "
          "compass bearing of the trigonometrical station in GR 2318 from the "
          "trigonometrical station in GR 2919. (j) Find the compass bearing of "
          "the school from the sawmill. (i) What is the settlement pattern found "
          "in GR 2817 and state a reason why it is such?",
          15, "Map Reading", 141, (140, 0.0, 1.0),
          "(a) e.g. 2715 (Factory B). (b) six-figure GR of the school. (c) "
          "six-figure GR of the sawmill. (d) contour interval read from the map "
          "(e.g. 20 m). (e) direction of school from police station. (f) road "
          "distance to nearest 0.1 km using the 1:50 000 scale. (g) landform in "
          "GR 2919 (e.g. valley/spur) with contour evidence. (h) compass bearing "
          "between the two trigonometrical stations. (j) bearing of school from "
          "sawmill. (i) settlement pattern (e.g. linear/clustered) with reason "
          "such as proximity to road or river.",
          "B1/B2 per answer; map-skills marking",
          stem="Topographical map, scale 1:50 000, with legend (contour lines in "
               "metres, houses, rubber tree plantation, mangrove swamp, road, "
               "bridge, embankment, trigonometrical station).",
          topic_id=301)

    # ── Section C: Structured Essay ──
    add_q(db, p1.id, exam_dir, 1, 5, "a",
          "Explain the effect of Earth's rotation in a 24 hour time period.",
          2, "Earth's Rotation", 142, (141, 0.0, 0.18),
          "As the Earth rotates once on its axis every 24 hours, the half facing "
          "the Sun experiences day while the half facing away experiences night; "
          "this causes the cycle of day and night.",
          "B2",
          topic_id=303)

    add_q(db, p1.id, exam_dir, 1, 5, "b",
          "Study Figure C below and answer the following question. Identify the "
          "type of landform shown above and describe its formation.",
          3, "Landforms", 142, (141, 0.16, 0.55),
          "Identify the landform shown (e.g. a fold mountain / steep peak) and "
          "describe its formation by compression of crustal rocks pushing layers "
          "up into folds.",
          "B-marks for identification + formation",
          stem="Figure C: photograph of a mountain landform.",
          topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 5, "c",
          "Study Figure D below and describe how convection currents cause "
          "crustal movements.",
          4, "Crustal Movements", 142, (141, 0.53, 0.85),
          "Heat from the Earth's core heats the mantle, causing hot magma to "
          "rise; as it cools it sinks, forming convection currents. These "
          "currents drag the crustal plates, causing them to move apart or "
          "together (continents move apart / move together).",
          "B-marks per stage",
          stem="Figure D: diagram of convection currents in the mantle with "
               "continents moving apart and together.",
          topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 5, "d",
          "Using clear examples, describe three types of crustal movements.",
          6, "Crustal Movements", 142, (141, 0.83, 1.0),
          "Convergent (plates move together, e.g. forming fold mountains/"
          "subduction); Divergent (plates move apart, e.g. mid-ocean ridges); "
          "Transform (plates slide past each other, e.g. faults causing "
          "earthquakes).",
          "B2 per type with example",
          topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 6, "a",
          "Describe how the !Kung Bushmen adapt to the hot daytime and cold "
          "night-time environment of the Kalahari desert.",
          3, "Adaptation / Vegetation", 143, (142, 0.0, 0.30),
          "By day they wear minimal clothing and rest in shade; at night they "
          "build fires and shelter in simple huts of branches and grass to keep "
          "warm; they move in search of food and water and store water in "
          "ostrich eggshells.",
          "B-marks per adaptation",
          topic_id=311)

    add_q(db, p1.id, exam_dir, 1, 6, "b",
          "Study the picture below (cover of a tourist brochure 'Explore Mount "
          "Kilimanjaro'). In which country is this volcano located? Explain why "
          "this volcano is safe for tourism activities.",
          3, "Volcanoes / Tourism", 143, (142, 0.28, 0.70),
          "Mount Kilimanjaro is located in Tanzania. It is considered safe "
          "because it is a dormant/extinct volcano with no recent eruptions, so "
          "the risk to tourists is low.",
          "B-marks for country + reason",
          stem="Tourist brochure cover: 'Explore Mount Kilimanjaro — Marangu, "
               "Machame and Rongai routes'.",
          topic_id=312)

    add_q(db, p1.id, exam_dir, 1, 6, "c",
          "With the aid of well-labelled diagrams, identify the features of a "
          "volcano.",
          5, "Volcanoes", 144, (143, 0.0, 0.35),
          "Labelled features: magma chamber, vent, crater, cone (layers of lava "
          "and ash), side vent, lava flow, ash cloud.",
          "B1 per correctly labelled feature",
          topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 6, "d",
          "With reference to the map of the Pacific Ring of Fire, cite a volcano "
          "that you have studied in the region marked in the box. Describe the "
          "risks of living near a volcano.",
          4, "Volcanoes", 144, (143, 0.33, 1.0),
          "Cite a volcano from the boxed Southeast Asia region (e.g. a volcano "
          "in Indonesia/Philippines). Risks: loss of life and property from "
          "eruptions, lava flows and ash; respiratory health problems; "
          "destruction of crops and disruption to travel.",
          "B-marks for example + risks",
          stem="Map of the Pacific Ring of Fire with a boxed region in Southeast "
               "Asia.",
          topic_id=310)

    db.commit()
    print(f"Seeded Riverside Geography 2013 exam id={exam.id}: "
          f"{len(p1.questions)} question rows.")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
