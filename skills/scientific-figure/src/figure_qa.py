import re,xml.etree.ElementTree as ET
from PIL import Image
try:
 import pymupdf
except ImportError:
 pymupdf=None
from .qa_gate_policy import evaluate

def vector_qa(svg,pdf,png,profile,layout,log):
 root=ET.parse(svg).getroot();ids={e.get('id') for e in root.iter() if e.get('id')};invalid=[]
 for e in root.iter():
  for val in e.attrib.values():
   for ref in re.findall(r'url\(#([^)]*)\)',val):
    if ref not in ids:invalid.append(ref)
  href=e.get('{http://www.w3.org/1999/xlink}href','')
  if href.startswith('#') and href[1:] not in ids:invalid.append(href)
 def mm(v):return float(v[:-2])*(25.4/72 if v.endswith('pt') else 1)
 w,h=mm(root.get('width')),mm(root.get('height'));pdfsize=None;images=0;pdf_status='PASS'
 if pymupdf is None:pdf_status='PDF_QA_UNAVAILABLE'
 else:
  pdfdoc=pymupdf.open(pdf);page=pdfdoc[0];pdfsize=[page.rect.width*25.4/72,page.rect.height*25.4/72];images=len(page.get_images());pdfdoc.close()
 image=Image.open(png);missing=layout.get('render_diagnostics',{}).get('missing_glyph_messages',[v for v in layout['warnings'] if 'Glyph' in v and 'missing' in v]);raster=sum(e.tag.endswith('}image') for e in root.iter())
 physical=abs(w-profile['target_width_mm'])<=.1 and (pdf_status=='PASS' and abs(pdfsize[0]-w)<=.1) and abs(image.width-w/25.4*300)<=1
 boxes=layout['panel_boxes'];aligned=all(abs(a[2]-b[2])<1e-6 and abs(a[3]-b[3])<1e-6 for a in boxes for b in boxes)
 noncolor={}
 for record in layout.get('encoding_records',[]):noncolor.setdefault((record['marker'],record['linestyle'],record['fill_state']),set()).add(record['identity'])
 color_only=any(len(v)>1 for v in noncolor.values())
 checks={'physical_size':'PASS' if physical else 'FAIL','raster_embedding':'PASS' if raster+images==0 else 'FAIL','clip_validity':'PASS' if not invalid else 'FAIL','scientific_DOM':'PASS' if log['scientific_primitive_hashes_identical'] else 'FAIL','missing_glyph':'PASS' if not missing else 'FAIL','artwork_edge':'WARN' if layout['overflow_text'] else 'PASS','legend_overlap':'PASS' if all(x['external_verified'] for x in layout['legends']) else 'WARN','marker_overlap':'WARN' if any(x['near_count'] for x in layout['marker_overlap']) else 'PASS','dense_marker_misuse':'PASS' if layout.get('archetype')!='DENSE_TIMESERIES' or all(p['marker_pt']==0 for p in layout['parameters']) else 'FAIL','annotation_collision':'WARN' if layout.get('annotation_collisions',[]) else 'PASS','panel_alignment':'PASS' if aligned else 'WARN','excessive_outer_whitespace':'WARN' if layout['outer_whitespace_fraction']>.25 else 'PASS','encoding_uniqueness':'PASS' if layout.get('encoding_unique') and not layout.get('encoding_collisions') else 'FAIL','color_only_encoding':'WARN' if color_only else 'PASS'}
 checks['annotation_placement']='WARN' if any(not p['safe'] for p in layout.get('annotation_placement',[])) else 'PASS'
 checks['legend_label_overlap']='WARN' if layout.get('legend_label_collisions') else 'PASS'
 checks['legend_overflow']='WARN' if any(b['bbox_pt'][0]<0 or b['bbox_pt'][2]>w/25.4*72 for b in layout['legends']) else 'PASS'
 # WARN does not mean measured layout clearance. Technical vector gate uses structural validity.
 policy=evaluate(checks)
 return {'status':'FAIL' if policy['block'] or pdf_status!='PASS' else 'PASS','gate_policy':policy,'checks':checks,'width_mm':w,'height_mm':h,'viewBox':root.get('viewBox'),'pdf_size_mm':pdfsize,'pdf_qa_status':pdf_status,'png_dimensions':image.size,'font_policy':'role-based portable fallback chains; glyph warnings captured','overflow_text':layout['overflow_text'],'missing_glyph_warnings':missing,'invalid_clip_ids':invalid,'minimum_configured_stroke_pt':.65,'outer_whitespace_fraction':layout['outer_whitespace_fraction'],'annotation_collision_pairs':layout.get('annotation_collisions',[]),'panel_boxes':boxes,'limitation':'Layout clearance warnings are separate from structural vector validity; no aesthetic judgement.'}
