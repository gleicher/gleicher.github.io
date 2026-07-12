# Action Plan

*Prioritized roadmap from the July 2026 review — see [REVIEW.md](REVIEW.md) for rationale. Ordered by impact-per-effort; each phase leaves the site deployable.*

## Phase 0 — Bug fixes & content triage (an afternoon)

Independent of any theme decision; worth doing even if nothing else happens.

1. Fix `usablevr` → `usablearvr` in `content/_index.md:53` (restores the missing research theme on the homepage).
2. Fix "Papaer" typo in `content/video/2026_guitar/index.md` (visible on the videos landing page).
3. Fix `pullall.bat`: roadster's branch is `main`, not `master` (or make it per-submodule).
4. Delete one of the identical `layouts/shortcodes/summary.html` / `summary.md`.
5. Prune reachable scaffolding: `content/researchtheme/test/`, `content/badpage.md` or `content/pages/bad-page.md` (keep at most one), `content/pages/arxiv-test.md`, `content/problem-test.md`, empty `content/homepagepics/`.
6. Remove the stray 1.5MB `.ppt` from `content/talks/2001_02_animationbyadaptation/` (externalize via the GleicherAssets convention if worth keeping).
7. Decide the three `draft: true` posts: publish or delete.

## Phase 1 — Editorial refresh (independent of code; highest visitor-facing impact)

1. Update the "Current Research Themes" — the homepage currently *tells visitors* it's out of date. Rewrite the intro, re-sort current vs. past themes.
2. Add talks since mid-2024 (the section reading as dormant while videos run to 2026 is the most misleading staleness signal on the site).
3. Overhaul or retire `gradschoolfaq.md` ("almost comically out of date" by its own description). Even a short current version beats the 2010/2016 layer cake.
4. Refresh the homepage "Selected Recent Publications" list.
5. Compress the oversized images (3.5MB Teaser-01.jpg, 2.5MB study-design.png, 2.3MB relaxedIK.PNG, 1.7MB abstractsViewerStill.png, 1.4MB vr-teaser.jpg → target <300KB each; consider Hugo's image processing for thumbnails so originals stop shipping).

## Phase 2 — Structural consolidation (2–4 focused days; the core recommendation)

Goal: one theme, one template generation, one CSS bundle. Do this *before* the visual refresh so styling changes are cheap.

1. **Eliminate roadster.** Copy the six-ish files actually used into local `layouts/` / `assets/`: `_partials/{header,sidebar,mathjax,post_tags}.html`, `home.html`, `static/js/menu.js`; fold the 93-line `v2-styles.css` into the main SCSS (fixing its dangling `var(--color-*)` references). Remove the submodule from `.gitmodules` and `config.toml`. Verify with a clean `hugo` build + htmltest.
2. **Own the primary theme.** Either fork 559Theme into `themes/gleicher/` (or move it into the root `layouts`/`assets`) so this site stops tracking a course theme, or prune the shared theme carefully. Delete the ~35 unused shortcodes, `staff/` templates, course content stubs, and the html-hint library (replace the single `{{< tooltip >}}` use with a `title` attribute or drop it).
3. **Migrate to the modern template layout** (root `layouts/baseof.html`, `_partials/`; Hugo ≥0.146 conventions), rename `config.toml` → `hugo.toml`, lowercase the `[params]` tables, delete commented-out dead config. This removes the dual-generation lookup risk entirely.
4. **Unify CSS.** One `main.scss` entry; generate Hugo params into a single `_hugo-variables.scss` instead of templating logic throughout; resolve `themestyle = "old"` to concrete styles and delete both the switch and the dead branches; delete the dead dark-mode code in `menu.js` (or wire it up properly in Phase 3 — decide, don't carry).
5. Pin or vendor Lunr (currently unpinned from unpkg), and extract the inline JS/CSS from `baseof.html`/`head.html` into asset files.

## Phase 3 — Visual refresh (design time; now cheap to implement)

1. **Give the homepage a header and navigation.** Drop `noheader: true` (or design a slimmer homepage header variant). This single change fixes the mobile no-navigation problem and unifies the site.
2. **Restructure the homepage:** short landing section (photo, one-paragraph bio, prominent links to Papers/Talks/Videos/Advice), then compact research-theme cards; move the full teaching history to its own page. Aim for a homepage a visitor can absorb in one screen.
3. **Typography:** body 16–17px with ~1.6 line-height; consider a system-font stack (free performance win) or an intentional font pairing; establish a real heading scale.
4. **Color discipline:** keep UW red (#C5050C) as accent (header, headings, rules); use a quieter link treatment (darker red or underlined default-weight) so links stop shouting on link-dense pages.
5. **Modernize list pages:** replace paginated blog cards with year-grouped single-page archives for talks and videos (60–70 items don't need 6 pages); consider a responsive card grid for videos where thumbnails are the point.
6. Small credibility touches: favicon/social meta check, dark mode only if you actually want to maintain it, footer cleanup.

## Phase 4 — Optional / later

1. `.git` history slim-down (99MB for a 39MB tree). Only worth it if clone size annoys you; a BFG/filter-repo pass rewrites history, so coordinate with any other clones.
2. Consider generating the homepage publications list from a data file (`data/publications.yaml`) instead of hand-edited Markdown, making updates one-line edits.
3. Revisit whether talks should get the same `paperpage`-style cross-links videos have.
4. Re-evaluate restart (Option C in REVIEW.md) only if you decide you want a fundamentally different site structure; after Phase 2 you'll be in the best position to judge, and the migration cost will be at its lowest.

## Suggested sequencing

Phase 0 now; Phase 1 as editorial time permits (it's the most visitor-visible); Phase 2 as one concentrated block (don't interleave with content edits — it's a mechanical refactor best verified by diffing `hugo` output before/after); Phase 3 after 2, iteratively. Phases 0–1 are safe regardless of what you decide about 2–3.
