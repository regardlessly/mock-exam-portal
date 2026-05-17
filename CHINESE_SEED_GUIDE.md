# Chinese (普通华文 / 华文) Exam Seed Guide — for processing agents

Follow the EXACT pattern of `seed_queensway.py`. This is the **Chinese G3
(Sec 1 普通华文 / 华文)** subject. Differences:

1. `Exam(... subject="Chinese" ...)` — MUST set subject to **"Chinese"**.
2. `topic_id` uses the **Chinese range 201–212** (NOT 1–14, NOT 101–114).
3. **NO KaTeX. NO `$`. NO LaTeX.** All `question_text`, `stem`, `answer_text`,
   `mark_scheme` are **pure CJK text**. Never wrap anything in `$`.
4. Target **试卷二 (Paper 2: 语文应用 + 阅读理解)** — it carries the
   objective/short-answer sections. Skip 试卷一 (作文 composition, open-ended)
   and 试卷三/四 (听力/口试). Use `paper_number=2`, but `paper_num=1` in the
   image filename prefix is fine (single paper per exam → keep `q1_<n>.png`).
5. Store the FULL question (passage + stem + options if MCQ) in
   `question_text`. For comprehension, put the passage in `stem` and the
   sub-question in `question_text`. Answer (model answer / correct option +
   brief Chinese reasoning) goes in `answer_text`. `mark_scheme="B1"` for
   objective MCQ; for short-answer use the marking points in Chinese.
6. Crop each question region into `uploads/{exam_id}/q1_<n>.png`.
7. Use the paper's 参考答案 / 评分标准 (answer key, usually at the end of the
   PDF or a separate answer file). If absent, infer from Chinese-language
   knowledge and note it.

## Chinese topic_id mapping (pick the closest per question)
- 201 汉语拼音与字音字形 (拼音、声调、多音字、形近字、错别字)
- 202 词语运用 (选词填空、近义词、反义词、语境用词)
- 203 词语搭配 (动宾/主谓/定中/固定搭配)
- 204 语法基础 (词类、句子成分、短语、词序)
- 205 病句辨析与修改
- 206 成语、谚语与惯用语 (成语、谚语、歇后语、惯用语)
- 207 标点符号
- 208 句子重组与改写 (句子重组、句式转换、扩写缩写、整理乱句)
- 209 综合填空 / 短文填空 (关联词、虚词、完形)
- 210 阅读理解（记叙文）
- 211 阅读理解（实用文/说明文）
- 212 实用文常识 (电邮、书信、便条、启事、通告格式)

Reuse an existing `schools` row if the school already exists (query by name
first); else create it. Idempotent re-seed scoped by school + year + subject
(see seed_queensway.py: filter on school_id AND year; also confirm subject so
a Math/Science exam for the same school+year is NOT deleted — add
`Exam.subject == "Chinese"` to the existing-exam query).

## Sourcing the PDF
Search these direct-PDF-host sites for **Secondary 1 华文 / 普通华文** papers
(EOY / SA2 / End-of-Year preferred; Paper 2 / 试卷二):
- freetestpaper.com  (e.g. /paper/Secondary/Chinese/...)
- sgexam / sgfreepapers / bestfreepapers Chinese Sec 1 listings
- thelearningspace.sg
Use WebSearch + WebFetch to locate a direct `.pdf` link, then download with
curl to `/Users/timmy/Downloads/sec1-papers/<slug>_chi.pdf`. Prefer real
school papers (named secondary schools). One PDF per school per year.

## CRITICAL: image size limit (lesson learned from Science)
These are large scans. Reading full pages at dpi=200 EXCEEDS the 2000px
many-image limit and the agent will fail. You MUST:
- Extract PREVIEW pages for transcription at **dpi≈110** to `/tmp/<slug>_lowres/`
- After saving each PNG, open with PIL; if width or height > **1600**, resize
  down (preserve aspect ratio) and re-save BEFORE reading it
- Read pages in small groups (3–4 at a time), **one PDF fully before the next**
- Cropped question images written via `crop_question_image()` may stay at
  dpi=200 (they are small crops, not full pages)

## Steps
1. Source + download ONE Sec 1 华文/普通华文 Paper-2 PDF.
2. Extract LOW-RES preview pages to `/tmp/<slug>_lowres/` at dpi≈110, downscale >1600px.
3. Read pages visually, transcribe questions (pure Chinese, NO `$`).
4. Create `seed_<slug>_chi.py` (pattern = seed_queensway.py, subject="Chinese",
   topic_id 201–212, paper_number=2, idempotent query includes
   `Exam.subject == "Chinese"`).
5. Run locally to verify:  `python3 seed_<slug>_chi.py`
6. Then seed Railway:
   `DATABASE_URL="postgresql://postgres:CLqaXXoZXOgKlrhyNfriZwsdMVxbBwzY@junction.proxy.rlwy.net:54125/railway" python3 seed_<slug>_chi.py`
7. Copy cropped `uploads/{local_exam_id}/q*.png` to
   `uploads/{railway_exam_id}/`, delete any `page_*.png`.
8. Do NOT git commit (the orchestrator handles commit + reconciliation).

## Quality bar
- Aim for the full Paper-2 question set per exam (typically 20–40 items).
- Verify each crop visually matches its `question_text` before finishing.
- Report: school name, year, local exam_id, Railway exam_id, #questions.
