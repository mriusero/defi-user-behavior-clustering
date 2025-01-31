import streamlit as st

from src.backend.ml.processing.distribution_analysis import statistical_tests

def page_3():
    st.markdown('<div class="header">#3 Statistics_</div>', unsafe_allow_html=True)

    st.write("""
> Before perform statistical test, features engineering have to be done first.
    """)


    if st.button("Run Statistical Tests"):
        statistical_tests()

    with open("docs/statistical_analysis.md", "r", encoding="utf-8") as file:
        markdown_content = file.read()
    st.markdown(markdown_content, unsafe_allow_html=True)

    with open("data/features/statistical_analysis.json", "r", encoding="utf-8") as file:
        json_content = file.read()
    st.json(json_content)

