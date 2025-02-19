import json

try:
    from plot_clustering_rate import plot_cluster_metrics
    from plot_tx_activity import plot_tx_activity
    from plot_interaction_types import plot_interaction_types
    from plot_engagement import plot_engagement
    from plot_diversity_and_influence import plot_diversity_and_influence
    from plot_timing_behavior import plot_timing_behavior
    from plot_tx_statistics import plot_tx_statistics
    from plot_exposure_metrics import plot_exposure_metrics
except ImportError as e:
    print(f"Erreur d'importation : {e}")

def main(metrics_data, base_directory):
    print("\n===== Plotting cluster metrics =====\n")

    plot_cluster_metrics(metrics_data, base_directory)
    plot_tx_activity(metrics_data, base_directory)
    plot_interaction_types(metrics_data, base_directory)
    plot_engagement(metrics_data, base_directory)
    plot_diversity_and_influence(metrics_data, base_directory)
    plot_timing_behavior(metrics_data, base_directory)
    plot_tx_statistics(metrics_data, base_directory, tx_type='sent')
    plot_tx_statistics(metrics_data, base_directory, tx_type='received')
    plot_exposure_metrics(metrics_data, base_directory, plot_type='scatter')
    plot_exposure_metrics(metrics_data, base_directory, plot_type='box')

if __name__ == "__main__":
    with open('src/frontend/layouts/data/kmeans_clusters_metrics.json', 'r', encoding='utf-8') as file:
        metrics = json.load(file)

    base_path = "src/frontend/layouts/pictures/kmeans_analysis"

    main(metrics, base_path)
