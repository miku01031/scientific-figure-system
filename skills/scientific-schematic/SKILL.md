---
name: scientific-schematic
description: Public candidate for explicit semantic scientific diagrams using native draw.io cells and optional application export. Supports nine registered grammars; rejects unknown grammar and requires supplied scientific topology and layout.
---
# Scientific schematic 0.1.x — public candidate
This candidate is not installed and awaits independent review. Never replace manuscript artwork without author authorization.
Read config/grammar_registry.yaml and validate schema/diagram_semantic_spec.schema.json. Canonical input is a semantic JSON spec plus the native .drawio document, never an embedded full-diagram SVG.
Run `python -m src.pipeline --spec diagram_semantic_spec.json --out NEW_OUTPUT_DIRECTORY` from this directory. Never execute research simulation code. The output directory must be empty. Native XML generation does not require draw.io or Cairo; optional application/PDF/PNG capabilities are reported explicitly.
Use explicit source/target relationships, supplied coordinates and scientifically authorized labels. Unknown grammar, primitive, style or unsupported size fails closed. This package does not infer scientific topology or invent a layout.
Default JOURNAL_MINIMAL; optional JOURNAL_FUNCTIONAL_COLOR uses restrained functional fills. Default 145 mm; 90 mm requires explicit single_column_authority and an algorithm/staged profile.
Publication path: native .drawio → draw.io application SVG → metadata-only normalizer → optional CairoSVG/native-Cairo PDF/PNG. See docs/EXPORT_CONTRACT.md. Require native node/edge/text/group preservation, no foreignObject or raster, exact physical size and no missing text when the application/export capability is available. Review QA.json: structural/technical PASS does not clear geometric warnings or imply human visual acceptance.
Primitive capabilities and reserved interfaces are described in docs/PRIMITIVES.md. No Visio dependency. Installation does not authorize manuscript replacement.
