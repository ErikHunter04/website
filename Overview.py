import streamlit as st
from PIL import Image

# ---------- App shell ----------
st.set_page_config(page_title="Applied Capital - Overview", layout="wide")
st.logo("assets/logo_white.svg")
st.title("Strategy Overview")

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

st.subheader("Methodology")
Meth = Image.open("assets/Methodology.png")
st.image(Meth, caption="Overview of our Strategy", use_container_width=False)

    