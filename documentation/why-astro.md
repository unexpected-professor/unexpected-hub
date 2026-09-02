# Why Astro for the website

Decision record expanding ADR-004. Astro was chosen for the public site in
`apps/site/`. This note explains the reasoning and what the alternatives would
have cost, so the choice can be re-evaluated deliberately rather than by habit.

## The framing question: what shape is this?

Static-site tools cluster into three archetypes, and the right tool depends on
which one the project is:

| Shape | Typical tools | Is this us? |
|---|---|---|
| Linear textbook / handbook | mdBook, Quarto, VitePress | No — lessons are a growing library, not a fixed sequence |
| Documentation portal (versioned, API-style, search-first) | Docusaurus, MkDocs Material, Starlight | Partly |
| A website that hosts a lesson library and embeds interactive tools | **Astro**, Eleventy | **Yes** |

The Unexpected Professor site is a public identity with a landing page, an
About page, a lesson library, a lab catalogue, and legal pages — with bespoke
interactive components (a consent-gated video embed, an embedded Dash lab). It
is a website that contains teaching material, not a documentation set.

## Why Astro fits

1. **Islands architecture.** Pages ship zero JavaScript by default; only
   components that need it hydrate (`YouTubeEmbed`, `LabEmbed`). This is the
   mechanism that makes "a useful page must remain readable when JavaScript is
   unavailable" (hub section 7.1) real rather than aspirational. Portal-style
   generators hydrate the whole page as a single-page app.
2. **Bring-your-own components.** The consent gate and the lab iframe wrapper
   are project-specific. In Astro they are plain `.astro` components. mdBook
   would need preprocessor hacks; VuePress/VitePress restrict you to Vue;
   Docusaurus means overriding theme internals.
3. **Schema-validated content collections.** `src/content.config.ts` rejects a
   malformed lesson at build time — already caught issues during development.
   Hugo, Eleventy and mdBook offer nothing equivalent without extra work.
4. **One coherent system** for marketing pages and lessons, rather than a docs
   theme with a separate site bolted alongside it.
5. **Portable static output, no runtime lock-in.** Plain HTML/CSS, no Vue or
   React runtime shipped to visitors. Matches the "keep the platform portable"
   principle — it moves between hosts trivially.

## The alternatives, and what they would have cost

| Tool | Language | Model | Maths | Custom interactivity | Docs UX built in | Maintained (2026) |
|---|---|---|---|---|---|---|
| **Astro** (chosen) | JS | General framework, islands | KaTeX / rehype | Excellent (any framework, partial hydration) | No — add Starlight or Pagefind | Very active (v5) |
| Astro + Starlight | JS | Astro's docs theme | KaTeX | Excellent | Yes | Very active |
| VitePress | JS / Vue | Docs SSG | markdown-it plugin | Vue only | Yes | Active |
| VuePress 2 | JS / Vue | Docs SSG | plugin | Vue only | Yes | Low momentum |
| Docusaurus 3 | JS / React | Docs portal | KaTeX | React, heavier runtime | Yes (+ Algolia) | Very active |
| mdBook | Rust | Linear book | MathJax | Very limited (preprocessors) | Yes | Active |
| MkDocs Material | Python | Docs | plugin | Limited | Yes (excellent) | Very active |
| Hugo | Go | General SSG | shortcodes / passthrough | Manual | Partial (themes) | Very active |
| Quarto | R / Python | Scientific publishing | Best in class, + PDF export | Awkward | Partial | Active, growing |
| Eleventy | JS | Minimal SSG | plugin | Zero-JS but all DIY | No | Active |

Two alternatives were genuinely defensible:

- **Quarto** — if rigorous maths typesetting, PDF export of each lesson, and
  running Python to generate figures mattered more than a custom-designed
  site. Worth revisiting if the project ever wants a printable course reader.
- **Docusaurus / VitePress / MkDocs Material** — if a turnkey docs sidebar,
  built-in search, and versioning were worth accepting a more constrained
  visual design and more shipped JavaScript.

## What Astro does not give us for free

- **Navigation** beyond what we build. We assemble the header, footer, and
  (later) a per-sequence sidebar ourselves.
- **Search.** Not built in. Plan: [Pagefind](https://pagefind.app/) — static,
  index-at-build, no external service.
- **Docs niceties** (versioning, an opinionated sidebar, admonition styles).
  `Starlight` would provide these but constrains page design; if the site ever
  becomes primarily reference documentation, reconsider it then.

## Structural ideas worth borrowing

`learn.libre.solar` (an OER on DC energy systems, built on the now-EOL VuePress
1.x — a reminder to track upstream maintenance) has a well-structured layout
worth imitating:

- a persistent left sidebar with a chapter tree plus previous/next;
- a per-page "last updated" date and a "suggest an edit on GitHub" link;
- prominent OER / Creative Commons framing and funder logos in the footer;
- subject-based top-level sections as real landing pages, not a flat list;
- built-in search.

These are collected as a post-pilot backlog item (UPH-036).

## When to revisit this decision

- The site becomes primarily reference documentation → evaluate Starlight.
- A printable / PDF course reader becomes a requirement → evaluate Quarto.
- Astro's maintenance or breaking-change cadence becomes a burden → the static
  HTML output and Markdown content are portable; migration cost is mostly the
  components and layouts, not the content.
