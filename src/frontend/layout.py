import gc
import os
import streamlit as st

from .components import github_button

def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "styles.css")
    with open(css_path, "r", encoding="utf-8") as f:  # Ajout de l'encodage ici
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def app_layout():
    from .layouts import page_0, page_1, page_2, page_3, page_4

    st.set_page_config(
        page_title="DeFI Behavior",
        page_icon="👾",
        layout="wide",
        initial_sidebar_state="auto",
    )

    load_css()

    st.sidebar.markdown(" ## *DeFI Behavior*\n")

    if 'page' not in st.session_state:
        st.session_state.page = "# Introduction_"

    st.session_state.page = st.sidebar.radio(
        "Summary",
        [
            "# Performance Report_",
            "# Study Overview_",
            "# Data Collection_",
            "# Features Engineering_",
            "# Clustering_",
        ],
    )

    col1, col2 = st.columns([3, 4])
    with col1:
        st.markdown('<div class="title">DeFi Behavior</div>', unsafe_allow_html=True)
        st.markdown("#### *'User Behavior Analysis in DeFi Applications'* ")
        col_a, col_b= st.columns([1, 6])

        with col_a:
            github_button("https://github.com/mriusero/defi-user-behavior-clustering")

        with col_b:
            st.text("")
            st.write(""
                     "[![HuggingFace](https://img.shields.io/badge/%20COLLECTION-FFD700?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/collections/mriusero/defi-behavior-analysis-67a0d6d132ccecdff8068369)"
                     "[![HuggingFace](https://img.shields.io/badge/DATASET-FFD700?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/datasets/mriusero/DeFi-Protocol-Data-on-Ethereum-2023-2024)"
                     "[![HuggingFace](https://img.shields.io/badge/SPACE-FFD700?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/spaces/mriusero/DeFI-Behavior)"
                     "[![HuggingFace](https://img.shields.io/badge/MODEL-FFD700?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/mriusero/DeFI-Behavior-Models)")

    with col2:
        st.text("")
        st.text("")
        st.text("")

    line_style = """
        <style>
        .full-width-line {
            height: 2px;
            background-color: #FFFFFF;
            width: 100%;
            margin: 20px 0;
        }
        </style>
    """
    line_html = '<div class="full-width-line"></div>'

    st.markdown(line_style, unsafe_allow_html=True)
    st.markdown(line_html, unsafe_allow_html=True)

    if st.session_state.page == "# Performance Report_":
        page_4()
    elif st.session_state.page == "# Study Overview_":
        page_0()
    elif st.session_state.page == "# Data Collection_":
        page_1()
    elif st.session_state.page == "# Features Engineering_":
        page_2()
    elif st.session_state.page == "# Clustering_":
        page_3()


    st.sidebar.markdown("&nbsp;")

    gc.collect()
