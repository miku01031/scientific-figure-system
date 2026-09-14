import copy,json,sys
from pathlib import Path

ROOT=Path(__file__).parents[1]
def test_native_only_does_not_attest_application(monkeypatch,tmp_path):
    monkeypatch.setenv('PATH',str(tmp_path));monkeypatch.delenv('DRAWIO_EXECUTABLE',raising=False);monkeypatch.delenv('DRAWIO_CONFIG',raising=False)
    sys.path.insert(0,str(ROOT/'skills'/'scientific-schematic'))
    from src.pipeline import run
    spec=json.loads((ROOT/'skills/scientific-schematic/examples/T3.json').read_text(encoding='utf-8'))
    out=tmp_path/'native';result=run(spec,out)
    assert result['native_xml_generation']=='PASS'
    assert result['application_open_save_reopen']=='NOT_CHECKED'
    assert result['node_edge_label_group_preservation'] is None
    assert result['group_preservation'] is None
    assert result['connector_follow'] is None
    assert result['technical_status']=='NATIVE_XML_PASS'
    # Even a deliberately damaged copy is not silently attested as preserved.
    xml=out/'diagram.drawio';tampered=tmp_path/'tampered.drawio';text=xml.read_text(encoding='utf-8').replace('Feature matrix','TAMPERED')
    tampered.write_text(text,encoding='utf-8')
    qa=json.loads((out/'QA.json').read_text(encoding='utf-8'))
    assert qa['preservation_status']=='NOT_CHECKED'
