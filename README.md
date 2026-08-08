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
npm run verify   # check the build, after npm run build
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
- **One paragraph, one line.** A `<p>`, `<li>`, heading, `<summary>` or text-bearing
  `<Fragment>` keeps its opening tag, its text, and its closing tag on a single line, however
  long that line gets. Turn word wrap on in the editor; do not wrap it in the file.

  This is not a preference. HTML collapses the newline between running text and an inline
  element into nothing, so

  ```astro
  lives on its own page:
  <a href="/toolkit/">Toolkit</a>
  ```

  renders as `page:Toolkit`. The escapes are a literal `&#32;` or the hanging-bracket trick
  (`</a` on one line, `>` on the next) that code formatters emit for exactly this reason, and
  both are harder to read than the long line they avoid. Comments and attribute lists holding a
  JSX expression are exempt: neither is rendered text, so neither can lose a space.

  `scripts/reflow.py` applied this to the existing files once; `npm run verify` is what proves
  no space has been lost since.

## Verifying a build

`npm run verify` runs `scripts/verify.py` against `dist/`, never against the source. It needs
Python 3 and `beautifulsoup4` (`pip install beautifulsoup4`), which is why it is a separate
command rather than part of `npm run build`.

It checks that no JavaScript file is emitted, that no font is fetched from a third-party CDN,
that every folded passage carries its text in the HTML and none of them ships open, that the
banned characters are absent, that no internal link or anchor is dead, that the language
switcher points at the equivalent page, that each glossary term is marked once per page with
its own popover anchor, and finally that each built page still says exactly what its file in
`web/content/` says, word by word.

That last check is the one that pays for the script. It caught three lost spaces before a
glossary term in P-16, which nobody would find by reading the page.

## Working pages

`/ui-kit` collects every component on one page. It is a working page, marked `noindex`,
kept because it is the cheapest place to have a visual discussion.
