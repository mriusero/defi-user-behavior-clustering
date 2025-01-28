import streamlit as st

from src.backend.core.visualise import DataVisualizer

def page_1():
    st.markdown(
        '<div class="header">#1 Exploratory Data Analysis_</div>',
        unsafe_allow_html=True,
    )
    dataframes = st.session_state.get("dataframes")

    for key, df in dataframes.items():

        st.markdown(f"### DataFrame `{key.capitalize()}`")
        viz = DataVisualizer(df)

        col1, col2 = st.columns([1, 3])

        with col1:
            st.write(list(df.columns))
            viz.missing_data()

        with col2:
            st.write("")
            viz.show_dataframe()

            if key != "contracts":
                viz.summarize_data()

            if key == "users" or key == "market":
                viz.plot_correlation_heatmap()