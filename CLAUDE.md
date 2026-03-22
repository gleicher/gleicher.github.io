# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Site Overview

Academic personal website for Professor Michael Gleicher (UW-Madison CS). Built with Hugo (extended, v0.153.2 required).

## Build & Deploy Commands

```bash
# Local development
hugo server

# Build for deployment (Linux/macOS)
./deploy
# which runs: hugo -d ~/public/html-s --baseURL https://pages.cs.wisc.edu/~gleicher/

# Update theme submodules
./pullall.bat  # or manually: git submodule foreach --recursive git pull
```

CI (GitHub Actions) builds on master push and deploys to `gleicher/gleicher.github.io`.

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
