"""Explicit QA policy. Unknown checks default to REVIEW."""
POLICY={
 'physical_size':('BLOCK','Publication dimensions are contractual.'),
 'raster_embedding':('BLOCK','Vector-native output forbids raster embedding.'),
 'clip_validity':('BLOCK','Broken clip references corrupt geometry.'),
 'scientific_DOM':('BLOCK','Scientific SVG primitives must remain identical.'),
 'missing_glyph':('BLOCK','Missing glyphs change communicated content.'),
 'encoding_uniqueness':('BLOCK','Distinct scientific identities require distinct encoding tuples.'),
 'artwork_edge':('REVIEW','Canvas-edge proximity requires review.'),
 'legend_overlap':('REVIEW','Legend overlap requires review.'),
 'marker_overlap':('REVIEW','Severe marker overlap can obscure data.'),
 'annotation_collision':('REVIEW','Annotation proximity requires review.'),
 'annotation_placement':('REVIEW','Unresolved bounded placement requires review.'),
 'panel_alignment':('REVIEW','Panel asymmetry may be intentional but requires review.'),
 'color_only_encoding':('REVIEW','Color-only differentiation requires review.'),
 'legend_label_overlap':('REVIEW','Legend/text overlap requires review.'),
 'legend_overflow':('REVIEW','Legend overflow requires review.'),
 'dense_marker_misuse':('REVIEW','Dense-series markers can obscure the signal and require review.'),
 'excessive_outer_whitespace':('INFO','Whitespace does not alter science; retained as a named informational exemption.'),
}
EXEMPTIONS={'excessive_outer_whitespace':'INFO: does not block technical output; human production review may still act.'}
def evaluate(checks):
 classified={k:{'severity':POLICY.get(k,('REVIEW','Unknown QA key defaults to review.'))[0],'reason':POLICY.get(k,('REVIEW','Unknown QA key defaults to review.'))[1],'result':v} for k,v in checks.items()}
 block=[k for k,v in classified.items() if v['severity']=='BLOCK' and v['result']!='PASS']
 review=[k for k,v in classified.items() if v['severity']=='REVIEW' and v['result']!='PASS']
 info=[k for k,v in classified.items() if v['severity']=='INFO' and v['result']!='PASS']
 unknown=[k for k in checks if k not in POLICY]
 return {'checks':classified,'block':block,'review':review,'info':info,'unknown_default_review':unknown,'exemptions':EXEMPTIONS}
