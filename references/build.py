#!/usr/bin/env python3
"""Inject the Mermaid runtime into a Visual Artifact, replacing the
<!--MERMAID_RUNTIME--> marker that the template leaves in place.

Two modes:
  · self-contained (DEFAULT): inlines the vendored mermaid.min.js so the file
    works fully offline / on localhost and makes zero outside calls. ~3.3 MB.
  · --lightweight: emits a <script src> to the jsDelivr CDN. A few KB; needs
    internet. Use when publishing many artifacts to one host.

Usage:
  python build.py artifact.html                 # self-contained, edit in place
  python build.py draft.html  out.html          # write result to out.html
  python build.py artifact.html --lightweight   # CDN mode
"""
import os
import re
import sys

MARKER = "<!--MERMAID_RUNTIME-->"
CDN = "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"
HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, "mermaid.min.js")


def runtime_block(lightweight):
    if lightweight:
        return '<script src="%s"></script>' % CDN
    with open(LIB, "r", encoding="utf-8") as f:
        lib = f.read()
    # A closing tag inside the library would end our inline script early; neutralise it.
    lib = lib.replace("</script", "<\\/script")
    return "<script>\n%s\n</script>" % lib


KNOWN_DIAGRAMS = (
    "flowchart", "graph", "sequencediagram", "classdiagram", "statediagram",
    "erdiagram", "journey", "gantt", "pie", "mindmap", "timeline", "gitgraph",
    "quadrantchart", "requirementdiagram", "c4context", "sankey", "xychart", "block-beta",
)


def lint(html):
    """Pre-publish structural checks: each lens carries a diagram, each diagram looks real.
    Warns (non-fatal) so a broken or text-only artifact is caught before it ships."""
    warns = []
    html = re.sub(r"<!--.*?-->", "", html, flags=re.S)  # ignore example markup in comments
    sections = re.findall(r'<section\b[^>]*\bdata-lens="([^"]+)"[^>]*>(.*?)</section>', html, re.S)
    total = 0
    for lens, body in sections:
        pres = re.findall(r'<pre class="mermaid">(.*?)</pre>', body, re.S)
        if not pres:
            warns.append("lens '%s' has no diagram (visual-first: aim for 2+ per lens)" % lens)
        for i, raw in enumerate(pres, 1):
            total += 1
            text = re.sub(r"<[^>]+>", "", raw).replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
            lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
            if not lines:
                warns.append("lens '%s' diagram #%d is empty" % (lens, i))
                continue
            head = re.sub(r"[^a-z0-9-]", "", lines[0].lower().split(" ")[0])
            if not any(head.startswith(k) for k in KNOWN_DIAGRAMS):
                warns.append("lens '%s' diagram #%d: unrecognized type '%s' — may not render"
                             % (lens, i, lines[0][:32]))
    return warns, total, len(sections)


def main(argv):
    flags = [a for a in argv if a.startswith("--")]
    args = [a for a in argv if not a.startswith("--")]
    lightweight = "--lightweight" in flags
    if not args:
        sys.stdout.write(__doc__)
        return 2

    src = args[0]
    out = args[1] if len(args) > 1 else src
    with open(src, "r", encoding="utf-8") as f:
        html = f.read()

    warns, ndiag, nlens = lint(html)
    for w in warns:
        sys.stderr.write("lint: %s\n" % w)

    if MARKER not in html:
        sys.stderr.write("error: %s not found in %s (already built?)\n" % (MARKER, src))
        return 1

    html = html.replace(MARKER, runtime_block(lightweight), 1)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)

    if lightweight:
        note = "lightweight (CDN, needs internet)"
    else:
        note = "self-contained (%d KB inlined, works offline)" % (os.path.getsize(LIB) // 1024)
    lint_note = "" if not warns else " · %d lint warning(s) above" % len(warns)
    sys.stdout.write("built %s — %s · %d diagrams / %d lenses%s\n" % (out, note, ndiag, nlens, lint_note))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
