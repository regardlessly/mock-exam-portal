"""Practice API router — MCQ quiz + free response with AI marking."""

import base64
import json
import os
import random
import re

import boto3
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from models import (
    SessionLocal, CurriculumTopic, BankQuestion, Question, Answer,
    Student, PracticeAttempt, School,
)

router = APIRouter(prefix="/api/practice", tags=["practice"])

# Simple in-memory cache for static data
_cache = {}
def cached(key, ttl=300):
    """Simple cache decorator check. Returns (hit, data)."""
    import time
    if key in _cache:
        ts, data = _cache[key]
        if time.time() - ts < ttl:
            return True, data
    return False, None
def set_cache(key, data):
    import time
    _cache[key] = (time.time(), data)

# Lazy Bedrock client
_bedrock = None


def get_bedrock():
    global _bedrock
    if _bedrock is None:
        _bedrock = boto3.client(
            "bedrock-runtime",
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        )
    return _bedrock


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Request/Response models ─────────────────────────────────

class StudentCreate(BaseModel):
    name: str

class MCQAnswer(BaseModel):
    student_id: int
    bank_question_id: int
    selected_answer: int  # 0-3
    time_taken_seconds: int = 0
    input_mode: str = "keyboard"

class FreeAnswer(BaseModel):
    student_id: int
    exam_question_id: int
    student_answer: str  # LaTeX or plain text
    time_taken_seconds: int = 0
    input_mode: str = "keyboard"

class RecogniseRequest(BaseModel):
    image_data: str  # base64 PNG from canvas
    subject: str = "Mathematics"


# ── Student ─────────────────────────────────────────────────

@router.post("/students")
def create_student(req: StudentCreate, db: Session = Depends(get_db)):
    # Reuse existing student if name matches
    existing = db.query(Student).filter(Student.name == req.name).first()
    if existing:
        return {"id": existing.id, "name": existing.name}
    student = Student(name=req.name)
    db.add(student)
    db.commit()
    db.refresh(student)
    return {"id": student.id, "name": student.name}


@router.get("/students")
def list_students(db: Session = Depends(get_db)):
    students = db.query(Student).order_by(Student.name).all()
    return [{"id": s.id, "name": s.name} for s in students]


# ── Topics ──────────────────────────────────────────────────

@router.get("/topics")
def practice_topics(subject: str = "Mathematics", db: Session = Depends(get_db)):
    hit, data = cached(f"topics:{subject}")
    if hit:
        return data

    topics = (
        db.query(CurriculumTopic)
        .filter(CurriculumTopic.subject == subject)
        .order_by(CurriculumTopic.id)
        .all()
    )

    # Single query for MCQ counts
    mcq_counts = dict(
        db.query(BankQuestion.topic_id, func.count(BankQuestion.id))
        .group_by(BankQuestion.topic_id).all()
    )
    # Single query for exam counts
    exam_counts = dict(
        db.query(Question.topic_id, func.count(Question.id))
        .filter(Question.topic_id.isnot(None))
        .group_by(Question.topic_id).all()
    )

    result = [
        {
            "id": t.id,
            "semester": t.semester,
            "title": t.title,
            "description": t.description,
            "mcq_count": mcq_counts.get(t.id, 0),
            "exam_count": exam_counts.get(t.id, 0),
        }
        for t in topics
    ]
    set_cache(f"topics:{subject}", result)
    return result


# ── MCQ Questions ───────────────────────────────────────────

@router.get("/mcq")
def get_mcq_questions(topic_id: int, count: int = 10, db: Session = Depends(get_db)):
    questions = db.query(BankQuestion).filter(
        BankQuestion.topic_id == topic_id
    ).all()
    if not questions:
        raise HTTPException(404, "No MCQs for this topic")
    sample = random.sample(questions, min(count, len(questions)))
    return [
        {
            "id": q.id,
            "topic_id": q.topic_id,
            "question_number": q.question_number,
            "question_text": q.question_text,
            "options": [q.option_a, q.option_b, q.option_c, q.option_d],
        }
        for q in sample
    ]


@router.post("/check-mcq")
def check_mcq(req: MCQAnswer, db: Session = Depends(get_db)):
    q = db.query(BankQuestion).filter(BankQuestion.id == req.bank_question_id).first()
    if not q:
        raise HTTPException(404, "Question not found")
    is_correct = req.selected_answer == q.correct_answer
    # Record attempt
    attempt = PracticeAttempt(
        student_id=req.student_id,
        question_type="mcq",
        bank_question_id=q.id,
        topic_id=q.topic_id,
        student_answer=str(req.selected_answer),
        is_correct=is_correct,
        score=100 if is_correct else 0,
        input_mode=req.input_mode,
        time_taken_seconds=req.time_taken_seconds,
    )
    db.add(attempt)
    db.commit()
    return {
        "correct": is_correct,
        "correct_answer": q.correct_answer,
        "explanation": q.explanation,
        "options": [q.option_a, q.option_b, q.option_c, q.option_d],
    }


# ── Exam Questions (free response) ──────────────────────────

@router.get("/exam")
def get_exam_questions(
    topic_id: int = None,
    paper_id: int = None,
    school_id: int = None,
    subject: str = "Mathematics",
    count: int = 5,
    db: Session = Depends(get_db),
):
    from models import Paper, Exam
    # Always scope through the Exam so subject is enforced (a school can have
    # both a Math and a Science exam under the same school_id).
    query = (
        db.query(Question)
        .join(Paper, Question.paper_id == Paper.id)
        .join(Exam, Paper.exam_id == Exam.id)
        .filter(Exam.subject == subject)
    )
    if topic_id:
        query = query.filter(Question.topic_id == topic_id)
    if paper_id:
        query = query.filter(Question.paper_id == paper_id)
    if school_id:
        query = query.filter(Exam.school_id == school_id)
    matched_parts = query.order_by(Question.paper_id, Question.question_number, Question.part).all()
    if not matched_parts:
        raise HTTPException(404, "No exam questions found for these filters")

    # Fetch ALL sibling parts for matched questions (so we don't split a/b)
    sibling_keys = list(set((q.paper_id, q.question_number) for q in matched_parts))
    from sqlalchemy import or_, and_
    sibling_filters = [
        and_(Question.paper_id == pid, Question.question_number == qnum)
        for pid, qnum in sibling_keys
    ]
    all_parts = db.query(Question).filter(
        or_(*sibling_filters)
    ).order_by(Question.paper_id, Question.question_number, Question.part).all()

    # Group parts by (paper_id, question_number)
    from collections import OrderedDict
    groups = OrderedDict()
    for q in all_parts:
        key = (q.paper_id, q.question_number)
        if key not in groups:
            groups[key] = []
        groups[key].append(q)

    # Sample whole groups, not individual parts
    group_keys = list(groups.keys())
    sampled_keys = random.sample(group_keys, min(count, len(group_keys)))
    questions = []
    for k in sampled_keys:
        questions.extend(groups[k])

    # Get paper/school info in ONE join query
    paper_ids = list(set(q.paper_id for q in questions))
    paper_rows = (
        db.query(Paper, Exam, School)
        .join(Exam, Paper.exam_id == Exam.id)
        .join(School, Exam.school_id == School.id)
        .filter(Paper.id.in_(paper_ids))
        .all()
    )
    paper_cache = {
        p.id: {"paper_number": p.paper_number, "exam_id": e.id, "exam_title": e.title, "school": s.name}
        for p, e, s in paper_rows
    }
    return [
        {
            "id": q.id,
            "question_number": q.question_number,
            "part": q.part,
            "stem": q.stem,
            "question_text": q.question_text,
            "marks": q.marks,
            "topic": q.topic,
            "page_image": q.page_image,
            "pdf_page": q.pdf_page,
            "paper_id": q.paper_id,
            "exam_id": paper_cache.get(q.paper_id, {}).get("exam_id"),
            "paper_number": paper_cache.get(q.paper_id, {}).get("paper_number"),
            "school": paper_cache.get(q.paper_id, {}).get("school"),
            "exam_title": paper_cache.get(q.paper_id, {}).get("exam_title"),
        }
        for q in questions
    ]


@router.get("/exam/filters")
def get_exam_filters(subject: str = "Mathematics", db: Session = Depends(get_db)):
    """Get available schools and papers for filtering."""
    hit, data = cached(f"exam_filters:{subject}")
    if hit:
        return data
    from models import Paper, Exam
    # Single join query
    rows = (
        db.query(Exam, School, Paper)
        .join(School, Exam.school_id == School.id)
        .join(Paper, Paper.exam_id == Exam.id)
        .filter(Exam.subject == subject)
        .order_by(Exam.school_id, Exam.year, Paper.paper_number)
        .all()
    )
    exams_map = {}
    for exam, school, paper in rows:
        if exam.id not in exams_map:
            exams_map[exam.id] = {
                "exam_id": exam.id, "school_id": school.id,
                "school": school.name, "title": exam.title,
                "year": exam.year, "papers": [],
            }
        exams_map[exam.id]["papers"].append({"id": paper.id, "paper_number": paper.paper_number})
    result = list(exams_map.values())
    set_cache(f"exam_filters:{subject}", result)
    return result


@router.post("/check-free")
def check_free_response(req: FreeAnswer, db: Session = Depends(get_db)):
    q = db.query(Question).filter(Question.id == req.exam_question_id).first()
    if not q:
        raise HTTPException(404, "Question not found")
    answer = db.query(Answer).filter(Answer.question_id == q.id).first()
    correct_answer = answer.answer_text if answer else ""
    mark_scheme = answer.mark_scheme if answer else ""

    # Determine subject (Question -> Paper -> Exam) for subject-aware marking
    subject = "Mathematics"
    if q.paper and q.paper.exam and q.paper.exam.subject:
        subject = q.paper.exam.subject

    # AI marking via Bedrock
    try:
        result = ai_mark_answer(
            question=q.question_text,
            stem=q.stem or "",
            student_answer=req.student_answer,
            correct_answer=correct_answer,
            mark_scheme=mark_scheme,
            marks=q.marks or 1,
            subject=subject,
        )
    except Exception as e:
        result = {"score": 0, "feedback": f"AI marking unavailable: {e}", "is_correct": False}

    attempt = PracticeAttempt(
        student_id=req.student_id,
        question_type="exam",
        exam_question_id=q.id,
        topic_id=q.topic_id,
        student_answer=req.student_answer,
        is_correct=result["is_correct"],
        score=result["score"],
        feedback=result["feedback"],
        input_mode=req.input_mode,
        time_taken_seconds=req.time_taken_seconds,
    )
    db.add(attempt)
    db.commit()
    return {
        "score": result["score"],
        "is_correct": result["is_correct"],
        "feedback": result["feedback"],
        "correct_answer": correct_answer,
        "mark_scheme": mark_scheme,
    }


# ── Handwriting Recognition ─────────────────────────────────

@router.post("/recognise")
def recognise_handwriting(req: RecogniseRequest):
    """Send canvas image to Claude Vision to extract math answer."""
    try:
        result = ai_recognise_handwriting(req.image_data, subject=req.subject)
        return {"recognised_text": result}
    except Exception as e:
        # Return error message instead of 500 so frontend can handle it
        return {"recognised_text": None, "error": str(e)}


# ── Progress ────────────────────────────────────────────────

@router.get("/progress/{student_id}")
def get_progress(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(404, "Student not found")

    attempts = db.query(PracticeAttempt).filter(
        PracticeAttempt.student_id == student_id
    ).all()

    # Per-topic stats
    topic_stats = {}
    for a in attempts:
        tid = a.topic_id or 0
        if tid not in topic_stats:
            topic_stats[tid] = {"total": 0, "correct": 0}
        topic_stats[tid]["total"] += 1
        if a.is_correct:
            topic_stats[tid]["correct"] += 1

    total = len(attempts)
    correct = sum(1 for a in attempts if a.is_correct)

    return {
        "student_id": student_id,
        "name": student.name,
        "total_attempts": total,
        "total_correct": correct,
        "accuracy": round(correct / total * 100) if total > 0 else 0,
        "topic_stats": {
            str(tid): {
                "total": s["total"],
                "correct": s["correct"],
                "accuracy": round(s["correct"] / s["total"] * 100) if s["total"] > 0 else 0,
            }
            for tid, s in topic_stats.items()
        },
    }


# ── AI Functions (Bedrock) ──────────────────────────────────

def _call_claude(messages, max_tokens=500, temperature=0.1):
    """Call Claude via Bedrock or Anthropic API, with fallback."""
    # Try Bedrock first
    try:
        bedrock = get_bedrock()
        response = bedrock.converse(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            messages=messages,
            inferenceConfig={"maxTokens": max_tokens, "temperature": temperature},
        )
        return response["output"]["message"]["content"][0]["text"]
    except Exception as bedrock_err:
        pass

    # Try Anthropic API
    try:
        import anthropic
        client = anthropic.Anthropic()  # uses ANTHROPIC_API_KEY env var
        # Convert Bedrock message format to Anthropic format
        ant_messages = []
        for m in messages:
            content = []
            for c in m["content"]:
                if "text" in c:
                    content.append({"type": "text", "text": c["text"]})
                elif "image" in c:
                    img = c["image"]
                    content.append({
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": f"image/{img['format']}",
                            "data": base64.b64encode(img["source"]["bytes"]).decode(),
                        },
                    })
            ant_messages.append({"role": m["role"], "content": content})

        resp = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=max_tokens,
            messages=ant_messages,
        )
        return resp.content[0].text
    except Exception:
        pass

    raise RuntimeError(f"No AI backend available. Bedrock error: {bedrock_err}")


def ai_mark_answer(question, stem, student_answer, correct_answer, mark_scheme, marks,
                   subject="Mathematics"):
    """Use Claude to mark a free-response answer (subject-aware)."""
    if subject == "Chinese":
        # 中文作文 / 阅读理解 评分 — 评语用中文
        prompt = (
            "你是一位严格的新加坡中学一年级（中一）普通华文阅卷老师。\n\n"
            f"题目：{stem} {question}\n"
            f"参考答案：{correct_answer}\n"
            f"评分标准：{mark_scheme}\n"
            f"满分：{marks}\n\n"
            f"学生的答案：{student_answer}\n\n"
            "评分要求：\n"
            "- 从【内容】【语言】【结构】三方面综合评估学生答案。\n"
            "- 把学生答案与参考答案严格对照；若答非所问或意思错误，给 0 分，is_correct=false。\n"
            "- 只有当答案在意思上与参考答案一致、表达通顺时才给 is_correct=true。\n"
            "- 部分正确（分数 30-70）：要点不全或有语言错误但方向正确。\n"
            "- 随意作答或与题意无关的答案给 0 分。\n"
            "- 反馈（feedback）必须用中文，语气鼓励但要诚实指出对错。\n\n"
            '只回复一个 JSON 对象（不要 markdown，不要多余文字）：\n'
            '{"score": <0 到 100>, "is_correct": true/false, "feedback": "简短的中文鼓励性评语"}'
        )
    else:
        prompt = (
            f"You are a STRICT marker for a Secondary 1 {subject} exam.\n\n"
            f"Question: {stem} {question}\n"
            f"Correct answer: {correct_answer}\n"
            f"Mark scheme: {mark_scheme}\n"
            f"Total marks: {marks}\n\n"
            f"Student's answer: {student_answer}\n\n"
            "IMPORTANT RULES:\n"
            "- Compare the student's answer EXACTLY against the correct answer.\n"
            "- If the student's answer does not match or is wrong, score 0 and is_correct=false.\n"
            "- Only give is_correct=true if the answer is equivalent to the correct answer.\n"
            "- Partial credit (score 30-70) only if the student shows correct working but makes a minor error.\n"
            "- An answer of just a random value that doesn't match is score 0.\n"
            "- Be encouraging in feedback but HONEST about whether it's right or wrong.\n\n"
            'Respond ONLY with a JSON object (no markdown, no extra text):\n'
            '{"score": <0 to 100>, "is_correct": true/false, "feedback": "brief encouraging feedback"}'
        )

    text = _call_claude(
        [{"role": "user", "content": [{"text": prompt}]}],
        max_tokens=500, temperature=0.1,
    )
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        parsed = json.loads(text[start:end])
        # If feedback is itself a JSON string, extract it
        fb = parsed.get("feedback", "")
        if isinstance(fb, str) and fb.strip().startswith("{"):
            try:
                inner = json.loads(fb)
                parsed = inner
            except (ValueError, json.JSONDecodeError):
                pass
        # Ensure required fields
        return {
            "score": parsed.get("score", 0),
            "is_correct": parsed.get("is_correct", False),
            "feedback": parsed.get("feedback", ""),
        }
    except (ValueError, json.JSONDecodeError):
        return {"score": 0, "is_correct": False, "feedback": text}


GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

MATH_RECOGNITION_PROMPT = (
    "Look at this handwritten math expression. "
    "Return ONLY the LaTeX representation of what is written. "
    "Do not include any explanation, dollar signs, or delimiters. "
    "Just the raw LaTeX. For example: \\frac{1}{2} or x = 5 or 42"
)


CHINESE_RECOGNITION_PROMPT = (
    "请识别这张图片中手写的中文内容。"
    "只返回识别出的中文文字本身，不要任何解释、标点说明或定界符。"
    "保留原有的标点符号。直接输出文字。"
)


def _clean_recognised(text):
    """Strip delimiters the model might include (same as math-stylus-support)."""
    import re
    text = text.strip()
    text = re.sub(r'^\$\$', '', text)
    text = re.sub(r'\$\$$', '', text)
    text = re.sub(r'^\$', '', text)
    text = re.sub(r'\$$', '', text)
    text = re.sub(r'^```latex\n?', '', text)
    text = re.sub(r'\n?```$', '', text)
    return text.strip()


def ai_recognise_handwriting(image_base64, subject="Mathematics"):
    """Recognise handwriting — Gemini Flash (preferred) or Claude Haiku fallback.

    Subject-aware: Chinese uses a Chinese-character OCR prompt; everything
    else uses the math/LaTeX prompt.
    """
    if "," in image_base64:
        image_base64 = image_base64.split(",", 1)[1]

    image_bytes = base64.b64decode(image_base64)
    is_chinese = subject == "Chinese"
    rec_prompt = CHINESE_RECOGNITION_PROMPT if is_chinese else MATH_RECOGNITION_PROMPT

    # Try Gemini Flash first (free tier)
    api_key = GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY")
    if api_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content([
                {"mime_type": "image/png", "data": image_bytes},
                rec_prompt,
            ], generation_config={"max_output_tokens": 1024, "temperature": 0.0})
            text = response.text
            return text.strip() if is_chinese else _clean_recognised(text)
        except Exception:
            pass  # Fall through to Claude

    # Fallback to Claude Haiku via Bedrock
    text = _call_claude(
        [{
            "role": "user",
            "content": [
                {"image": {"format": "png", "source": {"bytes": image_bytes}}},
                {"text": rec_prompt},
            ],
        }],
        max_tokens=100, temperature=0,
    )
    return text.strip() if is_chinese else _clean_recognised(text)
