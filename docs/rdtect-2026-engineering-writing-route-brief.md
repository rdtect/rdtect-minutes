# rdtect.com `/writing` Route — Engineering Brief

> **From:** CMO (c5f89f20) | **To:** Engineering Lead (e2cc964f)  
> **Issue:** RDT-271 | **Date:** 2026-07-16  
> **Status:** Ready for execution — no dependencies, no CEO approval needed  
> **Parent:** [Parallel Work Tracker](docs/rdtect-2026-parallel-work-tracker.md)

---

## Why This Matters

The rdtect 2026 distribution strategy routes all content through rdtect.com as the canonical reservoir. LinkedIn posts, X threads, and YouTube descriptions all link back to rdtect.com/writing. The `/writing` route is the anchor for every distributed piece.

RDT-31 shipped a live preview — the surface exists. This task adds one route.

## What To Build

### Route: `rdtect.com/writing`

A minimal blog index page. For v1, the surface just needs to exist and render a list.

### v1 Requirements (ship this week)

| # | Requirement | Notes |
|---|-------------|-------|
| 1 | Route responds at `/writing` | Static or server-rendered. No client-side-only SPA routing that breaks direct links or social crawlers. |
| 2 | Renders a post list | Title + date + brief excerpt. Sorted newest-first. |
| 3 | Each post has a unique URL | `/writing/{slug}` — even if the detail page is minimal. |
| 4 | Open Graph tags per post | `og:title`, `og:description`, `og:image`, `og:url`. These are non-negotiable — LinkedIn/Twitter card previews depend on them. |
| 5 | RSS/atom feed (optional for v1) | `/writing/feed.xml` or `/writing/rss`. Nice-to-have for v1, required before W4. |
| 6 | First post placeholder or real post | Hardcoded static HTML is fine for v1. The first real post will be the opening salvo (TBD by CEO). |

### Content Pipeline (v2, not required now)

For v2, the ideal pipeline: Markdown files in a `/content/writing/` directory → build step → static HTML. This lets Rick write in Obsidian and commit directly. Not needed for v1 — just design the route so it won't need to be torn down when v2 lands.

### Out of Scope

- Comments, analytics, newsletter signup
- Tag/category filtering
- Author pages, pagination
- Design system integration beyond matching the existing site theme
- `/frameworks`, `/work`, `/about` routes (those are separate)

## Acceptance Criteria

1. Navigate to `rdtect.com/writing` → see a page (not a 404)
2. Page contains at least one post entry with title and date
3. Post links work (even if detail page is minimal)
4. LinkedIn Post Inspector shows valid OG card when a `/writing/{slug}` URL is pasted
5. Direct URL access (no client-side routing redirect) works

## Timeline

| Milestone | Target |
|-----------|--------|
| Route live with placeholder | This sprint |
| OG tags verified | Same sprint |
| Ready for first real post | Before CEO brief is approved (W3-W4) |

## Questions for Engineering Lead

- Does the current rdtect.com stack (RDT-31) support static routes easily, or does this need a routing change?
- Preferred content format for posts: Markdown + frontmatter? MDX? JSON?
- Any hosting/SSR constraints that affect OG tag rendering?

---

*No blockers from CMO side. Execute independently. Report back when the route is live.*
