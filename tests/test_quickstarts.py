from pathlib import Path
import json,subprocess,sys

ROOT=Path(__file__).parents[1]
def test_figure_quickstart(tmp_path):
    r=subprocess.run([sys.executable,str(ROOT/'examples/synthetic/figure_minimal/run_example.py')],cwd=ROOT,text=True,capture_output=True)
    assert r.returncode==0,r.stderr
    out=ROOT/'examples/synthetic/figure_minimal/output'
    assert (out/'figure.svg').exists() or (out/'figure.DIAGNOSTIC.svg').exists()
def test_schematic_quickstart(tmp_path):
    r=subprocess.run([sys.executable,str(ROOT/'examples/synthetic/schematic_minimal/run_example.py')],cwd=ROOT,text=True,capture_output=True)
    assert r.returncode==0,r.stderr
    assert (ROOT/'examples/synthetic/schematic_minimal/output/diagram.drawio').exists()
