"""Seed Xinmin Secondary School 2022 WA1 Sec 1 Normal Chinese (华文) Paper 2."""

import os
from datetime import date

from models import SessionLocal, School, Exam, Paper, Question, Answer, init_db
from processor import crop_question_image

PDF_PATH = "/Users/timmy/Downloads/sec1-papers/xinmin_chi.pdf"

init_db()

# Reading comprehension passage (用于 Q18-Q22 的 stem)
PASSAGE = (
    "①一位老人有三个儿子。老大是个本领很强的水手。他坚强、勇敢、有责任心又有冒险精神。"
    "这个儿子大胆和勇猛的精神，就像一头虎虎生威的狮子。可惜的是，他在冬天一个夜黑风高的"
    "晚上出意外，结果不幸在大海中淹死。\n"
    "②老人的二儿子是一个力气很大的建筑工人。父亲很疼爱他，尤其是在大儿子死了之后，更"
    "认为这是上天给他最大的补偿。可是两年后，二儿子在工地发生意外，不幸被石块压死了。\n"
    "③老人的两个儿子都去世后，他非常伤心。所幸他还有一个小儿子，这是他唯一的安慰。于是，"
    "老人改变了主意，决心不让小儿子成为一个出众的人物。因为他实在不能再忍受失去儿子的痛苦。"
    "他叹着气说：“唉！与其让他因为有才能而死，我宁愿他是一个毫无本事、没有出息的人啊！”"
    "从此，老人亲自教育这个小儿子。\n"
    "④这个小儿子，也真听话，果然没有让父亲失望。10 年后，他长大了，成为一个既胆小又自私，"
    "而且好吃懒做，整天呆在家里的没有用的人。到了这个时候，老人感受到一种从来没有过的悲哀。"
    "他一边后悔自己所犯的错误，一边又怜惜自己无用的小儿子。"
)


def add_q(db, paper_id, exam_dir, num, part, text, marks, topic, topic_id,
          pdf_page, crop_region, answer_text, mark_scheme, stem=None):
    part_suffix = part if part else ""
    img_name = f"q1_{num}{part_suffix}.png"
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

    school = db.query(School).filter(School.name == "Xinmin Secondary School").first()
    if not school:
        school = School(name="Xinmin Secondary School")
        db.add(school)
        db.flush()

    existing = db.query(Exam).filter(
        Exam.school_id == school.id, Exam.year == 2022,
        Exam.subject == "Chinese",
    ).first()
    if existing:
        print(f"Xinmin Chinese 2022 already seeded (id={existing.id}). Re-seeding.")
        for p in existing.papers:
            for q in p.questions:
                db.query(Answer).filter(Answer.question_id == q.id).delete()
            db.query(Question).filter(Question.paper_id == p.id).delete()
        db.query(Paper).filter(Paper.exam_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    exam = Exam(
        school_id=school.id,
        title="Weighted Assessment 1 2022 (计分测验一)", year=2022,
        level="Secondary 1 Normal", subject="Chinese",
        source_pdf="xinmin_chi.pdf", status="ready",
    )
    db.add(exam)
    db.flush()

    exam_dir = os.path.join(os.path.dirname(__file__), "uploads", str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)

    # 试卷二 (Paper 2): 课文词语考查 + 理解问答, 共40分, 50分钟
    p2 = Paper(exam_id=exam.id, paper_number=2, duration_minutes=50, total_marks=40,
               date=date(2022, 2, 10), instructions="本试卷共有两项试题：（一）课文词语考查、（二）理解问答，共占40分。")
    db.add(p2); db.flush()

    # ───────── 一、课文词语考查 (22分) ─────────
    # (A) 词语搭配 Q1-Q6 — page 2 (idx 1)
    add_q(db, p2.id, exam_dir, 1, None,
        "（A）词语搭配：将左右两栏适合搭配的词语连接起来。"
        "左栏：抵挡、冤枉、人缘、设施、推荐、引起；"
        "右栏：极好、齐全、攻势、好人、怀疑、工作。"
        "Q1 抵挡___　Q2 冤枉___　Q3 人缘___　Q4 设施___　Q5 推荐___　Q6 引起___",
        6, "词语搭配", 203, 2, (1, 0.05, 0.46),
        "Q1 抵挡攻势；Q2 冤枉好人；Q3 人缘极好；Q4 设施齐全；Q5 推荐工作；Q6 引起怀疑。",
        "每题1分，共6分。")

    # (B) 选择词语 Q7-Q12 — page 2 (idx 1)
    add_q(db, p2.id, exam_dir, 7, None,
        "选择词语：奶奶___（兴致勃勃　小心翼翼　认认真真）地把古董花瓶放在桌上，生怕打破它。",
        1, "词语运用", 202, 2, (1, 0.59, 0.66),
        "小心翼翼。形容做事极为谨慎小心，与“生怕打破”相符。", "B1")

    add_q(db, p2.id, exam_dir, 8, None,
        "选择词语：任何有关电脑的问题，你都可以去找明华，因为他是班上的 IT ___（矮人　达人　工人）。",
        1, "词语运用", 202, 2, (1, 0.66, 0.72),
        "达人。指在某方面非常精通的人。", "B1")

    add_q(db, p2.id, exam_dir, 9, None,
        "选择词语：看到高头大马的大雄欺负我班的同学，我有些___（手足无措　心惊胆跳　挺身而出），不知如何是好。",
        1, "成语、谚语与惯用语", 206, 2, (1, 0.72, 0.79),
        "手足无措。形容遇事慌乱、不知怎么办，与“不知如何是好”相呼应。", "B1")

    add_q(db, p2.id, exam_dir, 10, None,
        "选择词语：兄弟两人争着去拿盘子，在___（拼命　拉扯　完成）之间，打破了它。",
        1, "词语运用", 202, 2, (1, 0.79, 0.85),
        "拉扯。指互相牵拉争夺，符合两人争抢盘子的语境。", "B1")

    add_q(db, p2.id, exam_dir, 11, None,
        "选择词语：同学们取笑美华胆子小，她___（赌气　重新　保护）地说：“不和你们玩了！”",
        1, "词语运用", 202, 2, (1, 0.85, 0.91),
        "赌气。指因不满或受刺激而任性行事，符合“不和你们玩了”的情绪。", "B1")

    add_q(db, p2.id, exam_dir, 12, None,
        "选择词语：如果你带香烟进校园，一定会___（惹麻烦　口头禅　爱捣乱）的。",
        1, "词语运用", 202, 2, (1, 0.91, 0.98),
        "惹麻烦。指招来麻烦或纠纷，符合违规带香烟的后果。", "B1")

    # (C) 填写词语（汉语拼音）Q13-Q17 — page 3 (idx 2)
    add_q(db, p2.id, exam_dir, 13, None,
        "根据汉语拼音填写词语：哥哥每个周末都去公园跑步，___（duàn liàn）身体。",
        2, "汉语拼音与字音字形", 201, 3, (2, 0.05, 0.10),
        "锻炼。", "每题2分。")

    add_q(db, p2.id, exam_dir, 14, None,
        "根据汉语拼音填写词语：顽皮的弟弟爱___（dǎo luàn），常常惹妈妈生气。",
        2, "汉语拼音与字音字形", 201, 3, (2, 0.10, 0.14),
        "捣乱。", "每题2分。")

    add_q(db, p2.id, exam_dir, 15, None,
        "根据汉语拼音填写词语：要在全班同学面前唱歌，妹妹感到十分___（biè niu）。",
        2, "汉语拼音与字音字形", 201, 3, (2, 0.14, 0.18),
        "别扭。", "每题2分。")

    add_q(db, p2.id, exam_dir, 16, None,
        "根据汉语拼音填写词语：那名偶像被观众丢鸡蛋，样子十分___（láng bèi）。",
        2, "汉语拼音与字音字形", 201, 3, (2, 0.18, 0.22),
        "狼狈。", "每题2分。")

    add_q(db, p2.id, exam_dir, 17, None,
        "根据汉语拼音填写词语：志强为了___（zhèng míng）自己没偷钱，主动让老师搜查书包。",
        2, "汉语拼音与字音字形", 201, 3, (2, 0.22, 0.27),
        "证明。", "每题2分。")

    # ───────── 二、理解问答 (18分) ─────────
    add_q(db, p2.id, exam_dir, 18, None,
        "根据短文的内容，把正确的答案填写在表格的空格里。"
        "表格列：什么人 / 什么时间（2分）/ 什么地点（2分）/ 发生什么事（4分）。"
        "大儿子（地点：大海）——什么时间？发生什么事？"
        "二儿子——什么时间？地点？（发生：在工地发生意外，被石块压死）"
        "小儿子（时间：10年后）——什么地点？发生什么事？",
        8, "阅读理解（记叙文）", 210, 4, (3, 0.04, 0.43),
        "大儿子：冬天；大海；在一个夜黑风高的晚上出意外，结果不幸在大海中淹死（2分）。"
        "二儿子：两年后；工地；在工地发生意外，被石块压死。"
        "小儿子：10年后；家里；成为一个既胆小又自私，而且好吃懒做，整天呆在家里的没有用的人（2分）。",
        "时间/地点各2分，事件各2分，共8分。",
        stem=PASSAGE)

    add_q(db, p2.id, exam_dir, 19, None,
        "文中哪一句话是比喻句？"
        "（1）力气很大的建筑工人。"
        "（2）就像一头虎虎生威的狮子。"
        "（3）老人感受到一种从来没有过的悲哀。"
        "（4）我宁愿他是一个毫无本事、没有出息的人啊！",
        2, "阅读理解（记叙文）", 210, 4, (3, 0.43, 0.58),
        "（2）就像一头虎虎生威的狮子。该句用“狮子”比喻大儿子大胆勇猛的精神。", "B1（2分）",
        stem=PASSAGE)

    add_q(db, p2.id, exam_dir, 20, None,
        "文中的“冒险精神”是指："
        "（1）做事情非常有责任心。"
        "（2）不顾危险地进行某种活动。"
        "（3）坚强又勇猛地进行某种活动。"
        "（4）大胆却不勇猛地进行某种活动。",
        2, "阅读理解（记叙文）", 210, 4, (3, 0.58, 0.74),
        "（2）不顾危险地进行某种活动。", "B1（2分）",
        stem=PASSAGE)

    add_q(db, p2.id, exam_dir, 21, None,
        "为什么老人要改变对小儿子的教育方式？",
        4, "阅读理解（记叙文）", 210, 4, (3, 0.74, 0.81),
        "因为他的大儿子和二儿子都遇难死了，两个很有才干的儿子都因意外身亡（1分）；"
        "他不想让小儿子成为一个出众的英雄人物（1分）；不要小儿子因为有才能而死（1分）；"
        "他不能再忍受失去儿子的痛苦（1分），所以改变对小儿子的教育方式。",
        "答对要点，每点1分，共4分。",
        stem=PASSAGE)

    add_q(db, p2.id, exam_dir, 22, None,
        "如果你是故事中的那名老人，你会故意让小儿子成为没有用的人吗？为什么？",
        4, "阅读理解（记叙文）", 210, 4, (3, 0.81, 0.92),
        "我不会这么做（1分）。因为大儿子和二儿子是因为发生意外才会死亡，跟有没有才能没有关系"
        "（1分）；如果把小儿子培养成一个没有用的人，不仅毁了小儿子的前途，也会让自己老了没有"
        "依靠（2分）。（言之成理即可）",
        "立场1分，理由3分，共4分。",
        stem=PASSAGE)

    db.commit()
    print(f"Seeded Xinmin Chinese exam id={exam.id}: Paper 2 ({len(p2.questions)} questions)")
    print(f"Images in {exam_dir}")
    db.close()


if __name__ == "__main__":
    main()
