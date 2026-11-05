# QA-147: read_stored and calculate cannot read a dotted module key (d0.esp): the path is split at every dot, the error then suggests the same key

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | geomind |
| Reporter | Manual QA-IV |
| Found | 2026-11-05 16:40 UTC |
| Versions | Seen on geomind 0.4.87-0.4.91 (runs of 2026-11-05); the code is unchanged in geomind 0.4.96 / gemini 0.6.16 (live, backend 1.1.99) |
| Where | geomind.team run logs (GET /assistant/runs/{id}/log), 42 runs of 2026-11-05; e.g. design runs ed03d7ea, 37950240, 3bdd7ebb |
| Fixer | |

## Steps

1. Simulate a plant with a doublet; the result's module keys are dotted names: `d0.esp`, `d0.well`, `d0.reservoir`.
2. An agent reads `read_stored(reference=result-..., path="d0.esp.fluid_in.volume_flow")` (or `calculate` / `run_python` with a stored operand on the same path).

## Expected

The value of module `d0.esp`, port `fluid_in`, field `volume_flow`.

## Actual

`read_stored: path = d0; 'd0' is no key or index of the result; expected one of d0.esp`. The agent sends exactly the key it is told
(`d0.esp...`) and gets the same refusal again: the key can never be reached. `calculate`: `result-#: d0 does not exist; expected one of d0.esp`.

Counts over the 42 runs: read_stored 44+ refusals on `d0`/`d1` (`expected one of d#.esp / d#.well / d#.reservoir`), calculate 13+, run_python 4+.
The speed baseline (documents/project/plans/speed-case-plant-baseline.md, cause 1) counts 284 wrong-path refusals in 24 runs; this bug is the part that is the tool's fault, not the agent's.

## Evidence

- Run logs in /tmp/logs on the Dell (fetch again with .claude/notes/sessions/manual-qa-3-tools/api.py); cluster with `tool.py 2026-11-05 read_stored 8 230`.

## Cause

Fact: `geomind/geomind/tools/stored.py:254` walks `path.split(".")`, one dict key per part, so a key that holds a dot (`d0.esp`) is never matched.
`geomind/geomind/tools/calculate.py:170` does the same. The error then lists `d0.esp` as the valid key, which the same split refuses.

Suggested fix: at each level, try the longest run of the remaining parts joined with "." that is a key (`d0.esp`, then `fluid_in`, then `volume_flow`); same in calculate.py. A unit test with a result holding `d0.esp`.

## Fix

## Retest
