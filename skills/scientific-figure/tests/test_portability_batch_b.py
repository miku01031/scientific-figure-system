import json
from pathlib import Path
import pytest

from src.render_diagnostics import resolve_fonts
from src.runtime import configure_cairosvg


def test_cjk_missing_is_explicit(monkeypatch, tmp_path):
    cfg = tmp_path / 'fonts.json'
    cfg.write_text(json.dumps({
        'latin_serif': ['DejaVu Serif'],
        'cjk_serif': ['FONT_THAT_DOES_NOT_EXIST'],
        'math': ['DejaVu Serif'],
    }), encoding='utf-8')
    monkeypatch.setenv('SCIFIG_FONT_CONFIG', str(cfg))
    result = resolve_fonts()
    assert result['cjk']['available'] is False
    assert result['cjk']['error'] == 'CJK_FONT_UNAVAILABLE'
    assert result['latin']['available'] is True


def test_runtime_has_no_private_path_requirement(monkeypatch):
    monkeypatch.delenv('SCIFIG_RUNTIME_ROOT', raising=False)
    try:
        cairo, info = configure_cairosvg({})
    except ValueError as exc:
        pytest.skip(str(exc))
    assert callable(cairo.svg2pdf)
    assert info['verification'] == 'module-capability'
