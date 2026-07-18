# Design & Implementation Review

*Prepared July 7, 2026. Companion document: [ACTION-PLAN.md](ACTION-PLAN.md).*

## Verdict in brief

The site is in better shape than "due for a rethink" might suggest: content is well-organized and consistently structured, the CI/deploy pipeline is modern and correct, and day-to-day content edits are safe. The liabilities are concentrated in the presentation stack. Two divergent forks of the same ancestor theme (Mainroad) are stacked across two different generations of Hugo's template system, held together by back-compat behavior; the CSS is three independently compiled bundles with dead branches; and the visual design is a decade-old blog aesthetic that under-serves an academic homepage. A **consolidation** (fold what's actually used into one local theme, drop roadster entirely, prune 559Theme's course cruft) gets most of the benefit of a restart at a fraction of the cost, and creates a clean base for a visual refresh. A from-scratch restart is defensible but not required — content migration risk is low either way because coupling runs through only ~6 shortcodes.

---

## Part 1: Design review (rendered site)

Inspected live at gleicher.sites.cs.wisc.edu, desktop (1440px) and mobile (390px).

### The homepage is the weakest page — and it's the one that matters

- **No navigation on the homepage.** `content/_index.md` sets `noheader: true`, which removes the banner *and* the menu bar. On desktop the sidebar "Sections" list substitutes; on mobile the sidebar drops to the bottom of a ~7,700px-tall page, so a phone visitor gets **no navigation at all** until they scroll past everything. Interior pages get a proper header and a mobile MENU toggle — only the homepage is broken this way. There is also no `<nav>` landmark on the homepage (accessibility).
- **It's a wall of text.** One long hand-authored Markdown file: bio → 10 research-theme summaries → full teaching history → curated publications. Everything a visitor might want is there, but nothing is prioritized. The "Current Research Themes" intro even says, on the live site, "The projects list was more than slightly out of date. I need to revitalize it."
- **One research theme silently missing.** `_index.md:53` calls `{{< summary "researchtheme/usablevr" >}}` but the directory is `usablearvr` — the shortcode resolves to nothing and drops without error. Concrete bug, one-line fix.
- **Red overload.** Every link renders bold UW-red (#C5050C). On a link-dense page this makes the red carry no signal; headings, links, and emphasis compete. UW red works better as an accent (header rule, headings) than as the body link color.

### Interior pages: dated but functional

Talks/videos lists and single pages are perfectly serviceable — Mainroad-style card lists with thumbnails, dates, and PDF/YouTube badges. The look is recognizably a ~2015 blog theme: 14px Open Sans body (small by current standards; 16–18px is the norm), tight 22px leading, boxed layout on a gray canvas, dark-red "badge" buttons. The clock/folder glyph metadata icons and "Read formatted page…" links feel bloggy for what is really a portfolio/archive. Pagination ("1/6 » (last)") on a 60-item archive is friction; a single year-grouped page would serve visitors better and helps search.

Nothing is *broken* visually: the layout is responsive, `<meta viewport>` is present, one `h1` per page, `lang` is set, link contrast (≈5.9:1) passes WCAG AA, no console errors from site code.

### Content staleness (independent of any theme work)

Talks end mid-2024 while videos run to 2026 — the gap reads as inactivity to a visitor who checks Talks. Research themes were last meaningfully edited Oct 2023 and are self-flagged as stale. `pages/Advice/gradschoolfaq.md` describes itself as "almost comically out of date" (last update 2010, "as of right now (August 2016)…"). Visible typo on the videos landing page: "TVCG Papaer" (`content/video/2026_guitar/index.md`). Test/scaffolding content is reachable: `researchtheme/test/` (2 words), `badpage.md` + `pages/bad-page.md`, `pages/arxiv-test.md`, empty `homepagepics/`.

---

## Part 2: Implementation review

### Theme architecture: two forks of one theme, cross-woven

Both 559Theme and roadster descend from Mainroad. They are stacked (`theme = ["559Theme","roadster"]`) but the layering is not primary-plus-fallback in practice — rendering a single page draws from both:

| From 559Theme (old template layout: `_default/`, `partials/`) | From roadster (new layout: root `layouts/`, `_partials/`) |
|---|---|
| baseof, head, menu, logo, footer, list/summary templates, 11 widgets, 47 shortcodes, main SCSS | header, sidebar, mathjax, post_tags partials; `home.html`; `menu.js`; `v2-styles.css` |

The two themes use **different generations of Hugo's template system**, and the site works because Hugo currently unifies `partials/` and `_partials/` lookups. That is the single biggest fragility: a future Hugo release that tightens template resolution could break the site in non-obvious ways, and debugging "which theme rendered this?" requires holding the whole cross-theme map in your head.

Roadster earns its 3.5MB submodule badly: ~90% is dead weight (an unloaded 1,424-line `style.css`, 24 i18n files, its own full layout set shadowed by 559Theme, and an `examplesite/` that recursively vendors the theme three levels deep). It exists to supply roughly six files. 559Theme, meanwhile, carries its course-site heritage: of its 47 shortcodes, only ~10 are used by this site; `staff/` templates, course content stubs, and a vendored ~2,000-line html-hint tooltip library (used by exactly one tooltip in all content) ride along.

### CSS: three bundles, dead branches, latent breakage

- Three independently compiled stylesheets that cannot share variables: `main.scss` (via Hugo Pipes + Dart Sass), roadster's `v2-styles.css`, and the `customCss` files. Colors are redefined across them.
- `main.scss` is Go-template-inside-SCSS (`ExecuteAsTemplate`), which defeats SASS tooling/linters. `themestyle = "old"` conditionals thread through ~2,000 lines of SCSS — a permanent branch whose other side is never taken.
- **Dead dark-mode subsystem**: `menu.js` ships full theme-toggle logic, but the live baseof has no toggle button and no loaded CSS contains a single `prefers-color-scheme` or `data-theme` rule. Light-only site carrying inert machinery.
- **Dangling CSS variables**: `v2-styles.css` (loaded) references `var(--color-menu-bg)` etc., defined only in roadster's `style.css` (never loaded). Harmless today only because the menu is flat; a trap for the next change.
- The theme's own `themes/559Theme/CRITIQUE.md` already diagnoses all of this accurately and sketches the right refactor.

### What's in good shape

- **CI/deploy**: `.github/workflows/hugo.yml` is current best practice — pinned Hugo 0.163.3 extended, artifact-based Pages deploy, least-privilege permissions, submodule + GitInfo handling correct. The recent `[security] allowContent` CVE fix is applied.
- **Config**: modern in substance (current pagination key, JSON output for Lunr search). Cosmetic nits only: legacy `config.toml` name, mixed-case `[Params]`, commented-out dead keys.
- **Content model**: page bundles with highly consistent per-section front matter (`extpdfs`/`extvideos`/`youtube`/`paperpage`), heavy media correctly externalized to GleicherAssets via `fixer.py`. Raw-HTML dependence (Goldmark `unsafe=true`) is light — 13 files.
- **JS**: minimal and framework-free. One `menu.js`, per-page Lunr search, MathJax. (Lunr loads unpinned from unpkg — pin or vendor it.)

### Concrete bugs & hygiene items

1. Homepage `usablevr` → should be `usablearvr` (`content/_index.md:53`).
2. `pullall.bat` checks out `master` on both submodules; roadster's branch is `main` — silently fails.
3. `layouts/shortcodes/summary.html` and `summary.md` are byte-identical duplicates; Hugo picks one arbitrarily.
4. "TVCG Papaer" typo in `content/video/2026_guitar/index.md` (visible on the videos landing page).
5. Stray 1.5MB PowerPoint checked into `content/talks/2001_02_animationbyadaptation/`.
6. Unoptimized in-repo images: 3.5MB `commchar/Teaser-01.jpg`, 2.5MB `2019_tongs/study-design.png`, 2.3MB `relaxedIK.PNG`, 1.7MB AbstractsViewer still, 1.4MB `vr-teaser.jpg` (page-load cost wherever used, repo cost everywhere).
7. `.git` is 99MB against a 39MB working tree — history bloat from pre-externalization binary churn. Cosmetic unless it bothers you.
8. Test/scaffolding content listed in Part 1; 3 of 4 posts are `draft: true` limbo.

### Maintainability assessment

Low-velocity-safe, refactor-hostile. Content edits: fine indefinitely. Styling or layout changes: you must reason about three CSS bundles, template logic inside SCSS, two theme generations, and dead code that looks live. The stack is far heavier than a single-author academic site warrants; consolidation would cut theme surface area by more than half and remove every "works only by luck" dependency.

---

## Part 3: Options (cleanup → restart)

> **Update (2026-07-15): Option B happened, but as a shared-theme
> unification across all four Gleicher/CS559 Hugo sites, not a local
> fork of 559Theme for this site alone.** Roadster is gone, the CSS is one
> SASS pipeline with style presets, and this site's look is preserved as the
> `mainroad-sans` preset. See `ACTION-PLAN.md`'s Phase 2 update and
> `themes/559Theme/THEME-PLAN.md` for what actually happened. Options A/C
> below are now moot in the "which structural path" sense; Option B's Part 3
> framing (comparing restart-cost vs. consolidation-cost) is still accurate
> reasoning if a *visual* restart is ever reconsidered — the structural risk
> it warned about is resolved either way.

**Option A — Fix and freeze.** Fix the bugs and stale content, touch nothing structural. Days of effort, but every future styling change stays expensive and the Hugo back-compat risk remains.

**Option B — Consolidate into one local theme, then refresh visuals. (Recommended.)** Vendor the ~6 roadster files 559Theme lacks into local `layouts/`/`assets/`, drop the roadster submodule; prune or locally fork 559Theme (delete ~35 unused shortcodes, course templates, html-hint); migrate to the modern template layout and `hugo.toml`; unify the CSS into one SCSS bundle with the `themestyle` branch resolved. *Then* do the visual refresh (type scale, homepage restructure, color discipline) on a codebase where CSS changes are cheap. This removes every structural risk while preserving all templates/content that work. Roughly 2–4 focused days for consolidation, plus design time.

**Option C — Restart on a modern theme (or minimal custom theme).** Content migration risk is genuinely low: front matter is theme-agnostic, and coupling is confined to six shortcodes you'd re-implement (`summary` + its render layout, `coauths`, `leftpic`, `assetlink`, `link`, `tooltip`) plus the talks/video single templates that consume `extpdfs`/`extvideos`. The catch: academic-personal-site themes rarely fit a talks-and-videos archive of this shape, so you'd be writing those templates anyway — at which point Option C converges on Option B with a new coat of paint. Choose C only if you want a fundamentally different site structure (e.g., a compact landing page with the archive demoted), not just a better-looking version of this one.

A practical note: Option B's endpoint leaves you with a small, single-purpose local theme you fully understand — which is also the best possible starting position if you later decide on C.
