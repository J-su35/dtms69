# Task 03 : Root Cause Analysis

## Objective

Investigate abnormal differences between DTMS and aggregated AMI measurements.

Identify the most probable engineering causes.

---

# Input

comparison_result.parquet

validation_report.md

---

# Trigger Condition

Analyze every period where

Absolute Error > Threshold

or

MAPE exceeds threshold

or

Difference persists for more than 1 hour.

---

# Investigation Workflow

## Step 1

Classify anomaly

Missing AMI

Missing DTMS

Sudden Spike

Sudden Drop

Flat Signal

Negative Power

Clock Shift

Communication Gap

High Variance

Persistent Bias

---

## Step 2

Analyze Temporal Pattern

Duration

Frequency

Hour of Day

Weekday

Weekend

Month

Holiday

---

## Step 3

Engineering Investigation

Evaluate possibility of

Transformer technical loss

Meter communication failure

AMI missing meters

Meter replacement

Clock synchronization issue

CT/PT ratio mismatch

Transformer overload

Phase imbalance

Reverse power

Solar generation

EV charging

Data aggregation bug

Database issue

---

## Step 4

Correlation Analysis

Compare

Voltage

Current

Power Factor

Frequency

Temperature (if available)

Loading

---

## Step 5

Assign Root Cause Probability

For every anomaly

Estimate

Very High

High

Medium

Low

Unknown

Provide reasoning.

---

## Step 6

Group Similar Cases

Cluster anomalies

by

Duration

Magnitude

Time

Shape

Frequency

Possible cause

---

## Step 7

Recommendation

Suggest

Field inspection

Meter inspection

Communication verification

CT/PT verification

Clock synchronization

Firmware check

Database validation

---

# Deliverables

Generate

root_cause_report.md

root_cause_summary.csv

anomaly_timeline.csv

root_cause_dashboard.html

---

# Final Report

For every abnormal event provide

Start Time

End Time

Duration

Maximum Error

Average Error

Likely Cause

Confidence

Recommended Action

Priority

High

Medium

Low
