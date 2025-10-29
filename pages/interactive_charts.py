import pandas as pd
import numpy as np
import plotly.graph_objects as go

BRAND = {
    "bg": "white",
    "fg": "#003366",
    "grid": "#cce0ff",
    "portfolio": "#e64f3c",
    "market":    "#007acc",
    "drawdown_fill_pf": "#f28c3c",
    "drawdown_fill_mkt": "#66a3ff",
}

def _to_ts_index(r_period_idx: pd.PeriodIndex) -> pd.DatetimeIndex:
    return r_period_idx.to_timestamp("M")

def _ensure_decimal(ser: pd.Series) -> pd.Series:
    """Auto-fix % inputs (e.g., 1.2 = 1.2%) into decimals (0.012)."""
    s = pd.to_numeric(ser, errors="coerce")
    # If typical magnitude suggests percents, scale down
    if s.dropna().abs().median() > 0.5:
        s = s / 100.0
    return s

def _wealth_from_r(r: pd.Series, start=1.0) -> pd.Series:
    return start * (1 + r.fillna(0)).cumprod()

def _drawdown_from_r(r: pd.Series) -> pd.Series:
    w = _wealth_from_r(r)
    return w / w.cummax() - 1.0

def plot_cumulative_interactive(
    r_pf: pd.Series,
    r_mkt: pd.Series,
    *,
    title: str = "Cumulative Return (Monthly, %)",
    log_scale: bool = False,
) -> go.Figure:
    # align and sanitize
    common = r_pf.index.intersection(r_mkt.index)
    rpf = _ensure_decimal(r_pf.loc[common].astype(float))
    rmk = _ensure_decimal(r_mkt.loc[common].astype(float))

    # to timestamp index for plotting
    idx_ts = _to_ts_index(common)
    w_pf = _wealth_from_r(rpf).set_axis(idx_ts)
    w_mk = _wealth_from_r(rmk).set_axis(idx_ts)

    # Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=w_pf.index, y=w_pf - 1.0, mode="lines", name="Portfolio",
        line=dict(color=BRAND["portfolio"], width=2.4),
        hovertemplate="%{x|%b %Y}<br>Portfolio: %{y:.2%}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=w_mk.index, y=w_mk - 1.0, mode="lines", name="S&P500",
        line=dict(color=BRAND["market"], width=2.4),
        hovertemplate="%{x|%b %Y}<br>S&P500: %{y:.2%}<extra></extra>",
    ))

    fig.update_layout(
        title=title,
        plot_bgcolor=BRAND["bg"],
        paper_bgcolor=BRAND["bg"],
        xaxis=dict(
            title="Date",
            rangeslider=dict(visible=True),
            showgrid=True, gridcolor=BRAND["grid"]
        ),
        yaxis=dict(
            title="Cumulative Return (%)",
            tickformat=".0%",
            showgrid=True, gridcolor=BRAND["grid"],
            type="log" if log_scale else "linear",
        ),
        legend=dict(orientation="h", y=1.08, x=0),
        hovermode="x unified",
        margin=dict(l=50, r=10, t=60, b=40),
    )
    return fig

def plot_drawdown_interactive(
    r_pf: pd.Series,
    r_mkt: pd.Series,
    *,
    title: str = "Drawdown (Monthly)",
) -> go.Figure:
    common = r_pf.index.intersection(r_mkt.index)
    rpf = _ensure_decimal(r_pf.loc[common].astype(float))
    rmk = _ensure_decimal(r_mkt.loc[common].astype(float))
    idx_ts = _to_ts_index(common)
    dd_pf = _drawdown_from_r(rpf).set_axis(idx_ts)
    dd_mk = _drawdown_from_r(rmk).set_axis(idx_ts)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dd_pf.index, y=dd_pf, name="Portfolio",
        mode="lines", line=dict(color=BRAND["portfolio"], width=2.0),
        fill="tozeroy", fillcolor="rgba(242,140,60,0.18)",
        hovertemplate="%{x|%b %Y}<br>Portfolio DD: %{y:.2%}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=dd_mk.index, y=dd_mk, name="S&P500",
        mode="lines", line=dict(color=BRAND["market"], width=2.0),
        fill="tozeroy", fillcolor="rgba(102,163,255,0.14)",
        hovertemplate="%{x|%b %Y}<br>S&P500 DD: %{y:.2%}<extra></extra>",
    ))
    fig.update_layout(
        title=title,
        plot_bgcolor=BRAND["bg"], paper_bgcolor=BRAND["bg"],
        xaxis=dict(title="Date", rangeslider=dict(visible=True), showgrid=True, gridcolor=BRAND["grid"]),
        yaxis=dict(title="Drawdown (%)", tickformat=".0%", showgrid=True, gridcolor=BRAND["grid"]),
        legend=dict(orientation="h", y=1.08, x=0),
        hovermode="x unified",
        margin=dict(l=50, r=10, t=60, b=40),
    )
    return fig
