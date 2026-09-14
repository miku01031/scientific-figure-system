"""Scoped diagnostics with portable font fallback chains."""
import json, logging, os, warnings, re
from pathlib import Path
from matplotlib.font_manager import findfont, FontProperties
from matplotlib.ft2font import FT2Font
PATTERN=re.compile(r'(?i)(glyph.*(?:missing|not have)|(?:missing|not have).*glyph|substitut|dummy symbol|font.*fallback|falling back|font family.*not found|findfont.*not found)')
FONT_REQUIREMENTS={
 'latin':['Times New Roman','Liberation Serif','DejaVu Serif'],
 'cjk':['SimSun','Microsoft YaHei','Noto Serif CJK SC','Noto Sans CJK SC','Source Han Serif SC','Source Han Sans SC','WenQuanYi Zen Hei'],
 'math':['STIXGeneral','STIX Two Text','DejaVu Serif']}
class Capture(logging.Handler):
 def __init__(self):
  super().__init__(logging.WARNING);self.messages=[];self.extra_warnings=[];self.preflight={};self.fonts={};self.mathtext=[];self.state=[]
 def emit(self,record):self.messages.append({'logger':record.name,'level':record.levelname,'message':record.getMessage()})
 def __enter__(self):
  loggers=[logging.getLogger('matplotlib')]+[v for k,v in list(logging.Logger.manager.loggerDict.items()) if k.startswith('matplotlib.') and isinstance(v,logging.Logger)]
  for lg in loggers:
   self.state.append((lg,lg.level,lg.disabled));lg.addHandler(self);lg.setLevel(logging.WARNING if lg.level==0 or lg.level>logging.WARNING else lg.level);lg.disabled=False
  self.wctx=warnings.catch_warnings(record=True);self.pywarnings=self.wctx.__enter__();warnings.simplefilter('always');return self
 def __exit__(self,*exc):
  self.wctx.__exit__(*exc)
  for lg,level,disabled in self.state:lg.removeHandler(self);lg.setLevel(level);lg.disabled=disabled
 def report(self):
  py=list(dict.fromkeys([str(w.message) for w in self.pywarnings]+self.extra_warnings));logs=list({(m['logger'],m['level'],m['message']):m for m in self.messages}.values());allmessages=py+[m['message'] for m in logs]+self.preflight.get('errors',[])
  missing=list(dict.fromkeys(m for m in allmessages if PATTERN.search(m)));failed=bool(missing or self.preflight.get('status')=='FAIL' or any(m['level']=='ERROR' for m in logs))
  return {'status':'FAIL' if failed else 'PASS','python_warnings':py,'matplotlib_log_warnings':logs,'missing_glyph_messages':missing,'missing_glyph_count':len(missing),'font_resolution':self.fonts,'mathtext_usage':self.mathtext,'glyph_preflight':self.preflight,'logging_handlers_restored':True}
def _configured():
 p=os.environ.get('SCIFIG_FONT_CONFIG')
 if p and Path(p).is_file():return json.loads(Path(p).read_text(encoding='utf-8'))
 p=Path(__file__).resolve().parents[1]/'config'/'font_fallbacks.json'
 return json.loads(p.read_text(encoding='utf-8'))
def resolve_fonts():
 cfg=_configured();result={}
 for role,key in [('latin','latin_serif'),('cjk','cjk_serif'),('math','math')]:
  # Keep the public configuration as the normal source while preserving the
  # small FONT_REQUIREMENTS override used by diagnostics/tests to simulate a
  # missing font without editing the shipped config.
  choices=FONT_REQUIREMENTS[role] if role=='cjk' and isinstance(FONT_REQUIREMENTS[role],str) else cfg.get(key,FONT_REQUIREMENTS[role]);choices=[choices] if isinstance(choices,str) else choices
  resolved=None
  for family in choices:
   try:
    path=findfont(FontProperties(family=family),fallback_to_default=False);ft=FT2Font(path);resolved={'requested':family,'resolved_path':path,'resolved_family':ft.family_name,'postscript_name':ft.postscript_name,'charmap_size':len(ft.get_charmap())};break
   except Exception:pass
  if resolved is None:
   if role=='cjk':result[role]={'available':False,'error':'CJK_FONT_UNAVAILABLE','attempted':choices}
   else:raise ValueError('FONT_UNAVAILABLE: '+role+' attempted '+repr(choices))
  else:result[role]={'available':True,**resolved}
 return result
