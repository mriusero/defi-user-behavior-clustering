import matplotlib.pyplot as plt
import seaborn as sns

def plot_diversity_and_influence(hierarchical_metrics, base_path, range_color_map):
    """Plot and save diversity and influence metrics by cluster."""
    diversity_influence_data = {cluster: metrics['diversity-and-influence']
                                for cluster, metrics in hierarchical_metrics.items()}

    _, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 10))

    metrics_to_plot = ['protocol_type_diversity', 'protocol_name_diversity', 'net_flow_eth', 'whale_score']
    statistics = ['mean', 'max', 'min', 'median']

    for i, (ax, metric) in enumerate(zip(axes.flatten(), metrics_to_plot)):
        for stat in statistics:
            data = {cluster: metrics[metric][stat] for cluster, metrics in diversity_influence_data.items()}
            if stat == 'min' or stat == 'max':
                linestyle = '-'
            else:
                linestyle = '--'
            sns.lineplot(x=list(data.keys()), y=list(data.values()), ax=ax, marker='o', linestyle=linestyle, color=range_color_map[stat], label=stat.capitalize())

        ax.set_title(metric.replace("_", " ").title() + " by Cluster")
        ax.set_ylabel('Value')
        ax.set_xlabel('Clusters')
        ax.legend(title='Metrics')

        if i < 2:
            ax.set_yscale('linear')
        else:
            ax.set_yscale('symlog', linthresh=0.1)
        ax.grid(True, axis='x')
    plt.tight_layout()
    try:
        plt.savefig(f'{base_path}/diversity_influence_plot.png')
        print("--> Diversity and Influence plot saved.")
        plt.close()
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"--> Error: {base_path} does not exist.") from exc
