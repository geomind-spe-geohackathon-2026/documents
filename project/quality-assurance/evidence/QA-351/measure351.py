"""Characters agents got from Knowledge reads in recorded runs, before and with QA-351's rule."""
import gzip, glob, json, sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, ".")
from geomind.tools.files import contents_first

ROOT = Path("../documents/project/quality-assurance")
docs = {f"knowledge/{p.name}": p.read_text() for p in (ROOT / "inputs").glob("handbook-*.md")}
before, after, calls, whole = defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int)
runs = 0
bydoc = defaultdict(lambda: [0, 0])
for path in sorted(glob.glob(str(ROOT / "evidence/*/run-*.json*"))):
    try:
        data = json.load(gzip.open(path) if path.endswith(".gz") else open(path))
    except Exception:
        continue
    steps = data.get("steps") if isinstance(data, dict) else None
    if not steps:
        continue
    runs += 1
    for step in steps:
        for call in step.get("tool_calls") or []:
            if call.get("tool") not in ("read_rag", "read_knowledge"):
                continue
            arguments = call.get("input") or {}
            name = str(arguments.get("name", ""))
            if call["tool"] == "read_knowledge" and not name.startswith("knowledge/"):
                name = "knowledge/" + name.lstrip("/")
            if not name.startswith("knowledge/"):
                continue
            agent = step.get("agent") or "?"
            got = len(json.dumps(call.get("output"), ensure_ascii=False))
            before[agent] += got
            calls[agent] += 1
            plain = not any(arguments.get(k) for k in ("section", "outline", "rows", "columns", "start"))
            out = call.get("output") if isinstance(call.get("output"), dict) else {}
            text = docs.get(name)
            if text is None and out.get("total", 0) > 12_000 and isinstance(out.get("text"), str):
                text = out["text"] + " " * (out["total"] - len(out["text"]))
            bydoc[name][0] += got
            if plain and text is not None and contents_first(name, text) is not None:
                bydoc[name][1] += 1
                whole[agent] += 1
                after[agent] += len(json.dumps(contents_first(name, text), ensure_ascii=False))
            else:
                after[agent] += got
print(f"runs read: {runs}")
print(f"{'agent':24} {'calls':>5} {'whole reads':>11} {'before chars':>13} {'after chars':>12}")
for agent in sorted(before, key=lambda a: -before[a]):
    print(f"{agent:24} {calls[agent]:5} {whole[agent]:11} {before[agent]:13,} {after[agent]:12,}")
print(f"{'TOTAL':24} {sum(calls.values()):5} {sum(whole.values()):11} {sum(before.values()):13,} {sum(after.values()):12,}")
print()
for name, (chars, n) in sorted(bydoc.items(), key=lambda kv: -kv[1][0])[:12]:
    print(f"{name:55} {chars:11,}  whole reads {n}")
