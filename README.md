# Scientific Figure System

[English](README.md) | [中文](README_zh.md)

A small, evidence-preserving toolkit for creating publication-oriented scientific figures and editable technical schematics.

This private release candidate is for researchers who already have project code and results and want Codex to help rebuild figures without changing scientific values. It is not a universal plotting service and it does not replace scientific judgment.

All preview images in this repository use synthetic data or synthetic diagram specifications owned by this project. They are demonstrations, not scientific evidence.

## What this project does

The repository contains two separate Codex Skills:

- **scientific-figure** reads a scientific figure specification and produces vector data figures. Its current production-tested renderers are:
  - Dense time series (DENSE_TIMESERIES)
  - Discrete comparison (DISCRETE_COMPARISON)
  - Point/whisker intervals (ERRORBAR_POINTWHISKER)
- **scientific-schematic** reads an explicit semantic diagram specification and produces an editable native .drawio file. It registers nine semantic grammars for control diagrams, workflows, architectures, and related technical diagrams.

The simple rule is **data first, meaning first, style second**. The tools check that plotting and vector processing do not silently change protected values such as x/y arrays, interval endpoints, thresholds, or event positions. When the input is ambiguous or unsupported, the tools stop and explain the problem instead of guessing.

<a href="docs/readme_assets/chart_archetype_atlas.png"><img src="docs/readme_assets/chart_archetype_atlas.png" alt="Scientific chart archetype atlas" width="100%"></a>

The chart atlas is a reference for choosing a representation. It covers 49 explored archetypes, but it is not a claim that 49 production renderers exist. The three production-tested renderers are listed above. Click the image for the full-resolution atlas; family-level views are available in the asset folder.

<a href="docs/readme_assets/schematic_quality_overview.png"><img src="docs/readme_assets/schematic_quality_overview.png" alt="Synthetic scientific schematic examples" width="100%"></a>

This overview shows synthetic control, FDI/FTC, observer, and method diagrams generated during development. The editable source is native .drawio XML. It does not expand the nine-grammar support boundary.

## Quick Start — Recommended

The easiest workflow is: clone the repository, install the core dependencies, copy the two Skills into your Codex Skill directory, then open **your own research project** in Codex. You do not need to copy your research data into this repository.

### 1. Download the repository

~~~bash
git clone https://github.com/miku01031/scientific-figure-system.git
cd scientific-figure-system
~~~

While this repository is private, cloning requires permission to access it. Remove or update this note before a public release.

### 2. Install the core dependencies

Python 3.10 or 3.11 is recommended.

Windows PowerShell:

~~~powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements-core.txt
~~~

macOS/Linux:

~~~bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-core.txt
~~~

Core dependencies are enough for SVG scientific figures and native editable .drawio schematics. CairoSVG, PyMuPDF, and draw.io Desktop are not required for this first step.

### 3. Install the Codex Skills

The repository contains skills/scientific-figure and skills/scientific-schematic. Copy them to the local Codex Skill directory, then restart Codex so it discovers them.

Windows PowerShell:

~~~powershell
$skillRoot = "$env:USERPROFILE\.codex\skills"
New-Item -ItemType Directory -Force $skillRoot | Out-Null
Copy-Item ".\skills\scientific-figure" "$skillRoot\scientific-figure" -Recurse -Force
Copy-Item ".\skills\scientific-schematic" "$skillRoot\scientific-schematic" -Recurse -Force
~~~

macOS/Linux:

~~~bash
mkdir -p ~/.codex/skills
cp -R skills/scientific-figure ~/.codex/skills/
cp -R skills/scientific-schematic ~/.codex/skills/
~~~

Restart Codex after copying so the two Skills become discoverable.

### 4. Open your own project

Open the folder that contains your existing Python/MATLAB code, CSV/MAT/JSON/NPY files, and result folders in Codex. The scientific data does not need to be moved into this repository.

### 5. Ask Codex in one sentence

Copy this prompt into the project you want to work on:

> Use the scientific-figure Skill to inspect this project, find the existing result data and plotting code, and generate publication-oriented scientific figures. Preserve all scientific values and do not invent or modify data. Use the supported renderer and default visual system when possible. Save the reproducible plotting code/spec together with the SVG output.

If the project structure is clear, an even shorter prompt is:

> Use scientific-figure to improve the figures in this project.

Codex should ask before drawing when the scientific meaning, source provenance, interval definition, or supported chart type is unclear.

## Advanced Usage

The quick start above is enough for most first runs. The sections below cover existing-code migration, batch work, representation choices, schematic grammars, palettes, and review.

## Three common ways to use it

### Improve existing figures

If you already have MATLAB or Python plotting code:

> Use scientific-figure to inspect the existing plotting code in this project. Keep all underlying scientific values unchanged, but rebuild the figure using the repository's publication-oriented visual system. Do not replace any scientific calculation.

This is the recommended migration path for an existing result figure. The Skill changes figure construction and vector output, not scientific computation.

### Generate new figures from project results

> Inspect this project and find the result data used for the paper figures. For each figure, identify whether it matches a supported scientific-figure renderer. Generate the supported figures, preserve the source data and intervals, save reproducible code/spec files, and clearly report anything that is unsupported or needs my decision.

For a batch request:

> Inspect all plotting scripts and result figures in this project. Use scientific-figure for figures that match its supported production renderers. For unsupported figure types, do not call them validated scientific-figure output; explain the limitation and preserve the scientific results. Do not modify the calculations.

### Generate an editable scientific schematic

> Use scientific-schematic to inspect this project and create an editable technical diagram that explains the main method or system architecture. Do not invent scientific modules that are not supported by the project. Output an editable .drawio file.

For a diagram derived from code:

> Inspect the source code and documentation in this project and build a scientific-schematic diagram that summarizes the actual processing, control, or diagnosis pipeline. Before drawing, list the inferred modules and connections. If any relationship is uncertain, ask me instead of inventing it.

The schematic Skill requires semantic relationships and layout coordinates to be supplied by the specification. A grammar organizes a diagram; it is not automatic scientific understanding or an unrestricted layout engine.

## What can currently be generated

### Production-tested data figures

| User-friendly type | Code name | Typical use |
| --- | --- | --- |
| Dense time series | DENSE_TIMESERIES | Connected time-domain signals with at least 32 samples |
| Discrete comparison | DISCRETE_COMPARISON | Explicit categorical/discrete comparisons with up to 8 uniquely encoded series |
| Point/whisker interval | ERRORBAR_POINTWHISKER | Estimates with explicit lower and upper endpoints |

The renderer scope is fail-closed. Heatmaps, confusion matrices, arbitrary flowcharts, networks, 3D, radar, Sankey, and other unsupported types are not silently converted into one of these recipes. The 49-entry chart registry is reference and planning material; use it to discuss a possible representation, not to claim a production renderer.

### Schematic grammars

The current registry contains these nine semantic grammars:

- CONTROL_BLOCK_DIAGRAM — control loops and named signal paths
- ALGORITHM_DECISION_LOOP — iterative algorithms with a stopping decision
- STAGED_METHOD_PIPELINE — sequential method stages and intermediate objects
- BRANCH_MERGE_WORKFLOW — parallel branches that later merge
- OFFLINE_ONLINE_SWIMLANE — training/offline work and online deployment
- HIERARCHICAL_ARCHITECTURE — layered system interfaces
- DUAL_STREAM_FUSION — complementary data and model streams
- SEMANTIC_METHOD_OVERVIEW — method or model transformations
- EXPERIMENTAL_DATA_LIFECYCLE — acquisition, cleaning, analysis, and validation

The grammar does not invent topology. Codex or the user must provide the actual modules, connections, labels, and layout coordinates.

## Colors and visual style

The default bundled categorical palette is our_moderate_vivid. Most users should let the Skill choose colors automatically from the figure type and number of series.

You can use natural-language requests such as:

- “Use a restrained color scheme.”
- “Highlight Method A and keep the other methods neutral.”
- “Use color together with marker or line-style redundancy.”

The renderer still checks encoding uniqueness and accessibility; it will stop when a palette cannot distinguish the requested number of scientific identities. The public candidate does not bundle the internally evaluated Tol or Okabe–Ito numeric tables.

Some colors have semantic roles instead of representing a series: fault_event, threshold, reference, neutral, baseline, missing, and text. You normally do not need to choose their hex values yourself.

For difficult representations, the advisory registry may suggest:

- near-overlapping curves → a central absolute trend plus a spread summary;
- two endpoints with intervals and a denominator/count → a forest-style display with aligned side information;
- probability/interval results against a reference → a horizontal interval display with a reference line.

These are suggestions only. They never rewrite a real paper's scientific representation without author confirmation.

## Output formats

Core output:

- Data figures: SVG, with reproducible code/spec and QA records.
- Schematics: native editable .drawio XML.

SVG can be inspected or refined in Illustrator, Inkscape, or another vector editor. Do not change scientific values during manual polishing. For schematics, open the .drawio file in draw.io Desktop to move native nodes, edit labels, or adjust spacing.

Optional publication export:

~~~powershell
.venv\Scripts\python -m pip install -r requirements-publication.txt
~~~

or on macOS/Linux:

~~~bash
.venv/bin/python -m pip install -r requirements-publication.txt
~~~

PDF/PNG export also requires a platform-native Cairo library. Installing the Python CairoSVG package alone does not prove that native Cairo is available. PDF inspection and PDF-QA are a separate optional layer:

~~~powershell
.venv\Scripts\python -m pip install -r requirements-pdfqa.txt
~~~

See [installation notes](docs/INSTALLATION.md), [runtime distribution policy](docs/RUNTIME_DISTRIBUTION_POLICY.md), and [third-party notices](THIRD_PARTY_NOTICES.md).

## What you should expect Codex to return

A good assisted run normally returns:

1. the generated SVG or .drawio;
2. reproducible plotting code or a semantic specification;
3. a QA/capability result and any warnings;
4. PDF/PNG only when the optional publication layer is available.

Machine QA is a safety check, not a journal-acceptance decision. Inspect the figure at the intended physical size and confirm the caption, interpretation, and final scientific message yourself.

## When the system stops

A stop is intentional. Examples include:

- too many series for uniquely distinguishable encodings;
- an invalid or inverted interval;
- missing or mismatched source provenance;
- an unknown archetype or grammar;
- missing CJK glyphs or forbidden raster/vector content.

The system prefers to explain the problem rather than produce a plausible-looking figure with an unverified meaning.

## A short revision vocabulary

After a first pass, you can ask:

- “The legend covers the curve. Keep the data unchanged and re-layout the figure.”
- “Emphasize Method A and keep the other methods as neutral context.”
- “Do not change the curves; adjust only typography, spacing, and the legend.”
- “Make a version that is suitable for a single-column paper.”
- “Generate an editable .drawio version.”

## Manual use without Codex

Codex is the recommended workflow, but the repository also contains deterministic synthetic launchers:

~~~powershell
.venv\Scripts\python examples/synthetic/figure_minimal/run_example.py
.venv\Scripts\python examples/synthetic/schematic_minimal/run_example.py
~~~

The first writes an SVG under examples/synthetic/figure_minimal/output/ (or an explicitly named diagnostic SVG when optional publication export is unavailable). The second writes examples/synthetic/schematic_minimal/output/diagram.drawio. These examples use synthetic data and are not a substitute for preparing a provenance-backed specification from your own project.

For detailed prompts, troubleshooting, and project workflow, read [the full Codex usage guide](docs/CODEX_USAGE.md). Chinese users can read [the Chinese guide](docs/CODEX_USAGE_zh.md).

## Recommended workflow

1. Prepare or locate the scientific data and existing plotting code.
2. Ask Codex to inspect the project and state what it found.
3. Generate the figure or schematic.
4. Read the QA and capability result.
5. Inspect the output at its intended physical size.
6. Make and record any required human edits.
7. Use the reviewed result in the manuscript.

## Tested environments

Hosted core CI has passed on Windows, Ubuntu, and macOS with Python 3.10 and 3.11. The Python package range is defined in requirements-core.txt; Python and Matplotlib versions are separate constraints. Ubuntu integration also tests native Cairo publication export and the optional PyMuPDF PDF-QA layer.

Native .drawio XML generation is a core capability and does not require draw.io Desktop. Desktop export is optional and was locally tested with draw.io Desktop 31.4.5; hosted CI does not run Desktop E2E.

## Repository map

- skills/ — the two Codex Skills;
- registries/ — palette, chart-reference, representation-advisor, and grammar registries;
- schemas/ — small contracts used by the tools;
- examples/synthetic/ — deterministic demonstrations;
- tests/ — core and hygiene checks;
- docs/ — installation, review, runtime, and detailed usage notes.

## Author

Li Yingxi ([@miku01031](https://github.com/miku01031))

## Citation

If you use the renderer or schematic backend, cite this software using [CITATION.cff](CITATION.cff).

## License status

The license decision remains explicitly pending author confirmation. See [LICENSE_DECISION_REQUIRED.md](LICENSE_DECISION_REQUIRED.md).

For detailed usage and troubleshooting, see [docs/CODEX_USAGE.md](docs/CODEX_USAGE.md).
