import streamlit as st
from pyarrow import feather

from src.backend.core.ranking import fetch_rank


@st.cache_data
def pre_load_ranks():
    ranks = feather.read_table('src/frontend/layouts/data/users_scored.arrow').to_pandas()
    return ranks



def page_4():
    st.markdown('<div class="header">Who am I ?</div>', unsafe_allow_html=True)

    st.markdown("""
    Give me your ethereum address and I will tell who you are.
    """)
    ranks = pre_load_ranks()
    st.write(ranks.sample(5))
    address = st.text_input("Address", value="0x...")

    if st.button("Submit"):
        st.write(f"If your address is {address} then your performances are :".format(address))

        address_score = fetch_rank(ranks, address)

        global_performance = address_score['global_performance']
        cluster_performance = address_score['cluster_performance']

        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("Global Performance")
            for key, value in global_performance.items():
                st.progress(value / 1)
                st.write(f"{key}: {value}")

        with col2:
            st.subheader("Cluster Performance")
            for key, value in cluster_performance.items():
                st.progress(value / 1)
                st.write(f"{key}: {value}")