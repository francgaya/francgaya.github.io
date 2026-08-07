#!/usr/bin/env python3
"""
Verification of the built site, run against dist/ and never against source.

What it checks, and why each one is here:

  1. Emitted JavaScript. The site ships none. The one inline script is the
     language switcher enhancement, and it is counted separately so that a
     bundle sneaking in cannot hide behind it.
  2. Google font CDN. Serving the fonts from it breaches the GDPR per the
     Landgericht Muenchen I ruling, and the target audience is in DACH.
  3. Folded content in the HTML. A <details> whose body is fetched on open
     does not index, does not print, and is not in view-source.
  4. Banned characters: em dash, middle dot, en dash, soft hyphen.
  5. WORD-BY-WORD transcription against web/content. This is the one that
     earns its keep: in P-16 it caught three lost spaces before a glossary
     term that are invisible to the eye.

Run:  python3 scripts/verify.py
"""
from __future__ import annotations

import difflib
from collections import Counter
import pathlib
import re
import sys

from bs4 import BeautifulSoup

SITE = pathlib.Path(__file__).resolve().parents[1]
DIST = SITE / "dist"
CONTENT = SITE.parents[0] / "content"

# Built page -> its source of record. /ui-kit has none: it is a working page.
PAGES = {
    "index.html": "en/index.md",
    "what-i-do/index.html": "en/what-i-do.md",
    "career/index.html": "en/career.md",
    "toolkit/index.html": "en/toolkit.md",
    "about/index.html": "en/about.md",
    "es/index.html": "es/index.md",
    "es/lo-que-hago/index.html": "es/lo-que-hago.md",
    "es/trayectoria/index.html": "es/trayectoria.md",
    "es/herramientas/index.html": "es/herramientas.md",
    "es/sobre-mi/index.html": "es/sobre-mi.md",
}

BANNED = {
    "—": "em dash",
    "·": "middle dot",
    "–": "en dash",
    "­": "soft hyphen",
}

failures: list[str] = []
notes: list[str] = []


def report(ok: bool, label: str, detail: str = "") -> None:
    mark = "PASS" if ok else "FAIL"
    print(f"[{mark}] {label}{(': ' + detail) if detail else ''}")
    if not ok:
        failures.append(label)


def html_files() -> list[pathlib.Path]:
    return sorted(DIST.rglob("*.html"))


# --------------------------------------------------------------------------
# 1. JavaScript
# --------------------------------------------------------------------------
emitted = [p for p in DIST.rglob("*") if p.suffix in {".js", ".mjs"} and ".prerender" not in p.parts]
report(not emitted, "no emitted JavaScript files", f"{len(emitted)} found")

inline_total = 0
for f in html_files():
    inline_total += len(re.findall(r"<script", f.read_text(encoding="utf-8")))
expected = len(html_files())  # exactly one, the switcher enhancement, per page
report(
    inline_total == expected,
    "exactly one inline script per page (the language switcher)",
    f"{inline_total} across {expected} pages",
)

# --------------------------------------------------------------------------
# 2. Fonts
# --------------------------------------------------------------------------
cdn = [
    f
    for f in list(DIST.rglob("*.html")) + list(DIST.rglob("*.css"))
    if re.search(r"fonts\.googleapis|gstatic", f.read_text(encoding="utf-8"))
]
report(not cdn, "no Google font CDN reference", f"{len(cdn)} files")
woff2 = list(DIST.rglob("*.woff2"))
report(bool(woff2), "fonts are self-hosted", f"{len(woff2)} woff2 files")

# --------------------------------------------------------------------------
# 3. Folded content is in the HTML, and closed
# --------------------------------------------------------------------------
open_by_default = 0
empty_folds = 0
for f in html_files():
    soup = BeautifulSoup(f.read_text(encoding="utf-8"), "html.parser")
    for det in soup.select("details.disclosure"):
        if det.has_attr("open"):
            open_by_default += 1
        body = det.find("div", class_="prose-block")
        if not body or len(body.get_text(strip=True)) < 40:
            empty_folds += 1
report(open_by_default == 0, "no disclosure open by default", f"{open_by_default} open")
report(empty_folds == 0, "every disclosure carries its body in the HTML", f"{empty_folds} empty")

# --------------------------------------------------------------------------
# 4. Banned characters
# --------------------------------------------------------------------------
hits = 0
for f in html_files():
    text = f.read_text(encoding="utf-8")
    for ch, name in BANNED.items():
        n = text.count(ch)
        if n:
            hits += n
            notes.append(f"{f.relative_to(DIST)}: {n} x {name}")
report(hits == 0, "no em dash, middle dot, en dash, or soft hyphen", f"{hits} hits")


# --------------------------------------------------------------------------
# 5. Word-by-word transcription against web/content
# --------------------------------------------------------------------------
def words_from_markdown(path: pathlib.Path) -> list[str]:
    """Body words of a content file: no front matter, no HTML comments, no
    internal notes, and no markdown syntax."""
    raw = path.read_text(encoding="utf-8")
    raw = re.sub(r"^---\n.*?\n---\n", "", raw, flags=re.S)
    # The L1 summary marker IS content (it becomes the <details> summary), so
    # it is unwrapped rather than dropped. Every other comment is a note.
    raw = re.sub(r"<!--\s*L1 summary:\s*(.*?)\s*-->", r"\1", raw, flags=re.S)
    raw = re.sub(r"<!--.*?-->", " ", raw, flags=re.S)
    raw = re.sub(r"^>.*$", " ", raw, flags=re.M)  # blockquoted internal notes
    raw = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", raw)  # images
    raw = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", raw)  # links keep their text
    raw = re.sub(r"\{#[a-z-]+\}", " ", raw)  # anchor syntax
    raw = re.sub(r"[#*`_|>-]", " ", raw)
    return normalise(raw)


def words_from_html(path: pathlib.Path) -> list[str]:
    """Body words of a built page: the main region minus the shared CTA, which
    lives in _common.md and is verified separately."""
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    main = soup.find("main")
    for cta in main.select("section.on-deep.bg-surface-deep"):
        # The page header band is also on-deep; only the CTA has a mt-24.
        if "mt-24" in cta.get("class", []):
            cta.decompose()
    # Glossary popovers are the gloss, not the page copy.
    for gloss in main.select(".term-gloss"):
        gloss.decompose()
    # The section index repeats the six titles by design, and it LINKS.
    for idx in main.select("nav[aria-label]"):
        idx.decompose()
    return normalise(main.get_text(" "))


def normalise(text: str) -> list[str]:
    text = text.replace(" ", " ").replace("&", "and")
    text = re.sub(r"[‘’]", "'", text)
    text = re.sub(r"[“”]", '"', text)
    text = re.sub(r"[^\w'\s]", " ", text, flags=re.UNICODE)
    return text.lower().split()


print()
print("Word-by-word transcription, built page against its content file.")
print("Two separate claims, and only the first one is a hard failure:")
print("  MULTISET  no word was lost, added, or altered.")
print("  SEQUENCE  the order matches too. A pure reordering is legitimate,")
print("            because the markdown does not encode visual order: on")
print("            /career the dates are set above the role by TimelineEntry.")
print()
for page, source in PAGES.items():
    html_words = words_from_html(DIST / page)
    md_words = words_from_markdown(CONTENT / source)

    lost = Counter(md_words) - Counter(html_words)
    added = Counter(html_words) - Counter(md_words)
    multiset_ok = not lost and not added

    sm = difflib.SequenceMatcher(None, md_words, html_words, autojunk=False)
    ratio = sm.ratio()
    diffs = [op for op in sm.get_opcodes() if op[0] != "equal"]

    flag = "PASS" if multiset_ok else "FAIL"
    order = "exact" if not diffs else f"{len(diffs)} moves"
    print(f"  [{flag}] {page:32} words {len(md_words):5}  seq {ratio:.4f}  order {order}")
    if not multiset_ok:
        failures.append(f"transcription {page}")
        if lost:
            print(f"        LOST from content : {dict(lost)}")
        if added:
            print(f"        ADDED in build    : {dict(added)}")
    elif diffs:
        # Reordering only. Print it so it is a decision on the record rather
        # than a threshold quietly swallowing it.
        for tag, i1, i2, j1, j2 in diffs:
            if tag == "insert":
                print(f"        moved earlier: {' '.join(html_words[j1:j2])[:90]!r}")

# --------------------------------------------------------------------------
# 6. Internal links, anchors, and the language pairing
#
# /ui-kit is excluded: its buttons and inline links are specimens that need an
# href in order to be a specimen, and they deliberately point nowhere.
# --------------------------------------------------------------------------
built_routes = set()
for f in html_files():
    rel = "/" + str(f.relative_to(DIST)).replace("index.html", "")
    built_routes.add(rel if rel.endswith("/") else rel + "/")

dead_links: list[str] = []
dead_anchors: list[str] = []
mispaired: list[str] = []

for f in html_files():
    name = str(f.relative_to(DIST))
    soup = BeautifulSoup(f.read_text(encoding="utf-8"), "html.parser")
    if not name.startswith("ui-kit"):
        ids = {e["id"] for e in soup.select("[id]")}
        for a in soup.select("a[href]"):
            href = a["href"]
            if href.startswith(("http", "mailto:")):
                continue
            path, _, frag = href.partition("#")
            if not path:
                if frag not in ids:
                    dead_anchors.append(f"{name} -> {href}")
                continue
            if path not in built_routes:
                dead_links.append(f"{name} -> {href}")
            elif frag:
                target = DIST / ((path.strip("/") + "/index.html") if path != "/" else "index.html")
                if f'id="{frag}"' not in target.read_text(encoding="utf-8"):
                    dead_anchors.append(f"{name} -> {href}")

    # The switcher has to point at the EQUIVALENT page, never at the home page.
    switches = {a["href"] for a in soup.select("a[data-lang-switch]")}
    if len(switches) != 1:
        mispaired.append(f"{name}: {sorted(switches)}")

report(not dead_links, "no dead internal links", f"{len(dead_links)}")
for d in dead_links:
    print("      " + d)
report(not dead_anchors, "no dead anchors", f"{len(dead_anchors)}")
for d in dead_anchors:
    print("      " + d)
report(not mispaired, "one language-switcher target per page", f"{len(mispaired)}")
for d in mispaired:
    print("      " + d)

# --------------------------------------------------------------------------
# 7. Glossary terms
#
# Two properties, and the second is the one that bit P-16: shared anchor names
# all resolve to the LAST element in the document, so every popover on a page
# opened under the last term instead of the one that was clicked.
# --------------------------------------------------------------------------
dup_terms: list[str] = []
bad_anchors: list[str] = []
for f in html_files():
    name = str(f.relative_to(DIST))
    text = f.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")
    labels = [b.get_text(" ", strip=True) for b in soup.select("button.term")]
    for label in {l for l in labels if labels.count(l) > 1}:
        dup_terms.append(f"{name}: {label!r} marked {labels.count(label)} times")
    anchors = re.findall(r"anchor-name:\s*(--[\w-]+)", text)
    if len(anchors) != len(set(anchors)):
        bad_anchors.append(f"{name}: {len(anchors)} anchors, {len(set(anchors))} unique")
    if len(soup.select("span.term-gloss")) != len(labels):
        bad_anchors.append(f"{name}: term and popover counts differ")

report(not dup_terms, "each glossary term marked once per page", f"{len(dup_terms)}")
for d in dup_terms:
    print("      " + d)
report(not bad_anchors, "one unique popover anchor per term", f"{len(bad_anchors)}")
for d in bad_anchors:
    print("      " + d)

print()
if notes:
    print("Notes:")
    for n in notes:
        print("  " + n)

print()
if failures:
    print(f"FAILURES: {len(failures)}")
    for f in failures:
        print("  " + f)
    sys.exit(1)
print("All checks passed.")
