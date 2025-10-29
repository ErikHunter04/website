import streamlit as st
import json
import pandas as pd

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
        "Annualized Alpha": None, # MISSING
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
    # TODO: Interactive Graph