// @ts-check
import { defineConfig } from 'astro/config';
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
  vite: { plugins: [tailwindcss()] },
});
