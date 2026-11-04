# Improvements

Things that work but should be faster, cheaper or make fewer mistakes. A bug (something wrong)
goes in [BUGS.md](BUGS.md); an idea to make the app better goes here. One section per idea,
`IMP-<nnn>`; take the next id and add your section at once. Statuses: idea, agreed, doing, done,
dropped. A change to the agents' behaviour, or to gemini, needs Sahand's OK before work starts.

## Where the time goes: run a61cfb19 (2026-11-04)

Chat "design heating and cooling based on files" (challenge PDF and two daily demand CSVs);
[run JSON](evidence/QA-007/run-a61cfb19bfb04ae99e92060fc5bd2e40.json.gz), downloaded while the run was
still active, 58 steps.

- About 26 minutes, and the design had not started: all of it went to setting the case.
- LLM calls: about 1,575 s. Tools: about 90 s, of which 73 s is the nested geoscientist (LLM
  again); gemini's own tool time is under 20 s. The LLM is about 99 % of the time.
- 2.47 M input tokens, 90 k output tokens, 0.06 USD. The case lead's calls carry 40 k to 78 k
  input tokens each.
- The slowest calls are the ones that write long JSON by hand: 209 s, 149 s, 122 s (cut at the
  output limit), 106 s, 87 s.
- Lost work: a 504 that stopped the case lead (about 10 min, QA-011), three empty answers
  (QA-012), one call cut at the output limit (QA-013), three asks of the same question (QA-009).

## Summary

| Id | Status | Area | Idea | Gain |
|---|---|---|---|---|
| IMP-001 | idea | geomind | ask_economics fills the catalogue's recommended rows itself; the agent sends only exceptions | 3-4 min per run, no output-limit cuts |
| IMP-002 | idea | geomind | ask_economics checks everything and lists every problem in one refusal | fewer retries (QA-007) |
| IMP-003 | idea | geomind | ask_user answers go into the problem state and every later agent's brief | no repeated questions (QA-009) |
| IMP-004 | idea | geomind, backend | Retry 5xx and timeouts with a back-off; stream the LLM calls | no lost nested runs (QA-011) |
| IMP-005 | idea | geomind | read_rag on a time-series CSV returns a summary, not all rows | smaller contexts, fewer empty answers |
| IMP-006 | idea | geomind | A defined path for "use reasonable assumptions": find sourced candidates and ask to approve | the design can go on (QA-010) |
| IMP-007 | idea | data, geomind | Catch what gemini refuses before the agent sends it | fewer refused calls |
| IMP-008 | idea | geomind | Keep the case lead's context small: drop file texts and old tool outputs once used | faster calls, lower cost |
| IMP-009 | idea | geomind | read_case returns an unset section as empty with a note, not an error | fewer red errors (QA-001, QA-014) |

## IMP-001: ask_economics fills the recommended rows itself

Now the case lead writes every economics key (about 55) with its row, its `others` and a long note.
These calls take 87 to 209 s and 6,000 to 13,000 output tokens; one hit the 16,000-token limit
(QA-013). The catalogue already marks the recommended row per key. Proposal: ask_economics takes
only the exceptions (a key with a different row, a key left open, a note per key), and the tool
fills the rest from the catalogue. The question the user sees stays the same.

## IMP-002: one refusal lists every problem

ask_economics refuses on the first problem it finds; the agent fixes it and the next call fails on
another one (QA-007). set_case already lists every problem in one answer ("fix every one in the
next call"). ask_economics should do the same, and drop a key that is not an economics key with a
note instead of refusing the whole question.

## IMP-003: user answers are kept for the whole run

An ask_user answer stays inside the nested run that asked. A new case lead run does not know it,
and the project lead asks for the same values again. Proposal: every answer is written to the
problem state (question, answer, time) and is part of every later brief; the project lead reads it
before it sends a task that asks the user.

## IMP-004: retry and stream LLM calls

One OpenRouter 504 ("Upstream idle timeout exceeded") stopped the nested case lead and lost about
10 minutes. Proposal: retry 5xx, 429 and timeouts with a back-off (for example 3 tries); stream the
LLM calls so a long generation does not hit an idle timeout.

## IMP-005: summaries for time-series files

read_rag returns the full text of each 365-row demand CSV, and the case lead reads the files again
in every run. set_case takes the file itself, so the agent needs only the shape: columns, number of
rows, time span and step, minimum, maximum, peak date, annual sum. That keeps the context smaller;
the empty answers (QA-012) came on contexts of 74 k to 78 k tokens.

## IMP-006: a path for a delegated answer

When the user says "use reasonable, documented engineering assumptions", the agent now sets
nothing (QA-010). Proposal, within the no-default-values rule: the agent searches RAG and the
connectors (for example a weather source for site air, a technology data sheet for network return
temperatures), puts the sourced candidates to the user as one question with approve all / change
some, and sets what is approved. If nothing has a source, the run ends with one clear message: the
values the user must type, with units, and that the design waits for them. Needs Sahand's decision.

## IMP-007: catch gemini's refusals earlier

Refusals seen in one run: a catalogue unit the key does not take (`kg CO2e/kg CH4` on a
dimensionless key, QA-004), an efficiency as 70 % instead of 0.7 (QA-002), a case key in the
economics (QA-007). Proposal: fix the catalogue rows so every unit is one the key accepts (a check
in the catalogue's tests); say in the case lead's prompt that an efficiency is a fraction 0-1 with
no unit and no `over`/`when`.

## IMP-008: a smaller context for the case lead

The case lead's input grows to 78 k tokens per call (the PDF, both CSVs, catalogue rows, earlier
tool outputs). Every call pays for it in time. Proposal: once a file's values are in the case,
replace its text in the context with a short line; keep only the last output of a repeated tool;
let the case lead read the catalogue by key, not by whole groups.

## IMP-009: unset sections are not errors

read_case on a project with no case, or on a section that is not set yet, returns a red error
(QA-001, QA-014). Three agents in this run start with that error. Proposal: return the empty
section with a note ("not set yet; set_case sets it"), and give the list of sections that exist.
