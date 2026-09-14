from pathlib import Path
import re

ROOT = Path(__file__).parents[1]
PRIVATE_PATTERNS = [re.compile(r"[A-Za-z]:[\\/]Research(?:[\\/]|$)", re.I),
                   re.compile(r"[A-Za-z]:[\\/]代码(?:[\\/]|$)"),
                   re.compile(r"[A-Za-z]:[\\/]drawio(?:[\\/]|$)", re.I),
                   re.compile(r"[A-Za-z]:[\\/]Users[\\/][^\\/]+(?:[\\/]|$)", re.I)]
IGNORED_DIRS={"__pycache__",".pytest_cache",".git","coverage",".venv","venv"}

def test_public_tree_hygiene():
    bad=[]
    for p in ROOT.rglob('*'):
        if any(part in IGNORED_DIRS for part in p.parts): continue
        if p.is_file() and (p.suffix in {'.pyc','.pyo'} or p.name in {'Thumbs.db','.DS_Store'}):bad.append(str(p))
        if p.is_file() and p.stat().st_size>25*1024*1024:bad.append(str(p))
        if p.is_file() and p.suffix.lower() in {'.md','.yaml','.yml','.json','.py','.toml','.cff','.txt'}:
            text=p.read_text(encoding='utf-8',errors='ignore')
            for pat in PRIVATE_PATTERNS:
                if pat.search(text):bad.append(f'{p}: private path pattern {pat.pattern}')
    assert not bad,bad
