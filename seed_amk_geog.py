"""Seed Ang Mo Kio Secondary School Mid-Year (SA1) 2012 Sec 1 Express Geography exam."""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/amk_geog.pdf"

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
        source_pdf="Sec-1-Geography-2013.pdf (Ang Mo Kio SA1 2012)", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)

    # Single paper: 1 hr 15 min, 100 marks. Section A MCQ, B Mapwork, C Structured.
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=75, total_marks=100,
               date=date(2012, 5, 10),
               instructions="Answer ALL questions in Section A and B. In Section C, "
                            "answer Question 19 (compulsory) and either Question 20 "
                            "or Question 21.")
    db.add(p1); db.flush()

    # ── SECTION A — Multiple Choice (15 marks) ──
    # pdf idx 1 = page 2 (Q1-3); idx 2 = page 3 (Q4-7); idx 3 = page 4 (Q8-11)
    add_q(db, p1.id, exam_dir, 1, 1, None,
        "Which of the following is an example of a physical environment? "
        "A. Botanic Garden  B. Colorado River  C. Marina Bay Sands  "
        "D. Oil palm plantation",
        1, "Physical & Human Environment", 2, (1, 0.13, 0.27),
        "B. Colorado River", "B1", topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 2, None,
        "Which of the following diagrams shows the most appropriate "
        "inter-relationship between people and the environment? "
        "(A: affect much / impact little; B: affect little / impact much; "
        "C: affect little / impact little; D: affect much / impact much)",
        1, "People & Environment", 2, (1, 0.27, 0.78),
        "D. Affect much, impact much", "B1", topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 3, None,
        "Which of the following is not a human activity that causes changes "
        "to the physical environment? A. Deforestation  B. Mining  "
        "C. Pollution  D. Tsunami",
        1, "Human Impact on Environment", 2, (1, 0.78, 0.97),
        "D. Tsunami", "B1", topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 4, None,
        "Which of the following statement about the Earth is correct? "
        "A. Earth has a shorter orbit than Mercury.  "
        "B. Earth is much bigger than Jupiter.  "
        "C. Earth is the only planet that is able to support life.  "
        "D. Earth is the planet that is nearest to Sun.",
        1, "The Earth", 3, (2, 0.06, 0.22),
        "C. Earth is the only planet that is able to support life.", "B1",
        topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 5, None,
        "Why does the Sun appear to rise in the east and set in the west? "
        "A. It is because the Earth rotates westward.  "
        "B. It is because the Earth rotates eastward.  "
        "C. It is because the Sun rotates westward.  "
        "D. It is because the Sun rotates eastward.",
        1, "Earth Rotation", 3, (2, 0.22, 0.36),
        "B. It is because the Earth rotates eastward.", "B1", topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 6, None,
        "Contour lines which are close together represent _____. "
        "A. a gentle slope on a map  B. a hill on a map  "
        "C. a lowland area on a map  D. a steep slope on a map",
        1, "Contours & Relief", 3, (2, 0.36, 0.50),
        "D. a steep slope on a map", "B1", topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 7, None,
        "Which of the following shows a plateau? (Four contour map options "
        "A, B, C and D are shown.)",
        1, "Contours & Relief", 3, (2, 0.50, 0.95),
        "D (contour pattern showing a flat-topped upland - plateau)", "B1",
        topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 8, None,
        "What is normally used to locate a place in an atlas? "
        "A. grid references  B. letter-number system  "
        "C. latitudes and longitudes  D. lengths and widths",
        1, "Locating Places", 4, (3, 0.06, 0.20),
        "C. latitudes and longitudes", "B1", topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 9, None,
        "Which of the following correctly shows 1 cm on the map represents "
        "1 km on actual ground? A. 1:100  B. 1:1000  C. 1:10000  D. 1:100000",
        1, "Scale", 4, (3, 0.20, 0.40),
        "D. 1:100000", "B1", topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 10, None,
        "Which is the most accurate way to locate Singapore on the map? "
        "A. Singapore is located at 1 deg N, 103 deg E.  "
        "B. Singapore is located at the centre of South-East Asia.  "
        "C. Singapore is located in the Northern Hemisphere.  "
        "D. Singapore is located to the South of Peninsular Malaysia.",
        1, "Latitude & Longitude", 4, (3, 0.40, 0.58),
        "A. Singapore is located at 1 deg N, 103 deg E.", "B1", topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 11, None,
        "The figure shows the structure of the Earth, with labels 1, 2 and 3 "
        "(from outer to inner). Which option correctly names them? "
        "A. Crust / Mantle / Core  B. Core / Crust / Mantle  "
        "C. Mantle / Core / Crust  D. Mantle / Crust / Core",
        1, "Structure of the Earth", 4, (3, 0.58, 0.97),
        "A. 1 = Crust, 2 = Mantle, 3 = Core", "B1", topic_id=302)

    # idx 4 = page 5 (Q12-14); idx 5 = page 6 (Q15)
    add_q(db, p1.id, exam_dir, 1, 12, None,
        "What is the rock type shown in the picture below? (A photograph of "
        "rock with visible layers/strata is shown.) A. Igneous  "
        "B. Metamorphic  C. Molten  D. Sedimentary",
        1, "Rock Types", 5, (4, 0.06, 0.45),
        "D. Sedimentary", "B1", topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 13, None,
        "Which of the following indicates that movement of the Earth's plates "
        "is still going on? A. Landslides  B. Occurrence of earthquakes  "
        "C. Occurrence of storms  D. Weathering of mountains",
        1, "Plate Movement", 5, (4, 0.45, 0.65),
        "B. Occurrence of earthquakes", "B1", topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 14, None,
        "The figure shows a rock being broken down through a weathering "
        "process (a large rock on the ground with cracks). Which of the "
        "following is a likely location for this weathering process to take "
        "place? A. Antarctica  B. Amazon rainforest  C. Pacific Ocean  "
        "D. Sahara Desert",
        1, "Weathering", 5, (4, 0.65, 0.97),
        "D. Sahara Desert", "B1", topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 15, None,
        "The figure shows a rock found in the desert. Which of the following "
        "best explains why only the base of the rock was eroded? "
        "A. The water level was only high enough to reach the base of the rock  "
        "B. The sand is heavy and cannot be blown to a high level in the air.  "
        "C. The strength of the wave is too weak to erode other parts of the rock  "
        "D. The erosion process is too short for the entire rock to be fully eroded",
        1, "Wind Erosion - Desert", 6, (5, 0.06, 0.55),
        "B. The sand is heavy and cannot be blown to a high level in the air.",
        "B1", topic_id=302)

    # ── SECTION B — Part 1: Mapwork (15 marks) — Q16, page 7-8 (idx 6-7) ──
    map_stem = ("Refer to Map 1 (the Shrubam Town topographical map with scale "
                "1:50000) to answer Question 16.")
    add_q(db, p1.id, exam_dir, 1, 16, "a",
        "What is the contour interval shown on the map?",
        1, "Mapwork - Contour Interval", 8, (7, 0.10, 0.17),
        "50 m", "B1", stem=map_stem, topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 16, "b",
        "What does the dashed symbol (.....) represent on the map?",
        1, "Mapwork - Conventional Symbols", 8, (7, 0.17, 0.22),
        "Railway", "B1", topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 16, "c",
        "Identify a physical and a human feature on the map.",
        2, "Mapwork - Physical & Human Features", 8, (7, 0.22, 0.30),
        "Physical: a tree / hill / mountain. Human: a road / railway / factory.",
        "B1, B1", topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 16, "d",
        "What is the highest point on the map?",
        1, "Mapwork - Relief", 8, (7, 0.30, 0.36),
        "385 m", "B1", topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 16, "e",
        "Give the 4-figure grid reference for Hillside train station.",
        1, "Mapwork - 4-Figure Grid Reference", 8, (7, 0.36, 0.42),
        "0534", "B1", topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 16, "f",
        "Give the 6-figure grid reference for the trigonometrical station on "
        "Mt Beacon.",
        1, "Mapwork - 6-Figure Grid Reference", 8, (7, 0.42, 0.48),
        "015338", "B1", topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 16, "g",
        "What is the straight line distance from the peak of Mt Beacon to the "
        "peak of May Hill? Show your working and show your answer in km.",
        2, "Mapwork - Measuring Distance", 8, (7, 0.48, 0.57),
        "About 7 cm on the map x 0.5 km = 3.5 km (accept 3.5 +/- 0.3 km).",
        "M1 for working, A1", topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 16, "h",
        "If you took a train from May's Train station towards Beacon Town, in "
        "which general direction would the train be moving?",
        1, "Mapwork - Direction", 8, (7, 0.57, 0.63),
        "North-west", "B1", topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 16, "i",
        "What is the compass bearing of the trigonometrical station at Mt "
        "Beacon from the trigonometrical station at May Hill?",
        1, "Mapwork - Bearings", 8, (7, 0.63, 0.69),
        "About 238 deg / 237 deg / 239 deg", "B1", topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 16, "j",
        "What type of work would probably be carried out in the factories "
        "shown on the map?",
        1, "Mapwork - Land Use", 8, (7, 0.69, 0.75),
        "Processing rubber (rubber plantation / agro-processing industry).",
        "B1", topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 16, "k",
        "Why are towns built at intersections of roads?",
        1, "Mapwork - Settlement", 8, (7, 0.75, 0.81),
        "They are highly accessible - roads meeting allows easy movement of "
        "people and goods, encouraging trade and growth.", "B1", topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 16, "l",
        "Why are there no rubber plantations or buildings found at May Hill "
        "and Mt Beacon?",
        2, "Mapwork - Relief & Land Use", 8, (7, 0.81, 0.92),
        "Hill and mountain are too steep, therefore difficult to plant or "
        "build buildings; also too high, therefore difficult to travel.",
        "B1, B1", topic_id=302)

    # ── SECTION B — Part 2: Basic Techniques (10 marks) ──
    # Q17 page 9 (idx 8) ; Q18 page 10 (idx 9)
    energy_stem = ("Study Table 1, which shows the energy resources available "
                   "in Japan (% of Japan's energy use, % of resource found in "
                   "Japan, % imported, and supplying countries for Coal, Oil, "
                   "Gas, Uranium, Hydro-electric, Geothermal and Solar).")
    add_q(db, p1.id, exam_dir, 1, 17, "a",
        "State the resource used most in Japan. Support your answer with "
        "value from the table.",
        1, "Data Interpretation - Energy", 9, (8, 0.10, 0.40),
        "Oil, with 29% of Japan's energy use.", "B1",
        stem=energy_stem, topic_id=305)

    add_q(db, p1.id, exam_dir, 1, 17, "b",
        "State one renewable energy resource found in Japan.",
        1, "Renewable Energy", 9, (8, 0.40, 0.50),
        "Hydro-electric / Geothermal / Solar (any one).", "B1", topic_id=305)

    add_q(db, p1.id, exam_dir, 1, 17, "c",
        "Identify the resource that is the least found and most imported in "
        "Japan.",
        1, "Data Interpretation - Energy", 9, (8, 0.50, 0.60),
        "Uranium (0% found in Japan, 100% imported) - accept oil.", "B1",
        topic_id=305)

    add_q(db, p1.id, exam_dir, 1, 17, "d",
        "Does Singapore have geothermal energy? Explain your answer.",
        2, "Geothermal Energy", 9, (8, 0.60, 0.72),
        "No. Singapore does not lie along plate boundaries / has no volcanic "
        "or tectonic activity, so there are no geothermal sources.",
        "B1, B1", topic_id=305)

    graph_stem = ("Graph 1 shows the number of eruptions which Mount Merapi "
                  "experienced from the 16th century to the 20th century.")
    add_q(db, p1.id, exam_dir, 1, 18, "a",
        "State the number of eruptions that occurred in the 16th century.",
        1, "Graph Reading", 10, (9, 0.40, 0.50),
        "6 eruptions", "B1", stem=graph_stem, topic_id=305)

    add_q(db, p1.id, exam_dir, 1, 18, "b",
        "In which century were there around 21 eruptions?",
        1, "Graph Reading", 10, (9, 0.50, 0.58),
        "19th century", "B1", topic_id=305)

    add_q(db, p1.id, exam_dir, 1, 18, "c",
        "Describe the trend for the occurrence of eruptions from the 16th to "
        "20th century. Use values from the graph to support your answer.",
        3, "Describing Trends", 10, (9, 0.58, 0.72),
        "From the 16th to 18th century there were about 6 to 7 eruptions per "
        "century. The number rose sharply in the 19th century to about 21 "
        "eruptions, reaching its peak in the 20th century at about 27 "
        "eruptions.", "B1 x 3", topic_id=305)

    # ── SECTION C — Structured Questions (compulsory Q19; choose Q20 or Q21) ──
    # Q19 pages 11-13 (idx 10-12)
    add_q(db, p1.id, exam_dir, 1, 19, "a",
        "Figure 1 shows the distribution of volcanoes in the world. Describe "
        "the distribution of volcanoes.",
        1, "Distribution of Volcanoes", 11, (10, 0.45, 0.95),
        "Most volcanoes can be found along the Pacific plate / ring of fire / "
        "along plate boundaries.", "B1", topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 19, "bi",
        "Figure 2 shows part of a volcano. Identify parts of the volcano, A, "
        "B and C.",
        3, "Parts of a Volcano", 12, (11, 0.06, 0.55),
        "A = crater, B = pipe/vent, C = vent/cone (accept crater, pipe, vent).",
        "B1 x 3", topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 19, "bii",
        "Explain the formation of a volcano.",
        5, "Formation of a Volcano", 12, (11, 0.55, 0.80),
        "A volcano is a cone-shaped landform formed from the built-up of lava "
        "that has reached the Earth's surface. Magma below the Earth's surface "
        "experiences pressure when the plates move towards each other. This "
        "pressure forces the magma to rise upwards through the vent in the "
        "Earth's crust. The lava cools and solidifies around the vent, "
        "building up a cone over repeated eruptions.", "B1 x 5", topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 19, "ci",
        "Figure 3 is an article extract about volcanic activity in Miyakejima "
        "that caused poisonous gas to leak, forcing the 3600 island residents "
        "to evacuate in 2000. With reference to Figure 3 and studies made, "
        "explain the advantages and disadvantages of living near a volcano.",
        4, "Living Near Volcanoes", 13, (12, 0.30, 0.62),
        "Advantages: fertile volcanic soil for farming; geothermal energy; "
        "tourism income; mineral deposits. Disadvantages: risk of eruptions, "
        "poisonous gas, lava and ash destroying homes and forcing evacuation; "
        "loss of life and property.", "B1 x 4", topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 19, "cii",
        "With reference to Figure 3 and studies made, explain ways to reduce "
        "the problems during a volcanic eruption.",
        2, "Volcanic Hazard Management", 13, (12, 0.62, 0.78),
        "Early warning and monitoring systems; evacuation plans and drills; "
        "public education; building of barriers / safe shelters.",
        "B1 x 2", topic_id=302)

    # Q20 pages 14-15 (idx 13-14) — choice
    add_q(db, p1.id, exam_dir, 1, 20, "ai",
        "Figure 4 shows the !Kung Bushmen who live in the Kalahari Desert of "
        "South Africa hunting for food, and Figure 5 shows the buildings "
        "along Singapore River, an important river to Singapore. With "
        "reference to Figures 4 and 5, compare the environment in Singapore "
        "and Kalahari Desert.",
        2, "Environment Comparison", 14, (13, 0.55, 0.78),
        "Singapore has a built / urban environment with many buildings, while "
        "the Kalahari Desert has a natural environment with little vegetation "
        "and few people.", "B1 x 2", topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 20, "aii",
        "Compare the way of life of Singaporeans and !Kung Bushmen.",
        4, "Way of Life Comparison", 15, (14, 0.06, 0.20),
        "Singaporeans live a modern urban life, working in offices/industries "
        "and buying food. The !Kung Bushmen lead a traditional life, hunting "
        "and gathering food and depending directly on the natural "
        "environment.", "B1 x 4", topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 20, "bi",
        "Figure 6 shows cutting down forests (deforestation) and the effects "
        "of deforestation. Explain why Man need to carry out deforestation.",
        3, "Causes of Deforestation", 15, (14, 0.20, 0.45),
        "To clear land for farming, settlement and industry; for timber and "
        "wood products; for roads and infrastructure.", "B1 x 3",
        topic_id=309)

    add_q(db, p1.id, exam_dir, 1, 20, "bii",
        "Explain how deforestation affects the environment negatively.",
        4, "Impacts of Deforestation", 15, (14, 0.45, 0.62),
        "Loss of habitat and biodiversity; soil erosion; flooding; release of "
        "carbon dioxide leading to global warming; loss of water catchment.",
        "B1 x 4", topic_id=309)

    add_q(db, p1.id, exam_dir, 1, 20, "biii",
        "Describe how you can play a part in taking care of the Earth.",
        2, "Conservation", 15, (14, 0.62, 0.80),
        "Reduce, reuse and recycle; save water and electricity; use public "
        "transport; plant trees; avoid products that harm the environment.",
        "B1 x 2", topic_id=309)

    # Q21 pages 16-17 (idx 15-16) — choice
    add_q(db, p1.id, exam_dir, 1, 21, "a",
        "Figure 7 shows a weathering process. Describe the weathering process "
        "shown in Figure 7.",
        3, "Weathering Process", 16, (15, 0.06, 0.40),
        "Repeated heating and cooling (or freezing and thawing) causes the "
        "rock to expand and contract, leading to cracks and eventual break-up "
        "of the rock into smaller pieces (physical weathering).", "B1 x 3",
        topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 21, "b",
        "Figure 8 shows a cliff. Is it possible to build a house on A as "
        "shown in Figure 8? Support your answer.",
        4, "Relief & Land Use", 16, (15, 0.40, 0.80),
        "No - A is on a steep, unstable cliff edge that is subject to erosion "
        "and rockfall, making it dangerous and difficult to build on.",
        "B1 x 4", topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 21, "c",
        "Figure 9 shows the rock cycle (igneous, sedimentary and metamorphic "
        "rocks). With the aid of Figure 9, explain the rock cycle.",
        4, "Rock Cycle", 17, (16, 0.06, 0.62),
        "Molten magma cools to form igneous rock. Igneous rock is weathered "
        "and eroded; sediments are deposited and compacted to form "
        "sedimentary rock. Heat and pressure change rocks into metamorphic "
        "rock, which can melt back into magma, repeating the cycle.",
        "B1 x 4", topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 21, "d",
        "Landforms such as mountains affect people in many ways. Explain one "
        "positive and one negative way in which they affect us.",
        2, "Landforms & People", 17, (16, 0.62, 0.80),
        "Positive: mountains provide water (rivers), tourism and recreation. "
        "Negative: they are barriers to transport and difficult to build on "
        "or farm.", "B1, B1", topic_id=302)

    db.commit()
    cnt = len(p1.questions)
    print(f"Seeded Ang Mo Kio Geography 2012 exam id={exam.id}: {cnt} questions")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
