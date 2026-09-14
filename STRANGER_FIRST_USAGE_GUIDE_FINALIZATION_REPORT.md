# Stranger-First Usage Guide Finalization Report

## Scope

This change updates the bilingual README and adds detailed Codex usage guides. Renderer code, QA logic, schemas, palette values, grammar definitions, requirements, CI capability, license, citation metadata, and scientific contracts were not modified.

## Documentation checks

| Check | Result |
| --- | --- |
| English README complete | PASS |
| Chinese README complete | PASS |
| Quick Start / Advanced Usage split | PASS |
| Clone and core-install commands documented | PASS |
| Codex Skill installation documented for Windows and macOS/Linux | PASS |
| One-line simple prompt | PASS |
| Existing MATLAB/Python plotting-code workflow | PASS |
| Batch figure workflow | PASS |
| Three production-tested renderers | PASS |
| 49-entry atlas boundary | PASS |
| Nine schematic grammars | PASS |
| Default palette from the public registry | PASS |
| Semantic colors from the public registry | PASS |
| Manual/no-Codex mode | PASS |
| Detailed English and Chinese guides | PASS |

The public registry was checked before writing the text. It contains only the bundled our_moderate_vivid categorical table; the semantic color roles documented here are fault_event, threshold, reference, neutral, missing, baseline, and text. The documented production renderer names match the current supported-archetype contract.

## Local validation

- README and guide relative-link scan: PASS.
- Required-file and asset existence scan: PASS.
- Internal development wording and private-path scan for the changed documentation: PASS.
- Git whitespace check: PASS.
- Core tests: 6 passed.
- python -O tests: 6 passed.
- PYTHONOPTIMIZE=1 tests: 6 passed.
- Figure launcher with a temporary venv: exit 0; core SVG generated. The local environment reported the expected optional publication-export-unavailable status because CairoSVG is not installed.
- Schematic launcher with a temporary venv: exit 0; native diagram.drawio generated without draw.io Desktop.
- No functional source file was changed.

The default pytest temporary directory on this workstation is permission-restricted, so validation used an explicitly writable basetemp. The single cache warning is environmental and does not affect the six passing tests.

## Hosted CI

Documentation commit: 0359b3229ea714c1bbf6e46ec0c261c7c0f88cc2

Workflow: https://github.com/miku01031/scientific-figure-system/actions/runs/34844983678

Result: success.

Passed jobs included:

- Windows core, Python 3.10 and 3.11;
- Ubuntu core, Python 3.10 and 3.11;
- macOS core, Python 3.10 and 3.11;
- optimized-core;
- schema-and-examples;
- capability-aware-core;
- Ubuntu publication integration;
- Ubuntu PDF-QA integration.

The draw.io Desktop E2E job remained optional and skipped, as documented by the repository capability model.

## Files

Changed:

- README.md
- README_zh.md

Added:

- docs/CODEX_USAGE.md
- docs/CODEX_USAGE_zh.md
- this report

## Repository state

The repository remains private. No renderer, QA, schema, palette, grammar, requirements, CI, license, citation, or scientific files were changed.

## Status

STRANGER_FIRST_USAGE_GUIDE = PASS
