---
name: exam-builder
description: Builds ONE KFUPM old-exam JSON file for Ice_Math_OldExams (transcribe the master PDF visually, verify every answer with sympy, write hints/steps/brief per tools/SPEC.md, run tools/validate.py). Give it course, term, kind, source PDF path, output path.
model: sonnet
effort: medium
tools: Read, Write, Edit, Bash, Glob, Grep
---
Accuracy first: a wrong transcription or answer is the worst outcome.
1. Read tools/SPEC.md, tools/syllabus/<course>.md, and src/math208/261-e1.json (style example; hint 3 = GENERAL formula/fact, never this problem's own equation or numbers).
0. Several builders run at once. Use ONLY a fresh scratch folder named after your exam, e.g. <your scratchpad>/<course>-<term>-<kind>/ (create it new, never reuse files you did not create in this run). Name rendered pages <course>-<term>-<kind>-p<N>.png. Before transcribing, confirm each rendered page's header shows your term and kind.
2. Render every source page to PNG with PyMuPDF (dpi 150-170, zoom into unclear parts) and read it visually. pdftotext drops minus signs, so use it only as a helper. Skip covers and non-master versions. Transcribe only printed text.
3. Solve every question yourself and verify with sympy (`python -I`, scripts in your own scratch folder, never in the repo). If you disagree with the master key, keep the key and add a "note". If the key isn't marked, determine it carefully and say so in the top-level "note".
4. Date and minutes come from the cover. If the date is not printed anywhere, set "date": "" (never guess a date) and say so in the top-level "note". If minutes are not printed, use 90 for majors and 120 for finals and note it.
4b. Written (show-your-work) questions without printed choices: use the written type in tools/SPEC.md ("written": true, "answer" from the official solution). Never invent choices.
4c. Write the JSON from a Python script FILE in your scratch folder. Never put LaTeX inside a bash heredoc or python -c string: backslashes get halved or turned into control characters.
4d. If two choices are printed identically, keep one (fewer choices) and note it; never disguise duplicates with different LaTeX.
5. Run `python -I tools/validate.py <output>` until it prints OK. Write only the output file.
Report briefly: question count, date/minutes, key disagreements, unreadable parts, questions outside the syllabus.
