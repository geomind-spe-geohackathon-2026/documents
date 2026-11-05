# QA-359: Every agent-sized design fails all steps: 'd0.esp: flow = 8808335 m3/s gives head = 3824522' on 2027-01-01 (runs edb42b40 and b3a69d7c, 6 of 6 sized plants, 3 doublets at 2,500 m); the minimize studies then end 'done' with no result

| Field | Value |
|---|---|
| Status | fixed |
| Severity | blocker |
| Area | gemini |
| Reporter | Manual QA-IV |
| Found | 2026-11-05 21:21 UTC |
| Versions | backend 1.1.133 (geomind 0.4.137, gemini 0.6.34) |
| Where | projects 4138a399-c1c2-4c2f-a1ee-2f7e6f70c568 (run edb42b40) and bf1bccef-f12e-43e5-b273-9040337062cc (run b3a69d7c): studies hp_comp_sized, abs_direct_sized, full_direct_sized, hp_comp_sized, abs_chill_sized, deep_full_sized |
| Fixer | hotfix-python-lead-II |

## Steps

Clean agent runs (no brief): the design lead builds 3 classes, patches 100+ values, sizes them (run study with prepare size): each sized plant has 3 doublets at 2,500 m.

## Expected

The sized plants run the year (Sahand's run d935c2b1 on the same day: sized 34.61 EUR/MWh, 12/12).

## Actual

All 6 sized plants: 4 checks pass, 18 'not assessed'; first failure on 2027-01-01: `d0.esp: flow = 8808335.19531637 m3/s gives head = 3824522.2748500933`, an impossible ESP flow (8.8e6 m3/s). The minimize studies on these designs end 'done' with result null and no error (only hp_comp_opt in bf1bccef gave a result: LCTS 340.6, 7 pass, 5 not assessed).

## Cause

Guess: the ESP solve diverges after sizing (unset ESP curves derived from the design flow; 3 doublets; gemini 0.6.34 'ESP: unset curves give no out_of_range text instead of TypeError' changed this path), and the minimize study hides that no trial was feasible. Both clean report runs are blocked by it.

## Fix

- 2026-11-05 21:35 UTC: gemini 0.6.35 (55f2ddff) + geomind 0.4.138; pending deploy
## Retest
