import streamlit as st
import json, os
import pandas as pd
import plotly.graph_objects as go

# ---------- Helper functions ----------

def _load_stats(main="outputs/metrics.json"):
    """
    Load the latest metrics, preferring the fixed file.
    If it's missing, fall back to the most recent backup.
    Returns: dict of raw numeric stats.
    """
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

# Gross
PRTF_PATH = "outputs/gr_prtf_ret.csv"
PRTF_VER = os.path.getmtime("outputs/gr_prtf_ret.csv")

mkt, gross_prtf = load_data(MKT_PATH, MKT_VER, PRTF_PATH, PRTF_VER)

# Net
PRTF_PATH = "outputs/net_prtf_ret.csv"
PRTF_VER = os.path.getmtime("outputs/net_prtf_ret.csv")

mkt, net_prtf = load_data(MKT_PATH, MKT_VER, PRTF_PATH, PRTF_VER)

# ---------- VISUAL ----------
def figure(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["cum_ret"], mode="lines",
        name="Portfolio", line=dict(color="#e64f3c", width=2.5)
    ))
    fig.add_trace(go.Scatter(
        x=mkt["date"], y=mkt["cum_ret"], mode="lines",
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
    fig.update_yaxes(tickformat="")      # percent ticks
    return fig

# ---------- Page section ----------

def render_performance():
    st.title("Performance")
    st.subheader("Gross Metrics")

    try:
        stats, source_path = _load_stats("outputs/gross_metrics.json")
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
        figure(gross_prtf),
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

    st.divider()

    st.subheader("Net Metrics")

    try:
        stats, source_path = _load_stats("outputs/net_metrics.json")
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
        figure(net_prtf),
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

    st.subheader("Cross-Sectional Holdings") 

    st.divider()

    st.subheader("Top 10 Holdings")
    top10 = pd.read_csv("outputs/top10.csv")

    # Apply styling: center text, bold headers, and hide index
    styled_df = (
        top10.style
        .hide(axis="index")
        .set_table_styles([
            {"selector": "th", "props": [("font-weight", "bold"), ("text-align", "center"), ("background-color", "#0E1117"), ("color", "white")]},
            {"selector": "td", "props": [("text-align", "center")]}
        ])
    )

    # Display with Streamlit
    st.dataframe(styled_df, use_container_width=True)

    st.divider()

    st.subheader("Bottom 10 Holdings")
    bot10 = pd.read_csv("outputs/bot10.csv")

    # Apply styling: center text, bold headers, and hide index
    styled_df = (
        bot10.style
        .hide(axis="index")
        .set_table_styles([
            {"selector": "th", "props": [("font-weight", "bold"), ("text-align", "center"), ("background-color", "#0E1117"), ("color", "white")]},
            {"selector": "td", "props": [("text-align", "center")]}
        ])
    )

    # Display with Streamlit
    st.dataframe(styled_df, use_container_width=True)

# ---------- Run Page ---------
if __name__ == "__main__":
    st.set_page_config(page_title="Applied Capital - Portfolio Performance", layout="wide")
    st.logo("assets/logo_white.svg")
    render_performance()