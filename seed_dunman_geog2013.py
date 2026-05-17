"""Seed Dunman Secondary School Mid-Year 2013 Sec 1 Express Geography exam."""

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

    school = db.query(School).filter(School.name == "Dunman Secondary School").first()
    if not school:
        school = School(name="Dunman Secondary School")
        db.add(school)
        db.flush()

    existing = (db.query(Exam)
                .filter(Exam.school_id == school.id, Exam.year == 2013,
                        Exam.subject == "Geography")
                .first())
    if existing:
        print(f"Dunman Geography 2013 already seeded (id={existing.id}). Re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id, title="Mid-Year Examination 2013", year=2013,
        level="Secondary 1 Express", subject="Geography",
        source_pdf="smiletutor_2013.pdf (Dunman 2013 Geography)", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)

    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=120, total_marks=100,
               date=date(2013, 5, 10), instructions="Answer ALL questions in the spaces provided. The paper consists of three sections: A (MCQ), B (Map-Reading & Basic Techniques), C (Structured Questions).")
    db.add(p1); db.flush()

    # ── SECTION A — MCQ (Q1-15, 15 marks) idx 96-100 ──
    add_q(db, p1.id, exam_dir, 1, 1, None,
        "The study of Geography is about the interaction between ____. A) human and physical environments  B) man-made and human environments  C) natural and physical environments  D) human and animal environments",
        1, "Nature of Geography", 96, (96, 0.05, 0.22),
        "A) the interaction between human and physical environments.", "B1",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 2, None,
        "Which of the following is not a component of the human environment? A) Rubber plantation  B) Power lines  C) River  D) Canal",
        1, "Human & Physical Environment", 96, (96, 0.22, 0.40),
        "C) A river is a natural (physical) feature, not part of the human environment.", "B1",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 3, None,
        "Which one of the following activities will least damage the environment? A) Using water from the river to water the crops  B) Dumping untreated sewage into the sea  C) Building a beach resort  D) Throwing litter into the drains",
        1, "Human Impact on Environment", 96, (96, 0.40, 0.60),
        "A) Using river water to water crops causes the least environmental damage.", "B1",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 4, None,
        "Which of the following descriptions about the !Kung Bushmen is NOT true? A) They use simple tools to hunt for a living.  B) They make big changes to their environment in order to survive.  C) They use ostrich eggs to collect water.  D) They do not build permanent shelters as they are always on the lookout for food and water.",
        1, "People & Environment", 96, (96, 0.60, 0.95),
        "B) Untrue — the !Kung Bushmen make minimal changes to their environment; they adapt to it.", "B1",
        topic_id=309)

    add_q(db, p1.id, exam_dir, 1, 5, None,
        "The diagram (Figure 1) shows a cross-section of the Earth with layers (i) and (ii). Which of the following is the correct order (innermost to outer / as labelled)? Options give combinations of Core / Mantle / Crust.",
        1, "Structure of the Earth", 97, (97, 0.05, 0.40),
        "The correct order of Earth's layers from the centre outwards is Core, Mantle, Crust (select the option matching the figure labels).", "B1",
        topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 6, None,
        "Figure 2 is a world map. Which letter indicates the location of the Southern Ocean? (Letters A-D marked on the map.)",
        1, "Oceans & Location", 97, (97, 0.40, 0.70),
        "The letter placed on the ocean surrounding Antarctica (the Southern Ocean) - read from Figure 2.", "B1",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 7, None,
        "Figure 3 is a world map. Which letter indicates the location of the Australian Continent? (Letters A-D marked on the map.)",
        1, "Continents & Location", 97, (97, 0.70, 0.95),
        "The letter placed on the Australian landmass - read from Figure 3.", "B1",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 8, None,
        "Study the landforms in Figure 4. Which of these landforms best represents a plain? A) a broad flat-topped raised land  B) a range of high pointed peaks  C) two tall steep mountains  D) a low, flat, level stretch of land",
        1, "Landforms", 98, (98, 0.05, 0.62),
        "D) A plain is a low, flat and level stretch of land (the flat low landform in Figure 4).", "B1",
        topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 9, None,
        "The horizontal lines on a grid map are called ____. A) axis  B) equator  C) northings  D) eastings",
        1, "Grid References", 98, (98, 0.62, 0.80),
        "C) Horizontal grid lines on a map are called northings.", "B1",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 10, None,
        "A ____ refers to an imaginary line joining points or places of the same height. A) latitude  B) scale  C) longitude  D) contour",
        1, "Contours", 98, (98, 0.80, 0.97),
        "D) A contour is an imaginary line joining points of the same height.", "B1",
        topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 11, None,
        "The 0 degree latitude is also known as the ____. A) Tropic of Capricorn  B) Tropic of Cancer  C) Equator  D) North Pole",
        1, "Latitude & Longitude", 99, (99, 0.18, 0.40),
        "C) The 0 degree latitude is the Equator.", "B1",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 12, None,
        "The action of running water commonly takes place in ____. A) sandy beaches in Australia  B) deserts in Africa  C) rivers in Thailand  D) polar regions in Alaska",
        1, "Rivers & Running Water", 99, (99, 0.40, 0.60),
        "C) Running water acts most commonly in rivers, e.g. rivers in Thailand.", "B1",
        topic_id=307)

    add_q(db, p1.id, exam_dir, 1, 13, None,
        "Maps ____. i) are tools used in planning; ii) are sources of information; iii) are used to calculate the distances between places accurately; iv) are used to record changes over time. A) i and iii only  B) ii and iv only  C) i, ii and iv only  D) all of the above",
        1, "Maps & Uses", 99, (99, 0.60, 0.82),
        "C) i, ii and iv only — maps cannot give perfectly accurate distances, so iii is not fully correct.", "B1",
        topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 14, None,
        "Molten rock which is found in the mantle layer is known as ____. A) lava  B) magma  C) rock fragments  D) vulcanicity",
        1, "Rocks & Magma", 99, (99, 0.82, 0.97),
        "B) Molten rock found in the mantle is called magma (it is called lava only when it reaches the surface).", "B1",
        topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 15, None,
        "The diagram (Figure 5) shows the contour lines, with values 96-100 and a river, of a ____. A) hill  B) mountain  C) plateau  D) valley",
        1, "Relief & Contours", 100, (100, 0.05, 0.78),
        "D) A valley — contours form a V-shape pointing towards higher ground with a river flowing through.", "B1",
        topic_id=302)

    # ── SECTION B Map-Reading (Q16, 15 marks) idx 101-102 ──
    add_q(db, p1.id, exam_dir, 1, 16, None,
        "Section B (Map-Reading). Study the map of Capers Town (Map A, scale 1:25 000). (a) Express the scale as a statement [1]; (b) Name a physical feature located in grid square 2813 [1]; (c) 4-figure grid reference of the sports complex [1]; (d) 6-figure grid reference of the school [1]; (e) Contour interval in the topographical map [1]; (f) Direction of the school from Capers Motel [1]; (g) Direction of Caravan Park from Capers Motel [1]; (h) Bearing of Capers Motel from Caravan Park [1]; (i) Distance of the track from Capers Motel to Capers' Bay in km [1]; (j) Name two physical features one can see standing on top of the sports complex looking east [2]; (k) Describe the slopes found in the given grid square, giving evidence [2]; (l) What could be the main economic activity in the area? Use map evidence [2].",
        15, "Map-Reading", 101, (101, 0.05, 0.97),
        "Use Map A, its 1:25 000 scale, grid lines and contour pattern: (a) 1 cm represents 250 m; (b)/(c)/(d) read eastings then northings; (e) from contour values; (f)/(g)/(h) use the north arrow/compass; (i) measure track then apply scale; (j) e.g. bay/sea/stream; (k) describe gentle/steep slope from contour spacing; (l) e.g. farming (corn/vegetables shown) or tourism (motel/caravan park).",
        "Marks per part as shown (total 15).", topic_id=301)

    # ── SECTION B Basic Techniques (Q17-18, 10 marks) idx 103-104 ──
    add_q(db, p1.id, exam_dir, 1, 17, None,
        "Section B (Basic Techniques). The diagram (Diagram 1) shows the magnitude of 5 deadliest earthquakes and the magnitude of the Haiti and Japan earthquakes. (a) What is the magnitude of the earthquake that occurred in Haiti in 2010? [1]; (b) How many deaths were recorded during the earthquake in Japan in 1923? [1]; (c) Which country had the highest number of deaths? [1]; (d) Where do earthquakes usually take place? [2].",
        5, "Earthquakes — Data Interpretation", 103, (103, 0.05, 0.97),
        "Read values from Diagram 1: (a)/(b)/(c) state the figures shown on the diagram; (d) earthquakes usually occur along plate boundaries / fault lines.",
        "Marks as shown.", topic_id=305)

    add_q(db, p1.id, exam_dir, 1, 18, None,
        "The diagram (Diagram 2) shows the percentage of deforestation of different regions in the 1990s and 2000s. (a) What is Indonesia's percentage of deforestation in the 1990s? [1]; (b) Which country had a decrease in deforestation in the 2000s? [1]; (c) Which country had the lowest percentage of deforestation in the 1990s and 2000s? [1]; (d) Describe a trend in deforestation as shown in the diagram, including evidence from the diagram [2].",
        5, "Deforestation — Data Interpretation", 104, (104, 0.05, 0.62),
        "Read percentages from the Diagram 2 pie charts: (a)/(b)/(c) state the figures/regions shown; (d) describe whether deforestation generally increased or decreased between the 1990s and 2000s, quoting figures.",
        "Marks as shown.", topic_id=309)

    # ── SECTION C — Structured Questions (60 marks) idx 105-113 ──
    add_q(db, p1.id, exam_dir, 1, 19, None,
        "Section C, Q19. (a) Figure 6 shows a landform formed by plate movement: (i) identify landform X and the plate movement that has led to its formation [2]; (ii) with the help of the diagram above, describe the formation of landform X [4]; (iii) name one example of landform X [1]. (b) Read the excerpt about Mt Merapi's eruption: (i) based on the excerpt, identify and describe two negative impacts of Mt Merapi's eruption [4]; (ii) explain why people live near volcanoes despite the risks [4].",
        15, "Plate Tectonics & Volcanoes", 105, (105, 0.05, 0.97),
        "(a)(i) X = fold mountain formed by two plates colliding (compression / convergent movement). (ii) continental crust is compressed and buckled upward by colliding plates, folding into mountains. (iii) e.g. Himalayas / Alps. (b)(i) e.g. ash fall destroying crops and homes, loss of life, businesses affected. (ii) fertile volcanic soils, geothermal energy, tourism, minerals and attachment to home.",
        "Marks as shown.", topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 20, None,
        "Section C, Q20. (a)(i) Define the term erosion [2]; (ii) Describe the action of wind on rocks [3]. (b) Study Figure 7 which shows a type of weathering process: (i) identify the weathering process found in the figure [1]; (ii) with help from Figure 7, describe the weathering process you have stated in (i) [5]; (iii) state two other causes of weathering [2].",
        13, "Weathering & Erosion", 106, (106, 0.55, 0.97),
        "(a)(i) erosion is the wearing away and removal of rock and soil by agents such as wind, water or ice. (a)(ii) wind carries sand which abrades and wears down exposed rock surfaces (wind abrasion/deflation). (b)(i)/(ii) e.g. physical/chemical/biological weathering — describe from Figure 7 (e.g. tree roots prising rock = biological). (b)(iii) e.g. temperature change, water/rain, plant roots, chemical action.",
        "Marks as shown.", topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 21, None,
        "Section C, Q21. (a) Study Photograph A: explain how the !Kung Bushmen in Photograph A have adapted to the environment [4]. (b) Photograph B (top: Singapore in the past; bottom: Singapore now): (i) define 'physical' and 'human' environments [2]; (ii) describe how Man has changed the environment in Photograph B [4]. (c) 'We live in a fragile earth. Human activities and natural disasters can damage earth.' (i) name one human activity that can damage earth [1]; (ii) give two reasons why the earth is fragile [4].",
        15, "People & Environment", 108, (108, 0.50, 0.97),
        "(a) the !Kung use simple tools, hunt and gather, collect water in ostrich eggs and move with food/water sources rather than altering the land. (b)(i) physical environment = natural surroundings (air, land, water, living things); human environment = features built/made by people. (b)(ii) Man cleared land and built high-rise buildings, roads and infrastructure. (c)(i) e.g. deforestation/mining/pollution. (c)(ii) resources are limited and easily exhausted; ecosystems are sensitive and slow to recover.",
        "Marks as shown.", topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 22, None,
        "Section C, Q22. (a) Study Photograph C carefully: (i) identify the type of photograph shown [1]; (ii) describe both the human and physical features found in the foreground and middle ground of the photograph [4]. (b) The photographs are taken before and after a city was affected by an earthquake: (i) identify the type of photograph shown [1]; (ii) compare three differences that you can see in the photos before and after the earthquake [6]; (iii) state three uses of photographs in Geography [3].",
        15, "Photographs & GIS", 111, (111, 0.05, 0.97),
        "(a)(i) e.g. ground/oblique photograph. (a)(ii) describe people, buildings (human) and land, vegetation, water (physical) seen in the foreground and middle ground. (b)(i) aerial/satellite photograph. (b)(ii) e.g. collapsed buildings, blocked roads, debris after the quake. (b)(iii) record changes over time, study landscapes, planning, evidence for analysis.",
        "Marks as shown.", topic_id=302)

    db.commit()
    print(f"Seeded Dunman 2013 Geography exam id={exam.id}: {len(p1.questions)} questions")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
