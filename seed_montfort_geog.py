"""Seed Montfort Secondary School EOY 2022 Sec 2 Express Geography exam."""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/montfort_geog.pdf"

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

    school = db.query(School).filter(School.name == "Montfort Secondary School").first()
    if not school:
        school = School(name="Montfort Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(
        Exam.school_id == school.id, Exam.year == 2022,
        Exam.subject == "Geography",
    ).first()
    if existing:
        print(f"Montfort Geography 2022 already seeded (id={existing.id}). Re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id, title="End-of-Year Examination 2022", year=2022,
        level="Secondary 2 Express", subject="Geography",
        source_pdf="montfort_geog.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)

    # ══════════════════════════════════════════════
    # PAPER 1 — Geography, 36 marks, 1 hour 15 minutes
    # Section A: Q1 Housing (18). Section B: Q2 Transport (18).
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=75, total_marks=36,
               date=date(2022, 10, 7), instructions="Answer all questions. Candidates should support their answers with the use of relevant examples.")
    db.add(p1); db.flush()

    # ── Section A — Q1 Housing ──
    # Q1 stem: Fig. 1 = line graph of percentage urbanisation in China 1980-2020.
    fig1_stem = ("Section A. Study Fig. 1, which shows the percentage of urbanisation "
                 "in China from 1980 to 2020. The line graph shows urban population "
                 "as a percentage of total population: 1980 = 19.4%, 1985 = 23.7%, "
                 "1990 = 26.5%, 1995 = 29.1%, 2000 = 32%, 2005 = 44.1%, 2010 = 50.1%, "
                 "2015 = 57.3%, 2020 = 63.8%.")

    add_q(db, p1.id, exam_dir, 1, 1, "a",
        "Describe the trends in the percentage of urbanisation in China from 1980 to 2020.",
        3, "Urbanisation Trends", 2, (1, 0.10, 0.95),
        "The percentage of urbanisation increased overall from 19.4% in 1980 to "
        "63.8% in 2020, an increase of 44.4 percentage points. The increase was "
        "gradual from 1980 to 2000 (19.4% to 32%), then increased more rapidly "
        "from 2000 to 2020 (32% to 63.8%).",
        "B1 overall increase with figures, B1 gradual phase, B1 rapid phase",
        stem=fig1_stem, topic_id=312)

    add_q(db, p1.id, exam_dir, 1, 1, "b",
        "Study Fig. 2, which shows a photograph of a slum in New Delhi, India. "
        "With reference to Fig. 2, describe the location of the slum and suggest "
        "two reasons why it is not a safe shelter for its residents.",
        3, "Informal Housing / Slums", 3, (2, 0.05, 0.95),
        "The slum is located next to (along) a railway line / railway track on "
        "marginal land. It is not safe because the makeshift materials such as "
        "canvas, plastic sheets and wooden sticks which increase the risk of "
        "fires; and because dwellings are built close to the railway with poor "
        "sanitation and overcrowding, making residents vulnerable to accidents "
        "and disease.",
        "B1 location next to railway/marginal land, B1+B1 two valid safety reasons",
        topic_id=312)

    add_q(db, p1.id, exam_dir, 1, 1, "c",
        "Explain how the expansion of cities can result in negative impacts to "
        "forests and water resources.",
        4, "Urban Expansion Impacts", 4, (3, 0.05, 0.55),
        "Forests: to build housing and transport infrastructure, more land is "
        "needed, leading to greater demand for clean water to be drawn for "
        "construction and use, and forests are cleared (depletion of forests). "
        "Water resources: as populations grow, more resources such as building "
        "materials and fuel for cooking and warmth are needed; resources are "
        "extracted and depleted, and household and industrial waste can lead to "
        "the disposal of waste directly or as leakage into waterways, resulting "
        "in water pollution.",
        "Up to 2m forests, up to 2m water resources",
        topic_id=309)

    fig3_stem = ("Study Figs. 3A and 3B, which show features of sustainable housing "
                 "in Singapore. Fig. 3A shows residential blocks with solar panels "
                 "mounted on the rooftops of HDB flats. Fig. 3B shows the 'Tree "
                 "House' condominium covered with a large vertical garden of "
                 "different types of plants.")
    add_q(db, p1.id, exam_dir, 1, 1, "d",
        "Identify and explain how environmentally friendly features of housing "
        "seen in Fig. 3A and 3B promote environmental sustainability in Singapore.",
        4, "Sustainable Housing", 5, (4, 0.45, 0.95),
        "Solar panels (Fig. 3A): they tap on sunlight, a renewable source of "
        "energy, which is converted to electricity, reducing reliance on fossil "
        "fuels and lowering carbon emissions. Green walls / vertical gardens "
        "(Fig. 3B): the plants provide shade and surrounding temperatures are "
        "lowered, so there is less need for air-conditioning, which lowers "
        "energy consumption and carbon emissions.",
        "2m for solar panels feature + explanation, 2m for green wall feature + explanation",
        stem=fig3_stem, topic_id=312)

    add_q(db, p1.id, exam_dir, 1, 1, "e",
        "Explain how land-use planning affects the location of formal and "
        "informal housing in cities.",
        2, "Land-use Planning", 5, (5, 0.05, 0.45),
        "Land-use planning provides guidelines drawn by planning authorities "
        "who typically practise zoning, so the built environment is well "
        "developed. Formal housing is built where it is allocated and "
        "land-use is permitted, while informal housing tends to spring up on "
        "land that is not designed for housing development, often where "
        "regulations are not enforced.",
        "B1 role of zoning/guidelines, B1 contrast formal vs informal location",
        topic_id=312)

    add_q(db, p1.id, exam_dir, 1, 1, "f",
        "Explain why it is important to make public housing inclusive in cities.",
        2, "Inclusive Housing", 5, (5, 0.45, 0.85),
        "Inclusive housing ensures developments cater to people of all ages and "
        "physical abilities, for example with barrier-free access and ramps for "
        "the elderly and persons with disabilities. It also provides a range of "
        "housing to cater for different groups, meeting their varying needs and "
        "fostering social mixing.",
        "B1 cater to all ages/abilities, B1 range of housing for different groups",
        topic_id=312)

    # ── Section B — Q2 Transport ──
    add_q(db, p1.id, exam_dir, 1, 2, "a",
        "Section B. Identify and explain two reasons for the need of transport "
        "systems to be in cities.",
        4, "Need for Transport Systems", 7, (6, 0.05, 0.55),
        "Movement of people: transport allows individuals to commute to work, "
        "school or access social activities and services. Movement of goods and "
        "services: businesses and consumers need transport to move raw materials "
        "and goods to and from businesses and consumers. Connecting different "
        "transport modes: journeys made from one location to another can be made "
        "of several transport systems connected at point-to-point networks.",
        "2m per reason (identification + explanation), max 4m",
        topic_id=312)

    fig4_stem = ("Study Fig. 4, which shows a map of the Shinkansen rail system in "
                 "Japan in 2016. The map indicates 'High Frequency and Capacity': "
                 "number of train services per day = 373; number of passengers per "
                 "day = 477,000; number of seating available = 1323.")
    add_q(db, p1.id, exam_dir, 1, 2, "b",
        "Transport infrastructure is key to moving people and goods. The "
        "Shinkansen in Japan is a high-speed rail system which connects people "
        "from one place to another efficiently. With reference to Fig. 4, "
        "describe two indicators which show that the Shinkansen rail system is "
        "a form of high-quality transport infrastructure in Japan. Provide "
        "evidence from Fig. 4 to support your answer.",
        4, "High-quality Transport Infrastructure", 9, (7, 0.05, 0.95),
        "High capacity: the Shinkansen can transport a large number of "
        "passengers, with up to 477,000 passengers per day and 1323 seats "
        "available, showing it serves many users efficiently. High frequency: "
        "there are 373 train services per day, so trains run very regularly, "
        "reducing waiting time and reliably moving large numbers of people.",
        "2m per indicator with evidence from Fig. 4, max 4m",
        stem=fig4_stem, topic_id=312)

    add_q(db, p1.id, exam_dir, 1, 2, "c",
        "Study Fig. 5, which shows the traffic conditions during morning "
        "peak-hour period in Singapore (a congested road full of cars). With "
        "reference to Fig. 5 and your knowledge, identify and describe two "
        "negative impacts caused by transport systems in cities.",
        4, "Negative Impacts of Transport", 10, (9, 0.05, 0.55),
        "Traffic congestion: a large road usage and a large number of vehicles "
        "lead to traffic congestion, increasing travelling time and causing "
        "frustration. Health and safety risks: vehicles emit harmful air "
        "pollutants and carbon dioxide, which can cause respiratory problems "
        "and a higher risk of lung cancer and accidents while travelling.",
        "2m per impact (identify + describe), max 4m",
        topic_id=312)

    add_q(db, p1.id, exam_dir, 1, 2, "d",
        "Compare the difference between a point-to-point and hub-and-spoke "
        "network. Give an example of a hub-and-spoke network.",
        2, "Transport Networks", 11, (10, 0.05, 0.32),
        "In a point-to-point network there are various laws and policies that "
        "can be implemented to manage people directly from origin to destination, "
        "while in a hub-and-spoke network services connect via a central hub. "
        "Example: an airline network such as Singapore Changi Airport, or "
        "Beijing Daxing International Airport.",
        "B1 valid comparison of the two networks, B1 valid example of hub-and-spoke",
        topic_id=312)

    add_q(db, p1.id, exam_dir, 1, 2, "ei",
        "Explain one strategy that cities adopt to manage transport systems "
        "sustainably.",
        2, "Sustainable Transport Strategy", 11, (10, 0.32, 0.62),
        "Laws and policies on transport, e.g. congestion pricing where road "
        "users pay an additional sum to use a specific stretch of road at "
        "certain times of the day, discouraging the use of private vehicles "
        "and controlling the number of private vehicles. Alternatively, "
        "integrated land use and transport planning ensures the demand for "
        "travel and need for transport infrastructure are well planned so "
        "developments are served by efficient public transport.",
        "B1 valid strategy named, B1 explanation of how it manages transport sustainably",
        topic_id=312)

    add_q(db, p1.id, exam_dir, 1, 2, "eii",
        "Evaluate the effectiveness of the strategy explained in 2e(i).",
        2, "Evaluating Transport Strategies", 11, (10, 0.62, 0.85),
        "Award 1m for benefit and 1m for challenge for the same strategy. "
        "Congestion pricing benefit: road users pay an additional sum to use "
        "a specific stretch of road, hence there is less traffic at these "
        "roads. Challenge: the overall flow of traffic is not reduced, just "
        "diverted to other roads, and systems need to be in place to enforce "
        "regulations and collect fees.",
        "B1 benefit, B1 challenge for the same strategy",
        topic_id=312)

    db.commit()
    p1_count = len(p1.questions)
    print(f"Seeded Montfort Geography exam id={exam.id}: Paper 1 ({p1_count} parts)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
