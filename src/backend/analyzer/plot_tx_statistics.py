import matplotlib.pyplot as plt

def plot_metric(ax, metric, data):
    clusters = list(data.keys())
    values = {label: [] for label in ['Min', 'Max', 'Mean', 'Median']}

    for cluster_data in data.values():
        if metric in cluster_data:
            values['Min'].append(cluster_data[metric][0])
            values['Max'].append(cluster_data[metric][3])
            values['Mean'].append(cluster_data[metric][1])
            values['Median'].append(cluster_data[metric][2])
        else:
            for label in values:
                values[label].append(None)

    for label, vals in values.items():
        ax.plot(range(len(clusters)), vals, label=label, marker='o', linestyle='--')

    ax.set_title(f'{metric.replace("_", " ").title()} Statistics')
    ax.set_xlabel('Cluster')
    ax.set_ylabel('Value')
    ax.set_yscale('symlog', linthresh=0.1)
    ax.set_xticks(range(len(clusters)))
    ax.set_xticklabels(clusters)
    ax.legend()

def plot_tx_statistics(hierarchical_metrics, base_path, tx_type):
    """Plot TX statistics by cluster and save the figure."""
    tx_key = f"{tx_type}-tx-statistics"

    metrics_keys = {
        'eth': [f'{suffix}_{tx_type}_eth' for suffix in ['min', 'avg', 'med', 'max', 'std']],
        'gas': [f'{suffix}_{tx_type}_gas' for suffix in ['min', 'avg', 'med', 'max', 'std']] + [f'avg_gas_efficiency_{tx_type}']
    }

    tx_data = {
        cluster: {
            key: [
                metrics[tx_key][key]['min'],
                metrics[tx_key][key]['mean'],
                metrics[tx_key][key]['median'],
                metrics[tx_key][key]['max']
            ]
            for key in metrics_keys['eth'] + metrics_keys['gas']
        }
        for cluster, metrics in hierarchical_metrics.items()
    }

    fig, axes = plt.subplots(nrows=6, ncols=2, figsize=(15, 30))
    fig.suptitle(f'{tx_type.capitalize()} Transactions Statistics by Cluster', fontsize=16)

    for ax, metric in zip(axes[:, 0], metrics_keys['eth']):
        plot_metric(ax, metric, tx_data)

    for ax, metric in zip(axes[:, 1], metrics_keys['gas']):
        plot_metric(ax, metric, tx_data)

    plt.tight_layout(rect=[0, 0, 1, 0.95])

    try:
        plt.savefig(f"{base_path}/{tx_type}_tx_statistics.png")
        print(f"--> {tx_type} TX statistics plot saved.")
        plt.close()
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Directory {base_path} does not exist.") from exc
