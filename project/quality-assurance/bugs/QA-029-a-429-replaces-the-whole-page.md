# QA-029: A 429 replaces the whole page with 'Rate limit exceeded'; no wait for Retry-After and no retry

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | frontend |
| Reporter | hotfix-back |
| Found | 2026-11-04 20:25 UTC |
| Versions | frontend 1.1.33+, backend 1.1.24 |
| Where | any page, e.g. the chat or Settings of a project (follow-up of QA-024) |
| Fixer | hotfix-front |

## Steps

1. Make the API answer 429 (before backend 1.1.24: several browsers signed in as the same user).
2. Open or reload any project page.

## Expected

The page keeps what it shows, waits `Retry-After` seconds and tries again; at most a small notice.

## Actual

The whole page is replaced by the red text "Rate limit exceeded" and stays so until a manual reload; a running run's question is not visible meanwhile.

## Evidence

- QA-024 screenshots: `../evidence/QA-024/` (qa-1, qa-5, qa-6, qa-7). The 429 carries `Retry-After` (e.g. 2) and `X-RateLimit-*` headers.

## Cause

Fact: the backend side is fixed in 1.1.24 (per sign-in bucket), so 429s should be rare; the page's handling of a 429 is still a full-page error with no retry.

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-04 20:26 UTC: fixed in frontend 1.1.42 (8f3d186), waiting for deploy: client retries 429 after Retry-After (max 15 s, 5 tries); a 429 that outlasts that still shows the error
## Retest

(Who, when, result.)
