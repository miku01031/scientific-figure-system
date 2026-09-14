
import json,logging,copy
import pytest
from test_candidate import fixture,PROFILE
from src.pipeline import run
pytestmark=pytest.mark.cairo_integration
from src.render_diagnostics import Capture

def mixed_fixture(tmp_path):
 s=fixture(tmp_path);p=s['panels'][0];p['title']=r'中文标题 $\sigma^2$';p['x_axis']['label']=r'根级配对及时检出差 $\Delta_{\mathrm{root}}$（相对 D0 匹配基线）';p['y_axis']['label']=r'健康背景 $b_{\max}$ 配对位移';p['x_axis'].update(ticks=[0,1,2],tick_labels=[r'条件 $\alpha_1$',r'条件 $\alpha_2$',r'条件 $\alpha_3$']);p['series'][0]['meaning']=r'系列 $\beta^2$';p['annotations']=[{'series_id':'s','point_index':1,'text':r'注释 $\theta_0$'}];return s

def test_mixed_cjk_math_missing_glyph_detected(tmp_path):
 s=mixed_fixture(tmp_path);s['panels'][0]['x_axis']['label']+='\U0010ffff';r=run(s,{**PROFILE,'target_language':'zh'},tmp_path/'out');assert not r['FIRST_PASS_TECHNICAL_SUCCESS'];assert r['vector']=='FAIL';assert not (tmp_path/'out/figure.pdf').exists();assert not (tmp_path/'out/figure.png').exists();d=json.loads((tmp_path/'out/RENDER_DIAGNOSTICS.json').read_text(encoding='utf8'));assert d['missing_glyph_count']>0

def test_mixed_cjk_math_valid_render_passes(tmp_path):
 r=run(mixed_fixture(tmp_path),{**PROFILE,'target_language':'zh'},tmp_path/'out');assert r['FIRST_PASS_TECHNICAL_SUCCESS'],r
 d=json.loads((tmp_path/'out/RENDER_DIAGNOSTICS.json').read_text(encoding='utf8'));assert d['missing_glyph_count']==0;assert d['glyph_preflight']['status']=='PASS';assert sum(q['mixed_compositor'] for q in d['mathtext_usage'])>=6
 assert all((tmp_path/'out'/('figure.'+e)).exists() for e in ['svg','pdf','png'])

def test_logger_warning_rejects_pipeline(tmp_path,monkeypatch):
 import src.render_matplotlib as rm
 original=rm._render
 def bad(*args,**kw):
  value=original(*args,**kw);logging.getLogger('matplotlib.mathtext').warning("Font 'test' does not have a glyph, substituting with a dummy symbol.");return value
 monkeypatch.setattr(rm,'_render',bad);r=run(fixture(tmp_path),PROFILE,tmp_path/'out');assert r['vector']=='FAIL';assert not r['FIRST_PASS_TECHNICAL_SUCCESS'];assert not (tmp_path/'out/figure.pdf').exists()

def test_missing_required_font_fails_closed(tmp_path,monkeypatch):
 import src.render_diagnostics as rd
 monkeypatch.setitem(rd.FONT_REQUIREMENTS,'cjk','RC1_TEST_FONT_DOES_NOT_EXIST');r=run(mixed_fixture(tmp_path),PROFILE,tmp_path/'out');assert r['vector']=='FAIL';assert 'FAIL_CLOSED_FONT_ENVIRONMENT' in r['error'];assert not (tmp_path/'out/figure.pdf').exists()

def test_logger_configuration_restored_on_exception():
 parent=logging.getLogger('matplotlib');child=logging.getLogger('matplotlib.mathtext');before=[(l,l.level,l.disabled,l.propagate,list(l.handlers),list(l.filters)) for l in [parent,child]]
 with pytest.raises(RuntimeError):
  with Capture() as c:
   child.warning('dummy symbol injected');raise RuntimeError('test cleanup')
 for l,lev,dis,pro,handlers,filters in before:assert (l.level,l.disabled,l.propagate,l.handlers,l.filters)==(lev,dis,pro,handlers,filters)
 assert c.report()['status']=='FAIL'

def test_python_warning_capture():
 import warnings
 with Capture() as c:warnings.warn('Glyph 999 missing from font')
 assert c.report()['missing_glyph_count']==1
