# Geography Exam Seed Guide — for processing agents

Follow the EXACT pattern of `seed_queensway.py`. This is the **Geography G3
(Sec 1 / Lower Secondary)** subject. Differences:

1. `Exam(... subject="Geography" ...)` — MUST set subject to **"Geography"**.
2. `topic_id` uses the **Geography range 301–312** (NOT 1–14 / 101–114 / 201–212).
3. **NO KaTeX. NO `$`. NO LaTeX.** Plain English text everywhere.
4. Geography papers = MCQ section + structured / data-response / source-based.
   - Store the FULL question in `question_text` (include any
     "Study Figure X / Source A" reference). Put a shared passage/source in
     `stem` if several parts use it.
   - Model answer + marking points → `answer_text`. `mark_scheme="B1"` for MCQ;
     for structured, the marking points in plain English.
5. Crop each question region (INCLUDING its map / graph / photo / source) into
   `uploads/{exam_id}/q{paper_num}_{n}.png` via `crop_question_image()`. Crop
   fidelity matters — Geography answers depend on the figure.
6. Use the paper's mark scheme / answer key for correct MCQ options. If absent,
   infer from Geography knowledge and note it.

## Geography topic_id mapping (pick the closest per question)
- 301 Geographical Skills: Maps & Map Reading (grid refs, scale, distance, direction, symbols)
- 302 Geographical Skills: Relief, Photographs & GIS (contours, cross-sections, photos, GIS)
- 303 Weather & Climate: Elements & Instruments (weather elements, instruments, Stevenson screen)
- 304 Factors Affecting Temperature & Rainfall (latitude, altitude, rainfall types)
- 305 Climate Graphs & Data Interpretation
- 306 The Water Cycle & Drainage Basins
- 307 Rivers & River Landforms
- 308 Water Resources & Management (incl. Singapore's Four National Taps)
- 309 Tropical Rainforest Ecosystems
- 310 Variable Weather & Climate Change
- 311 Natural Vegetation & Biomes
- 312 Tourism & Sustainable Development

Reuse an existing `schools` row if the school already exists (query by name
first); else create it. Idempotent re-seed scoped by school + year + subject:
the existing-exam query MUST include `Exam.subject == "Geography"` so a
Math/Science/Chinese exam for the same school+year is NOT deleted.

## Sourcing the PDF
Search for **Secondary 1 / Lower Secondary Geography** papers (EOY / SA2 / End-
of-Year; Express / G3). Try:
- freetestpaper.com (Secondary → Geography / Humanities)
- sgfreepapers.com, testpapersfree.com, bestfreepapers.com, sgexam
- school .moe.edu.sg sites
Use WebSearch + WebFetch to locate a direct `.pdf` link, then download with
curl to `/Users/timmy/Downloads/sec1-papers/<slug>_geog.pdf`. Prefer real
named-school papers. One PDF per school per year.

## DUAL OUTPUT per exam — seed file AND bank fragment
For EACH exam you process, produce TWO things:

**(a) `seed_<slug>_geog.py`** — full exam (all questions, crops), pattern =
`seed_queensway.py`, `subject="Geography"`, `paper_number` as on the paper.

**(b) `geography_bank/_raw/<slug>.py`** — every OBJECTIVE MCQ found in that
paper, for the practice bank. Exact format:

```python
FRAGMENT = [
    {"q": "Full question text (include any figure description in words)",
     "opts": ["option A", "option B", "option C", "option D"],
     "ans": 0,                # 0-based index of the correct option
     "explain": "one-line reason from the mark scheme / knowledge",
     "topic_id": 301},        # 301-312, closest topic
    ...
]
```
Only real MCQs from the paper — do NOT invent questions. If an MCQ depends
entirely on an un-transcribable figure, skip it from the fragment (it still
lives in the exam seed with its crop). A single sequential builder
(`build_geography_bank.py`, run later by the orchestrator) aggregates all
`_raw/*.py` into `geography_bank/topic_3NN.py` — so DO NOT write
`geography_bank/topic_*.py` yourself.

## CRITICAL: image size limit (lesson from Science/Chinese)
Large scans. Reading full pages at dpi=200 EXCEEDS the 2000px many-image limit
and the agent will fail. You MUST:
- Extract PREVIEW pages for transcription at **dpi≈110** to `/tmp/<slug>_lowres/`
- After saving each PNG, open with PIL; if width or height > **1600**, resize
  down (preserve aspect ratio) and re-save BEFORE reading it
- Read pages in small groups (3–4 at a time), **one PDF fully before the next**
- Cropped question images via `crop_question_image()` may stay at dpi=200

## CRITICAL: cross-subject ID-collision safety (lesson from Chinese)
The `uploads/{exam_id}/` dir is keyed by exam id. Local exam ids you create
may collide with git-tracked dirs that serve LIVE Railway exams of other
subjects. Therefore:
- Do NOT `git commit`. Do NOT delete other agents' `uploads/` dirs.
- After local seed, also seed Railway and copy crops to the **Railway** exam
  dir; the orchestrator runs a sequential reconciliation
  (`git checkout -- uploads/`, then commit only the new Railway-aligned dirs).

## Steps (per exam, one PDF fully before the next)
1. Source + download ONE Sec 1 Geography PDF.
2. Extract LOW-RES pages to `/tmp/<slug>_lowres/` at dpi≈110, downscale >1600px.
3. Read pages visually, transcribe questions (plain English, NO `$`).
4. Create `seed_<slug>_geog.py` (subject="Geography", topic_id 301–312,
   idempotent query includes `Exam.subject == "Geography"`).
5. Create `geography_bank/_raw/<slug>.py` with the FRAGMENT list of real MCQs.
6. Run locally:  `python3 seed_<slug>_geog.py`
7. Seed Railway:
   `DATABASE_URL="postgresql://postgres:CLqaXXoZXOgKlrhyNfriZwsdMVxbBwzY@junction.proxy.rlwy.net:54125/railway" python3 seed_<slug>_geog.py`
8. Copy `uploads/{local_exam_id}/q*.png` → `uploads/{railway_exam_id}/`,
   delete any `page_*.png`.

## Report
Per exam: school, year, source URL, local exam_id, Railway exam_id,
#questions seeded, #MCQs in the bank fragment, seed filename.
