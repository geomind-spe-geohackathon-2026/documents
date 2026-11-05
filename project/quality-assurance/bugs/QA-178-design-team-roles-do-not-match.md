# QA-178: Design team roles do not match handbook-design 0.3 groups: lead briefs 'Reservoir engineer II: treatment and gas' and 'Energy systems engineer II: cooling'; well_engineer is never used

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind,data |
| Reporter | QA-AI-design-I |
| Found | 2026-11-05 17:15 UTC |
| Versions | backend 1.1.102 at run start, 1.1.103 and 1.1.104 deployed during the run (geomind 0.4.98, gemini 0.6.16 then 0.6.17) |
| Where | api.geomind.team; project QA-TEST QA-AI-design-I 1 (b9ef5c9a-e030-4357-91ee-b17dabfdeaa6); chat efb95fd0-f997-4530-a314-f93baf64ef5f; run 0df89b7e-69e0-46b3-abe1-231e51d9570a; design_lead step #10 fill_parts briefs |
| Fixer | |

## Steps

1. As QA-174; the lead splits the 111 build issues with `fill_parts`.

## Expected

Each module group of handbook-design 0.3 (I subsurface and wells, II treatment and gas, III heating, IV cooling) goes to the engineer role that knows it, and the ESP and pump depth go to the well engineer, as `prompts/design/lead.md` step 3 says ("The pump depth and the ESP are the well engineer's").

## Actual

Briefs (`../evidence/QA-178/fill-parts-briefs.json`): `reservoir_engineer` "Reservoir engineer I: subsurface and wells" (owns `params.d0.esp.*` and the pump depth: "the ESP is yours"), `reservoir_engineer` "Reservoir engineer II: treatment and gas" (degasser, filters, flare), `energy_systems_engineer` I heating, II cooling. `well_engineer` gets no brief. Reservoir engineer II spends its run reading chapter 5 with a prompt written for the subsurface; Reservoir engineer I sets the ESP (empty coefficient arrays, refused in QA-175) although the well engineer's prompt covers pumps.

The lead copied this split from its own prompt: `prompts/design/lead.md` step 3 gives exactly this example ("Reservoir engineer I: subsurface and wells (`params.d0.*`); Reservoir engineer II: treatment and gas ..."), which contradicts the next sentence (ESP is the well engineer's) and the role list of `fill_parts` (reservoir, well, energy systems). The handbook numbers its groups I-IV too, so "Engineer II" in the handbook and "Reservoir engineer II" (instance name) mean different things. The briefs also name sections that do not exist ("3 Wells"), see QA-169.

## Cause

Fact: prompt example in `geomind/prompts/design/lead.md` lines 68-72; handbook-design.md 0.3 table names groups by Roman numerals with no role.

## Proposed fix

- geomind `prompts/design/lead.md` step 3: one mapping table: subsurface (`params.d0` reservoir, sink, drainage) -> `reservoir_engineer`; wells and pumps (`d0.well/riser/injector/esp`, injection pump) -> `well_engineer`; treatment and gas -> `well_engineer` or `energy_systems_engineer` (pick one); heating -> `energy_systems_engineer`; cooling -> `energy_systems_engineer`. Example briefs with these role names; section names copied from the outline (number only, e.g. section "4").
- Knowledge `handbook-design.md` 0.3 (data, via the handbook session): add a Role column with the fill_parts role per group; drop "Engineer I..IV" labels or call them "Group A-D" so they do not clash with instance names.

## Fix

- 2026-11-05 18:55 UTC: deploy 36: backend 1.1.118, geomind 0.4.130, gemini 0.6.26 (hotfix-python-lead-II)
## Retest
