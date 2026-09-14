import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]

def test_figure_import():
    sys.path.insert(0, str(ROOT / "skills" / "scientific-figure"))
    import src.pipeline  # noqa: F401

def test_schematic_import():
    sys.path.insert(0, str(ROOT / "skills" / "scientific-schematic"))
    for name in list(sys.modules):
        if name == "src" or name.startswith("src."): del sys.modules[name]
    import src.pipeline  # noqa: F401
