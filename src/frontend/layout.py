import gc
import os

import streamlit as st


from .components import github_button


def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "styles.css")
    with open(css_path, "r", encoding="utf-8") as f:  # Ajout de l'encodage ici
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def app_layout():
    from .layouts import page_0, page_1, page_2, page_3, page_4, page_5, page_6

    st.set_page_config(
        page_title="SDA-MACHINE-LEARNING",
        layout="wide",
        initial_sidebar_state="auto",
    )

    load_css()

    st.sidebar.markdown(
        "# --- DeFi Ecosystem ---\n\n"
        " ## *'User Behavior Pattern Analysis in DeFi Applications'*\n"
    )

    page = st.sidebar.radio(
        "Project_",
        [
            "#0 Introduction_",
            "#1 Exploration_",
            "#2 Feature Engineering_",
            "#3 Page_",
            "#4 Page_",
            "#5 Page_",
            "#6 Page_",
        ],
    )
    col1, col2 = st.columns([6, 4])
    with col1:

        st.markdown('<div class="title">DeFi Ecosystem</div>', unsafe_allow_html=True)
        st.markdown("#### *'User Behavior Pattern Analysis in DeFi Applications'* ")
        col_a, col_b, col_c, col_d = st.columns([1, 4, 4, 2])

        with col_a:
            github_button("https://github.com/mriusero/defi-user-behavior-clustering")

        with col_b:
            st.text("")
            st.link_button(
                "Kaggle Dataset",
                "https://www.kaggle.com/datasets/mariusayrault/defi-protocol-data-on-ethereum-2yr-23-to-24",
            )

        with col_c:
            st.text("")
            st.link_button(
                "Hugging Face Dataset",
                "https://huggingface.co/datasets/mriusero/DeFi-Protocol-Data-on-Ethereum-2023-2024",
            )

        with col_d:
            st.text("")
            if st.button("👾"):
                os.system("clear")

    with col2:
        st.text("")
        st.text("")
        st.text("")

    line_style = """
        <style>
        .full-width-line {
            height: 2px;
            background-color: #FFFFFF; /* Changez la couleur ici (rouge) */
            width: 100%;
            margin: 20px 0;
        }
        </style>
    """
    line_html = '<div class="full-width-line"></div>'

    st.markdown(line_style, unsafe_allow_html=True)
    st.markdown(line_html, unsafe_allow_html=True)

    if page == "#0 Introduction_":
        page_0()
    elif page == "#1 Exploration_":
        page_1()
    elif page == "#2 Feature Engineering_":
        page_2()
    elif page == "#3 Page_":
        page_3()
    elif page == "#4 Page_":
        page_4()
    elif page == "#5 Page_":
        page_5()
    elif page == "#6 Page_":
        page_6()

    st.sidebar.markdown("&nbsp;")

    gc.collect()
