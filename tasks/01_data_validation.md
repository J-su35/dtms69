# Task 01 : Data Validation

## Objective

Perform a comprehensive data quality assessment for both DTMS and AMI datasets before any comparison.

No analysis is allowed until data quality checks have passed.

---

# Input

DTMS dataset
(5-minute interval)

AMI Load Profile
(15-minute interval)

October–December 2025

---

# Expected Output

Produce

- validation_report.md
- cleaned_dtms.parquet
- cleaned_ami.parquet
- validation_summary.csv

---

# Validation Checklist

## 1. Dataset Overview

Report

- number of rows
- number of columns
- memory usage
- column names
- data types
- date range

---

## 2. Missing Values

Check

Missing rows

Missing timestamps

Missing kW

Missing kWh

Missing voltage

Missing current

Missing transformer ID

Missing meter ID

Report

Count

Percentage

Affected period

---

## 3. Duplicate Records

Detect

Duplicate timestamp

Duplicate meter

Duplicate transformer

Completely duplicated rows

Report

Number

Affected period

Recommendation

---

## 4. Timestamp Validation

Verify

Timestamp format

Timezone

Sorting

Continuous interval

Expected interval

DTMS

5 minutes

AMI

15 minutes

Detect

Gap

Overlap

Backward timestamp

Future timestamp

---

## 5. Interval Validation

Calculate

Actual interval

Compare with expected interval

Generate

Interval histogram

Interval statistics

---

## 6. Outlier Detection

Check

Negative kW

Negative kWh

Impossible voltage

Impossible current

Constant values

Large spikes

Sudden drop

Apply

IQR

Z-score

Rolling statistics

Flag every outlier.

Do NOT remove automatically.

---

## 7. Value Range Validation

Check

Voltage

Current

Power Factor

Frequency

kW

kWh

Transformer loading

Identify physically impossible values.

---

## 8. Data Completeness

For every day

Calculate

Expected samples

Actual samples

Completeness %

Generate heatmap.

---

## 9. Data Consistency

Verify

Meter always belongs to same transformer

Transformer ID consistency

Duplicate Meter ID

Duplicate Transformer ID

---

# Deliverables

Generate

validation_report.md

containing

Summary

Tables

Charts

Recommendations

and

overall data quality score

from 0–100.