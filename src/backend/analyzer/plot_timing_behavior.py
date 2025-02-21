import matplotlib.pyplot as plt

def plot_timing_metric(ax, metric, data, range_color_map):
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
        color = range_color_map.get(label.lower(), 'silver')
        if label == 'Min' or label == 'Max':
            linestyle = '-'
        else:
            linestyle = '--'
        ax.plot(range(len(clusters)), vals, label=label, marker='o', linestyle=linestyle, color=color)

    ax.set_title(f'{metric.replace("_", " ").title()} Statistics')
    ax.set_xlabel('Clusters')
    ax.set_ylabel('Value')
    ax.set_yscale('symlog', linthresh=0.1)
    ax.set_xticks(range(len(clusters)))
    ax.set_xticklabels(clusters)
    ax.grid(True, axis='x')
    ax.legend(title='Metrics')

def plot_timing_behavior(hierarchical_metrics, base_path, range_color_map):
    """
    Generate and save line plots for timing behavior metrics by cluster.
    """
    timing_behavior_data = {
        cluster: {
            key: [
                metrics['timing-behavior'][key]['min'],
                metrics['timing-behavior'][key]['mean'],
                metrics['timing-behavior'][key]['median'],
                metrics['timing-behavior'][key]['max']
            ]
            for key in [
                'peak_hour_sent', 'peak_count_sent', 'tx_frequency_sent',
                'peak_hour_received', 'peak_count_received', 'tx_frequency_received'
            ]
        }
        for cluster, metrics in hierarchical_metrics.items()
    }

    _, axes = plt.subplots(nrows=3, ncols=2, figsize=(15, 20))

    received_metrics = [
        'peak_hour_received',
        'peak_count_received',
        'tx_frequency_received'
    ]

    sent_metrics = [
        'peak_hour_sent',
        'peak_count_sent',
        'tx_frequency_sent'
    ]

    for ax, metric in zip(axes[:, 0], received_metrics):
        plot_timing_metric(ax, metric, timing_behavior_data, range_color_map)

    for ax, metric in zip(axes[:, 1], sent_metrics):
        plot_timing_metric(ax, metric, timing_behavior_data, range_color_map)

    plt.tight_layout()
    try:
        plt.savefig(f"{base_path}/timing_behavior_plots.png")
        print("--> timing behavior line plots saved.")
        plt.close()
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"--> Error: {base_path} does not exist.") from exc
