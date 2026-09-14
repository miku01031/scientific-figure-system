# README preview assets

These three PNGs are public-safe visual previews generated from this repository's own code and synthetic inputs.

- figure_gallery.png uses the current scientific-figure pipeline with the deterministic fixtures under examples/synthetic/readme_previews/figure_*.
- schematic_gallery.png uses the current scientific-schematic pipeline with the existing synthetic T1.json, T3.json, and T5.json specifications. The canonical source is native drawio XML; the local preview used draw.io Desktop 31.4.5 for application export.
- hero_preview.png is a montage of the same generated outputs. It only arranges, crops whitespace, labels, and scales panels; it does not change scientific geometry or semantic relationships.

All inputs are synthetic demonstrations, not scientific evidence. No third-party assets, real research data, screenshots, or manual scientific edits are included. draw.io Desktop and the configured publication runtime are optional local tools for regeneration; hosted core CI does not run Desktop E2E.

To regenerate locally, set SCIFIG_RUNTIME_ROOT and DRAWIO_EXECUTABLE to tools available on your machine, then run:

python examples/synthetic/readme_previews/run_previews.py
