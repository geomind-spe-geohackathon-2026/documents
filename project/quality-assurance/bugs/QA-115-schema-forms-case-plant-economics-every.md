# QA-115: Schema forms (Case, Plant, Economics ...): every collapsible group opens by default

| Field | Value |
|---|---|
| Status | verified |
| Severity | minor |
| Area | frontend |
| Reporter | user via coordinator |
| Found | 2026-11-05 11:00 UTC |
| Versions | frontend 1.1.86 |
| Where | Design > Case form (and Plant, Economics: every schema form, `src/shared/forms`) |
| Fixer | hotfix-front-III |

## Steps

1. Open Design > Case.
2. Look at the groups (Air, Fluid, Ground, Reservoir ...).

## Expected

Every group collapsed by default; the user opens what they want. A group holding a validation error or a missing required value opens (or shows a marker) so problems are not hidden. The open/closed state stays while the user stays on the page.

## Actual

The groups open by default.

## Evidence

- ![case form](../evidence/QA-115/1.png)

## Cause

Fact: `GroupFields` in `frontend/src/shared/forms/schema-fields.tsx` opened every optional group that had a value or was top level (`open={hasContent(value) || needsAttention || !path.includes(".")}`) and drew required groups as an always-open fieldset.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

hotfix-front-III, frontend 1.1.93 (564972b): one `CollapsibleGroup` for required and optional groups, closed by default; a group with a form error, a gemini problem or a missing value reported by gemini opens and shows a warning mark; the open/closed state is kept per path while the page stays loaded (also across the form's tabs). Deploy 11:30 UTC.
- 2026-11-05 14:11 UTC: frontend 1.1.99 (e9435c4) deployed 14:10 UTC, bundle index-BlepNtQt.js
## Retest

(Who, when, result.)
- 2026-11-05 14:12 UTC: live 1.1.99: Case Demand/Site/Economics groups closed by default; Air stays open across tab switches
