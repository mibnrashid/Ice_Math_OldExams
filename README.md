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
```

- **Site:** one static `index.html` (vanilla JavaScript, no framework), with MathJax 3 for the maths.
  No server needed, so it runs on GitHub Pages.
- **PDFs:** generated with pdfLaTeX (TinyTeX); PyMuPDF adds the credit line.
- **Content:** the exams were transcribed from the official master PDFs on the
  [KFUPM Mathematics exam page](https://math.kfupm.edu.sa/miscellaneous/exam), and every answer was
  re-solved and verified in Python (SymPy). The official key is always used. Where the official key
  looks wrong, or a question was missing from the published file, it is documented in [NOTES.md](NOTES.md).

Rebuild everything:

```
python -I tools/validate.py src/*/*.json
python -I tools/build.py
```

## Found a mistake?

Please open an issue: https://github.com/mibnrashid/Ice_Math_OldExams/issues
