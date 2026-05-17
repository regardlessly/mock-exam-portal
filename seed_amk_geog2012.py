"""Seed Ang Mo Kio Secondary School Mid-Year 2012 Sec 1 Express Geography exam."""

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

    school = db.query(School).filter(School.name == "Ang Mo Kio Secondary School").first()
    if not school:
        school = School(name="Ang Mo Kio Secondary School")
        db.add(school)
        db.flush()

    existing = (db.query(Exam)
                .filter(Exam.school_id == school.id, Exam.year == 2012,
                        Exam.subject == "Geography")
                .first())
    if existing:
        print(f"AMK Geography 2012 already seeded (id={existing.id}). Re-seeding.")
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
        source_pdf="smiletutor_2013.pdf (AMK 2012 Geography)", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)

    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=75, total_marks=100,
               date=date(2012, 5, 10), instructions="Answer all questions in Sections A and B. In Section C answer any TWO questions (Q19 compulsory, then Q20 or Q21).")
    db.add(p1); db.flush()

    # ── SECTION A — MCQ (Q1-15, 15 marks) idx 3-7 ──
    add_q(db, p1.id, exam_dir, 1, 1, None,
        "Which of the following is an example of a physical environment? A) Botanic Garden  B) Colorado River  C) Marina Bay Sands  D) Oil palm plantations",
        1, "Physical & Human Environment", 2, (3, 0.10, 0.28),
        "B) Colorado River — a naturally formed feature, unlike the man-made others.", "B1",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 2, None,
        "Which of the following diagram shows the most appropriate inter-relationship between people and the environment? (Diagrams A-D show varying Affect/Impact arrows between People and Environment.)",
        1, "People & Environment", 2, (3, 0.28, 0.62),
        "D) People affect the environment much and the environment impacts people much (two-way strong relationship).", "B1",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 3, None,
        "Which of the following is not a human activity that causes changes to the physical environment? A) Deforestation  B) Mining  C) Pollution  D) Tsunami",
        1, "People & Environment", 2, (3, 0.62, 0.80),
        "D) Tsunami — a natural process, not a human activity.", "B1",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 4, None,
        "Which of the following statement about the Earth is correct? A) Earth has a shorter orbit than Mercury.  B) Earth is much bigger than Jupiter.  C) Earth is the only planet that is able to support life.  D) Earth is the planet that is nearest to Sun.",
        1, "Earth in Space", 3, (4, 0.05, 0.22),
        "C) Earth is the only planet known to support life.", "B1",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 5, None,
        "Why does the Sun appear to rise in the east and set in the west? A) It is because the Earth rotates westward.  B) It is because the Earth rotates eastward.  C) It is because the Sun rotates westward.  D) It is because the Sun rotates eastward.",
        1, "Earth's Rotation", 3, (4, 0.22, 0.38),
        "B) The Earth rotates eastward, so the Sun appears to move east to west.", "B1",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 6, None,
        "Contour lines which are close together represent ____. A) a gentle slope on a map  B) a hill on a map  C) a lowland area on a map  D) a steep slope on a map",
        1, "Relief & Contours", 3, (4, 0.38, 0.52),
        "D) a steep slope on a map — closely spaced contours indicate steep gradient.", "B1",
        topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 7, None,
        "Which of the following shows a plateau? (Four contour diagrams A-D are shown.)",
        1, "Relief & Contours", 3, (4, 0.52, 0.95),
        "D) The diagram with widely spaced low outer contours and a broad flat-topped high area (closely spaced edge contours, large flat top).", "B1",
        topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 8, None,
        "What is normally used to locate a place in an atlas? A) grid references  B) letter-number system  C) latitudes and longitudes  D) lengths and widths",
        1, "Maps & Location", 4, (5, 0.05, 0.20),
        "C) latitudes and longitudes are used to locate places in an atlas.", "B1",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 9, None,
        "Which of the following correctly shows 1 cm on the map represents 1 km on actual ground? A) 1:100  B) 1:1000  C) 1:10000  D) 1:100000",
        1, "Map Scale", 4, (5, 0.20, 0.36),
        "D) 1:100000 — 1 cm represents 100000 cm = 1 km.", "B1",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 10, None,
        "Which is the most accurate way to locate Singapore on the map? A) Singapore is located at 1 deg N, 103 deg E.  B) Singapore is located at the centre of South-East Asia.  C) Singapore is located in the Northern Hemisphere.  D) Singapore is located to the South of Peninsular Malaysia.",
        1, "Maps & Location", 4, (5, 0.36, 0.52),
        "A) Singapore is located at 1 deg N, 103 deg E — coordinates give the most accurate location.", "B1",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 11, None,
        "The figure shows the structure of the Earth, with parts 1, 2 and 3 labelled from the outside inwards. Which option correctly names parts 1, 2 and 3? A) Crust / Mantle / Core  B) Core / Crust / Mantle  C) Mantle / Core / Crust  D) Mantle / Crust / Core",
        1, "Structure of the Earth", 4, (5, 0.52, 0.95),
        "A) 1 = Crust, 2 = Mantle, 3 = Core (from the outside inwards).", "B1",
        topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 12, None,
        "What is the rock type shown in the picture below? A) Igneous  B) Metamorphic  C) Molten  D) Sedimentary  (Photograph shows clearly visible horizontal layers/strata.)",
        1, "Rocks", 5, (6, 0.05, 0.45),
        "D) Sedimentary — the visible layering (strata) is characteristic of sedimentary rock.", "B1",
        topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 13, None,
        "Which of the following indicates that movement of the Earth's plates is still going on? A) Landslides  B) Occurrence of earthquakes  C) Occurrence of storms  D) Weathering of mountains",
        1, "Plate Tectonics", 5, (6, 0.45, 0.62),
        "B) Occurrence of earthquakes shows that plate movement is still active.", "B1",
        topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 14, None,
        "The figure shows a large rock being broken down through a weathering process (water seeps into cracks, freezes, widens cracks). Which of the following is a likely location for this weathering process to take place? A) Antarctica  B) Amazon rainforest  C) Pacific Ocean  D) Sahara Desert",
        1, "Weathering", 5, (6, 0.62, 0.95),
        "A) Antarctica — freeze-thaw (frost) weathering requires temperatures that fluctuate around freezing point.", "B1",
        topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 15, None,
        "The figure shows a mushroom-shaped rock found in the desert. Which of the following best explains why only the base of the rock was eroded? A) The water level was only high enough to reach the base of the rock  B) The sand is heavy and cannot be blown to a high level in the air  C) The strength of the wave is too weak to erode other parts of the rock  D) The erosion process is too short for the entire rock to be fully eroded",
        1, "Weathering & Erosion", 6, (7, 0.05, 0.55),
        "B) Sand carried by wind is heavy and stays close to the ground, so abrasion erodes mainly the base.", "B1",
        topic_id=302)

    # ── SECTION B Part 1 — Mapwork (Q16, 20 marks) idx 8-9 ──
    add_q(db, p1.id, exam_dir, 1, 16, None,
        "Refer to Map 1 (Shorbun Town) and answer the following: (a) contour interval [1]; (b) what does the +H+H+ symbol represent [1]; (c) identify a physical and a human feature [2]; (d) highest point on the map [1]; (e) 4-figure grid reference for Hillside train station [1]; (f) 6-figure grid reference for the trigonometrical station on Mt Beacon [1]; (g) straight-line distance from peak of Mt Beacon to peak of May Hill in km, showing working [2]; (h) general direction of a train from May's Train station towards Beacon Town [1]; (i) compass bearing of the trig station at Mt Beacon from the trig station at May Hill [1]; (j) type of work in the factories shown [1]; (k) why are towns built at intersections of roads [1]; (l) why are there no rubber plantations or buildings at May Hill and Mt Beacon [2].",
        20, "Mapwork & Map Reading", 7, (8, 0.05, 0.95),
        "Use the map scale, grid lines and contour pattern. (a) read from contour values; (e)/(f) eastings then northings; (g) measure with ruler then apply scale; (h)/(i) use the compass/north arrow; (j) likely light industry/manufacturing; (k) road junctions ease accessibility and movement of goods/people; (l) steep relief / high land unsuitable for cultivation and building.",
        "Marks per part as shown (total 20).", topic_id=301)

    # ── SECTION B Part 2 — Basic Techniques (Q17-18) idx 9-10 ──
    add_q(db, p1.id, exam_dir, 1, 17, None,
        "Study Table 1 (energy resources available in Japan: Coal, Oil, Gas, Uranium, Hydro-electric, Geothermal, Solar with % of energy use, % found in Japan, % imported, supplier country). (a) State the resource used most in Japan, supporting with a value [1]; (b) State one renewable energy resource found in Japan [1]; (c) Identify the resource that is the least found and most imported in Japan [1]; (d) Does Singapore have geothermal energy? Explain [2].",
        5, "Resources — Data Interpretation", 9, (10, 0.05, 0.55),
        "(a) Oil — 29% of Japan's energy use. (b) Hydro-electric / Geothermal / Solar (any one). (c) Uranium — 0% found in Japan, 100% imported. (d) No — Singapore has no volcanic/tectonic activity, so no geothermal energy source.",
        "B1/B1/B1/B2.", topic_id=308)

    add_q(db, p1.id, exam_dir, 1, 18, None,
        "Graph 1 shows the number of eruptions Mount Merapi experienced from the 16th to the 20th century. (a) State the number of eruptions in the 16th century [1]; (b) In which century were there around 21 eruptions? [1]; (c) Describe the trend for the occurrence of eruptions from the 16th to 20th century, using values from the graph [3].",
        5, "Graphs — Data Interpretation", 10, (11, 0.05, 0.55),
        "(a) About 6 eruptions. (b) 19th century. (c) The number of eruptions remained low and roughly constant (about 6-7) from the 16th to 18th century, then rose sharply from the 18th to 20th century, reaching about 27 by the 20th century.",
        "B1/B1/B3.", topic_id=305)

    # ── SECTION C — Structured (Q19 compulsory, then Q20/Q21) idx 12-18 ──
    add_q(db, p1.id, exam_dir, 1, 19, None,
        "Section C, Q19 (compulsory). (a) Figure 1 shows the distribution of volcanoes in the world. Describe the distribution of volcanoes [1]. (b) Figure 2 shows part of a volcano: (i) identify parts A, B and C [3]; (ii) explain the formation of a volcano [5]. (c) Figure 3 is an article extract 'The Town where everyone wears a Mask' about Miyakejima: (i) with reference to Figure 3 and studies made, explain the advantages and disadvantages of living near a volcano [4]; (ii) explain ways to reduce the problems during a volcanic eruption [2].",
        30, "Volcanoes", 11, (12, 0.05, 0.95),
        "(a) Volcanoes are found mainly along plate boundaries / the Pacific Ring of Fire. (b)(i) e.g. A = crater/vent, B = magma chamber, C = lava layers (label from figure). (b)(ii) magma rises through a vent from the magma chamber due to pressure, erupts as lava/ash which cools and builds up into a cone. (c) advantages — fertile volcanic soil, geothermal energy, tourism; disadvantages — toxic gas, ash, danger to life; reduce problems via monitoring, evacuation plans, protective gear.",
        "Marks as shown (total 30).", topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 20, None,
        "Section C, Q20. Figure 4 shows the !Kung Bushmen who live in the Kalahari Desert; Figure 5 shows the buildings along Singapore River. (a)(i) With reference to Figures 4 and 5, compare the environment in Singapore and the Kalahari desert [2]; (ii) compare the way of life of Singaporeans and !Kung Bushmen [4]. (b) Figure 6 shows tiles cutting down forests (deforestation) and its effects: (i) explain why Man need to carry out deforestation [3]; (ii) explain how deforestation affects the environment negatively [4]; (iii) describe how you can play a part in taking care of the Earth [2].",
        30, "Environment & People; Deforestation", 14, (15, 0.05, 0.95),
        "(a) Singapore = built-up, urban, modern; Kalahari = natural, arid desert with sparse vegetation. Bushmen = hunter-gatherer, traditional; Singaporeans = urban, modern economy. (b) deforestation for farmland/timber/development; negatives — soil erosion, loss of habitat, flooding, climate change; personal action — recycle, conserve, plant trees.",
        "Marks as shown (total 30).", topic_id=309)

    add_q(db, p1.id, exam_dir, 1, 21, None,
        "Section C, Q21. (a) Figure 7 shows a weathering process: describe the weathering process shown in Figure 7 [3]. (b) Figure 8 shows a cliff: is it possible to build a house on A as shown in Figure 8? Support your answer [4]. (c) Figure 9 shows the rock cycle: with the aid of Figure 9, explain the rock cycle [4]; (d) Landforms such as mountains affect people in many ways — explain one positive and one negative way in which they affect us [2].",
        30, "Weathering & Rock Cycle", 16, (17, 0.05, 0.95),
        "(a) e.g. physical/mechanical weathering — rock broken into smaller fragments by temperature change or frost action. (b) No — the cliff is unstable / prone to erosion and collapse, so building there is unsafe. (c) the rock cycle: weathering and erosion break rocks into sediments which compact into sedimentary rock; heat and pressure form metamorphic rock; melting then cooling forms igneous rock, and the cycle continues. (d) positive — mountains attract tourism and provide water catchment; negative — landslides and difficult accessibility.",
        "Marks as shown (total 30).", topic_id=302)

    db.commit()
    print(f"Seeded AMK 2012 Geography exam id={exam.id}: {len(p1.questions)} questions")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
