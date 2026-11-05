import json,datetime as dt,collections
res=json.load(open('res.json')); tools=json.load(open('tools.json')); causes=json.load(open('causes.json'))
def p(s): return dt.datetime.fromisoformat(s.replace('Z','+00:00')) if s else None
rows=[]
for rid,r in res.items():
    ru=r['run']; a,b=p(ru['started']),p(ru['ended'])
    wall=(b-a).total_seconds()/60 if a and b else None
    rows.append((ru['started'],rid[:8],ru['_project_name'],ru['status'],wall,r))
rows.sort()
def cell(r,k):
    v=r['stages'].get(k)
    return f"{v['steps']} / {v['t']/60:.1f}" if v else "-"
L=[]
L.append("| Started (UTC) | Run | Project | Status | Wall min | Case steps / min | Plant | Sizing | Simulate | Other | Calls (refused) | Q / A cards | Instances |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for s,i,n,st,w,r in rows:
    calls=sum(v['tools'] for v in r['stages'].values()); err=sum(v['err'] for v in r['stages'].values())
    q=sum(v['cards_q'] for v in r['stages'].values()); a=sum(v['cards_a'] for v in r['stages'].values())
    L.append(f"| {s[5:16].replace('T',' ')} | {i} | {n} | {st} | {w:.1f} |" if w is not None else f"| {s[5:16].replace('T',' ')} | {i} | {n} | {st} | - |")
    L[-1]+=f" {cell(r,'case')} | {cell(r,'plant')} | {cell(r,'sizing')} | {cell(r,'simulate')} | {cell(r,'other')} | {calls} ({err}) | {q} / {a} | {len(r['inst'])} |"
runtab="\n".join(L)
T=collections.defaultdict(collections.Counter)
for r in res.values():
    for k,v in r['stages'].items():
        for a,b in v.items(): T[k][a]+=b
nr=collections.Counter(k for r in res.values() for k in r['stages'])
st=["| Stage | Runs with it | Steps | Tool calls | Refused | Refused % | Active min total | Active min per run | Q cards | A cards |","|---|---|---|---|---|---|---|---|---|---|"]
for k in ('case','plant','sizing','simulate','other'):
    v=T[k]; st.append(f"| {k} | {nr[k]} | {v['steps']} | {v['tools']} | {v['err']} | {100*v['err']/v['tools']:.0f}% | {v['t']/60:.0f} | {v['t']/60/nr[k]:.1f} | {v['cards_q']} | {v['cards_a']} |")
sttab="\n".join(st)
tt=["| Tool | Calls | Refused | Refused % | First tries | First-try refused | First-try refusal % |","|---|---|---|---|---|---|---|"]
for k,v in sorted(tools['tool_stat'].items(),key=lambda kv:-kv[1][1]):
    if v[0]>=10 and v[1]>0: tt.append(f"| {k} | {v[0]} | {v[1]} | {100*v[1]/v[0]:.1f}% | {v[2]} | {v[3]} | {100*v[3]/max(v[2],1):.1f}% |")
tttab="\n".join(tt)
tc=sum(v[0] for v in tools['tool_stat'].values()); te=sum(v[1] for v in tools['tool_stat'].values())
rep=", ".join(f"{k} {v}" for k,v in sorted(tools['repeats'].items(),key=lambda x:-x[1])[:6])
rer=", ".join(f"{k} {v}" for k,v in sorted(tools['rereads'].items(),key=lambda x:-x[1])[:6])
json.dump(dict(runtab=runtab,sttab=sttab,tttab=tttab,tc=tc,te=te,rep=rep,rer=rer,n=len(rows)),open('tables.json','w'))
print(sttab);print(tc,te,rep,rer)
print(runtab[:3000])
