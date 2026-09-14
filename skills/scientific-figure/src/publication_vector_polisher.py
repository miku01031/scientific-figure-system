"""Fail-closed viewport composition. No data or axis geometry mutations."""
import xml.etree.ElementTree as ET
import hashlib,json,copy
NS='http://www.w3.org/2000/svg';ET.register_namespace('',NS);ET.register_namespace('xlink','http://www.w3.org/1999/xlink')
def snapshot(root):
 primitives=[(e.tag,dict(e.attrib),e.text) for e in root.iter() if e.tag.split('}')[-1] in ['path','use','clipPath','text','rect','line','polygon','polyline','circle','ellipse']]
 groups={e.get('id'):hashlib.sha256(ET.tostring(e)).hexdigest() for e in root.iter() if (e.get('id') or '').startswith('scientific_')}
 # Ancestor transforms are part of the scientific geometry contract.
 parents={c:p for p in root.iter() for c in p};ancestors={}
 for e in root.iter():
  if (e.get('id') or '').startswith('scientific_'):
   a=e;chain=[]
   while a in parents:a=parents[a];chain.append([a.get('id'),a.get('transform')])
   ancestors[e.get('id')]=chain
 return {'primitive_hash':hashlib.sha256(json.dumps(primitives,sort_keys=True).encode()).hexdigest(),'scientific_groups':groups,'ancestor_transforms':ancestors}
def polish(src,dest,layout):
 root=ET.parse(src).getroot();before=snapshot(root);ops=[];reason=None
 if root.get('data-pipeline')!='scientific-figure-v1-candidate':reason='unrecognized producer'
 elif layout.get('expected_svg_snapshot')!=before:reason='expected primitive fingerprint mismatch'
 elif set(before['scientific_groups'])!=set(layout['scientific_ids']):reason='scientific group manifest mismatch'
 elif any(e.tag.split('}')[-1]=='image' for e in root.iter()):reason='raster embedding'
 if reason:
  dest.write_bytes(src.read_bytes());return {'status':'SKIPPED_UNSAFE_STRUCTURE','reason':reason,'before':before,'after':before,'scientific_primitive_hashes_identical':True,'operations':[]}
 vb=list(map(float,root.get('viewBox').split()));width,height=vb[2:];top=max(0,layout['artwork_bbox_pt'][1]-6);bottom=min(height,layout['artwork_bbox_pt'][3]+6)
 # Overflow is not silently cropped or repaired. Preserve original viewport and warn.
 if bottom<=top or layout['artwork_bbox_pt'][1]<0 or layout['artwork_bbox_pt'][3]>height:top=0;bottom=height
 for record in layout['legends']:
  if not record['external_verified']:continue
  g=next((e for e in root.iter() if e.get('id')==record['id']),None)
  if g is None:continue
  if any((e.get('id') or '').startswith('scientific_') for e in g.iter()):continue
  b=record['bbox_pt'];dx=width/2-(b[0]+b[2])/2
  # Only a single full-width panel's external legend can be centered globally.
  if len(layout['legends'])!=1 or b[0]+dx<0 or b[2]+dx>width:continue
  g.set('transform',f'translate({dx:.8f} 0) '+g.get('transform',''));ops.append({'operation':'external_legend_rigid_translation','id':g.get('id'),'dx_pt':dx,'dy_pt':0})
 root.set('width',f'{layout["width_mm"]:.9f}mm');root.set('height',f'{(bottom-top)/72*25.4:.9f}mm');root.set('viewBox',f'0 {top:.9f} {width:.9f} {bottom-top:.9f}')
 ops.append({'operation':'viewport_crop_and_physical_metadata','top_removed_pt':top,'bottom_removed_pt':height-bottom,'scale':1})
 after=snapshot(root)
 if before!=after:raise ValueError('SCIENTIFIC_DOM_CHANGED: export forbidden')
 dest.write_bytes(ET.tostring(root,encoding='utf8',xml_declaration=True))
 return {'status':'APPLIED','before':before,'after':after,'scientific_primitive_hashes_identical':before==after,'operations':ops}
