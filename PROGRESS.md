# Progress

ALL COURSES DONE (local only: nothing pushed, published or committed). See NOTES.md for every decision, key disagreement and doubtful item.

| Course | Exams built | Terms | Notes |
|---|---|---|---|
| Math 208 | 36 | 221 to 261 (no 242 Final) | 221-e1/e2 have 4 written questions each |
| Math 201 | 35 | 221 to 261 | 222 majors not published (key tables only); 251 Major II has versions A and B |
| Math 102 | 34 | 221 to 261 (nothing for 242) | 9 figures |
| Math 101 | 30 | 221 to 251 (nothing newer published) | 2 figures |
| Stat 201 | 19 | STAT 201 251-252, STAT 319 222-243 | labelled "Originally STAT 319"; 27 images |

Total: 154 exams. Build everything: `python -I tools/build.py` (writes data/, pdf/, index.html). One course: `python -I tools/build.py <course>`.

## Checks used (all pass on every file)
- python -I tools/validate.py src/*/*.json. It checks the spec, plus: control characters, single backslashes before a digit, doubled backslashes outside environments, array column counts, choices that differ only in LaTeX formatting, and \llbracket.
- python -I tools/xcheck.py ../Ice_Math_OldExams_sources/<course> src/<course>/*.json (transcription vs the PDF text layer).
- PDFs: credit stamp on page 1 and on the "Answer Key" page; long keys are split over two pages.
- Site: checked with `python -I -m http.server 8765 --bind 127.0.0.1` plus headless Edge screenshots (the Chrome extension was not connected).

## Owner decisions (2026-10-28, applied)
1. Math 201 251 Major II: both versions are on the site (src/math201/251-e2.json = Version A, 251b-e2.json = Version B, built by the coordinator). Terms like "251b" need "version": "B"; the site shows "Version A/B".
2. Master-key disagreements were re-checked by recomputation and all hold; the official key wins (NOTES.md): math201 222-fx Q7, math102 232-fx Q20, math101 222-fx Q22, stat201 242-e2 Q3, stat201 233-fx Q16 (the key's 10.01 = 1400/139.86, an MSE typo for 138.86).
3. Missing questions are "omitted" placeholders ({"omitted": true, "q": "..."}), shown at the end of the exam with "omitted" in the key: math201 232-e1 Q10, math101 241-fx Q7-Q8, math101 242-e1 Q11.
Total now 154 exams.

## If something needs redoing
Sources: ../Ice_Math_OldExams_sources/<course>/<term>-<kind>.pdf. Rebuild one exam with the exam-builder agent (see .claude/agents/exam-builder.md), then validate, cross-check and build.
