"""Seed Queenstown Secondary School EOY 2023 Sec 1 G3 华文 (Chinese) exam.

Source: freechinesematerials.com — Queenstown Sec Sch Sec 1 G3 Chinese EOY 2023.
Single Chinese paper (实用文 + 作文); modelled per CHINESE_SEED_GUIDE.md.
"""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/queenstown_chi.pdf"

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

    school = db.query(School).filter(School.name == "Queenstown Secondary School").first()
    if not school:
        school = School(name="Queenstown Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(
        Exam.school_id == school.id, Exam.year == 2023,
        Exam.subject == "Chinese",
    ).first()
    if existing:
        print(f"Queenstown Chinese 2023 already seeded (id={existing.id}). Re-seeding.")
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
        source_pdf="queenstown_chi.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)

    p2 = Paper(exam_id=exam.id, paper_number=2, duration_minutes=90, total_marks=60,
               date=date(2023, 9, 29), instructions="本试卷包括实用文与作文两组，共占60分。仔细阅读每一组的说明后才作答。不必抄题。")
    db.add(p2)
    db.flush()

    # 一、实用文（共20分）— Q1 私人电邮
    add_q(db, p2.id, exam_dir, 1, 1, None,
        "一、实用文（共20分）\n"
        "请你根据以下电子邮件的内容，写一个回复电邮。电邮中必须要使用举例子、列数字的方式来加以说明。\n\n"
        "发件人：林明义<linmingyi@abc.com>\n"
        "收件人：陈自强<chenzq@def.net>\n"
        "日期：2023年9月29日\n"
        "主题：培养良好的学习习惯\n\n"
        "自强：\n"
        "你好吗？好久没有和你联络了。最近过得如何？\n"
        "今年我升上了中学，不是小学生了。妈妈要我对自己的学习负责任。"
        "我知道你的学习成绩一向良好，你能告诉我，你是如何培养良好的学习习惯？"
        "良好的学习习惯对你有什么好处？\n"
        "我就写到这里，下次再谈。\n"
        "祝好！\n"
        "明义",
        20, "实用文（私人电邮）", 2, (1, 0.07, 0.55),
        "回复电邮，内容要点8分：(1) 问候语＋写信目的＋结束语；"
        "(2) 介绍良好的学习习惯，例如：上课认真听课做笔记、回家先做功课、"
        "做功课时把手机关掉、当天功课当天完成、测验提早准备、早睡早起；"
        "(3) 良好习惯的好处：精神好学习效果佳、不沉迷手机、学业成绩好、"
        "父母骄傲、与父母关系良好。须运用列数字或举例子的方法，至少写两个方法。"
        "语文／格式10分：电邮七大格式（发件人、收件人电邮、日期、回复主题、"
        "称呼＋冒号、祝词、署名），格式错误每个扣1分，扣满4分为限。",
        "内容要点8分（说明方法2分／习惯4分／好处4分）＋语文格式10分；"
        "格式每错扣1分（上限4分）",
        topic_id=212)

    # 二、作文（字数在220字以上，共40分）— Q2 写事记叙文
    add_q(db, p2.id, exam_dir, 1, 2, None,
        "二、作文（字数在220字以上，共40分）\n"
        "你因为不想挨骂而对妈妈撒谎，最后谎言被识破了，你也得到了教训。"
        "试写出这件事情的经过以及你的感受。\n\n"
        "建议运用以下的人物描写手法完成作文：肖像描写、行动描写、"
        "语言描写、心理描写。\n"
        "课文参考词汇：焦急、瞬间、性格、仿佛、疑惑、泪痕、歉意、哀求、"
        "心虚、由衷、沉默寡言、小心翼翼、哑口无言、不堪设想、振振有词。",
        40, "作文（写事记叙文）", 3, (1, 0.55, 0.99),
        "写事记叙文。内容要点：(1) 写出你为了什么事撒谎；"
        "(2) 谎话是怎么被识破的；(3) 谎话被识破后有什么后果；"
        "(4) 你学到了什么教训。须具备记叙文六大要素："
        "时间、地点、人物、事件（起因、经过、结果），紧扣关键词"
        "“撒谎／识破／挨骂”，并运用人物描写手法表达内心感受。",
        "记叙文六要素齐全；扣题“撒谎／识破／挨骂”；"
        "运用人物描写手法；情感真实——按内容、结构、语文综合评分",
        topic_id=210)

    db.commit()
    print(f"Seeded Queenstown Chinese exam id={exam.id}: Paper 2 ({len(p2.questions)} questions)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
