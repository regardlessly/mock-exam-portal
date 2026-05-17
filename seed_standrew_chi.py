"""Seed St Andrew's Secondary School EOY 2023 Sec 1 G3 华文 (Chinese) exam.

Source: freechinesematerials.com — St Andrew's Sec Sch Sec 1 G3 Chinese EOY 2023.
Single Chinese paper (实用文 + 作文); modelled per CHINESE_SEED_GUIDE.md.
"""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/standrew_chi.pdf"

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

    school = db.query(School).filter(School.name == "St Andrew's Secondary School").first()
    if not school:
        school = School(name="St Andrew's Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(
        Exam.school_id == school.id, Exam.year == 2023,
        Exam.subject == "Chinese",
    ).first()
    if existing:
        print(f"St Andrew's Chinese 2023 already seeded (id={existing.id}). Re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id, title="End-of-Year Examination 2023 (华文)", year=2023,
        level="Secondary 1 Express", subject="Chinese",
        source_pdf="standrew_chi.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)

    p2 = Paper(exam_id=exam.id, paper_number=2, duration_minutes=90, total_marks=60,
               date=date(2023, 9, 25), instructions="一、实用文（任选一题，字数在120以上，占20分）。二、作文（任选一题，字数在150字以上，占40分）。")
    db.add(p2)
    db.flush()

    # 一、实用文 Q1 — 电邮（庆祝教师节）
    add_q(db, p2.id, exam_dir, 1, 1, None,
        "一、实用文（任选一题，字数在120以上，占20分）\n"
        "根据以下电子邮件的内容，写一封电邮给对方。\n\n"
        "发件人：李志刚<zhigang@kgoomail.com>\n"
        "收件人：张国平<guoping@kgoomail.com>\n"
        "日期：2023年9月25日\n"
        "主题：庆祝教师节\n\n"
        "国平：\n"
        "你好！好久不见！\n"
        "时间过得真快，一转眼我们离开小学已经快一年了。九月假期前，"
        "我的学校热热闹闹地庆祝了教师节，同学们组织了很多活动。"
        "听到歌声的那一刻，我很想念我的小学老师们。\n"
        "你能不能告诉我，你的学校是怎么庆祝教师节的？我打算明年教师节"
        "去感谢我的小学老师，你觉得我该怎么做才能表达我对小学老师的感谢呢？\n"
        "希望早日收到你的回复。\n"
        "祝好！\n"
        "志刚",
        20, "实用文（电邮）", 2, (1, 0.05, 0.98),
        "回复电邮。内容要点：(1) 说明你的学校是怎么庆祝教师节的（活动、节目）；"
        "(2) 建议志刚明年可以怎么做来表达对小学老师的感谢"
        "（如：回校探望、写感谢卡、送小礼物、表演节目等）。"
        "格式须含电邮七要素（发件人、收件人、日期、主题、称呼、祝词、署名），"
        "字数在120字以上。",
        "内容要点＋语文格式综合评分；电邮格式齐全；字数达标",
        topic_id=212)

    # 一、实用文 Q2 — 电邮（保持健康）
    add_q(db, p2.id, exam_dir, 1, 2, None,
        "一、实用文（任选一题）\n"
        "根据以下电子邮件的内容，写一封电邮给对方。\n\n"
        "发件人：王明达<zhigang@kgoomail.com>\n"
        "收件人：孙新民<guoping@kgoomail.com>\n"
        "日期：2023年9月25日\n"
        "主题：保持健康\n\n"
        "新民：\n"
        "你好！好久不见！\n"
        "今年我上了中学，可能是因为功课多，没时间运动，也可能是因为"
        "空气中有很多病毒，我今年经常生病。爸爸妈妈让我多多去运动，"
        "可是，我有很多功课要做，还有课外活动，还得参加补习班。"
        "哪里有时间运动呢？\n"
        "你觉得我们应该运动吗？为什么？我该怎么做才能确保自己不生病呢？"
        "希望早日收到你的回复。\n"
        "祝好！\n"
        "明达",
        20, "实用文（电邮）", 3, (2, 0.0, 0.60),
        "回复电邮。内容要点：(1) 说明应该运动及理由（增强体质、减少生病、"
        "舒缓压力等）；(2) 给明达建议如何在忙碌中保持健康及不生病"
        "（如：合理安排时间、利用零碎时间运动、均衡饮食、充足睡眠、"
        "勤洗手戴口罩等）。电邮格式齐全，字数120字以上。",
        "内容要点＋语文格式综合评分；电邮格式齐全；字数达标",
        topic_id=212)

    # 二、作文 Q3 — 克服困难
    add_q(db, p2.id, exam_dir, 1, 3, None,
        "二、作文（任选一题，字数在150字以上，占40分）\n"
        "进入中学后，你遇到了一个困难，经过努力，你克服了困难。"
        "请写出这件事的起因、经过、结果，并写出你的感受。",
        40, "作文（写事记叙文）", 3, (2, 0.648, 0.755),
        "写事记叙文。须写出困难的起因、经过、结果，并表达克服困难后的"
        "真实感受与体会。结构完整，叙述清楚。",
        "记叙文六要素齐全；扣题“困难／克服”；情感真实——综合评分",
        topic_id=210)

    # 二、作文 Q4 — 做好事受表扬
    add_q(db, p2.id, exam_dir, 1, 4, None,
        "二、作文（任选一题）\n"
        "在放学回家的路上，你做了一件好事，得到了家长的表扬。"
        "请写出这件事情的起因、经过、结果，并写出你的感受。",
        40, "作文（写事记叙文）", 3, (2, 0.755, 0.828),
        "写事记叙文。须写出做好事的起因、经过、结果，"
        "以及得到家长表扬后的感受。结构完整，叙述清楚。",
        "记叙文六要素齐全；扣题“好事／表扬”；情感真实——综合评分",
        topic_id=210)

    # 二、作文 Q5 — 友情修复
    add_q(db, p2.id, exam_dir, 1, 5, None,
        "二、作文（任选一题）\n"
        "最近发生的一件事影响了你和好友之间的友情，在老师的帮助下，"
        "你们最终和好了。请写出这件事的起因、经过和结果，"
        "并说说你的感受。",
        40, "作文（写事记叙文）", 3, (2, 0.828, 0.905),
        "写事记叙文。须写出影响友情的事件起因、经过、结果，"
        "以及在老师帮助下和好的过程与感受。结构完整，情感真挚。",
        "记叙文六要素齐全；扣题“友情／和好／老师帮助”；情感真实——综合评分",
        topic_id=210)

    db.commit()
    print(f"Seeded St Andrew's Chinese exam id={exam.id}: Paper 2 ({len(p2.questions)} questions)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
