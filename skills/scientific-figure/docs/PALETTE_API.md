# Palette API — 1.1.x public candidate
No palette field preserves the legacy/default color path. Explicit `palette: auto`
selects the bundled `our_moderate_vivid` table; this opt-in differs from the
legacy default. Other palette values may be supplied by users with their own
provenance and license record; this public candidate does not redistribute
third-party numeric tables.
Profile fields: palette (auto or registered exact name), palette_family (default, vivid, restrained, high_contrast), color_strategy (categorical or focus_context). Focus mode also requires focus_identity matching a series identity. Unknown choices fail closed.
High contrast supports at most three categories; colors never cycle. Line and interval assignments prefer darker colors; white-background contrast below 3 produces a warning. Filled marks can use lighter colors. Semantic reference/event colors come from an independent registry.
Sequential entries are registry metadata, not additional supported renderers. Diverging remains experimental/pending. Only the existing three data archetypes are supported. User preferences are recorded, not a universal publication approval.
