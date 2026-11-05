import json,glob,collections,datetime as dt
rs={x['id']:x for x in json.load(open('/tmp/sa/data/runs.json'))}
def p(s): return dt.datetime.fromisoformat(str(s).replace('Z','+00:00'))
A=collections.defaultdict(lambda:[0,0.0,0.0,0.0,0]) # steps, llm s, tool s, gap s, runs
slow_tools=[];slow_llm=[];ttool=collections.defaultdict(lambda:[0,0.0])
runs_seen=collections.defaultdict(set)
for f in glob.glob('/tmp/sa/data/*/log.json'):
    rid=f.split('/')[-2]; d=json.load(open(f)); S=d['steps']
    for i,s in enumerate(S):
        a=A[s['agent']]; a[0]+=1; runs_seen[s['agent']].add(rid)
        l=sum(c.get('duration') or 0 for c in s['llm_calls']); a[1]+=l
        for c in s['llm_calls']:
            slow_llm.append((c.get('duration') or 0,rid[:8],s['agent'],s['index'],(c.get('usage') or {}).get('prompt_tokens') if isinstance(c.get('usage'),dict) else None))
        for t in s['tool_calls']:
            du=t.get('duration') or 0
            if t['tool'] in ('ask_user','ask_economics'): continue
            ttool[t['tool']][0]+=1; ttool[t['tool']][1]+=du
            if s['agent']!=t['tool']: a[2]+=du
            slow_tools.append((du,rid[:8],s['agent'],t['tool']))
print('agent steps llm_min tool_min runs')
for k,v in sorted(A.items(),key=lambda kv:-kv[1][1]): print(f"{k:24s} {v[0]:4d} {v[1]/60:6.1f} {v[2]/60:6.1f} {len(runs_seen[k])}")
print('\ntool calls total_min mean_s (excluding delegations)')
DEL={'case_lead','geoscientist','design_lead','economist','analysis_lead','reviewer','explainer','project_lead','support_lead','curator'}
for k,v in sorted(ttool.items(),key=lambda kv:-kv[1][1])[:15]:
    if k not in DEL: print(f"{k:22s} {v[0]:4d} {v[1]/60:6.2f} {v[1]/v[0]:6.1f}")
print('\nslowest llm calls');[print(x) for x in sorted(slow_llm,reverse=True)[:10]]
print('\nslowest tool calls (non-delegation)');[print(x) for x in sorted([x for x in slow_tools if x[3] not in DEL],reverse=True)[:12]]
import statistics as st
L=[x[0] for x in slow_llm]; print('\nllm calls',len(L),'median',st.median(L),'mean',sum(L)/len(L),'total min',sum(L)/60)
