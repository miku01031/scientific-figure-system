import json
from pathlib import Path

from src.portability import discover_drawio
from src.pipeline import run

ROOT = Path(__file__).resolve().parents[1]


def test_drawio_discovery_can_be_unavailable(monkeypatch, tmp_path):
    monkeypatch.delenv('DRAWIO_EXECUTABLE', raising=False)
    monkeypatch.delenv('DRAWIO_CONFIG', raising=False)
    monkeypatch.setenv('PATH', str(tmp_path))
    result = discover_drawio({'drawio_executable': str(tmp_path / 'missing.exe')})
    assert result['available'] is False
    assert result['reason'] == 'DRAWIO_NOT_FOUND'


def test_native_generation_without_application(tmp_path, monkeypatch):
    monkeypatch.delenv('DRAWIO_EXECUTABLE', raising=False)
    monkeypatch.delenv('DRAWIO_CONFIG', raising=False)
    monkeypatch.delenv('SCHEMATIC_REQUIRE_DRAWIO', raising=False)
    monkeypatch.setenv('PATH', str(tmp_path))
    spec = json.loads((ROOT / 'examples' / 'T1.json').read_text(encoding='utf-8'))
    result = run(spec, tmp_path / 'native')
    assert result['native_only'] is True
    assert result['application_export_capability'] == 'UNAVAILABLE'
    assert result['native_xml_generation'] == 'PASS'
    assert result['application_open_save_reopen'] == 'NOT_CHECKED'
    assert result['node_edge_label_group_preservation'] is None
    assert result['group_preservation'] is None
    assert result['connector_follow'] is None
    assert result['technical_status'] == 'NATIVE_XML_PASS'
    assert (tmp_path / 'native' / 'diagram.drawio').exists()
