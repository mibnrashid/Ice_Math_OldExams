---
name: update-old-exams
description: Check the KFUPM Mathematics exam page for old exams that are not on the Ice Math Old Exams site yet (Math 101, 102, 201, 208, Stat 201 incl. old Stat 319), then download, build, verify and publish them locally. Use when the owner asks to update, add new old exams, or "check for new exams".
---

# Update the archive with new old exams

Work in the main session. Do NOT start subagents unless the owner asks for them in this request (they cost a lot of usage).
Never commit, push or deploy: the owner does that.

## 1. Find what is new

```
python -I tools/find_new_exams.py
```

It reads https://math.kfupm.edu.sa/miscellaneous/exam and prints every exam (term >= 221) that has no
`src/<course>/<term>-<kind>.json` and is not in `tools/known_skips.json`.
- Nothing new: tell the owner and stop.
- Otherwise show the list and continue (newest first). For many exams (more than ~4), say how many and
  that each takes a while, and suggest doing a few now.

Download them:
```
python -I tools/find_new_exams.py --download
```
PDFs go to `../Ice_Math_OldExams_sources/<course>/<term>-<kind>.pdf` (never into the repo).
Check each one opens with PyMuPDF and its page header shows the right course, term and kind.

Special cases:
- A file with only an answer-key table (no questions): add it to `tools/known_skips.json` with the reason; do not build.
- Two different exams for the same term/kind (files like `math201a-` and `math201b-`): the second one is
  term `<term>b` with `"version": "B"`, and the first gets `"version": "A"` (tools/SPEC.md).
- A STAT 319 file belongs to `stat201`; set `"source"` to the original file name (it starts with `stat319`), so
  the site labels it "Originally STAT 319".
- A new term whose syllabus is not in `tools/syllabus/<course>.md`: the existing file is fine for section labels
  (older/newer questions keep their textbook section). Only update it if the owner asks.

## 2. Build each new exam (one at a time)

Follow the exam rules in `.claude/agents/exam-builder.md` and the format in `tools/SPEC.md` exactly. In short:
- Render every page with PyMuPDF (~170 dpi, zoom 250 dpi on unclear maths) and READ the images. The text
  layer drops minus signs, complement bars and primes; scans may have no text at all. Transcribe only printed
  text, never handwriting. Use the MASTER pages.
- `"source"` = the published file name exactly as `find_new_exams.py` printed it (keep any GUID suffix).
- The official key always wins. If it looks wrong, recheck hard; if it still looks wrong, keep the key, explain
  in the last step, and add a `note`. No marked key: solve it yourself (the master convention puts the answer
  at (a)), and say "no official key; answers derived and verified" in the top-level `note`.
- Verify every answer in Python (sympy / math / statistics; scipy may be missing) from a script FILE in the
  scratchpad. Never put LaTeX in a bash heredoc or `python -c`: backslashes get halved.
- Hints: H1 the idea, H2 the first move (no numbers), H3 the general formula/fact (never this problem's numbers).
  Steps use only methods from `tools/syllabus/<course>.md`. Out-of-syllabus questions stay in and are solved normally.
- Figures needed by a question: crop only the printed figure (~200 dpi) to `src/<course>/img/<course>-<term>-<kind>-q<N>.png`
  and set `"img"`. Handwriting over it: `python -I tools/decolor.py in.png out.png 15`, then LOOK at the result
  (it also removes printed colour). Data tables: LaTeX `array` (enough columns; no `\multicolumn`).
- Shared stems (one data set for several questions): repeat the stem in each question (questions are shuffled).
- Written questions (no printed choices): `"written": true` + `"answer"`. Missing question in the source:
  `{"omitted": true, "q": "Question N of the original exam is omitted (...)."}`. Identical printed choices: keep one.
- Date: from the cover; never guess (`""` if not printed). Minutes: printed, else 90 (major) / 120 (final).
- Write the JSON with a script file, then: `python -I tools/validate.py src/<course>/<file>.json` until OK.

## 3. Check

```
python -I tools/validate.py src/*/*.json
python -I tools/xcheck.py ../Ice_Math_OldExams_sources/<course> src/<course>/<term>-<kind>.json
```
xcheck compares the transcription with the PDF text (scores below ~0.8 are usually LaTeX words; a wrong term or
many very low scores means a problem). Hand-check 2-3 answers and the hardest question yourself, and look at
every cropped image.

## 4. Build and verify

```
python -I tools/build.py <course>
```
Then serve the repo (`python -I -m http.server 8765 --bind 127.0.0.1`, in the background) and:
- open `http://127.0.0.1:8765/tools/mjtest.html` (headless Edge `--dump-dom` works) and confirm
  "problems 0": it renders every string on the site with MathJax;
- open the new exam page and its PDF once (title, question count, figures, answer key);
- stop the server when done.

The home page highlights the next exam kind from the exam dates automatically; nothing to change.

## 5. Record and report

- Add a short entry to NOTES.md (what was added, key disagreements, no-key exams, omitted questions,
  anything doubtful) and update the counts in PROGRESS.md and README.md (number of exams, latest term).
- Tell the owner: which exams were added, any key disagreements or doubtful items, and that it is ready for
  them to commit and push.
