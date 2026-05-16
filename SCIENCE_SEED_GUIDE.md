# Science Exam Seed Guide (for processing agents)

Follow the EXACT pattern of `seed_queensway.py`. Differences for Science:

1. `Exam(... subject="Science" ...)` — MUST set subject to "Science"
2. `topic_id` uses the Science range below (NOT 1-14)
3. These are MCQ papers (scanned image PDFs). Read page images visually with the
   Read tool. Each question is typically multiple-choice (options A-D). Store the
   full question (incl. options) in `question_text`, and the answer (e.g. "C" with
   brief reasoning) in `answer_text`. Use `mark_scheme="B1"` for MCQ.
4. Plain text / KaTeX `$...$` for any formula; `$\$...$` for dollars (rare in Science).
5. Crop each question region into `uploads/{exam_id}/q1_<n>.png` (single paper → paper_num=1).
6. Many Science papers have an answer key near the end — use it. If no key, infer
   the correct MCQ option from subject knowledge and note it.

## Science topic_id mapping
- 101 Introduction to Science & the Laboratory (apparatus, safety, scientific method)
- 102 Physical Quantities, Units & Measurement (SI units, length/volume/mass/time, density)
- 103 Particulate Nature of Matter (states, kinetic theory, changes of state, diffusion)
- 104 Elements, Compounds & Mixtures (atoms, molecules, symbols)
- 105 Separation Techniques (filtration, distillation, chromatography)
- 106 Solutions & Solubility (solute/solvent, saturation)
- 107 Cells — The Basic Unit of Life (microscope, plant/animal cells, organisation)
- 108 Movement of Substances (diffusion, osmosis, SA:V)
- 109 Human Digestive System (nutrients, enzymes, organs, absorption, diet)
- 110 Transport in Living Things (heart, blood, transport in plants)
- 111 Energy (forms, conversions, conservation, energy sources)
- 112 Forces (types, effects, friction, mass/weight, springs)
- 113 Electrical Systems (circuits, current, conductors, series/parallel)
- 114 Ray Model of Light (light, reflection, refraction, the eye)

Pick the closest topic_id per question. Reuse an existing `schools` row if the
school already exists (query by name first); else create it.

## CRITICAL: image size limit
These PDFs are large scans. Reading full pages at dpi=200 EXCEEDS the 2000px
many-image limit and the agent will fail. You MUST:
- Extract PREVIEW pages for transcription at dpi=110 to /tmp/<slug>_lowres/
- After saving each PNG, open with PIL; if width or height > 1600, resize down
  (preserve aspect ratio) and re-save BEFORE reading it
- Read pages in small groups (3-4 at a time), one PDF fully before the next
- The cropped question images written to uploads/{exam_id}/ via
  crop_question_image() may stay at dpi=200 (they are small crops, not full pages)

## Steps
1. Extract LOW-RES preview pages to /tmp/<slug>_lowres/ at dpi=110, downscale >1600px
2. Read pages visually, transcribe MCQs
3. Create seed_<slug>_sci.py (pattern = seed_queensway.py, subject="Science")
4. Run locally to verify, then against Railway:
   DATABASE_URL="postgresql://postgres:CLqaXXoZXOgKlrhyNfriZwsdMVxbBwzY@junction.proxy.rlwy.net:54125/railway"
5. Copy cropped q*.png to uploads/{railway_exam_id}/, delete page_*.png
6. Do NOT git commit
