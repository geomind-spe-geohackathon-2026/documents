# Experience-memory seed

`seed.json` holds the best verified designs as experience entries, in the format geomind's
`keep_design` writes (`geomind/tools/memory.py`), with the design and the case in full:

- `plant`: the design as gemini writes it (every module, parameter, sizing, setpoint, connection);
- `case_file` and `case_files`: the case file with every section, value and source, and the
  content of its JSON files (the economics);
- `kpis`, `verdict`, `checks`: gemini's KPIs and its verdict with every requirement;
- `lessons`: for the best design of each case, the largest LCTS swings of gemini's one-at-a-time
  sensitivity of that design; empty where no study shows one;
- `origin`: where the design comes from (gemini study file and commit, or the exported run).

How it is built (`build_seed.py`, offline):

- gemini's example studies (`gemini/examples/<name>/study.json`) are run on the gemini clone;
- exported real designs in `export/` (or `exports/<name>/`: `plant.json`, `case.json` with its
  files, `origin.json`) are re-checked the same way;
- every design is simulated for the whole year and judged by gemini's verdict; only feasible
  designs are kept, and of them the best of each plant family per case (lowest LCTS, then CO2).

`check_seed.py` loads the seed into an in-memory store and runs geomind's `search_experience`
with the backend's similarity threshold (0.8) for each example case.

Nothing is inserted into any database by these scripts. Someone with access to the memory
store imports `seed.json`.
