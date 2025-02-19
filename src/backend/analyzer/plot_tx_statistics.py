import matplotlib.pyplot as plt
import numpy as np

def plot_sent_tx_statistics(hierarchical_metrics, base_path):
    """Plot sent TX statistics by cluster and save the figure."""
    sent_tx_data = {
        cluster: {
            key: [
                metrics['sent-tx-statistics'][key]['min'],
                metrics['sent-tx-statistics'][key]['mean'],
                metrics['sent-tx-statistics'][key]['median'],
                metrics['sent-tx-statistics'][key]['max']
            ]
            for key in [
                'min_sent_eth', 'avg_sent_eth', 'med_sent_eth', 'max_sent_eth', 'std_sent_eth',
                'min_sent_gas', 'avg_sent_gas', 'med_sent_gas', 'max_sent_gas', 'std_sent_gas', 'avg_gas_efficiency_sent'
            ]
        }
        for cluster, metrics in hierarchical_metrics.items()
    }

    fig, axes = plt.subplots(nrows=6, ncols=2, figsize=(15, 30))
    fig.suptitle('Sent TX Transactions Statistics by Cluster', fontsize=16)

    metrics_eth = ['min_sent_eth', 'avg_sent_eth', 'med_sent_eth', 'max_sent_eth', 'std_sent_eth']
    metrics_gas = ['min_sent_gas', 'avg_sent_gas', 'med_sent_gas', 'max_sent_gas', 'std_sent_gas', 'avg_gas_efficiency_sent']

    def plot_metric(ax, metric, data):
        clusters = list(data.keys())

        min_values = []
        max_values = []
        mean_values = []
        median_values = []

        try:
            for cluster_data in data.values():
                if metric in cluster_data:
                    min_values.append(cluster_data[metric][0])
                    max_values.append(cluster_data[metric][3])
                    mean_values.append(cluster_data[metric][1])
                    median_values.append(cluster_data[metric][2])
                else:
                    min_values.append(None)
                    max_values.append(None)
                    mean_values.append(None)
                    median_values.append(None)

            ax.plot(range(len(clusters)), min_values, label='Min', marker='o', linestyle='--')
            ax.plot(range(len(clusters)), max_values, label='Max', marker='o', linestyle='--')
            ax.plot(range(len(clusters)), mean_values, label='Mean', marker='o', linestyle='--')
            ax.plot(range(len(clusters)), median_values, label='Median', marker='o', linestyle='--')

            ax.set_title(f'{metric.replace("_", " ").title()} Statistics')
            ax.set_xlabel('Cluster')
            ax.set_ylabel('Value')
            ax.set_yscale('symlog', linthresh=0.1)
            ax.set_xticks(range(len(clusters)))
            ax.set_xticklabels(clusters)
            ax.legend()
        except KeyError as e:
            ax.set_title(f'{metric.replace("_", " ").title()} Statistics (Missing Data)')
            print(f"Missing data for metric: {e}")

    for ax, metric in zip(axes[:, 0], metrics_eth):
        plot_metric(ax, metric, sent_tx_data)

    for ax, metric in zip(axes[:, 1], metrics_gas):
        plot_metric(ax, metric, sent_tx_data)

    plt.tight_layout(rect=[0, 0, 1, 0.95])

    try:
        plt.savefig(f"{base_path}/sent_tx_statistics.png")
        print(f"--> sent TX statistics plot saved.")
        plt.close()
    except FileNotFoundError:
        raise FileNotFoundError(f"Directory {base_path} does not exist.")

def plot_received_tx_statistics(hierarchical_metrics, base_path):
    """Plot received TX statistics by cluster and save the figure."""
    sent_tx_data = {
        cluster: {
            key: [
                metrics['received-tx-statistics'][key]['min'],
                metrics['received-tx-statistics'][key]['mean'],
                metrics['received-tx-statistics'][key]['median'],
                metrics['received-tx-statistics'][key]['max']
            ]
            for key in [
                'min_received_eth', 'avg_received_eth', 'med_received_eth', 'max_received_eth', 'std_received_eth',
                'min_received_gas', 'avg_received_gas', 'med_received_gas', 'max_received_gas', 'std_received_gas', 'avg_gas_efficiency_received'
            ]
        }
        for cluster, metrics in hierarchical_metrics.items()
    }

    fig, axes = plt.subplots(nrows=6, ncols=2, figsize=(15, 30))
    fig.suptitle('Received Transactions Statistics by Cluster', fontsize=16)

    metrics_eth = ['min_received_eth', 'avg_received_eth', 'med_received_eth', 'max_received_eth', 'std_received_eth']
    metrics_gas = ['min_received_gas', 'avg_received_gas', 'med_received_gas', 'max_received_gas', 'std_received_gas', 'avg_gas_efficiency_received']

    def plot_metric(ax, metric, data):
        clusters = list(data.keys())

        min_values = []
        max_values = []
        mean_values = []
        median_values = []

        try:
            for cluster_data in data.values():
                if metric in cluster_data:
                    min_values.append(cluster_data[metric][0])
                    max_values.append(cluster_data[metric][3])
                    mean_values.append(cluster_data[metric][1])
                    median_values.append(cluster_data[metric][2])
                else:
                    min_values.append(None)
                    max_values.append(None)
                    mean_values.append(None)
                    median_values.append(None)

            ax.plot(range(len(clusters)), min_values, label='Min', marker='o', linestyle='--')
            ax.plot(range(len(clusters)), max_values, label='Max', marker='o', linestyle='--')
            ax.plot(range(len(clusters)), mean_values, label='Mean', marker='o', linestyle='--')
            ax.plot(range(len(clusters)), median_values, label='Median', marker='o', linestyle='--')

            ax.set_title(f'{metric.replace("_", " ").title()} Statistics')
            ax.set_xlabel('Cluster')
            ax.set_ylabel('Value')
            ax.set_yscale('symlog', linthresh=0.1)
            ax.set_xticks(range(len(clusters)))
            ax.set_xticklabels(clusters)
            ax.legend()
        except KeyError as e:
            ax.set_title(f'{metric.replace("_", " ").title()} Statistics (Missing Data)')
            print(f"Missing data for metric: {e}")

    for ax, metric in zip(axes[:, 0], metrics_eth):
        plot_metric(ax, metric, sent_tx_data)

    for ax, metric in zip(axes[:, 1], metrics_gas):
        plot_metric(ax, metric, sent_tx_data)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    try:
        plt.savefig(f"{base_path}/received_tx_statistics.png")
        print(f"--> received TX statistics plot saved.")
        plt.close()
    except FileNotFoundError:
        raise FileNotFoundError(f"Directory {base_path} does not exist.")