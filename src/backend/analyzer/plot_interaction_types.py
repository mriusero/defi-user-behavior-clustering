import numpy as np
import matplotlib.pyplot as plt

def plot_interaction_types(hierarchical_metrics, base_path):
    """Plot interaction types metrics per cluster and save the plot."""
    interaction_types_data = {}
    for cluster, metrics in hierarchical_metrics.items():
        interaction_types_data[cluster] = {
            interaction_type: metrics['interaction-types'][interaction_type]['mean']
            for interaction_type in metrics['interaction-types']
        }

    clusters = list(interaction_types_data.keys())
    interaction_types = list(interaction_types_data[clusters[0]].keys())
    data = np.array([[interaction_types_data[cluster][interaction_type] for interaction_type in interaction_types] for cluster in clusters])

    data_percentage = (data.T / data.sum(axis=1)).T * 100

    _, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 6))

    ax1 = axes[1]
    bottom_values = np.zeros(len(clusters))
    for i, interaction_type in enumerate(interaction_types):
        ax1.bar(clusters, data_percentage[:, i], bottom=bottom_values, label=interaction_type)
        bottom_values += data_percentage[:, i]

    ax1.set_ylabel('Rate')
    ax1.set_title('Stacked Bar Plot of Interaction Types by Cluster')
    ax1.legend(title='Interaction Types')

    ax2 = axes[0]
    bottom_values = np.zeros(len(clusters))
    for i, interaction_type in enumerate(interaction_types):
        ax2.bar(clusters, data[:, i], bottom=bottom_values, label=interaction_type)
        bottom_values += data[:, i]

    ax2.set_ylabel('Mean Interaction')
    ax2.set_title('Stacked Bar Plot of Interaction Types by Cluster')
    ax2.legend(title='Interaction Types')

    plt.tight_layout()
    try:
        plt.savefig(f"{base_path}/interaction_types_plot.png")
        print("--> interaction types plot saved.")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Directory {base_path} does not exist.") from exc
