import streamlit as st
from pages.overview import render_overview
from pages.models import render_models
from pages.performance import render_performance

# ---------- App shell ----------

def main():
    st.set_page_config(page_title="Applied Capital - FIAM Hackathon", layout="wide")
    st.title("Applied Capital Strategy")
    st.caption("Skeleton app: tabs only. Data wiring comes later.")
    tab1, tab2, tab3 = st.tabs(["Strategy Overview", "Models", "Performance"])

    with tab1:
        render_overview()
    with tab2:
        render_models()
    with tab3:
        render_performance()

if __name__ == "__main__":
    main()