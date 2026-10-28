"""Check exam JSON files against tools/SPEC.md.

Usage: python -I tools/validate.py src/math208/253-fx.json [more files...]
"""
import json
import re
import sys
from pathlib import Path

KINDS = {"e1", "e2", "fx"}
BANNED = [r"\\textbf", r"\\textit", r"\\newcommand", r"\\color", r"\$\$", r"\*\*", "`",
          r"\\begin\{equation", r"\\begin\{align\}", r"\\begin\{align\*\}", r"\\displaystyle", r"\\emph",
          r"\\llbracket", r"\\rrbracket",  # not in amssymb: use \lfloor x\rfloor for the greatest integer
          r"\\multicolumn"]  # MathJax 3 cannot render it: put a spanning header over the first column instead
UNICODE_MATH = "≤≥≠±×÷√∞∫∑→←⇒⇔∈∉⊂⊆∪∩°πθλαβγδεμσρ−–—“”‘’…"


def split_math(s):
    """Yield (is_math, text) chunks; raises ValueError on unbalanced delimiters."""
    out, i, n = [], 0, len(s)
    buf = ""
    while i < n:
        if s.startswith("\\[", i):
            j = s.find("\\]", i + 2)
            if j < 0:
                raise ValueError("unclosed \\[")
            out.append((False, buf)); buf = ""
            out.append((True, s[i + 2:j])); i = j + 2
        elif s[i] == "$":
            j = i + 1
            while j < n and not (s[j] == "$" and s[j - 1] != "\\"):
                j += 1
            if j >= n:
                raise ValueError("unbalanced $")
            out.append((False, buf)); buf = ""
            out.append((True, s[i + 1:j])); i = j + 1
        elif s.startswith("\\]", i):
            raise ValueError("stray \\]")
        else:
            buf += s[i]; i += 1
    out.append((False, buf))
    return out


def check_text(s, where, errs):
    if not isinstance(s, str) or not s.strip():
        errs.append(f"{where}: empty or not a string"); return
    for b in BANNED:
        if re.search(b, s):
            errs.append(f"{where}: banned pattern {b!r}")
    for ch in UNICODE_MATH:
        if ch in s:
            errs.append(f"{where}: unicode character {ch!r}; use LaTeX")
    try:
        chunks = split_math(s)
    except ValueError as e:
        errs.append(f"{where}: {e}"); return
    for is_math, t in chunks:
        if is_math:
            if t.count("{") != t.count("}"):
                errs.append(f"{where}: unbalanced braces in maths {t[:40]!r}")
            for env in re.findall(r"\\begin\{(\w+\*?)\}", t):
                if t.count("\\begin{%s}" % env) != t.count("\\end{%s}" % env):
                    errs.append(f"{where}: unmatched environment {env}")
            for spec, body in re.findall(r"\\begin\{array\}\{([^}]*)\}(.*?)\\end\{array\}", t, re.S):
                cols = len(re.findall(r"[lcr]|p\{[^}]*\}", spec))
                widest = max(row.count("&") + 1 for row in re.split(r"\\\\", body))
                if "\\multicolumn" not in body and widest > cols:
                    errs.append(f"{where}: array has {widest} cells in a row but only {cols} columns in {{{spec}}}")
        else:
            if re.search(r"<[a-zA-Z/]", t):
                errs.append(f"{where}: HTML-like tag outside maths in {t.strip()[:50]!r}")
            if re.search(r"[%&#_^]", t):
                errs.append(f"{where}: literal % & # _ or ^ outside maths in {t.strip()[:50]!r}")
            if re.search(r"\\[a-zA-Z]", t):
                errs.append(f"{where}: LaTeX command outside maths in {t.strip()[:50]!r}")


def norm_opt(s):
    """Strip formatting that doesn't change how a choice looks, to catch disguised duplicates."""
    s = s.replace("\\dfrac", "\\frac").replace("\\tfrac", "\\frac").replace("\\left", "").replace("\\right", "")
    s = re.sub(r"\\frac\{?(\w)\}?\{?(\w)\}?", r"\1/\2", s)
    s = re.sub(r"\\[,;:! ]|\s|\$", "", s)
    return s.replace("{", "").replace("}", "")


def strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from strings(v)


def validate(path):
    errs = []
    p = Path(path)
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"{p}: cannot parse JSON: {e}"]
    if re.search(r"[\x00-\x09\x0b-\x1f]", "".join(strings(d))):
        errs.append("control character in a string (a LaTeX backslash was probably eaten, e.g. \\b in \\begin)")
    outside = re.sub(r"\\begin\{(\w+)\}.*?\\end\{\1\}", " ", "\n".join(strings(d)), flags=re.S)
    if re.search(r"\\\\", outside):
        errs.append("doubled backslash outside a matrix/aligned/cases environment (e.g. \\\\lim instead of \\lim)")
    if re.search(r"(?<!\\)\\[\d-]", "".join(strings(d))):
        errs.append("single backslash before a digit or minus: a matrix/aligned row break must be \\\\ (doubled in JSON)")
    for k in ("course", "term", "kind", "date", "minutes", "qs"):
        if k not in d:
            errs.append(f"missing top-level field {k}")
    if d.get("kind") not in KINDS:
        errs.append("kind must be e1, e2 or fx")
    if not re.fullmatch(r"\d{3}(b)?", str(d.get("term", ""))):
        errs.append("term must be 3 digits as a string (a second version of the same exam: 3 digits + 'b')")
    elif str(d["term"]).endswith("b") and d.get("version") != "B":
        errs.append("a 'b' term needs \"version\": \"B\"")
    if p.stem != f"{d.get('term')}-{d.get('kind')}":
        errs.append(f"file name should be {d.get('term')}-{d.get('kind')}.json")
    if d.get("date", None) == "":
        if not d.get("note"):
            errs.append("empty date (not printed) needs a top-level note")
    elif not re.fullmatch(r"\d{1,2} [A-Z][a-z]+ \d{4}", str(d.get("date", ""))):
        errs.append("date must look like '5 August 2026' (or \"\" if not printed)")
    qs = d.get("qs") or []
    if not qs:
        errs.append("no questions")
    for i, q in enumerate(qs, 1):
        w = f"Q{i}"
        if q.get("omitted"):
            if q["omitted"] is not True or set(q) - {"omitted", "q", "note"}:
                errs.append(f"{w}: an omitted placeholder has only \"omitted\": true, \"q\" and an optional \"note\"")
            else:
                check_text(q["q"], w + ".q", errs)
            continue
        need =("sec", "q", "answer", "hints", "steps", "brief") if q.get("written") else \
            ("sec", "q", "opts", "ans", "hints", "steps", "brief")
        for k in need:
            if k not in q:
                errs.append(f"{w}: missing {k}")
        if errs and any(e.startswith(w + ": missing") for e in errs):
            continue
        check_text(q["q"], w + ".q", errs)
        if q.get("written"):
            if q["written"] is not True or "opts" in q or "ans" in q:
                errs.append(f"{w}: a written question has \"written\": true, an \"answer\" and no opts/ans")
            check_text(q["answer"], w + ".answer", errs)
        elif not isinstance(q["opts"], list) or len(q["opts"]) < 2:
            errs.append(f"{w}: opts must be a list of choices")
        else:
            for j, o in enumerate(q["opts"]):
                check_text(o, f"{w}.opt{j}", errs)
                if re.match(r"^\s*\(?[a-eA-E]\)\s", o):
                    errs.append(f"{w}.opt{j}: do not include the choice letter")
            if len(set(q["opts"])) != len(q["opts"]):
                errs.append(f"{w}: duplicate choices")
            elif len({norm_opt(o) for o in q["opts"]}) != len(q["opts"]):
                errs.append(f"{w}: two choices differ only in LaTeX formatting (they render the same)")
        if not q.get("written") and (not isinstance(q["ans"], int) or not (0 <= q["ans"] < len(q["opts"]))):
            errs.append(f"{w}: ans out of range")
        if not isinstance(q["hints"], list) or len(q["hints"]) != 3:
            errs.append(f"{w}: need exactly 3 hints")
        else:
            for j, h in enumerate(q["hints"]):
                check_text(h, f"{w}.hint{j+1}", errs)
        if not isinstance(q["steps"], list) or not q["steps"]:
            errs.append(f"{w}: steps must be a non-empty list")
        else:
            for j, s in enumerate(q["steps"]):
                check_text(s, f"{w}.step{j+1}", errs)
        check_text(q["brief"], w + ".brief", errs)
        for fld in ("hints", "steps"):
            for s in q.get(fld) or []:
                if re.search(r"(choice|option|answer)\s*\(?[a-e]\)|\([a-e]\)\s*(is|are)", s, re.I):
                    errs.append(f"{w}.{fld}: refers to a choice letter: {s[:60]!r}")
        if "img" in q and not (p.parent / "img" / q["img"]).exists():
            errs.append(f"{w}: image {q['img']} not found in {p.parent / 'img'}")
    return [f"{p.name}: {e}" for e in errs]


if __name__ == "__main__":
    allerr = []
    for a in sys.argv[1:]:
        allerr += validate(a)
    print("\n".join(allerr) if allerr else "OK")
    sys.exit(1 if allerr else 0)
