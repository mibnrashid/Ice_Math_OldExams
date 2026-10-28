"""List exams on the KFUPM Mathematics exam page that are not built yet (and optionally download them).

Usage:
  python -I tools/find_new_exams.py              # report only
  python -I tools/find_new_exams.py --download   # also download new PDFs to ../Ice_Math_OldExams_sources/<course>/

An exam is "built" when src/<course>/<term>-<kind>.json exists (version B: <term>b-<kind>.json).
Exams we decided not to build are listed in tools/known_skips.json, with the reason.
STAT 319 exams belong to the stat201 course on the site.
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT.parent / "Ice_Math_OldExams_sources"
PAGE = "https://math.kfupm.edu.sa/miscellaneous/exam"
SITE = "https://math.kfupm.edu.sa"
COURSE = {"math101": "math101", "math102": "math102", "math201": "math201", "math208": "math208",
          "stat201": "stat201", "stat319": "stat201"}
KIND = {"e1": "e1", "ex1": "e1", "e2": "e2", "ex2": "e2", "fx": "fx"}
FIRST_TERM = 221
LINK = re.compile(r'href="(/docs/[^"]*?/((math10[12]|math20[18]|stat201|stat319)([ab])?-(\d{3})-(ex1|ex2|e1|e2|fx))[^"/]*?\.pdf)[^"]*"', re.I)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def main(download):
    html = fetch(PAGE).decode("utf-8", "replace")
    skips = json.loads((ROOT / "tools" / "known_skips.json").read_text(encoding="utf-8"))
    found = {}
    for m in LINK.finditer(html):
        path, _, code, ver, term, kind = m.groups()
        code, kind = code.lower(), KIND[kind.lower()]
        if int(term) < FIRST_TERM:
            continue
        course = COURSE[code]
        tkey = term + ("b" if ver and ver.lower() == "b" else "")
        found[(course, tkey, kind)] = {"url": SITE + path, "source": path.rsplit("/", 1)[1], "orig": code}
    new = []
    for (course, term, kind), info in sorted(found.items(), key=lambda x: (x[0][0], -int(x[0][1][:3]), x[0][1], x[0][2])):
        key = f"{course}/{term}-{kind}"
        if (ROOT / "src" / course / f"{term}-{kind}.json").exists() or key in skips:
            continue
        new.append((key, info))
    print(f"exams on the page (from {FIRST_TERM}): {len(found)}; not built yet: {len(new)}")
    for key, info in new:
        line = f"  NEW {key}  source={info['source']}" + ("  (originally STAT 319)" if info["orig"] == "stat319" else "")
        if download:
            course, name = key.split("/")
            dest = SOURCES / course / f"{name}.pdf"
            dest.parent.mkdir(parents=True, exist_ok=True)
            data = fetch(info["url"])
            if not data.startswith(b"%PDF"):
                line += "  DOWNLOAD FAILED (not a PDF)"
            else:
                dest.write_bytes(data)
                line += f"  -> {dest}"
        print(line)
    if not new:
        print("Nothing new: everything on the page is built or in tools/known_skips.json.")


if __name__ == "__main__":
    main("--download" in sys.argv)
