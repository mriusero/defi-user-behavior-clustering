import matplotlib.pyplot as plt


def plot_cluster_metrics(hierarchical_metrics, base_path):
    """
    Plots and saves the repartition rates and address counts for clusters.
    """
    clusters = list(hierarchical_metrics.keys())
    repartition_rates = [hierarchical_metrics[cluster]['repartition_rate'] for cluster in clusters]
    address_count = [hierarchical_metrics[cluster]['address'] for cluster in clusters]

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    bars = axes[0].bar(clusters, repartition_rates, color=plt.cm.Paired.colors)
    axes[0].set_xlabel('Cluster')
    axes[0].set_ylabel('Repartition Rate')
    axes[0].set_title('Repartition Diagram by Cluster')
    axes[0].tick_params(axis='x', rotation=45)

    for bar, count, rate in zip(bars, address_count, repartition_rates):
        formatted_count = f'{count:,}'.replace(',', ' ')
        height = bar.get_height()
        axes[0].annotate(f'{formatted_count} users\n({rate*100:.2f}%)',
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 0),
                         textcoords="offset points",
                         ha='center', va='center')

    axes[1].pie(repartition_rates, labels=clusters, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    axes[1].set_title('Sector Repartition by Cluster')

    plt.tight_layout()
    try:
        plt.savefig(f"{base_path}/cluster_repartition.png")
        print(f"--> cluster repartition plot saved.")
    except FileNotFoundError:
        raise f"Directory {base_path} does not exist."