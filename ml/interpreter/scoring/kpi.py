import pandas as pd
import pyarrow as pa
from pyarrow import feather
import matplotlib.pyplot as plt

from .calculate_score import performances_scores
from .checks import check_scores, analyze_distribution

FEATURES_PATH = 'data/features/features_standardised.arrow'
RESULTS_PATH = 'data/clustering/kmeans/kmeans_predictions.arrow'
SCORES_PATH = 'src/frontend/layouts/data/users_scored.arrow'

def merge_data():
    """ Merge the features and results dataframes """
    users = feather.read_table(FEATURES_PATH).to_pandas()
    results = feather.read_table(RESULTS_PATH).to_pandas()
    features = pd.merge(users, results, on='address', how='left')

    features['total_error_exposure'] = features['total_error_exposure'].fillna(0)

    return features

def normalize(series):
    """ Normalize a pandas series """
    return (series - series.min()) / (series.max() - series.min())

def calculate_kpi(features):
    """ Calculate the KPIs """
    print("...calculating KPI")

    df = pd.DataFrame()
    for col in ['address', 'cluster']:
        df[col] = features[col]

    weights = {
        'roi': 0.2,
        'activity_score': 0.15,
        'interaction_diversity': 0.1,
        'engagement_diversity': 0.1,
        'sending_behavior': 0.05,
        'sending_fee_efficiency': 0.05,
        'receiving_behavior': 0.05,
        'receiving_fee_efficiency': 0.05,
        'global_fee_efficiency': 0.05,
        'frequency_efficiency': 0.05,
        'timing_efficiency': 0.05,
        'global_market_exposure_score': 0.05,
        'risk_index': 0.05,
        'opportunity_score': 0.05,
        'performance_index': 0.05,
        'adoption_activity_score': 0.05,
        'stability_index': 0.05,
        'volatility_exposure': 0.05,
        'market_influence': 0.05
    }

    features = performances_scores(features)
    features['global_score'] = normalize(sum(features[score] * weight for score, weight in weights.items()))

    return df.merge(features[['address'] + list(weights.keys()) + ['global_score']], on='address', how='left')


def rank_users(df):
    """ Rank the users by their scores """
    kpi = df.columns.drop(['address', 'cluster']).tolist()

    global_ranks = df[kpi].rank(ascending=False)                                                            # Calculate global ranks
    global_ranks_normalized = global_ranks / len(df)
    global_ranks_normalized = global_ranks_normalized.add_suffix('_global_rank')

    cluster_ranks = df.groupby('cluster')[kpi].rank(ascending=False)                                     # Calculate cluster ranks
    cluster_ranks_normalized = cluster_ranks.groupby(df['cluster']).transform(lambda x: x / x.max())
    cluster_ranks_normalized = cluster_ranks_normalized.add_suffix('_cluster_rank')

    return df.join(global_ranks_normalized).join(cluster_ranks_normalized)


def save_scores(scores):
    """ Save the scores to a feather file """
    table = pa.Table.from_pandas(scores)
    feather.write_feather(table, SCORES_PATH)
    print(f"\nScores saved to {SCORES_PATH}")


def compute_scoring():
    """ Compute the scoring of users """

    features = merge_data()
    result_out_of_bounds, result_nan_inf = check_scores(features.copy().drop(columns=['address', 'cluster']))
    print("Features out of bounds :", result_out_of_bounds)
    print("Features NaN or Inf :", result_nan_inf)

    scores = calculate_kpi(features)
    result_out_of_bounds, result_nan_inf = check_scores(scores.copy().drop(columns=['address', 'cluster']))
    print("Score out of bound :", result_out_of_bounds)
    print("Score NaN or Inf :", result_nan_inf)

    ranks = rank_users(scores)
    analyze_distribution(ranks)

    save_scores(ranks)
    return scores