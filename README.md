# francgaya.com

Personal site of Franc Gaya, Application Reference Engineer at E.G.O. Appliance Controls.
Static, bilingual (English at the root, Spanish under `/es/`), no analytics, no tracking.

Built with [Astro](https://astro.build) and [Tailwind CSS](https://tailwindcss.com) v4,
compiled in GitHub Actions and served from GitHub Pages.

## Running it

The Node version is declared once, in `.nvmrc`, and read by both `nvm use` locally and
`actions/setup-node` in CI, so the two environments cannot drift apart.

First time, and after any change to `package.json` or `package-lock.json`:

```sh
nvm use          # Node 24, from .nvmrc
npm ci           # wipes node_modules and reinstalls the exact locked versions
```

Day to day:

```sh
npm run dev      # development server, Ctrl+C to stop it
npm run build    # static output in dist/
npm run preview  # serve that build locally
```

`nvm use` is per terminal, not per run: it sets the `PATH` of the shell you type it in, so it
is needed once in every new terminal. `npm ci` is not part of the daily loop, only of the two
cases above.

CI runs `nvm use`'s equivalent, `npm ci`, and `npm run build`, in that order. A build you
cannot reproduce on your own machine is a build you cannot debug on the day it breaks.

## Layout

```
src/
  components/    one file per component, reused across pages
  data/          the L2 glossary
  i18n/          the five pages, paired across languages
  layouts/       header, page body, CTA, footer
  pages/         file-based routing: the filename is the URL
  styles/        one global sheet: the theme and a handful of component utilities
public/          copied verbatim, including the CNAME for the custom domain
```

## Conventions

- **No committed build output.** `dist/` and the generated CSS stay out of the repository:
  a committed artifact drifts out of sync in silence, and the source is what is worth reading.
- **Fonts are self-hosted** through Fontsource, never loaded from a third-party CDN.
- **Folded content is in the HTML from the start.** Every `<details>` on the site ships its
  contents whether it is open or not, so the text is indexed, printed, and readable in the
  source. Folding is a visual device, not a loading strategy.
- **Progressive enhancement.** The site ships zero JavaScript. The mobile menu, the
  accordions, and the glossary popovers are all native HTML.
- **Content in the language of the page; identifiers, classes, and comments in English.**

## Working pages

`/ui-kit` collects every component on one page. It is a working page, marked `noindex`,
kept because it is the cheapest place to have a visual discussion.
