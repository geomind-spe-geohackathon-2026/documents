"""Build experience-memory entries from gemini's own example studies, offline; insert nothing.

Each example folder of gemini (``examples/<name>/study.json`` with its ``case.json``) is run as
gemini's ``gm.Study``: every candidate plant is sized, searched on its objective, simulated for
the whole year and judged by gemini's verdict. Every candidate whose best design is feasible
(no violation) becomes one entry in the format of geomind's ``keep_design``
(``geomind/tools/memory.py``): the case's general features, the sections it sets and its
services, the design, the result, gemini's KPIs, the verdict, the candidates the study tried and
its lessons. Nothing is invented: every value is gemini's; a candidate that is not feasible is
left out. The entries are written to ``seed.json`` beside this script; someone with access to
the memory store imports it.

Run from the project root, with gemini's dev clone and geomind's clone on the path:

    PYTHONPATH=gemini:geomind geomind/.venv/bin/python documents/project/memory-seed/build_seed.py
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
GEMINI = ROOT / "gemini"
EXAMPLES = ("hackathon_2026", "shallow_district")
"""The example folders of gemini whose study is run."""
PROCESSES = 8
"""Worker processes of the searches; the numbers equal a serial run."""
OUT = Path(__file__).resolve().parent / "seed.json"


def commit():
    """Return the short commit of gemini's clone, which the entries cite."""
    found = subprocess.run(
        ["git", "-C", str(GEMINI), "rev-parse", "--short", "HEAD"], capture_output=True, text=True
    )
    return found.stdout.strip()


def entry(example, study, run, case, case_data, names, version, head):
    """Return one experience entry of a feasible candidate, in ``keep_design``'s format."""
    from geomind.tools.gemini.assessment import kpi_values, rounded
    from geomind.tools.memory import case_features, case_summary
    from geomind.utils.json import to_jsonable

    source = f"gemini study examples/{example}/study.json, gemini {version} ({head})"
    return {
        "id": f"seed-{example}-{run.plant_name}",
        "features": case_features(case),
        "case": case_summary(case_data),
        "design": f"examples/{example} {run.plant_name}, sized and searched ({study.method} "
        f"{study.objective}, {study.evaluations} evaluations per doublet count, seed {study.seed})",
        "result": f"examples/{example}/study.json: {run.plant_name}",
        "kpis": to_jsonable(rounded(kpi_values(run.plant, case, run.results))),
        "verdict": "passed",
        "families": names,
        "lessons": [],
        "origin": {"run": None, "source": source},
        "project_id": None,
    }


def entries_of(example, version, head):
    """Return the entries of one example's study and a line per candidate on why it is in or out."""
    import gemini as gm

    folder = GEMINI / "examples" / example
    study = gm.Study.from_json(folder / "study.json")
    case_data = json.loads((folder / "case.json").read_text())
    case = gm.Case.from_json(folder / "case.json")
    with gm.runtime.settings(processes=PROCESSES):
        result = study.run()
    names = [run.plant_name for run in result.runs]
    found, notes = [], []
    for run in result.runs:
        reasons = [item.get("name") for item in run.verdict.get("reasons") or ()]
        if not run.verdict.get("feasible"):
            notes.append(f"{example} {run.plant_name}: left out, infeasible {reasons}")
            continue
        found.append(entry(example, study, run, case, case_data, names, version, head))
        notes.append(f"{example} {run.plant_name}: kept, feasible")
    return found, notes


def main():
    """Run every example study, write the seed and print why each candidate is in or out."""
    import gemini as gm

    head = commit()
    entries, notes = [], []
    for example in EXAMPLES:
        if not (GEMINI / "examples" / example / "study.json").exists():
            continue
        found, why = entries_of(example, gm.__version__, head)
        entries += found
        notes += why
    OUT.write_text(json.dumps({"kind": "experience", "entries": entries}, indent=1) + "\n")
    print("\n".join(notes))
    print(f"{len(entries)} entries written to {OUT}")


if __name__ == "__main__":
    sys.exit(main())
