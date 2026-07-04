# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Site Overview

Academic personal website for Professor Michael Gleicher (UW-Madison CS). Built with Hugo (extended).

Keep the local Hugo version and the CI version in sync. When the local Hugo version changes, update the `HUGO_VERSION` env var in `.github/workflows/hugo.yml` to match (check local with `hugo version`) rather than pinning a specific version here. As of this writing both are on `0.163.3`.

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

Two stacked themes (both git submodules):
- `559Theme` (primary) — CS559 course theme, used for most styling
- `roadster` (fallback)

Custom overrides live in `layouts/` and `assets/css/`.

### Content Structure

- `content/talks/` — 60+ talk entries dating back to 1997
- `content/video/` — 70+ video entries indexed by year
- `content/researchtheme/` — Research project pages (~17 themes)
- `content/posts/` — Blog posts
- `content/pages/` — Static pages (Advice, Bio, etc.)
- `content/papers/` — Links to external papers database

### External Assets

Large files (PDFs, images) are stored externally at `https://graphics.cs.wisc.edu/GleicherAssets/`. The `fixer.py` script manages moving PDFs from content dirs to this external store with naming convention `year_month_filename`.

### Key Configuration (config.toml)

- `themestyle = "old"` — Legacy theme styling variant
- `unsafe = true` in Goldmark — allows raw HTML in markdown
- Main sections: `["main"]`
- Sidebar widgets: lunr search, sectionlinks, links, taglist
- Outputs include HTML, RSS, and JSON

### Custom Shortcodes

- `{{< summary "path" >}}` — Embeds research theme summary inline
- `{{< leftpic asset="..." width=... >}}` — Left-aligned image with text wrap
- `{{< coauths >}}` — Co-author display

### Layouts

Custom layout overrides in `layouts/researchtheme/` for research theme pages. Shortcodes in `layouts/shortcodes/`.
