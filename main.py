import os
import shutil
import uuid

# Load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from models import (
    SessionLocal, Exam, Paper, Question, Answer, School,
    CurriculumTopic, CurriculumSubtopic, BankQuestion, init_db
)
from processor import process_pdf
from practice_api import router as practice_router

app = FastAPI(title="Mock Exam Portal")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(practice_router)

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")
PRACTICE_DIR = os.path.join(os.path.dirname(__file__), "practice")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Serve frontend
app.mount("/practice", StaticFiles(directory=PRACTICE_DIR, html=True), name="practice")
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Exam endpoints ──────────────────────────────────────────────

@app.get("/api/exams")
def list_exams(db: Session = Depends(get_db)):
    exams = db.query(Exam).order_by(Exam.created_at.desc()).all()
    results = []
    for e in exams:
        school_name = e.school.name if e.school else None
        total_questions = sum(len(p.questions) for p in e.papers)
        validated = sum(1 for p in e.papers for q in p.questions if q.is_validated)
        results.append({
            "id": e.id,
            "school": school_name,
            "title": e.title,
            "year": e.year,
            "level": e.level,
            "subject": e.subject,
            "status": e.status,
            "source_pdf": e.source_pdf,
            "total_questions": total_questions,
            "validated_questions": validated,
            "papers": [{"id": p.id, "paper_number": p.paper_number} for p in e.papers],
        })
    return results


@app.get("/api/exams/{exam_id}")
def get_exam(exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(404, "Exam not found")
    school_name = exam.school.name if exam.school else None
    return {
        "id": exam.id,
        "school": school_name,
        "title": exam.title,
        "year": exam.year,
        "level": exam.level,
        "subject": exam.subject,
        "status": exam.status,
        "source_pdf": exam.source_pdf,
        "papers": [
            {
                "id": p.id,
                "paper_number": p.paper_number,
                "duration_minutes": p.duration_minutes,
                "total_marks": p.total_marks,
                "date": str(p.date) if p.date else None,
                "instructions": p.instructions,
            }
            for p in exam.papers
        ],
    }


# ── Paper / Question endpoints ──────────────────────────────────

@app.get("/api/papers/{paper_id}/questions")
def list_questions(paper_id: int, db: Session = Depends(get_db)):
    paper = db.query(Paper).filter(Paper.id == paper_id).first()
    if not paper:
        raise HTTPException(404, "Paper not found")
    questions = db.query(Question).filter(Question.paper_id == paper_id).order_by(
        Question.question_number, Question.part
    ).all()
    return [
        {
            "id": q.id,
            "question_number": q.question_number,
            "part": q.part,
            "stem": q.stem,
            "question_text": q.question_text,
            "marks": q.marks,
            "topic": q.topic,
            "topic_id": q.topic_id,
            "page_image": q.page_image,
            "pdf_page": q.pdf_page,
            "is_validated": q.is_validated,
            "answers": [
                {"id": a.id, "answer_text": a.answer_text, "mark_scheme": a.mark_scheme}
                for a in q.answers
            ],
        }
        for q in questions
    ]


@app.get("/api/questions/{question_id}")
def get_question(question_id: int, db: Session = Depends(get_db)):
    q = db.query(Question).filter(Question.id == question_id).first()
    if not q:
        raise HTTPException(404, "Question not found")
    return {
        "id": q.id,
        "question_number": q.question_number,
        "part": q.part,
        "stem": q.stem,
        "question_text": q.question_text,
        "marks": q.marks,
        "topic": q.topic,
            "topic_id": q.topic_id,
        "page_image": q.page_image,
        "pdf_page": q.pdf_page,
        "is_validated": q.is_validated,
        "answers": [
            {"id": a.id, "answer_text": a.answer_text, "mark_scheme": a.mark_scheme}
            for a in q.answers
        ],
    }


@app.get("/api/questions/{question_id}/similar")
def similar_questions(question_id: int, limit: int = 5, db: Session = Depends(get_db)):
    q = db.query(Question).filter(Question.id == question_id).first()
    if not q:
        raise HTTPException(404, "Question not found")
    if q.embedding is None:
        return []
    # Cosine distance search
    similar = (
        db.query(Question)
        .filter(Question.id != question_id, Question.embedding.isnot(None))
        .order_by(Question.embedding.cosine_distance(q.embedding))
        .limit(limit)
        .all()
    )
    return [
        {
            "id": s.id,
            "question_number": s.question_number,
            "part": s.part,
            "question_text": s.question_text,
            "topic": s.topic,
            "paper_id": s.paper_id,
        }
        for s in similar
    ]


@app.patch("/api/questions/{question_id}/validate")
def toggle_validate(question_id: int, db: Session = Depends(get_db)):
    q = db.query(Question).filter(Question.id == question_id).first()
    if not q:
        raise HTTPException(404, "Question not found")
    q.is_validated = not q.is_validated
    db.commit()
    return {"id": q.id, "is_validated": q.is_validated}


# ── Upload endpoint ─────────────────────────────────────────────

@app.post("/api/exams/upload")
async def upload_exam(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are accepted")

    # Create a temporary exam record
    school = db.query(School).filter(School.name == "Unknown School").first()
    if not school:
        school = School(name="Unknown School")
        db.add(school)
        db.flush()

    exam = Exam(
        school_id=school.id,
        title="Uploaded Exam",
        subject="Mathematics",
        source_pdf=file.filename,
        status="processing",
    )
    db.add(exam)
    db.flush()

    # Save PDF and extract images
    exam_dir = os.path.join(UPLOAD_DIR, str(exam.id))
    os.makedirs(exam_dir, exist_ok=True)
    pdf_path = os.path.join(exam_dir, "original.pdf")

    with open(pdf_path, "wb") as f:
        content = await file.read()
        f.write(content)

    try:
        result = process_pdf(pdf_path, exam_dir)
        exam.status = "ready"
    except Exception as e:
        exam.status = "error"
        db.commit()
        raise HTTPException(500, f"PDF processing failed: {e}")

    db.commit()

    return {
        "id": exam.id,
        "status": exam.status,
        "page_count": result["page_count"],
        "message": "PDF uploaded and images extracted. Questions need to be added manually or via processing pipeline.",
    }


# ── Image serving ───────────────────────────────────────────────

@app.get("/images/{exam_id}/{filename}")
def serve_image(exam_id: int, filename: str):
    path = os.path.join(UPLOAD_DIR, str(exam_id), filename)
    if not os.path.isfile(path):
        raise HTTPException(404, "Image not found")
    return FileResponse(path, media_type="image/png")


# ── Curriculum endpoints ─────────────────────────────────────────

@app.get("/api/curriculum/topics")
def list_topics(db: Session = Depends(get_db)):
    topics = db.query(CurriculumTopic).order_by(CurriculumTopic.id).all()
    return [
        {
            "id": t.id,
            "semester": t.semester,
            "title": t.title,
            "description": t.description,
            "subtopics": [
                {"id": s.id, "title": s.title, "question_range": s.question_range}
                for s in t.subtopics
            ],
            "question_count": len(t.bank_questions),
        }
        for t in topics
    ]


@app.get("/api/curriculum/topics/{topic_id}")
def get_topic(topic_id: int, db: Session = Depends(get_db)):
    t = db.query(CurriculumTopic).filter(CurriculumTopic.id == topic_id).first()
    if not t:
        raise HTTPException(404, "Topic not found")
    return {
        "id": t.id,
        "semester": t.semester,
        "title": t.title,
        "description": t.description,
        "subtopics": [
            {"id": s.id, "title": s.title, "question_range": s.question_range}
            for s in t.subtopics
        ],
        "question_count": len(t.bank_questions),
    }


@app.get("/api/curriculum/questions")
def list_bank_questions(
    topic_id: int = None,
    subtopic_id: int = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    query = db.query(BankQuestion)
    if topic_id:
        query = query.filter(BankQuestion.topic_id == topic_id)
    if subtopic_id:
        query = query.filter(BankQuestion.subtopic_id == subtopic_id)
    total = query.count()
    questions = query.order_by(BankQuestion.topic_id, BankQuestion.question_number).offset(offset).limit(limit).all()
    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "questions": [
            {
                "id": q.id,
                "topic_id": q.topic_id,
                "subtopic_id": q.subtopic_id,
                "question_number": q.question_number,
                "question_text": q.question_text,
                "options": [q.option_a, q.option_b, q.option_c, q.option_d],
                "correct_answer": q.correct_answer,
                "explanation": q.explanation,
            }
            for q in questions
        ],
    }


# ── Root redirect ───────────────────────────────────────────────

@app.get("/")
def root():
    from fastapi.responses import RedirectResponse
    return RedirectResponse("/frontend/index.html")


if __name__ == "__main__":
    init_db()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
