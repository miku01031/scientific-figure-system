"""Neutral semantics validation; no renderer imports."""
import json,hashlib,math,copy
from pathlib import Path
import numpy as np
import jsonschema
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(',',':')).encode()).hexdigest()
def array_hash(x):return hashlib.sha256(np.asarray(x,dtype='<f8').tobytes()).hexdigest()
def resolve_source_paths(s,base_dir=None):
 """Resolve example-relative provenance paths without requiring user paths."""
 if not base_dir:return s
 base=Path(base_dir).expanduser().resolve()
 if not base.is_dir():raise ValueError('SOURCE_ROOT_INVALID: '+str(base))
 out=copy.deepcopy(s)
 for q in out.get('sources',[]):
  p=Path(q['path']);q['path']=str((base/p).resolve()) if not p.is_absolute() else str(p.resolve())
 for p in out.get('panels',[]):
  for q in p.get('series',[]):
   d=q.get('display_label_source')
   if d and not Path(d['path']).is_absolute():d['path']=str((base/Path(d['path'])).resolve())
 return out
def require(condition,message):
 if not condition:raise ValueError(message)
def validate(s,check_sources=True):
 jsonschema.Draft202012Validator(json.loads((ROOT/'schema/figure_semantic_spec.schema.json').read_text(encoding="utf-8"))).validate(s)
 digest(s)
 if check_sources:
  for q in s['sources']:
   if sha(q['path'])!=q['sha256']:raise ValueError('SOURCE_SHA_MISMATCH: '+q['path'])
 require(len({p['panel_id'] for p in s['panels']})==len(s['panels']),'DUPLICATE_PANEL_ID')
 for p in s['panels']:
  ids={q['series_id']:q for q in p['series']};require(len(ids)==len(p['series']),'DUPLICATE_SERIES_ID')
  for a in ['x_axis','y_axis']:
   lo,hi=p[a]['range'];require(math.isfinite(lo) and math.isfinite(hi) and lo<hi,'INVALID_AXIS_RANGE')
   if 'tick_labels' in p[a]:require(len(p[a]['ticks'])==len(p[a]['tick_labels']),'TICK_LABEL_LENGTH_MISMATCH')
  for q in p['series']:
   if 'display_label' in q:
    require('display_label_source' in q,'display_label provenance required')
    ds=q['display_label_source']
    if check_sources:require(sha(ds['path'])==ds['sha256'],'DISPLAY_LABEL_SOURCE_SHA_MISMATCH')
   require(len(q['x'])==len(q['y']),'XY_LENGTH_MISMATCH')
   for a in ['x','y','lower','upper']:
    if a in q:require(all(math.isfinite(v) for v in q[a]),'NONFINITE_SCIENTIFIC_VALUE')
   if 'valid' in q:require(len(q['valid'])==len(q['x']),'VALID_MASK_LENGTH_MISMATCH')
   interval_keys={'lower','upper','interval_axis','interval_definition'} & q.keys()
   if interval_keys:
    require(len(interval_keys)==4,'INCOMPLETE_INTERVAL')
    require(len(q['lower'])==len(q['upper'])==len(q['x']),'INTERVAL_LENGTH_MISMATCH')
    require(all(lo<=v<=hi for lo,v,hi in zip(q['lower'],q[q['interval_axis']],q['upper'])),'INVALID_INTERVAL_ENDPOINTS')
  for a in p.get('annotations',[]):require(a['series_id'] in ids and 0<=a['point_index']<len(ids[a['series_id']]['x']),'INVALID_ANNOTATION_REFERENCE')
  for r in p.get('references',[])+p.get('events',[]):
   if 'series_id' in r:require(r['series_id'] in ids,'INVALID_REFERENCE_SERIES')
  for r in p.get('invalid_regions',[]):require(r['start']<r['end'],'INVALID_REGION_ORDER')
 return s

def manifest(s):
 return {'semantic_sha256':digest(s),'sources':s['sources'],'panels':[{ 'panel_id':p['panel_id'],'axes':{a:p[a] for a in ['x_axis','y_axis']},'series':[{ 'series_id':q['series_id'],'point_count':len(q['x']),'hashes':{a:array_hash(q[a]) for a in ['x','y','lower','upper'] if a in q},'valid_mask_sha256':digest(q.get('valid',[])),'interval_definition':q.get('interval_definition')} for q in p['series']],'reference_event_hash':digest([p.get('references',[]),p.get('events',[]),p.get('invalid_regions',[])])} for p in s['panels']]}
