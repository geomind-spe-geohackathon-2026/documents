import json,glob,collections,datetime as dt
rs={x['id']:x for x in json.load(open('/tmp/sa/data/runs.json'))}
def p(s): return dt.datetime.fromisoformat(str(s).replace('Z','+00:00'))
tok=[]
for f in sorted(glob.glob('/tmp/sa/data/*/log.json')):
    rid=f.split('/')[-2]; x=rs[rid]; S=json.load(open(f))['steps']
    ts=[p(s['ts']) for s in S]; st=p(x['started']); en=p(x['ended'])
    wall=(en-st).total_seconds(); llm=sum(c.get('duration') or 0 for s in S for c in s['llm_calls'])
    big=[]
    for i in range(1,len(S)):
        g=(ts[i]-ts[i-1]).total_seconds()
        if g>60: big.append((round(g),S[i-1]['agent'],[t['tool'] for t in S[i-1]['tool_calls']][:3]))
    asks=sum((t.get('duration') or 0) for s in S for t in s['tool_calls'] if t['tool'] in('ask_user','ask_economics'))
    print(rid[:8],x['_project_name'][9:28],f"wall {wall/60:.1f} llm {llm/60:.1f} ask {asks/60:.1f} first-step {(ts[0]-st).total_seconds():.0f}s",big[:4])
    for s in S:
        for c in s['llm_calls']: tok.append((c.get('input_tokens') or 0,c.get('output_tokens') or 0,c.get('duration') or 0,s['agent']))
import statistics as stt
print('input tokens median',stt.median(t[0] for t in tok),'max',max(t[0] for t in tok),'output median',stt.median(t[1] for t in tok))
for a in sorted({t[3] for t in tok}):
    T=[t for t in tok if t[3]==a]; print(f"{a:15s} n{len(T):4d} in_med {stt.median(t[0] for t in T):7.0f} in_max {max(t[0] for t in T):7d} out_med {stt.median(t[1] for t in T):5.0f} s/call {sum(t[2] for t in T)/len(T):5.1f}")
slow=sorted(tok,key=lambda t:-t[2])[:6]; print(slow)
