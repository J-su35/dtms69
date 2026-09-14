# Final engineering report

## Executive summary

The conditional comparison across 8,814 reconstructed 15-minute intervals reports MAE **2.17 kW**, RMSE **2.77 kW**, MAPE **23.27%**, bias **0.80 kW**, correlation **0.905**, and R² **0.542**. These are analytical indicators, not an operational acceptance result, because source timestamps and ID mapping are missing.

## Direct answers

1. DTMS is not yet sufficiently evidenced as consistent with aggregated AMI for operational replacement: provenance prevents a valid clock-aligned test.
2. Average measurement error is 23.27% MAPE (2.17 kW MAE), conditional on reconstruction.
3. Only one transformer is supplied, so no cross-transformer ranking is possible.
4. 67-018400 requires investigation because its identifier was inferred rather than supplied and 493 persistent discrepancy events were flagged.
5. The most credible discrepancy causes are aggregation/mapping mismatch, clock alignment, and CT/PT configuration; technical loss cannot be quantified from these fields.
6. DTMS may be a validation source only after raw timestamp/mapping recovery and a repeat comparison.
7. First priority: re-export timestamped source data with timezone and explicit transformer/meter mapping; then verify clocks and CT/PT ratios for persistent events.

## Monthly metrics

| period | intervals | mae_kw | rmse_kw | mape_pct | bias_kw | median_error_kw | p95_abs_error_kw | max_error_kw | min_error_kw | correlation | r2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2025-10 | 2976.000 | 1.765 | 2.213 | 17.013 | 0.820 | 1.118 | 4.180 | 9.895 | -12.126 | 0.936 | 0.737 |
| 2025-11 | 2862.000 | 2.024 | 2.531 | 22.424 | 0.805 | 1.284 | 4.994 | 10.605 | -10.395 | 0.910 | 0.587 |
| 2025-12 | 2976.000 | 2.724 | 3.407 | 30.354 | 0.775 | 1.206 | 6.543 | 18.992 | -10.040 | 0.880 | 0.218 |

## Research limitations and future work

Re-run this pipeline from raw 5-minute DTMS records, aggregate them to 15 minutes, include voltage/frequency/phase data, and quantify transformer loss after mapping validation.
