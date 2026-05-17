"""Seed Riverside Secondary School Mid-Year (SA1) 2012 Sec 1 Express Geography exam."""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/riverside_geog.pdf"

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

    school = (db.query(School)
              .filter(School.name == "Riverside Secondary School").first())
    if not school:
        school = School(name="Riverside Secondary School")
        db.add(school)
        db.flush()

    existing = (db.query(Exam)
                .filter(Exam.school_id == school.id, Exam.year == 2012,
                        Exam.subject == "Geography")
                .first())
    if existing:
        print(f"Riverside Geography 2012 already seeded (id={existing.id}). "
              f"Re-seeding.")
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
        source_pdf="Sec-1-Geography-2013.pdf (Riverside SA1 2012)",
        status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)

    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=90,
               total_marks=60, date=date(2012, 5, 4),
               instructions="Answer all questions. Section A: Basic "
                            "Techniques [10]. Section B: Map Reading [20]. "
                            "Section C: Structured Essay Questions [30].")
    db.add(p1); db.flush()

    # ── SECTION A — Basic Techniques [10] ──
    # Q1 page 2 (idx 1) — Earth tilt diagram
    earth_stem = ("Figure 1 shows the Earth on its tilted axis (North Pole "
                  "and South Pole labelled).")
    add_q(db, p1.id, exam_dir, 1, 1, "a",
        "In what direction is the Earth rotating?",
        1, "Earth's Rotation", 2, (1, 0.06, 0.78),
        "West to east", "B1", stem=earth_stem, topic_id=302)
    add_q(db, p1.id, exam_dir, 1, 1, "b",
        "At what angle is the Earth tilted?",
        1, "Earth's Tilt", 2, (1, 0.78, 0.83),
        "23.5 degrees", "B1", topic_id=302)
    add_q(db, p1.id, exam_dir, 1, 1, "c",
        "What is the effect of Earth's rotation in Figure 1?",
        1, "Effect of Rotation", 2, (1, 0.83, 0.88),
        "The cycle of day and night", "B1", topic_id=302)
    add_q(db, p1.id, exam_dir, 1, 1, "d",
        "What is the imaginary line that divides the Earth into the Northern "
        "and Southern Hemisphere?",
        1, "Lines of Latitude", 2, (1, 0.88, 0.93),
        "Equator", "B1", topic_id=301)
    add_q(db, p1.id, exam_dir, 1, 1, "e",
        "How long does it take Earth to complete one rotation?",
        1, "Earth's Rotation", 2, (1, 0.93, 0.99),
        "24 hours", "B1", topic_id=302)

    # Q2 page 3 (idx 2) — planets
    planet_stem = ("Table 1 and Figure 2 show information about planets in the "
                   "Solar System (Planet, distance from the Sun in million km, "
                   "diameter in thousand km: X=58/4.9, Y=228/6.8, Z=1427/120.7, "
                   "Uranus=2870/51.1).")
    add_q(db, p1.id, exam_dir, 1, 2, "a",
        "Identify planets X, Y and Z.",
        3, "The Solar System", 3, (2, 0.06, 0.85),
        "X = Mercury, Y = Mars, Z = Saturn", "B1 x 3", stem=planet_stem,
        topic_id=302)
    add_q(db, p1.id, exam_dir, 1, 2, "b",
        "Describe two characteristics of Planet Uranus.",
        2, "The Solar System", 3, (2, 0.85, 0.97),
        "It appears as a blue-green disk; it has rings encircling it; it is "
        "the second furthest planet from the Sun (any two).", "B1 x 2",
        topic_id=302)

    # ── SECTION B — Map Reading [20] ──
    # Q1 mapwork pages 4-6 (idx 3-5)
    map_stem = ("Refer to the (inset scale) topographical map (Heidelberg / "
                "Bond Town / Albert Village area, with a legend for road, "
                "track, train station, town, factory, contours, buildings and "
                "trigonometrical station). Answer all questions.")
    add_q(db, p1.id, exam_dir, 1, 3, "a",
        "Give the four figure grid reference of Mount Pacier Both on the map.",
        1, "Mapwork - 4-Figure Grid Reference", 4, (3, 0.40, 0.55),
        "GR 0131 / 0133 (accept 4-figure square containing the peak).", "B1",
        stem=map_stem, topic_id=301)
    add_q(db, p1.id, exam_dir, 1, 3, "b",
        "Give the four figure grid reference of the location of the three "
        "factories on the map.",
        1, "Mapwork - 4-Figure Grid Reference", 4, (3, 0.55, 0.62),
        "GR 0434", "B1", topic_id=301)
    add_q(db, p1.id, exam_dir, 1, 3, "c",
        "What is the highest point on the map? Give your answer in height (in "
        "metres).",
        1, "Mapwork - Relief", 4, (3, 0.62, 0.68),
        "785 m", "B1", topic_id=302)
    add_q(db, p1.id, exam_dir, 1, 3, "d",
        "Calculate the straight line distances of Bond Avenue and James "
        "Avenue.",
        2, "Mapwork - Measuring Distance", 4, (3, 0.68, 0.75),
        "About 2.1 km in total (Bond Avenue about 1.4 km + James Avenue about "
        "0.7 km; accept measured values).", "B1 x 2", topic_id=301)
    add_q(db, p1.id, exam_dir, 1, 3, "e",
        "Give the six figure grid reference of the trigonometrical station of "
        "Heidelberg Hill.",
        1, "Mapwork - 6-Figure Grid Reference", 4, (3, 0.75, 0.85),
        "GR 044358 (accept +/- 1)", "B1", topic_id=301)
    add_q(db, p1.id, exam_dir, 1, 3, "f",
        "What is the contour interval of the map?",
        1, "Mapwork - Contour Interval", 4, (3, 0.85, 0.92),
        "50 m", "B1", topic_id=302)
    add_q(db, p1.id, exam_dir, 1, 3, "h",
        "If you are heading to Albert Village from Bond Town via James "
        "Avenue, in which direction will you be heading?",
        1, "Mapwork - Direction", 4, (3, 0.92, 0.98),
        "Northwest / North-north-west", "B1", topic_id=301)
    add_q(db, p1.id, exam_dir, 1, 3, "i",
        "What are the two transportation routes people can take to reach the "
        "factories in Heidelberg Town?",
        2, "Mapwork - Transport", 5, (4, 0.06, 0.20),
        "Railway and road", "B1 x 2", topic_id=301)
    add_q(db, p1.id, exam_dir, 1, 3, "j",
        "Refer to the world map. Identify the oceans labelled E and F on the "
        "map.",
        2, "World Map - Oceans", 5, (4, 0.06, 0.70),
        "E = Atlantic Ocean, F = Indian Ocean", "B1 x 2", topic_id=301)
    add_q(db, p1.id, exam_dir, 1, 3, "k",
        "Identify continents A, B and C respectively.",
        4, "World Map - Continents", 5, (4, 0.70, 0.90),
        "A = Europe, B = Asia, C = Africa", "B1 x 4", topic_id=301)
    add_q(db, p1.id, exam_dir, 1, 3, "l",
        "Refer to the latitude/longitude map. What is the longitude of the "
        "Prime Meridian?",
        1, "Lines of Longitude", 6, (5, 0.06, 0.62),
        "0 degrees", "B1", topic_id=301)
    add_q(db, p1.id, exam_dir, 1, 3, "m",
        "What is the latitude of the Equator?",
        1, "Lines of Latitude", 6, (5, 0.62, 0.70),
        "0 degrees", "B1", topic_id=301)
    add_q(db, p1.id, exam_dir, 1, 3, "n",
        "Name line X (23.5 deg N) on the map.",
        1, "Lines of Latitude", 6, (5, 0.70, 0.78),
        "Tropic of Cancer", "B1", topic_id=301)
    add_q(db, p1.id, exam_dir, 1, 3, "o",
        "Name line Y (66.5 deg S) on the map.",
        1, "Lines of Latitude", 6, (5, 0.78, 0.86),
        "Antarctic Circle", "B1", topic_id=301)
    add_q(db, p1.id, exam_dir, 1, 3, "p",
        "What is another term given to the line of longitude of 180 degrees?",
        1, "Lines of Longitude", 6, (5, 0.86, 0.94),
        "International Date Line", "B1", topic_id=301)

    # ── SECTION C — Structured Essay Questions [30] ──
    # Q1 page 7 (idx 6) — natural resources
    res_stem = ("Figure 3 shows a picture of various types of natural "
                "resources found on Earth's surface (soil, coal, oil, fish, "
                "trees, water, timber, metals, minerals, fossil fuels, "
                "atmosphere, etc.).")
    add_q(db, p1.id, exam_dir, 1, 4, "i",
        "What are 'natural resources'?",
        2, "Natural Resources", 7, (6, 0.06, 0.55),
        "Natural resources are basic substances that exist naturally in the "
        "physical environment that humans can make use of.", "B1 x 2",
        stem=res_stem, topic_id=305)
    add_q(db, p1.id, exam_dir, 1, 4, "ii",
        "Using Figure 3, identify one renewable resource and two "
        "non-renewable resources.",
        3, "Renewable & Non-Renewable Resources", 7, (6, 0.55, 0.65),
        "Renewable: water (or trees / solar energy). Non-renewable: coal and "
        "oil (or fossil fuels, natural gas, minerals, metals - any two).",
        "B1 x 3", topic_id=305)
    add_q(db, p1.id, exam_dir, 1, 4, "iii",
        "Explain two ways how human beings have made use of resources in the "
        "environment.",
        4, "Use of Resources", 7, (6, 0.65, 0.78),
        "Human beings use water for drinking, cleaning, cooking and washing; "
        "use trees and timber to build furniture and houses; use coal, oil "
        "and gas as energy to power machines, homes and industries; use "
        "metals and minerals to make tools and products (any two explained).",
        "B1 x 4", topic_id=305)

    # Q1b page 8 (idx 7) — environments
    env_stem = ("Figures 2 and 3 show two different types of environments (a "
                "natural physical landscape and a built city environment).")
    add_q(db, p1.id, exam_dir, 1, 5, "i",
        "Identify the two types of environments in Figure 2 and Figure 3.",
        2, "Types of Environments", 8, (7, 0.06, 0.62),
        "Figure 2: physical (natural) environment. Figure 3: human (built) "
        "environment.", "B1 x 2", stem=env_stem, topic_id=302)
    add_q(db, p1.id, exam_dir, 1, 5, "ii",
        "Explain how the components of weather and natural vegetation in the "
        "environment shown in Figure 2 are interrelated.",
        4, "Weather & Vegetation", 8, (7, 0.62, 0.92),
        "Weather and climate are influenced by the amount of water vapour and "
        "heat. Water vapour comes from rivers, soil and plants and forms "
        "clouds and rain. Trees absorb mineral salts and moisture from the "
        "soil, are broken down from rocks, and when plants die and decay add "
        "nutrients to the soil - so weather affects vegetation and "
        "vegetation in turn affects weather and climate.", "B1 x 4",
        topic_id=303)

    # Q2 page 9 (idx 8) — !Kung Bushmen
    bush_stem = ("Figure 4 shows a picture of !Kung Bushmen in the Kalahari "
                 "Desert.")
    add_q(db, p1.id, exam_dir, 1, 6, "i",
        "In what ways are !Kung Bushmen able to live in the harsh conditions "
        "of the Kalahari Desert? Describe any three ways.",
        3, "Adapting to the Desert", 9, (8, 0.06, 0.55),
        "Clothing: they wear little or no clothing (animal hides) suited to "
        "the hot, arid climate. Housing: they build simple shelters from "
        "natural materials that can be moved as they search for water and "
        "food. Food: they hunt animals and gather wild plants, tubers and "
        "roots, and find/store water as the desert does not favour farming.",
        "B1 x 3", stem=bush_stem, topic_id=311)
    add_q(db, p1.id, exam_dir, 1, 6, "ii",
        "'!Kung Bushmen are living in harmony with the environment.' In what "
        "ways are they living in harmony with their environment in the "
        "desert?",
        4, "Living in Harmony with Environment", 9, (8, 0.55, 0.68),
        "They use simple tools to hunt in the desert and do not try to change "
        "it; they take only what they need and do not make major changes to "
        "the environment, so they live in harmony with the natural "
        "environment.", "B1 x 4", topic_id=311)
    add_q(db, p1.id, exam_dir, 1, 6, "iii",
        "Describe any two differences in the way of life between "
        "Singaporeans and the !Kung Bushmen.",
        4, "Way of Life Comparison", 9, (8, 0.68, 0.80),
        "Sources of food and water: Singaporeans buy food from shops and get "
        "water from reservoirs and taps, while the !Kung hunt and gather food "
        "and find water. Clothing/movement: the !Kung wear little clothing "
        "and move around in search of food, while Singaporeans live in fixed "
        "modern homes and lead an urban lifestyle (any two differences "
        "elaborated).", "B1 x 4", topic_id=311)
    add_q(db, p1.id, exam_dir, 1, 6, "iv",
        "Explain how the use of technology could affect the lives of the "
        "!Kung Bushmen in a positive and negative way. Give examples to "
        "support your answer.",
        4, "Impact of Technology", 9, (8, 0.80, 0.94),
        "Positive: technology can make their lives more comfortable (e.g. "
        "modern medicine, vehicles, tools). Negative: it may erode their "
        "traditional way of life and damage the environment (e.g. "
        "deforestation, loss of culture). Accept any plausible examples.",
        "B1 x 4", topic_id=311)

    db.commit()
    cnt = db.query(Question).filter(Question.paper_id == p1.id).count()
    print(f"Seeded Riverside Geography 2012 exam id={exam.id}: {cnt} questions")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
