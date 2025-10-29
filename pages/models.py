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
        farch = Image.open("assets/fourier_full_arch.png")
        right.image(farch, caption="Fourier Neural Network Architecture", use_container_width=True)
    # TODO: add sub-sections or accordions as needed
    # with st.expander("Model A"):
    #     st.write("Description, inputs, outputs, notes.")