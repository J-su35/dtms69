# DTMS vs AMI Analysis Agent

## Objective

This agent analyzes transformer-level DTMS data and customer-level AMI load profile data to evaluate how closely the DTMS measurements match the aggregated AMI measurements under the same transformer.

The goal is NOT simply comparing two datasets.

The goal is to quantify measurement consistency, identify discrepancies, explain possible causes, and produce engineering insights.

---

# Available Data

## 1. DTMS

Transformer monitoring system

Resolution:
- every 5 minutes

Contains variables such as

- Transformer ID
- Timestamp
- Voltage
- Current
- Power Factor
- Frequency
- kW
- kWh
- kVA
- kVAR
- etc.

---

## 2. AMI Load Profile

Smart Meter data

Resolution

- every 15 minutes

Contains

- Meter ID
- Transformer ID (or PEA_No)
- Timestamp
- kWh
- kW average
- Current
- Voltage
- Phase
- etc.

October 2025
November 2025
December 2025

---

# Primary Objective

Compare

DTMS

vs

Sum(AMI under the transformer)

for the same time period.

---

# Required Analysis Workflow

Always follow these steps.

## Step 1

Inspect datasets

Report

- shape
- columns
- data type
- missing values
- duplicated rows
- timestamp range

---

## Step 2

Validate timestamps

Check

- timezone
- timestamp consistency
- missing interval
- duplicated interval

---

## Step 3

Synchronize timestamps

DTMS = 5 minutes

AMI = 15 minutes

Aggregate DTMS into 15-minute intervals.

Preferred method

Average

for

- kW
- Current
- Voltage
- PF

Last value

for cumulative values if appropriate

Energy difference

for kWh.

Never compare

5-minute data

directly

against

15-minute data.

---

## Step 4

Aggregate AMI

For every timestamp

calculate

SUM of all AMI meters

under the transformer.

Generate

AMI_TOTAL

containing

Timestamp

Transformer

Sum_kW

Sum_kWh

Sum_Current

etc.

---

## Step 5

Merge datasets

Merge

DTMS_15min

with

AMI_TOTAL

using

Transformer ID

Timestamp

---

## Step 6

Calculate comparison metrics

For every timestamp compute

Difference

Absolute Difference

Percentage Error

Ratio

RMSE

MAE

MAPE

Correlation

R²

Bias

Maximum Error

Median Error

95 percentile error

---

## Step 7

Visualizations

Generate

Time Series

DTMS vs AMI

Difference Trend

Scatter Plot

DTMS vs AMI

Regression line

Histogram

Error Distribution

Daily Boxplot

Heatmap

Hour × Day error

Monthly comparison

---

## Step 8

Identify abnormal periods

Automatically detect

Large Difference

Missing AMI

Missing DTMS

Negative values

Sudden spikes

Constant values

Outliers

Flag every abnormal interval.

---

## Step 9

Engineering interpretation

Suggest possible causes such as

Communication loss

Clock mismatch

Meter missing

Transformer loss

Technical loss

Measurement error

CT/PT ratio issue

Meter replacement

AMI latency

Transformer auxiliary load

---

# Preferred Python Libraries

pandas

numpy

matplotlib

plotly

scipy

sklearn

statsmodels

---

# Coding Rules

Always

- write modular code
- create reusable functions
- avoid duplicated code
- explain assumptions
- print summary before plotting
- keep notebook reproducible

---

# Deliverables

Produce

1. Clean merged dataset

2. Statistical report

3. Visualization report

4. Error summary

5. Engineering conclusion

6. Recommended next investigation