"""Seed St. Gabriel's Secondary School First Semestral Examination 2013
Sec 1 Express Geography.

Source: smiletutor.sg Sec 1 Geography 2013 compilation PDF, St. Gabriel's
section (cover idx 78, paper idx 78-90, End of Paper idx 90).
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
        .filter(School.name == "St. Gabriel's Secondary School")
        .first()
    )
    if not school:
        school = School(name="St. Gabriel's Secondary School")
        db.add(school)
        db.flush()

    existing = (
        db.query(Exam)
        .filter(Exam.school_id == school.id, Exam.year == 2013,
                Exam.subject == "Geography")
        .first()
    )
    if existing:
        print(f"St. Gabriel's Geography 2013 already seeded (id={existing.id}). "
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
        title="First Semestral Examination 2013 (Geography)",
        year=2013, level="Secondary 1 Express", subject="Geography",
        source_pdf="smiletutor_sec1geog_2013.pdf (St. Gabriel's section)",
        status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)

    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=90,
               total_marks=50, date=date(2013, 5, 3),
               instructions="Section A Geographical Skills (20 marks). "
                            "Section B Structured Questions (30 marks): Q4 "
                            "compulsory; answer either Q5 or Q6.")
    db.add(p1)
    db.flush()

    # ── Section A: Geographical Skills [20 marks] ──
    add_q(db, p1.id, exam_dir, 1, 1, None,
          "Study Fig.1 (bar graph: Deforestation in the Brazilian Amazon, "
          "1988-2010, total amount of forested area cut down in thousand square "
          "km). (a) Which year had the highest rate of deforestation? (b) What "
          "was the total amount of forested area that was cut down between 2001 "
          "and 2004? You must show your working. (c) State a reason why so many "
          "trees have been cut down.",
          4, "Geographical Skills / Data", 80, (79, 0.0, 1.0),
          "(a) The year with the tallest bar (e.g. 1995, the peak). (b) Add the "
          "values of the bars for 2001, 2002, 2003 and 2004 from the graph and "
          "show the sum. (c) Trees cut down for timber, farmland/agriculture, "
          "cattle ranching or settlement and development.",
          "B1 per correct reading; M1 for working in (b)",
          stem="Fig.1: bar graph of deforestation in the Brazilian Amazon "
               "1988-2010.",
          topic_id=305)

    add_q(db, p1.id, exam_dir, 1, 2, None,
          "Study Fig.2 (topographical map, 1 cm represents 2 km, with legend: "
          "contour height in metres, footpath, quarry, hill resort, houses, "
          "flower orchard, vegetable farm, golf course, road, church, temple, "
          "post office, police station, school, market). (a) What is the "
          "four-digit grid reference of the quarry? (b) Measure the straight-line "
          "distance between the Post Office and the Hill resort. Express your "
          "answer in km. You must show your working. (c) What is the compass "
          "direction of the Post Office from the Flower Orchard? (d) What do the "
          "contours of the slope labelled AB tell us about its gradient? Support "
          "your answer with evidence.",
          6, "Maps & Map Reading", 81, (80, 0.0, 1.0),
          "(a) Four-digit grid reference of the quarry read off the map. "
          "(b) Measure map distance, multiply using the 1 cm to 2 km scale, show "
          "working, give answer in km. (c) Compass direction of Post Office from "
          "Flower Orchard. (d) The contour spacing along AB shows the gradient — "
          "widely spaced contours indicate a gentle slope, closely spaced "
          "indicate a steep slope; cite the contour evidence.",
          "B1/B2 per answer; M1 for scale working",
          stem="Fig.2: topographical map (1 cm to 2 km) with full legend.",
          topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 3, None,
          "Your geography teacher has asked you to carry out a fieldwork project "
          "to find the 'hotspot' in your school among 4 sites (Ecological Garden, "
          "Football Field, Foyer, Parade Square). (a) Name an instrument you "
          "would need to measure the temperature of the 4 sites. (b) Study Fig.3 "
          "(temperature recorded at different times at each of the 4 sites): "
          "(i) Calculate the mean temperature of Site A, Site B, Site C and Site "
          "D. You must show all your working. (ii) Rank the sites, starting from "
          "Rank No. 1, which has the highest temperature to Rank No. 4 which has "
          "the lowest temperature. (iii) State 1 reason why the site you ranked "
          "number 1 has the highest temperature. (iv) State 1 reason why the site "
          "you ranked number 4 has the lowest temperature.",
          10, "Weather & Climate: Instruments", 82, (81, 0.0, 1.0),
          "(a) A thermometer. (b)(i) Mean of each site's readings = sum of its "
          "readings divided by the number of readings (show working). (ii) Rank "
          "sites by their mean temperatures, highest to lowest. (iii) Highest "
          "site is exposed to direct sunlight with little shade and more concrete "
          "surfaces absorbing heat. (iv) Lowest site is shaded by trees/buildings "
          "with more vegetation, so it stays cooler.",
          "B1/M1 per part; M1 for mean working",
          stem="Fig.3: table of temperatures recorded at 11:00am-11:45am at "
               "Sites A, B, C and D.",
          topic_id=303)

    # ── Section B: Structured Questions [30 marks] — Q4 compulsory ──
    add_q(db, p1.id, exam_dir, 1, 4, "a",
          "State 2 conditions found on Planet Earth that supports life.",
          2, "Fragile Earth", 83, (82, 0.0, 0.30),
          "Any two of: a breathable atmosphere with oxygen; liquid water; "
          "suitable (not extreme) temperatures; protection from harmful "
          "radiation.",
          "B1 per condition",
          topic_id=303)

    add_q(db, p1.id, exam_dir, 1, 4, "b",
          "Study the figures (Fig.4 the earth shook in a city in China; Fig.5 "
          "very strong winds blew across a coastal area; Fig.6 chimneys of "
          "factories in Japan; Fig.7 feathers of a bird covered with oil). For "
          "Fig.4, 5 and 6, identify the name of the hazard and state whether it "
          "is a natural hazard or a human hazard. An example of the answer for "
          "Fig.7 is: an oil spill (human hazard).",
          3, "Variable Weather / Hazards", 84, (83, 0.0, 0.55),
          "Fig.4: earthquake (natural hazard). Fig.5: strong winds / storm "
          "(natural hazard). Fig.6: air pollution from factories (human hazard).",
          "B1 per correct identification + classification",
          stem="Fig.4-7: photographs of an earthquake, strong winds, factory "
               "chimneys and an oil-covered bird.",
          topic_id=310)

    add_q(db, p1.id, exam_dir, 1, 4, "c",
          "Study Fig.8 and Fig.9 and answer the question. Identify the type of "
          "environment shown in Fig.8 and Fig.9. Support your answer with an "
          "evidence from each photograph.",
          4, "Environments", 84, (83, 0.53, 1.0),
          "Fig.8: physical/natural environment — evidence such as natural "
          "vegetation/water with no human-made features. Fig.9: human "
          "environment — evidence such as houses/buildings built by people.",
          "B2 per figure (identify + evidence)",
          stem="Fig.8 and Fig.9: photographs of two different environments.",
          topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 4, "d",
          "Study Fig.10 carefully (four farmers: a small farmland in India "
          "growing rice with good harvest; a farmer in China upset that "
          "floodwaters washed away rice crops before harvest; a banana farm in "
          "the Philippines ruined for two months with low income; farmers in "
          "Indonesia happy that crops are growing well with enough sunlight and "
          "rain). Weather has a positive impact on the livelihood of farmers. "
          "Using examples from Fig.10, discuss the impact of weather on the "
          "farmers in some parts of Asia.",
          6, "Variable Weather & Climate Change", 85, (84, 0.0, 1.0),
          "Favourable weather (enough sunlight and rain) gives good harvests and "
          "income, as for the farmers in India and Indonesia; extreme/unfavourable "
          "weather (floods, prolonged rain) destroys crops and reduces income, as "
          "for the farmers in China and the Philippines. Use the specific "
          "examples from Fig.10.",
          "Levelled marking with examples",
          stem="Fig.10: four farmers in different parts of Asia experiencing "
               "different weather impacts.",
          topic_id=310)

    # ── Q5 (answer either Q5 or Q6) ──
    add_q(db, p1.id, exam_dir, 1, 5, "a",
          "State the main difference between renewable natural resources and "
          "non-renewable natural resources.",
          2, "Water Resources & Management", 86, (85, 0.0, 0.22),
          "Renewable resources can be replaced or replenished within a short "
          "time (e.g. water, trees), while non-renewable resources take a very "
          "long time to form and cannot be replaced once used up (e.g. gold, "
          "minerals).",
          "B2",
          topic_id=308)

    add_q(db, p1.id, exam_dir, 1, 5, "b",
          "With reference to Fig.11, Fig.12 and Fig.13, briefly describe how each "
          "of the natural resource is useful to man.",
          3, "Water Resources & Management", 86, (85, 0.20, 1.0),
          "Fig.11 water: for drinking, washing, irrigation and industry. Fig.12 "
          "trees: provide timber, oxygen and habitats. Fig.13 gold: used for "
          "jewellery, electronics and as a store of value.",
          "B1 per resource",
          stem="Fig.11 (water), Fig.12 (trees), Fig.13 (gold).",
          topic_id=308)

    add_q(db, p1.id, exam_dir, 1, 5, "c",
          "Study Fig.14, Fig.15, Fig.16 and Fig.17. With reference to the "
          "figures, state how the !Kung Bushmen and Singaporeans do the "
          "following: (i) Obtain their food. (ii) Build their houses.",
          4, "Natural Vegetation & Biomes", 87, (86, 0.0, 0.55),
          "(i) !Kung Bushmen hunt animals and gather plants/water from the wild; "
          "Singaporeans buy cooked or packaged food from shops and markets. "
          "(ii) !Kung Bushmen build simple temporary shelters from branches and "
          "grass; Singaporeans build permanent houses of concrete and metal.",
          "B1 per correct comparison",
          stem="Fig.14-17: photographs of the !Kung Bushmen and Singaporeans.",
          topic_id=311)

    add_q(db, p1.id, exam_dir, 1, 5, "d",
          "Study Fig.18 and answer the questions. Note: April has 30 days. "
          "(Fig.18 shows a date/number calculation grid: 29 28 12 11 8 6 X "
          "3 5 17.) Compute the value indicated.",
          3, "Geographical Skills", 87, (86, 0.53, 1.0),
          "Work through the date/number calculation shown in Fig.18 step by step "
          "using the note that April has 30 days, and state the value of X.",
          "M1/A1 for working and answer",
          stem="Fig.18: date and number calculation grid.",
          topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 5, "e",
          "(Weather instruments) (i) State the direction of the prevailing wind. "
          "(ii) What does X stand for? Calculate the value of X. "
          "(iii) Draw a well-labelled diagram of a rain gauge.",
          6, "Weather & Climate: Instruments", 88, (87, 0.0, 0.40),
          "(i) State the prevailing wind direction from the data shown. "
          "(ii) Explain what X represents and calculate its value from the "
          "figures. (iii) A labelled rain gauge: funnel, copper cylinder, "
          "collecting jar/measuring cylinder, outer casing.",
          "B1/M1 per part",
          topic_id=303)

    # ── Q6 (alternative to Q5) ──
    add_q(db, p1.id, exam_dir, 1, 6, "a",
          "Study Fig.19 carefully (world map with grid of latitude and longitude "
          "and points A and B). State the latitudes and longitudes of A and B.",
          2, "Maps & Map Reading", 88, (87, 0.38, 1.0),
          "Give the latitude and longitude pair for point A and for point B, "
          "read off the gridded world map.",
          "B1 per correct coordinate pair",
          stem="Fig.19: world map with latitude-longitude grid and points A "
               "and B.",
          topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 6, "b",
          "The line labelled 'X' divides the globe into 2 hemispheres. (i) What "
          "is the line 'X' known as? (ii) Name the 2 hemispheres.",
          3, "Maps & Map Reading", 88, (87, 0.55, 1.0),
          "(i) The Equator. (ii) The Northern Hemisphere and the Southern "
          "Hemisphere.",
          "B1 per correct answer",
          topic_id=301)

    add_q(db, p1.id, exam_dir, 1, 6, "c",
          "Study the photographs which were taken in the same area in Singapore "
          "(Fig.20 Year 1950; Fig.21 Year 2010). (i) What type of photographs are "
          "these? Where were they taken from? (ii) Name 2 major changes that have "
          "taken place in this area, between 1950 and 2010.",
          4, "Photographs & GIS", 89, (88, 0.0, 1.0),
          "(i) Ground-level (oblique ground) photographs taken from the ground. "
          "(ii) Two changes e.g. low buildings/kampong replaced by tall "
          "buildings; natural land replaced by roads and built-up urban "
          "development.",
          "B1/B2 per answer",
          stem="Fig.20 (Year 1950) and Fig.21 (Year 2010): same area of "
               "Singapore.",
          topic_id=302)

    add_q(db, p1.id, exam_dir, 1, 6, "d",
          "Fig.22 shows the layout of a school (building, stone path, tree, "
          "grass, garden). (i) Of the four sites that have been stratified, which "
          "is the best location (A, B, C or D) to place a Stevenson Screen? State "
          "2 reasons why you have chosen that location. (ii) Draw a well-labelled "
          "diagram of the water cycle.",
          6, "Weather & Climate / Water Cycle", 90, (89, 0.0, 1.0),
          "(i) Choose the open, grassy site away from buildings and trees so the "
          "screen records the true air temperature; reasons: away from heat "
          "radiated by buildings/paths, and on grass which does not absorb and "
          "re-radiate heat like concrete. (ii) Labelled water cycle: evaporation, "
          "condensation, precipitation, surface runoff/collection.",
          "B1/B2 per part; B-marks for labelled diagram",
          stem="Fig.22: layout plan of a school with sites A, B, C and D.",
          topic_id=303)

    db.commit()
    print(f"Seeded St. Gabriel's Geography 2013 exam id={exam.id}: "
          f"{len(p1.questions)} question rows.")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
