import os,sys,json,time,traceback
from pathlib import Path
from .archetype_selector import select,complexity_reason
from .production_policy import clearance,width_status
from .semantic_spec import validate,manifest,digest,resolve_source_paths

def converter(profile=None):
 from .runtime import configure_cairosvg
 return configure_cairosvg(profile)[0]

def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf8')
def run(spec,profile,out):
 start=time.perf_counter();out=Path(out)
 if out.exists() and any(out.iterdir()):raise ValueError('Refuse overwrite of nonempty output directory')
 out.mkdir(parents=True,exist_ok=True);profile=profile or {};spec=resolve_source_paths(spec,profile.get('source_root'));archetype=select(spec)
 optimization={'python_optimization_level':sys.flags.optimize,'__debug__':__debug__}
 result={'optimization':optimization,'SUPPORTED_ARCHETYPE':archetype is not None,'archetype':archetype,'render':'NOT_RUN','scientific':'NOT_RUN','vector':'NOT_RUN','manual_UI_interactions':0,'manual_parameter_edits_before_first_pass':0,'failure_retry_count':0}
 if archetype is None:
  result.update(status='UNSUPPORTED',reason=complexity_reason(spec) or 'UNSUPPORTED_ARCHETYPE',TECHNICAL_STATUS='NOT_RUN',PRODUCTION_CLEARANCE='UNSUPPORTED',fail_closed=True,runtime_s=time.perf_counter()-start);dump(out/'RESULT.json',result);return result
 try:
  validate(spec);before=manifest(spec);result['scientific']='PASS'
  for key in ['target_width_mm','target_language','output_context','panel_mode']:
   if key not in profile:raise ValueError('Missing authoritative profile input: '+key)
  if not 50<=profile['target_width_mm']<=400:raise ValueError('Target width outside candidate scope')
  from .render_matplotlib import render
  from .publication_vector_polisher import polish
  from .figure_qa import vector_qa
  from .color_qa import previews
  work=out/'work';work.mkdir();layout=render(spec,profile,work,archetype);validate(spec);after=manifest(spec)
  invariant=before==after and all(q['identical'] for q in layout['checks'])
  dump(out/'SCIENTIFIC_INVARIANCE.json',{'before':before,'after':after,'artist_readback_checks':layout['checks'],'ALL_SCIENTIFIC_VALUES_IDENTICAL':invariant,**optimization})
  if not invariant:result['scientific']='FAIL';raise ValueError('Scientific invariant failed; final export forbidden')
  diagnostics=layout['render_diagnostics'];result['glyph_preflight']=diagnostics['glyph_preflight']['status'];result['renderer_diagnostics']=diagnostics['status'];result['missing_glyph_count']=diagnostics['missing_glyph_count']
  if diagnostics['status']=='FAIL' or diagnostics['glyph_preflight']['status']!='PASS':
   result['vector']='FAIL';raise ValueError('GLYPH_PREFLIGHT_OR_RENDER_DIAGNOSTICS_FAIL: no final PDF/PNG export')
  log=polish(work/'draft.svg',out/'figure.svg',layout);dump(out/'VECTOR_TRANSFORM_LOG.json',log);dump(out/'RENDER_LAYOUT.json',layout)
  try:
   cv=converter(profile);cv.svg2pdf(url=str(out/'figure.svg'),write_to=str(out/'figure.pdf'));cv.svg2png(url=str(out/'figure.svg'),write_to=str(out/'figure.png'),dpi=300)
  except ValueError as ex:
   # SVG is the core renderer output.  Keep it only as an explicitly named
   # diagnostic artifact when the optional publication converter is absent.
   diag=out/'figure.DIAGNOSTIC.svg';(out/'figure.svg').replace(diag)
   result.update(render='PASS',vector='PASS',core_status='PASS',publication_export='UNAVAILABLE',publication_export_error=str(ex),status='PUBLICATION_EXPORT_UNAVAILABLE')
   result['FIRST_PASS_TECHNICAL_SUCCESS']=False;result['TECHNICAL_STATUS']='FAIL';result['PRODUCTION_CLEARANCE']='REVIEW_REQUIRED'
   (out/'PUBLICATION_EXPORT.json').write_text(json.dumps({'status':'PUBLICATION_EXPORT_UNAVAILABLE','error':str(ex),'svg_core':'PASS'},indent=2),encoding='utf8')
   result['runtime_s']=time.perf_counter()-start;dump(out/'RESULT.json',result);return result
  from PIL import Image
  im=Image.open(out/'figure.png');im.save(out/'figure.png',dpi=(300,300));qa=vector_qa(out/'figure.svg',out/'figure.pdf',out/'figure.png',profile,layout,log);dump(out/'QA.json',qa);dump(out/'COLOR_QA.json',previews(out/'figure.png',out));(out/'CAPTION.txt').write_text(spec['caption_information']+'\n\n'+json.dumps([{'panel':p['panel_id'],'references':p.get('references',[]),'events':p.get('events',[]),'invalid_regions':p.get('invalid_regions',[])} for p in spec['panels']],ensure_ascii=False,indent=2),encoding='utf8')
  result.update(render='PASS',vector=qa['status'],physical_size=qa['checks']['physical_size'],vector_polish=log['status'],warnings={k:v for k,v in qa['checks'].items() if v!='PASS'},generated=['SVG','PDF','PNG'])
 except Exception as ex:
  result.update(status='FAILED',error=str(ex),failure_retry_count=1)
  if 'FAIL_CLOSED_FONT_ENVIRONMENT' in str(ex):result.update(vector='FAIL',glyph_preflight='FAIL',renderer_diagnostics='FAIL')
  if 'SOURCE_SHA_MISMATCH' in str(ex) or 'Scientific invariant' in str(ex):result['scientific']='FAIL'
  if result['render']=='NOT_RUN' and result['scientific']=='NOT_RUN':result['scientific']='FAIL'
  (out/'ERROR.txt').write_text(traceback.format_exc(),encoding='utf8')
  if not (out/'SCIENTIFIC_INVARIANCE.json').exists():dump(out/'SCIENTIFIC_INVARIANCE.json',{'validation':'REJECTED',**optimization})
 result['FIRST_PASS_TECHNICAL_SUCCESS']=result['scientific']=='PASS' and result['render']=='PASS' and result['vector']=='PASS' and result['manual_parameter_edits_before_first_pass']==0
 result['TECHNICAL_STATUS']='PASS' if result['FIRST_PASS_TECHNICAL_SUCCESS'] and result.get('physical_size')=='PASS' else 'FAIL'
 result['PRODUCTION_CLEARANCE']=clearance(result,locals().get('qa',{}),profile)
 result['WIDTH_STATUS']=width_status(profile)
 dump(out/'PRODUCTION_CLEARANCE.json',{'TECHNICAL_STATUS':result['TECHNICAL_STATUS'],'PRODUCTION_CLEARANCE':result['PRODUCTION_CLEARANCE'],'width_status':result['WIDTH_STATUS'],'automatic_formal_replacement':False})
 result['runtime_s']=time.perf_counter()-start;result.setdefault('status','COMPLETED');dump(out/'RESULT.json',result);return result
if __name__=='__main__':
 import argparse
 a=argparse.ArgumentParser();a.add_argument('--spec',required=True);a.add_argument('--profile',required=True);a.add_argument('--out',required=True);q=a.parse_args();print(json.dumps(run(json.loads(Path(q.spec).read_text(encoding='utf8')),json.loads(Path(q.profile).read_text(encoding='utf8')),q.out)))
