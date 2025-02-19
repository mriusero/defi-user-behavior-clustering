import json

from plot_clustering_rate import plot_cluster_metrics
from plot_tx_activity import plot_tx_activity
from plot_interaction_types import plot_interaction_types
from plot_engagement import plot_engagement
from plot_diversity_and_influence import plot_diversity_and_influence
from plot_timing_behavior import plot_timing_behavior
from plot_tx_statistics import plot_sent_tx_statistics, plot_received_tx_statistics
from plot_exposure_metrics import plot_exposure_metrics, plot_exposure_metrics_box_plot


def main(metrics, base_path):

    print("\n===== Plotting cluster metrics =====\n")
    plot_cluster_metrics(metrics, base_path)
    plot_tx_activity(metrics, base_path)
    plot_interaction_types(metrics, base_path)
    plot_engagement(metrics, base_path)
    plot_diversity_and_influence(metrics, base_path)
    plot_timing_behavior(metrics, base_path)
    plot_sent_tx_statistics(metrics, base_path)
    plot_received_tx_statistics(metrics, base_path)
    plot_exposure_metrics(metrics, base_path)
    plot_exposure_metrics_box_plot(metrics, base_path)

if __name__ == "__main__":

    with open('src/frontend/layouts/data/kmeans_clusters_metrics.json', 'r') as file:
        metrics = json.load(file)

    base_path = "src/frontend/layouts/pictures/kmeans_analysis"


    main(metrics, base_path)
