"""Cross-check: words of each JSON question vs the text layer of its source PDF.
Usage: python -I xcheck.py <srcdir> <json>...   (scanned PDFs have no text layer -> reported)"""
import json, re, sys
from pathlib import Path
import pymupdf

srcdir = Path(sys.argv[1])
for f in sys.argv[2:]:
    d = json.load(open(f, encoding="utf-8"))
    pdf = srcdir / f"{d['term']}-{d['kind']}.pdf"
    doc = pymupdf.open(pdf)
    import unicodedata
    text = unicodedata.normalize("NFKC", " ".join(p.get_text() for p in doc)).lower()
    pw = set(re.findall(r"[a-z]{4,}", text))
    hdr = [ " ".join(p.get_text().split())[:40] for p in doc]
    terms = set(re.findall(r"\b(2[2-6]\d), math", text))
    if len(pw) < 30:
        print(f"{f}: no text layer (scan) - check visually"); continue
    bad = []
    for i, q in enumerate(d["qs"], 1):
        w = set(re.findall(r"[a-z]{4,}", re.sub(r"\\[a-z]+", " ", q["q"].lower())))
        if w:
            r = len(w & pw) / len(w)
            if r < 0.8: bad.append(f"Q{i}:{r:.2f}")
    print(f"{f}: {len(d['qs'])} qs, pdf terms {sorted(terms)}, low-match {bad or 'none'}")
