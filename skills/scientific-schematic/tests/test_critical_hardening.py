import copy,json,xml.etree.ElementTree as ET
from pathlib import Path
import pytest
from src.pipeline import validate,run,read,cellmap
from src.native_backend import prim
from src.normalizer import compare_non_size,normalize
from src.qa import structure_attestation
from src.publication_gate import publication_svg_fail_closed
ROOT=Path(__file__).resolve().parents[1]
def load(name='T4'):return json.loads((ROOT/'examples'/f'{name}.json').read_text(encoding='utf-8'))
def test_equation_text_from_spec(tmp_path):
 s=load();n=next(n for n in s['nodes'] if n.get('primitive')=='equation');n['scientific_content']['equation_text']='x_dot = f(x, u)';validate(s);out=tmp_path/'x.drawio';from src.pipeline import build;build(s,out);values=[c.get('value') for c in read(out).iter('mxCell')];assert 'x_dot = f(x, u)' in values and 'dx/dt = Ax + Bu' not in values
def test_equation_missing_input_fail_closed():
 s=load();n=next(n for n in s['nodes'] if n.get('primitive')=='equation');n.pop('scientific_content')
 with pytest.raises(ValueError,match='EQUATION_TEXT_REQUIRED'):validate(s)
def test_iconic_non_data_contract():
 s=load('T3');nodes=[n for n in s['nodes'] if n.get('primitive')];assert nodes and all(n['representation_class']=='ICONIC_NON_DATA' for n in nodes);wave=next(n for n in nodes if n['primitive']=='waveform');assert all(x['kind']!='text' for x in prim(wave))
 s['nodes'][0]['representation_class']='SCIENTIFIC_DATA'
 with pytest.raises(ValueError,match='ICONIC_NON_DATA'):validate(s)
def test_normalizer_attestation_negative(tmp_path):
 before='<svg xmlns="http://www.w3.org/2000/svg" width="100px" height="50px" viewBox="0 0 100 50"><text x="2" y="4" style="fill:black">A</text></svg>'
 for after in [before.replace('A','B'),before.replace('x="2"','x="3"'),before.replace('fill:black','fill:red')]:
  q=compare_non_size(before,after);assert not q['all_non_size_bytes_identical'] and not q['geometry_text_style_unchanged']
 p=tmp_path/'a.svg';o=tmp_path/'b.svg';p.write_text(before,encoding='utf-8');q=normalize(p,o,145);assert q['all_non_size_bytes_identical'] and q['geometry_text_style_unchanged']
def test_application_attestation_negative():
 s=load('T3');from src.pipeline import build
 import tempfile
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'x.drawio';build(s,p);before=cellmap(read(p));after=cellmap(read(p));after['model'].set('value','tampered');assert not structure_attestation(before,after)
def test_publication_svg_negative_gate(tmp_path):
 s='<svg xmlns="http://www.w3.org/2000/svg" width="145mm" height="50mm" viewBox="0 0 100 50"><text x="2" y="4">A</text></svg>';p=tmp_path/'x.svg';p.write_text(s,encoding='utf-8');assert publication_svg_fail_closed(p,145,['A'],'test',exact=True)['physical_size_pass']
 p.write_text(s.replace('<text','<image href="x.png"/><text'),encoding='utf-8')
 with pytest.raises(ValueError,match='PUBLICATION_SVG_FAIL_CLOSED'):publication_svg_fail_closed(p,145,['A'],'tampered',exact=True)
def test_clearance_rerender_re_gated(tmp_path):
 from src.portability import discover_drawio
 if not discover_drawio({}).get('available'):pytest.skip('draw.io Desktop unavailable; application re-export is optional')
 q=run(load('SMOKE_B4'),tmp_path/'run');stages=[x['stage'] for x in q['publication_gate']];assert stages==['application_initial','normalized_initial','final_initial','application_clearance','normalized_clearance','final_clearance']
def test_unknown_grammar_no_artwork(tmp_path):
 s=load('T3');s['grammar']='UNKNOWN';out=tmp_path/'out'
 with pytest.raises(ValueError,match='UNKNOWN_GRAMMAR'):run(s,out)
 assert not out.exists()
