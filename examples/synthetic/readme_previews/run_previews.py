from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


FIGURE_CASES = [
    ("figure_dense", "Dense time series"),
    ("figure_discrete", "Discrete comparison"),
    ("figure_errorbar", "Point / whisker interval"),
]
SCHEMATIC_CASES = [
    ("T1.json", "Control loop"),
    ("T3.json", "Method pipeline"),
    ("T5.json", "Offline / online"),
]


def font(size: int, bold: bool = False):
    names = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for name in names:
        if Path(name).exists():
            return ImageFont.truetype(name, size)
    return ImageFont.load_default()


def run_json(command, *, cwd, env):
    proc = subprocess.run(
        command,
        cwd=str(cwd),
        env=env,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            "Pipeline failed:\n"
            + " ".join(command)
            + "\nSTDOUT:\n"
            + proc.stdout[-4000:]
            + "\nSTDERR:\n"
            + proc.stderr[-4000:]
        )
    try:
        return json.loads(proc.stdout.strip())
    except Exception as exc:
        raise RuntimeError(f"Pipeline returned no JSON: {proc.stdout[-4000:]}") from exc


def fit_image(source: Path, box):
    image = Image.open(source).convert("RGB")
    mask = image.convert("L").point(lambda value: 255 if value < 245 else 0)
    bbox = mask.getbbox()
    if bbox:
        left, top, right, bottom = bbox
        pad = max(12, min(image.width, image.height) // 50)
        image = image.crop((max(0, left - pad), max(0, top - pad), min(image.width, right + pad), min(image.height, bottom + pad)))
    image.thumbnail((box[2], box[3]), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (box[2], box[3]), "white")
    x = (box[2] - image.width) // 2
    y = (box[3] - image.height) // 2
    canvas.paste(image, (x, y))
    return canvas


def add_panel(canvas, source, title, x, y, width, height):
    draw = ImageDraw.Draw(canvas)
    border = (215, 220, 225)
    draw.rounded_rectangle((x, y, x + width, y + height), radius=10, fill="white", outline=border, width=2)
    title_font = font(26, bold=True)
    draw.text((x + 22, y + 14), title, fill=(36, 32, 35), font=title_font)
    image = fit_image(source, (x + 18, y + 62, width - 36, height - 78))
    canvas.paste(image, (x + 18, y + 62))


def make_gallery(paths, labels, output, heading):
    width, height = 1800, 700
    canvas = Image.new("RGB", (width, height), (250, 251, 252))
    draw = ImageDraw.Draw(canvas)
    draw.text((50, 28), heading, fill=(36, 32, 35), font=font(36, bold=True))
    margin = 50
    gap = 28
    panel_width = (width - 2 * margin - 2 * gap) // 3
    panel_y = 92
    panel_h = 550
    for i, (path, label) in enumerate(zip(paths, labels)):
        add_panel(canvas, path, label, margin + i * (panel_width + gap), panel_y, panel_width, panel_h)
    canvas.save(output, format="PNG", optimize=True)


def make_hero(figure_paths, schematic_paths, output):
    width, height = 2000, 620
    canvas = Image.new("RGB", (width, height), (250, 251, 252))
    draw = ImageDraw.Draw(canvas)
    draw.text((56, 32), "Scientific figures", fill=(36, 32, 35), font=font(36, bold=True))
    draw.text((1036, 32), "Scientific schematics", fill=(36, 32, 35), font=font(36, bold=True))
    divider = (224, 227, 230)
    draw.line((1000, 30, 1000, height - 24), fill=divider, width=2)
    labels = ["Dense time series", "Discrete comparison", "Point / whisker interval"]
    for i, path in enumerate(figure_paths):
        add_panel(canvas, path, labels[i], 42 + i * 310, 98, 286, 480)
    labels = ["Control loop", "Method pipeline", "Offline / online"]
    for i, path in enumerate(schematic_paths):
        add_panel(canvas, path, labels[i], 1042 + i * 310, 98, 286, 480)
    canvas.save(output, format="PNG", optimize=True)


def main():
    parser = argparse.ArgumentParser(description="Generate README preview assets from synthetic repository fixtures.")
    parser.add_argument("--assets", type=Path, default=None)
    parser.add_argument("--runtime-root", default=os.environ.get("SCIFIG_RUNTIME_ROOT", ""))
    parser.add_argument("--drawio", default=os.environ.get("DRAWIO_EXECUTABLE", ""))
    args = parser.parse_args()

    repo = Path(__file__).resolve().parents[3]
    assets = args.assets or (repo / "docs" / "readme_assets")
    assets.mkdir(parents=True, exist_ok=True)
    if not args.runtime_root:
        raise SystemExit("SCIFIG_RUNTIME_ROOT is required for reproducible publication preview generation")
    if not args.drawio:
        raise SystemExit("DRAWIO_EXECUTABLE is required for schematic application-export previews")
    runtime_root = Path(args.runtime_root)
    drawio = Path(args.drawio)
    if not runtime_root.exists():
        raise SystemExit(f"Configured runtime root does not exist: {runtime_root}")
    if not drawio.exists():
        raise SystemExit(f"Configured draw.io executable does not exist: {drawio}")

    figure_skill = repo / "skills" / "scientific-figure"
    schematic_skill = repo / "skills" / "scientific-schematic"
    fixture_root = repo / "examples" / "synthetic" / "readme_previews"
    schematic_root = schematic_skill / "examples"
    figure_paths = []
    schematic_paths = []

    with tempfile.TemporaryDirectory(prefix="readme-preview-") as temp:
        temp_root = Path(temp)
        for case, _ in FIGURE_CASES:
            case_dir = fixture_root / case
            spec = case_dir / "spec.json"
            profile = json.loads((case_dir / "profile.json").read_text(encoding="utf-8"))
            profile["source_root"] = str(case_dir)
            profile["runtime_root"] = str(runtime_root)
            profile_path = temp_root / f"{case}-profile.json"
            profile_path.write_text(json.dumps(profile, indent=2), encoding="utf-8")
            out = temp_root / case
            env = os.environ.copy()
            env["PYTHONPATH"] = str(figure_skill)
            env["MPLCONFIGDIR"] = str(temp_root / f"{case}-mplconfig")
            result = run_json(
                [sys.executable, "-m", "src.pipeline", "--spec", str(spec), "--profile", str(profile_path), "--out", str(out)],
                cwd=figure_skill,
                env=env,
            )
            if result.get("scientific") != "PASS" or result.get("vector") != "PASS" or not (out / "figure.png").exists():
                raise RuntimeError(f"Figure preview did not pass the current pipeline: {case}: {result}")
            target = temp_root / f"{case}.png"
            shutil.copy2(out / "figure.png", target)
            figure_paths.append(target)

        schematic_profile = {
            "target_width_mm": 145,
            "style": "JOURNAL_MINIMAL",
            "require_application_export": True,
            "runtime_root": str(runtime_root),
            "drawio_executable": str(drawio),
        }
        for filename, _ in SCHEMATIC_CASES:
            spec = schematic_root / filename
            profile_path = temp_root / f"{Path(filename).stem}-schematic-profile.json"
            profile_path.write_text(json.dumps(schematic_profile, indent=2), encoding="utf-8")
            out = temp_root / Path(filename).stem
            env = os.environ.copy()
            env["PYTHONPATH"] = str(schematic_skill)
            result = run_json(
                [sys.executable, "-m", "src.pipeline", "--spec", str(spec), "--profile", str(profile_path), "--out", str(out)],
                cwd=schematic_skill,
                env=env,
            )
            if not (out / "figure.png").exists() or not (out / "diagram.drawio").exists():
                raise RuntimeError(f"Schematic preview did not produce required artifacts: {filename}: {result}")
            target = temp_root / f"{Path(filename).stem}.png"
            shutil.copy2(out / "figure.png", target)
            schematic_paths.append(target)

        assets.mkdir(parents=True, exist_ok=True)
        figure_gallery = assets / "figure_gallery.png"
        schematic_gallery = assets / "schematic_gallery.png"
        hero = assets / "hero_preview.png"
        make_gallery(figure_paths, [x[1] for x in FIGURE_CASES], figure_gallery, "Production-tested scientific figures")
        make_gallery(schematic_paths, [x[1] for x in SCHEMATIC_CASES], schematic_gallery, "Representative editable schematics")
        make_hero(figure_paths, schematic_paths, hero)

    print(json.dumps({
        "assets": [str(assets / name) for name in ["hero_preview.png", "figure_gallery.png", "schematic_gallery.png"]],
        "figure_cases": [x[0] for x in FIGURE_CASES],
        "schematic_cases": [x[0] for x in SCHEMATIC_CASES],
        "synthetic": True,
        "manual_scientific_edit": False,
    }, indent=2))


if __name__ == "__main__":
    main()
