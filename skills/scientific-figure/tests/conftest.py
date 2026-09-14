import pytest
from src.runtime import configure_cairosvg

def _cairo_error():
    try:
        configure_cairosvg({});return None
    except ValueError as exc:return str(exc)

def pytest_configure(config):
    config.addinivalue_line('markers','cairo_integration: requires loadable native Cairo for PDF/PNG export')

def pytest_collection_modifyitems(config,items):
    reason=_cairo_error()
    if not reason:return
    mark=pytest.mark.skip(reason='Cairo publication capability unavailable: '+reason)
    for item in items:
        if 'cairo_integration' in item.keywords:item.add_marker(mark)
