# QA-098: Browser tab shows a generic globe instead of the GeoMind icon (no favicon)

| Field | Value |
|---|---|
| Status | verified |
| Severity | minor |
| Area | frontend |
| Reporter | user via coordinator |
| Found | 2026-11-05 10:18 UTC |
| Versions | frontend 1.1.84 |
| Where | https://geomind.team, any page, the browser tab |
| Fixer | hotfix-front-II |

## Steps

1. Open https://geomind.team in a browser.
2. Look at the tab icon.

## Expected

The GeoMind logo (the sidebar mark) as the tab icon: favicon.ico plus SVG/PNG sizes (16, 32, 180 apple-touch), linked in index.html, each URL returning the image.

## Actual

A generic globe. /favicon.svg, /favicon-32.png and /favicon.ico all returned index.html (text/html, 3225 bytes).

## Evidence

- ![tab](../evidence/QA-098/1.png)

## Cause

`vite.config.ts` sets `publicDir` off for the build (so the MSW worker in `public/` never ships); the favicons were in `public/` too, so they were never in `dist/` and nginx fell back to index.html.

## Fix

frontend 1.1.86 (hotfix-front-II): icons moved to `static/`, the build's publicDir; added favicon.ico (16/32/48), favicon-16.png, apple-touch-icon.png (180, white ground) rendered from the logo SVG; all linked in index.html; nginx serves them as files (=404 otherwise, 1-day cache). Local build: each URL 200 with image/svg+xml, image/png or image/x-icon; mockServiceWorker.js still not shipped. Deploy: 10:30 UTC window.
- 2026-11-05 10:33 UTC: frontend 1.1.86, commit 2738c1c, deployed 10:31 UTC (bundle index-C9q6wEoE.js)
## Retest

(Who, when, result.)
- 2026-11-05 10:33 UTC: hotfix-front-II 10:33 UTC: index.html links favicon.ico, favicon.svg, favicon-16/32.png, apple-touch-icon.png; curl on geomind.team: each 200 with image/x-icon, image/svg+xml or image/png (not index.html). Tab icon itself not seen (headless browser fetches no favicon); a browser may need a hard reload for its icon cache
