from pathlib import Path
import hashlib,json,shutil,sys
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
sys.path.insert(0,str(REPO/'skills'/'scientific-figure'))
from src.pipeline import run
spec=json.loads((HERE/'spec.json').read_text(encoding='utf-8'))
source=HERE/'data.csv';spec['sources'][0]['sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
profile=json.loads((HERE/'profile.json').read_text(encoding='utf-8'));profile['source_root']=str(HERE)
out=HERE/'output'
if out.exists():shutil.rmtree(out)
result=run(spec,profile,out);print(json.dumps(result,ensure_ascii=False,indent=2))
