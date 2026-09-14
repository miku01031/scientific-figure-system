"""Implementation layer. Scientific arrays are read-only inputs; direct endpoints."""
import json,math,warnings,re
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.text import Text
from .semantic_spec import ROOT,digest
from .production_policy import display_label,add_legends,place_annotations,contain_production_labels,position_shared_legend

_CJK_TEXT=re.compile(r'[\u2e80-\u9fff\uac00-\ud7af\uf900-\ufaff\uff00-\uffef\u3000-\u303f]')

def _contains_cjk(value):
 if isinstance(value,str): return bool(_CJK_TEXT.search(value))
 if isinstance(value,dict): return any(_contains_cjk(v) for v in value.values())
 if isinstance(value,(list,tuple)): return any(_contains_cjk(v) for v in value)
 return False

def _render(s,profile,out,archetype,capture):
 t=json.loads((ROOT/'config/design_tokens.yaml').read_text(encoding="utf-8"));w=profile['target_width_mm'];n=len(s['panels'])
 if n>6:raise ValueError('unsupported panel count')
 cols=1 if n==1 or (archetype=='ERRORBAR_POINTWHISKER' and n==2) else 2;rows=math.ceil(n/cols)
 h=max(66,rows*59+15) if cols==1 else rows*64+14
 fonts=t['font_pt'];plt.rcParams.update({'font.family':t['font_family'],'font.size':fonts['tick'],'axes.labelsize':fonts['axis'],'xtick.labelsize':fonts['tick'],'ytick.labelsize':fonts['tick'],'axes.linewidth':t['spine_pt'],'svg.fonttype':'path','svg.hashsalt':'scientific-figure-v1-candidate','path.simplify':False,'agg.path.chunksize':0,'mathtext.fontset':'stix'})
 fig,axs=plt.subplots(rows,cols,figsize=(w/25.4,h/25.4),squeeze=False)
 fig.subplots_adjust(left=max(.09,14/w),right=.97,bottom=14/h,top=1-10/h,wspace=.42,hspace=.65)
 identities=list(dict.fromkeys(q['identity'] for p in s['panels'] for q in p['series']));
 if len(identities)>8:raise ValueError('ENCODING_CAPACITY_EXCEEDED: maximum 8 distinct identities')
 colors={v:t['palette'][i%len(t['palette'])] for i,v in enumerate(identities)}
 from .palette_api import resolve
 color_plan=resolve(profile,identities,'line' if archetype=='DENSE_TIMESERIES' else 'interval' if archetype=='ERRORBAR_POINTWHISKER' else 'filled_marker')
 if color_plan is not None:
  colors=color_plan['colors'];t['reference_color']=color_plan['semantic_colors']['reference'];t['event_color']=color_plan['semantic_colors']['fault_event']
  (out/'PALETTE_PLAN.json').write_text(json.dumps(color_plan,indent=2),encoding='utf8')
 marks=['o','s','^','D','v','P','X','h'];styles=['-','--',':','-.'];checks=[];encoding_records=[];scientific_ids=[];overlap=[];params=[];legends=[];legend_groups=[];resolved_scope='panel';annotation_placement=[]
 def gid(a,p,k):
  name='scientific_'+str(p)+'_'+str(k);a.set_gid(name);scientific_ids.append(name);return a
 def check(name,actual,expected):checks.append({'name':name,'identical':np.array_equal(np.asarray(actual),np.asarray(expected))})
 with warnings.catch_warnings(record=True) as caught:
  warnings.simplefilter('always')
  for pi,(p,ax) in enumerate(zip(s['panels'],axs.flat)):
   ax.set_gid('panel_'+str(pi));ax.set_xlim(p['x_axis']['range']);ax.set_ylim(p['y_axis']['range'])
   for a in ['x','y']:
    info=p[a+'_axis'];getattr(ax,'set_'+a+'label')(info['label'],labelpad=4)
    if 'ticks' in info:getattr(ax,'set_'+a+'ticks')(info['ticks'],info.get('tick_labels'))
   # Explicitly reassert frozen ranges after tick placement.
   ax.set_xlim(p['x_axis']['range']);ax.set_ylim(p['y_axis']['range'])
   ax.set_title((p.get('panel_label','')+' '+p['title']).strip() if 'panel_label' in p else p['title'],fontsize=fonts['panel'],pad=7);ax.tick_params(direction='in',length=3,width=t['spine_pt'],pad=3)
   for ri,r in enumerate(p.get('invalid_regions',[])):
    fn=ax.axvspan if r['axis']=='x' else ax.axhspan;gid(fn(r['start'],r['end'],color='#eeeeee',zorder=0),pi,'invalid'+str(ri))
   byid={q['series_id']:q for q in p['series']}
   for ri,r in enumerate(p.get('references',[])):
    color=colors[byid[r['series_id']]['identity']] if 'series_id' in r else t['reference_color'];fn=ax.axhline if r['axis']=='y' else ax.axvline
    a=gid(fn(r['value'],color=color,lw=t['reference_pt'],ls=':',zorder=1),pi,'ref'+str(ri));check('reference',a.get_ydata() if r['axis']=='y' else a.get_xdata(),[r['value']]*2)
   for si,q in enumerate(p['series']):
    idx=identities.index(q['identity']);color=colors[q['identity']];x=np.asarray(q['x']);y=np.asarray(q['y']);ms=t['marker_pt']
    pts=ax.transData.transform(np.column_stack([x,y]));risk=False
    for prev in p['series'][:si]:
     if len(prev['x'])==len(x) and np.array_equal(prev['x'],x):
      dist=np.linalg.norm(pts-ax.transData.transform(np.column_stack([prev['x'],prev['y']])),axis=1)*72/fig.dpi
      near=int(np.count_nonzero(dist<ms));overlap.append({'panel':pi,'series':q['series_id'],'other':prev['series_id'],'nominal_diameter_pt':ms,'near_count':near,'minimum_distance_pt':float(min(dist))});risk|=near>0
    if risk:ms=t['overlap_marker_pt']
    dense=archetype=='DENSE_TIMESERIES';marker=None if dense else marks[idx%len(marks)];stat=q['statistic'];ls=styles[idx%4] if dense else '--' if 'median' in stat and len({v['statistic'] for v in p['series']})>1 else '-'
    filled=archetype=='DISCRETE_COMPARISON' and not ('median' in stat and len({v['statistic'] for v in p['series']})>1)
    encoding_records.append({'identity':q['identity'],'color':str(color),'marker':str(marker),'linestyle':str(ls if q['connect'] else 'None'),'fill_state':'filled' if filled else ('none' if marker is None else 'hollow')})
    a,=ax.plot(x,y,label=display_label(q),color=color,lw=t['data_linewidth_pt'],ls=ls if q['connect'] else 'None',marker=marker,ms=ms,mfc=color if filled else 'white',mec=color,mew=.8,zorder=3)
    a._semantic_identity=q['identity'];gid(a,pi,'series'+str(si));check('x',a.get_xdata(),x);check('y',a.get_ydata(),y)
    if 'interval_axis' in q:
     lo=np.asarray(q['lower']);hi=np.asarray(q['upper']);vertical=q['interval_axis']=='y'
     segments=np.stack([np.column_stack([x,lo]),np.column_stack([x,hi])],axis=1) if vertical else np.stack([np.column_stack([lo,y]),np.column_stack([hi,y])],axis=1)
     from matplotlib.collections import LineCollection
     c=gid(LineCollection(segments,colors=color,linewidths=1,zorder=2),pi,'interval'+str(si));ax.add_collection(c);check('interval_endpoints',c.get_segments(),segments)
     for label,endpoint in [('lo',lo),('hi',hi)]:
      cap,=ax.plot(x if vertical else endpoint,endpoint if vertical else y,ls='None',marker='_' if vertical else '|',ms=5,color=color,mew=.8,zorder=2);gid(cap,pi,label+str(si))
    params.append({'panel':pi,'panel_width_mm':ax.get_position().width*w,'font_pt':fonts,'font_panel_ratio':fonts['axis']/72*25.4/(ax.get_position().width*w),'marker_pt':0 if dense else ms,'marker_panel_ratio':0 if dense else ms/72*25.4/(ax.get_position().width*w),'linewidth_pt':t['data_linewidth_pt']})
   for ei,r in enumerate(p.get('events',[])):
    if r['role']=='alarm' and 'series_id' in r:
     q=byid[r['series_id']];inds=[i for i,v in enumerate(q['x']) if abs(v-r['value'])<1e-12]
     if len(inds)!=1:raise ValueError('Frozen alarm not on unique sample; no nearest-sample invention')
     k=inds[0];a,=ax.plot([q['x'][k]],[q['y'][k]],marker='v',ms=4,color=colors[q['identity']],ls='None',label=r['meaning'],zorder=4);gid(a,pi,'event'+str(ei));check('alarm_x',a.get_xdata(),[q['x'][k]])
    else:
     fn=ax.axvline if r['axis']=='x' else ax.axhline;a=fn(r['value'],lw=.65,color=t['event_color'] if r['role']=='fault' else t['reference_color'],ls='--',zorder=1);gid(a,pi,'event'+str(ei));check('event',a.get_xdata() if r['axis']=='x' else a.get_ydata(),[r['value']]*2)
     if r['axis']=='x':ax.annotate(r['meaning'],(r['value'],1),xycoords=('data','axes fraction'),xytext=(2,-3),textcoords='offset points',va='top',fontsize=fonts['annotation'])
   for ann in p.get('annotations',[]):
    q=byid[ann['series_id']];k=ann['point_index'];ax.annotate(ann['text'],(q['x'][k],q['y'][k]),xytext=(0,7),textcoords='offset points',ha='center',fontsize=fonts['annotation'])
   check('x_range',ax.get_xlim(),p['x_axis']['range']);check('y_range',ax.get_ylim(),p['y_axis']['range'])
   # Per-panel legend, inside only when categorical labels already encode all identities.
   if archetype!='ERRORBAR_POINTWHISKER':
    handles,labels=ax.get_legend_handles_labels();labels=[v.replace('paired_median_delta','median').replace('paired_mean_delta','mean') for v in labels]
    if profile.get('legend_scope','panel')!='panel':
     legend_groups.append((ax,handles,labels));continue
    lg=ax.legend(handles,labels,loc='upper center',bbox_to_anchor=(.5,-.24),ncol=min(2,len(labels)),frameon=False,fontsize=fonts['legend'],handlelength=2,columnspacing=.8,labelspacing=.25);lg.set_gid('external_legend_'+str(pi));legends.append((lg,ax))
  if legend_groups:legends,resolved_scope=add_legends(fig,legend_groups,profile['legend_scope'],fonts['legend'])
  for ax in list(axs.flat)[n:]:ax.set_visible(False)
  from .mixed_text import install_and_preflight
  tuples={}
  for record in encoding_records:tuples.setdefault((record['color'],record['marker'],record['linestyle'],record['fill_state']),set()).add(record['identity'])
  encoding_collisions=[sorted(v) for v in tuples.values() if len(v)>1]
  if encoding_collisions:raise ValueError('ENCODING_UNIQUENESS_FAIL: '+repr(encoding_collisions))
  install_and_preflight(fig,capture)
  position_shared_legend(fig,legends)
  margin_log=contain_production_labels(fig) if profile.get('legend_scope')=='auto' else []
  if profile.get('annotation_placement')=='bounded':annotation_placement=place_annotations(fig)
  # Automatic measured vertical containment; keep each axes physical size unchanged.
  for iteration in range(3):
   fig.canvas.draw();renderer=fig.canvas.get_renderer();bb=fig.get_tightbbox(renderer);oldh=fig.get_figheight();addbottom=max(0,-bb.y0+2/25.4);addtop=max(0,bb.y1-oldh+2/25.4)
   if addbottom+addtop<.001:break
   positions=[ax.get_position().frozen() for ax in axs.flat];newh=oldh+addbottom+addtop;fig.set_figheight(newh)
   for ax,pos in zip(axs.flat,positions):ax.set_position([pos.x0,(pos.y0*oldh+addbottom)/newh,pos.width,pos.height*oldh/newh])
   position_shared_legend(fig,legends)
  h=fig.get_figheight()*25.4
  fig.canvas.draw();renderer=fig.canvas.get_renderer();bbox=fig.get_tightbbox(renderer);height_pt=h/25.4*72
  from matplotlib.text import Annotation
  annboxes=[(a.get_text(),a.get_window_extent(renderer)) for a in fig.findobj(Annotation)]
  collisions=[(a[0],b[0]) for i,a in enumerate(annboxes) for b in annboxes[:i] if a[1].overlaps(b[1])]
  legend_boxes=[];legend_label_collisions=[]
  for lg,ax in legends:
   b=lg.get_window_extent(renderer)
   if lg.get_gid()=='external_legend_shared':
    for axis in fig.axes:
     labels=[axis.xaxis.label,axis.yaxis.label,axis.title]
     for coord in ['x','y']:
      limits=getattr(axis,'get_'+coord+'lim')();ticks=getattr(axis,'get_'+coord+'ticks')();texts=getattr(axis,'get_'+coord+'ticklabels')()
      labels.extend(t for v,t in zip(ticks,texts) if min(limits)<=v<=max(limits))
     for label in labels:
      if label.get_visible() and label.get_text() and b.overlaps(label.get_window_extent(renderer)):legend_label_collisions.append(label.get_text())
   legend_boxes.append({'id':lg.get_gid(),'bbox_pt':[b.x0*72/fig.dpi,height_pt-b.y1*72/fig.dpi,b.x1*72/fig.dpi,height_pt-b.y0*72/fig.dpi],'external_verified':not b.overlaps(ax.get_window_extent(renderer))})
  overflow=[];overflow_bounds=[]
  for text in fig.findobj(Text):
   if text.get_visible() and text.get_text():
    b=text.get_window_extent(renderer)
    if b.x0<-.5 or b.y0<-.5 or b.x1>fig.bbox.x1+.5 or b.y1>fig.bbox.y1+.5:overflow.append(text.get_text());overflow_bounds.append({'text':text.get_text(),'bbox':list(b.bounds),'canvas':list(fig.bbox.bounds)})
  install_and_preflight(fig,capture)
  draft=out/'draft.svg';fig.savefig(draft,format='svg',metadata={'Date':None})
  import xml.etree.ElementTree as ET
  tree=ET.parse(draft);root=tree.getroot();root.set('data-pipeline','scientific-figure-v1-candidate');tree.write(draft,encoding='utf8',xml_declaration=True)
  manifest={'archetype':archetype,'encoding_records':encoding_records,'encoding_collisions':encoding_collisions,'encoding_unique':not encoding_collisions,'production_margin_containment':margin_log,'legend_label_collisions':legend_label_collisions,'legend_scope_resolved':resolved_scope,'annotation_placement':annotation_placement,'scientific_ids':scientific_ids,'artwork_bbox_pt':[bbox.x0*72,height_pt-bbox.y1*72,bbox.x1*72,height_pt-bbox.y0*72],'legends':legend_boxes,'width_mm':w,'height_mm':h,'checks':checks,'parameters':params,'marker_overlap':overlap,'overflow_bounds':overflow_bounds,'overflow_text':overflow,'warnings':list(dict.fromkeys(str(x.message) for x in caught)),'regular_dense_markers':False,'annotation_collisions':collisions,'automatic_containment_iterations':iteration,'panel_boxes':[[a.get_position().x0,a.get_position().y0,a.get_position().width,a.get_position().height] for a in list(axs.flat)[:n]],'outer_whitespace_fraction':max(0,1-bbox.width*bbox.height/(fig.get_figwidth()*fig.get_figheight()))}
  from .publication_vector_polisher import snapshot
  manifest['expected_svg_snapshot']=snapshot(root)
  capture.extra_warnings.extend(manifest['warnings'])
  plt.close(fig)
 return manifest


def render(s,profile,out,archetype):
 from .render_diagnostics import Capture,resolve_fonts
 capture=Capture();layout=None
 try:
  with capture:
   capture.fonts=resolve_fonts()
   if _contains_cjk(s) and not capture.fonts.get('cjk',{}).get('available',False):
    capture.preflight={'status':'FAIL','errors':['FAIL_CLOSED_FONT_ENVIRONMENT: CJK_FONT_UNAVAILABLE']}
    raise ValueError('FAIL_CLOSED_FONT_ENVIRONMENT: CJK_FONT_UNAVAILABLE')
   with plt.rc_context():
    layout=_render(s,profile,out,archetype,capture)
 except Exception as e:
  if 'FAIL_CLOSED_FONT_ENVIRONMENT' in str(e):capture.preflight={'status':'FAIL','errors':[str(e)]}
  raise
 finally:
  diag=capture.report();(out.parent/'RENDER_DIAGNOSTICS.json').write_text(json.dumps(diag,ensure_ascii=False,indent=2),encoding='utf8');(out.parent/'GLYPH_PREFLIGHT.json').write_text(json.dumps(diag['glyph_preflight'],ensure_ascii=False,indent=2),encoding='utf8')
 if layout is not None:layout['render_diagnostics']=diag
 return layout
