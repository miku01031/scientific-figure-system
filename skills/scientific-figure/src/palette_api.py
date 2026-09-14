"""Opt-in color strategy. No field -> untouched stable rendering path."""
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
KEYS=('palette','palette_family','color_strategy')
def luminance(hexcolor):
 v=[int(hexcolor[i:i+2],16)/255 for i in (1,3,5)];v=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in v];return sum(a*b for a,b in zip(v,[.2126,.7152,.0722]))
def resolve(profile,identities,mark='line'):
 if not any(k in profile for k in KEYS):return None
 reg=yaml.safe_load((ROOT/'config/palette_registry.yaml').read_text(encoding='utf8'));sem=yaml.safe_load((ROOT/'config/semantic_colors.yaml').read_text(encoding='utf8'))
 family=profile.get('palette_family','default');families={'default':'our_moderate_vivid'}
 if family not in families:raise ValueError('UNKNOWN_PALETTE_FAMILY')
 name=profile.get('palette','auto');name=families[family] if name=='auto' else name
 if name not in reg['categorical']:raise ValueError('UNKNOWN_CATEGORICAL_PALETTE')
 p=reg['categorical'][name];strategy=profile.get('color_strategy','categorical')
 if strategy not in ['categorical','focus_context']:raise ValueError('UNKNOWN_COLOR_STRATEGY')
 palette=p['colors'][:]
 # Light colors remain available for filled marks. Fine-line assignment prefers contrast.
 if mark in ['line','interval','small_marker']:palette=sorted(palette,key=luminance)
 if strategy=='categorical':
  if len(identities)>p['max_categories']:raise ValueError('NOT_APPLICABLE: palette category capacity exceeded; colors never recycled')
  colors=dict(zip(identities,palette))
 else:
  focus=profile.get('focus_identity')
  if focus not in identities:raise ValueError('FOCUS_IDENTITY_REQUIRED')
  colors={i:(palette[0] if i==focus else sem['baseline']) for i in identities}
 warnings=[{'identity':i,'color':c,'contrast_white':1.05/(luminance(c)+.05),'warning':'LOW_FINE_MARK_CONTRAST'} for i,c in colors.items() if mark in ['line','interval','small_marker'] and 1.05/(luminance(c)+.05)<3]
 return {'palette':name,'color_strategy':strategy,'mark':mark,'colors':colors,'semantic_colors':sem,'warnings':warnings}
