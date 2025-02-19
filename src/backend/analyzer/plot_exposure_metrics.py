import matplotlib.pyplot as plt
import numpy as np

def plot_exposure_metrics(hierarchical_metrics, base_path, plot_type='scatter'):
    """
    Plots exposure metrics from hierarchical metrics and saves the plot to base_path.
    plot_type can be 'scatter' or 'box'.
    """
    types = ['min', 'max', 'median', 'mean']
    exposure_data = {cluster: {metric: {t: metrics['market-exposure'][metric][t] for t in types}
                               for metric in metrics['market-exposure']}
                     for cluster, metrics in hierarchical_metrics.items()}

    _, axes = plt.subplots(5, 2, figsize=(20, 15))
    axes = axes.flatten()

    metrics_to_plot = [
        'total_volume_exposure', 'total_volatility_exposure',
        'total_gas_exposure', 'total_error_exposure',
        'total_liquidity_exposure', 'total_activity_exposure',
        'total_user_adoption_exposure', 'total_gas_volatility_exposure',
        'total_error_volatility_exposure', 'total_high_value_exposure'
    ]

    colors = {'min': 'red', 'max': 'green', 'median': 'purple', 'mean': 'blue'}
    box_colors = plt.get_cmap('tab20')(np.linspace(0, 1, len(exposure_data)))

    for ax, metric in zip(axes, metrics_to_plot):
        if plot_type == 'scatter':
            for stat_type, color in colors.items():
                values = [exposure_data[cluster][metric][stat_type] for cluster in exposure_data]
                x_values = range(len(values))
                ax.plot(x_values, values, marker='o', linestyle='--', color=color, label=stat_type)
                for i, value in enumerate(values):
                    if value == 0:
                        ax.plot(i, 0, marker='o', color='black')
        elif plot_type == 'box':
            data = [[exposure_data[cluster][metric][t] for t in types] for cluster in exposure_data]
            bplot = ax.boxplot(data, patch_artist=True)
            for patch, color in zip(bplot['boxes'], box_colors):
                patch.set_facecolor(color)

        ax.set_xlabel('Cluster')
        ax.set_ylabel('Value (symlog scale)')
        ax.set_yscale('symlog', linthresh=0.1)
        ax.set_xticks(range(len(exposure_data)))
        ax.set_title(metric.replace("_", " ").title() + " per cluster")
        if plot_type == 'scatter':
            ax.legend(title='Statistique')

    plt.tight_layout()
    try:
        plot_path = f"{base_path}/exposure_metrics_{plot_type}_plot.png"
        plt.savefig(plot_path)
        print(f"--> exposure metrics {plot_type} plot saved.")
        plt.close()
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Directory {base_path} does not exist.") from exc