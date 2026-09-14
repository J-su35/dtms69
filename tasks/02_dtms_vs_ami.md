# Task 02 : DTMS vs AMI Comparison

## Objective

Evaluate how closely DTMS measurements match the aggregated AMI measurements under the same transformer.

---

# Input

cleaned_dtms.parquet

cleaned_ami.parquet, produced from the merged output of
`notebook/merge_LP.ipynb`. Do not use the separate monthly LP parquet files.

## Required Analysis Scenarios

Run and export all results separately for these scenarios:

1. **S1 — Three observed months:** October–December 2025 using the merged
   AMI data as observed.
2. **S2 — Three months with December profile replacement:** use the same
   data as S1 except replace the December records for PEA_No `6200031084`
   with its October–November median profile. Create the profile separately
   for every 15-minute time-of-day slot (96 slots) and every measure used in
   the comparison. Apply the matching slot value to each December date,
   preserve December timestamps and meter ID, and label all substituted rows
   with `ami_profile_imputed = True`. Do not use December values to calculate
   this profile.
3. **S3 — Two observed months:** October–November 2025 only; exclude all
   December DTMS and AMI observations.

Report a row count, matched-interval count, active-meter count, and data
completeness for every scenario. Never combine scenario results in a single
metric without a `scenario_id` column.

---

# Workflow

## Step 1

Aggregate DTMS

5 min

→

15 min

Rules

Average

kW

Voltage

Current

PF

Energy difference

for cumulative kWh

---

## Step 2

Aggregate AMI

Group

Transformer

Timestamp

Calculate

Sum(kW)

Sum(kWh)

Sum(kW_net)

Sum(Current)

Average Voltage (optional)

Number of active meters

Use `kW_net = kW average - kW exp average` after validating the source
sign convention. Preserve separate import and export totals where available.

---

## Step 3

Merge

Join

Transformer

Timestamp

Inner Join

Report unmatched records.

---

## Step 4

Calculate Error Metrics

For every timestamp

Difference

Absolute Difference

Percentage Difference

Ratio

Bias

Calculate these measures separately for kW and kWh. kW is an interval power
comparison; do not sum kW across time. For kWh, compare DTMS interval energy
(the difference of valid cumulative DTMS kWh readings) with summed AMI
interval `KWH`. Also provide daily and monthly kWh totals and their
differences. If AMI export energy is unavailable, label the kWh comparison
as **import-energy versus DTMS net/cumulative energy**, rather than claiming
it is a net-energy comparison.

---

## Step 5

Daily Metrics

MAE

RMSE

MAPE

Median Error

Correlation

R²

95 percentile error

Maximum Error

Minimum Error

Calculate the full metric set for both kW and kWh. Exclude zero or near-zero
reference energy intervals from MAPE and report the excluded count.

---

## Step 6

Monthly Metrics

October

November

December

Generate comparison table.

Generate one table per `scenario_id`, with rows for each included month and
an overall row.

---

## Step 7

Visualization

Generate

Time Series

Scatter Plot

Regression

Residual Plot

Histogram

Boxplot

Daily Trend

Monthly Trend

Heatmap

Error by Hour

Error by Day

Daily kWh comparison (DTMS versus AMI)

Cumulative kWh comparison

---

## Step 8

Threshold Evaluation

Classify

Excellent

Good

Warning

Critical

Example

Absolute Error

<2%

2–5%

5–10%

>10%

---

## Step 9

Export

comparison_result.parquet (must include `scenario_id`, kW fields, kWh fields,
and `ami_profile_imputed`)

comparison_statistics.csv

comparison_dashboard.html

comparison_report.md

comparison_statistics_by_scenario.csv

comparison_result_s1.parquet

comparison_result_s2.parquet

comparison_result_s3.parquet

---

# Expected Conclusions

Answer

How close are DTMS and AMI?

How close are DTMS and AMI for kWh?

Which month is best?

Which transformer has highest error?

Is the error random or systematic?

Can DTMS represent AMI reliably?

How does the conclusion change across S1, S2, and S3?
