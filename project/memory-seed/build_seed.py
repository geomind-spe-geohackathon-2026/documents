"""Build experience-memory entries from the best verified designs, offline; insert nothing.

Sources, each re-checked on the gemini of the clone (simulated for the whole year, judged by
gemini's verdict, costed by its report):

- gemini's example studies (``gemini/examples/<name>/study.json`` on its ``case.json``): every
  candidate plant sized, searched on the study's objective and simulated;
- exports of real designs (``exports/<name>/`` beside this script): ``plant.json`` (the design
  as gemini writes it), ``case.json`` with the case files it names, and ``origin.json``
  (``{project_id, result, run, source}``), read-only copies from the app's store.

Only feasible designs are kept, and of them the best of each plant family (lowest LCTS, then
lowest CO2) for each case; the best design of each case also gets the one-at-a-time sensitivity
of LCTS from gemini, whose largest swings are its lessons. Each entry has the format of geomind's
``keep_design`` (``geomind/tools/memory.py``) plus the design and the case in full: ``plant``
(every module, parameter, sizing, setpoint and connection), ``case_file`` (every section and
value as the case file states it, sources included), ``case_files`` (the content of its JSON
files, the economics) and ``checks`` (gemini's verdict with each requirement). Nothing is
invented: every value is gemini's or the source file's. Written to ``seed.json``.

Run from the project root:

    PYTHONPATH=gemini:geomind geomind/.venv/bin/python documents/project/memory-seed/build_seed.py
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
GEMINI = ROOT / "gemini"
EXAMPLES = ("hackathon_2026", "shallow_district")
"""The example folders of gemini whose study is run."""
PROCESSES = 8
"""Worker processes of the searches; the numbers equal a serial run."""
LESSONS = 3
"""How many of the sensitivity's largest swings become lessons."""
OUT = HERE / "seed.json"


def commit():
    """Return the short commit of gemini's clone, which the entries cite."""
    found = subprocess.run(
        ["git", "-C", str(GEMINI), "rev-parse", "--short", "HEAD"], capture_output=True, text=True
    )
    return found.stdout.strip()


def json_files(folder, case_data):
    """Return ``{name: content}`` of the JSON files the case names (the economics), as data."""
    names = [value for value in case_data.values() if isinstance(value, str) and value.endswith(".json")]
    return {name: json.loads((folder / name).read_text()) for name in names if (folder / name).exists()}


def evaluated(plant, case):
    """Return ``(results, verdict dict, kpis)`` of a whole-year run of ``plant`` on ``case``."""
    import gemini as gm

    from geomind.tools.gemini.assessment import kpi_values, rounded
    from geomind.utils.json import to_jsonable

    results = gm.simulate(plant, case)
    verdict = gm.evaluate.verdict(plant, case, results)
    return results, to_jsonable(verdict.to_dict()), to_jsonable(rounded(kpi_values(plant, case, results)))


def entry(name, plant, case, folder, kpis, checks, design, families, origin):
    """Return one experience entry, in ``keep_design``'s format with the design and case in full."""
    from geomind.tools.memory import case_features, case_summary
    from geomind.utils.json import to_jsonable

    case_data = json.loads((folder / "case.json").read_text())
    return {
        "id": f"seed-{name}",
        "features": case_features(case),
        "case": case_summary(case_data),
        "design": design,
        "result": origin.get("result") or design,
        "kpis": kpis,
        "verdict": "passed",
        "families": families,
        "lessons": [],
        "origin": origin,
        "project_id": origin.pop("project_id", None),
        "plant": to_jsonable(plant.to_dict()),
        "case_file": case_data,
        "case_files": json_files(folder, case_data),
        "checks": checks,
    }


def example_entries(example, version, head):
    """Return the feasible candidates of one example study, each re-checked, and notes on each."""
    import gemini as gm

    folder = GEMINI / "examples" / example
    study = gm.Study.from_json(folder / "study.json")
    case = gm.Case.from_json(folder / "case.json")
    with gm.runtime.settings(processes=PROCESSES):
        result = study.run()
    families = [run.plant_name for run in result.runs]
    found, notes = [], []
    for run in result.runs:
        _, checks, kpis = evaluated(run.plant, case)
        if not checks.get("feasible"):
            reasons = [item.get("name") for item in checks.get("reasons") or ()]
            notes.append(f"{example} {run.plant_name}: left out, infeasible {reasons}")
            continue
        source = f"gemini study examples/{example}/study.json, gemini {version} ({head})"
        design = (
            f"examples/{example} {run.plant_name}, sized and searched ({study.method} "
            f"{study.objective}, {study.evaluations} evaluations per doublet count, seed {study.seed})"
        )
        origin = {"run": None, "source": source, "result": f"examples/{example}/study.json: {run.plant_name}"}
        item = entry(f"{example}-{run.plant_name}", run.plant, case, folder, kpis, checks, design, families, origin)
        found.append((example, run.plant_name, item, run.plant, case))
        notes.append(f"{example} {run.plant_name}: feasible")
    return found, notes


def export_entries(version, head):
    """Return the feasible exported designs, each re-checked on this gemini, and notes on each."""
    import gemini as gm

    found, notes = [], []
    for folder in export_folders():
        origin_file = folder / "origin.json"
        origin = json.loads(origin_file.read_text()) if origin_file.exists() else {}
        plant = gm.Plant.from_json(folder / "plant.json")
        case = gm.Case.from_json(folder / "case.json")
        _, checks, kpis = evaluated(plant, case)
        if not checks.get("feasible"):
            notes.append(f"export {folder.name}: left out, infeasible on gemini {version}")
            continue
        family = plant.to_dict().get("type") or folder.name
        origin = {**origin, "source": f"{origin.get('source', 'exported design')}; re-checked on gemini {version} ({head})"}
        design = origin.get("design") or f"exported design {folder.name}"
        item = entry(f"export-{folder.name}", plant, case, folder, kpis, checks, design, [family], dict(origin))
        found.append((case_key(item), family, item, plant, case))
        notes.append(f"export {folder.name}: feasible")
    return found, notes


def export_folders():
    """Return each exported design's folder: ``export/`` or ``exports/``, or one design in it."""
    folders = []
    for base in (HERE / "export", HERE / "exports"):
        if (base / "plant.json").exists():
            folders.append(base)
        elif base.is_dir():
            folders += sorted(path for path in base.iterdir() if (path / "plant.json").exists())
    return folders


def case_key(item):
    """Return the key of an entry's case: its name, for grouping the best designs per case."""
    return item["case_file"].get("name") or "case"


def score(item):
    """Return the ranking key of an entry: LCTS, then CO2, the lower the better."""
    kpis = item["kpis"]

    def number(name):
        value = (kpis.get(name) or {}).get("value")
        return float("inf") if value is None else float(value)

    return number("lcts"), number("co2")


def best_per_family(found):
    """Return the best entry of each (case, family), and the best of each case, ranked."""
    best = {}
    for case_name, family, item, plant, case in found:
        key = (case_key(item), family)
        if key not in best or score(item) < score(best[key][0]):
            best[key] = (item, plant, case)
    return sorted(best.values(), key=lambda kept: (case_key(kept[0]), score(kept[0])))


def sensitivity_lessons(plant, case):
    """Return the largest LCTS swings of gemini's one-at-a-time sensitivity, as lessons."""
    import gemini as gm

    from geomind.utils.json import to_jsonable

    try:
        tornado = to_jsonable(gm.study.sensitivity(plant, case, ["lcts"]).to_dict())
    except gm.errors.GeminiError:
        return []
    rows = sorted(
        tornado.get("rows") or (),
        key=lambda row: abs((row.get("effect") or {}).get("value") or 0),
        reverse=True,
    )
    lessons = []
    for row in rows[:LESSONS]:
        low, high = row.get("at_low") or {}, row.get("at_high") or {}
        lessons.append(
            f"LCTS moves most with {row.get('parameter')}: {low.get('value'):.4g} to "
            f"{high.get('value'):.4g} {high.get('unit')} over its range "
            f"({(row.get('low') or {}).get('value')} to {(row.get('high') or {}).get('value')} "
            f"{(row.get('high') or {}).get('unit') or ''}), gemini sensitivity".rstrip()
        )
    return lessons


def main():
    """Re-check every source, keep the best per family and case, add lessons, write the seed."""
    import gemini as gm

    head = commit()
    found, notes = [], []
    for example in EXAMPLES:
        if (GEMINI / "examples" / example / "study.json").exists():
            items, why = example_entries(example, gm.__version__, head)
            found += items
            notes += why
    if export_folders():
        items, why = export_entries(gm.__version__, head)
        found += items
        notes += why
    kept = best_per_family(found)
    leaders = {}
    for item, plant, case in kept:
        leaders.setdefault(case_key(item), (item, plant, case))
        if item["id"].startswith("seed-export-"):
            leaders[item["id"]] = (item, plant, case)
    for item, plant, case in leaders.values():
        with gm.runtime.settings(processes=PROCESSES):
            item["lessons"] = sensitivity_lessons(plant, case)
    entries = [item for item, _, _ in kept]
    OUT.write_text(json.dumps({"kind": "experience", "entries": entries}, indent=1) + "\n")
    print("\n".join(notes))
    for item in entries:
        lcts, co2 = score(item)
        print(f"kept {item['id']}: lcts {lcts} co2 {co2} lessons {len(item['lessons'])}")
    print(f"{len(entries)} entries written to {OUT}")


if __name__ == "__main__":
    sys.exit(main())
