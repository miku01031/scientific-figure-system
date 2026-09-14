"""Fail-closed publication checks shared by every export stage."""
from pathlib import Path
import re,xml.etree.ElementTree as ET
try:
 import pymupdf
except ImportError:
 pymupdf=None

def _length_mm(value):
 m=re.fullmatch(r'\s*([0-9.+-eE]+)\s*(mm|px|pt)?\s*',value or '')
 if not m:raise ValueError('INVALID_SVG_PHYSICAL_SIZE')
 v=float(m.group(1));u=m.group(2) or 'px'
 return v if u=='mm' else v*25.4/(96 if u=='px' else 72)
def _norm(text):return ''.join(text.split())
def publication_svg_fail_closed(svg,expected_width_mm,expected_texts,stage,pdf=None,exact=False):
 if pdf is not None and pymupdf is None:raise ValueError('PDF_QA_UNAVAILABLE: install PyMuPDF for PDF inspection')
 path=Path(svg);root=ET.parse(path).getroot();parts=(root.get('viewBox') or '').split()
 if len(parts)!=4 or float(parts[2])<=0 or float(parts[3])<=0:raise ValueError(f'PUBLICATION_SVG_FAIL_CLOSED[{stage}]: invalid canvas')
 fo=sum(x.tag.endswith('foreignObject') for x in root.iter());raster=sum(x.tag.endswith('image') for x in root.iter())
 rendered=_norm(''.join(x.text or '' for x in root.iter() if x.tag.endswith('text') or x.tag.endswith('tspan')))
 missing=[t for t in expected_texts if _norm(t) and _norm(t) not in rendered]
 glyph='\ufffd' in rendered or '\x00' in rendered;width=_length_mm(root.get('width'));tol=.1 if exact else .5
 outside=[]
 if pdf is not None:
  doc=pymupdf.open(pdf);page=doc[0];spans=[q for b in page.get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] for q in l['spans']]
  page_text=_norm(''.join(q['text'] for q in spans));missing=[t for t in expected_texts if _norm(t) and _norm(t) not in page_text]
  glyph=glyph or any('\ufffd' in q['text'] or '\x00' in q['text'] for q in spans)
  outside=[q['text'] for q in spans if not page.rect.contains(pymupdf.Rect(q['bbox']))];width=page.rect.width/72*25.4
 size_pass=(width>0 and expected_width_mm is None) or (expected_width_mm is not None and abs(width-expected_width_mm)<=tol)
 result={'stage':stage,'foreignObject':fo,'raster_embedding':raster,'missing_text':missing,'missing_glyph':bool(glyph),'text_outside_canvas':outside,'width_mm':width,'physical_size_pass':size_pass,'physical_size_policy':'positive source metadata' if expected_width_mm is None else f'{expected_width_mm} +/- {tol} mm','exact_tolerance_mm':None if expected_width_mm is None else tol}
 if fo or raster or missing or glyph or outside or not result['physical_size_pass']:raise ValueError(f'PUBLICATION_SVG_FAIL_CLOSED[{stage}]: {result}')
 return result
