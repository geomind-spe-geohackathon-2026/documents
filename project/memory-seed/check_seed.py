"""Check that geomind's search finds the seed's designs for a case, on a local memory only.

Loads ``seed.json`` into an in-memory store (``geomind.stores.memory.MemoryMemory``), takes the
features of gemini's example case of the competition brief and runs ``search_experience`` with
the backend's ``GEOMIND_MEMORY_SIMILARITY`` (0.8). Nothing is written anywhere.

    PYTHONPATH=gemini:geomind geomind/.venv/bin/python documents/project/memory-seed/check_seed.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
THRESHOLD = 0.8
"""The backend's GEOMIND_MEMORY_SIMILARITY."""


def main():
    """Print each entry the search finds for each example case, with its similarity."""
    import gemini as gm

    from geomind.stores.memory import MemoryMemory, search_experience
    from geomind.tools.memory import case_features

    seed = json.loads((Path(__file__).with_name("seed.json")).read_text())
    memory = MemoryMemory(seed["entries"])
    for example in ("hackathon_2026", "shallow_district"):
        case = gm.Case.from_json(ROOT / "gemini" / "examples" / example / "case.json")
        found = search_experience(memory, case_features(case), THRESHOLD)
        print(f"{example}: {len(found)} found")
        for item in found:
            lcts = item["kpis"].get("lcts", {})
            print(f"  {item['id']}  similarity {item['similarity']}  lcts {lcts.get('value')} {lcts.get('unit')}")


if __name__ == "__main__":
    main()
