"""Seed First Toa Payoh Secondary School Mid-Year 2012 Sec 1 Express Geography exam."""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/smiletutor_2013.pdf"

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

    school = db.query(School).filter(School.name == "First Toa Payoh Secondary School").first()
    if not school:
        school = School(name="First Toa Payoh Secondary School")
        db.add(school)
        db.flush()

    existing = (db.query(Exam)
                .filter(Exam.school_id == school.id, Exam.year == 2012,
                        Exam.subject == "Geography")
                .first())
    if existing:
        print(f"FTPSS Geography 2012 already seeded (id={existing.id}). Re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id, title="Mid-Year Examination 2012", year=2012,
        level="Secondary 1 Express", subject="Geography",
        source_pdf="smiletutor_2013.pdf (First Toa Payoh 2012 Geography)", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)

    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=90, total_marks=90,
               date=date(2012, 5, 1), instructions="Answer all questions. Section A on the Optical Answer Sheet; Sections B and C in the question paper.")
    db.add(p1); db.flush()

    # ── SECTION A — MCQ (Q1-15, 15 marks) idx 31-33 ──
    add_q(db, p1.id, exam_dir, 1, 1, None,
        "Which of the following are components of the physical environment? A) Air, land, water, waste  B) Air, soil, buildings, climate  C) Air, land, water, living environment  D) Solar system, temperature, wind, rain",
        1, "Physical Environment", 31, (31, 0.10, 0.30),
        "C) Air, land, water and the living environment make up the physical environment.", "B1",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 2, None,
        "With reference to the photograph, which of the following statements is True? A) The photograph shows a physical environment only.  B) The photograph shows physical features only.  C) The photograph shows how human environment is modified by man.  D) The photograph shows how physical environment is modified by man.",
        1, "Physical & Human Environment", 31, (31, 0.30, 0.78),
        "D) The photograph shows how the physical environment is modified by man.", "B1",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 3, None,
        "Which of the following is an example of a human feature? A) Ponds  B) Rivers  C) Reservoirs  D) Sea",
        1, "Physical & Human Features", 31, (31, 0.78, 0.95),
        "C) Reservoirs are man-made, so they are a human feature.", "B1",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 4, None,
        "Which of the following explains why the Earth is fragile? A) Human activities like driving a car, release toxic gases which is harmful to life on Earth  B) Many plants and trees are becoming extinct due to deforestation  C) The Earth is getting hotter because it is moving nearer to the Sun  D) All of the above",
        1, "Fragile Earth", 32, (32, 0.05, 0.22),
        "A) Human activities such as driving release toxic gases harmful to life on Earth.", "B1",
        topic_id=310)

    add_q(db, p1.id, exam_dir, 1, 5, None,
        "Which of the following pairs of items are useful natural resources? A) Motor vehicles and power stations  B) Electricity and fire  C) Fire and electronic gadgets  D) Water and wood",
        1, "Natural Resources", 32, (32, 0.22, 0.38),
        "D) Water and wood are natural resources.", "B1",
        topic_id=308)

    add_q(db, p1.id, exam_dir, 1, 6, None,
        "Technology is ____. A) old machinery  B) learning new skills  C) teaching new skills to people  D) understanding the environment",
        1, "Technology & Environment", 32, (32, 0.38, 0.55),
        "C) Technology involves teaching/applying new skills (knowledge applied to solve problems).", "B1",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 7, None,
        "The five main oceans on Earth are Atlantic, Pacific, ____. A) Indian, Arctic and Southern  B) African, Arctic and Southern  C) Indian, African and Southern  D) Indian, Arctic and Antarctica",
        1, "Oceans", 32, (32, 0.55, 0.72),
        "A) Indian, Arctic and Southern (the five oceans: Pacific, Atlantic, Indian, Arctic, Southern).", "B1",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 8, None,
        "Maps have many uses. Which of the following is not one of them? A) Sources of information  B) Proof of human existence  C) Record of changes  D) Tools used in planning",
        1, "Maps", 32, (32, 0.72, 0.88),
        "B) Proof of human existence is not a use of maps.", "B1",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 9, None,
        "All topographical maps have vertical grid lines called ____ and horizontal grid lines called ____. A) Eastings, Northings  B) Northings, Eastings  C) Latitudes, Longitudes  D) Longitudes, Latitudes",
        1, "Grid References", 32, (32, 0.88, 0.97),
        "A) Vertical grid lines are Eastings; horizontal grid lines are Northings.", "B1",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 10, None,
        "Different ____ on maps are used to show sizes and levels of details. A) scales  B) rulers  C) grid references  D) arrows",
        1, "Map Scale", 33, (33, 0.05, 0.18),
        "A) Different scales are used to show sizes and levels of detail.", "B1",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 11, None,
        "When plates meet, ____ mountains are often formed. A) rift  B) block  C) fold  D) horst",
        1, "Plate Tectonics — Fold Mountains", 33, (33, 0.18, 0.32),
        "C) Fold mountains are often formed when plates meet (collide).", "B1",
        topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 12, None,
        "The belt around the Pacific Ocean where a large number of the world's volcanoes are found is called ____. A) Pacific Ring of Five  B) Pacific Ring of Fire  C) Pacific Ocean of Five  D) Pacific Ocean of Fire",
        1, "Volcanoes — Ring of Fire", 33, (33, 0.32, 0.48),
        "B) The Pacific Ring of Fire.", "B1",
        topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 13, None,
        "The Earth's crust is made up of several ____ which can slide past, pull apart from or push towards each other. A) oceans  B) internal forces  C) magma chambers  D) plates",
        1, "Plate Tectonics", 33, (33, 0.48, 0.64),
        "D) The Earth's crust is made up of several plates.", "B1",
        topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 14, None,
        "Which of the following is not an element of climate? A) Wind  B) Air pressure  C) Temperature  D) Dust particles",
        1, "Elements of Climate", 33, (33, 0.64, 0.80),
        "D) Dust particles are not an element of climate.", "B1",
        topic_id=303)

    add_q(db, p1.id, exam_dir, 1, 15, None,
        "The temperate climate experiences ____. A) four seasons in a year  B) high rainfall all year round  C) high temperature all year round  D) extreme and harsh conditions all year round",
        1, "Climate Types", 33, (33, 0.80, 0.97),
        "A) The temperate climate experiences four seasons in a year.", "B1",
        topic_id=304)

    # ── SECTION B Part I — Mapwork (Q1, 15 marks) idx 34-35 ──
    add_q(db, p1.id, exam_dir, 1, 16, None,
        "Section B Part I (Mapwork). Refer to the map of Nashville. (a) Name two natural features shown in the map [2]; (b) In which grid square is the Post Office found? [1]; (c) Six-figure grid reference of the Hospital [1]; (d) Feature found in grid square (5186) [1]; (e) Direction of Factory A from the Hospital [1]; (f) Measure the straight line distance of Grace Road in km, showing working [2]; (g) Measure the curved distance of River Monash in km, showing working [2]; (h) Bearing of Factory A from the Post Office [2]; (i) Contour interval of this map [1]; (j) Highest point shown on this map [1]; (k) Other than education and marketing facilities, name one other facility provided for the people in Nashville town [1].",
        15, "Mapwork & Map Reading", 34, (34, 0.05, 0.97),
        "Use the Nashville map, its grid lines, scale and contour pattern: (a) e.g. river, swamp/hill; (b)/(c)/(d) read eastings then northings; (e)/(h) use the north arrow/compass; (f)/(g) measure with ruler/string then apply 1:50 000 scale; (i) from contour values; (j) highest spot height; (k) e.g. hospital / post office.",
        "Marks per part as shown (total 15).", topic_id=301)

    # ── SECTION B Part II — Basic Techniques (Q2-3, 10 marks) idx 36-37 ──
    add_q(db, p1.id, exam_dir, 1, 17, None,
        "Section B Part II (Basic Techniques). Study the weather forecast for Singapore from 16th-19th March 2012 and the detailed forecast for Monday 19th March. (a) Mary is planning for a picnic with her friends — suggest a date for her and explain why [2]; (b) Calculate the daily temperature range for 16th March 2012 [1]; (c) Calculate the mean daily temperature for 19th March 2012 [1]; (d) Describe the weather forecasted for 19th March 2012 [2].",
        6, "Weather Data — Interpretation", 36, (36, 0.05, 0.97),
        "(a) Choose a day with mix of cloud and sun (16 Mar) — least rain, suitable for a picnic. (b) range = 32 - 25 = 7 deg C. (c) mean = (25 + 28 + 32 + 29) / 4 = 28.5 deg C (using the four readings). (d) thundershowers with high temperatures around 32 deg C in the afternoon, cooler at night.",
        "Marks as shown.", topic_id=303)

    add_q(db, p1.id, exam_dir, 1, 18, None,
        "Study the climograph of country A. (a) Using information from the climograph, identify and describe the climate of country A [3]; (b) How do you think people adapt to life in country A? [2].",
        5, "Climate Graphs", 37, (37, 0.05, 0.60),
        "(a) Temperate climate — warm summers (about 16 deg C mid-year peak) and cool winters, with rainfall spread through the year; clear seasonal temperature variation. (b) People wear thicker clothing in winter, heat homes, and adjust farming/activities to the seasons.",
        "B3/B2.", topic_id=305)

    # ── SECTION C — Structured Essay (50 marks) idx 38-44 ──
    add_q(db, p1.id, exam_dir, 1, 19, None,
        "Section C, Q1. (a) Define physical environment [1]. Study Figures 1 and 2 and answer: (b) Compare and contrast how human beings shown in Figures 1 and 2 interact with the physical environment [4]. (c) Describe how people have changed the environment as shown in Figure 3 [2]. (d) Referring to your observations in (c), evaluate the impact of human activities on the environment shown in Figure 3 [3].",
        10, "People & Physical Environment", 38, (38, 0.05, 0.97),
        "(a) The physical environment is the natural surroundings — air, water, land and living things — not made by humans. (b) compare/contrast traditional vs modern interaction; (c) urbanisation/construction/transport changes; (d) impacts: loss of natural land, pollution, but provision of housing/infrastructure.",
        "Marks as shown.", topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 20, None,
        "Section C, Q2. Figure 4 shows a volcano that had just erupted. (a) Name the parts A and B and state their functions [4]; (b) Using an example, explain why the volcano is shaped as such in Figure 4 [3]; (c) Explain why people still live near volcanoes despite the dangers of eruption [3].",
        10, "Volcanoes", 40, (40, 0.05, 0.97),
        "(a) e.g. A = vent/crater (allows magma/lava to escape), B = magma chamber (stores magma) - label from figure. (b) repeated eruptions of lava and ash build up layers forming a cone-shaped (composite) volcano. (c) fertile volcanic soils, geothermal energy, tourism, mineral resources and attachment to home.",
        "Marks as shown.", topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 21, None,
        "Section C, Q3. Study the photographs of Singapore (Figures 5 and 6). (a) Figures 5 and 6 show two different types of photographs - identify each type of photograph [2]; (b) State one strength and one limitation of the photograph type shown in Figure 6 [2]; (c) Which photograph would be more useful in the detection of fires? Briefly explain your choice [2].",
        6, "Photographs in Geography", 41, (41, 0.05, 0.97),
        "(a) e.g. Figure 5 = ground/oblique photograph, Figure 6 = aerial/satellite photograph. (b) strength - covers a large area / shows patterns; limitation - less ground detail / needs interpretation. (c) the aerial/satellite photograph (Figure 6) - it can cover a wide area and detect heat/smoke quickly.",
        "Marks as shown.", topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 22, None,
        "Section C, Q4. Study Figure 7 which shows the landscape photograph of an area. With reference to the landscape photograph, describe the interrelationship between the people and the environment [4].",
        4, "People & Environment", 42, (42, 0.05, 0.97),
        "People depend on the environment for resources and shelter while also modifying it (e.g. clearing land, building); the environment in turn affects how people live and work.",
        "B4.", topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 23, None,
        "Section C, Q5. Figure 8 shows a simplified map of the major plate boundaries of the world. (a) Identify plate A and plate B [2]; (b) Explain how fold mountains are formed as a result of the Earth's internal forces [3]; (c) Using examples, explain how fold mountains affect the people living near the area [5].",
        10, "Plate Tectonics & Fold Mountains", 43, (43, 0.05, 0.97),
        "(a) name plates A and B from Figure 8. (b) when two plates carrying continental crust collide, the crust is compressed and buckles upward, forming fold mountains. (c) fold mountains provide tourism, water catchment and minerals but also pose hazards (landslides), poor accessibility and limited farmland.",
        "Marks as shown.", topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 24, None,
        "Section C, Q6. Study Figure 9 and answer. (a) State the element of weather that is used to produce energy in Figure 9 [1]; (b) Explain the difference between weather and climate [2]; (c) With the aid of examples, discuss how weather information is important to the daily human activities [3]; (d) With the aid of examples, discuss how climate can affect our food and water supplies [4].",
        10, "Weather & Climate", 44, (44, 0.05, 0.95),
        "(a) wind (the windmill uses wind energy). (b) weather is the day-to-day state of the atmosphere of a place; climate is the average weather over a long period (about 30 years). (c) e.g. plan outdoor events, farming, transport, clothing. (d) climate determines what crops grow and rainfall affects water supply - droughts reduce food and water; suitable climates support agriculture.",
        "Marks as shown.", topic_id=303)

    db.commit()
    print(f"Seeded First Toa Payoh 2012 Geography exam id={exam.id}: {len(p1.questions)} questions")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
