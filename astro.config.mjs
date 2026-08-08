// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

// Decisions here come from web/design/adr-001-stack.md, section 7.1.
// No `base`: the repository is francgaya.github.io (user site) and there is a
// custom domain, so setting it would break every internal link.
export default defineConfig({
  site: 'https://francgaya.com',
  i18n: {
    locales: ['en', 'es'],
    defaultLocale: 'en',
    // English at the root, Spanish under /es/. The link Franc pastes on
    // LinkedIn has to serve content, not a client-side redirect.
    routing: { prefixDefaultLocale: false },
  },
  // The only integration on the project, and adr-001 section 8 allowed for it
  // by name: "no integration added, not even sitemap, unless P-16c asks for
  // one". It does.
  //
  // The i18n option is deliberately NOT used. It pairs pages by prefix, and the
  // slugs here are translated (/career and /es/trayectoria), so it would emit
  // wrong pairs. The hreflang links in BaseLayout already say it correctly.
  integrations: [
    sitemap({
      // /ui-kit is published on purpose but is a working page, so it stays out
      // of the sitemap. It is NOT in robots.txt Disallow: blocking it there
      // would stop the crawler reading its own noindex, which is the opposite
      // of what is wanted. The 404 never gets in: Astro leaves it out itself.
      filter: (page) => !page.includes('/ui-kit'),
    }),
  ],
  vite: { plugins: [tailwindcss()] },
});
