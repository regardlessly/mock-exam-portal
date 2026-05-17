# Implementation Plan — Add Geography (Sec 1 G3), 4th subject

## Goal
Add **Secondary 1 Geography (G3)** as a fourth subject using the **exact same
architecture** as Math, Science and Chinese. Math + Science + Chinese stay
untouched; Geography is additive, isolated by the existing `subject`
discriminator. This is mostly **content + small UI strings**, not new
architecture.

Topic ID ranges (no collisions): Math `1–14`, Science `101–114`,
Chinese `201–212`, **Geography `301–3xx`**.

---

## 1. Reuse — what already works, no change needed
- `curriculum_topics.subject`, `exams.subject` columns ✅
- API `?subject=` filtering (topics, exams, filters, bank, curriculum) ✅
- Subject-scoped caching ✅
- Portal: subject toggle now **filters the Uploaded Exams listing** + Question
  Bank + curriculum (just shipped) ✅
- Practice app subject toggle + subject-aware (no-KaTeX) preview ✅
- GitHub → Railway auto-deploy pipeline ✅
- Per-exam seed-script pattern + parallel-agent PDF processing ✅
- Cross-subject ID-collision safety (restore tracked `uploads/`, commit only
  new Railway-aligned dirs) — the lesson from Chinese ✅

---

## 2. Geography-specific differences vs Chinese

| Concern | Chinese | Geography — what changes |
|---|---|---|
| Notation | Pure CJK, no `$` | English text, **no KaTeX/`$`** (same plain-text treatment as Chinese) |
| Fonts | Noto Sans SC CJK font | **None** — default sans is fine (English) |
| Question types | MCQ + 实用文/作文 | MCQ for objective; **data-response / source-based / structured** = free-response |
| MCQ content | Chinese | English Sec 1 Geography (maps, climate, water, etc.) |
| AI marking | Chinese 评分标准 prompt | **English Geography rubric**: content, use of data/evidence, geographical terms |
| Handwriting OCR | Chinese-character prompt | **Plain-English text** prompt (not LaTeX) — add a Geography branch |
| Images | Cropped question images | Same — but maps/graphs/photos are central; crop fidelity matters more |

The subject-aware preview gate (`currentSubject === 'Chinese'`) becomes a set:
`['Chinese','Geography'].includes(currentSubject)` → plain-text preview, no KaTeX.

---

## 3. Sec 1 Geography (G3) Curriculum — pre-seed from MOE syllabus

~12 topics (IDs 301–312), the objectively-testable areas of the MOE Lower
Secondary Geography syllabus. Semester split mirrors the other subjects.

**Semester 1**
- 301 Geographical Skills: Maps & Map Reading (grid refs, scale, distance, direction)
- 302 Geographical Skills: Relief, Photographs & GIS
- 303 Weather & Climate: Elements & Instruments
- 304 Weather & Climate: Factors Affecting Temperature & Rainfall
- 305 Climate Graphs & Data Interpretation
- 306 The Water Cycle & Drainage Basins

**Semester 2**
- 307 Rivers & River Landforms
- 308 Water Resources & Management
- 309 Tropical Rainforest Ecosystems
- 310 Variable Weather & Climate Change
- 311 Natural Vegetation & Biomes
- 312 Tourism & Sustainable Development

Confirm or adjust this topic list (same approach as Science/Chinese — topics
can be reconciled against the actual exam papers).

Deliverables: `curriculum_geography.py`, exported docs.

---

## 4. Geography MCQ Question Bank — extracted from sourced exam PDFs (CONFIRMED)

**No AI-fabricated questions.** The practice bank is built from the **real
objective MCQs found in the sourced Geography exam papers**, tagged to the 12
topics (301–312):
- Each sourcing agent, while transcribing a paper, also writes every objective
  MCQ it finds to a **per-exam fragment** `geography_bank/_raw/<slug>.py`
  exposing `FRAGMENT=[{q,opts,ans,explain,topic_id}]` (avoids parallel-write
  races on shared topic files).
- A single **sequential build step** (`build_geography_bank.py`) aggregates all
  `_raw/*.py` fragments → `geography_bank/topic_<id>.py` grouped by `topic_id`,
  de-duplicated, each with `QUESTIONS` (+ `SUBTOPIC_RANGES` from the curriculum
  subtopics, evenly split).
- `seed_curriculum_geography.py` (clone of `seed_curriculum_chinese.py`,
  `subject="Geography"`, IDs 301–312) then seeds curriculum + the aggregated
  bank to local + Railway.
- Rules: authentic MCQs only; 4 options; one correct (from the paper's mark
  scheme); English explanation; no `$`/LaTeX; valid UTF-8 Python.

Bank size depends on the objective-MCQ yield of the freely-available papers
(authentic over synthetic, per the user's choice — the Chinese lesson:
surface a decision if yield is low rather than pad with junk).

---

## 5. Geography Exam Papers — source from the internet

Same pipeline as Science/Chinese:
- Source Sec 1 (or Lower Sec) Geography EOY/SA2 PDFs from freetestpaper.com /
  sgfreepapers / school sites. Geography papers are MCQ + structured/
  data-response — store full question (and source/figure reference) in
  `question_text`, model answer + marking points in `answer_text`.
- Parallel agents create `seed_<school>_geog.py` (pattern = `seed_queensway.py`,
  `subject="Geography"`, topic_id 301–312, **no KaTeX**, cropped images incl.
  maps/graphs, answer key from mark scheme). Process **one PDF fully before the
  next**, low-res page extraction (dpi≈110, ≤1600px).
- **Sourcing-availability risk (Chinese lesson):** if free Sec 1 Geography
  papers are scarce, we keep whatever we reliably get and rely on the 960-MCQ
  bank for coverage — flagged for a decision rather than padding with junk.
- Target **≥15 exams** (same bar as Science) — subject to availability.

---

## 6. API changes — minimal

- `ai_mark_answer`: add a `Geography` branch — English rubric (content
  accuracy, use of data/evidence/case studies, correct geographical
  terminology; score + feedback). Bedrock handles this natively.
- `ai_recognise_handwriting`: add a Geography branch → plain-English text
  recognition prompt (reuse the Chinese branch's "return plain text" path with
  an English instruction).

No schema or endpoint changes; `?subject=Geography` already works.

---

## 7. Frontend changes — small additions

1. **Portal** (`frontend/index.html`): add `'Geography'` to the group `order`
   array + a 4th subject toggle button `Geography` (extend active-state logic
   to 4 buttons). Listing already filters by selected subject.
2. **Practice app** (`practice/index.html`): add a 4th toggle button
   `Geography` calling `setSubject('Geography')`; extend active-state to 4
   buttons; extend the no-KaTeX preview/`renderMath` gate to include
   `'Geography'`.
3. No font change (English).

---

## 8. File manifest

| File | Action |
|---|---|
| `curriculum_geography.py` | new — 12 topics (IDs 301–312) |
| `geography_bank/topic_3NN.py` | new — ~80 MCQs/topic (parallel agents) |
| `seed_curriculum_geography.py` | new — clone of Chinese version |
| `seed_<school>_geog.py` | new per exam (parallel agents) |
| `GEOGRAPHY_SEED_GUIDE.md` | new — agent guide (no-KaTeX, topic map, low-res rule, ID-collision safety) |
| `practice_api.py` | Geography branch in `ai_mark_answer` + `ai_recognise_handwriting` |
| `frontend/index.html` | 4th subject toggle + 'Geography' in order |
| `practice/index.html` | 4th subject toggle + extend no-KaTeX preview gate |
| `STRUCTURE.md` | document 4-subject platform |

---

## 9. Execution order
1. `curriculum_geography.py` + `seed_curriculum_geography.py` + `build_geography_bank.py`
2. Frontend: 4th subject toggle (portal + practice) + preview gate
3. `ai_mark_answer` + `ai_recognise_handwriting` Geography branches
4. `GEOGRAPHY_SEED_GUIDE.md`; source ≥15 Sec 1 Geography PDFs → parallel agents
   → `seed_*_geog.py` + `geography_bank/_raw/<slug>.py` fragments
5. **Sequential**: `build_geography_bank.py` aggregates fragments →
   `geography_bank/topic_3NN.py`; seed curriculum+bank local + Railway
6. **Sequential reconciliation**: restore tracked `uploads/`, verify each
   Railway `exam_id` has a matching `uploads/{id}/`, commit only new dirs
7. Spot-check crops (esp. maps/graphs) vs question text
8. Commit + push → GitHub auto-deploy → verify live

---

## 10. Risks / mitigations (learned from Science + Chinese)
- **Exam-source scarcity**: confirm availability early; keep reliable yield,
  lean on the MCQ bank; surface a decision if < target (the Chinese outcome).
- **Cross-subject local-ID collision** (local agent IDs overwriting
  git-tracked Railway dirs): restore tracked `uploads/` from git, commit only
  new Railway-aligned dirs — the exact Chinese safeguard.
- **Parallel-agent races**: process batches, then sequential reconciliation.
- **Scanned-image size limit**: dpi≈110, downscale >1600px in the guide.
- **Map/graph crop fidelity**: Geography questions depend heavily on the
  figure — mandate visual crop verification against question text.
- **Cross-subject leak**: already fixed globally (subject filter always
  enforced) — Geography inherits the fix.

---

## Confirmations needed (same 3 as Science/Chinese)
1. **MCQ bank** → AI-generate via Claude agents (assumed yes, matches the
   other 3 subjects).
2. **Curriculum** → pre-seed the 12 proposed Sec 1 Geography topics above —
   confirm or adjust the list.
3. **Exam PDFs** → I source Sec 1 Geography papers from the internet, ≥15 if
   available (same as Science; with the Chinese-style fallback if scarce).

No changes to Math, Science or Chinese. Geography is fully isolated by
`subject`.
