import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_engagement(hierarchical_metrics, base_path, qualitative_cmap):
    """Plot and save stacked bar plots of protocols engagement by cluster with a heatmap of percentage values."""
    protocols_data = {cluster: {protocol: metrics['protocols-engagement'][protocol]['mean']
                                for protocol in metrics['protocols-engagement']}
                      for cluster, metrics in hierarchical_metrics.items()}

    clusters = list(protocols_data.keys())
    protocols = list(protocols_data[clusters[0]].keys())

    data = np.array([[protocols_data[cluster][protocol] for protocol in protocols] for cluster in clusters])

    data_percentage = data / data.sum(axis=1, keepdims=True) * 100

    _, ax = plt.subplots(2, 1, figsize=(10, 10), gridspec_kw={'height_ratios': [3, 1]})

    cmap = plt.cm.get_cmap(qualitative_cmap)
    colors = cmap(range(len(protocols)))

    bottom_values = np.zeros(len(clusters))
    for i, protocol in enumerate(protocols):
        ax[0].bar(clusters, data[:, i], bottom=bottom_values, label=protocol, color=colors[i])
        bottom_values += data[:, i]

    ax[0].set_ylabel('Mean Engagement')
    ax[0].set_title('Mean Engagement Stacked Bar Plot')
    ax[0].legend(title='Protocols')

    sns.heatmap(data_percentage.T, ax=ax[1], cmap='YlGnBu', annot=True, fmt=".1f", xticklabels=clusters, yticklabels=protocols)
    ax[1].set_title('Heatmap of Protocols Engagement by Cluster (Percentage)')
    ax[1].set_xlabel('Cluster')
    ax[1].set_ylabel('Protocol')

    plt.tight_layout()
    try:
        plt.savefig(f'{base_path}/protocols_engagement_plot.png')
        print("--> protocols engagement plot saved.")
        plt.close()
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"--> Error: {base_path} does not exist.") from exc
