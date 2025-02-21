import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_interaction_types(hierarchical_metrics, base_path, qualitative_cmap):
    """Plot interaction types metrics per cluster and save the plot with a heatmap of percentage values."""
    interaction_types_data = {}
    for cluster, metrics in hierarchical_metrics.items():
        interaction_types_data[cluster] = {
            interaction_type: metrics['interaction-types'][interaction_type]['mean']
            for interaction_type in metrics['interaction-types']
        }

    clusters = list(interaction_types_data.keys())
    interaction_types = list(interaction_types_data[clusters[0]].keys())
    data = np.array([[interaction_types_data[cluster][interaction_type] for interaction_type in interaction_types] for cluster in clusters])

    # Normalize data to percentages
    data_percentage = data / data.sum(axis=1, keepdims=True) * 100

    _, ax = plt.subplots(2, 1, figsize=(10, 10), gridspec_kw={'height_ratios': [3, 1]})

    cmap = plt.cm.get_cmap(qualitative_cmap)
    colors = cmap.colors[:len(interaction_types)]

    bottom_values = np.zeros(len(clusters))
    for i, interaction_type in enumerate(interaction_types):
        ax[0].bar(clusters, data[:, i], bottom=bottom_values, label=interaction_type, color=colors[i])
        bottom_values += data[:, i]

    ax[0].set_ylabel('Mean Interaction')
    ax[0].set_xlabel('Cluster')
    ax[0].set_title('Stacked Bar Plot of Interaction Types by Cluster')
    ax[0].legend(title='Interaction Types')

    # Create the heatmap
    sns.heatmap(data_percentage.T, ax=ax[1], cmap='YlGnBu', annot=True, fmt=".1f", xticklabels=clusters, yticklabels=interaction_types)
    ax[1].set_title('Heatmap of Interaction Types by Cluster (Percentage)')
    ax[1].set_xlabel('Cluster')
    ax[1].set_ylabel('Interaction Type')

    plt.tight_layout()

    try:
        plt.savefig(f"{base_path}/interaction_types_plot.png")
        print("--> interaction types plot saved.")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Directory {base_path} does not exist.") from exc
