#!/usr/bin/env python3
"""
One paragraph, one line.

Wrapping prose across lines in .astro is not free: HTML collapses the newline
between running text and an inline element into nothing, so

    lives on its own page:
    <a href="/toolkit/">Toolkit</a>

renders as "page:Toolkit". The usual escapes are a literal &#32; or the
hanging-bracket trick (</a\\n>) that formatters produce, and both are worse than
just leaving the paragraph on one line and turning word wrap on in the editor.

This script applies that rule to existing files. It is a one-off migration
rather than part of the build: from here on the rule is written down in the
README, and scripts/verify.py is what proves no space was lost.

What it does, in order:
  1. Collapses whitespace INSIDE a tag, which folds multi-line attribute lists
     and the hanging bracket back onto one line.
  2. Collapses the CONTENT of prose elements onto one line.
  3. Drops {' '} separators, which only ever existed to survive a line break.

The frontmatter and any multi-line JSX expression are left alone.

Run:  python3 scripts/reflow.py [--check]
"""
from __future__ import annotations

import pathlib
import re
import sys

SRC = pathlib.Path(__file__).resolve().parents[1] / "src"

# Elements whose content is prose and therefore belongs on one line.
PROSE_TAGS = ["p", "li", "h1", "h2", "h3", "h4", "summary", "figcaption"]


def split_frontmatter(text: str) -> tuple[str, str]:
    """Astro frontmatter is TypeScript, not markup. It is never touched."""
    m = re.match(r"^---\n.*?\n---\n", text, flags=re.S)
    return (m.group(0), text[m.end() :]) if m else ("", text)


def collapse_inside_tags(template: str) -> str:
    """`<a\\n  href="x"\\n  class="y"\\n>` becomes `<a href="x" class="y">`.

    Only tags with no JSX expression in them: an attribute like
    class:list={[...]} is deliberately kept multi-line, because it is code.
    """

    def fix(m: re.Match[str]) -> str:
        tag = m.group(0)
        if "\n" not in tag or "{" in tag:
            return tag
        return re.sub(r"\s+", " ", tag).replace(" >", ">").replace(" />", " />")

    # Comments are excluded. They are not rendered, so they cannot lose a
    # space, and a wrapped comment is easier to read than a 300-character one.
    parts = re.split(r"(<!--.*?-->)", template, flags=re.S)
    return "".join(
        part if part.startswith("<!--") else re.sub(r"<[^<>]*>", fix, part, flags=re.S)
        for part in parts
    )


def collapse_prose(template: str) -> str:
    """Put the content of each prose element on the same line as its tags."""
    for tag in PROSE_TAGS:
        # Innermost first: content may not contain another element of the same
        # name, so a <li> holding a <p> is handled by the <p> pass.
        pattern = re.compile(
            rf"(<{tag}\b[^<>]*>)((?:(?!<{tag}\b|</{tag}>).)*?)(</{tag}>)",
            flags=re.S,
        )

        def fix(m: re.Match[str]) -> str:
            open_tag, body, close_tag = m.groups()
            if "\n" not in body:
                return m.group(0)
            # A multi-line JSX expression is code, not prose. Leave it.
            if re.search(r"\{[^{}]*\n", body):
                return m.group(0)
            body = re.sub(r"\s*\n\s*", " ", body).strip()
            body = body.replace("{' '}", " ")
            body = re.sub(r"  +", " ", body)
            return f"{open_tag}{body}{close_tag}"

        template = pattern.sub(fix, template)
    return template


BLOCK_CHILD = re.compile(r"<(p|ul|ol|li|div|section|h[1-6]|details|Image|Card|Chip)\b")


def collapse_slots(template: str) -> str:
    """A <Fragment slot="..."> holding running text is a paragraph too.

    Only when it holds running text: the hero slots on the two home pages hold
    three <p> elements, and putting those on one line would be the opposite of
    readable.
    """
    pattern = re.compile(
        r"(<Fragment\b[^<>]*>)((?:(?!<Fragment\b|</Fragment>).)*?)(</Fragment>)", flags=re.S
    )

    def fix(m: re.Match[str]) -> str:
        open_tag, body, close_tag = m.groups()
        if "\n" not in body or BLOCK_CHILD.search(body) or re.search(r"\{[^{}]*\n", body):
            return m.group(0)
        body = re.sub(r"\s*\n\s*", " ", body).strip()
        return f"{open_tag}{body}{close_tag}"

    return pattern.sub(fix, template)


def process(text: str) -> str:
    head, template = split_frontmatter(text)
    template = collapse_inside_tags(template)
    template = collapse_prose(template)
    template = collapse_slots(template)
    # A stray {' '} left between two elements is now just a space.
    template = re.sub(r"\{' '\}\s*", " ", template)
    return head + template


def main() -> int:
    check = "--check" in sys.argv
    changed: list[str] = []
    for path in sorted(SRC.rglob("*.astro")):
        before = path.read_text(encoding="utf-8")
        after = process(before)
        if before != after:
            changed.append(str(path.relative_to(SRC)))
            if not check:
                path.write_text(after, encoding="utf-8")
    verb = "would reflow" if check else "reflowed"
    print(f"{verb} {len(changed)} file(s)")
    for c in changed:
        print("  " + c)
    return 1 if (check and changed) else 0


if __name__ == "__main__":
    raise SystemExit(main())
