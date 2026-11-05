import sys, json
from pathlib import Path
sys.path.insert(0, "/home/fatemec/geomind-spe-hackathon-2026/backend")
from scripts.seed_qa_projects import Api, credentials
email, pw = credentials(Path("/home/fatemec/geomind-spe-hackathon-2026/backend/.env"))
api = Api("https://api.geomind.team/api/v1", email, pw)
out = Path("/tmp/sa/data")
def all_items(path, **params):
    out=[]; cur=None
    while True:
        q=dict(params, size=50 if 'project' not in params else 100)
        if cur: q["cursor"]=cur
        r=api.call("GET", path, params=q)
        out+=r["items"]; cur=r.get("next")
        if not cur: return out
projs=all_items("/workspace/projects")
print(len(projs),"projects")
runs=[]
for p in projs:
    for x in all_items("/assistant/runs", project=p["id"]):
        x["_project_name"]=p.get("name"); runs.append(x)
(out/"runs.json").write_text(json.dumps(runs))
print(len(runs),"runs")
