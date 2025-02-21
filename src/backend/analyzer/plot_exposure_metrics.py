import matplotlib.pyplot as plt


def plot_exposure_metrics(hierarchical_metrics, base_path, range_color_map):
    """
    Plots exposure metrics from hierarchical metrics and saves the plot to base_path.
    plot_type can be 'scatter' or 'box'.
    """
    types = ['min', 'max', 'median', 'mean']
    exposure_data = {cluster: {metric: {t: metrics['market-exposure'][metric][t] for t in types}
                               for metric in metrics['market-exposure']}
                     for cluster, metrics in hierarchical_metrics.items()}

    _, axes = plt.subplots(5, 2, figsize=(15, 30))
    axes = axes.flatten()

    metrics_to_plot = [
        'total_volume_exposure', 'total_volatility_exposure',
        'total_gas_exposure', 'total_error_exposure',
        'total_liquidity_exposure', 'total_activity_exposure',
        'total_user_adoption_exposure', 'total_gas_volatility_exposure',
        'total_error_volatility_exposure', 'total_high_value_exposure'
    ]

    for ax, metric in zip(axes, metrics_to_plot):
        for stat_type, color in range_color_map.items():
            values = [exposure_data[cluster][metric][stat_type] for cluster in exposure_data]
            x_values = range(len(values))
            if stat_type == 'min' or stat_type == 'max':
                linestyle = '-'
            else:
                linestyle = '--'
            ax.plot(x_values, values, marker='o', linestyle=linestyle, color=color, label=stat_type)
            for i, value in enumerate(values):
                if value == 0:
                    ax.plot(i, 0, marker='o', color='silver')

        ax.set_xlabel('Cluster')
        ax.set_ylabel('Value (symlog scale)')
        ax.set_yscale('symlog', linthresh=0.1)
        ax.set_xticks(range(len(exposure_data)))
        ax.set_title(metric.replace("_", " ").title() + " per cluster")
        ax.grid(True, axis='x')
        ax.legend(title='Metrics')

    plt.tight_layout()
    try:
        plot_path = f"{base_path}/exposure_metrics_plot.png"
        plt.savefig(plot_path)
        print("--> exposure metrics plot saved.")
        plt.close()
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Directory {base_path} does not exist.") from exc