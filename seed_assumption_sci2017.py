"""Seed Assumption English School EOY 2017 Sec 1 Express Science exam (MCQ Booklet A)."""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image, copy_existing_images

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/science/2017-Sec-1-Express-Science-SA2-Assumption-English-School.pdf"
IMAGES_DIR = "/tmp/assumption_sci2017_pages"

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

    school = db.query(School).filter(School.name == "Assumption English School").first()
    if not school:
        school = School(name="Assumption English School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(
        Exam.school_id == school.id, Exam.year == 2017, Exam.subject == "Science"
    ).first()
    if existing:
        print(f"Assumption 2017 Science already seeded (id={existing.id}). Deleting and re-seeding.")
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
        source_pdf="2017-Sec-1-Express-Science-SA2-Assumption-English-School.pdf",
        status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    copy_existing_images(IMAGES_DIR, exam_dir)

    p1 = Paper(exam_id=exam.id, paper_number=1, duration_minutes=120, total_marks=30,
               date=date(2017, 10, 12),
               instructions="Section A: 30 multiple-choice questions. Answer all questions.")
    db.add(p1); db.flush()

    Q = [
        # num, text, topic, topic_id, pdf_page, crop, answer
        (1, "In 2006, a former Russian spy was hospitalized and died three weeks later. Autopsy of his body revealed that he had died due to radioactive poisoning. Which symbol did he most likely ignore during one of his missions?\nA radioactive (trefoil) symbol\nB biohazard symbol\nC skull and crossbones (toxic) symbol\nD cross/irritant symbol",
         "Laboratory Safety Symbols", 101, 2, (1, 0.05, 0.34), "A"),
        (2, "Which part of the Bunsen burner is responsible for controlling the type of flame produced?\nA barrel\nB collar\nC gas tap\nD rubber tubing",
         "The Bunsen Burner", 101, 2, (1, 0.34, 0.50), "B"),
        (3, "Drills operated in mining fields are used to remove rock formation blocking access to the valuable ores beneath. The intense drilling also generates high amount of frictional heat. Which combinations of physical properties are of highest concern when considering the material used to make the drill?\nA hardness, electrical conductivity, boiling point\nB hardness, strength, melting point\nC strength, electrical conductivity, thermal conductivity\nD strength, melting point, transparency",
         "Physical Properties of Materials", 102, 2, (1, 0.50, 0.95), "B"),
        (4, "Mr Ng would like to perform an experiment to demonstrate how different temperatures affect the rate of dissolving sugar in water. He had to leave the hot water aside for 20 minutes while attending to questions from his pupils. Which of following cup should he choose to contain the hot water considering its physical property?\nA styrofoam — heat insulator\nB iron — high melting point\nC copper — heat conductor\nD plastic — low melting point",
         "Physical Properties of Materials", 102, 3, (2, 0.05, 0.50), "A"),
        (5, "Which mixture can be separated using magnetic attraction?\nA a mixture of salt and sesame seed\nB a solution of chlorophyll in water\nC colour pigments found within an ink\nD a mixture containing bits of steel",
         "Separation Techniques", 105, 3, (2, 0.50, 0.66), "D"),
        (6, "Which cell structure prevents a plant cell from bursting when soaked in pure water?\nA cell membrane\nB cell wall\nC chloroplasts\nD nucleus",
         "Plant Cell Structure", 107, 3, (2, 0.66, 0.95), "B"),
        (7, "Given is the complete structure of a red blood cell (cytoplasm rich in haemoglobin, cell membrane, no cell nucleus). Which of the following cellular activity cannot be performed by a red blood cell?\nA allow chemical reaction to take place within it\nB carry oxygen gas\nC control substance entering and leaving the cell\nD repair any damage done to red blood cell effectively",
         "Cells — Specialised Cells", 107, 4, (3, 0.05, 0.46), "D"),
        (8, "Arrange the following body structure in the order of increasing complexity.\nI. red muscle tissue\nII. muscle cells\nIII. circulatory system\nIV. heart\nA I, II, III, IV\nB I, IV, II, III\nC II, I, IV, III\nD II, III, I, IV",
         "Cellular Organisation", 107, 4, (3, 0.46, 0.70), "C"),
        (9, "Which is the correct explanation as to why a plant wilts?\nA Osmosis stops as the root hairs have low concentration of water.\nB The cell wall of the leaves is broken down so the cell sap escapes.\nC The roots are absorbing less water than the leaves are losing water.\nD The roots stop absorbing water and the leaves stop losing water.",
         "Transport in Plants", 110, 4, (3, 0.70, 0.95), "C"),
        (10, "In a plant, water travels through the ____ in a / an ____ direction.\nA phloem; upward\nB phloem; downward\nC xylem; upward\nD xylem; downward",
         "Transport in Plants", 110, 5, (4, 0.05, 0.27), "A"),
        (11, "The diagram shows a specialized cell from a plant (root hair cell). For which function is the cell modified?\nA absorption of water\nB fertilisation\nC transport of food\nD transport of oxygen",
         "Specialised Cells — Root Hair", 107, 5, (4, 0.27, 0.62), "A"),
        (12, "The rate of photosynthesis is dependent on certain conditions. Which of the following would reduce the rate?\nA an increase in atmospheric carbon dioxide content\nB an increase in mass of cloud covering the sky\nC an increase in amount of water\nD an increase in the sunlight level",
         "Photosynthesis", 110, 5, (4, 0.62, 0.95), "B"),
        (13, "Which statement(s) are correct descriptions of the oesophagus?\n1 Digestive enzymes are present in the oesophagus.\n2 Food moves along the oesophagus by peristalsis.\n3 There is some digestion of food in the oesophagus.\n4 There is no digestion of food in the oesophagus.\nA 1 and 2 only\nB 2 and 4 only\nC 1, 2 and 4 only\nD 1, 2 and 3 only",
         "Human Digestive System", 109, 6, (5, 0.05, 0.40), "B"),
        (14, "The diagram shows a section of the human digestive system. In which structure does the absorption of most food molecules occur? (A stomach, B liver, C large intestine, D small intestine)",
         "Human Digestive System — Absorption", 109, 6, (5, 0.40, 0.95), "D"),
        (15, "The diagram shows an experimental set-up to investigate the effect of enzyme X on digestion. Visking tubing contains a mixture of starch solution, glucose solution and enzyme X, suspended in water. After one hour, a few drops of iodine solution were added to the solution in the Visking tubing. The iodine solution remained brown. Which is enzyme X?\nA amylase\nB lipase\nC maltase\nD protease",
         "Digestive Enzymes", 109, 7, (6, 0.05, 0.50), "A"),
        (16, "The diagram shows the simplified human circulatory system (Lungs, Heart, Brain with vessels I, II, III, IV). Which blood vessels carry deoxygenated blood?\nA I and II\nB I and III\nC II and IV\nD III and IV",
         "Human Circulatory System", 110, 7, (6, 0.50, 0.95), "B"),
        (17, "Which statements are true?\nI Plasma helps to carry dissolved substances.\nII Platelets help in the clotting of blood.\nIII White blood cells help to transport oxygen.\nA I and II only\nB I and III only\nC II and III only\nD I, II and III",
         "Blood Components", 110, 8, (7, 0.05, 0.27), "A"),
        (18, "The human circulatory system is made up of ____.\nA arteries, veins and capillaries.\nB heart, blood vessels and blood.\nC heart, lungs and blood vessels.\nD plasma, red blood cells and white blood cells.",
         "Human Circulatory System", 110, 8, (7, 0.27, 0.47), "B"),
        (19, "The graph below shows changes in the thickness of the uterus lining of a lady over a period of 9 weeks. What happened at X (start of each cycle)?\nA fertilisation\nB implantation\nC menstruation\nD ovulation",
         "Menstrual Cycle", 109, 8, (7, 0.47, 0.95), "C"),
        (20, "How can AIDS be spread?\nA sharing of food with an infected person\nB being sneezed on by an infected person\nC sharing of medical needles with an infected person\nD resting on the same bed previously used by an infected person",
         "Sexually Transmitted Infections", 109, 9, (8, 0.05, 0.34), "C"),
        (21, "IVF (In-vitro fertilisation) is a method of fertilisation where the egg is fertilized by the sperm outside the body. The graph shows the percentage success rates of IVF treatments for women of different ages. Which conclusion can be drawn from this data?\nA Women above 45 have a pregnancy rate of 10%.\nB Multiple and single births remained constant throughout a woman's life.\nC The pregnancy success rate falls significantly after the age of 34.\nD The pregnancy success rate is not affected by the age of the woman.",
         "Human Reproduction — IVF", 109, 9, (8, 0.34, 0.95), "C"),
        (22, "Michael was tasked to group closely related animals together. Which pair has the two animals most distant and dissimilar from one another?\nA lion and tiger\nB shark and dolphin\nC snake and monitor lizard\nD rhinoceros and elephant",
         "Classification of Living Things", 107, 10, (9, 0.05, 0.30), "B"),
        (23, "A dichotomous key of some animals is given. Domestic dogs do not have retractable claws and have meat tearing teeth. Which group of animals do they belong to?\nA canidae\nB felix\nC panthera\nD ursidae",
         "Classification — Dichotomous Key", 107, 10, (9, 0.30, 0.95), "A"),
        (24, "Refer to the food chain: grass -> grasshopper -> shrew -> owl. Which is the primary consumer in this food chain?\nA grass\nB grasshopper\nC owl\nD shrew",
         "Food Chains", 107, 11, (10, 0.05, 0.40), "B"),
        (25, "What would happen to the population of owls if the number of shrews decreased greatly (in the chain grass -> grasshopper -> shrew -> owl)?\nA It will decrease in population size.\nB It will expand greatly in population size.\nC It will increase in population size.\nD No change will be observed. It remains the same.",
         "Food Chains — Population", 107, 11, (10, 0.40, 0.66), "A"),
        (26, "A couple of wild boars were recently found in Punggol HDB estates. Which is a possible cause of these incidents?\nA The wild boars were overhunted.\nB The wild boars lost their natural habitat.\nC The wild boars were having an adventure.\nD The wild boars were infected by a type of bacteria.",
         "Habitat and Environment", 107, 11, (10, 0.66, 0.95), "B"),
        (27, "The diagram shows a food web in a wetlands ecosystem. Which organism is both a primary and a secondary consumer?\nA duck\nB frog\nC lizard\nD water bug",
         "Food Webs", 107, 12, (11, 0.05, 0.50), "B"),
        (28, "The diagram shows losses from a rat to the environment (heat energy, carbon dioxide and water in exhaled air, water/salts and urea in urine). What will not be returned to the ecosystem and recycled?\nA carbon dioxide\nB heat energy\nC salts\nD urea",
         "Energy Flow in Ecosystems", 111, 12, (11, 0.50, 0.95), "B"),
        (29, "Read the paragraph: 'The ostrich always moves with a herd of zebras since it has a poor sense of hearing and smell, whereas zebras have very sharp senses. The ostrich has a keen sense of sight, which the zebra lacks. Hence, these two species depend on each other to warn one another of any nearby lurking dangers.' What is the relationship between the ostrich and zebras?\nA commensalism\nB mutualism\nC parasitism\nD predator-prey",
         "Interactions Between Organisms", 107, 13, (12, 0.05, 0.40), "B"),
        (30, "Which statement best describes an ecosystem?\nA A group of organisms of the same species that live in an area.\nB Many groups of organisms of different species that live in an area.\nC Many groups of organisms of different species interacting with each other and the environment in which they all live in.\nD The study of the interactions between many groups of organisms of different species and the environment in which they all live in.",
         "Ecosystems", 107, 13, (12, 0.40, 0.75), "C"),
    ]

    answers = {q[0]: q[6] for q in Q}
    for num, text, topic, tid, pg, crop, ans in Q:
        add_q(db, p1.id, exam_dir, 1, num, None, text, 1, topic, pg, crop,
              f"{ans}", "B1", topic_id=tid)

    db.commit()
    print(f"Seeded Assumption 2017 Science exam id={exam.id}: {len(p1.questions)} MCQs")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
