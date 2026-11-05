# QA-268: User denies a set_case card ('do not change the case, just tell me the NPV at 30 years'): the case lead's finish guard forces ask_economics, which proposes replacing the whole reference economics with other catalogue values (discount 0.051, electricity 115, HX 0.109 EUR/W); the user's question is never answered

| Field | Value |
|---|---|
| Status | fixed |
| Severity | major |
| Area | geomind |
| Reporter | QA-AI-analysis-I |
| Found | 2026-11-05 18:17 UTC |
| Versions | backend 1.1.112 (geomind 0.4.118/0.4.119), API only |
| Where | https://api.geomind.team; project `QA-TEST QA-AI-analysis-I 6` (d168c5d1-acd4-4795-9442-f2dbe56d0b2d); chat 2fd795ec-8012-40cc-8666-6eca57ecd2a3; run ca876a33-96a1-45b7-a428-70bccdb15152 |
| Fixer | |

## Steps

1. Project with the reference case + economics (analysis_period 25 yr), HackathonPlant costed (NPV 28.453 MEUR).
2. Chat: "Set the analysis period in the case to 30 years and give me the new NPV."
3. The case lead's `set_case` card (request-66, analysis_period 30 yr): Deny, reason "Do not change the case; just
   tell me what the NPV would be at 30 years."
4. Answer "stop" on the question that follows.

## Expected

After the denial: nothing written, and the what-if answered without changing the case (NPV at 30 yr from gemini on a
copy of the case, or a plain "I can only give it by changing the case; shall I?"). No other economics touched.

## Actual

- 18:13:54 set_case refused by the user. The case lead tries to `finish` (18:15:39, "The case is unchanged - nothing
  was written") and the guard refuses it: "economics not asked: you wrote economics with set_case, but the user never
  answered the economics question. Economics enter the case only through ask_economics: call it now ...".
- So at 18:15:59 it calls `ask_economics` (request-109): a question proposing EVERY economics key from the catalogue's
  recommended rows, replacing the reference values the case holds: discount_rate 0.051 (case 0.05), electricity
  115.015 EUR/MWh (105.75), gas 37.5077 (39.92), carbon 57.4757 EUR/t (57.03), heat_cost_share 0.76 (0.8),
  capex.heat_exchanger 0.108893 EUR/W (0.5 EUR/(W/K), another quantity, QA-168 part 4), injection_pump 0.0990291 EUR/W
  (0.5), cooler 0.0490933 (0.1), gas_makeup 636893 EUR (50000), opex.fixed.heat_pump 1652.04 EUR/MW/yr (0.2239 %/yr),
  plus keys this plant has no use for (ice_storage, thermal_storage, electric_boiler ...), with "approve all" as the
  first option. One click on "approve all" would have rewritten the whole economics of a user who had just said "do not
  change the case".
- After "stop": the answer says the case is unchanged (right) and "I cannot give [the 30-year NPV] ... needs the analysis
  team to re-run estimate_costs"; the question the user asked is not answered. 4 min 15 s, 222 k tokens, 0.0072 USD.
- Routing: the coordinator sent the request to the project loop -> case lead (no costing tools), not to the analysis
  lead.

## Evidence

- `../evidence/QA-268/run-ca876a33-log.json` (case lead steps 2-9), `question-request-109.txt` (the whole question).

## Cause

- The case lead's finish guard (geomind 0.4.107+, QA-168 fix, `agents/case/lead.py` around `calls_of(messages,
  "ask_economics")`) counts a `set_case` of economics that the user DENIED as "wrote economics", and forces
  `ask_economics`.
- `ask_economics` proposes all keys from the catalogue even when the case already holds approved economics; it does not
  start from the case's values.

## Proposed fix

1. Finish guard: only a `set_case` that was applied counts; a denied (or refused) call never forces `ask_economics`.
2. `ask_economics`: when the case already has economics, ask only about the keys the task changes (here
   analysis_period), never re-propose the others.
3. Coordinator: "what would X be if Y" / "set Y and give me X" -> the analysis lead (it can cost; it reused a stored
   sensitivity study for "LCTS at 8 %" in 19 s, run e26ff474), not the project loop.
4. A what-if on an economics value that no stored study covers: the economist re-costs the stored result on a
   modified copy of the case (no write), or the lead asks once "change the case?".

## More evidence (2026-11-05 18:50 UTC, backend 1.1.117)

It happens after an APPLIED, user-instructed change too. Project `QA-TEST QA-AI-analysis-I 9`, run
ac818659-26af-400b-a6f6-9cd41513e38d, chat "Change two economics values to my own: discount rate 6 % and carbon price 80
EUR/t ...". The case lead's `set_case` (discount 0.06, carbon 80) was approved and applied; its `finish` ("Set the two
economics values ... and nothing else") was refused by the guard; it then sent `ask_economics` (request-107, 21 136
chars) whose note says "Every other economics key keeps the value the case already holds" but whose values are the
catalogue's recommended rows, not the case's: heat_cost_share 0.76 (case 0.8), gwp.CH4 27.9 (29.8),
capex.absorption_chiller 0.233861 EUR/W (0.3), ... "approve all" would overwrite them. I answered with text "Keep
every other value exactly as the case already has it." Question: `../evidence/QA-268/question-request-107-run-ac818659.json`.

## Fix

- 2026-11-05 18:56 UTC: deploy 36: backend 1.1.118, geomind 0.4.130, gemini 0.6.26 (hotfix-python-lead-II)

## Retest

- 2026-11-05 19:12 UTC, QA-AI-analysis-I, backend 1.1.120 (geomind 0.4.130+): project `QA-TEST QA-AI-analysis-I 6`,
  same chat text, run edaad491-cb24-4145-8a7a-a1028aafe79d. The `set_case` card now shows the value ("Economics values:
  analysis_period: 30 yr"); denied with the same reason. No `ask_economics` followed; the project lead sent the what-if to
  the analysis lead, the economist answered "no run-level analysis-period override exists", and the user got: case
  untouched, the 25-year figures, and a one-line offer ("if you want the 30-year NPV, the case's analysis_period has to
  be set to 30 yr ... yours to approve"). 2 min 8 s, 0.0073 USD. Verified (parts 1-3). Part 4 (a what-if re-costing on a
  copy of the case) is not there, so the 30-year NPV itself is still not available without a case change.
  Log: `../evidence/QA-268/run-edaad491-retest-log.json`.
