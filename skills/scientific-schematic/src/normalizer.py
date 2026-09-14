"""Publication metadata normalizer: no SVG content or routing changes allowed."""
from pathlib import Path
import re,json,hashlib,xml.etree.ElementTree as ET
def masked(s):
 z=re.search(r'<svg\b[^>]*>',s)
 if z is None:raise ValueError('SVG_ROOT_NOT_FOUND')
 tag=re.sub(r'(?<![\w:-])(?:width|height)="[^"]*"','',z.group())
 return s[:z.start()]+tag+s[z.end():]
def compare_non_size(before,after):
 try:
  rb=ET.fromstring(before);ra=ET.fromstring(after)
 except ET.ParseError:
  return {'all_non_size_bytes_identical':False,'geometry_text_style_unchanged':False,'viewBox_unchanged':False}
 same=masked(before)==masked(after);view=rb.get('viewBox')==ra.get('viewBox')
 return {'all_non_size_bytes_identical':same,'geometry_text_style_unchanged':same and view,'viewBox_unchanged':view}
def normalize(source,destination,width_mm=145):
 raw=Path(source).read_text(encoding='utf8');m=re.search(r'<svg\b[^>]*>',raw)
 if m is None:raise ValueError('SVG_ROOT_NOT_FOUND')
 root=ET.fromstring(raw);parts=(root.get('viewBox') or '').split()
 if len(parts)!=4:raise ValueError('INVALID_VIEWBOX')
 vb=[float(x) for x in parts]
 if vb[2]<=0 or vb[3]<=0:raise ValueError('INVALID_VIEWBOX')
 height=width_mm*vb[3]/vb[2];tag=m.group();new=re.sub(r'(?<![\w:-])width="[^"]*"',f'width="{width_mm:.12g}mm"',tag,count=1);new=re.sub(r'(?<![\w:-])height="[^"]*"',f'height="{height:.12g}mm"',new,count=1)
 result=raw[:m.start()]+new+raw[m.end():];att=compare_non_size(raw,result)
 if not all(att.values()):raise ValueError('NORMALIZATION_INTEGRITY_FAILURE')
 Path(destination).write_text(result,encoding='utf8')
 h=lambda text:hashlib.sha256(text.encode('utf8')).hexdigest()
 return {'source':str(source),'destination':str(destination),'old_width':root.get('width'),'old_height':root.get('height'),'width_mm':width_mm,'height_mm':height,'viewBox':root.get('viewBox'),'non_size_byte_hash_before':h(masked(raw)),'non_size_byte_hash_after':h(masked(result)),**att}
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('output');a=p.parse_args();print(json.dumps(normalize(a.source,a.output),indent=2))
