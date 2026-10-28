# Ice Math Old Exams Archive (Unofficial)

**Live site: https://mibnrashid.github.io/Ice_Math_OldExams/**

A practice archive of KFUPM old exams for **Math 101, Math 102, Math 201, Math 208 and Stat 201**
(including the old Stat 319 exams), from term 221 up to the latest term (261).
It is a student effort and not official.

Students can solve an exam in the browser without seeing the answers. Each question has three
hints that open one at a time (the idea, the first move, the key formula), then a check of the
answer and a step-by-step solution that uses only methods from the course syllabus. Every exam can
also be downloaded as a PDF with an answer key.

- 154 exams (Major Exam I, Major Exam II and Final for each term that has them)
- Questions and choices are shuffled once, with a fixed seed, so the website and the PDF use the same order
- Progress is saved in the browser
- The home page highlights the exam that is coming up next (Major I, Major II or Final), based on past exam dates

## How it is built

```
src/<course>/<term>-<kind>.json   one exam per file: questions, choices, key, hints, steps (format: tools/SPEC.md)
tools/validate.py                 checks every exam file against the spec
tools/build.py                    shuffles each exam, writes data/*.js and index.html, builds the PDFs
tools/xcheck.py                   compares each transcription with the text of its source PDF
tools/mjtest.html                 renders every string on the site with MathJax and reports TeX errors
tools/find_new_exams.py           lists (and downloads) exams on the KFUPM page that are not built yet
```

- **Site:** one static `index.html` (vanilla JavaScript, no framework), with MathJax 3 for the maths.
  No server needed, so it runs on GitHub Pages.
- **PDFs:** generated with pdfLaTeX (TinyTeX); PyMuPDF adds the credit line.
- **Content:** the exams were transcribed from the official master PDFs on the
  [KFUPM Mathematics exam page](https://math.kfupm.edu.sa/miscellaneous/exam), and every answer was
  re-solved and verified in Python (SymPy). The official key is always used. Where the official key
  looks wrong, or a question was missing from the published file, it is documented in [NOTES.md](NOTES.md).

## How to update and how it works

### How to update

When KFUPM publishes new old exams:

1. Open this folder in Claude Code and type `/update-old-exams` (or say "check for new old exams").
2. Wait for the report. It lists the new exams it added and anything doubtful (for example an official
   key that looks wrong).
3. Look at the new exam on the local preview if you like, then commit and push yourself. The skill never
   commits or pushes.

To only check what is new, without Claude:

```
python -I tools/find_new_exams.py              # list exams on the KFUPM page that are not built yet
python -I tools/find_new_exams.py --download   # also download their PDFs to ../Ice_Math_OldExams_sources/
```

To rebuild everything by hand:

```
python -I tools/validate.py src/*/*.json
python -I tools/build.py
```

### How it works

The update is a pipeline. Scripts do the mechanical parts; Claude only does the part that needs judgement
(reading and solving an exam).

1. **Find** (script, no AI): `tools/find_new_exams.py` reads the KFUPM exam page, turns every link into
   course, term and kind (Major I = `e1`, Major II = `e2`, Final = `fx`; Stat 319 counts as Stat 201), and
   compares that with the files in `src/`. Exams we deliberately skip are listed with a reason in
   `tools/known_skips.json`, so they are not reported again.
2. **Download** (script): the new PDFs go to `../Ice_Math_OldExams_sources/<course>/`, outside the repo.
3. **Build the exam** (Claude, following `.claude/skills/update-old-exams/SKILL.md`): Claude reads each page
   as an image, transcribes the master version, solves and verifies every answer in Python, writes the
   hints and the step-by-step solution, and saves one JSON file per exam in `src/<course>/`. The format
   and rules are in `tools/SPEC.md`.
4. **Check** (scripts): `tools/validate.py` checks the JSON (format, LaTeX that would break, duplicate
   choices, table columns); `tools/xcheck.py` compares the transcription with the PDF text;
   `tools/mjtest.html` renders every string on the site and reports maths errors.
5. **Build** (script): `tools/build.py` shuffles each exam once with a fixed seed, writes the site data
   (`data/`), `index.html` and the PDFs (`pdf/`). The website and the PDF always use the same order.
6. **Record**: the skill adds what changed to `NOTES.md` and updates the counts in this README and
   `PROGRESS.md`. Then you commit and push.

The skill works in the main Claude session and does not start subagents unless you ask for them in your
request, because they cost a lot of usage.

## Found a mistake?

Please open an issue: https://github.com/mibnrashid/Ice_Math_OldExams/issues
