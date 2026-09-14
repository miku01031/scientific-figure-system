import copy,json,hashlib
import pytest
pytestmark=pytest.mark.cairo_integration
from test_candidate import fixture,PROFILE
from src.semantic_spec import validate
from src.pipeline import run
from src.production_policy import display_label,clearance,width_status

def two_panels(tmp_path):
 s=fixture(tmp_path);p=copy.deepcopy(s['panels'][0]);p['panel_id']='p2';s['panels'].append(p);return s

def test_meaning_and_display_label_separated(tmp_path):
 s=fixture(tmp_path);q=s['panels'][0]['series'][0];original=q['meaning'];q['display_label']='A';q['display_label_source']={**s['sources'][0],'locator':'explicit test display name'};validate(s)
 assert display_label(q)=='A' and q['meaning']==original

def test_display_label_provenance_required(tmp_path):
 s=fixture(tmp_path);s['panels'][0]['series'][0]['display_label']='A'
 with pytest.raises(Exception,match='provenance'):validate(s)

def test_shared_legend_identical_multiplanel(tmp_path):
 s=two_panels(tmp_path);out=tmp_path/'out';r=run(s,{**PROFILE,'panel_mode':'multi','legend_scope':'auto'},out);assert r['FIRST_PASS_TECHNICAL_SUCCESS']
 lay=json.loads((out/'RENDER_LAYOUT.json').read_text(encoding="utf-8"));assert lay['legend_scope_resolved']=='figure' and len(lay['legends'])==1
 assert not lay['legend_label_collisions']

def test_panel_legend_different_series(tmp_path):
 s=two_panels(tmp_path);s['panels'][1]['series'][0]['identity']='B';out=tmp_path/'out';r=run(s,{**PROFILE,'legend_scope':'auto'},out);assert r['FIRST_PASS_TECHNICAL_SUCCESS']
 lay=json.loads((out/'RENDER_LAYOUT.json').read_text(encoding="utf-8"));assert lay['legend_scope_resolved']=='panel' and len(lay['legends'])==2

def test_complex_factorial_discrete_fail_closed(tmp_path):
 s=fixture(tmp_path);s['panels'][0]['series']=[{**copy.deepcopy(s['panels'][0]['series'][0]),'series_id':str(i)} for i in range(9)]
 out=tmp_path/'out';r=run(s,PROFILE,out);assert r['reason']=='ENCODING_CAPACITY_EXCEEDED';assert r['PRODUCTION_CLEARANCE']=='UNSUPPORTED';assert not list(out.glob('figure.*'))
 s=fixture(tmp_path);s['panels'][0]['visual_factors']=['motor','component'];r=run(s,PROFILE,tmp_path/'factors');assert r['fail_closed']

def test_annotation_collision_clearance(tmp_path):
 result={'SUPPORTED_ARCHETYPE':True,'FIRST_PASS_TECHNICAL_SUCCESS':True}
 assert clearance(result,{'checks':{'annotation_collision':'WARN'}},{'width_authority':'user_explicit'})=='REVIEW_REQUIRED'
 s=fixture(tmp_path,'categorical');s['panels'][0]['annotations']=[{'series_id':'s','point_index':1,'text':t} for t in ['A','B']];out=tmp_path/'out'
 r=run(s,{**PROFILE,'annotation_placement':'bounded'},out);lay=json.loads((out/'RENDER_LAYOUT.json').read_text(encoding="utf-8"));assert r['scientific']=='PASS';assert len(lay['annotation_placement'])==2;assert all(v['candidate_count']==7 for v in lay['annotation_placement'])
 if lay['annotation_collisions']:assert r['PRODUCTION_CLEARANCE']=='REVIEW_REQUIRED'

def test_artwork_edge_requires_review():
 assert clearance({'FIRST_PASS_TECHNICAL_SUCCESS':True},{'checks':{'artwork_edge':'WARN'}},{'width_authority':'user_explicit'})=='REVIEW_REQUIRED'

def test_old_spec_backward_compatible(tmp_path):
 s=fixture(tmp_path);a=tmp_path/'a';b=tmp_path/'b';run(s,PROFILE,a);run(s,{**PROFILE,'legend_scope':'panel'},b)
 assert (a/'figure.svg').read_bytes()==(b/'figure.svg').read_bytes()
 assert (a/'figure.png').read_bytes()==(b/'figure.png').read_bytes()

def test_production_width_not_validation_width():
 p={**PROFILE,'target_width_mm':180,'width_authority':'validation'}
 assert width_status(p)=='NON_PRODUCTION_WIDTH'
 assert clearance({'FIRST_PASS_TECHNICAL_SUCCESS':True},{'checks':{}},p)=='REVIEW_REQUIRED'
 assert width_status({**p,'target_width_mm':390/72.27*25.4,'width_authority':'current_manuscript'})=='PRODUCTION_CONTEXT'
