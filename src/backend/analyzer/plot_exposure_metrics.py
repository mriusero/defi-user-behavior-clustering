import matplotlib.pyplot as plt
import numpy as np


def plot_exposure_metrics(hierarchical_metrics, base_path):
    """
    Plots exposure metrics from hierarchical metrics and saves the plot to base_path.
    """
    types = ['min', 'max', 'median', 'mean']
    exposure_data = {}

    for cluster, metrics in hierarchical_metrics.items():
        exposure_data[cluster] = {
            'total_volume_exposure': {t: metrics['market-exposure']['total_volume_exposure'][t] for t in types},
            'total_volatility_exposure': {t: metrics['market-exposure']['total_volatility_exposure'][t] for t in types},
            'total_gas_exposure': {t: metrics['market-exposure']['total_gas_exposure'][t] for t in types},
            'total_error_exposure': {t: metrics['market-exposure']['total_error_exposure'][t] for t in types},
            'total_liquidity_exposure': {t: metrics['market-exposure']['total_liquidity_exposure'][t] for t in types},
            'total_activity_exposure': {t: metrics['market-exposure']['total_activity_exposure'][t] for t in types},
            'total_user_adoption_exposure': {t: metrics['market-exposure']['total_user_adoption_exposure'][t] for t in types},
            'total_gas_volatility_exposure': {t: metrics['market-exposure']['total_gas_volatility_exposure'][t] for t in types},
            'total_error_volatility_exposure': {t: metrics['market-exposure']['total_error_volatility_exposure'][t] for t in types},
            'total_high_value_exposure': {t: metrics['market-exposure']['total_high_value_exposure'][t] for t in types}
        }

    fig, axes = plt.subplots(5, 2, figsize=(20, 15))
    axes = axes.flatten()

    metrics_to_plot = [
        'total_volume_exposure', 'total_volatility_exposure',
        'total_gas_exposure', 'total_error_exposure',
        'total_liquidity_exposure', 'total_activity_exposure',
        'total_user_adoption_exposure', 'total_gas_volatility_exposure',
        'total_error_volatility_exposure', 'total_high_value_exposure'
    ]

    colors = {'min': 'red', 'max': 'green', 'median': 'purple', 'mean': 'blue'}

    for ax, metric in zip(axes, metrics_to_plot):
        for stat_type, color in colors.items():
            values = [exposure_data[cluster][metric][stat_type] for cluster in exposure_data]
            x_values = range(len(values))

            ax.plot(x_values, values, marker='o', linestyle='--', color=color, label=stat_type)

            for i, value in enumerate(values):
                if value == 0:
                    ax.plot(i, 0, marker='o', color='black')

        ax.set_xlabel('Cluster')
        ax.set_ylabel('Value (symlog scale)')
        ax.set_yscale('symlog', linthresh=0.1)
        ax.set_xticks(x_values)
        ax.set_title(f'{metric.replace("_", " ").title()} per cluster')
        ax.legend(title='Statistique')

    plt.tight_layout()
    try:
        plot_path = f"{base_path}/exposure_metrics_scatter_plot.png"
        plt.savefig(plot_path)
        print(f"--> exposure metrics scatter plot saved.")
        plt.close()
    except FileNotFoundError:
        raise FileNotFoundError(f"Directory {base_path} does not exist.")




def plot_exposure_metrics_box_plot(hierarchical_metrics, base_path):
    """Plot exposure metrics per cluster and save the figure."""
    types = ['min', 'max', 'median', 'mean']
    exposure_data = {}

    for cluster, metrics in hierarchical_metrics.items():
        exposure_data[cluster] = {
            'total_volume_exposure': {t: metrics['market-exposure']['total_volume_exposure'][t] for t in types},
            'total_volatility_exposure': {t: metrics['market-exposure']['total_volatility_exposure'][t] for t in types},
            'total_gas_exposure': {t: metrics['market-exposure']['total_gas_exposure'][t] for t in types},
            'total_error_exposure': {t: metrics['market-exposure']['total_error_exposure'][t] for t in types},
            'total_liquidity_exposure': {t: metrics['market-exposure']['total_liquidity_exposure'][t] for t in types},
            'total_activity_exposure': {t: metrics['market-exposure']['total_activity_exposure'][t] for t in types},
            'total_user_adoption_exposure': {t: metrics['market-exposure']['total_user_adoption_exposure'][t] for t in types},
            'total_gas_volatility_exposure': {t: metrics['market-exposure']['total_gas_volatility_exposure'][t] for t in types},
            'total_error_volatility_exposure': {t: metrics['market-exposure']['total_error_volatility_exposure'][t] for t in types},
            'total_high_value_exposure': {t: metrics['market-exposure']['total_high_value_exposure'][t] for t in types}
        }

    fig, axes = plt.subplots(5, 2, figsize=(20, 15))
    axes = axes.flatten()

    metrics_to_plot = [
        'total_volume_exposure', 'total_volatility_exposure',
        'total_gas_exposure', 'total_error_exposure',
        'total_liquidity_exposure', 'total_activity_exposure',
        'total_user_adoption_exposure', 'total_gas_volatility_exposure',
        'total_error_volatility_exposure', 'total_high_value_exposure'
    ]
    colors = plt.cm.tab20(np.linspace(0, 1, len(exposure_data)))

    for ax, metric in zip(axes, metrics_to_plot):
        data = []
        for cluster in exposure_data:
            values = [exposure_data[cluster][metric][t] for t in types]
            data.append(values)

        bplot = ax.boxplot(data, patch_artist=True)

        for patch, color in zip(bplot['boxes'], colors):
            patch.set_facecolor(color)

        ax.set_xlabel('Cluster')
        ax.set_ylabel('Value (symlog scale)')
        ax.set_yscale('symlog', linthresh=0.1)
        ax.set_xticks(range(1, len(exposure_data) + 1))
        ax.set_title(f'{metric.replace("_", " ").title()} per cluster')

    plt.tight_layout()
    try:
        plot_path = f"{base_path}/exposure_metrics_box_plot.png"
        plt.savefig(plot_path)
        print(f"--> exposure metrics box plot saved.")
        plt.close()
    except FileNotFoundError:
        raise FileNotFoundError(f"Directory {base_path} does not exist.")