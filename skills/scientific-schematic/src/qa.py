from pathlib import Path
import xml.etree.ElementTree as E,re,math
try:
 import pymupdf
except ImportError:
 pymupdf=None

def structure_attestation(before,after):
 attrs=['value','source','target','parent','vertex','edge']
 return all(k in after and all((v.get(a) or '')==(after[k].get(a) or '') for a in attrs) for k,v in before.items())

def audit(s,out,before,after):
 if pymupdf is None:raise ValueError('PDF_QA_UNAVAILABLE: schematic QA requires PDF inspection')
 d=pymupdf.open(out/'figure.pdf');p=d[0];root=E.parse(out/'figure.svg').getroot();vb=[float(x) for x in root.get('viewBox').split()];scale=vb[2]/p.rect.width;ss=[q for b in p.get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] for q in l['spans']];texts=''.join(''.join(q['text'].split()) for q in ss);missing=[c.get('value') for c in before.values() if c.get('value') and ''.join(c.get('value').split()) not in texts]
 outside=[q['text'] for q in ss if not p.rect.contains(pymupdf.Rect(q['bbox']))];overlap=[]
 for i,a in enumerate(ss):
  for b in ss[i+1:]:
   r=pymupdf.Rect(a['bbox'])&pymupdf.Rect(b['bbox'])
   if r.width>1 and r.height>1:overlap.append([a['text'],b['text']])
 groups={g.get('data-cell-id'):g for g in root.iter() if g.get('data-cell-id')};segs=[];tips=[]
 for edge in s['edges']:
  for x in groups.get(edge['id'],E.Element('g')).iter():
   if not x.tag.endswith('path'):continue
   v=[float(a) for a in re.findall(r'-?\d+(?:\.\d+)?',x.get('d',''))];pts=list(zip(v[::2],v[1::2]))
   if x.get('fill')=='none':segs.extend((edge['id'],a,b) for a,b in zip(pts,pts[1:]))
   elif pts:tips.append((edge,pts[0]))
 def ori(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 crossings=[(e,f) for i,(e,a,b) in enumerate(segs) for f,c,dd in segs[i+1:] if e!=f and ori(a,b,c)*ori(a,b,dd)<-1e-8 and ori(c,dd,a)*ori(c,dd,b)<-1e-8]
 factor=s['canvas']['width_mm']/25.4*96/s['canvas']['width'];arrowhits=[]
 for e,(x,y) in tips:
  for n in s['nodes']:
   if n['id'] in [e['source'],e['target']] or n['type']=='container':continue
   nx,ny=n['layout']['preferred_position'];nw,nh=n['layout']['size']
   if nx*factor+1<x<(nx+nw)*factor-1 and ny*factor+1<y<(ny+nh)*factor-1:arrowhits.append([e['id'],n['id']])
 preserve=structure_attestation(before,after)
 result={'semantic_nodes':len(s['nodes']),'workflow_edges':len(s['edges']),'node_edge_label_group_preservation':preserve,'application_open_save_reopen':preserve,'text_collision':overlap,'connector_crossing':crossings,'arrow_block_collision':arrowhits,'text_outside_canvas':outside,'missing_text':missing,'missing_glyph':sum(q['text'].count('\ufffd')+q['text'].count('\x00') for q in ss),'foreignObject':sum(x.tag.endswith('foreignObject') for x in root.iter()),'raster_embedding':len(p.get_images())+sum(x.tag.endswith('image') for x in root.iter()),'width_mm':p.rect.width/72*25.4,'native_connector_relationships':all(after[e['id']].get('source')==e['source'] and after[e['id']].get('target')==e['target'] for e in s['edges']),'connector_follow':None,'group_preservation':all(k in after and after[k].get('parent')==v.get('parent') for k,v in before.items())}
 result['technical_status']='PASS' if result['application_open_save_reopen'] and preserve and not missing and not result['missing_glyph'] and not result['foreignObject'] and not result['raster_embedding'] and abs(result['width_mm']-s['canvas']['width_mm'])<.1 else 'FAIL';result['production_clearance']='PASS' if result['technical_status']=='PASS' and not any([overlap,crossings,arrowhits,outside]) else 'REVIEW_REQUIRED';return result
