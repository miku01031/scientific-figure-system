import json,copy,subprocess,sys,ast
from pathlib import Path
import pytest
try:
 import pymupdf
except ImportError:
 pymupdf=None
from src.pipeline import run
from src.native_backend import prim
from src.clearance import candidates,choose,plan
from src.portability import discover_drawio
ROOT=Path(__file__).resolve().parents[1]
DRAWIO_AVAILABLE=discover_drawio({}).get('available',False)
def load(name):return json.loads((ROOT/'examples'/f'{name}.json').read_text(encoding='utf-8'))
def test_utf8_cli_profile(tmp_path):
 p=tmp_path/'profile.json';p.write_text(json.dumps({'note':'中文配置','style':'JOURNAL_MINIMAL'},ensure_ascii=False),encoding='utf-8')
 r=subprocess.run([sys.executable,'-B','-m','src.pipeline','--spec',str(ROOT/'examples/T3.json'),'--profile',str(p),'--out',str(tmp_path/'out')],cwd=ROOT,capture_output=True)
 assert r.returncode==0,r.stderr.decode('utf-8',errors='replace')
def test_text_io_encoding_explicit():
 for folder in ['src','tests']:
  for p in (ROOT/folder).glob('*.py'):
   for n in ast.walk(ast.parse(p.read_text(encoding='utf-8-sig'))):
    if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ['read_text','write_text']:assert any(k.arg=='encoding' for k in n.keywords),str(p)
def test_edge_label_bounded_clearance():
 cs=candidates(10,0);assert len(cs)<=21 and len(set(cs))==len(cs)
 best,log=choose(None,10,0,lambda n,t:n in [14,30]);assert best['normal']==14 and best['tangent']==0;assert len(log)<=21
 best,_=choose(None,10,0,lambda n,t:False);assert best is None
@pytest.mark.skipif(pymupdf is None, reason='PyMuPDF PDF-QA capability unavailable')
def test_explicit_label_lock(tmp_path):
 d=pymupdf.open();p=d.new_page(width=200,height=100);p.insert_text((60,50),'infer',fontsize=10);p.insert_text((62,50),'caption',fontsize=10);d.save(tmp_path/'figure.pdf')
 (tmp_path/'figure.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100"/>',encoding='utf-8');s=load('T3');s['edges'][1]['label_position_locked']=True;before=copy.deepcopy(s)
 changed,logs=plan(s,tmp_path);assert not changed and s==before;log=next(q for q in logs if q['edge_id']=='p2');assert log['locked'] and log['collision_before']>0 and not log['tested_candidates']
def test_compact_equation_caption_no_collision():
 s=load('T4');n=next(n for n in s['nodes'] if n.get('primitive')=='equation');n['layout']['size'][1]=50;p=prim(n)[0];assert p['compact'] and p['y']>28
 # The actual application text bbox regression below verifies the compact zone.
def test_regular_equation_unchanged():
 n=next(n for n in load('T4')['nodes'] if n.get('primitive')=='equation');assert n['layout']['size'][1]==100;assert prim(n)==[{'kind':'text','x':n['layout']['size'][0]/2,'y':64.0,'text':'dx/dt = Ax + Bu'}]
@pytest.mark.parametrize('name',['SMOKE_B3','SMOKE_B4','SMOKE_B8'])
@pytest.mark.skipif(not DRAWIO_AVAILABLE,reason='draw.io Desktop unavailable; native XML core remains tested')
def test_application_collision_regression(name,tmp_path):
 s=load(name);before=copy.deepcopy(s);q=run(s,tmp_path/'run');assert s==before;assert q['production_clearance']=='PASS' and not q['text_collision'];assert q['node_edge_label_group_preservation'] and abs(q['width_mm']-145)<.1
 logs=json.loads((tmp_path/'run/EDGE_LABEL_CLEARANCE_LOG.json').read_text(encoding='utf-8'));assert all(len(x['tested_candidates'])<=21 for x in logs)
def test_unknown_grammar_zero_artwork(tmp_path):
 s=load('T3');s['grammar']='UNKNOWN';p=tmp_path/'unknown'
 with pytest.raises(ValueError,match='UNKNOWN_GRAMMAR'):run(s,p)
 assert not p.exists()
