# QA-177: Case lead prompt (0.4.100) and handbook-case contradict: set before or after the one question; converted units, ISA pressure and plants_need must be in a question that now comes before any set_case; calculate; tool names; Knowledge source label

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | geomind |
| Reporter | QA-AI-case-I |
| Found | 2026-11-05 17:15 UTC |
| Versions | geomind 0.4.100 (backend 1.1.104); Knowledge handbook-case 77135767 (= `documents/project/quality-assurance/inputs/handbook-case.md`, b83e54e), hackathon-2026-assumptions 9f98c448 |
| Where | `geomind/geomind/prompts/case/lead.md`, `geomind/geomind/prompts/case/geoscientist.md`, `knowledge/handbook-case.md` |
| Fixer | |

Review asked by Coordinator-V (round 2): the case prompts against the new general handbook-case.
Each line: where the two say different things, and the fix proposed.

## Contradictions

| # | Prompt says | Handbook / other prompt line says | Effect | Proposed fix |
|---|---|---|---|---|
| 1 | `lead.md` steps 3-4 (QA-153 fix): the ONE confirmation question comes first; "Nothing of these is saved before the user approves it"; then ONE `set_case`. "Confirming: Before the first `set_case` ..." | handbook §0.1 steps 4-6: "**Merge and set.** ... write the case once with everything the files and the user state", THEN "Search the gaps", THEN "Ask once". | The lead reads both (handbook via `search_rag`/`read_rag`); either order can win. The handbook order is the old one that broke QA-153. | handbook §0.1: move "Search the gaps" and "Ask once" before "Set once" (or say "set the file values only if no Knowledge value goes with them; Knowledge values only after approve all"). |
| 2 | `lead.md` "Copy every number ...": `set_case` lists a mapped unit in `converted`; "put each of those in the ONE confirmation question". Air pressure: `set_case` sets the ISA pressure from an elevation, "Show that value ... in the ONE question". Checklist: "`plants_need` ... each of its paths was asked for in the one confirmation question". handbook §8.4: the one question holds "every unit `set_case` listed in `converted`, every path in `plants_need`". | `lead.md` step 3/4 and "Setting the case": the question now comes BEFORE the first `set_case`. | `converted`, the ISA pressure and `plants_need` only exist after a `set_case`, so the rules cannot be followed; either the lead calls `set_case` first (breaks QA-153) or skips them, or asks a second question (breaks "ONE question"). | Use `validate`-only: let the lead call `set_case(..., dry_run=true)` (or `/design/case/validate`) with file + proposed values to get `converted`, `plants_need` and the ISA pressure without saving, then ask; or allow a second `ask_user` only for what the first `set_case` returns (`converted`, `plants_need`) and say so in both the prompt and §8.4. |
| 3 | `lead.md` "Compute nothing: ... never a value you work out from others"; "Never a sum, a product, a unit conversion, ... or any value from a formula". | handbook §8.5: "A derived number that matters is ... left to gemini, **or computed with `calculate` (skill `calculator`) and cited by its id**". The lead has `calculate`. | The model may compute a value with `calculate` and put it in the case (allowed by the handbook, forbidden by the prompt). | Pick one: for the case, never (`lead.md`), and drop "or computed with `calculate`" from §8.5, or allow it only in a question's note, never as a case value. |
| 4 | `lead.md` tools: `search_rag`, `read_rag("knowledge/<name>")`. | handbook §8.1: "search Knowledge ... (`search_knowledge`, then `read_knowledge` ...)"; those tools are the geoscientist's, the lead has none of them. | The lead may call a tool it lacks (a refused call) or think the step is not for it. | handbook §8.1: name both ("`search_rag` / `read_rag` for the lead; `search_knowledge` / `read_knowledge` for a geoscientist"). |
| 5 | `lead.md`: a time zone, a design choice and a delegated assumption are recorded `source: "agent"`; a Knowledge value has no rule (runs 1-2 recorded them as `source: "agent"`, `origin: "Team (design choice)"`). | handbook §8.3: Knowledge `source: knowledge`, connector `source: connector`. | The explainer and the report show Knowledge values as the agent's own choices. | `lead.md` "Confirming": "a Knowledge value is recorded with `source: \"knowledge\"`, `citation: {document, section}`; a server value with `source: \"connector\"`". |
| 6 | `geoscientist.md`: no requirement rules at all (no "one range = one requirement", durations, counts, fractions, `when: running`). | handbook §0.4: group IV "Read §6, §7"; §6.7, §6.11 "two requirements for one range" is a common mistake. The geoscientist prompt never tells it to read the handbook. | Geoscientist IV proposed two flow requirements in run 1 (QA-160); the lead copied them. | `geoscientist.md`: "For your group, read the handbook sections the brief names (`read_knowledge('knowledge/handbook-case.md', section=...)`, §0.4 table) before you finish", and copy §6.7 into the prompt. |
| 7 | `lead.md` step 1: "split the case's values into 2 to 4 field groups ... for example: I time and demand; II ground and reservoir; III brine and dissolved gas, utilities; IV requirements". | handbook §0.4: group III is "Brine, gas, **air** and utilities"; group I owns the indoor values. Not a contradiction in meaning but `site.air` has no owner in the prompt's example. | In run 1 the lead gave air to group I or III inconsistently (air values came from the assumptions document via Geoscientists II and III both reading it). | `lead.md` step 1: use the §0.4 groups by name, `site.air` in III. |

## Evidence

- Prompt: `geomind` 592d31a (0.4.100) `geomind/prompts/case/lead.md` lines 49-59 (steps 3-4),
  228-233 (`converted`), 296-306 (ISA pressure), 334 (Confirming), 350-356 (checklist,
  `plants_need`); `geomind/prompts/case/geoscientist.md` (whole).
- Handbook: `documents/project/quality-assurance/inputs/handbook-case.md` §0.1 (lines 45-63),
  §0.4, §6.7, §6.11, §8.1, §8.3, §8.4, §8.5.
- Run 3 (geomind 0.4.100) result: see the Retest of QA-153.

## Cause

The QA-153 fix changed the order in `lead.md` only; the handbook (rewritten the same hour as a
general textbook) and other lines of `lead.md` still follow the old order.

## Proposed fix

See the table: geomind `prompts/case/lead.md`, `prompts/case/geoscientist.md`; Knowledge
`handbook-case.md` (§0.1, §8.1, §8.4, §8.5), then re-upload.

## Decision (handbook-case-I, 2026-11-05 17:45 UTC)

Which rule is right, under the general handbook (documents 2afde46, Knowledge handbook-case 8caaf7c4,
since replaced by later revisions):

| # | Right rule | Change where |
|---|---|---|
| 1 | The prompt's QA-153 order: read, split, merge, search gaps, ONE confirmation question, then ONE `set_case`. Nothing that needs approval is saved before `approve all`. | handbook §0.1 done; `lead.md` step 1 still says "write the case ONCE with set_case" after merging: change to "merge; save nothing yet". |
| 2 | `converted`, the ISA pressure and `plants_need` are not in the one question. After the one `set_case`, ONE follow-up `ask_user` only for `plants_need` paths (by path and unit, no number) or a unit NAME `set_case` mapped. Conversions between units a key accepts are gemini's; the ISA pressure is derived, the elevation is what is confirmed. | handbook §0.1, §2.4, §8.4, §10.3, §10.4 done; `lead.md`: drop "put each converted in the ONE question" and "show the ISA value in the ONE question", checklist `plants_need` line to "asked in the follow-up". |
| 3 | The prompt: never compute a case value; `calculate` is not for the case. | handbook §8.5 done. |
| 4 | Both: `search_rag`/`read_rag` for the lead, `search_knowledge`/`read_knowledge` for a geoscientist. | handbook §8.1 done. |
| 5 | The handbook §8.3: Knowledge value `source: "knowledge"`, server value `source: "connector"`; `agent` only for design choices, the time zone and delegated assumptions. | `lead.md` "Confirming". |
| 6 | Geoscientists read the handbook sections their brief names (§0.4) and keep the requirement rules (§6.7, §6.11, §6.12). | `geoscientist.md`. |
| 7 | The handbook §0.4 groups, `site.air` in group III. | `lead.md` step 1. |

## Fix

(Hotfix session: cause, commit, version, deployed at.)

## Retest

(Who, when, result.)
