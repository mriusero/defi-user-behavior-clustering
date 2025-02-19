import matplotlib.pyplot as plt
import seaborn as sns

def plot_diversity_and_influence(hierarchical_metrics, base_path):
    """Plot and save diversity and influence metrics by cluster."""
    diversity_influence_data = {cluster: metrics['diversity-and-influence']
                                for cluster, metrics in hierarchical_metrics.items()}

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 10))
    fig.suptitle('Diversity and Influence Metrics by Cluster', fontsize=16)

    metrics_to_plot = ['protocol_type_diversity', 'protocol_name_diversity', 'net_flow_eth', 'whale_score']

    for i, (ax, metric) in enumerate(zip(axes.flatten(), metrics_to_plot)):
        mean_data = {cluster: metrics[metric]['mean'] for cluster, metrics in diversity_influence_data.items()}
        max_data = {cluster: metrics[metric]['max'] for cluster, metrics in diversity_influence_data.items()}
        min_data = {cluster: metrics[metric]['min'] for cluster, metrics in diversity_influence_data.items()}
        median_data = {cluster: metrics[metric]['median'] for cluster, metrics in diversity_influence_data.items()}

        sns.lineplot(x=list(mean_data.keys()), y=list(mean_data.values()), ax=ax, marker='o', label='Mean', color='skyblue')
        sns.lineplot(x=list(max_data.keys()), y=list(max_data.values()), ax=ax, marker='o', linestyle='--', color='green', label='Max')
        sns.lineplot(x=list(min_data.keys()), y=list(min_data.values()), ax=ax, marker='o', linestyle='--', color='red', label='Min')
        sns.lineplot(x=list(median_data.keys()), y=list(median_data.values()), ax=ax, marker='o', linestyle='--', color='purple', label='Median')

        ax.set_title(f'{metric.replace("_", " ").title()} by Cluster')
        ax.set_ylabel('Value')
        ax.set_xlabel('Cluster')
        ax.legend()

        if i < 2:
            ax.set_yscale('linear')
        else:
            ax.set_yscale('symlog', linthresh=0.1)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    try :
        plt.savefig(f'{base_path}/diversity_influence_plot.png')
        print(f"--> Diversity and Influence plot saved.")
        plt.close()
    except FileNotFoundError:
        raise FileNotFoundError(f"--> Error: {base_path} does not exist.")
