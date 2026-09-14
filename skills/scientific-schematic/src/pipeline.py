"""Renderer-neutral native schematic RC pipeline. No automatic topology synthesis."""
from pathlib import Path
import json,copy,hashlib,os,subprocess,xml.etree.ElementTree as ET,re,math
import yaml,jsonschema
from .native_backend import native
from .normalizer import normalize
from .portability import discover_drawio, configure_cairosvg
ROOT=Path(__file__).resolve().parents[1]
GRAMMARS={g['name'] for g in yaml.safe_load((ROOT/'config/grammar_registry.yaml').read_text(encoding='utf8'))['grammars']}
PRIMITIVES={'waveform','matrix','graph','model','probability','equation','dataset','artifact'}
ALIASES={'small_graph':'graph','network':'graph','model_artifact':'artifact','residual':'waveform','feature_vector':'matrix'}
def validate(s):
 if s.get('grammar') not in GRAMMARS:raise ValueError('UNKNOWN_GRAMMAR_FAIL_CLOSED')
 jsonschema.validate(s,json.loads((ROOT/'schema/diagram_semantic_spec.schema.json').read_text(encoding='utf8')))
 ids=[n['id'] for n in s['nodes']];edges=[e['id'] for e in s['edges']]
 if len(set(ids+edges))!=len(ids+edges):raise ValueError('DUPLICATE_ID')
 for n in s['nodes']:
  if n.get('primitive'):
   primitive=ALIASES.get(n['primitive'],n['primitive'])
   if primitive not in PRIMITIVES:raise ValueError('UNSUPPORTED_PRIMITIVE_FAIL_CLOSED')
   if n.get('representation_class') not in ['ICONIC_NON_DATA','SCIENTIFIC_DATA']:raise ValueError('PRIMITIVE_REPRESENTATION_CLASS_REQUIRED')
   if primitive=='equation':
    if n.get('representation_class')!='SCIENTIFIC_DATA':raise ValueError('EQUATION_MUST_BE_SCIENTIFIC_DATA')
    text=n.get('scientific_content',{}).get('equation_text')
    if not isinstance(text,str) or not text.strip():raise ValueError('EQUATION_TEXT_REQUIRED_FAIL_CLOSED')
   elif n.get('representation_class')!='ICONIC_NON_DATA':raise ValueError('ICONIC_NON_DATA_REQUIRED')
  group=n['layout'].get('group')
  if group and group not in ids:raise ValueError('MISSING_GROUP')
  seen={n['id']}
  while group:
   if group in seen:raise ValueError('GROUP_CYCLE')
   seen.add(group);group=next(x for x in s['nodes'] if x['id']==group)['layout'].get('group')
 for e in s['edges']:
  if e['source'] not in ids or e['target'] not in ids:raise ValueError('DANGLING_EDGE')
  if e.get('label_anchor','middle') not in ['source','middle','target']:raise ValueError('INVALID_LABEL_ANCHOR')
  if not 0<=e.get('label_fraction',.5)<=1:raise ValueError('INVALID_LABEL_FRACTION')
 return s['grammar']
def read(p):return ET.ElementTree(ET.fromstring(Path(p).read_text(encoding='utf-8-sig')))
def cellmap(t):return {c.get('id'):c for c in t.iter('mxCell')}
def style(c,k,v):c.set('style',';'.join([s for s in c.get('style','').split(';') if s and not s.startswith(k+'=')]+[f'{k}={v}'])+';')
def build(s,out,profile=None):
 validate(s);profile=profile or {};d=copy.deepcopy(s);w=profile.get('target_width_mm',d['canvas'].get('width_mm',145))
 if w==90 and not (profile.get('single_column_authority') and d['grammar'] in ['ALGORITHM_DECISION_LOOP','STAGED_METHOD_PIPELINE']):raise ValueError('NOT_RECOMMENDED_AT_90MM')
 if w not in [90,145]:raise ValueError('WIDTH_PROFILE_REVIEW_REQUIRED')
 d['canvas']['width_mm']=w
 family=profile.get('style','JOURNAL_MINIMAL')
 if family not in ['JOURNAL_MINIMAL','JOURNAL_FUNCTIONAL_COLOR']:raise ValueError('UNKNOWN_STYLE')
 for n in d['nodes']:
  if n.get('primitive'):n['primitive']=ALIASES.get(n['primitive'],n['primitive'])
 native(d,out);t=read(out);cs=cellmap(t)
 if len(cs)!=len(list(t.iter('mxCell'))):raise ValueError('GENERATED_CELL_ID_COLLISION')
 for c in cs.values():
  if c.get('value'):
   style(c,'convertToSvg',1)
   if 'whiteSpace=wrap' in c.get('style',''):style(c,'svgWhiteSpace','wrap')
 for n in d['nodes']:
  if family=='JOURNAL_FUNCTIONAL_COLOR' and not n.get('primitive') and n['type'] not in ['container','junction'] and n.get('shape')!='text':style(cs[n['id']],'fillColor',{'model':'#E6EFF5','physical_object':'#EBF1E8','action':'#F2EAF0'}.get(n['type'],'#F4F4F4'))
 for e in d['edges']:
  if not e['label'] or e['id']+'_label' not in cs:continue
  if 'label_fraction' not in e and 'label_anchor' not in e:continue
  f=e.get('label_fraction',{'source':0,'middle':.5,'target':1}[e.get('label_anchor','middle')]);g=cs[e['id']+'_label'].find('mxGeometry');g.set('x',str(2*f-1));g.set('y',str(e.get('label_normal_offset',10)));g.set('relative','1');offset=g.find('mxPoint')
  if offset is None:offset=ET.SubElement(g,'mxPoint',attrib={'as':'offset'})
  # Last explicit route segment is insufficient: find the segment containing arclength f.
  from .native_backend import route
  pts=route(e,{n['id']:n for n in d['nodes']});lens=[math.dist(a,b) for a,b in zip(pts,pts[1:])];target=f*sum(lens);cum=0;unit=(1,0)
  for a,b,l in zip(pts,pts[1:],lens):
   if l and cum+l>=target:unit=((b[0]-a[0])/l,(b[1]-a[1])/l);break
   cum+=l
  tangent=e.get('label_tangent_offset',0);offset.set('x',str(tangent*unit[0]));offset.set('y',str(tangent*unit[1]))
 t.write(out,encoding='utf-8',xml_declaration=True);return d

def run(s,out,profile=None):
 validate(s);out=Path(out)
 if out.exists() and any(out.iterdir()):raise ValueError('NONEMPTY_OUTPUT')
 out.mkdir(parents=True,exist_ok=True);profile=profile or {};p=out/'diagram.drawio';d=build(s,p,profile);env=os.environ.copy();work=out/'work';work.mkdir();logs=[];gate_log=[]
 for k,sub in [('APPDATA','profile'),('LOCALAPPDATA','local'),('TEMP','tmp'),('TMP','tmp')]:q=work/sub;q.mkdir(exist_ok=True);env[k]=str(q)
 discovery=discover_drawio(profile); (out/'DRAWIO_DISCOVERY.json').write_text(json.dumps(discovery,indent=2),encoding='utf-8')
 if not discovery['available']:
  if profile.get('require_application_export') or os.environ.get('SCHEMATIC_REQUIRE_DRAWIO')=='1': raise RuntimeError('DRAWIO_APPLICATION_EXPORT_UNAVAILABLE')
  result={'native_document':str(p),'application_export':'UNAVAILABLE','application_export_capability':'UNAVAILABLE','native_xml_generation':'PASS','semantic_nodes':len(d['nodes']),'workflow_edges':len(d['edges']),'node_edge_label_group_preservation':None,'application_open_save_reopen':'NOT_CHECKED','connector_follow':None,'group_preservation':None,'preservation_status':'NOT_CHECKED','technical_status':'NATIVE_XML_PASS','production_clearance':'REVIEW_REQUIRED','foreignObject':None,'raster_embedding':None,'missing_glyph':None,'width_mm':None,'native_only':True,'application_status':'NOT_CHECKED'}
  (out/'QA.json').write_text(json.dumps(result,indent=2),encoding='utf-8');(out/'RESULT.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
  return result
 exe=discovery['path']
 def app(src,dest,fmt):
  cmd=[exe,'--disable-update','--disable-gpu','--no-sandbox','--user-data-dir='+str(work/'drawio-user'),'--export','--format',fmt,'--output',str(dest)]+(['--uncompressed'] if fmt=='xml' else ['--theme','light','--size','page','--embed-svg-fonts','false'])+[str(src)];r=subprocess.run(cmd,env=env,capture_output=True,timeout=50,creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0);logs.append({'cmd':cmd,'exit':r.returncode,'stderr':r.stderr.decode(errors='replace')})
  if r.returncode or not dest.exists():raise RuntimeError('DRAWIO_EXPORT_FAIL')
 from .publication_gate import publication_svg_fail_closed
 try:
  cairosvg,runtime_info=configure_cairosvg(profile)
 except ValueError as exc:
  runtime_info={'available':False,'error':str(exc),'publication_export':'UNAVAILABLE'};(out/'CAIROSVG_RUNTIME.json').write_text(json.dumps(runtime_info,indent=2),encoding='utf-8')
  app(p,out/'saved.xml','xml');app(out/'saved.xml',out/'reopened.xml','xml');p.write_bytes((out/'reopened.xml').read_bytes());app(p,out/'application.svg','svg')
  result={'native_document':str(p),'application_export':'SVG_ONLY','publication_export':'UNAVAILABLE','publication_export_error':str(exc),'native_xml_generation':'PASS','semantic_nodes':len(d['nodes']),'workflow_edges':len(d['edges']),'node_edge_label_group_preservation':None,'application_open_save_reopen':'NOT_CHECKED','connector_follow':None,'group_preservation':None,'preservation_status':'NOT_CHECKED','technical_status':'NATIVE_XML_PASS','production_clearance':'REVIEW_REQUIRED','foreignObject':None,'raster_embedding':None,'missing_glyph':None,'width_mm':None,'native_only':False,'application_status':'NOT_CHECKED'}
  (out/'QA.json').write_text(json.dumps(result,indent=2),encoding='utf-8');(out/'RESULT.json').write_text(json.dumps(result,indent=2),encoding='utf-8');return result
 (out/'CAIROSVG_RUNTIME.json').write_text(json.dumps(runtime_info,indent=2),encoding='utf-8')
 expected=[c.get('value') for c in cellmap(read(p)).values() if c.get('value')]
 def export_chain(label):
  nonlocal p
  before=cellmap(read(p));app(p,out/'saved.xml','xml');app(out/'saved.xml',out/'reopened.xml','xml');after=cellmap(read(out/'reopened.xml'));p.write_bytes((out/'reopened.xml').read_bytes());app(p,out/'application.svg','svg')
  try:
   gate_log.append(publication_svg_fail_closed(out/'application.svg',None,expected,'application_'+label,exact=False))
   norm=normalize(out/'application.svg',out/'figure.svg',d['canvas']['width_mm']);gate_log.append(publication_svg_fail_closed(out/'figure.svg',d['canvas']['width_mm'],expected,'normalized_'+label,exact=True))
   cairosvg.svg2pdf(url=str(out/'figure.svg'),write_to=str(out/'figure.pdf'),background_color='white');cairosvg.svg2png(url=str(out/'figure.svg'),write_to=str(out/'figure.png'),dpi=300,background_color='white')
   gate_log.append(publication_svg_fail_closed(out/'figure.svg',d['canvas']['width_mm'],expected,'final_'+label,pdf=out/'figure.pdf',exact=True))
  except Exception:
   for q in ['figure.svg','figure.pdf','figure.png']:
    (out/q).unlink(missing_ok=True)
   raise
  return before,after,norm
 before,after,log=export_chain('initial')
 from .clearance import plan
 adjusted,clearance_log=plan(d,out)
 if adjusted:
  p.unlink();build(d,p,profile);before,after,log=export_chain('clearance')
 (out/'EDGE_LABEL_CLEARANCE_LOG.json').write_text(json.dumps(clearance_log,indent=2),encoding='utf-8')
 from .qa import audit
 qa=audit(d,out,before,after);qa['publication_gate']=gate_log;(out/'QA.json').write_text(json.dumps(qa,indent=2),encoding='utf8');(out/'NORMALIZER_LOG.json').write_text(json.dumps(log,indent=2),encoding='utf8');(out/'APPLICATION_LOG.json').write_text(json.dumps(logs,indent=2),encoding='utf8');return qa
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--spec',required=True);p.add_argument('--out',required=True);p.add_argument('--profile');a=p.parse_args();print(json.dumps(run(json.loads(Path(a.spec).read_text(encoding='utf8')),a.out,json.loads(Path(a.profile).read_text(encoding="utf-8")) if a.profile else {}),indent=2))
