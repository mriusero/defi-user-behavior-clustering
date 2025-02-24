import streamlit as st

from src.backend.reporting.ranking import fetch_rank
from src.backend.reporting.plot_radar import upper_and_lower_bounds, plot_radar_chart
from src.backend.reporting.display_kpi import display_kpi
from src.backend.reporting.inference import display_report

def get_radar(ranks, user_data):
    """ Display radar chart for global and cluster ranks """
    bounds = upper_and_lower_bounds(ranks)
    global_radar = plot_radar_chart(bounds, user_data, to_plot='global_rank')
    cluster_radar = plot_radar_chart(bounds, user_data, to_plot='cluster_rank')
    return global_radar, cluster_radar


def recommendations_board(ranks, address):
    """ Display user recommendations board """
    # Fetch metrics and cluster description of the user
    user_data = fetch_rank(ranks, address)

    # Display user information for introduction
    cluster_desc = user_data['cluster'].get('description', "Unknown Cluster")
    st.write(cluster_desc)
    st.write("---")

    # Display text-to-text reporting generated
    display_report(user_data, really=True)
    st.write("---")

    # Display radar charts and KPI for global and cluster ranks
    global_radar, cluster_radar = get_radar(ranks, user_data)
    display_kpi(
        user_data,
        global_radar,
        cluster_radar
    )