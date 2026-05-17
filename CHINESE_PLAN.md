# Implementation Plan — Add Chinese G3 (普通华文 / Normal Chinese), Sec 1

## Goal
Add **Secondary 1 Normal Chinese (普通华文, G3)** as a third subject, using the
**exact same architecture** as Mathematics and Science. Math + Science stay
untouched; Chinese is additive, isolated by the existing `subject` discriminator.

The subject infrastructure already exists (built for Science): `subject` column
on `curriculum_topics`, `?subject=` filters on every API, portal grouping, and
the practice-app subject toggle. Adding Chinese is mostly **content + 3 small UI
strings**, not new architecture.

---

## 1. Reuse — what already works, no change needed

- `curriculum_topics.subject`, `exams.subject` columns ✅
- API `?subject=` filtering (topics, exams, filters, bank, curriculum) ✅
- Subject-scoped caching ✅
- Portal groups exams by subject; practice app has a subject toggle ✅
- GitHub → Railway auto-deploy pipeline ✅
- Per-exam seed-script pattern + parallel-agent PDF processing ✅

Topic ID ranges (no collisions): Math `1–14`, Science `101–114`,
**Chinese `201–2xx`**.

---

## 2. Chinese-specific differences vs Science (the real work)

| Concern | Science | Chinese — what changes |
|---|---|---|
| Notation | KaTeX math `$...$` | **None.** Pure CJK Unicode text. Must NOT wrap anything in `$`. |
| Fonts | default sans | Add a **CJK web font** (Noto Sans SC) so 汉字 render on all devices |
| Question types | MCQ | MCQ for objective sections; composition/comprehension = free-response |
| MCQ content | English | All `question_text` / options / explanations in **Chinese** |
| AI marking | English Sci prompt | **Chinese-language** marking prompt (作文/阅读理解 rubric) |
| Keyboard input | textarea + KaTeX preview | KaTeX preview irrelevant → make preview subject-aware (hide for Chinese) |
| Handwriting | Gemini math OCR | Gemini Chinese-character OCR (prompt tweak: "recognise handwritten Chinese") |

---

## 3. Sec 1 普通华文 (G3) Curriculum — pre-seed from MOE syllabus

~12 topics (IDs 201–212), the objectively-testable areas of the 普通华文 syllabus.
Semester split mirrors Math/Science.

**Semester 1**
- 201 汉语拼音与字音字形 (Hanyu Pinyin, sound & form of characters)
- 202 词语运用 (Word usage / 选词填空)
- 203 词语搭配 (Word collocation)
- 204 语法基础 (Basic grammar: 词类, 句子成分)
- 205 病句辨析与修改 (Identifying & correcting faulty sentences)
- 206 成语、谚语与惯用语 (Idioms, proverbs, common expressions)

**Semester 2**
- 207 标点符号 (Punctuation)
- 208 句子重组与改写 (Sentence reordering / rewriting)
- 209 综合填空 / 短文填空 (Cloze passage)
- 210 阅读理解（记叙文）(Comprehension — narrative)
- 211 阅读理解（实用文/说明文）(Comprehension — functional/expository)
- 212 实用文常识 (Functional writing conventions: 电邮/书信/启事)

Final topic list confirmed against the actual exam papers (same approach as
Math/Science — topics derived from what the papers test).

Deliverables: `curriculum_chinese.md`, `question_bank_chinese.md`.

---

## 4. Chinese MCQ Question Bank — AI-generated (Claude)

Same method as Science (`science_bank/` → `chinese_bank/`):
- Parallel agents generate **~80 MCQs per topic** (~960 total) as
  `chinese_bank/topic_<id>.py` with `QUESTIONS=[{q,opts,ans,explain}]` +
  `SUBTOPIC_RANGES`, all text in **Chinese**.
- `seed_curriculum_chinese.py` (clone of `seed_curriculum_science.py`,
  `subject="Chinese"`, IDs 201–212) seeds local + Railway.
- Generation rules: Singapore 普通华文 Sec 1 level; 4 options; one correct;
  explanation in Chinese; balanced A/B/C/D; no `$`/LaTeX; valid UTF-8 Python.

---

## 5. Chinese Exam Papers — source from the internet

Same pipeline as the 18 Science papers:
- Source Sec 1 华文/普通华文 EOY/SA2 PDFs from thelearningspace.sg /
  freetestpaper.com (direct-PDF host preferred, as used for Science).
- Target **试卷二 (Paper 2: 语文应用 + 阅读理解)** — it carries the MCQ +
  short-answer sections. (试卷一 = 作文 composition, free-response; 试卷三/四
  = 听力/口试, skip or note.)
- Parallel agents create `seed_<school>_chi.py` (pattern = `seed_queensway.py`,
  `subject="Chinese"`, topic_id 201–212, **no KaTeX**, cropped images, answer
  key from the mark scheme). Process **one PDF fully before the next**, low-res
  page extraction (dpi≈110, ≤1600px) — the lesson learned from Science scans.
- Aim for **≥15 exams** (same bar the user set for Science).

---

## 6. API changes — minimal

The API is already subject-generic. Only addition:
- AI marking (`ai_mark_answer`): branch on subject — for `Chinese`, use a
  Chinese marking prompt (评分标准: 内容、语言、结构; output score + 中文反馈).
  Bedrock/Gemini handle Chinese natively.

No schema or endpoint changes; `?subject=Chinese` already works.

---

## 7. Frontend changes — 3 small additions

1. **Portal** (`frontend/index.html`): add `'Chinese'` to the group `order`
   array → a "Chinese (华文)" section appears automatically.
2. **Practice app** (`practice/index.html`): add a third toggle button
   `华文 (Chinese)` calling `setSubject('Chinese')`; extend the active-state
   logic to 3 buttons.
3. **CJK font + preview**: add `Noto Sans SC` (Google Fonts) to both pages’
   font stack; make the keyboard-input KaTeX preview render only when
   `currentSubject !== 'Chinese'` (plain text otherwise).

---

## 8. File manifest

| File | Action |
|---|---|
| `curriculum_chinese.py` | new — 12 topics (IDs 201–212) |
| `chinese_bank/topic_2NN.py` | new — ~80 MCQs/topic (parallel agents) |
| `seed_curriculum_chinese.py` | new — clone of science version |
| `seed_<school>_chi.py` | new per exam (parallel agents) |
| `CHINESE_SEED_GUIDE.md` | new — agent guide (no-KaTeX, topic map, low-res rule) |
| `practice_api.py` | Chinese branch in `ai_mark_answer` only |
| `frontend/index.html` | add 'Chinese' to group order + CJK font |
| `practice/index.html` | 3rd subject toggle + CJK font + subject-aware preview |
| `curriculum_chinese.md`, `question_bank_chinese.md` | exported docs |
| `STRUCTURE.md` | document 3-subject platform |

---

## 9. Execution order

1. `curriculum_chinese.py` + `seed_curriculum_chinese.py`
2. Parallel agents → `chinese_bank/` (~960 MCQs) → seed both DBs
3. Frontend: 3rd subject toggle + CJK font + subject-aware preview
4. `ai_mark_answer` Chinese prompt branch
5. Source ≥15 Sec 1 华文 Paper-2 PDFs → parallel agents → `seed_*_chi.py`
6. Reconcile image dirs (sequential safety net — the Science race lesson)
7. Spot-check crops vs question text
8. Commit + push → GitHub auto-deploy → verify live

---

## 10. Risks / mitigations (learned from Science)

- **Parallel-agent races** (image-dir deletion / ID churn): process exam
  batches, then a **sequential reconciliation pass**; verify each `exam_id` has
  a matching `uploads/{id}/` before commit.
- **Scanned-image size limit**: mandate dpi≈110, downscale >1600px in the guide.
- **Cross-subject school_id leak**: already fixed globally (subject filter
  always enforced) — Chinese inherits the fix.
- **CJK rendering**: verify Chinese displays on the deployed site (font), not
  just locally.
- **Composition marking**: Paper 1 (作文) is open-ended; AI marking gives
  indicative scores + feedback, flagged as guidance not official.

---

## Confirmations needed (same 3 as Science)

1. **MCQ bank** → AI-generate via Claude agents (assumed yes, matches Science).
2. **Curriculum** → pre-seed from the MOE 普通华文 syllabus (12 topics above) —
   confirm or adjust the topic list.
3. **Exam PDFs** → I source Sec 1 华文 Paper-2 papers from the internet
   (thelearningspace/freetestpaper), ≥15, same as Science.

No changes to Math or Science. Chinese is fully isolated by `subject`.
