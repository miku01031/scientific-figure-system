# Scientific Figure 1.1.x — public candidate

This candidate preserves the three supported renderers and the 1.1 palette API while providing portable runtime/font discovery, optimization-safe validation, encoding uniqueness, explicit QA policy, accessibility-preview labeling, dependency declarations and process-local Matplotlib state.

Core dependencies: NumPy, Matplotlib, jsonschema, Pillow, and PyYAML. CairoSVG/native Cairo is an optional publication-export capability and PyMuPDF is an optional PDF-QA capability; no dependency is installed automatically. Continuous registry entries do not enlarge supported renderer capability; diverging remains EXPERIMENTAL_PENDING.

No new palette fields retains the legacy visual path for inputs within the now-enforced encoding capacity. Correctness takes priority over the prior fail-open behavior above capacity. Runtime paths are configured explicitly or discovered; no workstation path is a shipped default. This candidate is not installed and is intended for independent review.
