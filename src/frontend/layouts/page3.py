import streamlit as st
import streamlit.components.v1 as components

#from src.backend.analyzer.plotter import analyze_clusters

def page_3():
    st.markdown('<div class="header">Clustering_</div>', unsafe_allow_html=True)
    st.write(""" 
    
This section presents the clustering analysis performed on the dataset in the purpose of identifying user behavior patterns. The clusters are described with their characteristics, interactions types, correlation matrix, transactions activity, diversity and influence, sent and received transactions statistics, exposure metrics and timing behavior.

---
    """)

    #if st.button("Reload graphs"):
    #    analyze_clusters()

    col1, col2 = st.columns(2)
    with col1:
        st.write("## Identified Clusters_")
        st.image('src/frontend/layouts/pictures/kmeans_analysis/cluster_repartition.png')
    with col2:
        st.write("## Synthesis_")
        st.write("""
        * **Cluster 0 (Small Investors)** - *Low transaction volume and frequency, limited platform activity, minimal market exposure.*
        
        * **Cluster 1 (Active Investors)** - *Moderate transaction activity, diverse interactions including loans and trades, moderate market exposure.*
        * **Cluster 2 (Whales)** - *High transaction volume and frequency, significant market influence, diverse asset holdings.*
        * **Cluster 3 (Explorers)** - *Moderate transaction activity, high diversity in interactions and assets, limited market influence.*
        """)

    st.write("## Interaction Types_")
    col1, col2 = st.columns(2)
    with col1:
        st.image('src/frontend/layouts/pictures/kmeans_analysis/interaction_types_plot.png')
    with col2:
        st.image('src/frontend/layouts/pictures/kmeans_analysis/protocols_engagement_plot.png')

    st.write("## Correlation matrix_")
    st.image('src/frontend/layouts/pictures/kmeans_analysis/general_heatmap.png')

    col1, col2 = st.columns(2)
    with col1:
        st.write("## Transactions Activity_")
        st.image('src/frontend/layouts/pictures/kmeans_analysis/tx_activity_plot.png')
    with col2:
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
        st.write("## Exposure Metrics_")
        st.image('src/frontend/layouts/pictures/kmeans_analysis/exposure_metrics_plot.png')
    with col2:
        st.write("## Timing Behavior_")
        st.image('src/frontend/layouts/pictures/kmeans_analysis/timing_behavior_plots.png')

    col1, col2 = st.columns(2)
    html_files = [f'src/frontend/layouts/pictures/kmeans_analysis/heatmap_{i}.html' for i in range(4)]
    for i, html_file in enumerate(html_files):
        with open(html_file, 'r', encoding='utf-8') as file:
            html_content = file.read()

            if i % 2 == 0:
                with col1:
                    st.write(f"## Heatmap Cluster_{i}")
                    components.html(html_content, height=500)
            else:
                with col2:
                    st.write(f"## Heatmap Cluster_{i}")
                    components.html(html_content, height=500)
