import json
import os
import sys
import joblib
import pandas as pd
import pyarrow as pa
import pyarrow.feather as feather
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from kmeans_analysis import analyze_kmeans, optimize_hyperparams, measure_performances
from ml.utils.splitting import splitting
from ml.utils.hf_hub import upload_model
from ml.interpreter.comparison import clusters_analysis
from ml.interpreter.scoring.kpi import compute_scoring
from src.backend.analyzer import plotter

class KMeansPipeline:
    """
     KMeans pipeline for clustering Ethereum addresses
    :param analyse: Whether to analyze the dataset to determine the optimal number of clusters.
    :param reduce_dimensions: Whether to reduce the dimensions of the dataset with PCA.
    :param optimization: Whether to optimize hyperparameters using Optuna.
    :param upload: Whether to upload the trained model to Hugging Face Hub.
    """

    def __init__(
        self, analyse=False, reduce_dimensions=True, optimization=False, upload=False, no_graph=False
    ):
        """Initialize the KMeans pipeline"""
        self.analyse = analyse
        self.reduce_dimensions = reduce_dimensions
        self.optimization = optimization
        self.upload = upload
        self.no_graph = no_graph
        self.dataset = None
        self.x_all = None
        self.y_all = None
        self.best_k = 4
        self.model = None
        self.clusters = None
        self.features_path = f"data/features/features.arrow"
        self.predictions_path = f"data/clustering/kmeans/kmeans_predictions.arrow"
        self.model_path = f"src/frontend/layouts/data/DeFI-Kmeans.pkl"
        self.optuna_results_path = "src/frontend/layouts/data/optuna_study_results.json"
        self.performance_path = f"src/frontend/layouts/data/kmeans_performance.json"

    def run(self):
        """Run the KMeans pipeline"""
        print("\n ======= Running ML pipeline ======= \n")
        self.load_data()
        self.analyze() if self.analyse else None
        self.reduce()
        self.load_hyperparameters()
        self.optimize_hyperparameters() if self.optimization else None
        self.train_model()
        self.save()
        self.load()
        self.predict()
        self.upload_model() if self.upload else None
        self.analyse_results()
        self.compute_graphics()
        self.score_users()
        print("\n ======= KMeans pipeline completed ======= \n")

    def load_data(self):
        """Load data and split into training and testing sets"""
        print("1. Splitting\n---------------------------------")
        self.dataset = splitting()
        self.x_all = self.dataset["all"][0]
        self.y_all = self.dataset["all"][1]

    def analyze(self):
        """Analyze the dataset to determine the optimal number of clusters"""
        print("\n2. Analyse\n---------------------------------")
        self.best_k = analyze_kmeans(self.x_all, set="train")
        print(f"Optimal number of clusters (train): {self.best_k}")

    def reduce(self):
        """Reduce the dimensions of the dataset with PCA"""
        if self.reduce_dimensions:
            print("\n3. Reduce dimensions\n---------------------------------")
            pca = PCA(n_components=28)
            self.x_all = pca.fit_transform(self.x_all)
            print(f"Dimensions reduced successfully: {self.x_all.shape}")
        else:
            print("\n3. No dimension reduction\n---------------------------------")

    def load_hyperparameters(self):
        """Load precomputed hyperparameters if available"""
        if os.path.exists(self.optuna_results_path):
            print(
                "\n4. Loading precomputed optimal hyperparameters\n---------------------------------"
            )
            try:
                with open(self.optuna_results_path, "r") as f:
                    saved_results = json.load(f)
                    best_params = saved_results.get("best_params", {})
                    self.best_k = best_params.get("n_clusters", 4)
                    print(
                        f"Best hyperparameters loaded: {best_params}\nMetric associated: {saved_results.get('best_value', 0)}"
                    )
            except Exception as e:
                print(f"Error loading hyperparameters: {e}, proceeding with default.")
        else:
            print("\n4. No precomputed hyperparameters found")

    def optimize_hyperparameters(self):
        """Optimize hyperparameters using Optuna"""
        print("\n5. Optimizing hyperparameters\n---------------------------------")
        results = optimize_hyperparams(
            self.x_all, n_trials=500, save_path=self.optuna_results_path
        )
        self.best_k = results["best_params"]["n_clusters"]
        print(f"Optimal number of clusters (all): {self.best_k}")

    def train_model(self):
        """Train the KMeans model"""
        print("\n6. Train\n---------------------------------")
        self.model = KMeans(n_clusters=self.best_k, random_state=42, n_init=10)
        self.model.fit(self.x_all)
        print("Model trained successfully")

    def save(self):
        """Save the Kmeans trained model"""
        print("\n7. Save model\n---------------------------------")
        print(f"Saving model to {self.model_path}")
        return joblib.dump(self.model, self.model_path)

    def load(self):
        """Load the trained KMeans model"""
        print("\n8. Load Model\n---------------------------------")
        print(f"Loading model from {self.model_path}")
        return joblib.load(self.model_path)

    def predict(self):
        """Predict the clusters for all addresses and save the results"""
        print("\n9. Predict\n---------------------------------")
        self.clusters = self.model.predict(self.x_all)
        results = pd.DataFrame({"address": self.y_all, "cluster": self.clusters})
        print(f"Predictions: {results.shape[0]} rows clustered")

        print("\n10. Save predictions\n---------------------------------")
        table = pa.Table.from_pandas(results)
        feather.write_feather(table, self.predictions_path)
        print(f"Predictions saved successfully to {self.predictions_path}")

    def upload_model(self):
        """Upload the trained model to Hugging Face Hub"""
        print("\n11. Upload model to HF\n---------------------------------")
        upload_model(self.model_path, "DeFI-Kmeans.pkl")

    def analyse_results(self):
        """Analyze the results of the KMeans clustering"""
        print("\n12. Analyzing results\n---------------------------------")

        print("\nPerformances:\n")
        db_index, ch_index, silhouette_avg = measure_performances(data=self.x_all, labels=self.clusters)
        print(f"--> Davies-Bouldin Index: {db_index}")
        print(f"--> Calinski-Harabasz Index: {ch_index}")
        print(f"--> Silhouette Avg: {silhouette_avg}")
        results = {
            "Davies-Bouldin Index": db_index,
            "Calinski-Harabasz Index": ch_index,
            "Silhouette Avg": silhouette_avg
        }
        with open(self.performance_path, 'w') as json_file:
            json.dump(results, json_file, indent=4)

        print("\nClusters analysis:\n")
        metrics = clusters_analysis(self.features_path, self.predictions_path)
        for cluster, data in metrics.items():
            print(f"Cluster {cluster}:")
            print(f"  Addresses count: {data['address']}")
            print(f"  Repartition rate: {data['repartition_rate']:.4f}")

    def compute_graphics(self):
        """Compute graphics for the KMeans clustering"""
        print("\n13. Computing graphics\n---------------------------------")
        if self.no_graph:
            print("Skipping graphics computation")
            return
        else:
            plotter.analyze_clusters()
            print("Graphics computed successfully")

    def score_users(self):
        """Compute the scoring of users"""
        print("\n14. Scoring\n---------------------------------")
        scores = compute_scoring()
        print(f"Scores computed successfully")


if __name__ == "__main__":
    pipeline = KMeansPipeline(
        analyse=False, reduce_dimensions=True, optimization=False, upload=False, no_graph=False,
    )
    pipeline.run()
