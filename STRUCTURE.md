# Mock Exam Portal — Confirmed Structure

## Architecture

```
Frontend (index.html)  ──>  FastAPI (main.py)  ──>  PostgreSQL + pgvector
     KaTeX math                 REST API              mock_exams DB
     Vanilla JS                 Static files
```

## Database Schema (PostgreSQL 17 + pgvector)

### Curriculum Layer

```
curriculum_topics (14 rows)
├── id              INT PK          — Topic 1–14
├── semester        INT             — 1 or 2
├── title           VARCHAR         — e.g. "Primes, HCF & LCM"
├── description     TEXT
└── created_at      TIMESTAMP

curriculum_subtopics (28 rows)
├── id              INT PK
├── topic_id        INT FK → curriculum_topics
├── title           VARCHAR         — e.g. "PRIME NUMBERS (Q1–25)"
├── question_range  VARCHAR         — e.g. "Q1–25"
└── sort_order      INT

bank_questions (2,101 rows)
├── id              INT PK
├── topic_id        INT FK → curriculum_topics
├── subtopic_id     INT FK → curriculum_subtopics (nullable)
├── question_number INT             — Position within topic (1–150)
├── question_text   TEXT
├── option_a–d      VARCHAR         — Four MCQ options
├── correct_answer  INT             — 0=A, 1=B, 2=C, 3=D
├── explanation     TEXT
├── embedding       vector(1536)    — For similarity search (future)
└── created_at      TIMESTAMP
```

### Exam Layer

```
schools (1 row)
├── id              INT PK
├── name            VARCHAR UNIQUE  — e.g. "Northbrooks Secondary School"
└── created_at      TIMESTAMP

exams (1 row)
├── id              INT PK
├── school_id       INT FK → schools
├── title           VARCHAR         — e.g. "End-of-Year Examination 2022"
├── year            INT
├── level           VARCHAR         — e.g. "Secondary 1 Express"
├── subject         VARCHAR         — e.g. "Mathematics"
├── source_pdf      VARCHAR         — Original filename
├── status          VARCHAR         — processing | ready | error
└── created_at      TIMESTAMP

papers (2 rows per exam)
├── id              INT PK
├── exam_id         INT FK → exams
├── paper_number    INT             — 1 or 2
├── duration_minutes INT
├── total_marks     INT
├── date            DATE
└── instructions    TEXT

questions (56 rows — 30 Paper 1 + 26 Paper 2)
├── id              INT PK
├── paper_id        INT FK → papers
├── question_number INT             — e.g. 1, 2, 3...
├── part            VARCHAR         — e.g. "a", "b", "ai", "aii", NULL
├── stem            TEXT            — Shared question stem (first part only)
├── question_text   TEXT            — Part-specific text (KaTeX math)
├── marks           INT
├── topic           VARCHAR         — Descriptive label
├── topic_id        INT             — FK-like ref to curriculum_topics.id
├── page_image      VARCHAR         — Cropped question image filename
├── pdf_page        INT             — Original PDF page number
├── is_validated    BOOLEAN         — Reviewer validation flag
├── embedding       vector(1536)    — For similarity search (future)
└── created_at      TIMESTAMP

answers (56 rows — 1 per question part)
├── id              INT PK
├── question_id     INT FK → questions
├── answer_text     TEXT            — Worked solution (KaTeX math)
└── mark_scheme     TEXT            — e.g. "M1, A1" or "B1"
```

### Relationships

```
curriculum_topics  1──M  curriculum_subtopics
curriculum_topics  1──M  bank_questions
curriculum_subtopics  1──M  bank_questions

schools  1──M  exams
exams    1──M  papers
papers   1──M  questions
questions  1──M  answers

questions.topic_id  ──>  curriculum_topics.id  (logical link)
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| **Exams** | | |
| GET | `/api/exams` | List all exams with validation progress |
| GET | `/api/exams/{id}` | Exam detail with papers |
| POST | `/api/exams/upload` | Upload PDF, extract page images |
| **Papers & Questions** | | |
| GET | `/api/papers/{id}/questions` | Questions for a paper (with stem, topic_id) |
| GET | `/api/questions/{id}` | Single question with answer |
| GET | `/api/questions/{id}/similar` | Similar questions via pgvector cosine |
| PATCH | `/api/questions/{id}/validate` | Toggle validation checkbox |
| **Curriculum** | | |
| GET | `/api/curriculum/topics` | 14 topics with subtopics and question counts |
| GET | `/api/curriculum/topics/{id}` | Single topic detail |
| GET | `/api/curriculum/questions` | Browse question bank (filter by topic_id, subtopic_id, pagination) |
| **Static** | | |
| GET | `/images/{exam_id}/{filename}` | Serve cropped question images |
| GET | `/frontend/index.html` | SPA frontend |

## Frontend Features

- **Dashboard** with Exams / Question Bank tabs
- **Upload zone** — drag/drop or file select for PDF upload
- **Exam viewer** — Paper 1/2 tabs, topic filter dropdown
- **Grouped questions** — shared stem above sub-parts (a), (b), (c)
- **Side-by-side** — digitised KaTeX text alongside cropped PDF image
- **Answers** — collapsible with M1/A1/B1 mark scheme badges
- **Validation** — checkbox per question, progress bar
- **Question Bank** — browse 2,101 MCQs, filter by topic, paginated
- **Image modal** — click thumbnail to see full cropped question

## Question Data Format

### Exam Questions (structured/open-ended)
- Stored with **stem** (shared preamble) + **part text**
- KaTeX math: `$...$` for inline, `$$...$$` for display
- Each part has a **cropped PDF image** for validation
- Answers include worked solutions and mark scheme

### Bank Questions (MCQ)
- 4 options (A/B/C/D) with one correct answer
- Explanation for the correct answer
- Linked to curriculum topic and subtopic

## Topic Alignment (Exam → Curriculum)

| Exam Topic | Topic ID | Curriculum Topic |
|---|---|---|
| Rounding / Approximation | 3 | Approximation & Estimation |
| Number Sets, Comparing Numbers | 2 | Integers, Rational & Real Numbers |
| Prime Factorisation, HCF, LCM | 1 | Primes, HCF & LCM |
| Algebra (Expansion/Factorisation/Substitution) | 4 | Basic Algebra & Manipulation |
| Linear Equations — Word Problem | 5 | Linear Equations |
| Coordinate Geometry, Linear Graphs | 6 | Linear Functions |
| Number Patterns | 7 | Number Patterns |
| Percentage | 8 | Percentage |
| Speed/Distance/Time, Rate, Ratio | 9 | Ratio, Rate & Speed |
| Angle Properties, Construction | 10 | Geometry & Angles |
| Polygon Angles | 11 | Polygons |
| Area (Semicircle/Trapezium) | 12 | Perimeter & Area |
| Volume (Cylinder/Cube) | 13 | Volume & Surface Area |

## File Structure

```
mock-exam-portal/
├── main.py                  # FastAPI app (all endpoints)
├── models.py                # SQLAlchemy models (8 tables)
├── processor.py             # PDF → page images + cropping
├── seed.py                  # Seed Northbrooks exam (56 questions)
├── seed_curriculum.py       # Seed curriculum + 2,101 MCQs
├── requirements.txt         # Python dependencies
├── frontend/
│   └── index.html           # SPA (KaTeX + vanilla JS)
├── uploads/{exam_id}/       # Cropped question images per exam
├── images/                  # Raw full-page PDF images
├── curriculum.md            # Curriculum structure (MD export)
├── question_bank.md         # 2,101 MCQs (MD export)
├── northbrooks_eoy2022_math.md  # Exam data with topic alignment (MD export)
└── STRUCTURE.md             # This file
```

## How to Start

```bash
export PATH="/opt/homebrew/opt/postgresql@17/bin:/opt/homebrew/bin:/Users/timmy/Library/Python/3.9/bin:$PATH"
brew services start postgresql@17
cd ~/Claude/mock-exam-portal
python3 -m uvicorn main:app --port 8000
# Open http://localhost:8000
```

## How to Re-seed

```bash
python3 seed.py              # Northbrooks exam questions
python3 seed_curriculum.py   # Curriculum + 2,101 MCQs
```
