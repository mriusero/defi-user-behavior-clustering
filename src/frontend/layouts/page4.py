import streamlit as st
from pyarrow import feather

def page_4():
    st.markdown('<div class="header">Who am I ?</div>', unsafe_allow_html=True)

    st.markdown("""
    Give me your ethereum address and I will tell who you are.
    """)
    ranks = feather.read_table('src/frontend/layouts/data/users_scored.arrow').to_pandas()
    st.write(ranks.sample(1000))

    #st.write(ranks.columns.tolist())

    address = st.text_input("Address", value="0x...")

    if st.button("Submit"):
        st.write(f"If your address is {address} then your performances are :".format(address))

        filtered_ranks = ranks[ranks['address'] == address]

        if not filtered_ranks.empty:
            # Extraire les scores généraux
            general_scores = filtered_ranks[['roi', 'activity_score', 'interaction_diversity', 'engagement_diversity',
                                             'sending_behavior', 'sending_fee_efficiency', 'receiving_behavior',
                                             'receiving_fee_efficiency', 'global_fee_efficiency',
                                             'frequency_efficiency',
                                             'timing_efficiency', 'global_market_exposure_score', 'risk_index',
                                             'opportunity_score', 'performance_index', 'adoption_activity_score',
                                             'stability_index', 'volatility_exposure', 'market_influence',
                                             'global_score']].to_dict(orient='records')[0]

            global_performance = filtered_ranks.filter(regex='_global_rank$').to_dict(orient='records')[0]
            cluster_performance = filtered_ranks.filter(regex='_cluster_rank$').to_dict(orient='records')[0]

            structured_data = {
                "address": filtered_ranks['address'].values[0],
                "cluster": filtered_ranks['cluster'].values[0],
                "general_scores": general_scores,
                "global_performance": global_performance,
                "cluster_performance": cluster_performance
            }
            st.json(structured_data)

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
        else:
            st.write("No data found for the given address.")


