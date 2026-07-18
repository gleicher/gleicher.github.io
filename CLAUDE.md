# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Site Overview

Academic personal website for Professor Michael Gleicher (UW-Madison CS). Built with Hugo (extended).

Keep the local Hugo version and the CI version in sync. When the local Hugo version changes, update the `HUGO_VERSION` env var in `.github/workflows/hugo.yml` to match (check local with `hugo version`) rather than pinning a specific version here. As of this writing both are on `0.164.0`.

## Build & Deploy Commands

```bash
# Local development
hugo server

# Update theme submodules
./pullall.bat  # or manually: git submodule foreach --recursive git pull
```

Deployment is handled entirely by CI — there is no local deploy step. This repo
(`gleicher/gleicher.github.io`) is both the Hugo source and the published site: on
push to `main`, the `.github/workflows/hugo.yml` GitHub Actions workflow builds the
site and deploys it to GitHub Pages (artifact-based deploy — no `gh-pages` branch).
It is served, via a custom domain, at <https://gleicher.sites.cs.wisc.edu/>.

## Architecture

### Themes

One theme (git submodule): `559Theme` — CS559 course theme, used for
most styling. It absorbed the former `roadster` fallback theme in
2026's theme unification project (canonical record:
`themes/559Theme/THEME-PLAN.md`'s Execution log; the workspace-level
`PLAN.md` is a frozen historical snapshot, not maintained).

Custom overrides live in `layouts/` and `assets/css/`.

**Bumping the theme:** the submodule tracks `origin` (`github.com/CS559/559Theme`)
directly — pushed and public, no local-only remote involved. To pick up a
theme change:

```bash
cd themes/559Theme
git checkout -q -- . && git clean -fdq   # discard any local test edits
git fetch origin && git checkout origin/master
cd ../.. && git add themes/559Theme && git commit -m "bump theme"
```

Always rebuild and diff against a `tools/baseline.sh` snapshot before
committing a bump (see `tools/compare.sh`), and follow
`themes/559Theme/docs/upgrading.md`'s routine-bump procedure — it covers the
pre-flight checks, the golden-master diff loop, and the changelog of
breaking changes to watch for.

### Content Structure

- `content/talks/` — 60+ talk entries dating back to 1997
- `content/video/` — 70+ video entries indexed by year
- `content/researchtheme/` — Research project pages (~17 themes)
- `content/posts/` — Blog posts
- `content/pages/` — Static pages (Advice, Bio, etc.)
- `content/papers/` — Links to external papers database

### External Assets

Large files (PDFs, images) are stored externally at `https://graphics.cs.wisc.edu/GleicherAssets/`. The `fixer.py` script manages moving PDFs from content dirs to this external store with naming convention `year_month_filename`.

### Key Configuration (hugo.toml)

- `params.style.preset = "mainroad-sans"` — the theme's non-course-web style
  preset (Open Sans, black normal-case headings, charcoal menu); the other
  preset (`uw-serif`) is what the course sites use
- `unsafe = true` in Goldmark — allows raw HTML in markdown
- Main sections: `["main"]`
- Sidebar widgets: search, sectionlinks, links, taglist
- Outputs include HTML, RSS, and JSON

### Custom Shortcodes

- `{{< summary "path" >}}` — Embeds research theme summary inline
- `{{< leftpic asset="..." width=... >}}` — Left-aligned image with text wrap
- `{{< coauths >}}` — Co-author display

### Layouts

Custom layout overrides in `layouts/researchtheme/` for research theme pages. Shortcodes in `layouts/shortcodes/`.
