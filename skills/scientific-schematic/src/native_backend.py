from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET,math,copy,csv,zipfile
from html import escape
B=Path(__file__).resolve().parents[1]
TOKENS={'font':'Times New Roman','font_size':15,'stroke':'#242023','accent':'#3288AC','fill':'#EDF4F7','stroke_width':1.2,'width_mm':145,'logical_width':720}
def save(p,v):
 p=B/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False),encoding='utf8')
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def node(i,t,x,y,w=110,h=52,kind='action',primitive=None,shape='rect',group=None):
 d=dict(id=i,label=t,type=kind,layout={'preferred_position':[x,y],'size':[w,h],'rank':0,'lane':None,'group':group},shape=shape)
 if primitive:d['primitive']=primitive
 return d
def edge(i,s,t,label='',sp='right',tp='left',points=None,label_position=None,role='information',style='solid'):
 return dict(id=i,source=s,target=t,label=label,direction='forward',style=style,semantic_role=role,source_port=sp,target_port=tp,waypoints=points or [],label_position=label_position)
def spec(i,grammar,h,n,e):return dict(id=i,grammar=grammar,notice='DEMONSTRATION_ONLY / NOT SCIENTIFIC EVIDENCE',canvas={'width':720,'height':h,'width_mm':145},layout={'direction':'LR'},nodes=n,edges=e)
def bounds(n):return n['layout']['preferred_position']+n['layout']['size']
def port(n,p):
 x,y,w,h=bounds(n);return {'left':(x,y+h/2),'right':(x+w,y+h/2),'top':(x+w/2,y),'bottom':(x+w/2,y+h),'center':(x+w/2,y+h/2)}[p]
def route(e,ns):return [port(ns[e['source']],e['source_port'])]+e['waypoints']+[port(ns[e['target']],e['target_port'])]
def prim(n):
 # Local geometry shared by native mxCells and SVG. No external image payload.
 _,_,w,h=bounds(n);p=n.get('primitive');out=[]
 def add(k,**kw):out.append(dict(kind=k,**kw))
 if p=='waveform':
  pts=[(8+j*(w-16)/28,32+(h-44)*(.5+.33*math.sin(j*.78)*math.exp(-j/90))) for j in range(29)]
  add('polyline',points=pts,color=TOKENS['accent'])
 elif p=='matrix':
  for r in range(3):
   for c in range(4):add('rect',x=14+c*(w-28)/4,y=29+r*(h-38)/3,w=(w-28)/4,h=(h-38)/3,fill=['#FFFFFF','#DFECF1','#A9CCD9'][(r+c)%3])
 elif p in ('graph','model'):
  xy=[(w*.2,36),(w*.2,h-13),(w*.5,30),(w*.5,h-10),(w*.8,(h+30)/2)]
  for a,b in [(0,2),(1,2),(1,3),(2,4),(3,4)]:add('graph_edge',points=[xy[a],xy[b]],source=a,target=b)
  for j,(x,y) in enumerate(xy):add('circle',x=x-4,y=y-4,w=8,h=8,fill=TOKENS['fill'],graph_node=j)
 elif p=='probability':
  for j,v in enumerate([.24,.72,.4]):add('rect',x=18+j*(w-30)/3,y=h-12-v*(h-42),w=13,h=v*(h-42),fill=TOKENS['accent'])
 elif p=='equation':add('text',x=w/2,y=(38 if h<70 else (h+28)/2),text=n['scientific_content']['equation_text'],**({'compact':True} if h<70 else {}))
 elif p=='dataset':
  for r in range(3):
   for c in range(3):add('rect',x=12+c*(w-24)/3,y=30+r*(h-38)/3,w=(w-24)/3,h=(h-38)/3,fill='#FFFFFF')
 elif p=='artifact':
  for j in range(3):add('rect',x=20+j*6,y=34-j*4,w=w-48,h=h-46,fill=TOKENS['fill'])
 return out

def native(d,path):
 mx=ET.Element('mxfile',host='app.diagrams.net',version='24.7.17',compressed='false')
 dg=ET.SubElement(mx,'diagram',id=d['id'],name=d['id']);model=ET.SubElement(dg,'mxGraphModel',dx='720',dy=str(d['canvas']['height']),grid='0',page='1',pageScale='1',pageWidth='720',pageHeight=str(d['canvas']['height']),math='0')
 root=ET.SubElement(model,'root');ET.SubElement(root,'mxCell',id='0');ET.SubElement(root,'mxCell',id='1',parent='0')
 def cell(i,value,parent,style,x,y,w,h):
  c=ET.SubElement(root,'mxCell',id=i,value=value,parent=parent,vertex='1',style=style+';fontFamily=Times New Roman;fontSize='+('14' if 'scientificEquation=1' in style else '15')+';fontColor=#242023;whiteSpace=wrap;html=0;');ET.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'});return c
 def line(i,parent,pts,source=None,target=None,arrow=False,style=''):
  at=dict(id=i,parent=parent,edge='1',style=f'endArrow={"block" if arrow else "none"};endSize=6;strokeWidth=1.2;strokeColor=#242023;rounded=0;'+style)
  if source:at.update(source=source,target=target)
  c=ET.SubElement(root,'mxCell',**at);g=ET.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'})
  for role,pt in [('sourcePoint',pts[0]),('targetPoint',pts[-1])]:ET.SubElement(g,'mxPoint',x=str(pt[0]),y=str(pt[1]),attrib={'as':role})
  if len(pts)>2:
   a=ET.SubElement(g,'Array',attrib={'as':'points'})
   for x,y in pts[1:-1]:ET.SubElement(a,'mxPoint',x=str(x),y=str(y))
  return c,g
 ns={n['id']:n for n in d['nodes']}
 for n in d['nodes']:
  x,y,w,h=bounds(n);parent=n['layout'].get('group') or '1'
  if parent!='1':
   gx,gy,_,_=bounds(ns[parent]);x-=gx;y-=gy
  shape={'rect':'rectangle','diamond':'rhombus','ellipse':'ellipse','text':'text'}[n['shape']]
  style=f'shape={shape};rounded=0;strokeColor=#242023;strokeWidth=1.2;fillColor=#FFFFFF;'
  if n['type']=='container':style+='dashed=1;strokeColor=#A0A0A0;fillColor=none;verticalAlign=top;spacingTop=5;container=1;'
  if n['shape']=='text':style+='strokeColor=none;fillColor=none;'
  if n.get('primitive'):
   cell(n['id'],'',parent,'group;connectable=1;',x,y,w,h)
   cell(n['id']+'_caption',n['label'],n['id'],'shape=text;strokeColor=none;fillColor=none;',0,0,w,24)
   for j,p in enumerate(prim(n)):
    pid=n['id']+'_p'+str(j)
    if p['kind'] in ('polyline','graph_edge'):
     if p['kind']=='graph_edge':line(pid,n['id'],p['points'],n['id']+'_g'+str(p['source']),n['id']+'_g'+str(p['target']))
     else:line(pid,n['id'],p['points'],style='strokeColor=#3288AC;')
    elif p['kind']=='text':
     if p.get('compact'):
      cc=cell(pid,p['text'],n['id'],'shape=text;strokeColor=none;scientificEquation=1;',0,28,w,max(1,h-28))
      cc.set('style',cc.get('style').replace('fontSize=14;','fontSize=10;').replace('whiteSpace=wrap;','whiteSpace=nowrap;'))
     else:cell(pid,p['text'],n['id'],'shape=text;strokeColor=none;scientificEquation=1;',0,p['y']-10,w,22)
    else:
     if 'graph_node' in p:pid=n['id']+'_g'+str(p['graph_node'])
     cell(pid,'',n['id'],f'shape={"ellipse" if p["kind"]=="circle" else "rectangle"};fillColor={p["fill"]};strokeColor=#242023;strokeWidth=0.8;',p['x'],p['y'],p['w'],p['h'])
  else:cell(n['id'],n['label'],parent,style,x,y,w,h)
 ports={'left':(0,.5),'right':(1,.5),'top':(.5,0),'bottom':(.5,1),'center':(.5,.5)}
 for e in d['edges']:
  sx,sy=ports[e['source_port']];tx,ty=ports[e['target_port']]
  c,g=line(e['id'],'1',route(e,ns),e['source'],e['target'],True,f'exitX={sx};exitY={sy};entryX={tx};entryY={ty};exitPerimeter=1;entryPerimeter=1;dashed={int(e["style"]=="dashed")};')
  # Edge labels are native relative children, anchored to the connector midpoint.
  if e['label']:
   pts=route(e,ns);a,b=pts[len(pts)//2-1:len(pts)//2+1];mid=((a[0]+b[0])/2,(a[1]+b[1])/2);lp=e['label_position'] or [mid[0],mid[1]-11]
   lab=ET.SubElement(root,'mxCell',id=e['id']+'_label',value=e['label'],vertex='1',connectable='0',parent=e['id'],style='edgeLabel;html=0;align=center;verticalAlign=middle;fontFamily=Times New Roman;fontSize=15;fontColor=#242023;resizable=0;')
   gg=ET.SubElement(lab,'mxGeometry',x='0',y='0',relative='1',attrib={'as':'geometry'});ET.SubElement(gg,'mxPoint',x=str(lp[0]-mid[0]),y=str(lp[1]-mid[1]),attrib={'as':'offset'})
 # draw.io coordinates are CSS pixels at 96 dpi; normalize every geometric quantity.
 scale=d['canvas']['width_mm']/25.4*96/d['canvas']['width']
 model.set('pageWidth',str(d['canvas']['width']*scale));model.set('pageHeight',str(d['canvas']['height']*scale))
 for g in mx.iter():
  if g.tag in ('mxGeometry','mxPoint'):
   for key in ('x','y','width','height'):
    if key in g.attrib:
     # Relative edge-label x/y are dimensionless; offsets are mxPoint.
     if g.tag=='mxGeometry' and g.get('relative')=='1' and key in ('x','y'):continue
     g.set(key,str(float(g.get(key))*scale))
  if g.tag=='mxCell' and g.get('style'):
   parts=[]
   for part in g.get('style').split(';'):
    if '=' in part:
     key,value=part.split('=',1)
     if key in ('fontSize','strokeWidth','endSize','spacingTop'):part=key+'='+str(float(value)*scale)
    parts.append(part)
   g.set('style',';'.join(parts))
 ET.indent(mx);ET.ElementTree(mx).write(path,encoding='utf-8',xml_declaration=True)
 return mx

def svg(d,path):
 ns={n['id']:n for n in d['nodes']};height=d['canvas']['height'];s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="145mm" height="{145*height/720}mm" viewBox="0 0 720 {height}">', '<defs><marker id="arrow" markerWidth="7" markerHeight="6" refX="7" refY="3" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 L7 3 L0 6 Z" fill="#242023"/></marker></defs>',f'<rect width="720" height="{height}" fill="white"/>']
 def text(x,y,t,size=15):
  lines=t.split('\n')
  for j,l in enumerate(lines):s.append(f'<text x="{x}" y="{y+(j-(len(lines)-1)/2)*17}" text-anchor="middle" dominant-baseline="middle" font-family="Times New Roman" font-size="{size}" fill="#242023">{escape(l)}</text>')
 def poly(pts,arrow=False,color='#242023',dash=False):s.append(f'<polyline points="'+ ' '.join(f'{x},{y}' for x,y in pts)+f'" fill="none" stroke="{color}" stroke-width="1.2"'+(' marker-end="url(#arrow)"' if arrow else '')+(' stroke-dasharray="4 4"' if dash else '')+'/>')
 for n in d['nodes']:
  x,y,w,h=bounds(n)
  if n['type']=='container':
   s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#A0A0A0" stroke-width="1.2" stroke-dasharray="4 4"/>');text(x+w/2,y+16,n['label']);continue
  if n.get('primitive'):
   text(x+w/2,y+12,n['label'])
   for p in prim(n):
    if p['kind'] in ('polyline','graph_edge'):poly([(x+a,y+b) for a,b in p['points']],color=p.get('color','#242023'))
    elif p['kind']=='text':text(x+p['x'],y+p['y'],p['text'],14)
    elif p['kind']=='circle':s.append(f'<ellipse cx="{x+p["x"]+p["w"]/2}" cy="{y+p["y"]+p["h"]/2}" rx="4" ry="4" fill="{p["fill"]}" stroke="#242023" stroke-width="0.8"/>')
    else:s.append(f'<rect x="{x+p["x"]}" y="{y+p["y"]}" width="{p["w"]}" height="{p["h"]}" fill="{p["fill"]}" stroke="#242023" stroke-width="0.8"/>')
  else:
   if n['shape']=='ellipse':s.append(f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w/2}" ry="{h/2}" fill="white" stroke="#242023" stroke-width="1.2"/>')
   elif n['shape']=='diamond':s.append(f'<polygon points="{x+w/2},{y} {x+w},{y+h/2} {x+w/2},{y+h} {x},{y+h/2}" fill="white" stroke="#242023" stroke-width="1.2"/>')
   elif n['shape']!='text':s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="white" stroke="#242023" stroke-width="1.2"/>')
   text(x+w/2,y+h/2,n['label'])
 for e in d['edges']:
  pts=route(e,ns);poly(pts,True,dash=e['style']=='dashed')
  if e['label']:
   a,b=pts[len(pts)//2-1:len(pts)//2+1];lp=e['label_position'] or [(a[0]+b[0])/2,(a[1]+b[1])/2-11];text(*lp,e['label'])
 s.append('</svg>');Path(path).write_text('\n'.join(s),encoding='utf8')

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('spec');p.add_argument('output');a=p.parse_args();native(json.loads(Path(a.spec).read_text(encoding='utf8')),a.output)
