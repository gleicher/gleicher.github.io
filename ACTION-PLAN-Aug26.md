# Action Plan — August 2026

*Written 2026-08-14, after re-auditing the repo against the July 2026
[REVIEW.md](REVIEW.md) and [ACTION-PLAN.md](ACTION-PLAN.md). ACTION-PLAN.md has
been marked up with per-item ✅/⬜ status and is now a historical record; this
document is the live plan. Revised the same day with Mike's decisions and with
measured page-weight data that corrected an early wrong assumption.*

## Where things actually stand

The **infrastructure problem the July review was mostly about is solved.** Work
ran 2026-07-12 → 2026-07-18 and delivered more than the plan asked for:

- Phase 0 (bug fixes, scaffolding pruning) — done, except the `draft: true` triage.
- Phase 2 (structural consolidation) — done, via the cross-repo **theme
  unification** project rather than by forking the theme here. `roadster` is
  gone; one theme, one CSS bundle, modern layout conventions, `hugo.toml`,
  `params.style.preset = "mainroad-sans"`, MiniSearch instead of a CDN Lunr.
- The theme is pushed and public (`github.com/CS559/559Theme`), documented, and
  has a deprecation checker.
- This site is pushed to `gleicher/gleicher.github.io` and deploys via GitHub
  Actions on push to `main`.

Verified fresh today: `hugo --gc` builds clean (199 pages, no warnings); the
theme's `tools/check-deprecated.py` reports **zero** deprecated shortcode uses in
this site's content; the submodule is 3 commits behind `origin/master`.

**Never started: Phase 1 (editorial), Phase 3 (visual), Phase 4 (optional).**
What remains is almost entirely content and design work.

---

## Measured facts that shape this plan

I measured actual first-load transfer per page (HTML + `<img>` + stylesheets +
scripts; `<a href>` links excluded, since nobody downloads those unless they
click). This **corrected my initial assumption** that site weight was a broad
problem:

| Page | First load | Verdict |
| --- | --- | --- |
| Homepage | 236 KB | fine |
| `/video/` list | 242 KB | fine |
| `/talks/` list | 182 KB | fine |
| A video single page | 45 KB | fine |
| **`/researchtheme/commchar/`** | **3,567 KB** | **bug** |
| **`/researchtheme/usablearvr/`** | **1,443 KB** | **bug** |

So: the theme's resizing works everywhere it's used. The 594 KB headshot on the
homepage is *not* first-load — `leftpic` correctly serves a resized copy and
links the original, exactly the pattern you asked for. List thumbnails are
resized. **The only viewer-weight bug on the site is the research-theme pages**,
and it has a single cause: `layouts/researchtheme/single.html` is a *local*
override (not the theme) that emits `<img src="{{ .RelPermalink }}">` — native
size, scaled down by CSS. Five pages are affected, ~6.4 MB total.

The other ~35 MB of large files in the 42 MB build are page-bundle resources in
`content/talks/*/` and `content/video/*/` that **no page references at all** —
Hugo publishes them verbatim. They cost deploy size and zero viewer bytes.

### Mobile navigation, verified

The July review's finding holds, and I confirmed the mechanism in the built HTML:

- Homepage: **no `<header>` and no `<nav>` element exists at all.** Main content
  begins at line 36; the sidebar — which holds the *only* navigation — begins at
  line 474, i.e. below ~11,000 characters of text.
- Every interior page: `<header>` at line 33, `<nav class="menu">` at line 45,
  both *before* main content, with a working MENU toggle.

On a phone the homepage therefore has no navigation until you scroll past the
entire page. It is also missing a `<nav>` landmark for screen readers. This is
caused by one line: `noheader: true` at `content/_index.md:4`.

---

## Track A — Mobile & homepage navigation (do first)

You called the mobile experience a big deal, and it's also the cheapest serious
fix on the list.

1. **Remove the homepage navigation gap.** Either drop `noheader: true`, or add a
   slim homepage header variant to the theme that keeps the banner minimal but
   restores the menu. I'd try dropping it first and just looking at it — it may
   be entirely acceptable, in which case this is a one-line fix to the worst
   accessibility and mobile problem on the site.
2. **Cheap typography/color pass while you're looking.** These are site-local
   one-liners in `hugo.toml`, no theme edit and no blast radius:

   | Want | Lever | Today |
   | --- | --- | --- |
   | Bigger body text | `params.style.vars.bodyFontSize` | `.875rem` (14px) |
   | Different body font | `params.style.vars.fontSans` | Open Sans |
   | Quieter links | `params.linkColor` | `#c5050c` (UW red) |
   | Accent color | `params.style.vars.uwred` | `#c5050c` |

   Line-height is already 1.6, so the review's "small and tight" complaint is
   really just the font size. Try `bodyFontSize = "1rem"` and look.

## Track B — The image bug (small, precise, now well-understood)

Per your call: correct `rimage` behavior — downsized copy on the page, link to
the full-size original — is the target, and it's *exactly* what's missing.

1. **Fix `layouts/researchtheme/single.html`** to use the theme's `rimage` idiom
   instead of raw `.RelPermalink`. This alone takes the worst page from 3.6 MB to
   a few tens of KB and fixes all five research-theme pages. **This is the whole
   viewer-weight bug.**
2. **Fix `layouts/researchtheme/summary.html` and `summarycontent.html`** while
   you're there — they do hand-rolled `.Fit` on `videoThumbSize` and predate the
   theme's current image handling. Not a weight problem (they already resize),
   but they're three local files drifting from the shared theme.
3. **Optional, separate:** shrink the source originals in `content/`. With (1)
   done this buys the *viewer* nothing — it's repo/deploy hygiene only. Worth
   doing opportunistically, not worth a project.

## Track C — Content currency (no code)

**The site reads as abandoned, and says so out loud.** This remains the largest
visitor-visible defect.

1. **Rewrite the "Current Research Themes" intro.** `content/_index.md:47` still
   ships "The projects list was more than slightly out of date. I need to
   revitalize it." Re-sort current vs. past themes while you're in there.
2. **Fix the teaching self-contradiction.** The top of the homepage says "CS559
   Spring 2026"; the Teaching section below says "In Spring of 2025 I taught an
   Accelerated Honors Section." Also refresh the "Office Hour: Summer 2026" line.
3. **Talks — leave the gap, remove the *implication*.** Per your answer: the gap
   is real, it isn't the end of the road, and you expect talks this year. So no
   backfill and no "archive" reframing. The only thing worth doing is making the
   section not *read* as dormant to someone who arrives cold — and honestly, the
   simplest version of that is adding this year's talks when they happen. Low
   priority; noted so it isn't mistaken for an oversight later.
4. **Refresh "Selected Recent Publications"** (newest entry is a 2025 arXiv item).
5. **Overhaul `gradschoolfaq.md`, preserving the timeless parts.** Per your
   answer: it's popular *because* much of its wisdom is ageless, so this is an
   edit, not a retirement. The work is stripping the 2016 and 2010 update layers
   and the self-deprecating "comically out of date" opener, keeping the durable
   advice, and refreshing only the genuinely time-bound bits (admissions process,
   who's hiring, "am I taking students"). It's linked three times from the
   homepage, so it earns the effort.
6. **Triage the three drafts** — `content/posts/main-supervised.md` (36 lines,
   also in [TO-DO.md](TO-DO.md)), `content/pages/webstuff/hugo.md` (11 lines),
   `content/pages/Advice/literature.md` (41 lines).

## Track D — Homepage restructure & redesign (the design project)

In scope, and the plan is: **settle structure first, then generate alternatives
with Claude Design.** Sequencing matters here — do this *after* Track C, so
you're restructuring content you've just rewritten rather than content you're
about to rewrite.

1. **Decide the information architecture** before any visual work. Working
   proposal: landing section (photo, one-paragraph bio, prominent links to
   Papers / Talks / Videos / Advice) → compact research-theme cards → everything
   else moved off. The full teaching history in particular is a page, not a
   homepage section.
2. **Generate design alternatives** against that structure.
3. **Modernize the list pages** — year-grouped archives for talks (61) and videos
   (69) instead of 12-per-page pagination; a card grid for videos, where the
   thumbnail is the point.

## Track E — Residue and maintenance

- Bump the theme submodule (3 commits: docs + a link fix). Use `/upgrade-theme`.
- Migrate `layouts/shortcodes/` → `layouts/_shortcodes/`. The theme moved during
  unification; the site didn't. Currently silent, but it's the last piece of the
  modern-layout migration on this side.
- No `<meta name="description">`, no Open Graph, no Twitter card on any page
  (verified). The favicon served is the theme's default, inherited not chosen.
- `publishResources` — see the note below.
- Run [`.htmltest.yml`](.htmltest.yml) again; last run 2026-07-04.
- Deferred, unchanged: `.git` slim-down (91 MB, and *more* disruptive than in
  July now that the repo has a real origin and CI); publications-from-data-file;
  `paperpage`-style cross-links for talks.

---

## On `publishResources` — you're not missing anything

You asked me to push back if you were. You aren't; your instinct is right.

Setting `_build.publishResources = false` (via `cascade` in `hugo.toml`) stops
Hugo copying unreferenced page-bundle files into `public/`. It is **safe** —
Hugo still publishes any resource whose `.RelPermalink` is called, so resized
copies and `leftpic`'s link-to-original keep working. It would cut the build from
~42 MB to roughly 7–10 MB.

**And it would improve viewer experience by exactly zero bytes**, because those
files are already never downloaded — no page links to them. It's deploy-artifact
and clone-size hygiene, not performance.

Is there a hidden reason to care? Not really. GitHub Pages' limits are a 1 GB
site and a 100 GB/month soft bandwidth budget; 42 MB is about 4% of the size
limit and the bandwidth is driven by what visitors actually fetch, not by what
sits in the artifact. The only real costs are marginally slower CI
upload/deploy and a bigger clone. The one non-size consideration worth a thought:
those unreferenced files *are* publicly reachable by URL, so if any bundle
contains a figure you'd rather not have served, that's a reason to enable it
that has nothing to do with weight.

**Recommendation:** turn it on as cheap hygiene whenever convenient, but don't
count it toward the problem you actually care about. Track B item 1 is the fix
for that.

---

## On the theme-divergence question

You raised the real tradeoff: this site is a genuinely different *kind* of page
from the course sites, so style divergence is appropriate — but that has to be
weighed against maintaining two themes instead of one.

For now the answer is easy, and it's the one you'd want either way: keep changes
**site-local** via `params.style.vars` and `params.linkColor` in `hugo.toml`.
That gets the sans-serif look you like with zero risk to the other consumers, and
it requires no decision about theme architecture. `mainroad-sans` is used only by
this site among the four workspace sites, but the theme has consumers outside the
workspace, so editing the preset itself is the riskier lever with no added
benefit right now.

The larger question — one shared theme with divergent presets vs. two themes —
should be **re-examined if and only if** Track D's redesign ends up wanting
structural changes (different layouts, different page types), not just token
changes. Token divergence is already well-served by the preset mechanism.
Recording it here so it's a deliberate future decision rather than a drift.

---

## Suggested sequencing

**A → B → C → D**, with E picked up whenever.

Track A is the worst defect and the cheapest fix. Track B is small, precisely
scoped, and now fully understood. Track C is where the visitor-visible damage is
and needs no code — it's also the track that doesn't need me. Track D is the only
item deserving a dedicated design session, and it should follow C.

## Correction to the previous draft of this plan

The first version of this document treated site weight as a broad problem
("42 MB build, ~25 files over 500 KB") and made it Track B with a batch
image-compression job as the primary fix. Measurement showed that was wrong: the
homepage and list pages are already light, the theme's resizing works, and the
entire viewer-facing problem is five research-theme pages caused by one local
layout override. The compression job has been demoted to optional hygiene.
