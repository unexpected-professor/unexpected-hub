# The Unexpected Professor — website

Astro static site for the public lesson library (hub sections 5 and 7).

## Requirements

- Node 22 LTS (see `.nvmrc`). With nvm: `nvm use`.

## Local development

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # astro check + static build into ./dist
npm run preview  # serve the built site locally
```

## Content

Lessons are Markdown/MDX files under `src/content/lessons/`. The front-matter
contract is enforced by `src/content.config.ts`. A lesson with `draft: true` is
shown in `dev` but excluded from production builds, the RSS feed, and search
indexing.

## Structure

- `src/pages/` — routes (`index`, `about`, `lessons/`, `labs/`, `404`, `rss.xml`).
- `src/layouts/BaseLayout.astro` — HTML shell, canonical URL, metadata, skip link.
- `src/components/` — header (subject-based navigation) and footer.
- `src/styles/global.css` — temporary token-based visual system, light/dark.
- `astro.config.mjs` — `SITE_URL`, sitemap and MDX integrations.

## Not yet wired in

Mathematics rendering (KaTeX or MathML, pending a render comparison), the full
canonical lesson template, the consent-gated YouTube component, and the
legal/privacy pages. These are separate commits in the project sequence.
