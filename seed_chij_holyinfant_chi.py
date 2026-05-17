"""Seed Convent of the Holy Infant Jesus EOY 2022 Sec 1 G3 Chinese exam.

Source: Sec 1 G3 华文 EOY 2022 写作试卷 (实用文 电邮 + 作文).
freechinesematerials.com — Convent-of-the-Holy-Infant-Jesus-Sec-1-G3-Chinese-EOY-2022-Paper-1.pdf
Pure CJK text. No LaTeX. subject="Chinese". topic_id in 201-212 range.
"""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/chij_holyinfant_chi.pdf"

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
        School.name == "Convent of the Holy Infant Jesus").first()
    if not school:
        school = School(name="Convent of the Holy Infant Jesus")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(
        Exam.school_id == school.id,
        Exam.year == 2022,
        Exam.subject == "Chinese",
    ).first()
    if existing:
        print(f"CHIJ 2022 Chinese already seeded (id={existing.id}). Re-seeding.")
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
        source_pdf="chij_holyinfant_chi.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)

    p = Paper(exam_id=exam.id, paper_number=2, duration_minutes=70,
              total_marks=60, date=date(2022, 10, 3),
              instructions="本试卷共两部分：一、实用文（任选一题，20分）；二、作文（任选一题，40分）。答案须用规范华文书写。")
    db.add(p)
    db.flush()

    # ── 一、实用文（电邮）──
    add_q(db, p.id, exam_dir, 2, 1, None,
        "根据以下电子邮件的内容，写一个电邮给对方。字数在120字以上。\n"
        "发件人：huiwen@tmail.com  收件人：yuxin@vmail.com  日期：2022年10月3日  主题：鼓励学生多阅读\n"
        "雨欣：\n你好！几个月不见，最近过得好吗？\n"
        "最近，我发现有许多学生在晨读时间不认真，她们很多时候都只是把故事书放在桌上，"
        "眼睛却盯住旁边的平板电脑。这样子根本没法养成真正的阅读习惯。\n"
        "我记得你曾经说过你的学校的晨读计划办得十分成功，学生们都热爱阅读。"
        "你认为有哪些方法可以鼓励学生具有良好的阅读习惯，可以和我分享吗？\n"
        "今天就写到这里，希望早日收到你的回复。\n祝好！\n慧文",
        20, "实用文 — 电邮（鼓励学生多阅读）", 1, (0, 0.05, 0.97),
        "回复电邮须含：称呼「慧文：」、问候语、正文回应（针对慧文提出的"
        "「如何鼓励学生养成良好阅读习惯」给出至少两三个具体建议，例如：设立班级图书角、"
        "举办读书分享会、师长以身作则、订立晨读规则收起电子产品、设奖励制度等，"
        "并结合个人或学校经验说明成效）、结束语、署名「雨欣」。"
        "格式正确、内容切题、语句通顺、字数达标（120字以上）。",
        "格式4分（称呼/问候/结束语/署名）；内容10分（针对问题、建议具体、有条理）；"
        "语言6分（用词准确、语句通顺、无明显病句错别字）。",
        stem="一、实用文（任选一题，字数在120字以上，占20分）。本题为Q1，与Q2择一作答。",
        topic_id=212)

    add_q(db, p.id, exam_dir, 2, 2, None,
        "根据以下电子邮件的内容，写一个电邮给对方。字数在120字以上。\n"
        "发件人：linyuting@kgoomail.com  收件人：xiaoxuan@kgoomail.com  日期：2022年10月3日  主题：储蓄的重要性\n"
        "小萱：\n你好吗？好久没有给你写电邮了。\n"
        "最近，我发现我身边有不少朋友花钱没有节制，也不了解储蓄的重要性，"
        "只要看到喜欢的东西，就不管价钱地乱买。他们吃喝玩乐，花钱如流水。\n"
        "你的身边是不是也有这样的朋友？你觉得我们该怎么样让年轻人懂得储蓄的重要性，"
        "并养成储蓄的好习惯呢？\n好了，我就写到这里，希望早日收到你的回复。\n祝好！\n宇婷",
        20, "实用文 — 电邮（储蓄的重要性）", 2, (1, 0.07, 0.62),
        "回复电邮须含：称呼「宇婷：」、问候语、正文回应（认同储蓄的重要性，"
        "并提出让年轻人养成储蓄习惯的具体方法，例如：制定每月预算、设立储蓄目标、"
        "记账区分需要与想要、家长或学校开设理财教育、延迟满足等，宜结合身边例子）、"
        "结束语、署名「小萱」。格式正确、内容充实、语句通顺、字数达标。",
        "格式4分；内容10分（建议具体可行、有条理）；语言6分（通顺、无明显病句错别字）。",
        stem="一、实用文（任选一题，字数在120字以上，占20分）。本题为Q2，与Q1择一作答。",
        topic_id=212)

    # ── 二、作文 ──
    add_q(db, p.id, exam_dir, 2, 3, None,
        "作文题（任选一题，字数在240字以上，占40分）。题目：《一位热心的邻居》。"
        "请以记叙文形式，通过具体事例描写一位热心邻居的性格特点与所做的事，"
        "并写出你的感受。",
        40, "作文 — 写人记叙文", 2, (1, 0.62, 0.78),
        "评分要点：选材切题（写出邻居「热心」的具体事例，不空泛）；"
        "人物形象鲜明（运用语言、动作、神态等描写）；结构完整（开头、经过、"
        "结尾、点出感受与中心）；语言通顺、用词恰当、标点正确；字数达标（240字以上）。",
        "内容20分（切题、选材、中心）；结构8分；语言12分（用词、句子、错别字标点）。",
        stem="二、作文（任选一题，字数在240字以上，占40分）。本题为Q3，与Q4择一作答。",
        topic_id=212)

    add_q(db, p.id, exam_dir, 2, 4, None,
        "作文题（任选一题，字数在240字以上，占40分）。"
        "你班上有一个不太受欢迎的同学，但是最近发生了一件事，让大家改变了对她的看法。"
        "试写出这件事的经过以及你的感受。",
        40, "作文 — 叙事记叙文", 2, (1, 0.78, 0.95),
        "评分要点：紧扣题意（写出「事件」如何使大家改变看法，前后态度有对比）；"
        "情节具体、有起伏；适当心理与场面描写；点明感受与道理；"
        "结构完整、语言通顺、标点正确；字数达标（240字以上）。",
        "内容20分（切题、情节、转变与中心）；结构8分；语言12分。",
        stem="二、作文（任选一题，字数在240字以上，占40分）。本题为Q4，与Q3择一作答。",
        topic_id=212)

    db.commit()
    print(f"Seeded CHIJ Chinese exam id={exam.id}: {len(p.questions)} questions")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
