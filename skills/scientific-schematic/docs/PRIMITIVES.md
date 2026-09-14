# Semantic primitives

Every primitive declares `representation_class`. `SCIENTIFIC_DATA` means the visible content is supplied explicitly by the semantic spec. The equation primitive is SCIENTIFIC_DATA and requires `scientific_content.equation_text`; missing text fails closed. The renderer never supplies a default equation.

`ICONIC_NON_DATA` primitives are schematic symbols, not measurements or scientific evidence. Waveform, probability, matrix, graph/model, dataset and artifact use abstract geometry without axes, ticks, scales or numerical labels. They must not be described as data figures or quantitative results. The diagram notice/caption must disclose demonstration-only status when synthetic examples are used.

Aliases remain small_graph/network→graph, model_artifact→artifact, residual→waveform and feature_vector→matrix. `mini_plot` remains unsupported and fails closed.
