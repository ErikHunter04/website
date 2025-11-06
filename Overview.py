import streamlit as st
from PIL import Image

# ---------- App shell ----------
st.set_page_config(page_title="Applied Capital - Overview", layout="wide")
st.logo("assets/logo_white.svg")
st.title("Strategy Overview")

st.subheader("Thesis")
st.markdown(
        """
        **Background** \n
        Traditional factor models like APT and Fama–French rely on fixed, hand-crafted factors (e.g., Value, Momentum)
        estimated through static regressions. These models struggle to adapt as market relationships change over time. 
        Our approach replaces these static factors with a Fourier Neural Operator (FNO) — a model designed to learn dynamic, 
        global relationships directly from data.
        """
)
st.latex(r"r_t = \beta_1 f_1 + \beta_2 f_2 + \dots + \beta_5 f_5")

st.markdown(
        """
        **Core Idea**
        We treat the global equity universe as a field of stock-level features. Each month, the FNO learns latent factor exposures 
        for every stock and combines them with time-varying factor premia to predict next-month returns. This makes the model a neural, 
        adaptive version of APT — able to capture nonlinear, cross-market patterns that traditional models miss.    
        """
)
st.latex(r"\hat{r}_{i,t+1} = z_{i,t}^\top w_t")

st.subheader("Methodology")
Meth = Image.open("assets/Methodology.png")
st.image(Meth, caption="Overview of our Strategy", use_container_width=False)

    