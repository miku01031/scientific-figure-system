"""Conservative production policies; never authorizes formal-artwork replacement."""
from .qa_gate_policy import evaluate
def display_label(q):return q.get('display_label',q['meaning'])
def width_status(profile):
 authority=profile.get('width_authority')
 if authority in ['current_manuscript','user_explicit']:return 'PRODUCTION_CONTEXT'
 if authority=='current_artwork_proxy':return 'REVIEW_REQUIRED_WIDTH_PROXY'
 return 'NON_PRODUCTION_WIDTH'
def clearance(result,qa,profile):
 if not result.get('SUPPORTED_ARCHETYPE',True):return 'UNSUPPORTED'
 policy=evaluate(qa.get('checks',{}))
 if policy['block']:return 'UNSUPPORTED'
 if not result.get('FIRST_PASS_TECHNICAL_SUCCESS'):return 'REVIEW_REQUIRED'
 if policy['review']:return 'REVIEW_REQUIRED'
 if width_status(profile)!='PRODUCTION_CONTEXT':return 'REVIEW_REQUIRED'
 return 'PASS'
def encoding_signature(handles,labels):
 return sorted([(getattr(h,'_semantic_identity',None),label,str(h.get_color()),h.get_linestyle(),str(h.get_marker()),h.get_markersize(),str(h.get_markerfacecolor()),str(h.get_markeredgecolor()),h.get_linewidth()) for h,label in zip(handles,labels)],key=repr)
def shared_compatible(groups):
 signatures=[encoding_signature(h,l) for ax,h,l in groups]
 return len(signatures)>1 and all(s==signatures[0] for s in signatures[1:])

def add_legends(fig,groups,scope,font):
 if scope not in ['panel','figure','auto']:raise ValueError('Invalid legend_scope')
 shared=scope in ['auto','figure'] and shared_compatible(groups)
 legends=[]
 if shared:
  ax,h,l=groups[0]
  lg=fig.legend(h,l,loc='lower center',bbox_to_anchor=(.5,.012),ncol=len(l),borderaxespad=0,frameon=False,fontsize=font,handlelength=2,columnspacing=.8,labelspacing=.25)
  lg.set_gid('external_legend_shared');legends.append((lg,ax))
 else:
  for i,(ax,h,l) in enumerate(groups):
   lg=ax.legend(h,l,loc='upper center',bbox_to_anchor=(.5,-.24),ncol=min(2,len(l)),frameon=False,fontsize=font,handlelength=2,columnspacing=.8,labelspacing=.25)
   lg.set_gid('external_legend_'+str(i));legends.append((lg,ax))
 return legends,'figure' if shared else 'panel'

def place_annotations(fig):
 from matplotlib.text import Annotation
 from matplotlib.transforms import Bbox
 from matplotlib.collections import LineCollection
 import numpy as np
 fig.canvas.draw();renderer=fig.canvas.get_renderer();annotations=fig.findobj(Annotation);obstacles=[];accepted=[];log=[]
 for ax in fig.axes:
  for line in ax.lines:
   if line.get_marker() in [None,'None','',' ']:continue
   radius=max(line.get_markersize(),2)*fig.dpi/72/2+2
   for x,y in ax.transData.transform(np.column_stack([line.get_xdata(),line.get_ydata()])):
    if ax.bbox.contains(x,y):obstacles.append(Bbox.from_extents(x-radius,y-radius,x+radius,y+radius))
  for c in ax.collections:
   if isinstance(c,LineCollection):
    for seg in c.get_segments():
     xy=ax.transData.transform(seg);lo=xy.min(axis=0);hi=xy.max(axis=0);obstacles.append(Bbox.from_extents(lo[0]-2,lo[1]-2,hi[0]+2,hi[1]+2))
 for a in annotations:
  original=a.get_position();ha=a.get_ha();va=a.get_va();bb=a.get_window_extent(renderer);w=bb.width*72/fig.dpi;h=bb.height*72/fig.dpi
  candidates=[(0,7,'center','bottom'),(-7,7,'right','bottom'),(7,7,'left','bottom'),(-7,0,'right','center'),(7,0,'left','center'),(-7,-7,'right','top'),(7,-7,'left','top')]
  def distance(c):
   x,y,hh,vv=c;cx=x+({'left':1,'center':0,'right':-1}[hh])*w/2;cy=y+({'bottom':1,'center':0,'top':-1}[vv])*h/2;return cx*cx+cy*cy
  selected=None
  for c in sorted(candidates,key=distance):
   a.set_position(c[:2]);a.set_ha(c[2]);a.set_va(c[3]);bb=a.get_window_extent(renderer)
   inside=bb.x0>=2 and bb.y0>=2 and bb.x1<=fig.bbox.width-2 and bb.y1<=fig.bbox.height-2
   if inside and not any(bb.overlaps(b) for b in accepted+obstacles):selected=c;break
  if selected is None:a.set_position(original);a.set_ha(ha);a.set_va(va)
  accepted.append(a.get_window_extent(renderer).expanded(1.03,1.03));log.append({'text':a.get_text(),'original_offset':original,'selected_offset':a.get_position(),'safe':selected is not None,'candidate_count':7})
 return log

def contain_production_labels(fig):
 log=[]
 for iteration in range(3):
  fig.canvas.draw();r=fig.canvas.get_renderer();bb=fig.get_tightbbox(r);width=fig.get_figwidth();left=max(0,-bb.x0+1/25.4);right=max(0,bb.x1-width+1/25.4)
  if left+right<.001:break
  if (left+right)/width>.05:break
  axes=[a for a in fig.axes if a.get_visible()];positions=[a.get_position().frozen() for a in axes];lo=min(p.x0 for p in positions);hi=max(p.x1 for p in positions);newlo=lo+left/width;newhi=hi-right/width;scale=(newhi-newlo)/(hi-lo)
  for ax,p in zip(axes,positions):ax.set_position([newlo+(p.x0-lo)*scale,p.y0,p.width*scale,p.height])
  log.append({'iteration':iteration,'left_added_in':left,'right_added_in':right,'operation':'renderer horizontal margin containment; physical canvas unchanged','scientific_values_changed':'NOT_CHECKED_HERE'})
 return log

def position_shared_legend(fig,legends):
 if not legends or legends[0][0].get_gid()!='external_legend_shared':return
 fig.canvas.draw();r=fig.canvas.get_renderer();lg=legends[0][0];bottom=min(a.get_tightbbox(r).y0 for a in fig.axes if a.get_visible());height=lg.get_window_extent(r).height;lg.set_bbox_to_anchor((.5,(bottom-4*fig.dpi/72-height)/fig.bbox.height))
