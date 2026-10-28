# Exam data spec

One JSON file per exam: `src/<course>/<term>-<kind>.json`, e.g. `src/math208/253-fx.json`.
`kind` is `e1` (Major Exam I), `e2` (Major Exam II) or `fx` (Final Exam).

Questions and choices are stored in the **official master order**. The build script
(`tools/build.py`) shuffles questions and choices once, with a fixed seed, and the website and the
PDF both use that same shuffled order.

```json
{
  "course": "math208",
  "term": "253",
  "kind": "fx",
  "date": "5 August 2026",
  "minutes": 120,
  "source": "math208-253-fx.pdf",
  "qs": [
    {
      "sec": "1.6",
      "q": "The solution of the exact differential equation \\[ ... \\] is given by",
      "opts": ["$...$", "$...$", "$...$", "$...$", "$...$"],
      "ans": 0,
      "hints": ["...", "...", "..."],
      "steps": ["...", "...", "..."],
      "brief": "One line for the PDF answer key."
    }
  ]
}
```

Optional per-question fields:
- `"lock": true` keeps the choices in master order (use only when a choice refers to another choice,
  e.g. "both (a) and (b)", or "None of the above" must stay last).
- `"img": "math208-253-fx-q7.png"` is a figure cropped from the source PDF and saved in
  `src/<course>/img/`. It is shown under the question text. Use only when the question cannot be
  written in text/LaTeX.
- **Written questions** (a show-your-work part with no printed choices, e.g. "(11 points)"): set
  `"written": true`, leave out `opts` and `ans`, and give `"answer"` = the final answer as printed in the
  official solution (LaTeX allowed, e.g. `"$y=c_1e^{x}+c_2xe^{x}$"`). `hints`, `steps` and `brief` work as usual.
  The brief must state the final result. Never invent choices for a written question. The build places written
  questions after the multiple-choice part (shuffled among themselves). The site shows "Show answer", and the PDF
  leaves working space and lists the answer in the key.
- **Omitted placeholder** (a question missing from the published source): `{"omitted": true, "q": "Question N of the original exam is omitted (...)."}` with no other fields, inserted at its master position. The build puts it at the end; the site shows only the text, and the PDF key says "omitted".
- **Second version of the same exam** (e.g. versions A and B given on the same day): use term `"251b"` (file `251b-e2.json`) with `"version": "B"`, and add `"version": "A"` to the first one. The site and PDF show "Term 251, Version B".
- `"date": ""` means the date is not printed in the source (never guess one); it then needs a top-level `note`.
- Top-level `"note"` (optional) records exam-level assumptions, e.g. "Date not printed; taken from
  the syllabus."
- `"note": "..."` is for the maintainer only and is never shown. Use it to flag anything doubtful,
  such as a master key that seems wrong or an unreadable scan.

## Fields

- `sec`: textbook section, such as `"1.5"`, `"4.3"`, `"7.6"`, `"11.3"` or `"Ch. 3"`. For Stat and other
  courses, use the section numbering from that course's syllabus.
- `q`: the question text, transcribed faithfully from the master version. Keep the wording. Fix
  only obvious typos.
- `opts`: the choices in master order, normally 5 (a–e). Do not include the letter.
- `ans`: 0-based index into `opts` of the correct choice. In the master version this is usually 0,
  since the correct answer is (a) and/or marked "(correct)". **Verify every answer yourself.** If your
  work disagrees with the master key, recheck carefully. If you still disagree, keep the master key
  and explain in `note`.
- `hints`: exactly 3 strings, in increasing strength:
  1. **The idea.** Which type of problem, method or concept this is (for example "This is a
     Bernoulli equation" or "Think about what 'consistent' means for the augmented matrix"). No
     computation.
  2. **The first move.** The concrete first step to take (what to substitute, which matrix to
     row-reduce, what to differentiate). No worked numbers.
  3. **The key formula or fact** needed to finish, stated in general form (for example
     $\rho=e^{\int P\,dx}$ and $(\rho y)'=\rho Q$, $W=y_1y_2'-y_1'y_2$, "a matrix is invertible iff
     $\det\neq0$", or "for $r=a\pm bi$ the solutions are $e^{ax}\cos bx$, $e^{ax}\sin bx$"). It must be
     general, **not this problem's own equation or numbers**: write "the characteristic equation
     $ar^2+br+c=0$", not "$m^2+m-6=0$". No intermediate results specific to this problem.

  A hint must never name the correct choice or rule choices in or out.
- `steps`: a clear step-by-step solution, usually 3–6 steps, each a short sentence plus maths.
  The last step must reach the value in the correct choice. Use **only methods taught in the course
  syllabus** (see the syllabus section list given to you) plus prerequisite courses. For Math 208
  that rules out Laplace transforms, Abel's formula, Cramer's-rule shortcuts beyond Ch. 3,
  Cayley–Hamilton, the "trace = sum of eigenvalues" trick, Jordan forms and similar. Do it the
  textbook way: row reduce, solve the characteristic equation, and so on. Keep a step under about 2
  lines when possible.
- `brief`: one short line (about 80 characters of rendered text) summarising the key computation, for the PDF
  answer key, e.g. `"Bernoulli, $n=4$, $v=y^{-3}$: $v'-\\frac{6}{x}v=-12x^3$."`

## Writing maths (must work in BOTH MathJax 3 and pdfLaTeX + amsmath/amssymb)

- Inline maths: `$...$`. Display maths: `\\[ ... \\]` (in JSON the backslash is doubled).
- Allowed: standard LaTeX maths, `\\frac`, `\\dfrac`, `\\tfrac`, `\\sqrt`, `\\left( \\right)`,
  `\\begin{bmatrix}`, `\\begin{pmatrix}`, `\\begin{vmatrix}`, `\\begin{aligned}`, `\\begin{cases}`,
  `\\begin{array}{...}`, `\\text{...}`, `\\mathbf{}`, `\\operatorname{}`, `\\ln`, `\\sin`, `\\vec`, `\\cdot`,
  `\\neq`, `\\le`, `\\ge`, `\\infty`, `\\sum`, `\\int`, `\\mathbb{R}`, `\\boxed`, `\\quad`.
  Write a linear system with `\\[\\begin{aligned} ... \\end{aligned}\\]` or an `array`.
- **Not allowed:** HTML tags, Markdown (`**`, backticks), `\\textbf` and other text-mode commands
  outside maths, `\\newcommand`, `\\color`, `\\displaystyle` at the start of options (use `\\dfrac`
  instead), `$$...$$`, Unicode maths symbols (write `\\le`, not `≤`; `-` is a normal minus inside maths).
- Plain text may use normal ASCII punctuation. Do not use a literal `%`, `&`, `#` or `_` outside maths
  (write `$\\%$` inside maths if needed). Use straight quotes.
- Degrees: write `$25^\\circ\\text{C}$`, not `°`.
- Rank and other operators: `\\operatorname{rank}(A)`, `\\operatorname{span}`, `\\det`, `\\dim`.
- Vectors: `\\mathbf{v}` and column vectors with `\\begin{bmatrix}`.

## Voice

Plain, clear student-friendly English. No "Let's", no emojis, no exclamation marks. Never mention
that the answer is "(a)" in hints or steps, because the choices get shuffled. Refer to values, not
letters.

## Validate

Run `python -I tools/validate.py src/<course>/<file>.json` and fix every error before finishing.
