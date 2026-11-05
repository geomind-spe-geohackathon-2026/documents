import sys, json
from pathlib import Path
sys.path.insert(0, "/home/fatemec/geomind-spe-hackathon-2026/backend")
from scripts.seed_qa_projects import Api, credentials
email, pw = credentials(Path("/home/fatemec/geomind-spe-hackathon-2026/backend/.env"))
api = Api("https://api.geomind.team/api/v1", email, pw)
out = Path("/tmp/sa/data")
projs = []
page = 1
while True:
    r = api.call("GET", "/workspace/projects", params={"page": page, "size": 100})
    items = r["items"] if isinstance(r, dict) else r
    projs += items
    if not isinstance(r, dict) or page >= r.get("pages", 1): break
    page += 1
print(len(projs), "projects", list(projs[0].keys()) if projs else None)
runs = []
for p in projs:
    pg = 1
    while True:
        r = api.call("GET", "/assistant/runs", params={"project": p["id"], "page": pg, "size": 100})
        for x in r["items"]:
            x["_project_name"] = p.get("name"); runs.append(x)
        if pg >= r.get("pages", 1): break
        pg += 1
(out/"runs.json").write_text(json.dumps(runs))
print(len(runs), "runs", list(runs[0].keys()) if runs else None)
