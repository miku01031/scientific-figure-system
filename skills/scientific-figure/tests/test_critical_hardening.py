import copy,json,sys
from pathlib import Path
import matplotlib.pyplot as plt
import pytest
from test_candidate import fixture,PROFILE
from src.pipeline import run
from src.semantic_spec import validate
from src.production_policy import clearance
from src.qa_gate_policy import evaluate

def duplicate_series(s,n):
 q=s['panels'][0]['series'][0];s['panels'][0]['series']=[]
 for i in range(n):
  v=copy.deepcopy(q);v['series_id']=f's{i}';v['identity']=f'I{i}';v['meaning']=f'Synthetic {i}';v['y']=[x+i*.01 for x in v['y']]
  s['panels'][0]['series'].append(v)
 return s
@pytest.mark.parametrize('case',['inverted_interval','xy_mismatch','duplicate_panel','wrong_display_sha','upper_mismatch'])
def test_five_invalid_cases_rejected(case,tmp_path):
 s=fixture(tmp_path,'categorical')
 if case=='inverted_interval':s['panels'][0]['series'][0]['lower'][0]=10
 if case=='xy_mismatch':s['panels'][0]['series'][0]['y'].pop()
 if case=='duplicate_panel':s['panels'].append(copy.deepcopy(s['panels'][0]))
 if case=='wrong_display_sha':
  q=s['panels'][0]['series'][0];q['display_label']='X';q['display_label_source']={**s['sources'][0],'sha256':'0'*64,'locator':'test'}
 if case=='upper_mismatch':s['panels'][0]['series'][0]['upper'].pop()
 out=tmp_path/'out';r=run(s,PROFILE,out);assert r['scientific']=='FAIL';assert not list(out.glob('figure.*'));inv=json.loads((out/'SCIENTIFIC_INVARIANCE.json').read_text(encoding='utf-8'));assert inv['validation']=='REJECTED' and inv['python_optimization_level']==sys.flags.optimize and inv['__debug__']==__debug__
@pytest.mark.parametrize('domain,n',[('discrete',9),('discrete',12),('time',9)])
def test_encoding_capacity_fail_closed(domain,n,tmp_path):
 s=duplicate_series(fixture(tmp_path,domain),n);out=tmp_path/'out';r=run(s,PROFILE,out);assert r['PRODUCTION_CLEARANCE']=='UNSUPPORTED';assert r['reason']=='ENCODING_CAPACITY_EXCEEDED';assert not list(out.glob('figure.*'))
@pytest.mark.cairo_integration
def test_encoding_tuple_unique(tmp_path):
 s=duplicate_series(fixture(tmp_path),8);out=tmp_path/'out';r=run(s,PROFILE,out);assert r['TECHNICAL_STATUS']=='PASS';layout=json.loads((out/'RENDER_LAYOUT.json').read_text(encoding='utf-8'));tuples={(q['color'],q['marker'],q['linestyle'],q['fill_state']) for q in layout['encoding_records']};assert len(tuples)==8 and layout['encoding_unique'];qa=json.loads((out/'QA.json').read_text(encoding='utf-8'));assert qa['checks']['encoding_uniqueness']=='PASS'
def test_qa_gate_policy_unknown_defaults_review():
 p=evaluate({'future_check':'WARN','physical_size':'PASS'});assert p['review']==['future_check'];assert p['unknown_default_review']==['future_check'];assert clearance({'SUPPORTED_ARCHETYPE':True,'FIRST_PASS_TECHNICAL_SUCCESS':True},{'checks':{'future_check':'WARN'}},{'width_authority':'user_explicit'})=='REVIEW_REQUIRED'
def test_qa_gate_encoding_blocks():
 p=evaluate({'encoding_uniqueness':'FAIL'});assert p['block']==['encoding_uniqueness'];assert clearance({'SUPPORTED_ARCHETYPE':True,'FIRST_PASS_TECHNICAL_SUCCESS':True},{'checks':{'encoding_uniqueness':'FAIL'}},{'width_authority':'user_explicit'})=='UNSUPPORTED'
@pytest.mark.cairo_integration
def test_color_preview_is_not_pass(tmp_path):
 s=fixture(tmp_path);out=tmp_path/'out';run(s,PROFILE,out);q=json.loads((out/'COLOR_QA.json').read_text(encoding='utf-8'));assert 'status' not in q and q['COLOR_PREVIEWS_GENERATED'] and q['evaluation']=='NOT_CHECKED'
@pytest.mark.cairo_integration
def test_matplotlib_global_state_restored(tmp_path):
 before=plt.rcParams.copy();run(fixture(tmp_path),PROFILE,tmp_path/'out');assert dict(plt.rcParams)==dict(before)
def test_dependency_truth():
 req=(Path(__file__).parents[3]/'requirements-core.txt').read_text(encoding='utf-8');assert 'PyYAML' in req
