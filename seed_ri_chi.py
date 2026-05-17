"""Seed Raffles Institution End-of-Year 2022 Sec 1 Higher Chinese exam.

Source PDF: freechinesematerials.com (RI Sec 1 HCL EOY Paper 1 2022).
This is 试卷一 (实用文 + 作文). No 试卷二 is freely available for Sec 1 华文.
Subject = "Chinese". topic_id in the 201-212 Chinese range. NO LaTeX / no $.
"""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/ri_chi.pdf"

init_db()

SCHOOL_NAME = "Raffles Institution"
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
        print(f"RI {YEAR} Chinese already seeded (id={existing.id}). Re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id, title="End-of-Year Examination 2022 (Higher Chinese)",
        year=YEAR, level="Secondary 1", subject="Chinese",
        source_pdf="ri_chi.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)

    p2 = Paper(exam_id=exam.id, paper_number=2, duration_minutes=120,
               total_marks=80, date=date(2022, 10, 4),
               instructions="高级华文试卷一：实用文（占20分）与作文（占60分）两部分，各任选一题作答。")
    db.add(p2)
    db.flush()

    # 一、实用文（任选一题，字数在220以上，占20分。）
    add_q(
        db, p2.id, exam_dir, 1, 1, None,
        "周杰伦是你的朋友，他发了一封电邮给你，请给周杰伦回一封电邮。"
        "发件人：周杰伦（zhouj1@xyz.com）；收件人：林俊杰（linjj@abc.com）；"
        "日期：2022年10月4日；主题：网上交友。"
        "电邮内容：“俊杰：好久没见面了，十分想念。你近来一切可好？"
        "最近，我通过网上的社交平台认识了一些志趣相投的“网友”，常常会"
        "在线上聊天。但父母认为网上交友很危险，要我和网友保持距离，"
        "这让我很不开心。其实我只不过想多认识一些朋友，希望多和他人"
        "交流。你是否和我父母有相同的看法？在网上交友时，你认为我们"
        "应该要注意些什么？请你分享一些建议。期待你的回复。祝好！杰伦”。",
        20, "实用文：电邮", 2, (1, 0.05, 0.95),
        "回复电邮须包含：称呼（杰伦）、问候语、写信目的；正文针对"
        "“网上交友”表明自己的看法（是否赞同父母的担忧及理由），并提出"
        "网上交友应注意的事项与具体建议（如保护个人资料、不轻信陌生人、"
        "不单独约见网友、提防网络诈骗、理性交友等）；最后写结束语与署名。",
        "内容要点：1 称呼+问候+写信目的；2 表明对网上交友的看法；"
        "3 提出网上交友须注意的事项及建议（至少两点）；4 结束语+署名。",
        stem="一、实用文（任选一题，字数在220以上，占20分。）",
        topic_id=212,
    )

    add_q(
        db, p2.id, exam_dir, 1, 2, None,
        "周杰伦是你的朋友，他发了一封电邮给你，请给周杰伦回一封电邮。"
        "发件人：周杰伦（zhouj1@xyz.com）；收件人：林俊杰（linjj@abc.com）；"
        "日期：2022年10月4日；主题：社交媒体。"
        "电邮内容：“俊杰：好久没见面了，十分想念。你近来一切可好？"
        "最近，我像你一样，在不同的社交媒体账号上，跟网友们分享生活"
        "点滴。我每天会精心挑选内容发布，也收获了不少网友的赞许与评论。"
        "但妈妈却认为我这是不务正业，还要求我关闭所有账号。你认同我"
        "妈妈的做法吗？我记得你刚开始经营社交媒体账号时，父母也十分"
        "不赞同。你当时是如何让他们放心的呢？希望你能跟我分享一些经验。"
        "期待你的回复。祝好！杰伦”。",
        20, "实用文：电邮", 3, (2, 0.05, 0.95),
        "回复电邮须包含：称呼（杰伦）、问候语、写信目的；正文表明对"
        "“经营社交媒体”的看法（是否认同妈妈的做法及理由），并分享自己"
        "当初让父母放心的经验与方法（如合理安排时间、注意内容健康、"
        "兼顾学业、与父母沟通取得信任等）；最后写结束语与署名。",
        "内容要点：1 称呼+问候+写信目的；2 表明对经营社交媒体的看法；"
        "3 分享让父母放心的经验与建议（至少两点）；4 结束语+署名。",
        stem="一、实用文（任选一题，字数在220以上，占20分。）二选一作答。",
        topic_id=212,
    )

    # 二、作文（任选一题，字数在500以上，占60分。）
    add_q(
        db, p2.id, exam_dir, 1, 3, None,
        "你一向独来独往，不太会主动和别人交流。最近发生了一件事，"
        "让你领悟到多和别人相处会让自己变得更快乐。请写出事情的经过"
        "和你的感受。",
        60, "作文：记叙文", 4, (3, 0.10, 0.40),
        "记叙文写作。须交代“自己一向独来独往”的背景，叙述使你转变"
        "想法的那件事的起因、经过与结果，描写人物心理活动；结尾写出"
        "“多和别人相处会让自己变得更快乐”的领悟与感受。字数500字以上，"
        "情节具体、情感真挚、结构完整、语言通顺。",
        "评分要点：内容切题、情节具体、领悟真切；语言通顺、用词准确、"
        "条理清楚；总分按高级华文作文标准评定（占60分）。",
        stem="二、作文（任选一题，字数在500以上，占60分。）",
        topic_id=210,
    )

    add_q(
        db, p2.id, exam_dir, 1, 4, None,
        "你向来说话过于直率，自己也不觉得这是一个大问题。直到有一天，"
        "你因为说话时没有考虑别人的感受，而使团队活动无法顺利进行。"
        "请写出事情的经过和你的感受。",
        60, "作文：记叙文", 4, (3, 0.40, 0.70),
        "记叙文写作。须交代“自己说话过于直率”的背景，叙述因说话不顾"
        "他人感受而使团队活动受影响的事件起因、经过与结果，刻画人物"
        "心理与他人反应；结尾写出自己的反省与感受（如学会换位思考、"
        "说话要顾及他人感受）。字数500字以上，叙事清楚、感悟深刻、"
        "语言通顺。",
        "评分要点：内容切题、情节具体、反省真切；语言通顺、描写生动、"
        "条理清楚；总分按高级华文作文标准评定（占60分）。",
        stem="二、作文（任选一题，字数在500以上，占60分。）二选一作答。",
        topic_id=210,
    )

    db.commit()
    print(f"Seeded RI Chinese exam id={exam.id}: Paper ({len(p2.questions)} questions)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
