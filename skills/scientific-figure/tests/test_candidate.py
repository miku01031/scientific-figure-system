
import json,copy,hashlib,xml.etree.ElementTree as ET
from pathlib import Path
import pytest
from src.semantic_spec import validate,manifest,digest
from src.archetype_selector import select
from src.pipeline import run
from src.publication_vector_polisher import polish,snapshot

def fixture(tmp_path,domain='discrete'):
 p=tmp_path/'source.json';p.write_text('[0,1,2]', encoding="utf-8");n=40 if domain=='time' else 3
 q={'series_id':'s','meaning':'synthetic fixture','identity':'A','statistic':'observed','x':list(range(n)),'y':[i/10 for i in range(n)],'connect':True}
 if domain=='categorical':q.update(connect=False,interval_axis='y',lower=[i/10-.1 for i in range(n)],upper=[i/10+.1 for i in range(n)],interval_definition='synthetic test bounds')
 a={'label':'x','unit':'s','range':[-1,n]};b={'label':'y','unit':'unit','range':[-1,n/10+1]}
 return {'schema_version':'1.0','figure_id':'synthetic-test','panels':[{'panel_id':'p','title':'Synthetic fixture','domain':domain,'x_axis':a,'y_axis':b,'series':[q]}],'caption_information':'Synthetic fixture only, not research data.','sources':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}]}
PROFILE={'target_width_mm':145,'target_language':'en','output_context':'synthetic test','panel_mode':'single'}

def test_schema_separation(tmp_path):
 s=fixture(tmp_path);validate(s);s['panels'][0]['font']='Arial'
 with pytest.raises(Exception):validate(s)
def test_interval_fail(tmp_path):
 s=fixture(tmp_path,'categorical');s['panels'][0]['series'][0]['lower'][0]=2
 with pytest.raises(Exception):validate(s)
def test_source_sha_fail_forbids_export(tmp_path):
 s=fixture(tmp_path);Path(s['sources'][0]['path']).write_text('changed', encoding="utf-8");r=run(s,PROFILE,tmp_path/'out');assert r['scientific']=='FAIL';assert not (tmp_path/'out/figure.svg').exists()
def test_array_hash_sensitivity(tmp_path):
 s=fixture(tmp_path);old=manifest(s);s['panels'][0]['series'][0]['y'][0]+=1e-12;assert manifest(s)!=old
@pytest.mark.parametrize('domain',['heatmap','confusion_matrix','schematic','3D'])
def test_fail_closed(tmp_path,domain):
 s=fixture(tmp_path);s['panels'][0]['domain']=domain;r=run(s,PROFILE,tmp_path/domain);assert r['fail_closed'];assert not list((tmp_path/domain).glob('*.svg'))
@pytest.mark.cairo_integration
@pytest.mark.parametrize('domain,expected',[('discrete','DISCRETE_COMPARISON'),('time','DENSE_TIMESERIES'),('categorical','ERRORBAR_POINTWHISKER')])
def test_integration(tmp_path,domain,expected):
 s=fixture(tmp_path,domain);assert select(s)==expected;out=tmp_path/'out';r=run(s,PROFILE,out);assert r['FIRST_PASS_TECHNICAL_SUCCESS'],r
 qa=json.loads((out/'QA.json').read_text(encoding="utf-8"));assert abs(qa['width_mm']-145)<.1
 log=json.loads((out/'VECTOR_TRANSFORM_LOG.json').read_text(encoding="utf-8"));assert log['before']==log['after'];assert log['scientific_primitive_hashes_identical']
 layout=json.loads((out/'RENDER_LAYOUT.json').read_text(encoding="utf-8"));src=out/'work/draft.svg';tree=ET.parse(src);root=tree.getroot();path=next(e for e in root.iter() if e.tag.endswith('}path'));path.set('d','M 0 0 L 1 1');tree.write(out/'tampered.svg')
 unsafe=polish(out/'tampered.svg',out/'unsafe.svg',layout);assert unsafe['status']=='SKIPPED_UNSAFE_STRUCTURE'
 # Malicious legend declaration cannot move a scientific group.
 safe_layout=copy.deepcopy(layout);sid=layout['scientific_ids'][0];safe_layout['legends']=[{'id':sid,'bbox_pt':[0,0,10,10],'external_verified':True}]
 log2=polish(src,out/'safe.svg',safe_layout);assert not any(x['operation']=='external_legend_rigid_translation' for x in log2['operations']);assert log2['before']==log2['after'];assert log2['status']=='APPLIED'
