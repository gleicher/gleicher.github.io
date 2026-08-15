# Action Plan — August 2026

*Written 2026-08-14 after re-auditing against the July 2026 [REVIEW.md](REVIEW.md)
and [ACTION-PLAN.md](ACTION-PLAN.md). **Revised 2026-08-15** after Mike landed the
homepage content refresh and a mobile-navigation fix. ACTION-PLAN.md is the
historical record; this is the live plan.*

## Status at 2026-08-15

Three commits landed (`589053f`, `c78aaf5`, `9660096`) and they close most of
what this plan called urgent:

- ✅ **Track A item 1 — mobile navigation. Fixed, and well built.** See below.
- ✅ **Track C item 1 — the "out of date" confession is gone**, replaced by four
  new 2026 research themes; the older themes moved to `/researchtheme/` under an
  honest framing ("Selected Research Themes (current and historic)").
- ✅ **Track C item 4 — publications refreshed** to 2025/2026 (RAL '25, CVPR '25,
  TVCG '26).
- 🟡 **Track C item 2 — teaching partly updated.** CS559 Spring 2026 added; a
  contradiction remains (below).
- ➕ **Bonus:** the homepage got *lighter*, 236 KB → **112 KB** first load, because
  the new theme summaries carry smaller thumbnails than the ones they replaced.

Build is clean (`hugo --baseURL /`, no `WARN`/`ERROR`).

**The site no longer reads as neglected.** That was the dominant defect in both
the July review and this plan, and it's resolved. What follows is smaller.

### The mobile fix, verified

`{{<narrownav>}}` + `.narrownav` rules in `assets/css/home.scss`. I checked it
rather than assuming, and it holds up on every count:

- Emits a real `<nav class="narrownav" aria-label="Site sections">` — so the
  missing landmark is fixed, not just the visual problem.
- Sits at **line 62 of a 320-line page**, above `.sidebar-wrapper` at line 253.
  The July failure was navigation arriving ~440 lines down; that's gone.
- Carries the **full main menu** (Home / Papers / Talks / Videos / Advice), because
  it reads the same headless `content/sectionlinks.md` the sidebar widget uses —
  one source, no duplicated link list to drift.
- CSS compiles correctly into `/css/home.css` (linked from the homepage), with
  `:has(.narrownav)` and the 980px breakpoint intact.
- The DOM matches the selectors: `.sidebar-wrapper` really is a *direct* child of
  `.wrapper`, so the `>` combinator applies.
- The breakpoint reasoning is documented in the SCSS and is sound — 980px sits
  just above the ~953px point where the `leftpic` block's 610px content column
  stops fitting beside a 25% sidebar.

`noheader: true` is still set, so the homepage still has no `<header>`. That is
now a **design choice, not a navigation failure** — the nav problem is solved
independently. Track D can revisit the header on its own merits.

---

## Fix first: one real bug in the new content

**`<!-- more -->` (with spaces) is silently ignored by Hugo.** Only `<!--more-->`
works. I verified this on Hugo 0.164.0 with a throwaway two-page build:

| Divider written | `.Truncated` | `.Summary` |
| --- | --- | --- |
| `<!--more-->` | `true` | first part only ✅ |
| `<!-- more -->` | `false` | **both parts** ❌ |

**Effect:** the intended "lead paragraph, then the rest" split isn't happening.
The homepage falls back to Hugo's automatic ~70-word truncation, so each theme
summary runs on past where it was meant to stop and ends at an arbitrary
sentence — it just *looks* deliberate, which is why it's easy to miss.

Affected — change `<!-- more -->` to `<!--more-->`:

- `content/researchtheme/26vispractice/index.md`
- `content/researchtheme/26educmedia/index.md`
- `content/researchtheme/26robotics/index.md`
- `content/researchtheme/inspection/index.md` *(pre-existing, same mistake)*

And `content/researchtheme/26visfoundations/index.md` has **no divider at all** —
add one so it matches its three siblings.

This is a genuine anomaly, not a house style: 14 other files across the site
already use the correct unspaced form.

## Track A — Homepage polish (what's left)

1. ✅ **DONE** — mobile navigation.
2. ⬜ **Cheap typography/color pass.** Untouched, still one-line changes in
   `hugo.toml`, no theme edit and no blast radius:

   | Want | Lever | Today |
   | --- | --- | --- |
   | Bigger body text | `params.style.vars.bodyFontSize` | `.875rem` (14px) |
   | Different body font | `params.style.vars.fontSans` | Open Sans |
   | Quieter links | `params.linkColor` | `#c5050c` (UW red) |
   | Accent color | `params.style.vars.uwred` | `#c5050c` |

   Line-height is already 1.6, so the "small and tight" complaint is just the
   font size. Try `bodyFontSize = "1rem"` and look.

## Track B — The image bug (unchanged, and the new pages inherit it)

Still the only viewer-weight problem on the site, and the new content added two
more instances of it:

| Page | First load | Cause |
| --- | --- | --- |
| `/researchtheme/26vispractice/` | **641 KB** | 594 KB PNG served at native size |
| `/researchtheme/26robotics/` | 270 KB | 224 KB PNG |
| `/researchtheme/commchar/` | 3,567 KB | 3.4 MB JPG |
| `/researchtheme/usablearvr/` | 1,443 KB | 1.4 MB JPG |

One cause: `layouts/researchtheme/single.html` is a **local** override that emits
`<img src="{{ .RelPermalink }}">` — native size, scaled by CSS. The theme's
`rimage` fix can't reach it. Everything else on the site is fine (homepage
112 KB, list pages 182–242 KB, video/talk pages 45 KB).

1. **Fix `layouts/researchtheme/single.html`** to use `rimage` (downsized copy
   shown, full-size linked — the behavior you asked for). Fixes all six pages at
   once and stops new themes from re-introducing it.
2. **Fix `summary.html` / `summarycontent.html`** in the same directory — they do
   hand-rolled `.Fit` on `videoThumbSize` and predate the theme's image handling.
   Not a weight problem, but three local files drifting from the shared theme.
3. *Optional:* shrink the source originals. With (1) done this buys the viewer
   nothing — repo hygiene only.

## Track C — Content currency (mostly done)

1. ✅ **DONE** — research themes rewritten, four new 2026 entries, old ones
   reframed as historic. Ordering claim in `researchtheme/_index.md` ("roughly
   organized by date") is accurate — verified.
2. 🟡 **Teaching — one contradiction left.** The header line says
   "**Teaching:** Spring 2026: CS765 Data Visualization", but the CS765 bullet's
   most recent entry is Fall 2025 and never mentions a 2026 offering. A `765-26`
   project exists locally, so the bullet is probably just missing it — but as
   written the page contradicts itself. Also `**Office Hour:** Summer 2026` is
   now stale (it's mid-August); and since the header line points backward at a
   finished semester, consider naming what you're teaching *this fall* instead.
3. ⬜ **`gradschoolfaq.md`** — untouched. Still opens by calling itself "almost
   comically out of date" with 2016 and 2010 layers on 2001 text. Per your call:
   an edit that keeps the ageless material, not a retirement. Linked three times
   from the homepage.
4. ✅ **DONE** — publications refreshed.
5. ⬜ **Talks** — unchanged by design; the gap is real and you expect talks this
   year. Noted so it isn't mistaken for an oversight.
6. ⬜ **Drafts — now four, not three.** `content/pages/Advice/new-do-research.md`
   was added (`draft: true`, not linked from anywhere). Joins
   `posts/main-supervised.md`, `pages/webstuff/hugo.md`,
   `pages/Advice/literature.md`. It reads as a genuinely useful piece — the
   "why do you want to do research" framing — so it's a publish candidate, not a
   delete one.

### Copy edits in the new prose

Small, but they're on the most-read pages:

- `_index.md:42` — "I consolidating my research portfolio" → "I am consolidating"
- `26robotics` — "interepret" → "interpret"; "I remain interesting in" → "interested in"
- `26vispractice` — "peoples' hands" → "people's hands"; "Can we standardized" → "standardize"
- `26visfoundations` — "time pressue" → "pressure"; "how to have good process" → "a good process"
- `26educmedia` — "things I've done of the past decades" → "over the past decades"

## Track D — Homepage restructure & redesign

Unchanged and still the one item deserving a dedicated session. Now genuinely
*optional* rather than urgent, since the neglect signals and the mobile problem
are both resolved.

1. **Decide the information architecture** before visual work. The full teaching
   history is still a homepage section and is still the longest thing on the
   page — it's a page, not a section.
2. **Generate design alternatives** against that structure.
3. **Modernize list pages** — year-grouped archives for talks (61) and videos
   (69). Worth noting `/researchtheme/` now paginates too: 17 themes, 12 per
   page, so the homepage's "more complete list" link lands on a partial view
   behind a pager.
4. **Revisit `noheader`** on its own merits, not as a nav fix.

## Track E — Residue and maintenance

- Theme submodule is current (`f4e6896`); `docs/upgrading.md` now distinguishes
  updates from the unification upgrade, with three verification levels.
- Migrate `layouts/shortcodes/` → `layouts/_shortcodes/` (theme moved during
  unification; the site didn't). Silent today.
- No `<meta name="description">`, no Open Graph, no Twitter card. Favicon is the
  theme's default, inherited not chosen.
- `assets/css/home.scss` uses `/** … */` for its doc comments, so they ship in
  `home.css` (~700 bytes). The theme's `main.scss` uses `//` specifically so
  comments are stripped — worth matching.
- `publishResources = false` would cut the build ~42 MB → ~7–10 MB with **zero**
  viewer benefit (see the note below). Hygiene, not performance.
- Run [`.htmltest.yml`](.htmltest.yml); last run 2026-07-04, and a lot of content
  has moved since — including new external links (VisSnacks, several papers).
- Deferred: `.git` slim-down (91 MB); publications-from-data-file;
  `paperpage`-style cross-links for talks.

---

## Suggested sequencing

**The `<!--more-->` fix and copy edits → Track C item 2 → Track B → the rest.**

The divider fix and the typos are minutes of work on the page most people see,
and the divider one is invisible-by-design — it will never announce itself. The
teaching contradiction is the last remaining thing on the homepage that a
careful reader would catch. Track B is a single-file change with a measurable
payoff. Everything after that is discretionary.

## Standing notes

**On `publishResources`.** Setting `_build.publishResources = false` via
`cascade` stops Hugo copying unreferenced page-bundle files into `public/`. It's
safe — resources whose `.RelPermalink` is called still publish, so resizing and
full-size links keep working. It would improve viewer experience by exactly zero
bytes, because those files are already never downloaded. GitHub Pages allows
1 GB; the site is at ~4%. The one non-size consideration: unreferenced files
*are* publicly reachable by URL.

**On theme divergence.** Keep style changes site-local via `params.style.vars`
and `params.linkColor`. `mainroad-sans` is used only by this site among the four
workspace sites, but the theme has consumers outside the workspace, so editing
the preset is the riskier lever with no added benefit. Revisit one-theme-vs-two
only if a redesign wants *structural* divergence, not token divergence.
