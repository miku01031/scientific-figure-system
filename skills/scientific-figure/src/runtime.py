"""Portable CairoSVG discovery; no workstation path is a functional default."""
from pathlib import Path
import importlib, os, sys

def configure_cairosvg(profile=None):
    profile = profile or {}
    root_value = profile.get("runtime_root") or os.environ.get("SCIFIG_RUNTIME_ROOT")
    python_value = os.environ.get("CANDIDATE_CAIRO_PATH")
    native = None
    if root_value:
        root = Path(root_value)
        if not root.exists():
            raise ValueError("RUNTIME_CONFIG_INVALID: SCIFIG_RUNTIME_ROOT does not exist: " + str(root))
        py = root / "python"
        native = root / "native"
        if not py.is_dir() and not native.is_dir():
            raise ValueError("RUNTIME_CONFIG_INVALID: runtime root has no python/native directories: " + str(root))
        if py.is_dir() and str(py) not in sys.path:
            sys.path.insert(0, str(py))
    elif python_value and Path(python_value).is_dir():
        py = Path(python_value)
        if str(py) not in sys.path:
            sys.path.insert(0, str(py))
        sibling = py.parent / "native"
        native = sibling if sibling.is_dir() else None
    if native and hasattr(os, "add_dll_directory") and native.is_dir():
        try:
            os.add_dll_directory(str(native))
        except OSError:
            pass
    if native and native.is_dir():
        # cairocffi also consults the process PATH (not only AddDllDirectory)
        # on Windows.  Prepend the configured directory before importing it.
        os.environ["PATH"] = str(native) + os.pathsep + os.environ.get("PATH", "")
    try:
        module = importlib.import_module("cairosvg")
    except ModuleNotFoundError as exc:
        raise ValueError("CAIROSVG_PYTHON_PACKAGE_MISSING: install the CairoSVG Python package") from exc
    except (OSError, ImportError) as exc:
        raise ValueError("NATIVE_CAIRO_MISSING: CairoSVG is installed but native Cairo could not be loaded") from exc
    except Exception as exc:
        raise ValueError("RUNTIME_CONFIG_INVALID: CairoSVG import failed") from exc
    missing = [name for name in ("svg2pdf", "svg2png") if not hasattr(module, name)]
    if missing:
        raise ValueError("CAIROSVG_INCOMPLETE: missing " + ", ".join(missing))
    try:
        probe=b'<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"><path d="M0 0"/></svg>'
        module.svg2pdf(bytestring=probe); module.svg2png(bytestring=probe)
    except (OSError, ImportError) as exc:
        raise ValueError("NATIVE_CAIRO_MISSING: CairoSVG capability probe failed") from exc
    return module, {"available": True, "verification": "module-capability", "version": getattr(module, "__version__", None), "configured_root": root_value, "module_file": str(getattr(module, "__file__", ""))}
