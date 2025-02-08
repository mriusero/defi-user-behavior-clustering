import json
import os
import sys
import joblib
import pandas as pd
import pyarrow as pa
import pyarrow.feather as feather
import hdbscan
import warnings
from sklearn.decomposition import PCA


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ml.hdbscan.hdbscan_analysis import optimize_hyperparams
from ml.utils.splitting import splitting
from ml.utils.hf_hub import upload_model

warnings.filterwarnings("ignore", message=".*'force_all_finite' was renamed to 'ensure_all_finite'.*")

class HDBSCANPipeline:
    """
    HDBSCAN pipeline for clustering Ethereum addresses using batch processing on CPU.
    :param analyse: Whether to analyze the dataset to determine optimal hyperparameters.
    :param reduce_dimensions: Whether to reduce the dimensions of the dataset with PCA.
    :param optimization: Whether to optimize hyperparameters using Optuna.
    :param upload: Whether to upload the trained model to Hugging Face Hub.
    """

    def __init__(self, analyse=False, reduce_dimensions=True, optimization=False, upload=False):
        """Initialize the HDBSCAN pipeline"""
        self.analyse = analyse
        self.reduce_dimensions = reduce_dimensions
        self.optimization = optimization
        self.upload = upload
        self.dataset = None
        self.x_all = None
        self.y_all = None
        self.best_params = {}
        self.model = None
        self.model_path = "models/hdbscan/DeFI-HDBSCAN.pkl"
        self.optuna_results_path = "models/hdbscan/optuna_study_results.json"
        self.predictions_path = "data/results/hdbscan_predictions.arrow"

    def run(self):
        """Run the HDBSCAN pipeline"""
        print("\n ======= Running ML pipeline ======= \n")
        self.load_data()
        self.reduce()
        self.load_hyperparameters()
        self.optimize_hyperparameters() if self.optimization else None
        self.train_model()
        self.save()
        self.load()
        self.predict()
        self.upload_model() if self.upload else None
        print("\n ======= HDBSCAN pipeline completed ======= \n")

    def load_data(self):
        """Load data and split into training and testing sets"""
        print("1. Splitting\n---------------------------------")
        self.dataset = splitting()
        self.x_all = self.dataset["all"][0]
        self.y_all = self.dataset["all"][1]

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
        default_params = {
            'min_cluster_size': 5,
            'min_samples': 1,
            'metric': 'euclidean',
            'cluster_selection_method': 'eom',
            'ensure_all_finite': True
        }
        if os.path.exists(self.optuna_results_path):
            print("\n4. Loading precomputed optimal hyperparameters\n---------------------------------")
            try:
                with open(self.optuna_results_path, "r") as f:
                    saved_results = json.load(f)
                    self.best_params = saved_results.get("best_params", {})
                    print(f"Best hyperparameters loaded: {self.best_params}")
            except Exception as e:
                print(f"Error loading hyperparameters: {e}, proceeding with default.")
                self.best_params = default_params
        else:
            print("\n4. No precomputed hyperparameters found")
            self.best_params = default_params

    def optimize_hyperparameters(self):
        """Optimize hyperparameters using Optuna"""
        print("\n5. Optimizing hyperparameters\n---------------------------------")
        self.best_params = optimize_hyperparams(self.x_all, n_trials=100, save_path=self.optuna_results_path)
        print(f"Optimal parameters found: {self.best_params}")

    def train_model(self):
        """Train the HDBSCAN model with batch processing in parallel"""
        print("\n6. Train\n---------------------------------")
        self.model = hdbscan.HDBSCAN(**self.best_params, core_dist_n_jobs=-1)
        self.model.fit(self.x_all)
        print("Model trained successfully")

    def save(self):
        """Save the trained HDBSCAN model"""
        print("\n7. Save model\n---------------------------------")
        print(f"Saving model to {self.model_path}")
        return joblib.dump(self.model, self.model_path)

    def load(self):
        """Load the trained HDBSCAN model"""
        print("\n8. Load Model\n---------------------------------")
        print(f"Loading model from {self.model_path}")
        return joblib.load(self.model_path)

    def predict(self):
        """Predict the clusters for all addresses and save the results"""
        print("\n9. Predict\n---------------------------------")
        if hasattr(self.model, 'labels_'):
            clusters = self.model.labels_
            results = pd.DataFrame({"address": self.y_all, "cluster": clusters})
            print(f"Predictions: {results.shape[0]} rows clustered")
        else:
            print("Model has not been fitted yet. Please fit the model first.")
            return
        print("\n10. Save predictions\n---------------------------------")
        table = pa.Table.from_pandas(results)
        feather.write_feather(table, self.predictions_path)
        print(f"Predictions saved successfully to {self.predictions_path}\n")

    def upload_model(self):
        """Upload the trained model to Hugging Face Hub"""
        print("\n11. Upload model to HF\n---------------------------------")
        upload_model(self.model_path, "DeFI-HDBSCAN.pkl")


if __name__ == "__main__":
    pipeline = HDBSCANPipeline(
        analyse=False,
        reduce_dimensions=True,
        optimization=False,
        upload=True,
    )
    pipeline.run()