# Implementation Plan — Add Science (Secondary 1 G3)

## Goal
Add **Lower Secondary Science (Sec 1 Express / G3)** to the existing portal using the
**exact same architecture** as Mathematics. Math stays untouched; Science is added
alongside it, selectable by subject.

---

## 1. Guiding Principle: Reuse, Don't Rebuild

Same stack, same patterns:
- Same PostgreSQL DB (`mock_exams` on Railway) + pgvector
- Same FastAPI backend (`main.py`, `practice_api.py`)
- Same SQLAlchemy models (`models.py`) — extend, don't replace
- Same seed-script-per-exam pattern (`seed_<school>.py`)
- Same parallel-agent PDF processing workflow
- Same cropped-image + KaTeX rendering (KaTeX still used for chemical/physics formulae & equations)
- Same Railway + GitHub deployment

The **only structural change**: a `subject` discriminator so Math and Science
coexist without collision.

---

## 2. Schema Changes (minimal, additive)

| Table | Change |
|-------|--------|
| `curriculum_topics` | **Add** `subject VARCHAR DEFAULT 'Mathematics'` |
| `exams` | Already has `subject` — populate `'Science'` for new exams |
| `bank_questions` | No change (inherits subject via `topic_id → curriculum_topics.subject`) |
| `practice_attempts` | No change (inherits subject via topic) |
| `questions` | No change (`exams.subject` already distinguishes; `topic_id` points at Science topics) |

Migration:
```sql
ALTER TABLE curriculum_topics ADD COLUMN IF NOT EXISTS subject VARCHAR DEFAULT 'Mathematics';
UPDATE curriculum_topics SET subject = 'Mathematics' WHERE subject IS NULL;
```

`models.py` — add `subject = Column(String, default="Mathematics")` to `CurriculumTopic`.

Topic IDs: Math uses 1–14. Science gets a separate ID range (e.g. **101–1xx**) so
`questions.topic_id` and `bank_questions.topic_id` never clash across subjects.

---

## 3. Sec 1 G3 Science Curriculum (Lower Sec Science syllabus)

Define ~12–14 topics, semester-split, mirroring the Math `curriculum.md` structure:

**Semester 1**
1. (101) Introduction to Science & the Laboratory — apparatus, safety, scientific method
2. (102) Physical Quantities, Units & Measurement — SI units, instruments, precision
3. (103) Particulate Nature of Matter — states, diffusion, kinetic model
4. (104) Elements, Compounds & Mixtures — classification, symbols
5. (105) Separation Techniques — filtration, distillation, chromatography
6. (106) Solutions & Suspensions — solubility, saturation

**Semester 2**
7. (107) Cells — plant/animal cells, organisation, microscopy
8. (108) Human Digestive System — enzymes, organs, absorption
9. (109) Transport in Living Things — diffusion, osmosis
10. (110) Energy — forms, conversions, sources
11. (111) Forces — types, effects, friction
12. (112) Electrical Systems — circuits, current, conductors
13. (113) Light & Sound — reflection, properties (if in scheme of work)
14. (114) Ray Model of Light / Heat (per school SoW)

Final topic list to be confirmed against the actual exam papers received
(topics are derived from what the papers test, same as Math).

Deliverables (same format as Math):
- `curriculum_science.md` — topic + subtopic structure
- `question_bank_science.md` — MCQ export

---

## 4. Science MCQ Question Bank

Math used the `math-quest` GitHub repo (2,101 MCQs). For Science:

**Option A (preferred):** Use an equivalent `science-quest` repo if one exists
(same `content/science/topics/*.ts` structure → reuse `seed_curriculum.py` parser
with minor path change → `seed_curriculum_science.py`).

**Option B:** Generate MCQs per topic via AI (Bedrock/Gemini) — 100–150 per topic,
4 options + explanation, written to the same `bank_questions` table with Science
`topic_id`s.

**Action:** confirm with user which source to use before seeding the bank.

---

## 5. Science Exam Processing (identical workflow)

For each Science exam PDF:
1. Extract page images with pymupdf → `/tmp/<school>_sci_pages/`
2. Parallel agents create `seed_<school>_sci.py` following the **exact same
   `seed_queensway.py` pattern**:
   - `School` row (reuse existing schools where the school already exists)
   - `Exam` with `subject="Science"`
   - `Paper` → `Question` (stem, part, KaTeX for formulae/equations, marks,
     topic, **Science topic_id**, crop region, answer, mark scheme)
3. Cropped question images → `uploads/{exam_id}/`
4. Seed local + Railway DB
5. Commit, push, Railway auto-deploys

KaTeX still renders science notation: `$\text{CO}_2$`, `$2\text{H}_2 + \text{O}_2 \to 2\text{H}_2\text{O}$`,
`$F = ma$`, units like `$5\ \text{m/s}^2$`.

---

## 6. API Changes (`practice_api.py`, `main.py`)

Add an optional `subject` query param (default `"Mathematics"` for backward compat):

| Endpoint | Change |
|----------|--------|
| `GET /api/practice/topics?subject=Science` | filter `curriculum_topics.subject` |
| `GET /api/practice/mcq` | already topic-scoped — works once topics are subject-tagged |
| `GET /api/practice/exam?subject=Science` | join `exams.subject` filter |
| `GET /api/practice/exam/filters?subject=Science` | filter exams by subject |
| `GET /api/exams?subject=Science` (portal) | filter exam list |
| `GET /api/curriculum/topics?subject=Science` | filter |

Caching keys become subject-scoped (`topics:Science`, `exam_filters:Science`).

---

## 7. Frontend Changes

**Practice app (`practice/index.html`):**
- Add a **subject toggle** on the landing screen: `[ Mathematics | Science ]`
- Store `currentSubject`; pass `?subject=` to all topic/exam/filter fetches
- Header subtitle switches: "Sec 1 Express Mathematics" / "Sec 1 Express Science"
- Everything else (MCQ flow, exam flow, keyboard/handwriting, marking) unchanged

**Portal (`frontend/index.html`):**
- Add subject filter chip to the exam list (All / Math / Science)

AI marking prompt for Science free-response: same `ai_mark_answer` function,
prompt tweaked to "Secondary 1 Science" and to accept scientific reasoning /
keyword-based mark schemes (B1/M1/A1 still apply).

---

## 8. File Manifest

| File | Action |
|------|--------|
| `models.py` | + `subject` on `CurriculumTopic` |
| `seed_curriculum_science.py` | **new** — seed Science topics + MCQ bank |
| `seed_<school>_sci.py` | **new** per Science exam (parallel agents) |
| `practice_api.py` | subject-aware filters + caching |
| `main.py` | subject filter on exam endpoints |
| `practice/index.html` | subject toggle |
| `frontend/index.html` | subject filter chip |
| `curriculum_science.md` | **new** — exported structure |
| `question_bank_science.md` | **new** — exported MCQs |
| `STRUCTURE.md` | update to document multi-subject |

---

## 9. Execution Order

1. Schema migration (`ALTER TABLE` + `models.py`) — local & Railway
2. Confirm Science MCQ source (repo vs AI-generated)
3. Build & run `seed_curriculum_science.py` → topics + bank
4. API: add `subject` params + subject-scoped cache
5. Frontend: subject toggle (practice) + filter (portal)
6. Receive Science exam PDFs → parallel agents → `seed_*_sci.py`
7. Verify (spot-check images vs question text, same as Math QA)
8. Commit, push, Railway deploy
9. Update memory + STRUCTURE.md

---

## 10. Open Questions for User

1. **Science MCQ bank source** — is there a `science-quest` repo, or generate via AI?
2. **Topic list** — derive purely from the exam papers (like Math), or seed from
   the MOE Lower Sec Science syllabus up front?
3. **Science exam PDFs** — provide them and we process in parallel batches,
   identical to the Math workflow.

No changes to Math. Science is purely additive and isolated by the `subject`
discriminator.
