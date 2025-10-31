import streamlit as st
import json, os
import pandas as pd
import plotly.graph_objects as go

# ---------- Helper functions ----------

def _load_stats():
    """
    Load the latest metrics, preferring the fixed file.
    If it's missing, fall back to the most recent backup.
    Returns: dict of raw numeric stats.
    """
    main = "outputs/metrics.json"
    try:
        with open(main, "r") as f:
            return json.load(f), main
    except Exception:
        raise FileNotFoundError("No metrics.json or backups found.")

def _format_percent(x):
    try:
        return f"{float(x):.2%}"
    except Exception:
        return str(x)
    
@st.cache_data
def load_data(m_path, m_ver, p_path, p_ver):
    mkt = pd.read_csv(m_path, parse_dates=["date"])
    prtf = pd.read_csv(p_path, parse_dates=["date"])
    return mkt, prtf

MKT_PATH = "outputs/mkt_ret.csv"
MKT_VER = os.path.getmtime("outputs/mkt_ret.csv")
PRTF_PATH = "outputs/prtf_ret.csv"
PRTF_VER = os.path.getmtime("outputs/prtf_ret.csv")

mkt, prtf = load_data(MKT_PATH, MKT_VER, PRTF_PATH, PRTF_VER)

# Compute cumulative returns
mkt["cumret"] = (1 + mkt["ret"]).cumprod() - 1
prtf["cumret"] = (1 + prtf["ret"]).cumprod() - 1

# ---------- VISUAL ----------

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=prtf["date"], y=prtf["cumret"], mode="lines",
    name="Portfolio", line=dict(color="#e64f3c", width=2.5)
))
fig.add_trace(go.Scatter(
    x=mkt["date"], y=mkt["cumret"], mode="lines",
    name="Market", line=dict(color="#007acc", width=2.5)
))

fig.update_layout(
    # center title over the plotting area
    title=dict(text="Cumulative Returns vs. Market", x=0.5, xanchor="center"),

    # legend truly centered below the chart
    legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.20),

    # symmetric margins = symmetric visuals
    margin=dict(l=60, r=60, t=70, b=70),
    yaxis_title="Cumulative Return",
    hovermode="x",        # one hover per trace at that x
    template="plotly_dark",
    height=500
)
fig.update_yaxes(tickformat=".0%")      # percent ticks


    
# ---------- Page section ----------

def render_performance():
    st.subheader("Performance")

    try:
        stats, source_path = _load_stats()
    except Exception as e:
        st.error(f"Could not load performance data: {e}")
        return

    # Build display dict with graceful fallbacks
    display = {
        "Annualized Return": stats["CAGR"], 
        "Annualized Std Dev": stats["STD"], 
        "Annualized Alpha": stats["Alpha"],
        "Sharpe Ratio": stats["Sharpe"],
        "Information Ratio": stats["IR"], 
        "Max Drawdown": stats["Max Drawdown"],
        "Max 1-Month Loss": stats["Max_one_month_loss"],
        "Turnover": stats["Avg_Turnover"],
    }

    # KPI tiles
    kpi_cols = st.columns(4)
    kpis = [
        ("Annualized Return", _format_percent(display["Annualized Return"])),
        ("Annualized Std Dev", _format_percent(display["Annualized Std Dev"])),
        ("Annualized Alpha", _format_percent(display["Annualized Alpha"])),
        ("Sharpe Ratio", f"{display['Sharpe Ratio']:.2f}" if display["Sharpe Ratio"] is not None else "—"),
        ("Information Ratio", f"{display['Information Ratio']:.2f}" if display["Information Ratio"] is not None else "—"),
        ("Max Drawdown", _format_percent(display["Max Drawdown"])),
        ("Max 1-Month Loss", _format_percent(display["Max 1-Month Loss"])),
        ("Turnover", _format_percent(display["Turnover"])),
    ]
    for i, (label, val) in enumerate(kpis):
        with kpi_cols[i % 4]:
            st.metric(label, val)

    st.divider()

    # Interactive Chart
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displaylogo": False,
            # remove everything except resetScale2d
            "modeBarButtonsToRemove": [
                "toImage","toggleSpikelines","hoverClosestCartesian","hoverCompareCartesian",
                "zoom","zoomIn2d","zoomOut2d","autoScale2d","pan2d","select2d","lasso2d",
                "orbitRotation","tableRotation","resetViewMapbox"
            ],
            # leave Reset; make double-click also reset
            "doubleClick": "reset",
            "scrollZoom": False,
            "responsive": True
        }
    )

# ---------- Run Page ---------
if __name__ == "__main__":
    st.set_page_config(page_title="Applied Capital - Portfolio Performance", layout="wide")
    st.logo("assets/logo_white.svg")
    render_performance()