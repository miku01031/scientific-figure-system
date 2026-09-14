# Codex Usage Guide

This guide assumes that your research project already contains code and results.

## 1. Install once

From the repository root:

~~~bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\python -m pip install -r requirements-core.txt
# macOS/Linux:       .venv/bin/python -m pip install -r requirements-core.txt
~~~

Copy the two Skill folders into the Codex Skill directory and restart Codex.

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

The Skill folders do not need to be copied into your research project.

## 2. Open the project you want to improve

In Codex, open the directory containing the actual work: plotting scripts, simulation results, CSV/MAT/JSON/NPY files, and figure output folders. Do not copy research data into this repository just to use the Skill.

Start with:

> Use the scientific-figure Skill to inspect this project, find the existing result data and plotting code, and generate publication-oriented scientific figures. Preserve all scientific values and do not invent or modify data. Use the supported renderer and default visual system when possible. Save the reproducible plotting code/spec together with the SVG output.

A shorter first request is:

> Use scientific-figure to improve the figures in this project.

Codex should inspect the project before drawing. If units, interval meanings, provenance, event positions, or topology are unclear, it should ask you.

## 3. Three practical modes

### Mode 1: improve existing figures

> Use scientific-figure to inspect the existing plotting code in this project. Keep all underlying scientific values unchanged, but rebuild the figure using the repository's publication-oriented visual system. Do not replace any scientific calculation.

Expected result: a source-backed figure specification, reproducible plotting code, SVG, and QA/capability records. The renderer may stop if the existing figure does not fit a tested archetype.

### Mode 2: generate figures from results

> Inspect this project and find the result data used for the paper figures. For each figure, identify whether it matches a supported scientific-figure renderer. Generate the supported figures, preserve the source data and intervals, save reproducible code/spec files, and clearly report anything that is unsupported or needs my decision.

For all figure scripts:

> Inspect all plotting scripts and result figures in this project. Use scientific-figure for figures that match its supported production renderers. For unsupported figure types, do not pretend they are validated scientific-figure output; provide a clear limitation and preserve the scientific results. Do not modify the calculations.

### Mode 3: generate an editable schematic

> Use scientific-schematic to inspect this project and create an editable technical diagram that explains the main method or system architecture. Do not invent scientific modules that are not supported by the project. Output an editable .drawio file.

For code-derived diagrams:

> Inspect the source code and documentation in this project and build a scientific-schematic diagram that summarizes the actual processing, control, or diagnosis pipeline. Before drawing, list the inferred modules and connections. If any relationship is uncertain, ask me instead of inventing it.

The schematic Skill writes native .drawio XML without draw.io Desktop. Desktop is optional for opening, editing, or exporting the native file.

## 4. Choosing a representation

The three tested data renderers are:

- DENSE_TIMESERIES — connected time-domain signals with at least 32 samples;
- DISCRETE_COMPARISON — explicit discrete/categorical comparisons, up to 8 uniquely encoded series;
- ERRORBAR_POINTWHISKER — estimates with explicit lower and upper interval endpoints.

The chart atlas and chart registry are reference material. If a desired chart is outside these three renderers, ask Codex to explain the limitation instead of silently forcing it into a supported recipe.

The representation advisor has three advisory rules:

- near-overlapping curves → central absolute trend plus a spread summary;
- two endpoints with intervals and denominator/count → forest-style display with aligned side information;
- probability/interval result against a reference → horizontal interval display with a reference line.

These rules suggest a visual question to discuss. They do not automatically rewrite a real scientific representation.

## 5. Colors

The public candidate bundles our_moderate_vivid as its default categorical palette. Usually you can omit color parameters:

> Use the default palette system and keep redundant marker/line-style encoding where it improves distinguishability.

Other useful requests:

> Use a restrained color scheme.

> Highlight Method A and keep the other methods neutral.

> Use color plus marker or line-style redundancy.

Semantic colors currently include fault_event, threshold, reference, neutral, baseline, missing, and text. The Skill keeps these roles separate from categorical series colors. If a requested palette cannot encode distinct scientific identities safely, it stops instead of recycling colors.

The public candidate does not bundle the internal Tol or Okabe–Ito numeric tables.

## 6. Schematic grammar hints

Ask for a grammar only when it matches the scientific relationships:

- CONTROL_BLOCK_DIAGRAM: control/plant feedback with named signals;
- ALGORITHM_DECISION_LOOP: an iterative method with a stop decision;
- STAGED_METHOD_PIPELINE: sequential method stages;
- BRANCH_MERGE_WORKFLOW: parallel branches that merge;
- OFFLINE_ONLINE_SWIMLANE: offline training and online inference;
- HIERARCHICAL_ARCHITECTURE: layered system interfaces;
- DUAL_STREAM_FUSION: complementary data/model evidence;
- SEMANTIC_METHOD_OVERVIEW: method/model transformations;
- EXPERIMENTAL_DATA_LIFECYCLE: acquisition through validation.

A grammar describes organization; it does not infer an arbitrary scientific topology. The semantic specification must provide the modules, relationships, labels, and positions.

## 7. Outputs and manual review

Expect the run to preserve:

- scientific arrays and interval endpoints;
- source/provenance records;
- the generated SVG or .drawio;
- reproducible code/spec;
- QA and capability results.

Inspect the result at the intended physical size. Machine QA does not decide journal likeness, scientific interpretation, or whether a figure should replace an existing manuscript figure.

Safe follow-up prompts include:

- “Keep the data unchanged and move the legend away from the curve.”
- “Emphasize Method A and keep the others as neutral context.”
- “Adjust only typography, spacing, and panel balance.”
- “Make a single-column version if the scientific labels remain readable.”
- “Give me the editable .drawio source.”

## 8. Manual launchers without Codex

From the repository root:

~~~powershell
.venv\Scripts\python examples/synthetic/figure_minimal/run_example.py
.venv\Scripts\python examples/synthetic/schematic_minimal/run_example.py
~~~

The figure launcher writes an SVG under examples/synthetic/figure_minimal/output/. If optional publication conversion is unavailable it writes an explicitly named diagnostic SVG and reports the capability. The schematic launcher writes examples/synthetic/schematic_minimal/output/diagram.drawio.

## 9. Optional capabilities and troubleshooting

**SVG works but PDF/PNG is unavailable.** Core SVG output does not require CairoSVG. Install requirements-publication.txt and a platform-native Cairo library. A Python CairoSVG import alone is not enough.

**PDF inspection is unavailable.** Install requirements-pdfqa.txt. PyMuPDF belongs to the PDF-QA layer, not core.

**draw.io is not installed.** Native .drawio generation still works. Install draw.io Desktop only if you need application editing or export.

**The figure type is unsupported.** Ask Codex to explain which renderer boundary was reached. Do not relabel an ordinary plot as validated scientific-figure output.

**There are too many series.** Reduce the number of distinct scientific identities only if that is scientifically justified, or ask for a review. Do not recycle colors silently.

**CJK text is missing.** Install/configure an available CJK font and rerun the glyph preflight. Do not accept a figure with missing glyphs.

**The Skill is not detected.** Check that the folders are exactly ~/.codex/skills/scientific-figure and ~/.codex/skills/scientific-schematic, then restart Codex.

For installation details, see docs/INSTALLATION.md and docs/RUNTIME_DISTRIBUTION_POLICY.md.

## 10. What this workflow does not do

It does not guarantee journal acceptance, infer missing scientific values, replace a manuscript figure automatically, support every chart type, or invent a control/diagnosis topology. Human review remains required.
