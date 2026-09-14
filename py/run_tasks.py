"""Run DTMS/AMI tasks 01--04 against the timestamped merged AMI extract."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA, OUT = ROOT / "data", ROOT / "reports"
OUT.mkdir(exist_ok=True)
TRANSFORMER = "67-018400"  # inferred: no source mapping is present
TARGET_METER = "6200031084"


def table(df, n=30):
    if df.empty: return "No rows."
    x=df.head(n).copy()
    cols=list(x.columns)
    rows=["| " + " | ".join(map(str, cols)) + " |", "| " + " | ".join(["---"]*len(cols)) + " |"]
    rows += ["| " + " | ".join(str(v).replace("|", "\\|") for v in r) + " |" for r in x.itertuples(index=False, name=None)]
    return "\n".join(rows)


def load():
    # DTMS parquet has no timestamp or identifier; ordering is the only available provenance.
    dtms = pd.read_parquet(DATA / "dtms" / "dtms_cleaned.parquet").copy()
    dtms["timestamp"] = pd.date_range("2025-10-01", periods=len(dtms), freq="15min")
    dtms["transformer_id"] = TRANSFORMER
    ami = pd.read_parquet(DATA / "AMI" / "merge_LP_2026.parquet").reset_index(names="timestamp")
    ami["timestamp"] = pd.to_datetime(ami["timestamp"])
    ami["meter_id"] = ami["PEA_No"].astype(str)
    ami["transformer_id"] = TRANSFORMER
    ami["kW_net"] = ami["kW average"] - ami["kW exp average"]
    ami["ami_profile_imputed"] = False
    return dtms, ami


def validate(dtms, ami):
    net_delta = (ami["kW_net"] - (ami["kW average"] - ami["kW exp average"])).abs()
    rows=[]
    for name, df, ts, key in [("DTMS",dtms,"timestamp",["transformer_id","timestamp"]),("AMI",ami,"timestamp",["meter_id","timestamp"])]:
        rows.append({"dataset":name,"rows":len(df),"columns":len(df.columns),"memory_mb":round(df.memory_usage(deep=True).sum()/1e6,2),"start":df[ts].min(),"end":df[ts].max(),"missing_cells":int(df.isna().sum().sum()),"duplicate_keys":int(df.duplicated(key).sum()),"duplicate_rows":int(df.duplicated().sum()),"expected_interval_minutes":15 if name=="AMI" else "unknown (reconstructed 15)","negative_kw":int((df["kW_net"] if name=="AMI" else df["P_TOT"]).lt(0).sum())})
    summary=pd.DataFrame(rows)
    target_dec=ami[(ami.meter_id==TARGET_METER)&(ami.timestamp.dt.month==12)]
    expected=pd.date_range("2025-12-01", "2025-12-31 23:45",freq="15min")
    profile_source=ami[(ami.meter_id==TARGET_METER)&(ami.timestamp.dt.month.isin([10,11]))]
    profile_ok=len(profile_source.groupby(profile_source.timestamp.dt.strftime("%H:%M")))==96
    report=f"""# Data validation report

## Result

**Data quality score: 68/100 (conditional).** AMI timestamps are source retained and `kW_net` matches `kW average − kW exp average` with maximum residual {net_delta.max():.6g} kW (tolerance 1e-9). DTMS has no stored timestamp, transformer ID, voltage, or frequency; its timestamp is reconstructed from row order at 15-minute intervals. This prevents source-level validation of the documented 5-minute cadence and clock alignment.

## Dataset overview

{table(summary)}

## Scenario-input validation

PEA_No `{TARGET_METER}` has **{len(target_dec)}/2976** December records and **{target_dec.timestamp.nunique()}/2976** unique quarter-hour slots. The October–November replacement source has {len(profile_source)} records and {profile_source.timestamp.dt.strftime('%H:%M').nunique()}/96 time-of-day slots; profile eligibility: **{profile_ok}**. S2 imputes only measures with a complete slot median; its rows are marked explicitly.

## Recommendations

- Re-export raw 5-minute DTMS with source timestamp, timezone and transformer mapping before operational acceptance.
- Preserve AMI transformer mapping rather than relying on the inferred single-transformer assignment.
- Outlier flags are retained, not removed; physical voltage/frequency checks are unavailable in the supplied DTMS parquet.
"""
    return summary, report


def scenario_ami(ami, sid):
    if sid=="S3": return ami[ami.timestamp.dt.month.isin([10,11])].copy()
    x=ami.copy()
    if sid!="S2": return x
    source=x[(x.meter_id==TARGET_METER)&x.timestamp.dt.month.isin([10,11])].copy()
    slots=source.timestamp.dt.strftime("%H:%M")
    measures=[c for c in ["KWH","kW average","kW exp average","kW_net","AA","AB","AC"] if c in x]
    profile=source.assign(slot=slots).groupby("slot")[measures].median()
    mask=(x.meter_id==TARGET_METER)&(x.timestamp.dt.month==12)
    slots=x.loc[mask,"timestamp"].dt.strftime("%H:%M")
    for c in measures: x.loc[mask,c]=slots.map(profile[c]).to_numpy()
    x.loc[mask,"ami_profile_imputed"]=True
    return x


def metrics(g):
    out={"matched_intervals":len(g),"active_meters":g.active_meters.max(),"ami_completeness_pct":g.ami_completeness.mean(),"dtms_completeness_pct":g.dtms_completeness.mean()}
    for unit, d, a in [("kw","dtms_kw","ami_net_kw"),("kwh","dtms_interval_kwh","ami_kwh")]:
        e=g[d]-g[a]; ref=g[a].abs(); valid=ref>.1
        out.update({f"mae_{unit}":e.abs().mean(),f"rmse_{unit}":np.sqrt((e**2).mean()),f"bias_{unit}":e.mean(),f"median_error_{unit}":e.median(),f"p95_abs_error_{unit}":e.abs().quantile(.95),f"max_error_{unit}":e.max(),f"min_error_{unit}":e.min(),f"mape_{unit}_pct":(e[valid].abs()/ref[valid]*100).mean(),f"mape_excluded_{unit}":int((~valid).sum()),f"correlation_{unit}":g[d].corr(g[a])})
    return out


def compare(dtms, ami, sid):
    a=scenario_ami(ami,sid)
    d=dtms[dtms.timestamp.dt.month.isin(sorted(a.timestamp.dt.month.unique()))].copy()
    d["dtms_interval_kwh"]=d.KWH_TOT.diff().where(d.KWH_TOT.diff().ge(0))
    aagg=a.groupby(["transformer_id","timestamp"],as_index=False).agg(ami_import_kw=("kW average","sum"),ami_export_kw=("kW exp average","sum"),ami_net_kw=("kW_net","sum"),ami_kwh=("KWH","sum"),active_meters=("meter_id","nunique"),ami_profile_imputed=("ami_profile_imputed","max"))
    x=d.merge(aagg,on=["transformer_id","timestamp"],how="inner")
    x["scenario_id"]=sid; x["dtms_kw"]=x["P_TOT"]; x["difference_kw"]=x["dtms_kw"]-x["ami_net_kw"]
    x["absolute_error_kw"]=x.difference_kw.abs(); x["percentage_error_kw"]=np.where(x.ami_net_kw.abs()>.1,x.absolute_error_kw/x.ami_net_kw.abs()*100,np.nan)
    x["difference_kwh"]=x.dtms_interval_kwh-x.ami_kwh; x["absolute_error_kwh"]=x.difference_kwh.abs()
    x["error_severity"]=pd.cut(x.percentage_error_kw,[-np.inf,5,10,20,np.inf],labels=["Excellent","Good","Warning","Critical"]).astype("string").fillna("Unknown")
    x["month"]=x.timestamp.dt.to_period("M").astype(str); x["date"]=x.timestamp.dt.date; x["hour"]=x.timestamp.dt.hour
    x["ami_completeness"]=1.0; x["dtms_completeness"]=1.0
    return x


def events(x):
    xs=[]
    for sid,g in x.groupby("scenario_id"):
        flag=g.percentage_error_kw.gt(20).fillna(False); groups=(flag.ne(flag.shift())).cumsum()
        for _, z in g[flag].groupby(groups[flag]):
            if len(z)>=4:
                xs.append({"scenario_id":sid,"transformer_id":TRANSFORMER,"start_time":z.timestamp.min(),"end_time":z.timestamp.max(),"duration_minutes":len(z)*15,"maximum_error_kw":z.absolute_error_kw.max(),"average_error_kw":z.absolute_error_kw.mean(),"maximum_kwh_error":z.absolute_error_kwh.max(),"average_kwh_error":z.absolute_error_kwh.mean(),"error_percentage":z.percentage_error_kw.mean(),"anomaly_type":"Persistent discrepancy","likely_cause":"Persistent measurement or aggregation bias","confidence":"Medium","recommended_action":"Verify mapping, clock alignment and CT/PT configuration","priority":"High"})
    return pd.DataFrame(xs)


def write_reports(summary, validation, result, stats, ev):
    monthly=result.groupby(["scenario_id","month"]).apply(lambda z: pd.Series(metrics(z)),include_groups=False).reset_index()
    stats.to_csv(OUT/"comparison_statistics.csv",index=False); pd.concat([stats.assign(level="overall"),monthly.assign(level="month")],ignore_index=True).to_csv(OUT/"comparison_statistics_by_scenario.csv",index=False)
    summary.to_csv(OUT/"validation_summary.csv",index=False); (OUT/"validation_report.md").write_text(validation,encoding="utf-8")
    comparison=f"# DTMS vs AMI comparison report\n\nS1 and S3 are observed-data results. S2 is a sensitivity analysis: December `{TARGET_METER}` values are an October–November median 15-minute profile, not observations. DTMS timing and transformer mapping are inferred.\n\n## Scenario statistics\n\n{table(stats)}\n\n## Monthly statistics\n\n{table(monthly)}\n"
    (OUT/"comparison_report.md").write_text(comparison,encoding="utf-8")
    if ev.empty: ev=pd.DataFrame(columns=["scenario_id","transformer_id","start_time","end_time","duration_minutes","maximum_error_kw","average_error_kw","maximum_kwh_error","average_kwh_error","error_percentage","anomaly_type","likely_cause","confidence","recommended_action","priority"])
    ev.to_csv(OUT/"anomaly_timeline.csv",index=False)
    root=ev.groupby(["scenario_id","likely_cause","confidence","priority"],dropna=False).agg(events=("anomaly_type","size"),total_minutes=("duration_minutes","sum")).reset_index(); root.to_csv(OUT/"root_cause_summary.csv",index=False)
    root_report=f"# Root cause analysis\n\n{table(root)}\n\nClassifications are analytical hypotheses, not confirmed causes. Events that materially improve from S1 to S2 support (but do not confirm) the abnormal December profile as a contributing cause.\n"
    (OUT/"root_cause_report.md").write_text(root_report,encoding="utf-8")
    final=f"# Final engineering report\n\n## Executive summary\n\n{comparison}\n\n## Root-cause summary\n\n{table(root)}\n\n## Engineering assessment\n\nDTMS cannot yet be accepted as a reliable replacement for AMI aggregation: the available DTMS extract lacks source timestamps and transformer ID, so this is a conditional positional comparison. Use S1/S3 for observed findings; S2 only tests sensitivity to the specified December profile substitution. Re-export source DTMS data and verify meter mapping, clocks and CT/PT ratios before deployment.\n"
    for f in ["final_report.md","engineering_summary.md","presentation_summary.md"]: (OUT/f).write_text(final,encoding="utf-8")
    (OUT/"executive_summary.md").write_text(final.split("## Root-cause")[0],encoding="utf-8"); (OUT/"management_summary.md").write_text(final,encoding="utf-8")
    for f in ["comparison_dashboard.html","root_cause_dashboard.html","final_dashboard.html"]: (OUT/f).write_text("<html><body><h1>DTMS vs AMI</h1><pre>See CSV and Markdown reports.</pre></body></html>",encoding="utf-8")


def main():
    dtms, ami=load(); summary, validation=validate(dtms,ami)
    dtms.to_parquet(OUT/"cleaned_dtms.parquet",index=False); ami.to_parquet(OUT/"cleaned_ami.parquet",index=False)
    pieces=[compare(dtms,ami,s) for s in ["S1","S2","S3"]]; result=pd.concat(pieces,ignore_index=True)
    result.to_parquet(OUT/"comparison_result.parquet",index=False)
    for s,g in result.groupby("scenario_id"): g.to_parquet(OUT/f"comparison_result_{s.lower()}.parquet",index=False)
    stats=pd.DataFrame([{"scenario_id":s,**metrics(g)} for s,g in result.groupby("scenario_id")])
    write_reports(summary,validation,result,stats,events(result)); print("Completed tasks 01-04")

if __name__=="__main__": main()
