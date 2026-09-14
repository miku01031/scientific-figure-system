# Contributing

## Development
Create a virtual environment and run `python -m pip install -r requirements-dev.txt`.
Run both skill test suites, then repeat integrity tests with `python -O` and
`PYTHONOPTIMIZE=1` where supported.

## Scientific integrity
Tests and examples must use synthetic data. Never weaken provenance, interval,
array-invariance, encoding-capacity, glyph, or vector fail-closed checks to make
a fixture pass. Human visual acceptance is separate from machine QA.

## Adding a palette or grammar
Add provenance and license information, deterministic capacity/semantic encoding
tests, grayscale/CVD evidence, and use/avoid documentation. A new schematic
grammar needs a schema fixture, native XML fixture, and explicit application
export status. Do not add a renderer merely by adding a registry row.

## Pull-request checklist
- no real research data, paper paths, or workstation-specific defaults
- normal, `-O`, and optimized integrity tests pass
- optional capability tests skip with an explicit reason when absent
- docs and dependency/license notices are updated
- private-path, secret, and packaging-hygiene scans pass
