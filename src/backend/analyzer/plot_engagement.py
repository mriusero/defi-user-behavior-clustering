import numpy as np
import matplotlib.pyplot as plt

def plot_engagement(hierarchical_metrics, base_path):
    """Plot and save stacked bar plots of protocols engagement by cluster."""
    protocols_data = {cluster: {protocol: metrics['protocols-engagement'][protocol]['mean']
                                for protocol in metrics['protocols-engagement']}
                      for cluster, metrics in hierarchical_metrics.items()}

    clusters = list(protocols_data.keys())
    protocols = list(protocols_data[clusters[0]].keys())

    data = np.array([[protocols_data[cluster][protocol] for protocol in protocols] for cluster in clusters])
    data_percentage = (data.T / data.sum(axis=1)).T * 100

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 6))

    for ax, data_set, ylabel, title in zip(axes, [data_percentage, data], ['Rate', 'Mean Engagement'],
                                           ['Percentage Stacked Bar Plot', 'Mean Engagement Stacked Bar Plot']):
        bottom_values = np.zeros(len(clusters))
        for i, protocol in enumerate(protocols):
            ax.bar(clusters, data_set[:, i], bottom=bottom_values, label=protocol)
            bottom_values += data_set[:, i]

        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.legend(title='Protocols')

    plt.tight_layout()
    try :
        plt.savefig(f'{base_path}/protocols_engagement_plot.png')
        print(f"--> protocols engagement plot saved.")
        plt.close()
    except FileNotFoundError:
        raise FileNotFoundError(f"--> Error: {base_path} does not exist.")