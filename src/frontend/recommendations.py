import streamlit as st

from src.backend.core.ranking import fetch_rank
from src.backend.core.plot_radar import upper_and_lower_bounds, plot_radar_chart


def get_description(ranks, address):
    """ Get cluster description according to a given address """
    cluster_descriptions = {
        0: "Small Investors - Characterized by low transaction volume and frequency, limited platform activity, minimal market exposure.",
        1: "Active Investors - Characterized by moderate transaction activity, diverse interactions including loans and trades, moderate market exposure.",
        2: "Whales - Characterized by high transaction volume and frequency, significant market influence, diverse asset holdings.",
        3: "Explorers - Characterized by moderate transaction activity, high diversity in interactions and assets, limited market influence."
    }
    cluster_id = ranks[ranks['address'] == address]['cluster'].values[0]
    cluster_desc = cluster_descriptions[ranks[ranks['address'] == address]['cluster'].values[0]]
    st.write(f"*''Cluster {cluster_id} - {cluster_desc}''*")


def display_radar(ranks, user_data):
    """ Display radar chart for global and cluster ranks """

    bounds = upper_and_lower_bounds(ranks)

    global_radar = plot_radar_chart(bounds, user_data, to_plot='global_rank')
    cluster_radar = plot_radar_chart(bounds, user_data, to_plot='cluster_rank')
    col1, col2 = st.columns([1, 1])
    with col1:
        st.pyplot(global_radar)
    with col2:
        st.pyplot(cluster_radar)


def display_metrics(user_data):
    """ Display user metrics """
    st.write("---")
    st.json(user_data)
    st.write("---")


def display_rates(user_data):
    """ Display user rates on progress bars with custom CSS. """
    metrics = {}
    for metric in user_data['performances']:
        name = metric['name']
        description = metric['description']
        cluster_rank = metric['cluster_rank']
        global_rank = metric['global_rank']
        metrics[name] = (description, global_rank, cluster_rank)

    custom_css = """
                <style>
                .progress-container {
                    position: relative;
                    width: 100%;
                    height: 40px;
                    background-color: #e0e0e0;
                    border-radius: 5px;
                    overflow: hidden;
                    margin-bottom: 10px;
                }
                .progress-bar {
                    height: 100%;
                    background-color: #1e8b22;
                    position: absolute;
                    top: 0;
                    left: 0;
                    border-radius: 5px;
                }
                .progress-text {
                    position: absolute;
                    width: 100%;
                    text-align: center;
                    font-size: 16px;
                    font-weight: bold;
                    line-height: 40px;
                    color: #333;
                }
                </style>
                """

    st.markdown(custom_css, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 2, 2])

    with col1:
        st.write("#### Global Performance")
        st.write("---")
        for name, (description, global_rank, cluster_rank) in list(metrics.items())[:10]:
            progress_width = f"{global_rank * 100}%"
            percentage = f"{global_rank * 100:.1f}%"
            st.markdown(f"""
                        <div class='progress-container'>
                            <div class='progress-bar' style='width: {progress_width};'></div>
                            <div class='progress-text'>{name.replace('_', ' ').title()} ({percentage})</div>
                        </div>
                        """, unsafe_allow_html=True)

    with col2:
        st.write("#### ")
        st.write("---")
        for name, (description, global_rank, cluster_rank) in list(metrics.items())[10:]:
            progress_width = f"{global_rank * 100}%"
            percentage = f"{global_rank * 100:.1f}%"
            st.markdown(f"""
                        <div class='progress-container'>
                            <div class='progress-bar' style='width: {progress_width};'></div>
                            <div class='progress-text'>{name.replace('_', ' ').title()} ({percentage})</div>
                        </div>
                        """, unsafe_allow_html=True)

    with col3:
        st.write("#### ")
        st.write("---")

    with col4:
        st.write("#### Cluster Performance")
        st.write("---")
        for name, (description, global_rank, cluster_rank) in list(metrics.items())[:10]:
            progress_width = f"{cluster_rank * 100}%"
            percentage = f"{cluster_rank * 100:.1f}%"
            st.markdown(f"""
                        <div class='progress-container'>
                            <div class='progress-bar' style='width: {progress_width};'></div>
                            <div class='progress-text'>{name.replace('_', ' ').title()} ({percentage})</div>
                        </div>
                        """, unsafe_allow_html=True)

    with col5:
        st.write("#### ")
        st.write("---")
        for name, (description, global_rank, cluster_rank) in list(metrics.items())[10:]:
            progress_width = f"{cluster_rank * 100}%"
            percentage = f"{cluster_rank * 100:.1f}%"
            st.markdown(f"""
                        <div class='progress-container'>
                            <div class='progress-bar' style='width: {progress_width};'></div>
                            <div class='progress-text'>{name.replace('_', ' ').title()} ({percentage}</div>
                        </div>
                        """, unsafe_allow_html=True)

def recommendations_board(ranks, address):
    user_data = fetch_rank(ranks, address)

    get_description(ranks, address)

    st.write("### Scores_")
    display_radar(ranks, user_data)

    st.write("### Analysis_")
    display_metrics(user_data)

    display_rates(user_data)

