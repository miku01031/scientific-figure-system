"""Bounded edge-label-only clearance from measured application text geometry.
Maximum 21 candidates; one application re-export; no random or unbounded search.
"""
import math,xml.etree.ElementTree as E
try:
 import pymupdf
except ImportError:
 pymupdf=None
from .native_backend import route
NORMALS=(14,-14,22,-22,30,-30)
def candidates(n,t):
 return [(n,t)]+[(x,t) for x in NORMALS if x!=n]+[(x,y) for x in (n,)+NORMALS for y in (10,-10) if (x,y)!=(n,t)]
def choose(original,normal,tangent,valid):
 cs=candidates(normal,tangent);tested=[{'normal':n,'tangent':t,'valid':valid(n,t)} for n,t in cs]
 good=[(i,c) for i,c in enumerate(tested) if c['valid']]
 best=min(good,key=lambda x:((x[1]['normal']-normal)**2+(x[1]['tangent']-tangent)**2,x[0]))[1] if good else None
 return best,tested

def plan(s,out):
 if pymupdf is None:raise ValueError('PDF_QA_UNAVAILABLE: edge-label clearance requires PDF text inspection')
 doc=pymupdf.open(out/'figure.pdf');page=doc[0];root=E.parse(out/'figure.svg').getroot();vb=list(map(float,root.get('viewBox').split()));scale=vb[2]/page.rect.width
 spans=[q for b in page.get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] for q in l['spans']];boxes=[pymupdf.Rect(*(v*scale for v in q['bbox'])) for q in spans];ns={n['id']:n for n in s['nodes']};K=s['canvas']['width_mm']/25.4*96/s['canvas']['width'];logs=[];changed=False
 def hit(a,b):r=a&b;return r.width>scale and r.height>scale
 segs=[]
 for e in s['edges']:
  pts=route(e,ns);segs += [tuple(v*K for v in (*a,*b)) for a,b in zip(pts,pts[1:])]
 nodeboxes=[pymupdf.Rect(x*K,y*K,(x+w)*K,(y+h)*K) for n in s['nodes'] if n['type']!='container' for x,y in [n['layout']['preferred_position']] for w,h in [n['layout']['size']]]
 for e in s['edges']:
  matches=[i for i,q in enumerate(spans) if q['text'].strip()==e['label'].strip()] if e['label'] else []
  if len(matches)!=1:continue
  i=matches[0];bb=boxes[i];before=sum(hit(bb,b) for j,b in enumerate(boxes) if j!=i);n=e.get('label_normal_offset',10);t=e.get('label_tangent_offset',0)
  log={'edge_id':e['id'],'original_anchor':e.get('label_anchor','middle'),'original_offset':[n,t],'collision_before':before,'tested_candidates':[],'selected_candidate':'current','collision_after':before,'locked':e.get('label_position_locked',False)}
  if not before or log['locked']:logs.append(log);continue
  pts=route(e,ns);ls=[math.dist(a,b) for a,b in zip(pts,pts[1:])];target=e.get('label_fraction',.5)*sum(ls);cum=0;unit=(1,0)
  for a,b,l in zip(pts,pts[1:],ls):
   if l and cum+l>=target:unit=((b[0]-a[0])/l,(b[1]-a[1])/l);break
   cum+=l
  tx,ty=unit;nx,ny=ty,-tx
  def translated(nn,tt):dx=(nn-n)*nx+(tt-t)*tx;dy=(nn-n)*ny+(tt-t)*ty;return bb+(dx,dy,dx,dy)
  def valid(nn,tt):
   r=translated(nn,tt)
   return pymupdf.Rect(0,0,vb[2],vb[3]).contains(r) and not any(hit(r,b) for j,b in enumerate(boxes) if j!=i) and not any(hit(r,b) for b in nodeboxes) and not any(r.intersects(pymupdf.Rect(min(x1,x2)-.6,min(y1,y2)-.6,max(x1,x2)+.6,max(y1,y2)+.6)) for x1,y1,x2,y2 in segs)
  best,tested=choose(bb,n,t,valid);log['tested_candidates']=tested
  if best:
   e['label_normal_offset']=best['normal'];e['label_tangent_offset']=best['tangent'];boxes[i]=translated(best['normal'],best['tangent']);changed=True;log['selected_candidate']=best;log['collision_after']=0
  else:log['selected_candidate']='UNRESOLVED_REVIEW_REQUIRED'
  logs.append(log)
 return changed,logs
