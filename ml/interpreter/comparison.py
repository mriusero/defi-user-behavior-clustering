from pyarrow import feather
import pandas as pd
import numpy as np
import json

BASE_PATH = 'data/clustering/kmeans'


def load_predictions(features_path, predictions_path):
    """ Load the predictions and features dataframes and merge them """
    users = feather.read_table(features_path).to_pandas()
    result = feather.read_table(predictions_path).to_pandas()
    df = pd.merge(users, result, on='address', how='left')

    for i in range(4):
        filtered_df = df[df['cluster'] == i]
        feather.write_feather(filtered_df, f'{BASE_PATH}/cluster_{i}.arrow')

    print(f"Clusters saved to {BASE_PATH}")

    return df


def aggregate_metrics(df):
    """ Aggregate metrics for each cluster per category """
    categories = {
        'tx-activity': [
            'received_count', 'total_received_eth', 'sent_count', 'total_sent_eth'
        ],
        'interaction-types': [
            'type_dex', 'type_lending', 'type_stablecoin', 'type_yield_farming', 'type_nft_fi'
        ],
        'protocols-engagement': [
            'curve_dao_count', 'aave_count', 'tether_count', 'uniswap_count', 'maker_count', 'yearn_finance_count',
            'usdc_count', 'dai_count', 'balancer_count', 'harvest_finance_count', 'nftfi_count'
        ],
        'diversity-and-influence': [
            'protocol_type_diversity', 'protocol_name_diversity', 'net_flow_eth', 'whale_score'
        ],
        'sent-tx-statistics': [
            'min_sent_eth', 'avg_sent_eth', 'med_sent_eth', 'max_sent_eth', 'std_sent_eth', 'min_sent_gas',
            'avg_sent_gas', 'med_sent_gas', 'max_sent_gas', 'std_sent_gas', 'avg_gas_efficiency_sent'
        ],
        'received-tx-statistics': [
            'min_received_eth', 'avg_received_eth', 'med_received_eth', 'max_received_eth', 'std_received_eth',
            'min_received_gas',
            'avg_received_gas', 'med_received_gas', 'max_received_gas', 'std_received_gas',
            'avg_gas_efficiency_received'
        ],
        'timing-behavior': [
            'peak_hour_sent', 'peak_count_sent', 'tx_frequency_sent',
            'peak_hour_received', 'peak_count_received', 'tx_frequency_received'
        ],
        'market-exposure': [
            'total_volume_exposure', 'total_volatility_exposure',
            'total_gas_exposure', 'total_error_exposure',
            'total_liquidity_exposure', 'total_activity_exposure',
            'total_user_adoption_exposure', 'total_gas_volatility_exposure',
            'total_error_volatility_exposure', 'total_high_value_exposure'
        ],
    }
    total_addresses = df['address'].nunique()
    address_counts = df.groupby('cluster')['address'].nunique()

    metrics_by_cluster = df.groupby('cluster')[sum(categories.values(), [])].agg(
        ['mean', 'median', 'std', 'var', 'max', 'min'])

    metrics = {
        cluster: {
            'address': int(count),
            'repartition_rate': float(count / total_addresses),
            **{
                category: {
                    col: {
                        'mean': float(metrics_by_cluster.loc[cluster, (col, 'mean')]),
                        'max': float(metrics_by_cluster.loc[cluster, (col, 'max')]),
                        'min': float(metrics_by_cluster.loc[cluster, (col, 'min')]),
                        'std': float(metrics_by_cluster.loc[cluster, (col, 'std')]),
                        'var': float(metrics_by_cluster.loc[cluster, (col, 'var')]),
                        'median': float(metrics_by_cluster.loc[cluster, (col, 'median')]),
                    }
                    for col in cols
                }
                for category, cols in categories.items()
            }
        }
        for cluster, count in address_counts.items()
    }
    metrics_json = json.dumps(metrics, indent=4)

    with open(f'{BASE_PATH}/kmeans_clusters_metrics.json', 'w') as json_file:
        json_file.write(metrics_json)

    print(f"Metrics saved to {BASE_PATH}")

    return metrics


def identify_variance(metrics):
    """ Identify the variance of each metric for each cluster """
    data = {
        'cluster0': {},
        'cluster1': {},
        'cluster2': {},
        'cluster3': {}
    }

    for cluster, metrics in metrics.items():
        for category, submetrics in metrics.items():
            if category != 'address' and category != 'repartition_rate':
                for variable, stats in submetrics.items():
                    for stat, value in stats.items():
                        key = f"{category}_{variable}_{stat}"
                        data[f'cluster{cluster}'][key] = value

    result = pd.DataFrame(data)
    result = result.astype(np.float64)

    result['variance'] = result.var(axis=1, ddof=0)
    result['std_dev'] = result.std(axis=1, ddof=0)

    result = result.sort_values(by='std_dev', ascending=False)
    result.to_csv(f'{BASE_PATH}/kmeans_clusters_variance.csv')

    print(f"Result saved to {BASE_PATH}")

    return result

def clusters_analysis(features_path, predictions_path):
    df = load_predictions(features_path, predictions_path)
    metrics = aggregate_metrics(df)
    result = identify_variance(metrics)
    return result
