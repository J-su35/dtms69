import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="DTMS vs AMI Dashboard", page_icon="⚡", layout="wide")
REPORTS = Path(__file__).parent / "reports"
required = REPORTS / "comparison_result.parquet"
if not required.exists():
    st.error("Required file reports/comparison_result.parquet is missing.")
    st.stop()
@st.cache_data
def load():
    x = pd.read_parquet(required); x["timestamp"] = pd.to_datetime(x["timestamp"]); return x
x = load(); st.title("⚡ DTMS vs AMI Dashboard")
scenario = st.sidebar.selectbox("Analysis scenario", sorted(x.scenario_id.unique()))
x = x[x.scenario_id == scenario]
transformers = sorted(x.transformer_id.astype(str).unique())
transformer = transformers[0] if len(transformers) == 1 else st.sidebar.selectbox("Transformer ID", transformers)
x = x[x.transformer_id.astype(str) == transformer]
dates = st.sidebar.date_input("Date range", (x.timestamp.dt.date.min(), x.timestamp.dt.date.max()))
if len(dates) == 2: x = x[x.timestamp.dt.date.between(dates[0], dates[1])]
if x.empty: st.info("No records match the selected filters."); st.stop()
err = x.dtms_kw - x.ami_net_kw; valid = x.ami_net_kw.abs() > .1
c1,c2,c3,c4 = st.columns(4); c1.metric("Matched intervals", f"{len(x):,}"); c2.metric("kW MAE", f"{err.abs().mean():.3f}"); c3.metric("kW RMSE", f"{(err.pow(2).mean() ** .5):.3f}"); c4.metric("MAPE", f"{(err[valid].abs()/x.loc[valid,'ami_net_kw'].abs()*100).mean():.2f}%")
mode = st.radio("Interaction mode", ["Zoom", "Pan"], horizontal=True)
fig = go.Figure(); fig.add_scatter(x=x.timestamp,y=x.dtms_kw,name="DTMS Active Power"); fig.add_scatter(x=x.timestamp,y=x.ami_net_kw,name="Aggregated AMI Net Power"); fig.update_layout(yaxis_title="kW",dragmode="zoom" if mode=="Zoom" else "pan",xaxis={"rangeslider":{"visible":True}})
config={"scrollZoom":True,"displaylogo":False,"responsive":True,"toImageButtonOptions":{"format":"png","filename":"dtms_ami_chart","scale":2}}
st.plotly_chart(fig,use_container_width=True,config=config)
st.plotly_chart(px.scatter(x,x="ami_net_kw",y="dtms_kw",color="error_severity",labels={"ami_net_kw":"AMI net kW","dtms_kw":"DTMS kW"}),use_container_width=True,config=config)
st.subheader("Filtered data"); st.download_button("Download CSV",x.to_csv(index=False),"comparison_filtered.csv","text/csv"); st.dataframe(x.head(10000),use_container_width=True)
