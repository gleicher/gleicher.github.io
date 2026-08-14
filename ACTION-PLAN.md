# Action Plan

*Prioritized roadmap from the July 2026 review — see [REVIEW.md](REVIEW.md) for rationale. Ordered by impact-per-effort; each phase leaves the site deployable.*

> **STATUS AUDIT (2026-08-14).** Work stopped 2026-07-18. Phases 0 and 2 are
> essentially complete; Phases 1, 3, and 4 were never started. Each item below
> is marked ✅ DONE / ⬜ OPEN against the actual repo state. **This document is now
> a historical record — the live plan is
> [ACTION-PLAN-Aug26.md](ACTION-PLAN-Aug26.md).**

## Phase 0 — Bug fixes & content triage (an afternoon) — ✅ DONE except item 7

Independent of any theme decision; worth doing even if nothing else happens.

1. ✅ **DONE** — Fix `usablevr` → `usablearvr` in `content/_index.md:53` (restores the missing research theme on the homepage).
2. ✅ **DONE** — Fix "Papaer" typo in `content/video/2026_guitar/index.md` (visible on the videos landing page).
3. ✅ **DONE (differently)** — Fix `pullall.bat`. Moot as written: roadster is gone. The script now does `git -C themes/559Theme checkout master` before the recursive pull.
4. ✅ **DONE** — Delete one of the identical `layouts/shortcodes/summary.html` / `summary.md`. (`summary.md` is gone.)
5. ✅ **DONE** — Prune reachable scaffolding. `researchtheme/test/`, `content/badpage.md`, `pages/arxiv-test.md`, `content/problem-test.md`, and `content/homepagepics/` are all gone; `content/pages/bad-page.md` survives, which is the "keep at most one" allowance.
6. ✅ **DONE** — Remove the stray 1.5MB `.ppt` from `content/talks/2001_02_animationbyadaptation/`.
7. ⬜ **OPEN** — Decide the three `draft: true` posts: publish or delete. Still three, and they are not the same three the review counted: `content/posts/main-supervised.md` (36 lines — also tracked in [TO-DO.md](TO-DO.md)), `content/pages/webstuff/hugo.md` (11 lines), `content/pages/Advice/literature.md` (41 lines).

## Phase 1 — Editorial refresh — ⬜ ALL OPEN

*(Independent of code; highest visitor-facing impact. Nothing here was started.)*

1. ⬜ **OPEN** — Update the "Current Research Themes" — the homepage currently *tells visitors* it's out of date. Rewrite the intro, re-sort current vs. past themes. (`content/_index.md:47` still reads "The projects list was more than slightly out of date. I need to revitalize it.")
2. ⬜ **OPEN** — Add talks since mid-2024. Latest is still `content/talks/2024_06_CVPR/`; videos run to `2026_guitar/`.
3. ⬜ **OPEN** — Overhaul or retire `gradschoolfaq.md`. Untouched since 2023-09-10; still self-describes as "almost comically out of date," with the 2016 and 2010 update layers intact.
4. ⬜ **OPEN** — Refresh the homepage "Selected Recent Publications" list (newest entry is a 2025 arXiv item). *Also newly noticed:* the Teaching section says CS559 "Spring of 2025" while the top of the same page says "CS559 Spring 2026" — the page contradicts itself.
5. ⬜ **OPEN** — Compress the oversized images. Unchanged and now measured on the built output: **42MB build**, with `commchar/Teaser-01.jpg` 3.4MB, `2019_tongs/study-design.png` 2.5MB, `2018_RelaxedIK/relaxedIK.PNG` 2.2MB, `2023_AbstractsViewer/abstractsViewerStill.png` 1.6MB, `2002_06_npar/Screenshot` 1.5MB, `usablearvr/vr-teaser.jpg` 1.4MB, and ~20 more over 500KB. **But the review's framing of this item was too broad** — measured 2026-08-14, the homepage (236KB), list pages (182–242KB), and video/talk single pages (45KB) are all already light, because the theme's resizing works. The only pages that actually ship a full-size image to a viewer are the five `researchtheme/` pages (`commchar` = 3.6MB), caused by the local `layouts/researchtheme/single.html` override. Everything else large is an unreferenced page-bundle resource that no visitor downloads. See ACTION-PLAN-Aug26 Track B.

## Phase 2 — Structural consolidation — ✅ DONE, via a different path than proposed below

> **Update (2026-08-14):** confirmed complete and *shipped*. Beyond the July 15
> note below: the site's Phase 6 migration landed (`config.toml` → `hugo.toml`,
> `themestyle` → `params.style.preset = "mainroad-sans"`, `lunr` → `search`
> widget, `[params]` lowercased), the theme was pushed to
> `origin/master` on `github.com/CS559/559Theme`, and this site is pushed to
> `gleicher/gleicher.github.io` and deploying via GitHub Actions. The submodule
> is currently 3 commits behind `origin/master` (docs + one link fix — trivial).
> The theme's own deprecation checker reports **zero** deprecated-shortcode uses
> in this site's content. Residual site-side cleanup is small and is carried
> forward to ACTION-PLAN-Aug26, not tracked here.
>
> **Update (2026-07-15):** this phase happened, but not the way items 1–4
> below describe. Instead of this site forking/owning its own copy of the
> theme, the **shared 559Theme absorbed roadster once, for all four
> consumer sites** (a cross-repo "theme unification" project — canonical
> record: `themes/559Theme/THEME-PLAN.md`). This site still tracks the
> shared theme, it just no longer needs a second `roadster` submodule to do
> it, and `themestyle` became `params.style.preset = "mainroad-sans"` (this
> site's look, preserved byte-for-byte — see the preset's doc comments).
> Item 5 (Lunr) is also done, differently: Lunr was replaced entirely by a
> vendored, no-CDN MiniSearch (`docs/search.md` in the theme). The list
> below is kept for the *reasoning* (still valid explanation of the original
> problem) — don't treat it as a live task list; see Phase 3 below for
> what's actually still open on this site.

Goal: one theme, one template generation, one CSS bundle. Do this *before* the visual refresh so styling changes are cheap.

1. **Eliminate roadster.** Copy the six-ish files actually used into local `layouts/` / `assets/`: `_partials/{header,sidebar,mathjax,post_tags}.html`, `home.html`, `static/js/menu.js`; fold the 93-line `v2-styles.css` into the main SCSS (fixing its dangling `var(--color-*)` references). Remove the submodule from `.gitmodules` and `config.toml`. Verify with a clean `hugo` build + htmltest.
2. **Own the primary theme.** Either fork 559Theme into `themes/gleicher/` (or move it into the root `layouts`/`assets`) so this site stops tracking a course theme, or prune the shared theme carefully. Delete the ~35 unused shortcodes, `staff/` templates, course content stubs, and the html-hint library (replace the single `{{< tooltip >}}` use with a `title` attribute or drop it).
3. **Migrate to the modern template layout** (root `layouts/baseof.html`, `_partials/`; Hugo ≥0.146 conventions), rename `config.toml` → `hugo.toml`, lowercase the `[params]` tables, delete commented-out dead config. This removes the dual-generation lookup risk entirely.
4. **Unify CSS.** One `main.scss` entry; generate Hugo params into a single `_hugo-variables.scss` instead of templating logic throughout; resolve `themestyle = "old"` to concrete styles and delete both the switch and the dead branches; delete the dead dark-mode code in `menu.js` (or wire it up properly in Phase 3 — decide, don't carry).
5. Pin or vendor Lunr (currently unpinned from unpkg), and extract the inline JS/CSS from `baseof.html`/`head.html` into asset files.

## Phase 3 — Visual refresh — ⬜ ALL OPEN

*(Design time; now cheap to implement, since Phase 2 landed. Nothing here was started.)*

1. ⬜ **OPEN** — **Give the homepage a header and navigation.** Drop `noheader: true` (or design a slimmer homepage header variant). This single change fixes the mobile no-navigation problem and unifies the site. (`content/_index.md:4` still sets `noheader: true`; the theme still honors it at `baseof.html:16`.)
2. ⬜ **OPEN** — **Restructure the homepage:** short landing section (photo, one-paragraph bio, prominent links to Papers/Talks/Videos/Advice), then compact research-theme cards; move the full teaching history to its own page. Aim for a homepage a visitor can absorb in one screen.
3. ⬜ **OPEN** — **Typography:** body 16–17px with ~1.6 line-height; consider a system-font stack (free performance win) or an intentional font pairing; establish a real heading scale. *Note:* this is now a change to the shared theme's `mainroad-sans` preset, not to local CSS — see ACTION-PLAN-Aug26 for the ownership question that raises.
4. ⬜ **OPEN** — **Color discipline:** keep UW red (#C5050C) as accent (header, headings, rules); use a quieter link treatment (darker red or underlined default-weight) so links stop shouting on link-dense pages. (Same preset-ownership caveat as item 3.)
5. ⬜ **OPEN** — **Modernize list pages:** replace paginated blog cards with year-grouped single-page archives for talks and videos (62 talks / 70 videos, still at `pagination.pagerSize = 12`); consider a responsive card grid for videos where thumbnails are the point.
6. ⬜ **OPEN** — Small credibility touches: favicon/social meta check, dark mode only if you actually want to maintain it, footer cleanup. (Checked 2026-08-14: a favicon *is* served, but it is the theme's own `themes/559Theme/static/favicon.ico` — i.e. the course-theme default, inherited rather than chosen. There is still no Open Graph / Twitter card metadata.)

## Phase 4 — Optional / later

1. ⬜ **OPEN** — `.git` history slim-down (now **91MB** `.git`). Only worth it if clone size annoys you; a BFG/filter-repo pass rewrites history, so coordinate with any other clones. *Note:* the site now has a real `origin` and CI deploy, so a history rewrite is more disruptive than it was in July.
2. ⬜ **OPEN** — Consider generating the homepage publications list from a data file (`data/publications.yaml`) instead of hand-edited Markdown, making updates one-line edits.
3. ⬜ **OPEN** — Revisit whether talks should get the same `paperpage`-style cross-links videos have.
4. ✅ **RESOLVED — no restart.** Re-evaluate restart (Option C in REVIEW.md)… Consolidation happened and worked; the theme is now shared, documented, and maintained across four sites. Restart is off the table.

## Suggested sequencing — superseded

*The original sequencing advice (below) assumed Phase 2 was still ahead. It isn't.
See [ACTION-PLAN-Aug26.md](ACTION-PLAN-Aug26.md) for current sequencing.*

Phase 0 now; Phase 1 as editorial time permits (it's the most visitor-visible); Phase 2 as one concentrated block (don't interleave with content edits — it's a mechanical refactor best verified by diffing `hugo` output before/after); Phase 3 after 2, iteratively. Phases 0–1 are safe regardless of what you decide about 2–3.
