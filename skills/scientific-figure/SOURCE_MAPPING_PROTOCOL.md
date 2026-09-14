# Agent-assisted source mapping protocol

Mapping is scientific preparation by an agent with source evidence, not a renderer inference feature.

1. Record every source absolute path and SHA-256 before reading or mapping.
2. Record each panel/series ID, exact CSV columns/row selectors or JSON pointers, x and y meanings, units, and validity masks.
3. Record interval endpoints and definition (CI/SD/other), confidence level and cohort/denominator from frozen metadata; do not recompute.
4. Record every threshold/event value and meaning. Preserve scientific axis ranges and categorical identity mappings. Existing display category offsets may be retained and explicitly identified; do not introduce new jitter.
5. Cross-check with the existing plotting script and source ledger by reading them; do not execute legacy main() or other potentially writing code.
6. If science, provenance, unit, missingness, interval or mapping is ambiguous: fail closed and ask. Do not resolve scientific uncertainty through visual guesses.
7. Never OCR a figure to guess scientific numbers, and never reverse-engineer scientific data from visual positions. Vector coordinates may verify an independently sourced mapping; they are not a source of numerical science.
8. Write MAPPING_LEDGER.json alongside the neutral spec. Include source path/hash, each series mapping, units, intervals, thresholds/events, and provenance checks. Reusing an approved exact spec records its path/hash and upstream chain.
9. Validate schema and source SHA before rendering; keep science, style config and renderer implementation separate.

NEVER MODIFY SCIENTIFIC DATA FOR VISUAL CLARITY. No simulation, fitting, scientific metric recomputation, smoothing or invention of missing data.


## Explicit display provenance and production width

For each series record semantic_meaning_source and display_label_source separately in MAPPING_LEDGER.json. Display priority: explicit label in current plotting code; frozen metadata/ledger display name; confirmed manuscript terminology; user-specified label. Record absolute path, SHA256 and locator. Put the display-label provenance alongside display_label in the neutral spec so runtime validation can verify the referenced file. Do not shorten or translate unilaterally. meaning remains the full scientific explanation; display_label is a source-backed representation, not a substitute scientific definition.

Panel label is optional and distinct from title. Preserve current manuscript terminology and units; never use a prior validation mapping as a production authority. For production width record actual current manuscript layout evidence (TeX point conversion uses 72.27 pt/in), or explicit user profile. Validation-only widths are NON_PRODUCTION_WIDTH. An existing artwork-size proxy requires review and is not a journal specification.

Declare multiple independent visual factors; more than eight discrete series is outside this RC's ordinary recipe. No arbitrary factorized-legend contract is accepted by this RC. Refuse rather than silently flattening the Cartesian product into a large ordinary legend.
