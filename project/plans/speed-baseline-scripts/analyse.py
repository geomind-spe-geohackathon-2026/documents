import json,glob,collections,re,os
D="/tmp/sa/data/"
runs={x['id'].replace('-',''):x for x in json.load(open(D+'runs.json'))}
CASE={'case_lead','geoscientist'}
PLANT={'design_lead','process_engineer','well_engineer','reservoir_engineer','energy_systems_engineer','integration_engineer','family_design_lead'}
SIZING={'size_plant','set_ranges','optimize'}
SIM={'simulate','check_results'}
DELEG={'case_lead','geoscientist','geoscientists','design_lead','energy_systems_engineer','process_engineer','well_engineer','reservoir_engineer','integration_engineer','economist','analysis_lead','reviewer','explainer','support_lead','curator','family_design_lead','comparison_driver'}
def stage(s):
    tools={t['tool'] for t in s['tool_calls']}
    a=s['agent']
    if a in CASE: return 'case'
    if tools&SIM and a in PLANT|{'analysis_lead'}: return 'simulate'
    if tools&SIZING: return 'sizing'
    if a in PLANT: return 'plant'
    return 'other'
def norm(m):
    m=re.sub(r"result-[0-9a-f]+","result-ID",m)
    m=re.sub(r"[0-9a-f]{8}-[0-9a-f-]{27}","UUID",m)
    m=re.sub(r"'[^']{0,60}'","'X'",m)
    m=re.sub(r"\b\d+(\.\d+)?\b","N",m)
    return m[:170]
res={}; tool_stat=collections.defaultdict(lambda:[0,0,0,0]) # calls, err, firsttry calls, firsttry err
causes=collections.defaultdict(lambda:{'n':0,'runs':set(),'ex':None,'tool':None,'code':None})
repeats=collections.Counter(); rereads=collections.Counter(); repflag=collections.Counter()
for f in sorted(glob.glob(D+'*/log.json')):
    rid=f.split('/')[-2].replace('-','')
    run=runs.get(rid) or runs.get(f.split('/')[-2])
    d=json.load(open(f))
    try: ag=json.load(open(f.replace('log','agents')))['agents']
    except Exception: ag=[]
    st=collections.defaultdict(lambda:{'steps':0,'llm':0,'tools':0,'err':0,'t':0.0,'cards_q':0,'cards_a':0,'wait':0.0,'deleg':0})
    last={}
    seen=collections.Counter()
    for s in d['steps']:
        g=st[stage(s)]; g['steps']+=1
        for l in s['llm_calls']: g['llm']+=1; g['t']+=l.get('duration') or 0
        for t in s['tool_calls']:
            g['tools']+=1
            if t['tool'] in DELEG: g['deleg']=g.get('deleg',0)+1
            elif t['tool'] in ('ask_user','ask_economics'): g['wait']=g.get('wait',0)+(t.get('duration') or 0)
            else: g['t']+=t.get('duration') or 0
            o=t['output']; err=isinstance(o,dict) and isinstance(o.get('error'),dict)
            if t['tool']=='ask_user':
                opts=json.dumps(t['input'].get('options',''))
                if 'approve' in opts.lower(): g['cards_a']+=1
                else: g['cards_q']+=1
            if t['tool']=='ask_economics': g['cards_a']+=1
            key=(s['agent'],t['tool'])
            first=not last.get(key,False)
            ts=tool_stat[t['tool']]; ts[0]+=1
            if first: ts[2]+=1
            if err:
                g['err']+=1; ts[1]+=1
                if first: ts[3]+=1
                e=o['error']; c=causes[(t['tool'],e.get('code'),norm(str(e.get('message',''))))]
                c['n']+=1; c['runs'].add(rid); c['tool']=t['tool']; c['code']=e.get('code')
                if c['ex'] is None: c['ex']=(str(e.get('message'))[:400],s['agent'])
                if 'repeated' in o: repflag[(t['tool'],e.get('code'))]+=1
            last[key]=err
            inp=json.dumps(t['input'],sort_keys=True)[:300]
            seen[(s['agent'],t['tool'],inp)]+=1
    for (a,tn,i),n in seen.items():
        if n>1 and tn in('read_stored','read_case','read_plant','describe_module','read_result','read_profile','read_rag','search_rag','list_plants','describe_case','read_skill'): rereads[tn]+=n-1
        elif n>1 and tn not in('finish',): repeats[tn]+=n-1
    inst=sorted({x['instance'] for x in ag if x.get('instance')})
    res[rid]=dict(run=run,stages={k:dict(v) for k,v in st.items()},inst=inst,
        nag=len(ag), runinfo=d['run'])
json.dump(res,open('/tmp/sa/res.json','w'),default=str)
json.dump({'tool_stat':tool_stat,'repeats':repeats,'rereads':rereads,'repflag':{str(k):v for k,v in repflag.items()}},open('/tmp/sa/tools.json','w'))
cl=sorted(causes.items(),key=lambda kv:-kv[1]['n'])
json.dump([dict(tool=k[0],code=k[1],norm=k[2],n=v['n'],runs=len(v['runs']),runids=sorted(v['runs']),ex=v['ex']) for k,v in cl],open('/tmp/sa/causes.json','w'),indent=1)
print(len(res),'runs;',len(cl),'cause clusters')
