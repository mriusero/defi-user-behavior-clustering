import json

from .plot_clustering_rate import plot_cluster_metrics
from .plot_tx_activity import plot_tx_activity
from .plot_interaction_types import plot_interaction_types
from .plot_engagement import plot_engagement
from .plot_diversity_and_influence import plot_diversity_and_influence
from .plot_timing_behavior import plot_timing_behavior
from .plot_tx_statistics import plot_tx_statistics
from .plot_exposure_metrics import plot_exposure_metrics
from .plot_heatmap import plot_heatmap

def analyze_clusters():
    """ Main function to plot all the clusters metrics and analysis"""
    print("\n===== Plotting clusters metrics =====\n")

    with open('src/frontend/layouts/data/kmeans_clusters_metrics.json', 'r', encoding='utf-8') as file:
        metrics = json.load(file)
    base_path = "src/frontend/layouts/pictures/kmeans_analysis"

    qualitative_cmap = 'Pastel1'
    range_color_map = {
        'min': 'red',
        'max': 'green',
        'median': 'navy',
        'mean': 'lightseagreen'
    }

    plot_cluster_metrics(metrics, base_path, qualitative_cmap)

    plot_interaction_types(metrics, base_path, qualitative_cmap)
    plot_engagement(metrics, base_path, qualitative_cmap)

    plot_tx_activity(metrics, base_path, range_color_map)
    plot_diversity_and_influence(metrics, base_path, range_color_map)

    plot_tx_statistics(metrics, base_path, range_color_map, tx_type='sent')
    plot_tx_statistics(metrics, base_path, range_color_map, tx_type='received')

    plot_timing_behavior(metrics, base_path, range_color_map)
    plot_exposure_metrics(metrics, base_path, range_color_map)

    plot_heatmap(base_path)

if __name__ == "__main__":
    analyze_clusters()
