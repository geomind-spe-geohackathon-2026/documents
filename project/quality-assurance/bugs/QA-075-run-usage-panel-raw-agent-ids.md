# QA-075: Run usage panel: raw agent ids, every tool call counted as failed, spinners on finished agents

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | frontend |
| Reporter | Sahand |
| Found | 2026-11-05 04:14 UTC |
| Versions | frontend <x.y.z>, backend <x.y.z> (geomind <x.y.z>) |
| Where | <URL>; project <name/id>; chat <id>; run <id>; step <n> |
| Fixer | |

## Steps
1. Open a chat after a run and its usage panel ("Last run: 0.235 USD · 183 model calls · 307 tool calls").

## Expected
Agents by display name (Project lead, Case lead, ...); "N failed" only for calls that failed; no spinner on agents that are not working.

## Actual
Raw ids (project_lead, case_lead); every agent reads "N tool calls (N failed)" in red with N of N (case_lead 40 of 40, geoscientist 7 of 7, project_lead 6 of 6); what looks like a spinner on every agent.

## Evidence
- Sahand's screenshot (in the chat with the coordinator, 2026-11-05 ~01:45 UTC).
- `GET /assistant/runs/6c5b17e1.../agents`: every tool call has `"error": false`.

## Cause
Fact: `agent-usage.tsx` counted a call as failed when `error !== null`; the API sends `false` for a success. The raw ids came from `toLabel` (the id's last part). The "spinners" are the context rings: a near-empty ring looks like one.

## Fix
frontend 1.1.73: 4bf6ec4 (failed = error true or non-empty text), 2267a4a (shared display-name map `shared/sse/agent-names.ts`, also in the run panel, the chat's busy lines and the run log), af889da (each ring shows its percent with a tooltip), 0269379 (version).

## Retest

(Who, when, result.)
