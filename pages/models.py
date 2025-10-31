import streamlit as st
from PIL import Image

# ---------- Page sections ----------

def render_models():
    st.subheader("Fourier Neural Operator (FNO)")
    with st.expander("What is FNO?", expanded=True):
        left, right = st.columns(2)
        left.markdown(
            """
            The Fourier Neural Operator (FNO) is a type of neural network architecture 
            designed to learn mappings between function spaces. It leverages the Fourier 
            Transform to efficiently capture global information in the input data, making 
            it particularly effective for solving partial differential equations (PDEs) 
            and other problems in scientific computing.
            """
        )
        FNOarch = Image.open("assets/fourier_full_arch.png")
        right.image(FNOarch, caption="Fourier Neural Network Architecture", width='stretch')
    
    st.divider()

    st.subheader("Regime Modeling")
    with st.expander("Statistical Jump Model", expanded=True):
        left, right = st.columns(2)
        left.markdown(
            """
            As both a feature for the FNO and the RL optimizer, we use a Statistical Jump Model 
            to identify market regimes, Growth vs Crash). The Statistical Jump Model (JM) minimizes:
            """
        )
        SJM_Math = Image.open("assets/SJM_Math.png")
        left.image(SJM_Math, width='content')
        left.markdown(
            """
            balancing fit with regime persistence.
            """
        )
        SJM_Regimes = Image.open("assets/SJM_Regimes.png")
        right.image(SJM_Regimes, caption="S&P Market Regimes", width='stretch')

    with st.expander("Sentiment Analysis", expanded=True):
        st.markdown(
            """
            We split each report into sentences and ranked their importance using TF-IDF 
            (Term Frequency-Inverse Document Frequency). Each document was condensed by 
            only keeping a subset of the sentences with highest importance. The condensed 
            text was passed through FinBERT to calculate sentiment scores. FinBERT is an 
            NLP model pre-trained on financial data. Separate sentiment scores were calculated 
            for “Risk Factors” and “Management Discussion and Analysis” to be used as features 
            for the FNO model.
            """
        )

    st.divider()
    st.subheader("Optimizer")
    with st.expander("...", expanded=True):
        st.markdown(
            """
            TBD
            """
        )

# ---------- Run Page ---------
if __name__ == "__main__":
    st.set_page_config(page_title="Applied Capital - Models", layout="wide")
    st.logo("assets/logo_white.svg")
    render_models()
    
    # TODO: add sub-sections or accordions as needed
    # with st.expander("Model A"):
    #     st.write("Description, inputs, outputs, notes.")