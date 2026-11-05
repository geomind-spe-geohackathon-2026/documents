import json,glob,collections,re,sys
D=sys.argv[1]; AG=set(sys.argv[2].split(','))
KNOW={'read_knowledge','read_rag','search_rag','search_knowledge','read_web_page','web_search'}
FILES={'read_file','list_files','read_project_file','search_files'}
cat=collections.Counter(); calls=0; pts=[]; per_tool=collections.Counter(); skills=collections.Counter(); sysp=collections.Counter()
for f in glob.glob(D+'/*/log.json'):
    for s in json.load(open(f))['steps']:
        if s['agent'] not in AG: continue
        for c in s['llm_calls']:
            calls+=1; names={}; tot=0; first=True
            for m in c['messages']:
                ct=m.get('content'); txt=ct if isinstance(ct,str) else json.dumps(ct or '')
                for tc in (m.get('tool_calls') or []):
                    fn=tc.get('function',{}) if isinstance(tc,dict) else {}
                    names[tc.get('id')]=fn.get('name') or tc.get('name')
                    a=fn.get('arguments') or json.dumps(tc.get('input') or tc.get('args') or '')
                    cat['assistant tool-call args']+=len(a); tot+=len(a)
                L=len(txt); tot+=L
                if m['role']=='system':
                    if first: cat['system prompt']+=L; sysp[s['agent']]=max(sysp[s['agent']],L); first=False
                    else: cat['system (state, notes)']+=L
                elif m['role']=='user': cat['user/brief']+=L
                elif m['role']=='assistant': cat['assistant text']+=L
                elif m['role']=='tool':
                    tn=names.get(m.get('tool_call_id'),'?')
                    sk=re.search(r"\[skill [^\]]*\]",txt)
                    if sk:
                        i=sk.start(); sl=len(txt)-i  # skill text to end (approx)
                        nm=sk.group(0); skills[nm]+=sl; cat['skills in tool results']+=sl; L-=sl
                    k='Knowledge (read/search)' if tn in KNOW else 'project files' if tn in FILES else 'tool: '+tn
                    cat[k]+=L; per_tool[tn]+=L
            pts.append((tot,c.get('input_tokens') or 0))
import statistics
# calibrate tokens = a + b*chars
n=len(pts); mx=sum(p[0] for p in pts)/n; my=sum(p[1] for p in pts)/n
b=sum((p[0]-mx)*(p[1]-my) for p in pts)/sum((p[0]-mx)**2 for p in pts); a=my-b*mx
T=sum(p[1] for p in pts)
print(f"{calls} calls, input tokens total {T/1e6:.2f} M, mean {T/calls:.0f}; fit tokens = {a:.0f} + {b:.3f}*chars (fixed part = tool schemas etc.)")
print(f"fixed per call: {a:.0f} tok = {a*calls/T*100:.0f}% of input")
tc=sum(cat.values())
for k,v in sorted(cat.items(),key=lambda kv:-kv[1])[:18]: print(f"{k:34s} {v*b/1e6:6.2f} M tok {100*v*b/T:5.1f}%")
print('system prompt max chars per agent',dict(sysp))
print('skills',[(k,round(v*b/1e3)) for k,v in skills.most_common(8)])
