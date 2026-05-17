"""Seed Raffles Girls' School (Secondary) End-of-Year 2022 Sec 1 Chinese (G3) exam.

Source PDF: freechinesematerials.com (RGS Sec 1 G3 Chinese EOY Paper 1 2022).
This is 试卷一 (实用文 + 作文). No 试卷二 is freely available for Sec 1 华文 —
all freely-downloadable Sec 1 Chinese school papers are 试卷一 (composition).
Subject = "Chinese". topic_id in the 201-212 Chinese range. NO LaTeX / no $.
"""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/rgs_chi.pdf"

init_db()

SCHOOL_NAME = "Raffles Girls' School (Secondary)"
YEAR = 2022


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

    school = db.query(School).filter(School.name == SCHOOL_NAME).first()
    if not school:
        school = School(name=SCHOOL_NAME)
        db.add(school)
        db.flush()

    existing = (
        db.query(Exam)
        .filter(Exam.school_id == school.id, Exam.year == YEAR,
                Exam.subject == "Chinese")
        .first()
    )
    if existing:
        print(f"RGS {YEAR} Chinese already seeded (id={existing.id}). Re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id, title="End-of-Year Examination 2022", year=YEAR,
        level="Secondary 1", subject="Chinese",
        source_pdf="rgs_chi.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)

    # Single paper per exam; paper_number=2 per the Chinese guide, q1_ image prefix.
    p2 = Paper(exam_id=exam.id, paper_number=2, duration_minutes=120,
               total_marks=80, date=date(2022, 9, 22),
               instructions="本试卷分为实用文和作文两部分，总分为80分。实用文部分占20分，作文部分占60分。两道题任选一题作答。")
    db.add(p2)
    db.flush()

    # 一、实用文（任选一题，字数在150以上，占20分。）
    add_q(
        db, p2.id, exam_dir, 1, 1, None,
        "根据以下电子邮件的内容，写一封回复电邮给对方。"
        "发件人：向梦（yumeng@xyz.com）；收件人：你（anna@abc.com）；"
        "日期：2022年9月18日；主题：向你请教。"
        "电邮内容：“心娜：别来无恙了？升上中学后的第一次年中考试即将"
        "来临，我感到很紧张。父母对我的期望很大，他们希望我在年终考试"
        "都能考到好成绩，这让我觉得很烦恼。我应该如何让父母明白自己"
        "心声的感受？另外，我现在做了很多练习题，成绩却一直停滞不前，"
        "我自己也很担心，你能不能告诉我应该如何在考试中作准备？好了，"
        "就此停笔，希望早日收到你的电邮。祝 生活愉快 向梦”。"
        "请你以“心娜”的身份给向梦回一封电邮。",
        20, "实用文：电邮", 2, (1, 0.05, 0.95),
        "回复电邮须包含：称呼（向梦）、问候语、写信目的（回应她的求助）；"
        "正文针对两个问题作答——（一）如何让父母明白自己面对的压力与"
        "心声（如主动沟通、坦诚表达感受、请父母调整期望）；（二）如何"
        "有效准备考试（如制定温习计划、错题归纳、调整心态、劳逸结合）；"
        "最后写鼓励的话、结束语、祝福语与署名。",
        "内容要点：1 称呼+问候+写信目的；2 就“与父母沟通压力”给建议；"
        "3 就“如何备考”给具体可行建议；4 结束语+署名。格式正确、语言通顺。",
        stem="一、实用文（任选一题，字数在150以上，占20分。）",
        topic_id=212,
    )

    add_q(
        db, p2.id, exam_dir, 1, 2, None,
        "根据以下电子邮件的内容，写一封回复电邮给对方。"
        "发件人：美丽（meiliwang@xyz.com）；收件人：你（beibeizhou@abc.com）；"
        "日期：2022年9月22日；主题：向你请教。"
        "电邮内容：“贝贝：考试考完了吗？你最近过得还好吗？最近，我一直"
        "被一件事困扰，不知道该如何处理。事情是这样的：刚开学时，我和"
        "班上的同学小美关系很亲近，关系也很好。可是放完假后，我们的"
        "关系越来越疏远，我们不再在一起吃饭、一起分享心事。我主动找她"
        "聊天，她也表现得很冷淡。我真的很想和小美重新做回好朋友，拥有"
        "一段深厚的友谊。那我应该怎么做才能够和她回到以前的样子呢？"
        "希望尽快收到你的回复。祝 学习进步 美丽”。"
        "请你以“贝贝”的身份给美丽回一封电邮。",
        20, "实用文：电邮", 3, (2, 0.05, 0.80),
        "回复电邮须包含：称呼（美丽）、问候语、写信目的（回应她的求助）；"
        "正文针对“与同学关系疏远”的问题，分析可能的原因并提出具体、"
        "可行的建议（如主动沟通、坦诚表达、寻找共同话题或活动、给对方"
        "时间、化解误会等）；最后写鼓励的话、结束语、祝福语与署名。",
        "内容要点：1 称呼+问候+写信目的；2 分析关系疏远的原因；"
        "3 提出具体可行的建议（至少两点）；4 鼓励语+结束语+署名。",
        stem="一、实用文（任选一题，字数在150以上，占20分。）二选一作答。",
        topic_id=212,
    )

    # 二、作文（任选一题，字数在300以上，占40分。）
    add_q(
        db, p2.id, exam_dir, 1, 3, None,
        "你无意间发现了同学的一个秘密，连忙把这个秘密告诉了其他人，"
        "这个同学因此受到了伤害。试写出事情的经过以及你从中得到的教训。",
        40, "作文：记叙文", 5, (4, 0.10, 0.40),
        "记叙文写作。须交代事情的起因（如何无意间发现秘密）、经过"
        "（把秘密告诉他人、同学因此受伤害）与结果；描写人物心理与感受；"
        "结尾点明从中得到的教训（如尊重他人隐私、谨言慎行、为人着想）。"
        "字数300字以上，结构完整、详略得当、语言通顺。",
        "评分要点：内容（8分）切题、有具体情节与教训；表达（12分）语句"
        "通顺、用词准确；总分（20分，按比例计入40分）。",
        stem="二、作文（任选一题，字数在300以上，占40分。）",
        topic_id=210,
    )

    add_q(
        db, p2.id, exam_dir, 1, 4, None,
        "有一次你在公共场所中看到一位老婆婆遇到了困难，当时，一个"
        "陌生人主动上前帮忙，这使你深受感动。试写出事情的经过和你的感想。",
        40, "作文：记叙文", 5, (4, 0.40, 0.70),
        "记叙文写作。须交代事情发生的时间、地点与人物，描写老婆婆"
        "遇到的困难、陌生人主动帮忙的经过与细节，刻画自己当时的心理"
        "与“深受感动”的感受；结尾抒发感想（如助人为乐、社会温情、"
        "见贤思齐）。字数300字以上，叙事清楚、情感真挚、语言通顺。",
        "评分要点：内容（8分）切题、情节具体、感想真切；表达（12分）"
        "语句通顺、描写生动；总分（20分，按比例计入40分）。",
        stem="二、作文（任选一题，字数在300以上，占40分。）二选一作答。",
        topic_id=210,
    )

    db.commit()
    print(f"Seeded RGS Chinese exam id={exam.id}: Paper ({len(p2.questions)} questions)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
