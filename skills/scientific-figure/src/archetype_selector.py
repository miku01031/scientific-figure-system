SUPPORTED=('DISCRETE_COMPARISON','DENSE_TIMESERIES','ERRORBAR_POINTWHISKER')
def complexity_reason(s):
 for p in s.get('panels',[]):
  if len(p.get('series',[]))>8 and p.get('domain') in ['discrete','time','categorical']:
   return 'ENCODING_CAPACITY_EXCEEDED'
  if p.get('domain')=='discrete' and len(p.get('visual_factors',[]))>1:
   return 'COMPLEX_FACTORIAL_DISCRETE_REQUIRES_DEDICATED_RECIPE'
 return None

def select(s):
 if complexity_reason(s):return None
 ps=s.get('panels',[])
 if not ps:return None
 ds={p.get('domain') for p in ps};ss=[q for p in ps for q in p.get('series',[])]
 if not ss:return None
 if ds=={'discrete'} and all(1<=len(q.get('x',[]))<=8 and 'interval_axis' not in q for q in ss) and all(len(p['series'])<=8 for p in ps):return SUPPORTED[0]
 if ds=={'time'} and all(len(q.get('x',[]))>=32 and q.get('connect') and 'interval_axis' not in q for q in ss):return SUPPORTED[1]
 if ds<= {'categorical','discrete'} and all('interval_axis' in q for q in ss):return SUPPORTED[2]
 return None
