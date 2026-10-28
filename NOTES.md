# Notes: decisions, questions, problems

## Decisions confirmed by the owner (2026-10-28, before the overnight run)
- Figures/graphs/tables needed by a question: crop from the source PDF into `src/<course>/img/` and use the `img` field (already supported by SPEC, build.py and the template).
- Master-key disagreement: the official key always wins. The disagreement is recorded in the question's `note` and listed here.
- Stat written / show-your-work parts: add a written question type (no choices; hints, then "Show answer" reveals the answer and steps; in the PDF, a question with space and the answer in the key). To be implemented when Stat 201 starts, without changing the Math 208 output.
- Exams with no master key: include them, solved and verified by us, with "no official key" in the top-level `note` and listed here.

## Coordinator decisions
- 233-e1, 233-fx and 251-e2 (unverified, written by cut-off agents) were moved to the session scratchpad as backup and are rebuilt from scratch.

- Wave 1: the 243-fx agent wrongly reported that its PDF mixed pages from 241/233/252. Page-text extraction shows a clean 243 Final MASTER (cover plus 11 pages, Q1-Q20). The agent was rerun with the page map. Lesson: before accepting a "bad source" report, check it with a PyMuPDF text dump.

- Cause of the 243-fx mistake: the builders rendered pages into a shared scratch folder with the same file names, so agents saw other exams' pages. .claude/agents/exam-builder.md now requires a fresh per-exam scratch folder and a header check on every page.
- Spec change (does not affect existing output): `"date": ""` is now allowed when the date is not printed (it needs a top-level note). The PDF prints "Original exam date: not printed." and the site leaves the date out. Agents must never guess a date. 233-e1 and 233-e2 have no cover page, so their dates are now empty (the agents had guessed). Minutes are assumed: 90 for a major, 120 for a final.
- validate.py now rejects control characters in strings (an eaten backslash, e.g. `\b` in `\begin`, which happened while I edited 251-e2 by hand).
- Coordinator cross-check (scratchpad xcheck.py): for each exam with a text layer, the words of every JSON question are compared with its own source PDF. All Math 208 files pass. Partial matches come only from LaTeX words.
- 232-e1 Q17: the agent set `lock` without a reason; removed so the choices shuffle.

- Wave 2: 232-fx, 231-fx and 223-fx have 28 questions (older finals). Counts were confirmed against the page layout or the answer-key table. 223-e1 and 223-e2 have 14 questions (confirmed by the key table). No cover (date "" with assumed minutes): 223-e1, 223-e2, 223-fx, 232-e2, 232-fx. 231-fx is 180 minutes (printed).
- 2026-10-28 (owner present, on request): added CLAUDE_CODE_SUBAGENT_MODEL=sonnet to the user-level ~/.claude/settings.json, so built-in subagents (general-purpose and others) no longer inherit Opus in any project. Later, on request, added .claude/agents/course-setup.md (model: haiku) for each course's setup step. The setup step uses it instead of general-purpose.

- SPEC CHANGE, written questions (approved type, implemented early because Math 208 221-e1 and 221-e2 have written Q9-Q12 worth 11 points each): `"written": true` plus `"answer"`, with no opts/ans. build.py puts written questions after the MCQs (shuffled among themselves); exams without written questions keep exactly the same shuffle. The PDF leaves 150pt of working space and the key shows "written" plus the brief. The site shows no choices and "Show answer" gives "Answer: ..." plus the steps; written questions count as answered but never as correct. Checked: all 30 earlier exams produce identical site data, and the 261-e1 PDF text is identical. SPEC.md, validate.py, build.py, the template and exam-builder.md are updated.
- 221-e1: the first run turned the written Q9-Q12 into MCQs with invented distractors (rejected). 221-e2: the first run left them out. Both were sent back to convert or add them as written questions.

## Math 201
- Setup (Sonnet general-purpose agent, since course-setup.md isn't loaded in this session): 36 PDFs downloaded to ../Ice_Math_OldExams_sources/math201/; tools/syllabus/math201.md written from syl261.pdf. All exams are pure MCQ, and no figures are needed (graph questions give equations).
- Not published: 261 Major II and Final (not yet), 231 Final (none listed).
- Skipped: 222 Major I and Major II. The site has only one-page answer-key tables, with no questions.
- 251 Major II has two different exams (math201a-251-e2.pdf and math201b-251-e2.pdf, same date, both MASTER), probably two sessions. The site has one slot per term and kind, so version "a" is used as 251-e2 and "b" (saved as 251-e2b.pdf) is not included. QUESTION FOR OWNER: add "b" as an extra entry? That would need a small route/kind change.
- 252-e2 page 10 is an appended explanation of Q8 (not a question).
- Plan: 34 exams.
- Wave A (all verified): 261-e1, 253-e1, 253-e2, 253-fx (21 questions), 252-e1, 252-e2, 252-fx (21 questions; "source" corrected to the GUID file name), 251-e1. No key disagreements.
  - No cover (date "", minutes assumed): 261-e1, 253-e1, 253-e2, 253-fx, 252-fx.
  - 251-e1: no marked key (derived; first choice correct throughout). Q13 (9 polar intersection points) re-checked numerically by me.
  - 252-e2 Q8: the key "does not exist" rests on the domain x>0, y>0 containing no disk around the origin; along the domain the value would be 0 (noted, key kept). Q5/Q11/Q15 are 13.7 on an Exam II (older coverage, kept).
  - Unneeded `lock` removed from 252-e2 Q8 and 252-e1 Q3 (the exam-builder prompt now states when lock is allowed).
  - Later exams verified: 251-e2 (version "a"), 251-fx (21), 243-e1, 243-e2, 243-fx, 242-e1, 242-e2, 242-fx, 241-e1, 241-e2, 241-fx, 233-e1. No key disagreements.
  - 243-fx Q10: the key 11/2 is the minimum on the x>0 branch (f is unbounded below for x<0); key kept. 241-fx Q2: the key 3 counts the pole as an intersection point.
  - 242-e1 Q10: the handwritten solution on the scan says -8/sqrt65, but the printed key -8/65 is correct (checked).
  - Also verified: 233-e2, 233-fx, 232-e1, 232-e2 (20), 231-e1 (20; no marked key, derived; first choice correct throughout).
  - 232-e1: Q10 is MISSING from the published scan (page 5 has only Q9, page 6 starts at Q11; checked visually). 19 questions are kept; the original numbering is noted.
  - Hand-checked by me (more): 233-e2 Q12, 232-fx Q5, 223-e1 Q7/Q8 (visual), 223-e2 Q11/Q12 (visual), 223-fx Q19/Q20 (visual), 221-e1 Q8.
  - Also verified: 232-fx (28), 231-e2 (20), 223-e1 (20), 223-e2 (20), 223-fx (28), 222-fx (28), 221-e1 (20), 221-e2 (20; no marked key, but the handwritten worked solutions and sympy agree).
  - Unneeded `lock` removed from 223-e1 Q20 and 221-e2 Q5.
  - 231-e2 Q18: statement (II) calls the x=0 trace an ellipse, but it is a single point; the key counts it as true (kept).
  - 223-fx Q15 choice (e) is printed with odd limits (kept as printed).
  - KEY DISAGREEMENT, math201 222-fx Q7: the tangent plane to z=2x-y^2 at (2,1,3) is z=2x-2y+1, and NONE of the five printed points lies on it (I checked the scan; the transcription is exact). Flawed question. The official key (-1,-2,-3) is kept, and the steps tell the student the printed data and the key don't agree.
  - Hand-checked by me: 251-e2 Q6, 243-e2 Q6, 242-fx Q6 and Q10, 233-e1 Q15, 243-fx Q10.
  - BUG FOUND AND FIXED: 243-e2 Q11 and 253-e2 Q14 started with "\\lim" (a LaTeX line break followed by "lim"). validate.py now rejects a doubled backslash outside matrix/aligned/cases environments, and exam-builder.md says to write the JSON from a script file (bash heredocs halve backslashes).
  - 253-e2 Q4: a stray handwritten mark sits next to (b); the printed key (a) is correct (checked: sqrt14/28).

- Math 201 DONE: all 34 exams validated, cross-checked and built (site data and 34 PDFs). Checked: the Final term list and the 252-e2 exam page in headless Edge, and the 222-fx and 251-e1 PDFs. Last item: 221-fx (28; no marked key, derived; first choice correct throughout).

## Math 102
- Setup: 34 exams (261-e1, plus 253 down to 221 with all three kinds; 242 has nothing published). All MCQ. Not built: the 232 lab and 231 recitation midterms (not lecture exams). No marked key: 241-fx, 232-e1.
- 261-e1: figures for Q1 and Q4 are cropped into src/math102/img/. The Q4 crop had the solver's coloured handwriting (A1/A2 and a line at x=4); I removed it with the new tools/decolor.py, which whitens coloured pixels because the print is grayscale. The Q13 and Q14 sketches on the scan are handwritten solution work, so they are not used; the questions are complete in text. Hand-checked Q1 (upper sum 16) and Q4 (-2).
- KEY DISAGREEMENT, math102 232-fx Q20: the sum of (-1)^n/(2n^3-1) from n=0, with error < 0.01. The scan really prints n=0 (I checked). Then 3 terms leave a bound of 1/53, about 0.019, so 4 terms are needed. The key's 3 matches a series starting at n=1. Key kept, with a note on the question.
- math102 221-e1 Q7 (loose question): the exact concave-up interval is (1/sqrt3, inf), which is not a choice; the key (1, inf) is the only choice inside it (checked). Key kept, with a note.
- math102 222-e1 Q6: decolor faded the tick labels, so the agent white-boxed the handwriting instead (two white patches and one small dot remain; the graph is complete). Answer 5/2-2pi checked.
- math102 223-e1 Q5: the key (1/2)sec^2 x vs the computed (1/2)tan^2 x differ by a constant (explained in the steps). Q16 = 3 checked.
- Math 102 DONE: 34 exams built, with 9 figures (261-e1 Q1/Q4, 231-e1 Q6/Q17, 223-e1 Q2/Q16, 223-fx Q15/Q24, 222-e1 Q6), all embedded in the PDFs and shown on the site. Key disagreements: only 232-fx Q20 (see above). No-key exams (derived): 241-fx, 232-e1.
- 221-e2: handwritten work on the scan uses sqrt(4-x^2) in Q3 and +ln|sec x| in Q6, but the printed text and the key are consistent (Q3 = 16/3 - 7sqrt5/3, checked with sympy).
- CAUTION: tools/decolor.py whitens ALL coloured pixels. Some printed figures use colour (math102 231-e1 Q17 has a blue printed line), so use decolor only when handwriting overlaps, and look at the result.
- Hand-checked figure questions: 231-e1 Q6 (3-2pi) and Q17 (area 2). Also 233-fx Q17/Q18 and 232-e2 Q7 (scan exponent), 241-fx Q7/Q13/Q19 and 232-e1 Q7/Q17 (no-key exams), 233-e1 Q10 (limits printed 3 to sqrt3; -pi/18 matches).
- 253-fx: the agent assumed 180 minutes; set to 120 (the rule; the 252 Final prints 120).
- 252-fx Q1/Q2/Q4: the original prints only the integral or sum (no verb); "Evaluate"/"Find the sum" was added. Answers hand-checked.

## Math 101
- Setup: 30 exams for terms 221 to 251. The site lists no Math 101 exams for 252, 253 or 261 (nothing to build). All MCQ.
- 233-e2: the file is a template master with no "(correct)" marks and no key table; it is included and solved by us (owner's rule for no-key exams).
- 242-e1: Q11 is struck out and marked "Omitted" on the master, so it is left out (13 questions). Q1 needs its printed graph (cropped).
- math101 241-fx: printed page 4 of 10 (Q7, Q8) is MISSING from the published scan (checked: the pages read 1, 2, 3, 5, 6, ...). 18 questions are kept.
- math101 233-fx Q9: the key -9 relies on the antiderivative -2ln|x| + ... being used for x < 0 (intended reading, noted).
- math101 232-fx Q24: (b) and (e) print identically. The agent had written them in two LaTeX forms to pass the duplicate check (both would look the same to students); I dropped (e), so 4 choices. The answer (a) is unchanged. Future prompts say: never disguise duplicates.
- math101 221-e1 Q11 (borderline): at x=1 the tangent to x^3+4 IS the line 3x-y+2=0 (coincident, not strictly parallel); the key counts 2 points. Kept. Q2 and Q18 are epsilon-delta (outside the 261 syllabus, kept).
- math101 222-e1 Q11: checked on the scan, the root covers 2x only (sqrt(2x) - 4), matching the key 1/sqrt(2x). Q8 is epsilon-delta (kept).
- math101 231-fx Q22: a printed figure was cropped; the handwritten x/y labels were blanked (faint ghosts remain).
- KEY DISAGREEMENT, math101 222-fx Q22: "using differentials, the estimate of the INCREASE of the area" as r goes from 10 to 10.1 is dA = 2pi, but the key is 102pi (the estimated new area). No choice equals 2pi. Key kept; the steps explain it.
- math101 222-fx Q23: (b) and (d) are both printed e^{-pi}. The agent had replaced (d) with an invented e^{-pi/2}; I dropped (d) instead (4 choices).
- math101 221-e2 Q14: borderline wording ("always true"); key kept (noted by the agent).
- BUILD FIX: three Math 101 files used \llbracket/\rrbracket (not in amssymb), which broke pdfLaTeX; replaced with \lfloor/\rfloor, and validate.py now bans them.
- Math 101 DONE: 30 exams built (figures in 242-e1 Q1 and 231-fx Q22). Key disagreements: only 222-fx Q22. Missing questions in the sources: 241-fx Q7-Q8 (page not published) and 242-e1 Q11 (omitted on the master). No-key exam (derived): 233-e2.
- validate.py now also rejects choices that differ only in LaTeX formatting (normalised comparison). All existing exams pass.
- The greatest-integer bracket (double brackets on the exams) is written as \lfloor x\rfloor (251-e1 uses [\![x]\!], which also renders).
- Hand-checked: 242-e1 Q1 (figure), 251-e1 Q7/Q8 (scan with no text), 242-e2 Q14, 241-e2 Q14 (c=e-1), 233-e2 Q8/Q11 (no-key exam), 242-fx Q3/Q17. 242-e2: "Roll's" fixed to "Rolle's". 243-fx Q7 (cosh derivative) is slightly beyond 5.9 Example 3 and kept.
- Fixed tools/syllabus/math102.md: section 5.6 is "indeterminate forms and L'Hopital's rule", not inverse trig derivatives (flagged by the setup agent; checked against the Math 101 syllabus).

## Stat 201
- Setup: 19 exams (STAT 201: 251 and 252, all three kinds; STAT 319: 243-e1, 242 x3, 241 x3, 233 x3, 231-e1/e2, 222-e1). No Stat exams are listed for 261, 253, 232, 223 or 221 (221 has only STAT 310, skipped). All pure MCQ, so the written type is NOT needed for Stat (it was used for Math 208 221).
- Statistical tables: no exam prints z/t/chi-square/F tables (students evidently use calculators). Decision: steps state the needed critical values directly; hints give the general formula.
- Figures: pictures (histograms, box plots, Venn diagrams, circuits, residual plots) and long R/software output are cropped as images; data and PMF tables are typeset as LaTeX arrays. Shared stems are repeated in each question because questions are shuffled.
- No marked key (derived; the master convention puts the answer at (a)): 251 x3, 243-e1, 233-e1, 233-e2. 242-fx Q6: the key says (c) is also accepted; the site can only mark one answer, so (a) is kept and the steps mention (c).
- Change: old STAT 319 exams are labelled "Originally STAT 319" on the term list and exam page, and "Original course: STAT 319" in the PDF header line. This is driven by the "source" file name; Math 208 data and the 261-e1 PDF text were checked identical afterwards.
- KEY DISAGREEMENT, stat201 242-e2 Q3 (STAT 319): normal with mean 10 and variance 4; P(X>13) = P(Z>1.5) = 0.0668, but the key is 0.0681 (z = 1.49; the transcription was checked against the PDF text). No choice is 0.0668. Key kept; the steps say so. Q8: the key uses the table value z = -2.33 (rounding, fine).
- stat201 252-e2 Q13: the array declared 6 columns but had 7 cells (would break pdfLaTeX); fixed, and validate.py now checks array column counts.
- stat201 243-e1 Q9: odd printed wording ("properly functioning components"); read as 4 - E(X) = 1, which matches the master (a). Noted. Q10 (box plot) noted.
- stat201 233-e1 Q13: the 90th percentile depends on the percentile rule (95.8 vs 95 vs 94.2, all among the choices); the master (a) 95.8 = the p(n+1) rule. Q6 is locked (the last choice is "there is no c").
- stat201 252-fx Q10: the key uses the normal approximation without continuity correction (noted).
- stat201 233-e2 Q5 (no official key): read literally ("the next 30 km" after the first 10), the answer e^-3 = 0.0498 is not a choice. The choice 0.1353 = e^-2 = P(X>30 | X>10) (inspection up to the 30 km mark), which is the master (a). The agent's steps had called it a misprint; I rewrote them to show the intended reading and mention the literal one. Q7: the closest choice is a table-rounded value (0.4524 vs exact 0.4415).
- stat201 242-fx: the "option (c) also accepted" remark is on Q5 (not Q6); the last step mentions it. Q9 and Q3 depend on table rounding and the quartile rule (noted).
- stat201 251-fx (no key, derived): Q7 is a table-rounded value (0.85083 vs exact 0.85122) and Q16 is a p-value range (noted).
- stat201 233-fx Q16 (minor key mismatch): F = 1400/138.86 = 10.08, but the key prints 10.01 (the only nearby choice; kept, noted). Q1/Q7/Q11/Q12/Q14/Q20 keys use rounded table values (last-digit differences).
- stat201 231-e1: Q15/Q16 had no red solution (derived: Q16 has one outlier, 941). Q11 is geometric (old STAT 319 topic, kept). Q13 uses the (n+1)p quartile rule.
- stat201 231-e2: several keys are table-rounded (Q3, Q9, Q10, Q13); Q11 is continuous uniform (old topic, kept).
- stat201 222-e1: Q12/Q15/Q18 keys are table-rounded; Q13 is hypergeometric; Q8 geometric, Q11 continuous uniform and Q14 normal approximation to Poisson are old STAT 319 topics (kept).
- Stat 201 DONE: 19 exams built, 27 cropped images. Key disagreements: 242-e2 Q3 (0.0681 vs 0.0668) and a minor one in 233-fx Q16 (10.01 vs 10.08). No-key exams (derived): 251 x3, 243-e1, 233-e1, 233-e2.
- Dates with a leading zero (222-e1, 243-e1) were normalised ("3 July 2025").
- Section numbers are written "6.1" (the textbook uses "6-1") so they sort like the other courses.

## Pre-deploy review (2026-10-28, owner present, done directly without subagents)
- Home page: the highlighted (black) exam button is now automatic. build.py writes every exam's month-day into data/courses.js (ICE_DATES), and the page highlights the kind whose next usual date comes soonest (it switches the day after an exam). On 28 October it highlights Major Exam II.
- MathJax check of all 34,774 site strings (questions, choices, hints, steps, answers) with tools/mjtest.html (serve the repo root and open /tools/mjtest.html). Found 8 Stat tables using \multicolumn, which MathJax 3 cannot render (pdfLaTeX could, so the PDFs were fine). Fixed by putting the spanning header over the first column; validate.py now bans \multicolumn. Re-run: 0 problems (the test was proven to catch both TeX errors and undefined commands).
- File checks: all 154 PDFs and 38 images are linked with exact-case names (GitHub Pages is case-sensitive), there are no stale files, the largest file is 0.7 MB, the total is 48.6 MB, and the only external dependency is MathJax 3.2.2 from jsDelivr.
- Special pages (omitted, written, Version B, Stat 319) load with no console errors.
- All cropped images were reviewed on contact sheets: all good (scan-derived ones show at most faint ghosts where handwriting was removed).

- Home page: the title is now "Ice Math Old Exams Archive - Unofficial" (page title and heading). The English note was replaced by the owner's Arabic note, placed right-to-left above "Choose a course and an exam", in IBM Plex Sans Arabic (Google Fonts).
- PHONE FIX (an issue from the original template): on narrow screens, wide formulas made the whole exam page scroll sideways. Questions, choices, hints and solution steps now scroll their own wide formulas, and the grids use minmax(0,1fr). Measured at 375 px on four exam pages: page width = screen width. Desktop is unchanged.
- README.md added (live link https://mibnrashid.github.io/Ice_Math_OldExams/ and an issues link for reporting mistakes).

## PDF layout fixes (build.py; exams of 21 or fewer questions are byte-for-byte the same text as before, checked on 261-e1)
- The "Student effort not Official..." credit line was stamped on the LAST page, assuming a one-page key. It is now stamped on the page with the "Answer Key" heading. All 70 PDFs checked: stamp on page 1 and the key page only.
- For exams with more than 21 questions (the 28-question finals: math208 223/231/232-fx, math201 221/222/223/232-fx), the key table didn't fit and LaTeX pushed it to the next page, leaving the heading page blank. Such keys are now split into two tables (half each, header repeated). Checked visually on math201 222-fx.

## Exams with no official key (answers solved and verified by us)
- math208 241-fx: the source is version CODE01, not the master (no marks); all 20 answers derived.
- math208 243-fx, 233-fx, 232-e1: master with no "(correct)" marks; derived, and the first choice was correct throughout (the usual convention).

## Master-key disagreements / doubtful items
- math208 251-e2 Q1: flawed question. The matrix has rank 3 for every alpha (checked with sympy), so every choice satisfies it. The key (alpha=1) is kept.
- math208 251-e2 Q15: the original exam prints the choice matrices run together (a typesetting bug, checked on the rendered page). Choices were reconstructed literally as P then D; (d) is identical to (b) and was dropped, so 4 choices. The agent had invented two distractors; I replaced them.
- math208 233-e1 Q10: the key's form A tan(Ax+B) covers only one sign of the integration constant (noted).
- math208 252-fx Q7: the key's "n >= 2" is a subset of the true range (noted).
- math208 243-fx Q17/Q19: the answers assume zero integration constants in variation of parameters.
- math208 231-e1 Q12: the master prints (b) and (c) identically; one copy was kept, so 4 choices.
- math208 231-fx Q17: which eigenvalue goes with which vector is inferred from the solution form (key -24 matches). Q21: the master says n >= 1, but the recurrence also holds for n = 0 (kept).
- math208 222-fx (no official key; 180 minutes): Q11 needs Cayley-Hamilton (outside the syllabus, kept per the rule and solved that way; the coefficients aren't unique because A^2=5A-6I, and the key 10 is the characteristic-polynomial choice). Q17 asks for a Jordan form (outside the syllabus, kept). Q7: y_p(0)=0 doesn't fix y_p; the key 3/8 is the polynomial y_p.
- math208 221-fx: minutes not printed; 180 assumed (the 222 and 231 finals print 180). Q1: the key -sqrt5 takes the negative root, though strictly the solution curve doesn't reach x=2. Q9: a missing e^{mu t} factor was added (typo, doesn't change the answer). Q8 (Cayley-Hamilton) and Q19 (Jordan form) are outside the syllabus and kept.
- math208 222-e1, 222-e2: no official key (derived; first choice correct throughout).
- math208 223-e2 Q8: the source tags it 5.1, but it uses complex roots (5.3); the tag is kept.
- math208 232-e2 Q14: the steps drop a homogeneous term to match the key.
- math208 233-fx Q5: the printed "R^3" should be R^4 (fixed, noted). 241-fx Q6 and Q9(c) have small print typos (noted).
- math208 243-e1 Q2: complex roots (sum still -1), noted.
- math208 242-e2 Q9: the printed equation was missing a "y" (added, noted).
- math208 251-fx Q14: the particular solution isn't unique; the key matches variation of parameters with zero constants.
