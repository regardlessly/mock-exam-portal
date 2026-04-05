from sqlalchemy import (
    create_engine, Column, Integer, String, Text, Boolean, Date, DateTime,
    ForeignKey, func
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from pgvector.sqlalchemy import Vector

DATABASE_URL = "postgresql://timmy@localhost:5432/mock_exams"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class School(Base):
    __tablename__ = "schools"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, server_default=func.now())
    exams = relationship("Exam", back_populates="school")


class Exam(Base):
    __tablename__ = "exams"
    id = Column(Integer, primary_key=True)
    school_id = Column(Integer, ForeignKey("schools.id"))
    title = Column(String, nullable=False)
    year = Column(Integer)
    level = Column(String)
    subject = Column(String)
    source_pdf = Column(String)
    status = Column(String, default="processing")
    created_at = Column(DateTime, server_default=func.now())
    school = relationship("School", back_populates="exams")
    papers = relationship("Paper", back_populates="exam", order_by="Paper.paper_number")


class Paper(Base):
    __tablename__ = "papers"
    id = Column(Integer, primary_key=True)
    exam_id = Column(Integer, ForeignKey("exams.id"))
    paper_number = Column(Integer)
    duration_minutes = Column(Integer)
    total_marks = Column(Integer)
    date = Column(Date)
    instructions = Column(Text)
    exam = relationship("Exam", back_populates="papers")
    questions = relationship("Question", back_populates="paper", order_by="Question.question_number, Question.part")


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    paper_id = Column(Integer, ForeignKey("papers.id"))
    question_number = Column(Integer)
    part = Column(String, nullable=True)
    stem = Column(Text, nullable=True)
    question_text = Column(Text, nullable=False)
    marks = Column(Integer)
    topic = Column(String)
    topic_id = Column(Integer, nullable=True)
    page_image = Column(String)
    pdf_page = Column(Integer)
    is_validated = Column(Boolean, default=False)
    embedding = Column(Vector(1536), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    paper = relationship("Paper", back_populates="questions")
    answers = relationship("Answer", back_populates="question")


class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    answer_text = Column(Text, nullable=False)
    mark_scheme = Column(Text)
    question = relationship("Question", back_populates="answers")


class CurriculumTopic(Base):
    __tablename__ = "curriculum_topics"
    id = Column(Integer, primary_key=True)
    semester = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    subtopics = relationship("CurriculumSubtopic", back_populates="topic", order_by="CurriculumSubtopic.sort_order")
    bank_questions = relationship("BankQuestion", back_populates="topic")


class CurriculumSubtopic(Base):
    __tablename__ = "curriculum_subtopics"
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey("curriculum_topics.id"))
    title = Column(String, nullable=False)
    question_range = Column(String)  # e.g. "Q1–25"
    sort_order = Column(Integer, default=0)
    topic = relationship("CurriculumTopic", back_populates="subtopics")


class BankQuestion(Base):
    __tablename__ = "bank_questions"
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey("curriculum_topics.id"))
    subtopic_id = Column(Integer, ForeignKey("curriculum_subtopics.id"), nullable=True)
    question_number = Column(Integer)  # position within topic (1-150)
    question_text = Column(Text, nullable=False)
    option_a = Column(String, nullable=False)
    option_b = Column(String, nullable=False)
    option_c = Column(String, nullable=False)
    option_d = Column(String, nullable=False)
    correct_answer = Column(Integer, nullable=False)  # 0=A, 1=B, 2=C, 3=D
    explanation = Column(Text)
    embedding = Column(Vector(1536), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    topic = relationship("CurriculumTopic", back_populates="bank_questions")


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    attempts = relationship("PracticeAttempt", back_populates="student")


class PracticeAttempt(Base):
    __tablename__ = "practice_attempts"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    question_type = Column(String)  # 'mcq' or 'exam'
    bank_question_id = Column(Integer, ForeignKey("bank_questions.id"), nullable=True)
    exam_question_id = Column(Integer, ForeignKey("questions.id"), nullable=True)
    topic_id = Column(Integer, ForeignKey("curriculum_topics.id"), nullable=True)
    student_answer = Column(Text)
    is_correct = Column(Boolean)
    score = Column(Integer)  # 0, 50, or 100 (avoid floats)
    feedback = Column(Text)
    input_mode = Column(String)  # 'keyboard' or 'handwriting'
    time_taken_seconds = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    student = relationship("Student", back_populates="attempts")


def init_db():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    init_db()
    print("Database tables created.")
