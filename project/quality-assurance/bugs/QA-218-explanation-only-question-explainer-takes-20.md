# QA-218: Explanation-only question: explainer takes 20 steps, 8.5 min, 1.45 M tokens; 26 search_rag hunting handbook sections it cannot open (no read_knowledge), 9 read_result, 7 read_case

| Field | Value |
|---|---|
| Status | open |
| Severity | major |
| Area | geomind |
| Reporter | QA-AI-project-I |
| Found | 2026-11-05 17:35 UTC |
| Versions | backend 1.1.104 to 1.1.106 (geomind 0.4.98+, gemini 0.6.17) |
| Where | https://api.geomind.team; project QA-TEST QA-AI-project-I 1 (35a70dbe-5e24-4f51-9c6f-50e06d47fe82); chat 134dae07-2e37-4a3a-ae0b-83b5e812017e; run afd1cd7a-675a-49cc-beb7-e40d6ee8c943 |
| Fixer | |

## Steps

1. Project with the reference case and HackathonPlant, already simulated, reviewed and costed in the chat (run b57abc5b...).
2. Message: "Explain only, do not build or simulate anything: which other plant configurations could serve this case, and why was an absorption chiller chosen for cooling here?"

## Expected

Routing is right (coordinator -> project lead -> explainer, nothing built: good). An answer from the case, the stored result and two or three handbook sections (handbook-design 7.2 absorption chillers, 8.2 when each archetype wins, the archetype table) in about 1 min.

## Actual

Run 17:22:45 to 17:31:11 UTC, 8 min 26 s; explainer 20 LLM calls, 1 451 815 input tokens, 397 s of LLM time, 0.032 USD (94 % of the run). The project lead then rewrites the explainer's 15 k-char answer (19.6 s).

- 26 `search_rag`, many asking for a section by its number or title: "7.2 absorption chillers ..." (steps 13, 19), "8.2 When each archetype wins ..." (13), "\"Choosing the cold source\" ... 7.8" (7, 9), "hackathon brief reference results ..." (4, 7, 10, 12, 15, 19). Each returns snippets of the same files (handbook-design.md, data-economics.csv, handbook-economics.md); the explainer cannot open the section it names.
- 9 `read_result` of module summaries (`cool_users`, `heat_users`, `chiller`, `heat_pump`, `d0.reservoir`, `flare`, `boiler`, `chiller_cooler`, the whole result) and 7 `read_case` (5 sections in step 1, `time` at 14, `demand` again at 17), against the prompt's "read once, in one step".
- Late steps grow: 52.8 s, 56.1 s, 55.2 s, 41.0 s, 85.9 s (9 525 output tokens) at 74 k to 90 k input tokens per call.
- The answer is forced into the verified-design headings (Design, Schematic, Capacities, Delivered, Costs, Checks, Open points, Decisions) although the question was about other families; the project lead re-formats it.

## Evidence

- Run log: `../evidence/QA-218/afd1cd7a-675a-49cc-beb7-e40d6ee8c943.log.json.gz`; trace: `../evidence/QA-218/afd1cd7a-675a-49cc-beb7-e40d6ee8c943.trace.txt` (every query and read).
- Project lead brief (step 1, tool `explainer`): "Explanation only ... answer them in text from the case, the knowledge base (search_rag / read_rag) and the stored design/result"; it names `read_rag`, which the explainer does not have.

## Cause

1. `geomind/agents/project/explainer.py`: the explainer has `search_rag` but no `read_knowledge` (the design and case agents have it), so a handbook section can only be fished for by search; the handbooks tell it the section numbers, which makes it search for them again and again.
2. `prompts/project/explainer.md` is written for one case only (explain the verified design, fixed 8 headings, read the KPIs and costs); there is no rule for a conceptual question, and no limit on search.
3. `prompts/project/lead.md`: "A request that asks only for an explanation ... is answered in text from the case, the knowledge base and the read tools" but it does not say by whom; the lead sends it to the explainer with the full verified-design frame.

## Proposed fix

- geomind `agents/project/explainer.py`: add `self.read_knowledge = for_run(tools.read_knowledge)` (read a handbook section by name), and in `explainer.md` Tools/Rules: "To read a handbook section, `read_knowledge(name, section)`; `search_rag` only to find which document holds a topic, at most 3 searches per answer."
- `explainer.md`: "For a question that is not the explanation of the verified design (other families, a concept, a why), answer that question only, under headings that fit it; read no result module the answer does not quote."
- Optional guard: a step limit for the explainer (e.g. 8) and `search_rag` refusing a query it already ran in this session.
- Expected: about 1 to 2 min and < 200 k tokens instead of 8.5 min and 1.45 M.

## Fix

## Retest
