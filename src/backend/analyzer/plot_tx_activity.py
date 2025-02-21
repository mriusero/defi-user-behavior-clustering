import matplotlib.pyplot as plt

def plot_tx_activity(hierarchical_metrics, base_path, range_color_map):
    """Plot transaction activity metrics per cluster and save the plot."""
    tx_activity_data = {}
    types = ['min', 'max', 'median', 'mean']

    for cluster, metrics in hierarchical_metrics.items():
        tx_activity_data[cluster] = {
            'received_count': {t: metrics['tx-activity']['received_count'][t] for t in types},
            'total_received_eth': {t: metrics['tx-activity']['total_received_eth'][t] for t in types},
            'sent_count': {t: metrics['tx-activity']['sent_count'][t] for t in types},
            'total_sent_eth': {t: metrics['tx-activity']['total_sent_eth'][t] for t in types}
        }

    _, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()

    metrics_to_plot = ['received_count', 'total_received_eth', 'sent_count', 'total_sent_eth']

    for ax, metric in zip(axes, metrics_to_plot):
        for stat_type, color in range_color_map.items():
            values = [tx_activity_data[cluster][metric][stat_type] for cluster in tx_activity_data]
            x_values = range(len(values))

            if stat_type == 'min' or stat_type == 'max':
                ax.plot(x_values, values, marker='o', linestyle='-', color=color, label=stat_type)
            else:
                ax.plot(x_values, values, marker='o', linestyle='--', color=color, label=stat_type)

            for i, value in enumerate(values):
                if value == 0:
                    ax.plot(i, 0, marker='o', color='silver')

        ax.set_xlabel('Clusters')
        ax.set_ylabel('Value (symlog scale)')
        ax.set_yscale('symlog', linthresh=0.1)
        ax.set_xticks(x_values)
        ax.set_title(metric.replace("_", " ").title() + " per cluster")
        ax.legend(title='Metrics')
        ax.grid(True, axis='x')
        #ax.grid(True, axis='y')

    plt.tight_layout()
    try:
        plt.savefig(f"{base_path}/tx_activity_plot.png")
        print("--> transaction activity plot saved.")
    except FileNotFoundError as exc:
        raise FileNotFoundError("Error: The path does not exist") from exc
