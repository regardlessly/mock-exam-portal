"""Seed Crescent Girls' School EOY 2021 Sec 1 G3 Chinese exam.

Source: Crescent Girls Sec 1 EOY 2021 写作试卷 (实用文 电邮 + 作文).
freechinesematerials.com — Crescent-Girls-Sec-Sch-Sec-1-EOY-2021-Paper-1-WM.pdf
Pure CJK text. No LaTeX. subject="Chinese". topic_id in 201-212 range.
"""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/crescent_chi.pdf"

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
        School.name == "Crescent Girls' School").first()
    if not school:
        school = School(name="Crescent Girls' School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(
        Exam.school_id == school.id,
        Exam.year == 2021,
        Exam.subject == "Chinese",
    ).first()
    if existing:
        print(f"Crescent 2021 Chinese already seeded (id={existing.id}). Re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id,
        title="年终考试 2021 (End-of-Year Examination 2021)",
        year=2021, level="Secondary 1 G3", subject="Chinese",
        source_pdf="crescent_chi.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)

    p = Paper(exam_id=exam.id, paper_number=2, duration_minutes=70,
              total_marks=60, date=date(2021, 9, 23),
              instructions="本试卷共两部分：一、实用文（任选一题，20分）；二、作文（任选一题，40分）。答案须用规范华文书写。")
    db.add(p)
    db.flush()

    # ── 一、实用文（电邮）──
    add_q(db, p.id, exam_dir, 2, 1, None,
        "根据以下电子邮件的内容，写一个电邮给对方。字数在250字以上。\n"
        "发件人：冯小萱 xiaoxuan@abc.com  收件人：王子希 wangzixi@xyz.com  日期：2021年9月23日  主题：网上交友\n"
        "子希：\n你好！好久没有写电邮给你，希望你一切安好。\n"
        "两个月前，我在网上认识了一名网友，他和我们一样，是一名中学生。"
        "我们俩有许多共同的爱好，经常相约到网上玩游戏，而且也常常聊天聊到深夜。\n"
        "有一次，妈妈发现我到了凌晨一点还没睡，就进来我的房里，"
        "看见我在和网友聊天时训了我一顿。最近，我的成绩退步了，上课还经常打瞌睡，"
        "妈妈说都是因为我在网上和陌生人交朋友才会这样，我因此和妈妈吵架了！\n"
        "子希，难道我不能自在地上网玩游戏、聊天？你是否也认为我不该在网上和"
        "陌生人交朋友？你能和我分享你的看法吗？\n希望早日收到你的电邮。\n祝好！\n小萱",
        20, "实用文 — 电邮（网上交友）", 1, (0, 0.05, 0.97),
        "回复电邮须含：称呼「小萱：」、问候语、正文回应（指出网上交友与熬夜的潜在"
        "风险——身份难辨、影响作息与学业、安全隐患；体谅妈妈的担忧；建议谨慎交友、"
        "节制上网时间、与父母沟通取得信任，宜结合自身经验）、结束语、署名「子希」。"
        "格式正确、内容切题、语句通顺、字数达标（250字以上）。",
        "格式4分（称呼/问候/结束语/署名）；内容10分（回应到位、建议具体有条理）；"
        "语言6分（用词准确、语句通顺、无明显病句错别字）。",
        stem="一、实用文（任选一题，字数在250字以上，占20分）。本题为Q1，与Q2择一作答。",
        topic_id=212)

    add_q(db, p.id, exam_dir, 2, 2, None,
        "根据以下电子邮件的内容，写一个电邮给对方。字数在250字以上。\n"
        "发件人：林凯婷 kaiting@abc.com  收件人：许丽玮 xuliwei@xyz.com  日期：2021年9月23日  主题：经常生病\n"
        "丽玮：\n你好！年终考试要到了，现在很忙吧？\n"
        "我现在也在准备考试，压力特别大。最近不知怎么的，我经常发烧、感冒"
        "而没到学校上课。我平时成绩就不特出，再加上缺席了很多天，"
        "我都跟不上同学们的进度了。虽然班上的同学和老师愿意帮助我，"
        "但我还是很担心自己年终考试没法顺利过关。\n"
        "另外，我也很担心自己的健康。明年就要上中二了，如果健康状况不改善，"
        "我将没法好好学习。丽玮，你一直都是健康宝宝，从不拿病假，而且成绩也很好。"
        "你能和我分享你如何准备考试以及你保持身体健康的方法吗？\n"
        "希望早日收到你的回邮！\n祝好！\n凯婷",
        20, "实用文 — 电邮（经常生病）", 2, (1, 0.05, 0.97),
        "回复电邮须含：称呼「凯婷：」、问候语、正文回应（安慰与鼓励；分享备考方法"
        "——制定温习计划、向师长同学请教补进度、调整心态；分享保持健康的方法"
        "——规律作息、均衡饮食、适量运动、注意卫生，宜结合自身经验）、"
        "结束语、署名「丽玮」。格式正确、内容切题、语句通顺、字数达标。",
        "格式4分；内容10分（建议具体可行、有条理、体贴）；语言6分（通顺、无明显病句错别字）。",
        stem="一、实用文（任选一题，字数在250字以上，占20分）。本题为Q2，与Q1择一作答。",
        topic_id=212)

    # ── 二、作文 ──
    add_q(db, p.id, exam_dir, 2, 3, None,
        "作文题（任选一题，字数在500字以上，占40分）。题目：《我最感激的一个人》。"
        "请以记叙文形式，通过具体事例写出你最感激的人的性格特点与所做的事，"
        "并写出你的感激之情。",
        40, "作文 — 写人记叙文", 3, (2, 0.12, 0.21),
        "评分要点：选材切题（围绕「感激」选取具体事例，不空泛）；"
        "人物形象鲜明（语言、动作、神态、细节描写）；写出感激之情与中心；"
        "结构完整、语言通顺、用词恰当、标点正确；字数达标（500字以上）。",
        "内容20分（切题、选材、中心）；结构8分；语言12分（用词、句子、错别字标点）。",
        stem="二、作文（任选一题，字数在500字以上，占40分）。本题为Q3，与Q4、Q5择一作答。",
        topic_id=212)

    add_q(db, p.id, exam_dir, 2, 4, None,
        "作文题（任选一题，字数在500字以上，占40分）。"
        "你原本开心地与朋友聚会，但却因为发生了一件不愉快的事而使聚会早早结束。"
        "试写出那件事的经过和你的感受。",
        40, "作文 — 叙事记叙文", 3, (2, 0.21, 0.32),
        "评分要点：紧扣题意（写出聚会由开心到「不愉快」而提前结束的事件，"
        "情绪有转折）；情节具体完整、有起伏；适当心理与场面描写；点明感受与中心；"
        "结构完整、语言通顺、标点正确；字数达标（500字以上）。",
        "内容20分（切题、情节、转折与中心）；结构8分；语言12分。",
        stem="二、作文（任选一题，字数在500字以上，占40分）。本题为Q4，与Q3、Q5择一作答。",
        topic_id=212)

    add_q(db, p.id, exam_dir, 2, 5, None,
        "作文题（任选一题，字数在500字以上，占40分）。"
        "你第一次为家人下厨，结果虽然不是很理想，但你从中学到了许多。"
        "试写出这件事的经过以及你的感想。",
        40, "作文 — 叙事记叙文", 3, (2, 0.32, 0.45),
        "评分要点：紧扣题意（写出第一次下厨的经过，结果不理想但有所学习与成长）；"
        "情节具体、有细节（准备、烹饪、出错、反思）；点明感想与中心；"
        "结构完整、语言通顺、标点正确；字数达标（500字以上）。",
        "内容20分（切题、情节、成长与中心）；结构8分；语言12分。",
        stem="二、作文（任选一题，字数在500字以上，占40分）。本题为Q5，与Q3、Q4择一作答。",
        topic_id=212)

    db.commit()
    print(f"Seeded Crescent Chinese exam id={exam.id}: {len(p.questions)} questions")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
