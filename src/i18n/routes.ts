/**
 * The five pages of the site, paired across languages.
 *
 * Astro's i18n helpers cannot do this on their own: the `path` option of
 * `locales` customises the LANGUAGE PREFIX, not the page slug, so
 * getRelativeLocaleUrl('es', 'career') would return /es/career, which does not
 * exist. Five rows of data are cheaper than an i18n integration, and they
 * double as the site map. See adr-001-stack.md, section 6.4.
 *
 * Anchors are English in both languages, so the language switcher can carry
 * the hash across verbatim.
 */
export type Locale = 'en' | 'es';

export interface Route {
  /** Stable identifier, used to look a page up regardless of language. */
  id: 'home' | 'what-i-do' | 'career' | 'toolkit' | 'about';
  en: string;
  es: string;
  labelEn: string;
  labelEs: string;
}

export const ROUTES: readonly Route[] = [
  { id: 'home',      en: '/',           es: '/es/',              labelEn: 'Home',       labelEs: 'Inicio' },
  { id: 'what-i-do', en: '/what-i-do/', es: '/es/lo-que-hago/',  labelEn: 'What I do',  labelEs: 'Lo que hago' },
  { id: 'career',    en: '/career/',    es: '/es/trayectoria/',  labelEn: 'Career',     labelEs: 'Trayectoria' },
  { id: 'toolkit',   en: '/toolkit/',   es: '/es/herramientas/', labelEn: 'Toolkit',    labelEs: 'Herramientas' },
  { id: 'about',     en: '/about/',     es: '/es/sobre-mi/',     labelEn: 'About',      labelEs: 'Sobre mi' },
];

/** Navigation entries for one language, in menu order. */
export function navFor(locale: Locale) {
  return ROUTES.map((r) => ({
    id: r.id,
    href: locale === 'en' ? r.en : r.es,
    label: locale === 'en' ? r.labelEn : r.labelEs,
  }));
}

/** The same page in the other language. */
export function alternateOf(id: Route['id'], locale: Locale): string {
  const route = ROUTES.find((r) => r.id === id);
  if (!route) throw new Error(`Unknown route id: ${id}`);
  return locale === 'en' ? route.es : route.en;
}

export const SWITCH_LABEL: Record<Locale, string> = {
  en: 'Castellano',
  es: 'English',
};
