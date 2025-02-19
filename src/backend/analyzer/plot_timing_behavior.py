import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_timing_behavior(hierarchical_metrics, base_path):
    """
    Generate and save box plots for timing behavior metrics by cluster.
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

    timing_df = pd.concat({k: pd.DataFrame(v) for k, v in timing_behavior_data.items()}).reset_index(level=1, drop=True).reset_index()
    timing_df = timing_df.melt(id_vars='index', var_name='Metric', value_name='Value')

    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(18, 15))

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
        sns.boxplot(x='index', y='Value', hue='index', data=timing_df[timing_df['Metric'] == metric], ax=ax, palette='Set2')
        ax.set_title(f'Box-plot of {metric} by Cluster')
        ax.set_xlabel('Cluster')
        ax.set_ylabel('Value')
        plt.setp(ax.get_xticklabels(), rotation=45)
        ax.grid(True)

    for ax, metric in zip(axes[:, 1], sent_metrics):
        sns.boxplot(x='index', y='Value', hue='index', data=timing_df[timing_df['Metric'] == metric], ax=ax, palette='Set2')
        ax.set_title(f'Box-plot of {metric} by Cluster')
        ax.set_xlabel('Cluster')
        ax.set_ylabel('Value')
        plt.setp(ax.get_xticklabels(), rotation=45)
        ax.grid(True)

    plt.tight_layout()
    try :
        plt.savefig(f"{base_path}/timing_behavior_boxplots.png")
        print(f"--> timing behavior box plots saved.")
        plt.close()
    except FileNotFoundError:
        raise FileNotFoundError(f"--> Error: {base_path} does not exist.")