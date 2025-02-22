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
    address = st.text_input("Address", value="0xbc8cbb3bcad18cd64de04a6d53503ccced07ef5b")

    if st.button("Submit"):
        st.write(f"If your address is {address} then your performances are :".format(address))

        user_data = fetch_rank(ranks, address)

        metrics = {}

        for metric in user_data['performances']:
            name = metric['name']
            description = metric['description']
            cluster_rank = metric['cluster_rank']
            global_rank = metric['global_rank']
            metrics[name] = (description, global_rank, cluster_rank)

        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            st.json(user_data)

        with col2:
            st.subheader("Global Performance")
            for name, (description, global_rank, cluster_rank) in metrics.items():
                st.write(f"###### {name.replace("_", " ").title()}:  {global_rank * 100:.2f}%")
                st.progress(global_rank)
                st.write("---")

        with col3:
            st.subheader("Cluster Performance")
            for name, (description, global_rank, cluster_rank) in metrics.items():
                st.write(f"###### {name.replace("_", " ").title()}:  {cluster_rank * 100:.2f}%")
                st.progress(cluster_rank)
                st.write("---")


