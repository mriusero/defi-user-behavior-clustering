import pandas as pd

def fetch_rank(ranks: pd.DataFrame, address: str):
    """ Fetch the ranking of a user based on its address """
    filtered_ranks = ranks[ranks['address'] == address]

    if filtered_ranks.empty:
        return None

    user_row = filtered_ranks.iloc[0].to_dict()

    metrics = [
        'roi', 'activity_score', 'interaction_diversity', 'engagement_diversity',
        'sending_behavior', 'sending_fee_efficiency', 'receiving_behavior',
        'receiving_fee_efficiency', 'global_fee_efficiency', 'frequency_efficiency',
        'timing_efficiency', 'global_market_exposure_score', 'risk_index',
        'opportunity_score', 'performance_index', 'adoption_activity_score',
        'stability_index', 'volatility_exposure', 'market_influence', 'global_score'
    ]

    cluster_descriptions = {
        0: "Small Investors - Characterized by low transaction volume and frequency, limited platform activity, minimal market exposure.",
        1: "Active Investors - Characterized by moderate transaction activity, diverse interactions including loans and trades, moderate market exposure.",
        2: "Whales - Characterized by high transaction volume and frequency, significant market influence, diverse asset holdings.",
        3: "Explorers - Characterized by moderate transaction activity, high diversity in interactions and assets, limited market influence."
    }

    metric_descriptions = {
        'roi': 'Return on Investment. High value indicates high profitability, while low value suggests low profitability or loss.',
        'activity_score': 'User activity score. High value indicates active participation, low value suggests inactivity.',
        'interaction_diversity': 'Diversity in user interactions. High value indicates varied interactions, low value suggests limited diversity.',
        'engagement_diversity': 'Diversity in engagement types. High value indicates broad engagement, low value suggests limited engagement.',
        'sending_behavior': 'Sending transaction behavior. High value indicates active and varied sending, low value suggests inactivity.',
        'sending_fee_efficiency': 'Efficiency of sending transaction fees. High value indicates efficient gas fee usage, low value suggests inefficiency.',
        'receiving_behavior': 'Receiving transaction behavior. High value indicates active and varied receiving, low value suggests inactivity.',
        'receiving_fee_efficiency': 'Efficiency of receiving transaction fees. High value indicates efficient gas fee usage, low value suggests inefficiency.',
        'global_fee_efficiency': 'Overall fee efficiency. High value indicates efficient gas fee usage, low value suggests inefficiency.',
        'frequency_efficiency': 'Transaction frequency efficiency. High value indicates optimal frequency, low value suggests irregularity.',
        'timing_efficiency': 'Transaction timing efficiency. High value indicates optimal timing (off-peak), low value suggests inefficiency (peak hours).',
        'global_market_exposure_score': 'Global market exposure score. High value indicates strong exposure, low value suggests limited exposure.',
        'risk_index': 'Risk level index. High value indicates low risk, low value suggests high risk.',
        'opportunity_score': 'Potential opportunities score. High value indicates many opportunities, low value suggests few opportunities.',
        'performance_index': 'Performance index. High value indicates high performance relative to risk, low value suggests low performance.',
        'adoption_activity_score': 'Adoption activity score. High value indicates strong user adoption, low value suggests limited activity.',
        'stability_index': 'Stability index. High value indicates high stability, low value suggests volatility.',
        'volatility_exposure': 'Market volatility exposure. High value indicates low exposure, low value suggests high exposure.',
        'market_influence': 'Market influence. High value indicates strong influence, low value suggests limited influence.',
        'global_score': 'Overall global score. High value indicates strong performance, low value suggests weak performance.'
    }

    performances = [
        {
            "name": metric,
            "description": metric_descriptions.get(metric, "Description not available"),
           # "value": user_row[metric],
            "cluster_rank": user_row.get(f"{metric}_cluster_rank", "Cluster rank not available"),
            "global_rank": user_row.get(f"{metric}_global_rank", "Global rank not available")
        }
        for metric in metrics
    ]

    cluster_id = user_row['cluster']
    cluster_description = cluster_descriptions.get(cluster_id, "Unknown Cluster")

    user_data = {
        "address": user_row['address'],
        "cluster": {
            "id": format(cluster_id),
            "description": f"Cluster representing a group of users with similar characteristics and behaviors. Here, the user is in the cluster {cluster_id} which are classified as {cluster_description}"
        },
        "performances": performances
    }
    return user_data