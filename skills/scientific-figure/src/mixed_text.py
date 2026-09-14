"""CJK/math segmented text, using native text/math vector backends at fixed pt."""
import re,math,copy
from matplotlib.text import Text
from matplotlib.font_manager import FontProperties
from matplotlib.ft2font import FT2Font
from matplotlib.mathtext import MathTextParser
CJK=re.compile(r'[\u2e80-\u9fff\uac00-\ud7af\uf900-\ufaff\uff00-\uffef\u3000-\u303f]')
MATH=re.compile(r'(\$(?:\\.|[^$])*\$)')
def mixed(s):return bool(CJK.search(s) and MATH.search(s))
def pieces(s,prop,fonts):
 for i,part in enumerate(MATH.split(s)):
  if not part:continue
  if i%2:
   fp=copy.copy(prop);fp.set_math_fontfamily('stix');yield part,fp,True,'math'
  else:
   runs=[]
   for ch in part:
    role='cjk' if CJK.match(ch) else 'latin'
    if runs and runs[-1][0]==role:runs[-1][1]+=ch
    else:runs.append([role,ch])
   for role,txt in runs:
    fp=copy.copy(prop);fp.set_file(fonts[role]['resolved_path']);yield txt,fp,False,role
class MixedRenderer:
 def __init__(self,base,fonts):self.base=base;self.fonts=fonts
 def __getattr__(self,k):return getattr(self.base,k)
 def get_text_width_height_descent(self,s,prop,ismath):
  if not mixed(s):return self.base.get_text_width_height_descent(s,prop,ismath)
  sizes=[self.base.get_text_width_height_descent(txt,fp,ism) for txt,fp,ism,role in pieces(s,prop,self.fonts)]
  return sum(v[0] for v in sizes),max(v[1]-v[2] for v in sizes)+max(v[2] for v in sizes),max(v[2] for v in sizes)
 def draw_text(self,gc,x,y,s,prop,angle,ismath=False,mtext=None):
  if not mixed(s):return self.base.draw_text(gc,x,y,s,prop,angle,ismath=ismath,mtext=mtext)
  advance=0;rad=math.radians(angle);sign=-1 if self.base.flipy() else 1
  for txt,fp,ism,role in pieces(s,prop,self.fonts):
   self.base.draw_text(gc,x+advance*math.cos(rad),y+sign*advance*math.sin(rad),txt,fp,angle,ismath=ism,mtext=None)
   advance+=self.base.get_text_width_height_descent(txt,fp,ism)[0]
class MixedTextMixin:
 def _proxy(self,r):return r if isinstance(r,MixedRenderer) else MixedRenderer(r,self._mixed_fonts)
 def _get_layout(self,renderer):return super()._get_layout(self._proxy(renderer))
 def draw(self,renderer):return super().draw(self._proxy(renderer))
_CLASSES={}
def install_and_preflight(fig,capture):
 # Force standard tick labels to exist without rendering the artwork.
 for ax in fig.axes:ax.get_xticklabels();ax.get_yticklabels()
 fonts=capture.fonts;maps={k:FT2Font(v['resolved_path']).get_charmap() for k,v in fonts.items() if v.get('resolved_path')};errors=[];records=[];mathusage=[];parser=MathTextParser('path')
 for artist in fig.findobj(Text):
  text=artist.get_text()
  if not text or not artist.get_visible():continue
  ismixed=mixed(text)
  if ismixed and not isinstance(artist,MixedTextMixin):
   cls=type(artist)
   if cls not in _CLASSES:_CLASSES[cls]=type('Mixed'+cls.__name__,(MixedTextMixin,cls),{})
   artist.__class__=_CLASSES[cls];artist._mixed_fonts=fonts
  resolved={};segments=[]
  for i,part in enumerate(MATH.split(text)):
   if not part:continue
   if i%2:
    if CJK.search(part):errors.append('missing glyph coverage: CJK inside math delimiters unsupported: '+part);continue
    try:
     # MathTextParser.parse is the public compatibility boundary.  Do not
     # inspect private parsed glyph tuples: their layout changed between
     # Matplotlib 3.10 and 3.11.  Font/glyph failures are still caught by the
     # renderer's normal text preflight and by the exported SVG/PDF gates.
     prop=copy.copy(artist.get_fontproperties());prop.set_math_fontfamily('stix');parser.parse(part,dpi=72,prop=prop)
     segments.append({'kind':'math','text':part,'api':'MathTextParser.parse'})
    except Exception as e:errors.append('Mathtext parse failure: '+str(e))
   else:
    for ch in part:
     if ch.isspace():continue
     roles=['cjk'] if ismixed and CJK.match(ch) else ['latin'] if ismixed else ['latin','cjk']
     role=next((r for r in roles if ord(ch) in maps[r]),None)
     if role is None:
      if CJK.match(ch) and not fonts.get('cjk',{}).get('available',False):errors.append('CJK_FONT_UNAVAILABLE')
      else:errors.append('missing glyph U+%04X in text %s'%(ord(ch),text))
     else:resolved[ch]=fonts[role]['resolved_path']
    segments.append({'kind':'plain','text':part})
  if '$' in text:mathusage.append({'text':text,'mixed_compositor':ismixed,'segments':segments})
  records.append({'text':text,'artist_type':type(artist).__name__,'resolved_plain_character_fonts':resolved,'mixed_compositor':ismixed})
 capture.preflight={'status':'FAIL' if errors else 'PASS','errors':list(dict.fromkeys(errors)),'checked_text_count':len(records),'texts':records};capture.mathtext=mathusage
 return capture.preflight
