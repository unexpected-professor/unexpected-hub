// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

// The canonical public hostname (ADR-011, UPH-002). Every absolute URL, the
// sitemap, and the feed are derived from this single value.
export const SITE_URL = 'https://theunexpectedprofessor.com';

// https://astro.build/config
export default defineConfig({
  site: SITE_URL,
  output: 'static',
  trailingSlash: 'never',
  build: {
    format: 'directory',
  },
  integrations: [
    mdx(),
    sitemap({
      filter: (page) => !page.includes('/404'),
    }),
  ],
  markdown: {
    // KaTeX / MathML pipeline is selected in a later commit after a render
    // comparison (hub section 7.1); no math plugin is wired in yet.
    shikiConfig: {
      theme: 'github-light',
      wrap: true,
    },
  },
});
