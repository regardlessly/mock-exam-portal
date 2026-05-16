"""Seed Woodlands Secondary School EOY 2017 Sec 1 Express Science exam (MCQ).

This PDF contains two papers:
  - Biology paper: Section A MCQ Q1-15  (PDF pages 2-7, idx 1-6; idx 0 = cover)
  - Physics paper: Section A MCQ Q5-15  (PDF pages 24-28, idx 23-27;
        idx 22 = cover. Physics Q1-4 are not present in this scan.)
Answer keys taken from the embedded mark schemes.
"""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/science/2017-Sec-1-Express-Science-SA2-Woodlands-Secondary.pdf"
IMAGES_DIR = "/tmp/woodlands_sci2017_lowres"

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

    school = db.query(School).filter(School.name == "Woodlands Secondary School").first()
    if not school:
        school = School(name="Woodlands Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(
        Exam.school_id == school.id, Exam.year == 2017, Exam.subject == "Science"
    ).first()
    if existing:
        print(f"Woodlands 2017 Science already seeded (id={existing.id}). Deleting and re-seeding.")
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
        source_pdf="2017-Sec-1-Express-Science-SA2-Woodlands-Secondary.pdf",
        status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # PAPER 1 — Biology Section A MCQ, Q1-15 (15 marks)
    # PDF pages 2-7 (idx 1-6)
    # Key: 1B 2B 3D 4B 5B 6D 7D 8A 9B 10C 11B 12C 13A 14D 15C
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=60, total_marks=15,
               date=date(2017, 10, 11),
               instructions="Science (Biology) — Section A: Multiple Choice Questions. Answer all questions. Four options A, B, C and D.")
    db.add(p1); db.flush()

    P1 = [
        (1, "Which structure is found in plant cells but not in animal cells?\nA cell membrane\nB cell wall\nC nucleus\nD small vacuole",
         "Cells — Plant and Animal", 107, 2, (1, 0.05, 0.25), "B"),
        (2, "The following diagram shows an electron micrograph of an animal cell. Which structure is responsible for protein synthesis? (parts A, B, C, D labelled)",
         "Cells — Structure and Function", 107, 2, (1, 0.25, 0.55), "B"),
        (3, "The photomicrograph below shows the appearance of two red blood cells viewed under the same magnification (defective red blood cell / normal red blood cell). Which description about the defective red blood cell is correct?\nA It contains a nucleus while the normal red blood cell does not.\nB It has the capacity to carry more oxygen than the normal red blood cell.\nC It has a lower water potential than the normal red blood cell.\nD It has a smaller surface area to volume ratio than the red blood cell.",
         "Specialised Cells — Red Blood Cell", 107, 2, (1, 0.55, 0.95), "D"),
        (4, "The diagram shows a blood vessel. A section of the blood vessel wall has been cut to show the blood flowing inside. Which option correctly identifies the order of classification for P and Q?\nA P cell / Q organ\nB P organ / Q cells\nC P organ / Q tissue\nD P tissue / Q organ",
         "Cellular Organisation", 107, 3, (2, 0.05, 0.55), "B"),
        (5, "An experiment was set up with visking tubing containing glucose solution placed in distilled water and left for half an hour. The process responsible for the movement of glucose molecules out of the visking tubing is\nA osmosis.\nB diffusion.\nC absorption.\nD transport.",
         "Movement of Substances — Diffusion", 108, 3, (2, 0.55, 0.95), "B"),
        (6, "The diagram shows a set-up used to investigate osmosis (tube, distilled water, concentrated starch solution, partially permeable membrane). Which molecules will move across the partially permeable membrane and how will levels 1 and 2 change?\nA starch / level 1 fall / level 2 rise\nB starch / level 1 rise / level 2 fall\nC water / level 1 fall / level 2 rise\nD water / level 1 rise / level 2 fall",
         "Movement of Substances — Osmosis", 108, 4, (3, 0.05, 0.45), "D"),
        (7, "Concentrated salt solution accidentally flooded a field of young rice plants. The graph shows the effect on two varieties of rice plants, X and Y, in the field. What caused the effect shown by the graph?\nA Water enters the root cells of plants X.\nB Water enters the root cells of plants Y.\nC Water leaves the root cells of plants X.\nD Water leaves the root cells of plants Y.",
         "Movement of Substances — Osmosis", 108, 4, (3, 0.45, 0.95), "D"),
        (8, "The diagram below shows cells in fresh blood and the same cells after it has been mixed with liquid X. Which statement describes the water potential of liquid X?\nA It is lower than that of the cell cytoplasm.\nB It is equal to that of the cell cytoplasm.\nC It is higher than that of the cell cytoplasm.\nD It is equal to that of distilled water.",
         "Movement of Substances — Osmosis", 108, 5, (4, 0.05, 0.55), "A"),
        (9, "The table below shows the percentage nutritional content of four different food substances (carbohydrates / fats / protein). Which of the following food should be avoided by someone who suffers from obesity?\nA carbs 11.5 / fats 15.0 / protein 73.5\nB carbs 12.0 / fats 75.6 / protein 12.4\nC carbs 15.1 / fats 60.4 / protein 24.5\nD carbs 45.2 / fats 16.4 / protein 38.4",
         "Human Digestive System — Diet", 109, 5, (4, 0.55, 0.95), "B"),
        (10, "Which of the following substances are built from amino acids?\nA bread\nB butter\nC lean meat\nD potato chips",
         "Human Digestive System — Nutrients", 109, 5, (4, 0.95, 1.0), "C"),
        (11, "The diagram below represents three types of nutrients found in food (P, Q, R). What are P, Q and R?\nA P fat / Q carbohydrate / R protein\nB P carbohydrate / Q fat / R protein\nC P protein / Q carbohydrate / R fat\nD P protein / Q fat / R carbohydrate",
         "Human Digestive System — Nutrients", 109, 6, (5, 0.05, 0.45), "B"),
        (12, "In which order do these events occur in human nutrition?\nA digestion -> ingestion -> absorption -> assimilation\nB digestion -> ingestion -> assimilation -> absorption\nC ingestion -> digestion -> absorption -> assimilation\nD ingestion -> digestion -> assimilation -> absorption",
         "Human Digestive System", 109, 6, (5, 0.45, 0.70), "C"),
        (13, "Which organ is not part of the alimentary canal? (parts A, B, C, D labelled on diagram)\nA A\nB B\nC C\nD D",
         "Human Digestive System — Organs", 109, 6, (5, 0.70, 0.95), "A"),
        (14, "Litmus paper turns red in acidic solutions and blue in alkaline solutions. Which part of the alimentary canal has secretions that would change litmus paper red?\nA colon\nB duodenum\nC ileum\nD stomach",
         "Human Digestive System — Enzymes", 109, 7, (6, 0.05, 0.40), "D"),
        (15, "The following figure shows the changes in the amounts of nutrients X, Y and Z as they pass through the different parts of the human alimentary canal. What nutrients are X, Y and Z?\nA X carbohydrate / Y fat / Z protein\nB X carbohydrate / Y protein / Z fat\nC X fat / Y carbohydrate / Z protein\nD X protein / Y carbohydrate / Z fat",
         "Human Digestive System — Digestion", 109, 7, (6, 0.40, 0.95), "C"),
    ]
    for num, text, topic, tid, pg, crop, ans in P1:
        add_q(db, p1.id, exam_dir, 1, num, None, text, 1, topic, pg, crop,
              f"{ans}", "B1", topic_id=tid)

    # ══════════════════════════════════════════════
    # PAPER 2 — Physics Section A MCQ, Q5-15 (Q1-4 not in scan)
    # PDF pages 24-28 (idx 23-27)
    # Key: 5A 6C 7C 8C 9B 10B 11A 12D 13D 14B 15D
    # ══════════════════════════════════════════════
    p2 = Paper(exam_id=exam.id, paper_number=2, duration_minutes=60, total_marks=11,
               date=date(2017, 10, 11),
               instructions="Science (Physics) — Section A: Multiple Choice Questions (Q5-15; Q1-4 not available in source scan). Four options A, B, C and D.")
    db.add(p2); db.flush()

    P2 = [
        (5, "Which of the following is the correct order of the speed of sound from the fastest to the slowest?\nA Iron -> Water -> Air\nB Water -> Air -> Iron\nC Air -> Water -> Iron\nD Water -> Iron -> Air",
         "Sound", 111, 24, (23, 0.05, 0.30), "A"),
        (6, "A guitarist wants to play a note of higher pitch with his guitar string. What will be the change in the frequency and vibration of the guitar string?\nA frequency decrease / vibration faster\nB frequency decrease / vibration slower\nC frequency increase / vibration faster\nD frequency increase / vibration slower",
         "Sound — Pitch and Frequency", 111, 24, (23, 0.30, 0.55), "C"),
        (7, "A student stands in front of a building and shouts. She hears an echo. What happens to the echo when she shouts at a greater distance from the building?\nA It is louder and takes a longer time to reach her.\nB It is louder and takes a shorter time to reach her.\nC It is softer and takes a longer time to reach her.\nD It is softer and takes a shorter time to reach her.",
         "Sound — Echo", 111, 24, (23, 0.55, 0.80), "C"),
        (8, "Which of the following statements about sound is incorrect?\nA A body must vibrate in order to produce sound.\nB Sound cannot pass through vacuum.\nC Sound travels at the same speed as light in air.\nD Sound carries energy from one place to another.",
         "Sound", 111, 24, (23, 0.80, 1.0), "C"),
        (9, "A student puts a bell into a jar, and switches it on so that it rings continuously. He turns on the vacuum pump to remove air from the jar slowly. What will the student hear as the air is being pumped out?\nA The bell will sound louder.\nB The bell will sound softer.\nC There will be no change in loudness.\nD There will be no sound instantly.",
         "Sound — Transmission", 111, 25, (24, 0.05, 0.45), "B"),
        (10, "An image which cannot be caught on a screen is known as a\nA real image\nB virtual image\nC diminished image\nD magnified image",
         "Ray Model of Light — Images", 114, 25, (24, 0.45, 0.65), "B"),
        (11, "The diagram below shows an object, X, placed 2 metres in front of a plane mirror. At which position is the object's image located? (positions A, B, C, D at 2 m intervals)\nA A\nB B\nC C\nD D",
         "Ray Model of Light — Reflection", 114, 25, (24, 0.65, 0.95), "A"),
        (12, "The diagram shows the position of the Sun above a house. Sunlight cannot pass through the roof of the house, but there is a hole that allows light to pass through. The walls and roof of the house are not reflective. Which point will be in the shadow?\nA A\nB B\nC C\nD D",
         "Ray Model of Light — Shadows", 114, 26, (25, 0.05, 0.50), "D"),
        (13, "A student stands in front of a mirror at point S. There are objects placed at points X, Y and Z. How many images of the objects can the student see in the mirror?\nA 0\nB 1\nC 2\nD 3",
         "Ray Model of Light — Reflection", 114, 26, (25, 0.50, 0.95), "D"),
        (14, "A ray of light travels from medium X to medium Y. If medium X is optically denser than medium Y, which of the following correctly shows the light path? (diagrams A, B, C, D)",
         "Ray Model of Light — Refraction", 114, 27, (26, 0.05, 0.95), "B"),
        (15, "A mirror is tilted at an angle of 30 degrees to the bench. A ray of light is directed so that it hits the mirror at an angle of 20 degrees to the surface of the mirror. What is the angle of reflection?\nA 20 degrees\nB 30 degrees\nC 50 degrees\nD 70 degrees",
         "Ray Model of Light — Reflection", 114, 28, (27, 0.05, 0.50), "D"),
    ]
    for num, text, topic, tid, pg, crop, ans in P2:
        add_q(db, p2.id, exam_dir, 2, num, None, text, 1, topic, pg, crop,
              f"{ans}", "B1", topic_id=tid)

    db.commit()
    p1_count = len(p1.questions)
    p2_count = len(p2.questions)
    print(f"Seeded Woodlands 2017 Science exam id={exam.id}: "
          f"Paper 1 Biology MCQ ({p1_count}), Paper 2 Physics MCQ ({p2_count})")
    print(f"Total questions: {p1_count + p2_count}")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
