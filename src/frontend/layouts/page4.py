import streamlit as st

from src.backend.ml.pipeline import ml_pipeline

def page_4():
    st.markdown('<div class="header">#4 ML Pipeline_</div>', unsafe_allow_html=True)

    if st.button("Run ML Pipeline"):
        ml_pipeline()