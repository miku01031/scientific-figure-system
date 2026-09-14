import copy,json
from pathlib import Path
import pytest
from src.pipeline import validate,build,read,cellmap,GRAMMARS
ROOT=Path(__file__).resolve().parents[1]
def spec():return json.loads((ROOT/'examples/T3.json').read_text(encoding='utf8'))
@pytest.mark.parametrize('p',sorted((ROOT/'examples').glob('*.json')),ids=lambda p:p.stem)
def test_schema(p):assert validate(json.loads(p.read_text(encoding='utf8'))) in GRAMMARS
@pytest.mark.parametrize('case',['grammar','edge','id','primitive','fraction','anchor'])
def test_fail_close(case):
 s=spec()
 if case=='grammar':s['grammar']='UNKNOWN'
 if case=='edge':s['edges'][0]['target']='MISSING'
 if case=='id':s['nodes'][1]['id']=s['nodes'][0]['id']
 if case=='primitive':s['nodes'][0]['primitive']='mini_plot'
 if case=='fraction':s['edges'][0]['label_fraction']=2
 if case=='anchor':s['edges'][0]['label_anchor']='unknown'
 with pytest.raises(Exception):validate(s)
def test_native(tmp_path):
 s=spec();p=tmp_path/'x.drawio';build(s,p);c=cellmap(read(p));assert all(c[e['id']].get('source')==e['source'] and c[e['id']].get('target')==e['target'] for e in s['edges']);assert not list(read(p).iter('image'));assert any(v.get('parent')=='matrix' for v in c.values())
def test_size_gate(tmp_path):
 with pytest.raises(ValueError):build(spec(),tmp_path/'x.drawio',{'target_width_mm':90})
def test_functional_geometry(tmp_path):
 a=tmp_path/'a.drawio';b=tmp_path/'b.drawio';build(spec(),a);build(spec(),b,{'style':'JOURNAL_FUNCTIONAL_COLOR'});ca=cellmap(read(a));cb=cellmap(read(b));import xml.etree.ElementTree as E
 assert all(E.tostring(ca[k].find('mxGeometry'))==E.tostring(cb[k].find('mxGeometry')) for k in ca if ca[k].find('mxGeometry') is not None)
