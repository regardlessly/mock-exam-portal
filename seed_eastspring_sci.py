"""Seed East Spring Secondary School 2019 Sec 1 Express Science (Section A MCQ)."""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/science/2019-Sec-1-Express-Science-SA2-East-Spring-Secondary.pdf"
IMAGES_DIR = "/tmp/eastspring_sci_pages"

init_db()


def add_q(db, paper_id, exam_dir, paper_num, num, text, topic, topic_id,
          pdf_page, crop_region, answer_text):
    img_name = f"q{paper_num}_{num}.png"
    img_path = os.path.join(exam_dir, img_name)
    pg, top, bot = crop_region
    crop_question_image(PDF_PATH, pg, top, bot, img_path)
    q = Question(
        paper_id=paper_id, question_number=num, part=None, stem=None,
        question_text=text, marks=1, topic=topic, topic_id=topic_id,
        page_image=img_name, pdf_page=pdf_page,
    )
    db.add(q)
    db.flush()
    db.add(Answer(question_id=q.id, answer_text=answer_text, mark_scheme="B1"))
    return q


def main():
    db = SessionLocal()

    school = db.query(School).filter(School.name == "East Spring Secondary School").first()
    if not school:
        school = School(name="East Spring Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(
        Exam.school_id == school.id, Exam.year == 2019,
        Exam.subject == "Science").first()
    if existing:
        print(f"East Spring Science 2019 already seeded (id={existing.id}). Re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id, title="Second Semestral Assessment 2019", year=2019,
        level="Secondary 1 Express", subject="Science",
        source_pdf="2019-Sec-1-Express-Science-SA2-East-Spring-Secondary.pdf",
        status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    # ══════════════════════════════════════════════
    # SECTION A — Multiple Choice, 30 questions, pages 2-10 (idx 1-9)
    # ══════════════════════════════════════════════
    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=60, total_marks=30,
               date=date(2019, 10, 4),
               instructions="Section A. Answer all questions on the OTAS.")
    db.add(p1); db.flush()

    add_q(db, p1.id, exam_dir, 1, 1,
        r"The following hazard symbols are found on a bottle containing a chemical in the laboratory. What can be concluded from them?"
        "\n\nA. The liquid can cause cell damage."
        "\nB. The liquid can be touched with bare hands."
        "\nC. The liquid cannot be used near a naked flame."
        "\nD. The liquid will explode when it is poured out of the container.",
        "Laboratory Safety / Hazard Symbols", 101, 2, (1, 0.06, 0.28),
        "A — the hazard symbols indicate the liquid can cause cell/tissue damage.")

    add_q(db, p1.id, exam_dir, 1, 2,
        r"A student tried to light up a Bunsen burner and a strikeback occurred. What could be the cause of the strikeback?"
        "\n\nA. The barrel was not cleaned properly."
        "\nB. Insufficient gas from the gas tap."
        "\nC. There was a crack in the collar."
        "\nD. The air-hole was opened.",
        "Laboratory Apparatus — Bunsen burner", 101, 2, (1, 0.28, 0.44),
        "D — a strikeback occurs when the air-hole is opened (too much air mixes with gas).")

    add_q(db, p1.id, exam_dir, 1, 3,
        r'A student carried out an experiment and recorded the statement: "When the current increases, the filament in the light bulb turns from orange to bright red." Which stage of the scientific method is the student carrying out?'
        "\n\nA. asking a question\nB. constructing a hypothesis\nC. drawing a conclusion\nD. analysing data",
        "Scientific Method", 101, 2, (1, 0.44, 0.62),
        "C — recording an observed outcome relationship is drawing a conclusion.")

    add_q(db, p1.id, exam_dir, 1, 4,
        r"The diagram below shows a plant cell. Which structure is also present in an animal cell?"
        "\n\nA. structure A\nB. structure B\nC. structure C\nD. structure D",
        "Cells — Plant vs Animal", 107, 2, (1, 0.62, 0.95),
        "A — the structure common to both plant and animal cells (e.g. nucleus/cytoplasm) is A.")

    add_q(db, p1.id, exam_dir, 1, 5,
        r"The human blood consists of red blood cells, white blood cells, platelets and plasma. Which of the following structure represents the human blood?"
        "\n\nA. cell\nB. tissue\nC. organ\nD. system",
        "Cells — Organisation", 107, 3, (2, 0.04, 0.18),
        "B — blood is a tissue (a group of cells working together).")

    add_q(db, p1.id, exam_dir, 1, 6,
        r"The diagram below shows a specialised plant cell. For what function is this cell modified?"
        "\n\nA. transport of water\nB. exchange of gases\nC. photosynthesis\nD. storage of food",
        "Cells — Specialisation", 107, 3, (2, 0.18, 0.46),
        "A — the cell (root hair / xylem-type) is modified for transport of water.")

    add_q(db, p1.id, exam_dir, 1, 7,
        r"Which part of the plant cell is responsible for controlling substances entering or leaving the cell?"
        "\n\nA. cell wall\nB. cell membrane\nC. chloroplast\nD. vacuole",
        "Cells — Structure & Function", 107, 3, (2, 0.46, 0.62),
        "B — the cell membrane controls the substances entering or leaving the cell.")

    add_q(db, p1.id, exam_dir, 1, 8,
        r"In which situation would diffusion occur fastest?"
        "\n\nA. aroma of freshly cooked food travelling through the air"
        "\nB. coloured dye mixing with a liquid"
        "\nC. food particles entering the living cells"
        "\nD. sugar dissolving in a liquid",
        "Movement of Substances — Diffusion", 108, 3, (2, 0.62, 0.78),
        "A — diffusion is fastest in gases, so aroma travelling through air is fastest.")

    add_q(db, p1.id, exam_dir, 1, 9,
        r"Andy extracted a component of blood and observed it under a microscope. He found that the component contained cells with nuclei. Which blood component was extracted?"
        "\n\nA. red blood cell\nB. white blood cell\nC. platelets\nD. plasma",
        "Transport in Living Things — Blood", 110, 3, (2, 0.78, 0.95),
        "B — only white blood cells contain a nucleus.")

    add_q(db, p1.id, exam_dir, 1, 10,
        r"The diagrams below show the apparatus used in an experiment with dialysis tubing, distilled water and sugar solution. In which tubes will osmosis take place?"
        "\n\nA. 1 & 2\nB. 1 & 4\nC. 2 & 3\nD. 3 & 4",
        "Movement of Substances — Osmosis", 108, 4, (3, 0.04, 0.34),
        "D — osmosis occurs where a water concentration gradient exists across the partially permeable tubing (tubes 3 & 4).")

    add_q(db, p1.id, exam_dir, 1, 11,
        r"A ring of bark was removed from a woody shoot undergoing photosynthesis, leaving only the xylem intact. Which of the following diagram represents the appearance of the stem a few weeks later?"
        "\n\nA. diagram A\nB. diagram B\nC. diagram C\nD. diagram D",
        "Transport in Plants — Phloem", 110, 4, (3, 0.34, 0.95),
        "B — sugars accumulate above the ring as phloem is removed, causing a swelling above the cut.")

    add_q(db, p1.id, exam_dir, 1, 12,
        r"A student used a pair of vernier calipers to measure the diameter of a test tube. What is the diameter of the test tube?"
        "\n\nA. 2.40 cm\nB. 2.14 cm\nC. 3.10 cm\nD. 2.54 cm",
        "Measurement — Vernier calipers", 102, 5, (4, 0.04, 0.30),
        "B — main scale 2 cm plus vernier reading gives 2.14 cm.")

    add_q(db, p1.id, exam_dir, 1, 13,
        r"Three balls have densities of 1.8 g/cm$^3$, 1.9 g/cm$^3$ and 2.2 g/cm$^3$ respectively. They are immersed in a beaker containing a liquid with a density of 2.1 g/cm$^3$. Which option most accurately shows what you will observe?"
        "\n\nA. option A\nB. option B\nC. option C\nD. option D",
        "Density — Floating and Sinking", 102, 5, (4, 0.30, 0.62),
        "C — balls less dense than the liquid (1.8, 1.9) float; the 2.2 g/cm$^3$ ball sinks.")

    add_q(db, p1.id, exam_dir, 1, 14,
        r"The picture below shows a drill, with a diamond on the tip of the drill bit. Which of the following physical properties explains why diamonds are used in drill bits?"
        "\n\nA. flexibility\nB. strength\nC. hardness\nD. density",
        "Materials — Properties", 101, 5, (4, 0.62, 0.95),
        "C — diamond is used because of its extreme hardness.")

    add_q(db, p1.id, exam_dir, 1, 15,
        r"A freshly baked cake is placed on a table. Which of the following describes the way the cake loses heat?"
        "\n\nA. conduction only\nB. convection only\nC. conduction and convection\nD. conduction, convection and radiation",
        "Energy — Heat Transfer", 111, 5, (4, 0.95, 1.00),
        "D — the cake loses heat by conduction, convection and radiation.")

    add_q(db, p1.id, exam_dir, 1, 16,
        r"Which of the following statements about radiation is incorrect?"
        "\n\nA. Black surfaces are good emitters of radiation."
        "\nB. Objects with higher temperature emit radiation at a lower rate."
        "\nC. Objects with larger surface area absorb radiation at a higher rate."
        "\nD. Radiation can travel through a vacuum.",
        "Energy — Radiation", 111, 6, (5, 0.04, 0.22),
        "B — hotter objects emit radiation at a higher rate, not a lower rate, so B is incorrect.")

    add_q(db, p1.id, exam_dir, 1, 17,
        r"An experimental setup is shown. The glass rod and the copper rod are of equal lengths. Each pin is attached to a rod with an equal amount of wax. Which pin will drop last?"
        "\n\nA. pin A\nB. pin B\nC. pin C\nD. pin D",
        "Energy — Conduction", 111, 6, (5, 0.22, 0.50),
        "A — glass is a poor conductor, so the pin furthest along the glass rod (pin A) drops last.")

    add_q(db, p1.id, exam_dir, 1, 18,
        r"Which of the following diagrams shows the correct direction of the convection current set up in the box?"
        "\n\nA. diagram A\nB. diagram B\nC. diagram C\nD. diagram D",
        "Energy — Convection", 111, 6, (5, 0.50, 0.95),
        "A — warm air rises above the candle and cool air sinks down the other chimney, giving the convection current in diagram A.")

    add_q(db, p1.id, exam_dir, 1, 19,
        r"An object is placed on a beam balance and on a compression spring balance on Earth. The same experiment is then repeated on Moon. Which set of observations is true about the beam balance and the spring balance readings?"
        "\n\nA. beam balance reads less on Moon, spring balance reads less on Moon"
        "\nB. beam balance reads less on Moon, spring balance reads the same on Moon"
        "\nC. beam balance reads the same on Moon, spring balance reads less on Moon"
        "\nD. beam balance reads the same on Moon, spring balance reads the same on Moon",
        "Forces — Mass and Weight", 112, 7, (6, 0.04, 0.34),
        "C — the beam balance compares mass (unchanged), but the spring balance measures weight, which is less on the Moon.")

    add_q(db, p1.id, exam_dir, 1, 20,
        r"A student stood on a weighing scale to measure her mass. She first stood on the scale on both feet, then changed to standing on one foot. Which of the following statements is true?"
        "\n\nA. The pressure exerted on the scale doubled when she changed to standing on one foot."
        "\nB. The pressure exerted on the scale halved when she changed to standing on one foot."
        "\nC. The reading on the weighing scale doubled when she changed to standing on one foot."
        "\nD. The reading on the weighing scale halved when she changed to standing on one foot.",
        "Forces — Pressure", 112, 7, (6, 0.34, 0.55),
        "A — total force is unchanged but contact area halves, so the pressure doubles.")

    add_q(db, p1.id, exam_dir, 1, 21,
        r"Forces were applied on a particular box: 3 N to the left (top), 9 N to the left, and 13 N to the right. What is the resultant force?"
        "\n\nA. 13 N to the right\nB. 1 N to the right\nC. 12 N to the left\nD. 1 N to the left",
        "Forces — Resultant Force", 112, 7, (6, 0.55, 0.78),
        "B — resultant = 13 − (3 + 9) = 1 N to the right.")

    add_q(db, p1.id, exam_dir, 1, 22,
        r"A soccer player took a penalty kick from a spot in front of the goalpost. Which effect of a force was applied?"
        "\n\nA. stopping a moving object"
        "\nB. moving a stationary object"
        "\nC. changing the shape of an object"
        "\nD. changing the direction of a moving object",
        "Forces — Effects of Forces", 112, 7, (6, 0.78, 0.95),
        "B — kicking a stationary ball moves a stationary object.")

    add_q(db, p1.id, exam_dir, 1, 23,
        r"In a theme park, passengers on a roller coaster are initially at rest at the top of the track at point X. The roller coaster then travels down and round a circular loop in the track at Y. What forms of energy are present at X and at Y?"
        "\n\nA. X kinetic only, Y gravitational potential only"
        "\nB. X kinetic and gravitational potential, Y kinetic only"
        "\nC. X gravitational potential only, Y kinetic and gravitational potential"
        "\nD. X gravitational potential only, Y kinetic only",
        "Energy — Conservation", 111, 8, (7, 0.04, 0.34),
        "C — at rest at the top X has only gravitational PE; at Y it has both KE and gravitational PE.")

    add_q(db, p1.id, exam_dir, 1, 24,
        r"An archer pulls a bow before releasing and shooting the arrow. Which of the following energy conversions is correct of the action above?"
        "\n\nA. chemical potential energy → elastic potential energy → kinetic energy"
        "\nB. elastic potential energy → chemical potential energy → kinetic energy"
        "\nC. kinetic energy → chemical potential energy → elastic potential energy"
        "\nD. chemical potential energy → kinetic energy → elastic potential energy",
        "Energy — Conversions", 111, 8, (7, 0.34, 0.58),
        "A — chemical PE (muscles) → elastic PE (bow) → kinetic energy (arrow).")

    add_q(db, p1.id, exam_dir, 1, 25,
        r"Which of the following statements indicate the possible ways to use renewable energy sources? "
        r"I. Build wind turbines to generate electricity using wind. "
        r"II. Install solar panels on the roof tops of buildings to capture solar energy. "
        r"III. Use charcoal instead of liquefied petroleum gas (LPG) for cooking food."
        "\n\nA. I & II only\nB. I & III only\nC. II & III only\nD. I, II and III",
        "Energy — Renewable Sources", 111, 8, (7, 0.58, 0.95),
        "A — I and II use renewable sources; charcoal (III) is non-renewable.")

    add_q(db, p1.id, exam_dir, 1, 26,
        r"Singapore is an industrialized small island country with limited land space. Being near the equator, it is sunny all year round. Suggest which type of renewable energy is suitable to be harvested in Singapore."
        "\n\nA. solar energy\nB. wind energy\nC. geothermal energy\nD. biofuel energy",
        "Energy — Renewable Sources", 111, 9, (8, 0.04, 0.22),
        "A — Singapore's sunny equatorial climate makes solar energy most suitable.")

    add_q(db, p1.id, exam_dir, 1, 27,
        r"A circuit with one light bulb is set up. What happens to the brightness of the light bulb when a second identical light bulb is added in series to the circuit?"
        "\n\nA. It becomes dimmer.\nB. It becomes brighter.\nC. The bulbs will not light up.\nD. There is no change in brightness.",
        "Electrical Systems — Series Circuits", 113, 9, (8, 0.22, 0.46),
        "A — adding a bulb in series increases resistance, so each bulb becomes dimmer.")

    add_q(db, p1.id, exam_dir, 1, 28,
        r"The diagram shows four resistors of equal resistance connected to a battery. In which resistor does the current have the largest value?"
        "\n\nA. resistor A\nB. resistor B\nC. resistor C\nD. resistor D",
        "Electrical Systems — Current", 113, 9, (8, 0.46, 0.78),
        "A — resistor A carries the full main-circuit current, the largest value.")

    add_q(db, p1.id, exam_dir, 1, 29,
        r"Many electrical equipment should not be plugged into the same socket. Why is this so?"
        "\n\nA. The fuse will keep \"blowing\"."
        "\nB. There is a risk of an electric shock."
        "\nC. There is a risk of an electrical fire."
        "\nD. The insulation will become damaged.",
        "Electrical Systems — Safety", 113, 9, (8, 0.78, 0.95),
        "C — overloading a socket draws excessive current, creating a risk of an electrical fire.")

    add_q(db, p1.id, exam_dir, 1, 30,
        r"Which fuse rating is suitable for a device that requires 8 A to function?"
        "\n\nA. 7 A\nB. 8 A\nC. 9 A\nD. 10 A",
        "Electrical Systems — Fuses", 113, 10, (9, 0.04, 0.30),
        "C — the fuse rating should be slightly above the operating current, so 9 A is suitable.")

    db.commit()
    p1_count = len(p1.questions)
    print(f"Seeded East Spring Science exam id={exam.id}: Section A ({p1_count} MCQs)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
