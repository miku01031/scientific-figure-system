# Scope and fail-closed rules

| Semantic family | Candidate support | Restrictions |
|---|---|---|
| DISCRETE_COMPARISON | Yes | 1–8 x values, up to 8 uniquely encoded series per figure, explicit linear ranges; single/multi panel |
| DENSE_TIMESERIES | Yes | Declared time domain, >=32 samples, connected scientific curves; event/threshold/invalid-region values frozen |
| ERRORBAR_POINTWHISKER | Yes | Explicit interval axis, lower/upper and definition; categorical or discrete domain |
| Heatmap/confusion matrix | No | No rendering |
| Schematic/flow/network | No | No rendering |
| 3D/radar/Sankey/montage | No | No rendering |
| Mixed/nonlinear/missing semantics | No | Stop for clarification or unsupported |

Domain declaration is required; sample count alone cannot reliably classify arbitrary science. Selector accuracy on prepared specs is different from autonomous image understanding. External adapters must not falsely label an unsupported figure.


Encoding capacity is checked from the final color/marker/linestyle/fill tuple. A selected palette or profile may have lower capacity; the renderer fails closed rather than recycling an encoding.
