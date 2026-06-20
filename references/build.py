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
    sys.stdout.write("built %s — %s\n" % (out, note))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
