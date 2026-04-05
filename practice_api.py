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
def practice_topics(db: Session = Depends(get_db)):
    topics = db.query(CurriculumTopic).order_by(CurriculumTopic.id).all()

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

    return [
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
    count: int = 5,
    db: Session = Depends(get_db),
):
    from models import Paper, Exam
    query = db.query(Question)
    if topic_id:
        query = query.filter(Question.topic_id == topic_id)
    if paper_id:
        query = query.filter(Question.paper_id == paper_id)
    if school_id:
        query = query.join(Paper, Question.paper_id == Paper.id).join(
            Exam, Paper.exam_id == Exam.id
        ).filter(Exam.school_id == school_id)
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
def get_exam_filters(db: Session = Depends(get_db)):
    """Get available schools and papers for filtering."""
    from models import Paper, Exam
    # Single join query
    rows = (
        db.query(Exam, School, Paper)
        .join(School, Exam.school_id == School.id)
        .join(Paper, Paper.exam_id == Exam.id)
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
    return list(exams_map.values())


@router.post("/check-free")
def check_free_response(req: FreeAnswer, db: Session = Depends(get_db)):
    q = db.query(Question).filter(Question.id == req.exam_question_id).first()
    if not q:
        raise HTTPException(404, "Question not found")
    answer = db.query(Answer).filter(Answer.question_id == q.id).first()
    correct_answer = answer.answer_text if answer else ""
    mark_scheme = answer.mark_scheme if answer else ""

    # AI marking via Bedrock
    try:
        result = ai_mark_answer(
            question=q.question_text,
            stem=q.stem or "",
            student_answer=req.student_answer,
            correct_answer=correct_answer,
            mark_scheme=mark_scheme,
            marks=q.marks or 1,
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
        result = ai_recognise_handwriting(req.image_data)
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


def ai_mark_answer(question, stem, student_answer, correct_answer, mark_scheme, marks):
    """Use Claude to mark a free-response answer."""
    prompt = (
        "You are marking a Secondary 1 Mathematics exam answer.\n\n"
        f"Question: {stem} {question}\n"
        f"Correct answer: {correct_answer}\n"
        f"Mark scheme: {mark_scheme}\n"
        f"Total marks: {marks}\n\n"
        f"Student's answer: {student_answer}\n\n"
        "Evaluate the student's answer. Be generous with partial credit. "
        "Focus on mathematical correctness, not formatting.\n\n"
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


def ai_recognise_handwriting(image_base64):
    """Recognise handwritten math — uses Gemini Flash (preferred) or Claude Haiku fallback."""
    if "," in image_base64:
        image_base64 = image_base64.split(",", 1)[1]

    image_bytes = base64.b64decode(image_base64)

    # Try Gemini Flash first (free tier, optimised for math handwriting)
    api_key = GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY")
    if api_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content([
                {"mime_type": "image/png", "data": image_bytes},
                MATH_RECOGNITION_PROMPT,
            ], generation_config={"max_output_tokens": 1024, "temperature": 0.0})
            return _clean_recognised(response.text)
        except Exception:
            pass  # Fall through to Claude

    # Fallback to Claude Haiku via Bedrock
    text = _call_claude(
        [{
            "role": "user",
            "content": [
                {"image": {"format": "png", "source": {"bytes": image_bytes}}},
                {"text": MATH_RECOGNITION_PROMPT},
            ],
        }],
        max_tokens=100, temperature=0,
    )
    return _clean_recognised(text)
