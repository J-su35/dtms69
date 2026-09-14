# Data validation report

## Result

**Data quality score: 55/100 (conditional).** The numeric profiles are nearly complete, but both supplied parquet exports have lost mandatory timestamp fields; DTMS also lacks a source transformer ID. Timestamps in all downstream outputs are reconstructed regular 15-minute calendars, not verified source timestamps. Input filenames say 2026, whereas the project brief and notebook evidence point to October–December 2025; this runner uses 2025.

## Overview

| dataset | rows | columns | memory_mb | missing_cells | duplicate_keys | duplicate_rows | start | end | expected_interval | negative_kw | numeric_columns |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DTMS | 8832.000 | 22.000 | 1.996 | 0.000 | 0.000 | 0.000 | 2025-10-01 00:00:00 | 2025-12-31 23:45:00 | 15 min (reconstructed) | 66.000 | Ia, Ib, Ic, KWH_A, KWH_B, KWH_C, KWH_TOT, PF_TOT, P_A, P_B, P_C, P_TOT, Q_A, Q_B, Q_C, Q_TOT, S_A, S_B, S_C, S_TOT |
| AMI | 173665.000 | 13.000 | 67.320 | 0.000 | 0.000 | 0.000 | 2025-10-01 00:00:00 | 2026-01-01 00:00:00 | 15 min (reconstructed) | 0.000 | KWH, kW average, AA, AB, AC, kW exp average |

## Findings and recommendations

- AMI's December profile for meter 6200031051 has 2,977 rows rather than the expected 2,976. With the source timestamp omitted, its position and whether it is a duplicate cannot be determined; it is retained and excluded from the study-period comparison.
- DTMS has 8,832 rows, exactly 92 days × 96 15-minute intervals, so it is already 15-minute data despite the brief describing 5-minute source data.
- No negative kW values were found. No source voltage or frequency columns are available for the requested physical-range checks.
- Re-export raw DTMS and AMI with timestamp, timezone, transformer mapping, and meter ID provenance before any operational conclusion. Validate source clock alignment rather than relying on reconstructed position.
