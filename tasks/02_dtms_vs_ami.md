# Task 02 : DTMS vs AMI Comparison

## Objective

Evaluate how closely DTMS measurements match the aggregated AMI measurements under the same transformer.

---

# Input

cleaned_dtms.parquet

cleaned_ami.parquet

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

Sum(Current)

Average Voltage (optional)

Number of active meters

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

---

## Step 6

Monthly Metrics

October

November

December

Generate comparison table.

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

comparison_result.parquet

comparison_statistics.csv

comparison_dashboard.html

comparison_report.md

---

# Expected Conclusions

Answer

How close are DTMS and AMI?

Which month is best?

Which transformer has highest error?

Is the error random or systematic?

Can DTMS represent AMI reliably?
