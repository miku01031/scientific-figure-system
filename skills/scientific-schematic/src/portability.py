"""Cross-machine discovery for optional draw.io and CairoSVG."""
from pathlib import Path
import json, os, shutil, subprocess, sys, importlib
def _configured_executable(profile):
    profile=profile or {}
    explicit=profile.get('drawio_executable') or os.environ.get('DRAWIO_EXECUTABLE')
    if explicit:return Path(explicit),'explicit'
    config=os.environ.get('DRAWIO_CONFIG')
    if config and Path(config).is_file():
        try:
            value=json.loads(Path(config).read_text(encoding='utf-8')).get('drawio_executable')
            if value:return Path(value),'config'
        except (OSError,ValueError):pass
    return None,None
def discover_drawio(profile=None):
    explicit,source=_configured_executable(profile);candidates=[]
    if explicit:candidates.append((explicit,source))
    for name in ('drawio','drawio.exe','draw.io','draw.io.exe','diagrams.net','diagrams.net.exe'):
        found=shutil.which(name)
        if found:candidates.append((Path(found),'PATH'))
    roots=[os.environ.get('ProgramFiles'),os.environ.get('ProgramFiles(x86)'),os.environ.get('LOCALAPPDATA')]
    for root in filter(None,roots):
        base=Path(root);candidates.extend(((base/'draw.io'/'draw.io.exe','standard'),(base/'diagrams.net'/'diagrams.net.exe','standard'),(base/'draw.io'/'bin'/'draw.io.exe','standard')))
    if sys.platform=='darwin': candidates.append((Path('/Applications/draw.io.app/Contents/MacOS/draw.io'),'standard'))
    seen=set()
    for path,src in candidates:
        try:path=path.expanduser().resolve()
        except OSError:continue
        if str(path).lower() in seen or not path.is_file():continue
        seen.add(str(path).lower());version=None
        try:
            r=subprocess.run([str(path),'--version','--disable-gpu','--no-sandbox'],capture_output=True,timeout=5,creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0);version=(r.stdout or r.stderr).decode('utf-8','replace').strip()[:200] or None
        except Exception:pass
        return {'available':True,'path':str(path),'source':src,'version':version}
    return {'available':False,'path':None,'source':None,'version':None,'reason':'DRAWIO_NOT_FOUND','message':'draw.io Desktop not discovered; native .drawio generation remains available'}
def configure_cairosvg(profile=None):
    profile=profile or {};root_value=profile.get('runtime_root') or os.environ.get('SCIFIG_RUNTIME_ROOT');native=None
    if root_value:
        root=Path(root_value)
        if not root.exists():raise ValueError('RUNTIME_CONFIG_INVALID: SCIFIG_RUNTIME_ROOT does not exist: '+str(root))
        py=root/'python';native=root/'native'
        if not py.is_dir() and not native.is_dir():raise ValueError('RUNTIME_CONFIG_INVALID: runtime root has no python/native directories: '+str(root))
        if py.is_dir() and str(py) not in sys.path:sys.path.insert(0,str(py))
    if native and hasattr(os,'add_dll_directory') and native.is_dir():
        try:os.add_dll_directory(str(native))
        except OSError:pass
    if native and native.is_dir():os.environ['PATH']=str(native)+os.pathsep+os.environ.get('PATH','')
    try:module=importlib.import_module('cairosvg')
    except ModuleNotFoundError as exc:raise ValueError('CAIROSVG_PYTHON_PACKAGE_MISSING: install the CairoSVG Python package') from exc
    except (OSError,ImportError) as exc:raise ValueError('NATIVE_CAIRO_MISSING: CairoSVG is installed but native Cairo could not be loaded') from exc
    except Exception as exc:raise ValueError('RUNTIME_CONFIG_INVALID: CairoSVG import failed') from exc
    missing=[x for x in ('svg2pdf','svg2png') if not hasattr(module,x)]
    if missing:raise ValueError('CAIROSVG_INCOMPLETE: '+','.join(missing))
    try:
        probe=b'<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"><path d="M0 0"/></svg>';module.svg2pdf(bytestring=probe);module.svg2png(bytestring=probe)
    except (OSError,ImportError) as exc:raise ValueError('NATIVE_CAIRO_MISSING: CairoSVG capability probe failed') from exc
    return module,{'available':True,'verification':'module-capability','version':getattr(module,'__version__',None),'configured_root':root_value,'module_file':str(getattr(module,'__file__',''))}
