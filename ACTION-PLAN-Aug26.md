# Action Plan — August 2026

*Live plan. [ACTION-PLAN.md](ACTION-PLAN.md) (July) and [REVIEW.md](REVIEW.md) are
historical. Rewritten 2026-08-15 — the previous version had gone stale within a day.*

## Done

Everything the July review and the first version of this plan called urgent:

- **Mobile navigation** — `{{<narrownav>}}` puts a real `<nav aria-label>` with the
  full menu near the top of the homepage. Verified in the built HTML: line 62 of
  320, where navigation used to arrive around line 440.
- **The "neglected site" signals** — the "out of date" confession is gone, four
  2026 research themes replace the old list, publications run to TVCG '26,
  teaching says Fall 2026.
- **The silent summary-divider bug** — `<!-- more -->` with spaces is ignored by
  Hugo; only `<!--more-->` works. Fixed in five files, and 559Theme now ships
  `_partials/content-lint.html` so it can never fail silently again on any
  consumer site.
- **The image bug** — `layouts/researchtheme/single.html` was emitting
  full-resolution originals scaled by CSS. Homepage + all theme pages went
  **9,078 KB → 2,715 KB (70% lighter)**; commchar alone 3,566 → 85 KB. Heaviest
  page on the site is now 438 KB, down from 3.5 MB.
- **Dead code and alt text** — `summarycontent` (both files) deleted;
  research-theme images have correct alt semantics.
- **Copy edits** — the six typos, plus the Morgridge and Fall 2026 fixes.
- **Link check** — `htmltest` passes clean: 217 documents, zero failures.

Build is clean: `hugo --baseURL /`, no `WARN`, no `ERROR`.

---

## What's left

Short answer to "is there anything besides the redesign and the talks/videos alt
tags?" — **yes, but only one item involves real writing.**

### 1. `gradschoolfaq.md` — the only substantial work left

Untouched since 2023-09-10. Opens by calling itself "almost comically out of
date," then layers a 2016 update and a 2010 update over 2001 text. Linked
**three times** from the homepage, so it gets traffic.

Per your call: an edit that keeps the ageless material and refreshes only the
genuinely time-bound parts (admissions process, whether you're taking students),
not a retirement. This is writing time, not code.

### 2. Alt text in the theme's video/talks layouts

Same defect just fixed in `researchtheme/`, but in the theme: list thumbnails use
the resource filename as alt (`alt="1991_briar.jpg"`, `alt="12e.png"`) across 12
list pages. Theme-level, so it affects every consumer site — wants its own branch
and golden-diff, like the content-lint change.

### 3. Homepage restructure & redesign

The one item deserving a dedicated session, and now genuinely optional rather
than urgent.

- Decide the information architecture first. The full teaching history is still
  a homepage section and still the longest thing on the page — it's a page.
- Then generate design alternatives.
- Year-grouped archives for talks (61) and videos (69) instead of 12-per-page
  pagination. `/researchtheme/` paginates too — 17 themes, 12 per page — so the
  homepage's "more complete list" link lands on a partial view behind a pager.
- Revisit `noheader: true` on its own merits. It's now a design choice, not a
  navigation failure.

### 4. Small, mechanical, each independent

- **Teaching bullet.** The header advertises "Fall 2026: CS765", but the CS765
  bullet's most recent entry is still Fall 2025 and never mentions a 2026
  offering. A `765-26` project exists locally, so the bullet is just missing it.
- **`Office Hour: Summer 2026`** is stale in mid-August.
- **Four drafts** to publish or delete: `pages/Advice/new-do-research.md` (reads
  like a publish candidate), `pages/Advice/literature.md`, `pages/webstuff/hugo.md`,
  `posts/main-supervised.md` (also in [TO-DO.md](TO-DO.md)).
- **Empty meta description.** The homepage ships
  `<meta name="description" content="">` — a present-but-empty tag, arguably
  worse than none. No Open Graph or Twitter card either, so links shared to
  Slack/Mastodon/etc. render bare. The favicon is still the theme's course
  default, inherited rather than chosen.
- **Typography one-liners.** Still untouched, still no blast radius:

  | Want | Lever | Today |
  | --- | --- | --- |
  | Bigger body text | `params.style.vars.bodyFontSize` | `.875rem` (14px) |
  | Different body font | `params.style.vars.fontSans` | Open Sans |
  | Quieter links | `params.linkColor` | `#c5050c` (UW red) |

  Line-height is already 1.6, so the review's "small and tight" complaint is just
  the font size. Try `bodyFontSize = "1rem"` and look.
- **`layouts/shortcodes/` → `layouts/_shortcodes/`.** The theme moved during
  unification; the site didn't. Silent today, and the last piece of that
  migration on this side.
- **`assets/css/home.scss` uses `/** … */`** for its doc comments, so they ship
  in `home.css`. The theme's `main.scss` uses `//` precisely so comments are
  stripped.

### 5. Deferred by choice

- **`publishResources = false`** would cut the build from 45 MB to roughly
  7–10 MB with **zero** viewer benefit — those files are never downloaded. Safe
  (resources whose `.RelPermalink` is called still publish). Hygiene, not
  performance. The one non-size angle: unreferenced files are publicly reachable
  by URL.
- **Shrinking source originals** — buys the viewer nothing now that the layout
  serves resized copies. Repo hygiene only.
- **`.git` slim-down** (91 MB), publications from a data file, `paperpage`-style
  cross-links for talks.

---

## Suggested order

**4 → 1 → 2 → 3.** The small items are minutes each and several are one-liners.
`gradschoolfaq` is the real remaining work and needs your writing. The theme alt
fix is mine to do whenever. The redesign is a session you schedule deliberately.

## Standing notes

**Theme divergence.** Keep style changes site-local via `params.style.vars` and
`params.linkColor`. `mainroad-sans` is used only by this site among the four
workspace sites, but the theme has consumers outside the workspace, so editing
the preset is the riskier lever with no added benefit. Revisit one-theme-vs-two
only if a redesign wants *structural* divergence, not token divergence.

**Two lessons worth not relearning.** Both came from measuring rather than
reasoning, and both were invisible in a passing build:

- A silent failure needs a loud guard, not a fix. `<!-- more -->` produced
  plausible-looking output for months. The fix was the build warning; correcting
  the files was the easy half.
- Fewer pixels is not fewer bytes. Hugo re-encodes, and a 969px PNG at 68,378
  bytes came back *larger* at 800px. Any resize should be adopted only when it
  actually wins.
