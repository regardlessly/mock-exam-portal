"""Seed Bendemeer Secondary School SA2 2022 Sec 1NA G2 华文 (Chinese) exam.

Source: freechinesematerials.com — Bendemeer Sec Sch Sec 1N G2 SA2 Paper 1 2022.
Single Chinese paper (实用文 + 作文); modelled per CHINESE_SEED_GUIDE.md.
"""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/bendemeer_chi.pdf"

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

    school = db.query(School).filter(School.name == "Bendemeer Secondary School").first()
    if not school:
        school = School(name="Bendemeer Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(
        Exam.school_id == school.id, Exam.year == 2022,
        Exam.subject == "Chinese",
    ).first()
    if existing:
        print(f"Bendemeer Chinese 2022 already seeded (id={existing.id}). Re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id, title="Semestral Assessment 2 2022 (华文)", year=2022,
        level="Secondary 1 Normal (Academic)", subject="Chinese",
        source_pdf="bendemeer_chi.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)

    p2 = Paper(exam_id=exam.id, paper_number=2, duration_minutes=90, total_marks=60,
               date=date(2022, 10, 3), instructions="一、实用文（任选一题，字数在120以上，占20分）。二、作文（任选一题，字数在180以上，占40分）。")
    db.add(p2)
    db.flush()

    # 一、实用文 Q1 — 回复电邮（食堂脏乱）
    add_q(db, p2.id, exam_dir, 1, 1, None,
        "一、实用文（任选一题，字数在120以上，占20分）\n"
        "试根据以下电子邮件的内容，写一个回复电邮。\n\n"
        "发件人：linmeiyi@kgoomail.com\n"
        "收件人：zhangdawei@kgoomail.com\n"
        "日期：2022年10月3日\n"
        "主题：食堂脏乱\n\n"
        "大伟：\n"
        "你好！好久没给你写电邮了，一切都顺利吗？\n"
        "最近，老师都说学校食堂的桌面和地板非常脏乱。一些同学吃完饭后，"
        "没有归还碗盘和杯子，地板上也有食物残渣和饮料罐，非常肮脏。"
        "这使清洁工人需要花更多时间清理干净。\n"
        "你对这些学生的行为有什么看法？听说你们学校的食堂总是很干净，"
        "你可以和我分享你们是如何保持食堂的清洁卫生吗？请你给我一些建议。\n"
        "希望早日收到你的电邮。\n"
        "祝好！\n"
        "美仪",
        20, "实用文（回复电邮）", 1, (0, 0.085, 0.86),
        "回复电邮。内容要点：(1) 对乱丢垃圾、不归还碗盘的行为表达看法"
        "（缺乏公德心、增加清洁工负担、影响卫生）；"
        "(2) 分享并建议如何保持食堂清洁（如：用餐后归还碗盘、"
        "自带餐具、不乱丢垃圾、设值日生、张贴提醒标语、举办卫生活动等）。"
        "须含电邮七大格式，字数120字以上。",
        "内容要点＋语文格式综合评分；电邮格式齐全；字数达标",
        topic_id=212)

    # 一、实用文 Q2 — 回复电邮（教师节庆祝活动）
    add_q(db, p2.id, exam_dir, 1, 2, None,
        "一、实用文（任选一题）\n"
        "试根据以下电子邮件的内容，写一个回复电邮。\n\n"
        "发件人：linmeiyi@kgoomail.com\n"
        "收件人：zhangdawei@kgoomail.com\n"
        "日期：2022年10月3日\n"
        "主题：教师节庆祝活动\n\n"
        "大伟：\n"
        "你好！好久没给你写电邮了，一切都顺利吗？\n"
        "我的学校在九月一日那天举办教师节庆祝活动。那天，"
        "全校充满了欢乐的气氛。\n"
        "你的学校是怎样庆祝教师节的呢？你最喜欢哪一个节目？为什么？"
        "请你和我分享你的看法。\n"
        "希望早日收到你的电邮。\n"
        "祝好！\n"
        "美仪",
        20, "实用文（回复电邮）", 2, (1, 0.15, 0.74),
        "回复电邮。内容要点：(1) 说明你的学校是怎样庆祝教师节的"
        "（如：颁奖、表演、班级布置、送贺卡等）；"
        "(2) 说出你最喜欢哪一个节目及理由。"
        "须含电邮七大格式，字数120字以上。",
        "内容要点＋语文格式综合评分；电邮格式齐全；字数达标",
        topic_id=212)

    # 二、作文 Q3 — 一个令我敬佩的人（写人）
    add_q(db, p2.id, exam_dir, 1, 3, None,
        "二、作文（任选一题，字数在180以上，占40分）\n"
        "一个令我敬佩的人",
        40, "作文（写人记叙文）", 3, (2, 0.085, 0.21),
        "写人记叙文。须通过具体事例突出人物令人敬佩的品质或事迹，"
        "运用人物描写手法（外貌、语言、动作、心理），并表达敬佩之情。"
        "结构完整，中心明确。",
        "选材切题；人物刻画具体；情感真挚——按内容、结构、语文综合评分",
        topic_id=210)

    # 二、作文 Q4 — 我伤透了父母的心（写事）
    add_q(db, p2.id, exam_dir, 1, 4, None,
        "二、作文（任选一题）\n"
        "我伤透了父母的心",
        40, "作文（写事记叙文）", 3, (2, 0.21, 0.28),
        "写事记叙文。须写出令父母伤心的事情起因、经过、结果，"
        "并写出自己的反省与感受，情感真实，叙述清楚。",
        "记叙文六要素齐全；扣题“伤透父母的心”；情感真实——综合评分",
        topic_id=210)

    # 二、作文 Q5 — 续写（下课的铃声响了……）
    add_q(db, p2.id, exam_dir, 1, 5, None,
        "二、作文（任选一题）\n"
        "下课的铃声响了。同学们争先恐后地跑到食堂去吃饭……\n"
        "试以上述的文字做开头，完成这篇文章。",
        40, "作文（命题续写）", 3, (2, 0.28, 0.42),
        "命题续写记叙文。须承接所给开头，合理展开情节，"
        "写出完整的故事（起因、经过、结果）并表达感受，"
        "首尾连贯，中心明确。",
        "衔接自然；情节合理完整；语言通顺——综合评分",
        topic_id=210)

    db.commit()
    print(f"Seeded Bendemeer Chinese exam id={exam.id}: Paper 2 ({len(p2.questions)} questions)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
