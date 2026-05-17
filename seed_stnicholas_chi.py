"""Seed CHIJ St. Nicholas Girls' School (IP) End-of-Year 2025 Sec 1 Higher
Chinese exam.

Source PDF: freechinesematerials.com
(CHIJ St Nicholas Girls IP Sec 1 HCL EOY 2025 Paper 1).
This is 试卷一 (实用文 + 作文). No 试卷二 is freely available for Sec 1 华文.
Subject = "Chinese". topic_id in the 201-212 Chinese range. NO LaTeX / no $.
"""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/stnicholas_chi.pdf"

init_db()

SCHOOL_NAME = "CHIJ St. Nicholas Girls' School"
YEAR = 2025


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
        print(f"St Nicholas {YEAR} Chinese already seeded (id={existing.id}). Re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id,
        title="End-of-Year Examination 2025 (Higher Chinese, IP)",
        year=YEAR, level="Secondary 1", subject="Chinese",
        source_pdf="stnicholas_chi.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)

    p2 = Paper(exam_id=exam.id, paper_number=2, duration_minutes=120,
               total_marks=80, date=date(2025, 9, 17),
               instructions="高级华文试卷一：实用文（占20分）与作文（占60分）两部分，各任选一题作答。")
    db.add(p2)
    db.flush()

    # 一、实用文（任选一题，字数在220以上，占20分。）
    add_q(
        db, p2.id, exam_dir, 1, 1, None,
        "华珍和佳佳是小学同学，现在就读不同的中学。最近，华珍在进行"
        "小组专题作业时遇到了一些问题，她写电邮向佳佳请教。假设你是"
        "佳佳，试写一则电邮回复华珍。"
        "发件人：华珍（huazhen@kgoomail.com）；收件人：佳佳"
        "（enjia@kgoomail.com）；日期：2025年9月17日；主题：同学不合作。"
        "电邮内容：“佳佳：你好！好久没给你写电邮了，别来无恙？最近，"
        "老师给我们布置了一项小组专题作业，要求我们四人一组合作完成。"
        "但是我们组的一位同学却始终不配合，我们留校讨论时，他常常无故"
        "缺席。交代他的任务也不是没做，就是迟交，即使做了，质量也很差。"
        "我想直接向老师汇报情况，让老师处罚他。可是我们组的另两位组员"
        "觉得应该要再给他一次机会。你认为我该直接告诉老师吗？如果他还是"
        "没有改变态度，我们应该怎么做呢？希望早日收到你的回邮。祝好！"
        "华珍”。",
        20, "实用文：电邮", 2, (0, 0.05, 0.97),
        "回复电邮须包含：称呼（华珍）、问候语、写信目的；正文针对"
        "“是否该直接告诉老师”表明看法并说明理由，并就“组员仍不改变"
        "态度时该怎么做”提出具体可行的建议（如先与该同学坦诚沟通、"
        "明确分工与期限、组内协商、必要时再请老师介入等）；最后写"
        "结束语、祝福语与署名。",
        "内容要点：1 称呼+问候+写信目的；2 对“是否告诉老师”表明看法及理由；"
        "3 提出后续应对建议（至少两点）；4 结束语+署名。格式正确、语言通顺。",
        stem="一、实用文（任选一题，字数在220以上，占20分。）",
        topic_id=212,
    )

    add_q(
        db, p2.id, exam_dir, 1, 2, None,
        "宇虹和明慧是同学。最近，宇虹的妹妹沉迷网络，宇虹很想帮助她，"
        "所以写了则电邮向明慧请求帮助。假设你是明慧，试写一则电邮回复"
        "宇虹。"
        "发件人：宇虹（yuhong@kgoomail.com）；收件人：明慧"
        "（minghui@kgoomail.com）；日期：2025年9月17日；主题：沉迷社交媒体。"
        "电邮内容：“明慧：你好！好久没联系了，你还好吗？最近，我发现"
        "我的妹妹每天花超过三个小时浏览脸书、抖音等社交媒体，有时甚至"
        "看到半夜，导致越来越没精神。不仅如此，她也经常在社交媒体发布"
        "动态，过后就一直留意别人的点赞和评论。有时候甚至会因为别人的"
        "评论太少或没有人点赞，就不开心，有一次还为此大哭了一场，让"
        "家人都很担心。我想找她聊一聊，可是我又担心性格敏感的妹妹不"
        "高兴，我该不该跟她聊呢？另外，你觉得我应该怎么做，才可以让她"
        "学会正确使用社交媒体呢？希望早日收到你的回邮。祝好！宇虹”。",
        20, "实用文：电邮", 3, (1, 0.05, 0.95),
        "回复电邮须包含：称呼（宇虹）、问候语、写信目的；正文针对"
        "“该不该跟敏感的妹妹谈”表明看法并说明沟通时的注意事项，并就"
        "“如何帮助妹妹正确使用社交媒体”提出具体可行的建议（如选择合适"
        "时机温和沟通、约定使用时间、培养其他兴趣、家人陪伴引导、"
        "树立正确的网络观念等）；最后写结束语、祝福语与署名。",
        "内容要点：1 称呼+问候+写信目的；2 对“是否与妹妹沟通”表明看法及"
        "沟通方式；3 提出帮助妹妹正确用网的建议（至少两点）；4 结束语+署名。",
        stem="一、实用文（任选一题，字数在220以上，占20分。）二选一作答。",
        topic_id=212,
    )

    # 二、作文（任选一题，字数在350以上，占60分。）
    add_q(
        db, p2.id, exam_dir, 1, 3, None,
        "最近，你的朋友遇到了困难，正打算放弃。你决定伸出援手，陪她"
        "一起克服这个困难。试写出这件事情的经过，并谈谈你的感受。",
        60, "作文：记叙文", 4, (2, 0.10, 0.33),
        "记叙文写作。须交代朋友遇到的困难及打算放弃的背景，叙述你"
        "伸出援手、陪她一起克服困难的经过与结果，描写人物心理与"
        "互动细节；结尾谈谈自己的感受与体会（如友情的可贵、坚持的"
        "意义、助人的快乐）。字数350字以上，情节具体、情感真挚、"
        "结构完整、语言通顺。",
        "评分要点：内容切题、情节具体、感受真切；语言通顺、用词准确、"
        "条理清楚；总分按高级华文作文标准评定（占60分）。",
        stem="二、作文（任选一题，字数在350以上，占60分。）",
        topic_id=210,
    )

    add_q(
        db, p2.id, exam_dir, 1, 4, None,
        "最近，你和同学参加了学校组织的义工活动。起初你不太情愿，但"
        "在活动中，你却有了意外的收获。试写出这件事情的经过，并谈谈"
        "你的感受。",
        60, "作文：记叙文", 4, (2, 0.33, 0.52),
        "记叙文写作。须交代参加义工活动的背景及自己起初不情愿的心态，"
        "叙述活动的经过以及“意外的收获”是什么，刻画心态的转变；结尾"
        "谈谈自己的感受与体会（如服务他人的意义、付出与收获、自我"
        "成长）。字数350字以上，叙事清楚、感悟真切、语言通顺。",
        "评分要点：内容切题、情节具体、收获与感受真切；语言通顺、"
        "描写生动、条理清楚；总分按高级华文作文标准评定（占60分）。",
        stem="二、作文（任选一题，字数在350以上，占60分。）二选一作答。",
        topic_id=210,
    )

    add_q(
        db, p2.id, exam_dir, 1, 5, None,
        "最近，你因为一次失败而心情失落，甚至怀疑自己。后来，经过"
        "一件事情，你逐渐恢复自信，并明白遇到挫折要学会积极面对。"
        "试写出这件事情的经过，并谈谈你的感受。",
        60, "作文：记叙文", 4, (2, 0.52, 0.74),
        "记叙文写作。须交代失败的经历及由此带来的失落与自我怀疑，"
        "叙述使你逐渐恢复自信的那件事情的经过，描写心理变化；结尾"
        "点明“遇到挫折要学会积极面对”的领悟与感受。字数350字以上，"
        "情节具体、感悟深刻、结构完整、语言通顺。",
        "评分要点：内容切题、情节具体、领悟真切；语言通顺、用词准确、"
        "条理清楚；总分按高级华文作文标准评定（占60分）。",
        stem="二、作文（任选一题，字数在350以上，占60分。）三选一作答。",
        topic_id=210,
    )

    db.commit()
    print(f"Seeded St Nicholas Chinese exam id={exam.id}: Paper ({len(p2.questions)} questions)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
