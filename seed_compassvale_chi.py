"""Seed Compassvale Secondary School EOY 2022 Sec 1 G3 Chinese exam.

Source: Compassvale Sec 1 EOY 2022 写作试卷 (电邮 + 作文).
freechinesematerials.com — Compassavle-Sec-1-EOY-2022-Paper-1-online-web.pdf
Pure CJK text. No LaTeX. subject="Chinese". topic_id in 201-212 range.
"""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/compassvale_chi.pdf"

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

    school = db.query(School).filter(
        School.name == "Compassvale Secondary School").first()
    if not school:
        school = School(name="Compassvale Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(
        Exam.school_id == school.id,
        Exam.year == 2022,
        Exam.subject == "Chinese",
    ).first()
    if existing:
        print(f"Compassvale 2022 Chinese already seeded (id={existing.id}). Re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id,
        title="年终考试 2022 (End-of-Year Examination 2022)",
        year=2022, level="Secondary 1 G3", subject="Chinese",
        source_pdf="compassvale_chi.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)

    p = Paper(exam_id=exam.id, paper_number=2, duration_minutes=70,
              total_marks=90, date=date(2022, 10, 4),
              instructions="本试卷共两部分：一、电子邮件（任选一题，20分）；二、作文（任选一题，70分）。答案须用规范华文书写。")
    db.add(p)
    db.flush()

    # ── 一、电子邮件 ──
    add_q(db, p.id, exam_dir, 2, 1, None,
        "根据以下电子邮件的内容，写一封电邮给对方。字数在120字以上。\n"
        "发件人：孙志明 zmsoon@abc.net  收件人：陈伟杰 chenwj@xyz.com  日期：2022年10月4日  主题：有意义的假期生活\n"
        "伟杰：\n你好！好久没有给你写电邮了。你最近还好吗？\n"
        "年底假期快要来临了，我好兴奋哦！我又可以过着没日没夜玩电脑和手机的日子了，"
        "完全不吃、不休息，我也愿意。爸爸妈妈却总是责备我。"
        "你觉得这样做有乐趣吗？你有其他度过假期的好介绍吗？\n"
        "希望能早日收到你的电邮。\n祝好！\n志明",
        20, "实用文 — 电邮（有意义的假期生活）", 1, (0, 0.05, 0.97),
        "回复电邮须含：称呼「志明：」、问候语、正文回应（指出整天玩电脑手机、"
        "不吃不休的坏处，劝告志明合理安排假期，并建议有意义的假期活动，例如：阅读、"
        "运动、学习新技能、做义工、陪伴家人、安排作息等，宜结合个人经验）、"
        "结束语、署名「伟杰」。格式正确、内容切题、语句通顺、字数达标。",
        "格式4分（称呼/问候/结束语/署名）；内容10分（回应到位、建议具体有条理）；"
        "语言6分（用词准确、语句通顺、无明显病句错别字）。",
        stem="一、电子邮件（任选一题，字数在120字以上，占20分）。本题为Q1，与Q2择一作答。",
        topic_id=212)

    add_q(db, p.id, exam_dir, 2, 2, None,
        "根据以下电子邮件的内容，写一封电邮给对方。字数在120字以上。\n"
        "发件人：孙志明 zmsoon@abc.net  收件人：陈伟杰 chenwj@xyz.com  日期：2022年10月4日  主题：父母过度保护\n"
        "伟杰：\n你好！好久没有给你写电邮了。你最近还好吗？\n"
        "我最近很烦恼，我发觉爸爸妈妈总是把我当作小孩一样，什么都帮我决定，"
        "不给我自由。就因为这样，我们总是吵架。\n"
        "你的父母也会这样吗？你觉得他们这样做好吗？我应该怎么做才能让他们知道"
        "我长大了，需要自己的空间呢？\n希望你能早日回复我。\n祝好！\n志明",
        20, "实用文 — 电邮（父母过度保护）", 2, (1, 0.05, 0.97),
        "回复电邮须含：称呼「志明：」、问候语、正文回应（体谅父母的关心，"
        "同时给出与父母沟通、用行动证明自己已长大、争取适当自主空间的具体建议，"
        "宜结合自身经验）、结束语、署名「伟杰」。"
        "格式正确、内容切题、语句通顺、字数达标。",
        "格式4分；内容10分（建议具体、有条理、得体）；语言6分（通顺、无明显病句错别字）。",
        stem="一、电子邮件（任选一题，字数在120字以上，占20分）。本题为Q2，与Q1择一作答。",
        topic_id=212)

    # ── 二、作文 ──
    add_q(db, p.id, exam_dir, 2, 3, None,
        "作文题（任选一题，字数在150字以上，占70分）。"
        "曾经有一个人，在你生活中默默付出，却不求回报，让你非常感恩。"
        "试写出这个人的性格特点，并说出他/她的付出，对你有什么意义。",
        70, "作文 — 写人记叙文", 3, (2, 0.07, 0.32),
        "评分要点：选材切题（写出「默默付出、不求回报」的具体事例）；"
        "人物性格鲜明（语言、动作、神态等描写）；写出付出对「我」的意义与感恩之情；"
        "结构完整、语言通顺、用词恰当、标点正确；字数达标（150字以上）。",
        "内容（切题、选材、中心）、结构、语言三方面综合评分，满分70分。",
        stem="二、作文（任选一题，字数在150字以上，占70分）。本题为Q3，与Q4、Q5择一作答。",
        topic_id=212)

    add_q(db, p.id, exam_dir, 2, 4, None,
        "作文题（任选一题，字数在150字以上，占70分）。"
        "最近发生了一件事，让你明白了我们必须从错误中学习的道理。"
        "试写出事情的经过和你的内心感想。",
        70, "作文 — 叙事记叙文", 3, (2, 0.32, 0.46),
        "评分要点：紧扣题意（事件能体现「从错误中学习」的道理）；"
        "情节具体完整、有起伏；适当心理描写；点明感想与中心；"
        "结构完整、语言通顺、标点正确；字数达标（150字以上）。",
        "内容、结构、语言三方面综合评分，满分70分。",
        stem="二、作文（任选一题，字数在150字以上，占70分）。本题为Q4，与Q3、Q5择一作答。",
        topic_id=212)

    add_q(db, p.id, exam_dir, 2, 5, None,
        "作文题（任选一题，字数在150字以上，占70分）。"
        "你向来不喜欢华文，也不常用华语交谈。但最近发生的一件事，"
        "改变了你的想法，让你发现到华文华语的重要性。"
        "试把这件事的经过及你的感想写出来。",
        70, "作文 — 叙事记叙文", 3, (2, 0.46, 0.66),
        "评分要点：紧扣题意（事件能体现态度转变与华文华语的重要性，前后有对比）；"
        "情节具体、有起伏；适当心理描写；点明感想与中心；"
        "结构完整、语言通顺、标点正确；字数达标（150字以上）。",
        "内容、结构、语言三方面综合评分，满分70分。",
        stem="二、作文（任选一题，字数在150字以上，占70分）。本题为Q5，与Q3、Q4择一作答。",
        topic_id=212)

    db.commit()
    print(f"Seeded Compassvale Chinese exam id={exam.id}: {len(p.questions)} questions")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
