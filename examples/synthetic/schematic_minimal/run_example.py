from pathlib import Path
import json,shutil,sys
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
sys.path.insert(0,str(REPO/'skills'/'scientific-schematic'))
from src.pipeline import run
spec=json.loads((HERE/'spec.json').read_text(encoding='utf-8'))
out=HERE/'output'
if out.exists():shutil.rmtree(out)
result=run(spec,out,{'target_width_mm':145,'style':'JOURNAL_MINIMAL','require_application_export':False})
print(json.dumps(result,ensure_ascii=False,indent=2))
