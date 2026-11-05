# QA-076: Start-to-end design run ends 'failed' after 66 min, 317 steps and 8.1M tokens with no stored plant: engineers' patch_plant calls refused (not_allowed), plant reads missing values; chat ends on a raw gemini error

| Field | Value |
|---|---|
| Status | fixing |
| Severity | major |
| Area | geomind |
| Reporter | functional-qa-I |
| Found | 2026-11-05 04:14 UTC |
| Versions | backend 1.1.62 at start, 1.1.65-1.1.69 at end (deploys during the run); geomind 0.4.60 to 0.4.64+ |
| Where | project QA2 functional-qa-I full run 61134432; chat 81b51db5-1a6b-402a-9223-66c8af1c6403; run 861ef137-08a2-4252-bf30-437630caf747 (started 00:43, ended 01:49 UTC, status failed) |
| Fixer | hotfix-python |

## Steps

1. New project, PDF + both CSVs, auto-approve on; send the full-challenge request (configurations, GEMINI checks, fix violations, explain, compare two).
2. Answer the case questions; leave it running.

## Expected

A stored, checked plant (at least one configuration, ideally two), or a plain statement of what blocked it.

## Actual

317 steps, 93 'needed another try', 8.09M tokens in, 0.30 USD, 66 min; run status failed; no plant stored (only skeleton designs). Tool errors in the run JSON: read_plant missing_value 35, patch_plant not_allowed 18 (e.g. integration_engineer: 'params.backup is no discipline's (design.owners names none); the integration engineer changes only its own part'; design_lead: 'patch_plant refused my own paths as not_allowed - gemini does not recognise me as well_engineer'), patch_plant missing_value 12, build_plant unconnected_port / missing_value, patch_plant unknown_name (design reference 'design/superstructure' vs stored 'design/hackathon_superstructure'). The plant asks for d0.reservoir.pressure, temperature, permeability, thickness, drainage radius although the case holds pressure, permeability, thickness (QA-049 pattern; temperature is derived). The chat ends on a raw gemini message ('d0.drainage_radius: no value [m]: ... d0.roughness ...'), no summary, no failure reason. Also 2 nested design_lead crashes at the start (QA-070, fixed in 1.1.65 mid-run).
## Evidence

- ![screenshot](../evidence/QA-076/1.png)
- Run JSON: `../evidence/QA-076/run-<id>.json`

## Final chat text (run 861ef137, chat 81b51db5)

After the three 'You answered' lines the chat shows only this, with no heading and no status:

> d0.drainage_radius: no value [m]: Radius of the drainage area around each well; d0.roughness: no value [m]: Absolute roughness of the inner wall of both vertical wells; d0.reservoir.pressure: no value [Pa]: Static reservoir pressure; d0.reservoir.temperature: no value [K]: Undisturbed reservoir temperature; d0.reservoir.permeability: no value [m2]: Permeability of the aquifer rock; d0.reservoir.aq… (d0.drainage_radius)

Screenshot: ../evidence/QA-076/final-chat.png, full chat text: ../evidence/QA-076/final-chat.txt. The run list says 'waiting' (QA-077), the JSON says 'failed'.

## Cause

Facts: ownership checks (design.owners) refuse writes of roles that do not own a path; engineers loop hand-backs. Guess: the ownership design needs a path for plant-level values (backup, esp) or the design lead needs write rights; the run kept re-reading the plant instead of stopping with a question to the user.

## Fix

(Hotfix session: cause, commit, version, deployed at.)

- 2026-11-05 hotfix-back (backend check): no backend part. The run's plants are built and read
  inside geomind (`build_plant`, `read_plant` on `design/hackathon_superstructure_2`); the backend's
  plant template and case code are not on that path. At steps[49] `read_plant` does not return
  issues: it fails with `error.code = missing_value` listing d0.drainage_radius, d0.roughness and
  the d0.reservoir.* values the case would fill (pressure, temperature, permeability, thickness,
  top_depth). So the design is read without the case, or the load raises before `gm.check(plant,
  case)` runs. Per QA-049, gemini fills a doublet's reservoir from the case only once the plant's
  `depth` is set, and gemini's check does not name `depth`. For hotfix-python-II (geomind
  `read_plant` / gemini).

## Retest

(Who, when, result.)
