# Task 05: Streamlit Dashboard Generation

## Objective

Build an interactive Streamlit dashboard for analyzing and comparing:

- DTMS transformer measurements
- Aggregated AMI measurements under the transformer
- Error metrics
- Data quality issues
- Abnormal events
- Root cause analysis results

The dashboard must also support the three analysis scenarios from Task 02 and
must display kW and kWh results as distinct quantities.

The dashboard must support interactive:

- Zoom
- Pan
- Hover
- Range selection
- Date filtering
- Reset axes
- Chart export
- Data filtering
- CSV download

Use Streamlit for the application and Plotly for interactive charts.

---

# Primary Users

The dashboard is intended for:

- Power system engineers
- Smart Grid engineers
- Data analysts
- Researchers
- Utility management

The interface should be understandable without requiring users to inspect Python code.

---

# Input Files

Read the following files from the `reports/` directory when available:

```text
reports/
├── cleaned_dtms.parquet
├── cleaned_ami.parquet
├── comparison_result.parquet
├── comparison_statistics.csv
├── anomaly_timeline.csv
├── root_cause_summary.csv
├── validation_summary.csv
├── comparison_report.md
├── root_cause_report.md
└── final_report.md
```

Not all optional files may exist.

The application must:

1. Detect which files are available.
2. Load available files safely.
3. Show a warning for missing optional files.
4. Stop with a clear error message only when a required file is missing.

Required file:

```text
reports/comparison_result.parquet
```

---

# Expected Project Structure

Generate the following structure:

```text
project/
├── app.py
├── dashboard/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── filters.py
│   ├── metrics.py
│   ├── charts.py
│   ├── pages.py
│   └── utils.py
├── reports/
├── requirements-dashboard.txt
└── README-dashboard.md
```

A simpler structure is acceptable for a small implementation, but avoid placing all logic in one large `app.py`.

---

# Technology Requirements

Use:

- Python
- Streamlit
- pandas
- NumPy
- Plotly Express
- Plotly Graph Objects
- PyArrow

Optional:

- SciPy
- scikit-learn
- statsmodels

Do not use Matplotlib for the primary dashboard charts.

---

# Dashboard Execution

The dashboard must run with:

```bash
streamlit run app.py
```

Default local URL:

```text
http://localhost:8501
```

Create `requirements-dashboard.txt` containing at least:

```text
streamlit
pandas
numpy
plotly
pyarrow
```

---

# General Dashboard Requirements

## Interactive Chart Requirements

Every time-series chart must support:

- Zoom by dragging over the chart
- Pan mode
- Scroll zoom
- Double-click to reset axes
- Hover tooltip
- Range slider where appropriate
- Plotly mode bar
- Download chart as PNG
- Autoscale
- Select and zoom to a date range

Use Plotly configuration similar to:

```python
plotly_config = {
    "scrollZoom": True,
    "displaylogo": False,
    "responsive": True,
    "modeBarButtonsToAdd": [
        "drawline",
        "drawrect",
        "eraseshape"
    ],
    "toImageButtonOptions": {
        "format": "png",
        "filename": "dtms_ami_chart",
        "scale": 2
    }
}
```

Render charts using:

```python
st.plotly_chart(
    fig,
    use_container_width=True,
    config=plotly_config
)
```

For time-series charts, provide a user control for:

```text
Interaction mode:
- Zoom
- Pan
```

Set the Plotly drag mode according to the selected option.

---

# Application Layout

Use a wide layout:

```python
st.set_page_config(
    page_title="DTMS vs AMI Dashboard",
    page_icon="⚡",
    layout="wide"
)
```

The dashboard should contain the following pages:

1. Overview
2. Data Quality
3. DTMS vs AMI Comparison
4. Error Analysis
5. Anomaly Explorer
6. Root Cause Analysis
7. Data Explorer
8. Methodology and Notes

Use Streamlit multipage navigation or sidebar page selection.

---

# Global Sidebar Filters

The sidebar must contain filters that affect the relevant charts and tables.

## Required Filters

- Transformer ID
- Start date
- End date
- Month
- Day of week
- Hour of day
- Error severity
- Anomaly type
- Root cause category
- Analysis scenario: S1, S2, or S3

If the dataset contains only one transformer, automatically select it and avoid forcing the user to choose.

## Optional Filters

When available:

- Phase
- Meter ID
- Solar customer flag
- Community battery status
- AMI data completeness
- Weekday or weekend
- Positive or negative power flow

Provide a button:

```text
Reset filters
```

---

# Page 1: Overview

## Objective

Provide a high-level summary of the DTMS versus AMI analysis.

## KPI Cards

Display:

- Analysis period
- Number of transformers
- Number of AMI meters
- Number of matched intervals
- AMI completeness
- DTMS completeness
- Overall MAE
- Overall RMSE
- Overall MAPE or sMAPE
- Overall kWh MAE, RMSE, MAPE/sMAPE, and bias
- Overall bias
- Correlation
- R²
- Number of abnormal events
- Total abnormal duration

Use clear units:

- kW
- kWh
- %
- hours
- number of intervals

## Main Charts

Display:

1. DTMS versus aggregated AMI time series
2. Difference or residual time series
3. Monthly error comparison
4. Error severity distribution

Add a date-range selector above the main time-series chart.

---

# Page 2: Data Quality

## Objective

Show the results of Task 01.

## Required Sections

### Data Completeness

Show:

- Expected records
- Actual records
- Missing records
- Completeness percentage

Break down by:

- Dataset
- Month
- Day
- Transformer
- Meter where applicable

### Missing Data Heatmap

Create a heatmap showing:

- X-axis: date
- Y-axis: meter or dataset
- Color value: completeness percentage or missing interval count

### Duplicate Summary

Show:

- Completely duplicated rows
- Duplicate timestamps
- Duplicate meter-timestamp records
- Duplicate transformer-timestamp records

### Interval Analysis

Show distributions of actual intervals:

- DTMS interval distribution
- AMI interval distribution

Clearly indicate expected intervals:

- DTMS: 5 minutes
- AMI: 15 minutes

### Outlier Summary

Show counts by category:

- Negative power
- Voltage outlier
- Current outlier
- Power factor outlier
- Flat signal
- Sudden spike
- Sudden drop

Do not imply that every flagged point is an incorrect measurement.

---

# Page 3: DTMS vs AMI Comparison

## Objective

Allow detailed comparison of DTMS and aggregated AMI values.

## Main Time-Series Chart

Display at least:

- DTMS kW
- Aggregated AMI net kW
- Optional AMI import kW
- Optional AMI export kW
- Optional community battery power

Provide a clear metric selector for **Power (kW)** and **Energy (kWh)**.
For kWh, display interval energy, daily energy, and cumulative-energy charts;
do not relabel power charts as energy charts.

Use a Plotly line chart.

Requirements:

- Zoom
- Pan
- Hover
- Range slider
- Selectable aggregation level

Provide aggregation options:

```text
15 minutes
30 minutes
Hourly
Daily
```

Aggregation rules must be physically correct.

For power:

```text
Use mean over the interval
```

For interval energy:

```text
Use sum over the interval
```

For cumulative energy:

```text
Use the difference between valid readings
```

Never sum kW values across time.

## Scatter Plot

Create a scatter plot:

```text
X-axis: Aggregated AMI kW
Y-axis: DTMS kW
```

Include:

- Identity line y = x
- Regression line
- R²
- Correlation
- Number of observations

Allow coloring points by:

- Month
- Hour
- Error severity
- Power flow direction

## Daily Energy Comparison

Compare:

- DTMS daily energy
- Aggregated AMI daily net energy

Show:

- Grouped bar chart
- Daily difference
- Daily percentage error

Add a scenario comparison table that reports S1, S2, and S3 side-by-side.
For S2, show an information banner: December PEA_No 6200031084 values are
modelled from the October–November median 15-minute profile and are not
observed readings.

---

# Page 4: Error Analysis

## Objective

Examine the magnitude, direction, and temporal behavior of discrepancies.

## Metrics

Calculate for the currently filtered data:

- Mean Error
- Bias
- MAE
- RMSE
- Normalized RMSE
- MAPE
- sMAPE
- WAPE
- Median Absolute Error
- P90 absolute error
- P95 absolute error
- Maximum absolute error
- Correlation
- R²

For kWh, calculate and label the same applicable metrics independently from
kW metrics.

## Important MAPE Rule

Do not calculate conventional MAPE for intervals where the denominator is zero or near zero.

Use a configurable threshold:

```text
Minimum AMI reference power for MAPE
```

Default:

```text
0.1 kW
```

Display:

- Number of intervals excluded from MAPE
- Percentage of intervals excluded
- sMAPE and WAPE as more stable alternatives

## Charts

Create:

1. Error time series
2. Absolute error time series
3. Percentage error time series
4. Error histogram
5. Error boxplot by month
6. Error boxplot by hour
7. Hour-of-day versus day-of-week heatmap
8. Rolling MAE
9. Rolling bias

Allow rolling window selection:

```text
4 intervals
8 intervals
1 day
7 days
```

---

# Page 5: Anomaly Explorer

## Objective

Allow users to inspect periods where DTMS and AMI differ abnormally.

## Anomaly Table

Load `anomaly_timeline.csv` when available.

Display:

- Event ID
- Transformer ID
- Start time
- End time
- Duration
- Maximum error
- Mean error
- Error percentage
- Anomaly type
- Severity
- Suspected cause
- Confidence
- Recommended action

Allow:

- Sorting
- Filtering
- Searching
- CSV download

## Event Drill-Down

When the user selects an event, show a chart with:

- At least 1 hour before the event
- Entire anomaly period
- At least 1 hour after the event

Plot:

- DTMS kW
- Aggregated AMI kW
- Difference
- Optional voltage
- Optional current
- Optional power factor
- Optional solar export
- Optional community battery power

Highlight the event period using a shaded rectangle.

## Event Navigation

Provide controls:

```text
Previous event
Next event
```

---

# Page 6: Root Cause Analysis

## Objective

Present findings from Task 03 without overstating causality.

## Root Cause Ranking

Display root-cause groups ranked by:

- Number of events
- Total duration
- Mean severity
- Maximum error
- Confidence

Example cause categories:

- AMI communication loss
- DTMS communication loss
- Missing AMI meter
- Timestamp mismatch
- Aggregation logic issue
- Sign convention mismatch
- Solar export handling issue
- Community battery handling issue
- CT ratio mismatch
- Voltage ratio mismatch
- Persistent measurement bias
- Transformer technical loss
- Phase mapping issue
- Unknown

## Confidence Levels

Use:

```text
Very High
High
Medium
Low
Unknown
```

Clearly state:

> Root-cause classifications are analytical hypotheses unless confirmed by field inspection, meter configuration records, communication logs, or equipment testing.

## Charts

Include:

- Root cause frequency bar chart
- Total abnormal duration by cause
- Severity versus confidence scatter plot
- Root cause trend by month
- Root cause timeline

Prefer bar charts over pie charts when comparing many categories.

---

# Page 7: Data Explorer

## Objective

Allow engineering users to inspect and export filtered data.

## Table

Display filtered records from `comparison_result.parquet`.

Recommended columns:

- Timestamp
- Transformer ID
- DTMS kW
- AMI import kW
- AMI export kW
- AMI net kW
- Battery kW
- Adjusted AMI kW
- Difference kW
- Absolute difference kW
- Percentage error
- Error severity
- AMI active meter count
- AMI completeness
- Anomaly flag

Use pagination or row limiting.

Do not render millions of rows at once.

Provide selectable maximum rows:

```text
1,000
5,000
10,000
50,000
```

## Download

Provide CSV download for:

- Current filtered comparison data
- Current anomaly table
- Current metric summary

Use descriptive filenames containing:

- Transformer ID
- Start date
- End date

---

# Page 8: Methodology and Notes

Explain:

- DTMS original sampling interval
- AMI original sampling interval
- Resampling method
- AMI aggregation method
- Import and export sign convention
- Community battery treatment
- Error metric definitions
- MAPE limitations
- Missing-data treatment
- Outlier treatment
- Root-cause confidence meaning
- Analysis limitations

- Definitions of S1, S2, and S3, including the S2 median-profile method

Read the content from existing Markdown reports where practical.

---

# AMI Net Power Convention

The application must not assume the sign convention without validation.

Determine and document the correct formula.

Possible convention:

```text
AMI_net_kW = AMI_import_kW - AMI_export_kW
```

However, verify the meaning and sign of each source column before applying the formula.

If AMI export is already negative, do not subtract it again.

Create a configuration section such as:

```python
AMI_IMPORT_COLUMN = "kW average"
AMI_EXPORT_COLUMN = "kW exp average"
AMI_EXPORT_IS_POSITIVE = True
```

For a positive export column:

```python
ami_net_kw = ami_import_kw - ami_export_kw
```

Report the selected convention on the Methodology page.

---

# Community Battery Treatment

If a community battery exists under the transformer, provide support for battery power.

The comparison equation should be explicitly defined based on the battery meter location and sign convention.

Possible formulation:

```text
Expected_DTMS_kW
=
AMI_customer_net_kW
+
Battery_grid_import_kW
-
Battery_grid_export_kW
+
Estimated_technical_loss_kW
+
Unmetered_auxiliary_load_kW
```

Do not apply this formula until column definitions and measurement locations are confirmed.

Provide dashboard controls to compare:

```text
Raw AMI total
AMI adjusted for battery
AMI adjusted for battery and estimated losses
```

---

# Error Severity Classification

Use configurable thresholds.

Default classification based on absolute percentage error:

```text
Excellent: less than 5%
Good: 5% to less than 10%
Warning: 10% to less than 20%
Critical: 20% or greater
Unknown: denominator below minimum threshold
```

Do not hard-code these values throughout the application.

Store them in one configuration object.

Allow the user to adjust thresholds from the sidebar or an advanced settings section.

---

# Performance Requirements

The AMI dataset may contain many records.

Implement the following:

## Data Caching

Use:

```python
@st.cache_data
```

for:

- Parquet loading
- CSV loading
- Metric calculations
- Aggregations

Use a sensible TTL only when required.

## Column Selection

Load only required Parquet columns where possible.

## Filter Order

Apply filters before expensive aggregations.

## Sampling

For very large scatter plots, allow:

```text
All points
Random sample: 10,000
Random sample: 50,000
Density plot
```

Use a fixed random seed for reproducibility.

## Large Time Series

When the selected period contains too many points:

- Automatically aggregate to a suitable resolution, or
- Show a warning and offer hourly aggregation

Do not freeze the application by plotting unnecessarily large datasets.

---

# Data Validation and Error Handling

The application must handle:

- Missing files
- Empty filtered datasets
- Invalid timestamps
- Missing columns
- Duplicate timestamps
- Infinite metric values
- Division by zero
- NaN values
- Unsupported data types

Show user-friendly Streamlit messages:

```python
st.info(...)
st.warning(...)
st.error(...)
```

Do not expose a long Python traceback as the primary user-facing message.

Keep detailed errors available for debugging.

---

# Units and Labels

Every chart must include:

- Clear title
- X-axis label
- Y-axis label
- Engineering unit
- Legend
- Hover information

Use consistent terms:

```text
DTMS Active Power
Aggregated AMI Net Power
Difference = DTMS - AMI
Absolute Error
Percentage Error
```

Do not mix:

- kW and kWh
- Power and energy
- Import and net power

---

# Visual Design

Use a clean engineering dashboard style.

Requirements:

- Wide layout
- Consistent spacing
- Clear section headings
- KPI cards at the top
- Avoid excessive colors
- Use consistent colors for the same signals
- DTMS and AMI must keep the same visual identity across pages
- Critical anomalies must be visually distinguishable
- Tables should use readable column names

Do not overload a single page with too many charts.

Use tabs or expanders where appropriate.

---

# Reproducibility

Create a configuration section for:

- File paths
- Timestamp column names
- Transformer ID column
- Meter ID column
- DTMS power column
- AMI import column
- AMI export column
- Battery power column
- Error thresholds
- Minimum MAPE denominator
- Expected intervals

Do not scatter column names as string literals throughout the code.

---

# README Requirements

Generate `README-dashboard.md` containing:

## Installation

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install packages:

```bash
pip install -r requirements-dashboard.txt
```

## Run

```bash
streamlit run app.py
```

## Stop

Press:

```text
Ctrl + C
```

## Expected Input Files

List required and optional report files.

## Troubleshooting

Include guidance for:

- `streamlit` command not found
- Missing PyArrow
- Parquet file cannot be opened
- Port 8501 already in use
- Browser does not open automatically
- Missing required columns

For a different port:

```bash
streamlit run app.py --server.port 8502
```

---

# Validation Before Completion

Before declaring the task complete, verify:

1. The Streamlit application starts successfully.
2. `comparison_result.parquet` loads successfully.
3. Global date filtering works.
4. Transformer filtering works.
5. Time-series zoom works.
6. Pan mode works.
7. Scroll zoom works.
8. Hover information works.
9. Range slider works.
10. Reset axes works.
11. CSV download works.
12. Empty filter results do not crash the app.
13. Missing optional files do not crash the app.
14. Error metrics are recalculated for filtered data.
15. Charts use the correct engineering units.
16. kW values are not summed across time.
17. Import and export sign conventions are documented.
18. MAPE excludes zero or near-zero denominators.
19. Large datasets do not make the dashboard unusable.
20. README instructions reproduce the application successfully.

---

# Deliverables

Generate:

```text
app.py
dashboard/data_loader.py
dashboard/filters.py
dashboard/metrics.py
dashboard/charts.py
dashboard/pages.py
dashboard/utils.py
requirements-dashboard.txt
README-dashboard.md
```

Optional outputs:

```text
.streamlit/config.toml
dashboard/config.py
tests/test_metrics.py
tests/test_data_loader.py
```

---

# Final Response

After implementation, report:

- Files created
- Command used to run the dashboard
- Local URL
- Required input file
- Optional files detected
- Any assumptions made
- Any missing columns or unavailable features
- Results of the validation checklist

Do not claim the dashboard works unless the Streamlit application was actually started and tested.
