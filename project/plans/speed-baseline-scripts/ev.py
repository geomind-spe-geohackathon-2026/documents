import sys, json, httpx
from pathlib import Path
sys.path.insert(0, "/home/fatemec/geomind-spe-hackathon-2026/backend")
from scripts.seed_qa_projects import Api, credentials
email, pw = credentials(Path("/home/fatemec/geomind-spe-hackathon-2026/backend/.env"))
api = Api("https://api.geomind.team/api/v1", email, pw)
rid="9696f5d4-4f99-4c2c-9db9-173d94e11eab"
runs={x['id']:x for x in json.load(open('/tmp/sa/data/runs.json'))}
proj=runs[rid]['project']
with api.http.stream("GET",f"/assistant/runs/{rid}/events",params={"project":proj},headers={"Accept":"text/event-stream"},timeout=30) as r:
    n=0
    for line in r.iter_lines():
        print(line[:400]); n+=1
        if n>60: break
