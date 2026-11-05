# Experience-memory seed

`seed.json` holds experience entries in the format geomind's `keep_design` writes
(`geomind/tools/memory.py`): the case's general features, the sections it sets and its services,
the design, the result, gemini's KPIs, the verdict, the candidates tried, lessons and the origin.

- Source: gemini's own example studies (`gemini/examples/<name>/study.json` on its `case.json`),
  run offline by `build_seed.py` on gemini 0.6.35. Every candidate is sized, searched on its
  objective, simulated for the whole year and judged by gemini's verdict; only feasible designs
  are kept. Every value is gemini's; `origin.source` names the study file and gemini's commit.
- Not included: designs of agent runs. Their plant files are in production's run store, not in
  the local files, so they cannot be re-evaluated here without inventing values.
- `check_seed.py` loads the seed into an in-memory store and runs geomind's `search_experience`
  with the backend's similarity threshold (0.8) for each example case.
- Nothing is inserted into any database by these scripts. Someone with access to the memory
  store imports `seed.json`.
