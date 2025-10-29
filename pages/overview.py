import streamlit as st

# ---------- Page sections ----------

def render_overview():
    st.subheader("Thesis")
    st.write(
        """
        Our approach is a long-only investment strategy – focused on North American equities – based
        on the hypothesis that stock returns within each country’s sector can be modeled as stochastic 
        processes governed by stochastic different equations (SDEs). Observed returns are treated as 
        realizations of these SDEs, with firm-level features and market-wide indicators acting as 
        state-dependent coefficients. We then employ a reinforcement learning optimizer to dynamically 
        allocate capital across sectors and individual stocks, adapting to evolving market regimes.
        """
    )