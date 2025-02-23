from src.backend.report.ranking import fetch_rank
from src.backend.report.plot_radar import upper_and_lower_bounds, plot_radar_chart
from src.backend.report.reporting import display_board

def get_cluster_desc(ranks, address):
    """ Get cluster description according to a given address """
    cluster_descriptions = {
        0: "Small Investors - Characterized by low transaction volume and frequency, limited platform activity, minimal market exposure.",
        1: "Active Investors - Characterized by moderate transaction activity, diverse interactions including loans and trades, moderate market exposure.",
        2: "Whales - Characterized by high transaction volume and frequency, significant market influence, diverse asset holdings.",
        3: "Explorers - Characterized by moderate transaction activity, high diversity in interactions and assets, limited market influence."
    }
    cluster_id = ranks[ranks['address'] == address]['cluster'].values[0]
    cluster_desc = cluster_descriptions[ranks[ranks['address'] == address]['cluster'].values[0]]
    return f"*''Cluster {cluster_id} - {cluster_desc}''*"


def get_radar(ranks, user_data):
    """ Display radar chart for global and cluster ranks """
    bounds = upper_and_lower_bounds(ranks)
    global_radar = plot_radar_chart(bounds, user_data, to_plot='global_rank')
    cluster_radar = plot_radar_chart(bounds, user_data, to_plot='cluster_rank')
    return global_radar, cluster_radar


def recommendations_board(ranks, address):
    """ Display user recommendations board """
    user_data = fetch_rank(ranks, address)
    cluster_desc = get_cluster_desc(ranks, address)

    global_radar, cluster_radar = get_radar(ranks, user_data)

    display_board(
        user_data,
        cluster_desc,
        global_radar,
        cluster_radar
    )