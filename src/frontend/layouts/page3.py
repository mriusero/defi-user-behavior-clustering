import streamlit as st


def page_3():
    st.markdown('<div class="header">Clustering_</div>', unsafe_allow_html=True)
    st.write(""" 
    
This section presents the clustering analysis performed on the dataset in the purpose of identifying user behavior patterns.
    
---
    """)
    col1, col2 = st.columns(2)
    with col1:
        st.write("## Clusters_")
        st.image('src/frontend/layouts/pictures/kmeans_analysis/cluster_repartition.png')

        st.write("## Interaction Types_")
        st.image('src/frontend/layouts/pictures/kmeans_analysis/interaction_types_plot.png')

        st.write("## Engagement_")
        st.image('src/frontend/layouts/pictures/kmeans_analysis/protocols_engagement_plot.png')
    with col2:
        st.write("## Transactions Activity_")
        st.image('src/frontend/layouts/pictures/kmeans_analysis/tx_activity_plot.png')

        st.write("## Diversity and Influence_")
        st.image('src/frontend/layouts/pictures/kmeans_analysis/diversity_influence_plot.png')


    col1, col2 = st.columns(2)
    with col1:
        st.write("## Sent Transactions Statistics_")
        st.image('src/frontend/layouts/pictures/kmeans_analysis/sent_tx_statistics.png')
    with col2:
        st.write("## Received Transactions Statistics_")
        st.image('src/frontend/layouts/pictures/kmeans_analysis/received_tx_statistics.png')


    col1, col2 = st.columns(2)
    with col1:
        st.write("## Timing Behavior_")
        st.image('src/frontend/layouts/pictures/kmeans_analysis/timing_behavior_boxplots.png')
    with col2:
        st.write("## Exposure Metrics_")
        st.image('src/frontend/layouts/pictures/kmeans_analysis/exposure_metrics_scatter_plot.png')
        st.image('src/frontend/layouts/pictures/kmeans_analysis/exposure_metrics_box_plot.png')





