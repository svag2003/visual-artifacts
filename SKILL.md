---
name: html-it
description: Turn any project, codebase, or idea into one shareable HTML "Visual Artifact" — a diagram-driven explainer with three tabs (Technical Architecture, User Workflow, Business Strategy) that a human can see and an agent can read straight from the HTML (no OCR). Self-contained by default; works offline, on localhost, or published to any static host. Use when the user says "html-it <target>", or asks for a visual/HTML diagram, architecture map, explainer, or one-pager of a system, project, or concept.
---

# html-it — Visual Artifacts

Produce ONE HTML file that explains a target through **drawn diagrams**, not a wall of text, across three switchable lenses:

- **Technical Architecture** — how the system is built (components, data flow, integrations).
- **User Workflow** — how a person actually moves through it.
- **Business Strategy** — what it is, who it's for, how it wins or makes money.

The same file serves two readers at once: a **human** opens it and sees the picture; an **agent** fetches it and reads the architecture directly, because every diagram is Mermaid *text* and every lens is a tagged HTML section. One link, two audiences — that is the point.

## What "good" means here (the bar to clear)
**Visual-first, always.** The reader should understand the system by *looking*, not reading. Text earns its place only as a one-line intro per lens and as figure captions.
1. **Carry each lens with diagrams, not prose.** Aim for **2+ diagrams per tab** (a structure diagram *and* a workflow/sequence). Show branching, layers, loops, and how things move — not a paragraph describing them.
2. **Turn facts into visuals.** A list of components → a `.board` of cards or a diagram. A comparison → a `.matrix`. Numbers → `.stat` cards. A pipeline → a `.flow` band or a funnel. Reach for a plain `<table>` ONLY when the data is genuinely tabular (a real truth/spec table).
3. **No walls of text.** Cap prose at one `.lead` line per lens + short captions/callouts. If you've written a paragraph, it probably wants to be a diagram or a card grid.
4. **Cohesive look.** The component kit + auto-themed Mermaid (palette-matched, not default blue) make every artifact feel designed. Use the kit; don't hand-roll one-off styles.
5. **Honest and dated.** Put the generation date in; date any "current status" claim so a stale file reads as a snapshot, not a lie.
6. **Readable by an agent.** Keep the structure conventional (below) so any agent can parse it without OCR.

## Procedure

### 1. Resolve the target (works on ANYTHING — no special setup)
- **A codebase / repo:** read its `README`, top-level layout, key config/manifests (`package.json`, `requirements.txt`, IaC, CI), and entry points. Infer the architecture from what's actually there. If a richer brief exists (a design doc, a `BMP.md`, an issue), use it — but never *require* one.
- **An idea or concept** described in chat: build from the description and your own knowledge; only research further if asked.
- If the target is ambiguous, state your best read in one sentence and proceed — don't bounce it back.

### 2. Author the three lenses
Copy `references/template.html` and fill the placeholders: `{{TITLE}}`, `{{SUBTITLE}}`, `{{DATE}}`, `{{TAB_TECHNICAL}}`, `{{TAB_USER}}`, `{{TAB_BUSINESS}}`. Leave the `<!--MERMAID_RUNTIME-->` marker untouched — the build step fills it.

Each tab = **2+ diagrams + visual blocks + a one-line intro.** Aim for a *structure* diagram and a *workflow* diagram per lens. Suggested per lens:

| Lens | Diagram 1 (structure) | Diagram 2 (workflow) | Visual blocks |
|------|----------------------|----------------------|---------------|
| Technical | `flowchart` of the real topology — services, stores, externals, layered with `subgraph` | `sequenceDiagram` or `flowchart` of one request/data path end to end | `.board` of subsystem status, `.flow` for a pipeline |
| User Workflow | `sequenceDiagram` of a real user journey | `flowchart` of the decision/state path (branches, retries) | `.flow` happy path, `.callout` for the key moment, `.stat` for numbers |
| Business Strategy | `flowchart` of the model/value loop | (optional) journey or growth flow | `.stat` cards, `.funnel` for the value funnel, `.matrix` for positioning |

**Mermaid tips:** keep each diagram readable (~5–12 nodes; split if bigger). Label edges (`A -->|writes| B`). Subgraphs for layers. Put the diagram in:
```html
<figure class="diagram">
  <pre class="mermaid">
flowchart LR
  U([User]) -->|HTTPS| API[API Gateway]
  API --> L[Lambda]
  L --> DB[(DynamoDB)]
  </pre>
  <figcaption>One line on what the reader is looking at.</figcaption>
</figure>
```
Do not HTML-escape inside `<pre class="mermaid">` — write raw Mermaid. (Avoid characters Mermaid chokes on in labels; wrap tricky labels in quotes.)

**Component kit** (already styled in the template — just emit the markup; Mermaid is auto-themed to the palette, so don't set diagram colors yourself):
- `<div class="flow"><div class="node"><span class="i">📦</span><span class="t">Title</span><span class="s">sub</span></div><div class="arrow">→</div>…</div>` (`node ai` accents a node; the `<span class="i">` icon is optional)
- `<div class="board"><div class="cell"><span class="i">⚙️</span><span class="dot ok"></span><span class="h">Head</span><div class="d">detail</div></div>…</div>` (dot: `ok|warn|idle|bad`; icon optional)
- `<div class="stats"><div class="stat"><span class="num">42</span><span class="label">what it counts</span></div>…</div>`
- `<div class="funnel"><div class="frow">stage<span class="s">note</span></div><div class="fdrop">▼</div>…</div>` (`frow ok|bad`)
- `<div class="matrix"><div class="quad"><div class="h">Axis label</div><div class="d">detail</div></div>…</div>` (a 2×2 — great for positioning instead of a table)
- `<div class="callout"><strong>The point.</strong> One thing the reader must not miss.</div>`
- `<span class="tag ok|warn|idle">label</span>` inside tables; wrap any real `<table>` in `<div class="tablewrap">…</div>` so it scrolls on mobile.
- Two diagrams side by side: wrap them in `<div class="grid2">…two `<figure class="diagram">`…</div>`.
- Section headers: `<h2>UPPERCASE LABEL</h2>`; open a tab with a single `<p class="lead">` line — then go visual.

**Mobile, zoom, and color themes are automatic** — the template is responsive (matrix/flow reflow on phones), makes every `<figure class="diagram">` tap-to-zoom (pinch / drag / wheel), and ships a built-in **theme switcher** (5 palettes — Amber, Indigo, Emerald, Rose, Slate) that re-themes both the UI and the Mermaid diagrams and persists the choice. Author normally with the component-kit classes and let diagram colors come from the theme — **do not hardcode colors** anywhere (no inline `style="color:…"`, no Mermaid `%%{init}%%` color blocks), or you break theme switching.

Light emoji icons (`<span class="i">`) on nodes/cards/headers are encouraged as visual anchors — one per item, tasteful, never decorative clutter.

The Overview-equivalent rule: **the Technical tab must stand on its own** — someone who reads only it should still get what the system is.

### 3. Save the draft
Write to an output file. Default location: a `visual-artifacts/` folder (create it if missing) in the user's project, named `<kebab-slug>--<YYYY-MM-DD>.html`; if it exists, suffix `-2`, `-3`. Never overwrite a prior generation — they are history.

### 4. Build (inject the diagram runtime)
```bash
python3 <skill>/references/build.py visual-artifacts/<slug>--<date>.html
```
- **Default = self-contained:** inlines Mermaid (~3.3 MB) so the file works fully offline, on `localhost`, or emailed — and makes zero outside calls (private by default).
- **`--lightweight`:** swaps in a CDN `<script>` (tiny file, needs internet). Use only when publishing many artifacts to one host.

If `references/mermaid.min.js` is missing (fresh install), vendor it once:
`curl -fsSL https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js -o <skill>/references/mermaid.min.js`

### 5. Deliver
Open it locally (`open` on macOS) and hand it to the user. If they want to share publicly, see **Publishing**.

## Agent-readability convention (keep this stable)
So any agent can read an artifact without OCR or a text extractor:
- Each lens is `<section class="view" data-lens="technical|user|business">`.
- Every diagram's source is plain text inside `<pre class="mermaid">`.
- Facts live in semantic HTML (the component kit + tables), not in images.
The diagram a human sees IS the text an agent reads — one source, no separate JSON, no drift.

## Publishing (optional — the skill only generates)
The file is static; host it anywhere and send the link. Same URL works for a human (renders) and an agent (reads HTML).
- **GitHub Pages** (free public link): commit the `.html` to a repo, enable Pages, share the URL.
- **Any static host:** S3+CloudFront, Netlify, Vercel, or a plain web server. Self-contained mode is most robust (no CDN dependency).
- **Private:** just don't publish — open the file or serve it on `localhost`; no one else can see it.

## Style rules
- Lead every section with its point. Plain language; no jargon walls.
- Tables only for genuinely enumerable facts; reasoning goes in prose.
- Be honest about status; date "current state" claims.
- Self-contained output must work years from now — that's why Mermaid is vendored, not assumed-online.
