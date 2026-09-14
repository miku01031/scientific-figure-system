---
name: scientific-figure
description: Hardening candidate for provenance-preserving production of three frozen scientific figure archetypes; optimization-safe validation, unique encodings, explicit QA gates, and no installation.
---

# Scientific figure 1.1.x — public candidate

This 1.1.x public candidate supports three archetypes only and is intended for portability and independent review. Consult `docs/SUPPORTED_ARCHETYPES.md`. It is not installed by this package and must not replace manuscript figures.

## First checks

1. Identify read-only frozen data, existing figure, source ledger, and authorized new output directory. Never execute a legacy plotting script merely to discover inputs: it may overwrite a manuscript path.
2. Require `target_width_mm`, `target_language`, `panel_mode`, and `output_context`. A width copied from a current artwork is an explicit experimental context, not a journal requirement. Ask if width or scientific scope is unknown; do not invent journal/thesis dimensions.
3. Inspect existing Python and dependencies. Do not install anything automatically. NumPy, Matplotlib, jsonschema, Pillow and PyYAML support core work; PyMuPDF and CairoSVG/native Cairo are optional publication-QA/export capabilities and are probed at runtime.
4. Prepare neutral JSON from a frozen plot-ready source. Source preparation may require human review and is not counted as automatic science extraction. Keep raw source SHA and explicit mapping ledger. Stop and ask about ambiguous series meaning, units, uncertainty definition, missing values, provenance, interval endpoints, or axis constraints. Do not infer missing scientific values.

## Separate three layers

- Scientific semantics: `schema/figure_semantic_spec.schema.json`: values, endpoints, ranges, units, meanings, event/threshold positions, validity, and caption information.
- Visual choices: `config/` and a separate output profile. Never put colors, fonts, Artist/Axes objects, SVG groups or renderer transforms into the scientific spec.
- Implementation: `src/`. Its layout manifest is a renderer artifact, not a semantic input.

## Safety rule

**NEVER MODIFY SCIENTIFIC DATA FOR VISUAL CLARITY**

Never jitter scientific x, offset scientific y, smooth, interpolate, decimate, change an interval or threshold, move an alarm, invent missing data, or exaggerate tiny differences through opportunistic range changes. A scientifically authorized transformation would be a separately reviewed upstream task; it is not a default behavior of this Skill. Preserve all samples, including validity flags. No simulation, training, metric recomputation, Git changes or legacy-script execution.

## Selection and deterministic choices

Run the selector on declared semantics; never coerce an unknown chart into a familiar recipe. DISCRETE_COMPARISON supports 1–8 x points and up to 8 uniquely encoded series per figure; DENSE_TIMESERIES requires time-domain connected series, at least 32 samples; ERRORBAR_POINTWHISKER requires explicit frozen lower/upper endpoints. Unsupported/mixed/unrecognized figures return `SUPPORTED_ARCHETYPE=false`, `UNSUPPORTED`, and no artwork. Heatmaps, confusion matrices, schematics, flows, networks, 3D, radar and image montages are unsupported.

Within known semantics, automatically choose conservative colors, line patterns, small marker shapes, absolute typography, panel grid and measured outer containment. Dense series have no regular sample markers; isolated frozen event markers are allowed. Interval orientation is scientific, not an aesthetic choice. Long explanations go to CAPTION.txt. See `docs/DESIGN_LANGUAGE.md` for defaults, ranges and exceptions.

## Execute

From this candidate directory, with an existing environment:

```text
python -B -m src.pipeline --spec /absolute/spec.json --profile /absolute/profile.json --out /absolute/new_empty_output
```

Set `MPLCONFIGDIR`, TMP/TEMP inside authorized staging. For optional publication export, use normal CairoSVG discovery or configure `SCIFIG_RUNTIME_ROOT`; the runtime probe reports whether native Cairo is actually loadable. Never guess or repair system dependencies automatically. `README.md` describes current evidence and portability limits.

The pipeline validates schema and source SHA, renders all scientific values, checks Artist coordinate readback and ranges, produces an SVG, checks primitive fingerprints, then exports PDF and 300 dpi PNG. Scientific FAIL forbids final export. Other QA failures permit diagnostic artwork but forbid claiming technical success. Preserve RESULT.json, SCIENTIFIC_INVARIANCE.json, QA.json, layout record, caption and vector log.

## Conservative vector safety

Only SVG produced by this candidate with an exact expected primitive snapshot is eligible. Current implemented operations are measured vertical viewport crop, physical metadata normalization and verified single-panel external legend rigid translation. Scientific path/use/clip attributes, scientific group subtrees and ancestor transforms must remain identical. Unknown/altered structure returns `SKIPPED_UNSAFE_STRUCTURE`. Do not guess transforms, align data independently of axes or rewrite paths. Horizontal metadata does not authorize stretching. Panel rigid alignment remains a future hook, not an implemented capability.

## Review and stop

Read QA PASS/WARN/FAIL, including source/arrays/units/endpoints, physical size, raster/clip/font, layout overlap, marker overlap and grayscale/CVD approximation. WARN is not a clearance certificate. For first-pass evaluation, freeze candidate source hashes and run all targets before viewing output; do not change parameters after preview. Report preparation, failures and manual work separately from rendering. A technical pass is not an aesthetic approval or evidence of 90% end-to-end automation. Do not rank aesthetics or replace existing figures without the requested external review.

## Assisted-production and glyph gates

Read SOURCE_MAPPING_PROTOCOL.md before source preparation and generate MAPPING_LEDGER.json. This is agent-assisted production with verified neutral inputs, not autonomous interpretation of arbitrary research files.

Rendering attaches a scoped handler for Matplotlib WARNING/ERROR and captures Python warnings. It restores previous handlers/levels/disabled states afterward; never use global basicConfig or rely only on stdout grep. Save RENDER_DIAGNOSTICS.json (warnings, logs, missing glyph messages, actual resolved fonts and mathtext usage) and GLYPH_PREFLIGHT.json.

Preflight inspects title, axis/tick labels, legends and annotations. For CJK mixed with mathtext, use the segmented vector compositor with the configured CJK and Latin fallback chains and separate STIX math; measured baseline composition preserves nominal font size. Ordinary non-mixed text keeps the approved rendering path. No translation, symbol deletion, whole-figure rasterization or font installation. Missing required CJK fonts -> CJK_FONT_UNAVAILABLE/FAIL_CLOSED_FONT_ENVIRONMENT.

Glyph preflight FAIL, missing glyph logs or renderer ERROR means vector FAIL and no final PDF/PNG export; a diagnostic SVG may remain. Never claim technical success from scientific hashes alone. Review known layout warnings separately; this candidate does not redesign legends or recipes.


## Production contracts (1.1.x candidate)

Skill never automatically replaces formal artwork. TECHNICAL_STATUS and PRODUCTION_CLEARANCE are separate. Technical correctness is not layout clearance or aesthetic approval. There is no READY_FOR_AUTO_REPLACE state.

Keep complete `meaning`; use optional `display_label` only with `display_label_source` containing absolute path, SHA256 and a locator. Validate the source hash. Mapping ledger records `semantic_meaning_source` and `display_label_source`. A source-backed display label must retain identity; never invent abbreviations or OCR a PNG. No reliable short label means use meaning and request review if it overflows.

Optional `panel_label` is separate from `title`. Old specs remain valid. Profiles default to legacy `legend_scope=panel`. With `auto` (or requested `figure`), identical identity/label sets AND actual rendered encodings share one legend. Incompatible panels fall back to panel legends. Auto production layout has a bounded, measured horizontal margin containment pass at unchanged physical width (at most three iterations, at most 5% correction each); it changes renderer placement only, not tokens or vector-polish geometry. Large overflow is left for review.

Declare independent `visual_factors` in panel semantics. Discrete panels over eight series fail closed as ENCODING_CAPACITY_EXCEEDED. Panels with multiple independent factors fail closed as COMPLEX_FACTORIAL_DISCRETE_REQUIRES_DEDICATED_RECIPE. This RC has no validator/renderer for a factorized-legend contract; do not bypass the gate with an unverified contract or hide factors.

Opt in via `annotation_placement=bounded`: seven deterministic text-only positions; marker and interval geometry never move. Unresolved placement/annotation collision, artwork edge, legend overflow or unresolved overlap means REVIEW_REQUIRED. The no-field legacy path retains original annotation placement.

Require current-manuscript or user-explicit production width evidence; do not reuse a larger validation width. Profile `width_authority`: current_manuscript, user_explicit, current_artwork_proxy, or validation. Missing/validation authority gives NON_PRODUCTION_WIDTH and review, even when technical rendering passes. The proxy category also requires review. Record the exact authority path/hash/locator in the mapping ledger and preserve the specified physical width.

Run tests with `python -m pytest tests`; explicit UTF-8 file I/O does not require UTF-8 mode; use writable staging for temporary files and cache. No package installation or permanent environment change is performed by this Skill.

## Opt-in color API (1.1.x candidate)
No new palette fields means exact legacy behavior. Do not add palette=auto to an old invocation. Explicit new API: palette, palette_family and color_strategy in the visual profile; see docs/PALETTE_API.md. The supported renderer list remains exactly three. Chart/advisor registries are references, not executable capabilities. This public candidate is not installed.
