# QA-158: Case lead prompt says dates without an offset are read as UTC, but gemini 0.6.17 refuses them without a time_zone

| Field | Value |
|---|---|
| Status | fixed |
| Severity | minor |
| Area | geomind |
| Reporter | handbook-case-I |
| Found | 2026-11-05 17:01 UTC |
| Versions | frontend <x.y.z>, backend <x.y.z> (geomind <x.y.z>) |
| Where | <URL>; project <name/id>; chat <id>; run <id>; step <n> |
| Fixer | |

## Steps

1. 
2. 

## Expected

## Actual

## Evidence

- ![screenshot](../evidence/QA-158/1.png)
- Run JSON: `../evidence/QA-158/run-<id>.json`

## Cause

(Facts, or a guess marked as one.)

## Fix

(Hotfix session: cause, commit, version, deployed at.)
- 2026-11-05 17:02 UTC: geomind 0.4.99 (163c82b, tag v0.4.99), pushed 2026-11-05; NOT deployed yet (deploy freeze during the live run): the backend hotfix-mode deploy picks it up. QA-152: design/<project plant name> or design/v<N> in every design tool; QA-158: case lead prompt asks time_zone as an assumption.
- 2026-11-05 17:07 UTC: Deployed: geomind 0.4.100 in backend 1.1.104 hotfix image, 2026-11-05.
## Retest

(Who, when, result.)
