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
        page_icon="random",
        layout="wide",
        initial_sidebar_state="auto",
    )

    load_css()

    st.sidebar.markdown(
        " ## *DeFI Behavior*\n"
    )

    page = st.sidebar.radio(
        "Summary",
        [
            "# Home_",
            "# Detected User Profiles_",
            "# Capital Migration Tracking_",
            "# Anomaly Detection_",
            "# Summary of Results_",
        ],
    )
    col1, col2 = st.columns([6, 4])
    with col1:

        st.markdown('<div class="title">DeFi Behavior</div>', unsafe_allow_html=True)
        st.markdown("#### *'User Behavior Pattern Analysis in DeFi Applications'* ")
        col_a, col_b, col_c, col_d = st.columns([1, 2, 2, 2])

        with col_a:
            github_button("https://github.com/mriusero/defi-user-behavior-clustering")

        with col_b:
            st.text("")
            st.link_button(
                "See dataset",
                "https://huggingface.co/datasets/mriusero/DeFi-Protocol-Data-on-Ethereum-2023-2024",
            )

        with col_c:
            st.text("")

        with col_d:
            st.text("")

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

    if page == "# Home_":
        page_0()
    elif page == "# Detected User Profiles_":
        page_1()
    elif page == "# Capital Migration Tracking_":
        page_2()
    elif page == "# Anomaly Detection_":
        page_3()
    elif page == "# Summary of Results_":
        page_4()

    st.sidebar.markdown("&nbsp;")

    gc.collect()
