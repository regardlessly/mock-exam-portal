"""Seed Bedok South Secondary School EOY 2017 Sec 1 Express Science exam (MCQ Section A)."""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/science/2017-Sec-1-Express-Science-SA2-Bedok-South-Secondary.pdf"
IMAGES_DIR = "/tmp/bedoksouth_sci2017_pages"

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

    school = db.query(School).filter(School.name == "Bedok South Secondary School").first()
    if not school:
        school = School(name="Bedok South Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(
        Exam.school_id == school.id, Exam.year == 2017, Exam.subject == "Science"
    ).first()
    if existing:
        print(f"Bedok South 2017 Science already seeded (id={existing.id}). Deleting and re-seeding.")
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
        source_pdf="2017-Sec-1-Express-Science-SA2-Bedok-South-Secondary.pdf",
        status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=120, total_marks=30,
               date=date(2017, 10, 3),
               instructions="Section A: 30 multiple-choice questions. Answer all questions.")
    db.add(p1); db.flush()

    Q = [
        (1, "A series of experiments tested the solubility of substance P in water (varying mass, particle size, water volume, temperature). Which set of apparatus was used to measure the maximum mass of P dissolved and the volume of water used?\nA electronic balance and beaker\nB burette and measuring cylinder\nC spring balance and measuring cylinder\nD electronic balance and measuring cylinder",
         "Measurement Apparatus", 102, 2, (1, 0.05, 0.50), "D"),
        (2, "Refer to the solubility experiments on substance P. Which set of experiments can be used to show that solubility of P does not depend on the size of particles?\nA 1 and 2\nB 1 and 3\nC 1 and 4\nD 2 and 3",
         "Solubility — Experimental Design", 106, 2, (1, 0.50, 0.70), "A"),
        (3, "A chemical powder has the toxic (skull and crossbones) symbol on its bottle. What precaution should a person take when using the powder?\nA Use a spatula when taking out the powder from its bottle.\nB Keep the powder away from the flame, spark or any heat source.\nC Wash down unused powder into the sink with a lot of running water.\nD Wear a face shield and lead-lined clothing before handling the powder.",
         "Laboratory Safety Symbols", 101, 2, (1, 0.70, 0.95), "A"),
        (4, "The figure shows an outline of the area occupied by Singapore on a grid. Each grid square unit measures an area of 20 km^2. What is the approximate area of Singapore?\nA 80 km^2\nB 1 600 km^2\nC 800 km^2\nD 16 000 km^2",
         "Area Measurement", 102, 3, (2, 0.05, 0.40), "C"),
        (5, "The diagram shows four substances P, Q, R and S placed in a measuring cylinder (layered). Which substance has the greatest mass if the volume of each substance is the same?\nA P\nB Q\nC R\nD S",
         "Density", 102, 3, (2, 0.40, 0.62), "D"),
        (6, "A student measured the volume of mercury and the volume of alcohol in two separate measuring cylinders (mercury meniscus convex, alcohol meniscus concave). What are the correct volumes for each liquid?\nA mercury 2.4 cm^3, alcohol 4.5 cm^3\nB mercury 2.6 cm^3, alcohol 4.3 cm^3\nC mercury 4.5 cm^3, alcohol 2.4 cm^3\nD mercury 5.5 cm^3, alcohol 3.6 cm^3",
         "Volume Measurement — Meniscus", 102, 3, (2, 0.62, 0.95), "A"),
        (7, "Which of these groups of elements has an element that has different properties from the rest in the group?\nA iron, lead, tin, copper\nB helium, gallium, chlorine, neon\nC carbon, sulfur, nitrogen, oxygen\nD sodium, caesium, calcium, magnesium",
         "Elements and the Periodic Table", 104, 4, (3, 0.05, 0.27), "B"),
        (8, "Element X is found to have similar chemical properties as nitrogen in the Periodic Table. Which of the following is true about element X?\nA It is a magnetic material.\nB It is an electrical insulator.\nC It has a very high melting point.\nD It belongs to Group III in the Periodic Table.",
         "Elements and the Periodic Table", 104, 4, (3, 0.27, 0.50), "B"),
        (9, "The formula of talcum powder is MgO.SiO2.H2O. What is the number of oxygen atoms in one molecule of talcum powder?\nA 2\nB 3\nC 4\nD 5",
         "Chemical Formulae", 104, 4, (3, 0.50, 0.70), "C"),
        (10, "Which of the sugar solutions will be the most saturated after the sugar has dissolved? (varying water volume and number of sugar cubes)\nA 100 cm^3 water, 3 cubes\nB 75 cm^3 water, 1 cube\nC 60 cm^3 water, 2 cubes\nD 20 cm^3 water, 1 cube",
         "Solutions and Solubility", 106, 4, (3, 0.70, 0.95), "D"),
        (11, "The table shows the colours of four solids W, X, Y, Z and their solubilities (W blue insoluble, X blue soluble, Y white insoluble, Z white soluble). A mixture of two solids was added to water, stirred and filtered. A blue filtrate and a white residue were obtained. Which two solids were present?\nA W and X\nB W and Y\nC X and Y\nD X and Z",
         "Separation Techniques", 105, 5, (4, 0.05, 0.45), "C"),
        (12, "An experiment was set up (distillation of seawater with thermometer, condenser, water in/out). Which correctly identifies the substances at positions X, Y and Z?\nA X seawater, Y seawater, Z water vapour\nB X seawater, Y water vapour, Z pure water\nC X water vapour, Y seawater, Z pure water\nD X water vapour, Y water vapour, Z pure water",
         "Separation — Distillation", 105, 5, (4, 0.45, 0.95), "D"),
        (13, "The diagram shows the process of breaking down a substrate molecule into its products (enzyme action). What represents the substrate?\nA structure A\nB structure B\nC structure C\nD structure D",
         "Enzymes", 109, 6, (5, 0.05, 0.40), "B"),
        (14, "The pie charts show the composition of four different foods A, B, C and D. Which food provides the most energy per serving for people living in cold countries?\nA food A\nB food B\nC food C\nD food D",
         "Diet and Nutrients", 109, 6, (5, 0.40, 0.70), "D"),
        (15, "The list shows various secretions: I bile, II gastric juice, III intestinal juice, IV pancreatic juice, V saliva. Which secretion contains proteases?\nA I, II and III only\nB III, IV and V only\nC II, III and V only\nD II, III, IV and V only",
         "Digestive Enzymes", 109, 6, (5, 0.70, 0.95), "C"),
        (16, "In an experiment, 1 cm^3 of lipase solution was added to a bottle of milk containing bile salts. A few drops of indicator added (acidic = red, neutral = green, alkaline = purple). Which is the colour observed at the beginning of the experiment and after 1 hour?\nA red then red\nB green then purple\nC purple then red\nD purple then purple",
         "Enzymes — Lipase Action", 109, 7, (6, 0.05, 0.45), "B"),
        (17, "The diagram shows a section of the human digestive system. A man ate a drug encased in a film that can be broken down under acidic conditions. This drug can paralyse muscles and cause their loss of function. Which part of the digestive system will first experience loss of function? (A oesophagus, B stomach, C small intestine, D large intestine)",
         "Human Digestive System", 109, 7, (6, 0.45, 0.95), "B"),
        (18, "The graph shows the changes in the percentage of undigested nutrients as food moves along the alimentary canal. Which graph represents the digestion of protein through the alimentary canal? (lines A, B, C, D)",
         "Digestion Along the Alimentary Canal", 109, 8, (7, 0.05, 0.45), "B"),
        (19, "Two metal balls P and Q are suspended 50 cm apart. Which statement about P and Q is true?\nA P and Q have equal density.\nB P and Q have equal volume.\nC P and Q have equal mass and weight.\nD P and Q have equal mass, volume and density.",
         "Mass, Weight and Density", 112, 8, (7, 0.45, 0.72), "C"),
        (20, "The diagram shows four forces acting on a block (3 N right, 4 N right, 2 N left, 7 N left). What is the resultant force?\nA 0 N\nB 5 N to the left\nC 6 N to the right\nD 11 N to the right",
         "Forces — Resultant Force", 112, 8, (7, 0.72, 0.95), "C"),
        (21, "When an aeroplane flies in the sky, which of the following forces is not experienced by it?\nA air resistance\nB gravitational force from the Earth\nC normal reaction from the ground\nD propelling force from the jet engine",
         "Forces — Types of Forces", 112, 9, (8, 0.05, 0.27), "C"),
        (22, "Which diagram shows an application of the turning effect of a force? (A parachute, B athlete jumping, C hands gripping, D hammer removing a nail)",
         "Forces — Turning Effect (Moments)", 112, 9, (8, 0.27, 0.50), "D"),
        (23, "Two instruments measure the weight and mass of an object on Earth. Spring balance reads 6 N and beam balance requires 6 pieces of 100 g discs to balance. The measurements are then repeated on the Moon (gravitational field strength 1/6 of Earth). Which correctly shows the results expected?\nA spring 1 N, 1 disc\nB spring 1 N, 6 discs\nC spring 6 N, 1 disc\nD spring 6 N, 6 discs",
         "Mass and Weight", 112, 9, (8, 0.50, 0.78), "B"),
        (24, "An elephant weighs 60 000 N. It stands on one foot with an area of 0.1 m^2. What is the pressure exerted on the ground when it stands on four feet?\nA 1 500 Pa\nB 60 000 Pa\nC 150 000 Pa\nD 600 000 Pa",
         "Pressure", 112, 9, (8, 0.78, 0.95), "C"),
        (25, "Which statement about friction is true?\nA It causes energy conversion to heat.\nB A stationary object is free from friction.\nC It only happens when an object moves.\nD It always acts in the same direction as the motion of an object.",
         "Friction", 112, 10, (9, 0.05, 0.30), "A"),
        (26, "Which person has done the most work?\nA A boy weighing 500 N climbing 1 m up a tree.\nB A girl lifting a 10 N book up onto a table 1 m high.\nC A weight-lifter holds a 600 N weight in the same position for 1 minute.\nD A man releasing a 100 N rock which then falls a distance of 10 m into a pit.",
         "Work and Energy", 111, 10, (9, 0.30, 0.62), "D"),
        (27, "A ball is pushed from a table onto the floor and follows the path shown (points P, Q, R, S, T). Which statements are correct?\nI At P, the ball has maximum potential energy and minimum kinetic energy.\nII The ball has more kinetic energy at R than at Q.\nIII The ball has zero kinetic energy at S.\nA I and II only\nB I and III only\nC II and III only\nD I, II and III only",
         "Kinetic and Potential Energy", 111, 10, (9, 0.62, 0.95), "A"),
        (28, "Which object does not possess any form of potential energy?\nA a battery\nB a compressed spring\nC a piece of chocolate\nD a magnet placed on the ground",
         "Forms of Energy", 111, 10, (9, 0.95, 1.0), "D"),
        (29, "The diagram shows how light energy is converted to other forms of energy: X -> light energy -> Y -> electrical energy. Which examples correctly represents X and Y?\nA X cooking, Y solar water heater\nB X steam engine, Y fossil fuels in car\nC X electric light bulb, Y battery\nD X photosynthesis in plants, Y solar toy car",
         "Energy Conversions", 111, 11, (10, 0.05, 0.45), "D"),
        (30, "Wendy is standing against a huge tree trunk and pushing against it in an attempt to make the tree fall to the ground. The tree did not move. Which of the following is true?\nA work done yes, energy used no\nB work done yes, energy used yes\nC work done no, energy used no\nD work done no, energy used yes",
         "Work and Energy", 111, 11, (10, 0.45, 0.80), "D"),
    ]

    for num, text, topic, tid, pg, crop, ans in Q:
        add_q(db, p1.id, exam_dir, 1, num, None, text, 1, topic, pg, crop,
              f"{ans}", "B1", topic_id=tid)

    db.commit()
    print(f"Seeded Bedok South 2017 Science exam id={exam.id}: {len(p1.questions)} MCQs")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
