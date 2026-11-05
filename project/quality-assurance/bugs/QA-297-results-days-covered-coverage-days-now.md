# QA-297: Results Days covered: coverage days now carry 'electricity' (heat-pump electricity, gemini >= 0.6.22, back-m1 QA-270); the card reads only 'geothermal', so heat-pump days look short of geothermal

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | frontend |
| Reporter | hotfix-front-lead (from back-m1) |
| Found | 2026-11-05 18:47 UTC |
| Versions | frontend <x.y.z>, backend <x.y.z> (geomind <x.y.z>) |
| Where | <URL>; project <name/id>; chat <id>; run <id>; step <n> |
| Fixer | hotfix-front-lead |

## Steps

1. 
2. 

## Expected

## Actual

## Evidence

- ![screenshot](../evidence/QA-297/1.png)
- Run JSON: `../evidence/QA-297/run-<id>.json`

## Cause

(Facts, or a guess marked as one.)

## Fix

(Hotfix session: cause, commit, version, deployed at.)

Fix: frontend 1.1.129 (commit afa855a, bundle index-DjK0zKa6.js), by front-m2: heat-pump electricity band and share in Days covered; geothermal + electricity without backup counts as geothermal-served.
- 2026-11-05 18:54 UTC: frontend 1.1.129
## Retest

(Who, when, result.)
