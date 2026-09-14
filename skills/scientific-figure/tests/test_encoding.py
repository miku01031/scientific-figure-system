import json,sys,subprocess,os
from pathlib import Path
from src.pipeline import dump
from src.semantic_spec import ROOT

def test_utf8_text_io_is_locale_independent(tmp_path):
 text={"label":"中文 Δ 下标 root₁（配对）；数学 $\\Delta_{root}$"}
 p=tmp_path/'unicode.json';dump(p,text)
 assert json.loads(p.read_text(encoding='utf-8'))==text
 code="import json; from pathlib import Path; p=Path(__import__('sys').argv[1]); s=p.read_text(encoding='utf-8'); x=json.loads(s); p.with_suffix('.roundtrip.json').write_text(json.dumps(x,ensure_ascii=False),encoding='utf-8')"
 env=os.environ.copy();env.pop('PYTHONUTF8',None)
 r=subprocess.run([sys.executable,'-X','utf8=0','-c',code,str(p)],env=env,capture_output=True)
 assert r.returncode==0,r.stderr
 assert json.loads(p.with_suffix('.roundtrip.json').read_text(encoding='utf-8'))==text
