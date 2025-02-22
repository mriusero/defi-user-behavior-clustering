import pandas as pd
import streamlit as st

def fetch_rank(ranks: pd.DataFrame, address: str):
    """ Fetch the ranking of a user based on its address """
    filtered_ranks = ranks[ranks['address'] == address]

    if not filtered_ranks.empty:
        general_scores = filtered_ranks[
            [
                'roi', 'activity_score', 'interaction_diversity', 'engagement_diversity',
                'sending_behavior', 'sending_fee_efficiency', 'receiving_behavior',
                'receiving_fee_efficiency', 'global_fee_efficiency',
                'frequency_efficiency',
                'timing_efficiency', 'global_market_exposure_score', 'risk_index',
                'opportunity_score', 'performance_index', 'adoption_activity_score',
                'stability_index', 'volatility_exposure', 'market_influence',
                'global_score'
            ]
        ].to_dict(orient='records')[0]

        global_performance = filtered_ranks.filter(regex='_global_rank$').to_dict(orient='records')[0]
        cluster_performance = filtered_ranks.filter(regex='_cluster_rank$').to_dict(orient='records')[0]

        pre_prompt = """
You are a data analyst specializing in evaluating user performance based on various metrics. Your task is to analyze your performance data, provided in JSON format, and present the results as a detailed and structured report in Markdown format. Here's what you need to do:

1. **Understand the Metrics:**
   - Familiarize yourself with the metric descriptions provided in the JSON. Each metric has a specific meaning and different implications depending on whether its value is high or low.

2. **Analyze Your Performance:**
   - **Metric Values:** Examine your metric values.
   - **Global Comparison:** Compare your metric values with the global ranks (global_rank) to understand how you stand relative to all users.
   - **Cluster Comparison:** Compare your metric values with the ranks within your cluster (cluster_rank) to evaluate your performance relative to users with similar characteristics.

3. **Interpret the Results:**
   - **Strengths:** Identify metrics where you excel, both globally and within your cluster.
   - **Areas for Improvement:** Highlight areas where you could improve, especially if your ranks are low compared to both comparison groups.
   - **Recommendations:** Provide actionable recommendations based on these observations to help you enhance your performance.

4. **Summary:**
   - Summarize your conclusions by emphasizing your strengths and areas for improvement.

5. **Format the Report:**
   - **Markdown Structure:** Ensure the report is formatted in Markdown with clear headings, bullet points, and tables where necessary.
   - **Readability:** Use a conversational tone and ensure the report is easy to read and understand.
   - **Insights:** Present the insights in a way that is engaging and informative for the user.

### Report Structure Example:

```markdown
# Performance Analysis Report

## Interpretation

### Strengths

- Metric 1: Explanation of why this is a strength.
- Metric 2: Explanation of why this is a strength.
- ...

### Areas for Improvement

- Metric 3: Explanation of why this needs improvement.
- Metric 4: Explanation of why this needs improvement.
- ...

### Recommendations

- Recommendation 1: Actionable steps.
- Recommendation 2: Actionable steps.
- ...

## Summary

- Emphasize your strengths.
- Highlight areas for improvement.
- Provide a brief overview of the recommendations.

By following this structure, you will create a comprehensive and well-organized report that is both informative and engaging for the user.
        """

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

        performances = []

        for metric, value in general_scores.items():
            performances.append({
                "name": metric,
                "description": metric_descriptions.get(metric, "Description not available"),
                "value": value,
                "cluster_rank": cluster_performance.get(f"{metric}_cluster_rank", "Cluster rank not available"),
                "global_rank": global_performance.get(f"{metric}_global_rank", "Global rank not available")
            })

        cluster_id = filtered_ranks['cluster'].values[0]
        cluster_description = cluster_descriptions.get(cluster_id, "Unknown Cluster")

        structured_data = {
            "pre_prompt": pre_prompt,
            "address": filtered_ranks['address'].values[0],
            "cluster": {
                "id": format(cluster_id),
                "description": f"Cluster representing a group of users with similar characteristics and behaviors. Here, the user is in the cluster {cluster_id} which are classified as {cluster_description}"
            },
            "performances": performances
        }

        st.json(structured_data)

        return structured_data
