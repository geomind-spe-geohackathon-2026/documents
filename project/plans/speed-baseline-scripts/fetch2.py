import sys, json
from pathlib import Path
sys.path.insert(0, "/home/fatemec/geomind-spe-hackathon-2026/backend")
from scripts.seed_qa_projects import Api, credentials
email, pw = credentials(Path("/home/fatemec/geomind-spe-hackathon-2026/backend/.env"))
api = Api("https://api.geomind.team/api/v1", email, pw)
runs=[x for x in json.load(open("/tmp/sa/data/runs.json")) if (x['started'] or '')>='2026-11-05']
for x in runs:
    d=Path("/tmp/sa/data")/x['id']; d.mkdir(exist_ok=True)
    for name,path in (("log","log"),("agents","agents")):
        try: (d/f"{name}.json").write_text(json.dumps(api.call("GET",f"/assistant/runs/{x['id']}/{path}", params={"project":x['project']})))
        except SystemExit as e: (d/f"{name}.err").write_text(str(e))
print("ok")
