import json,collections,re,datetime as dt
res=json.load(open('/tmp/sa/res.json')); tools=json.load(open('/tmp/sa/tools.json')); causes=json.load(open('/tmp/sa/causes.json'))
def p(s): return dt.datetime.fromisoformat(s.replace('Z','+00:00')) if s else None
def grp(x):
    t,code,n=x['tool'],x['code'],x['norm']
    if code=='missing_value' or (t=='evaluate_module' and 'no value' in n and 'inlets' not in n): return 'T1'
    if t=='evaluate_module' and ('needs the stream inlets' in n or 'invalid inlet' in n or 'validation error for Fluid' in n or 'Stream.fluid' in n): return 'T2'
    if t in('read_stored','read_result'): return 'T3'
    if t in('calculate','run_python'): return 'T4'
    if t=='patch_plant' and (code=='not_allowed' or code=='invalid_value'): return 'T5'
    if (t=='evaluate_module' and (code in('unknown_name','invalid_call'))) or (t=='patch_plant' and code=='unknown_name'): return 'T6'
    if code=='no_case' or (code=='unknown_name' and t in('read_plant','simulate','read_case')): return 'T7'
    if t in('patch_plant','build_plant','simulate') and code in('invalid_input','unconnected_port','internal','case_incomplete'): return 'T8'
    if t in('set_case','update_state'): return 'T9'
    if code in('nested_stopped',): return 'T10'
    if t=='web_search': return 'T11'
    return 'other'
agg=collections.defaultdict(lambda:{'n':0,'runs':0,'ex':{}})
for x in causes:
    g=agg[grp(x)]; g['n']+=x['n']; g['runs']=max(g['runs'],x['runs'])
    key=(x['tool'],x['code'])
    if key not in g['ex'] or x['n']>g['ex'][key][0]: g['ex'][key]=(x['n'],x['ex'][0],x['ex'][1])
for k,v in sorted(agg.items(),key=lambda kv:-kv[1]['n']):
    print(k,v['n'],v['runs'])
    for kk,e in sorted(v['ex'].items(),key=lambda kv:-kv[1][0])[:3]: print('   ',kk,e[0],'|',e[1][:260].replace('\n',' '),'|',e[2])
