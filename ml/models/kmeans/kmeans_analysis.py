import os
import json
import optuna
import numpy as np
from tqdm import tqdm
from joblib import Parallel, delayed
from matplotlib import pyplot as plt
from sklearn.metrics import silhouette_samples
from sklearn.cluster import MiniBatchKMeans, KMeans


def compute_inertia(k, x_train):
    """
    Computes the inertia (sum of squared distances to the nearest centroid) for a given number of clusters.
    :param:
        k (int): Number of clusters.
        x_train (ndarray): Training data.
    :return:
        float: Inertia value.
    """
    kmeans = MiniBatchKMeans(n_clusters=k, random_state=42, batch_size=100)
    kmeans.fit(x_train)
    return kmeans.inertia_


def compute_silhouette_score(k, x_train):
    """
    Computes the silhouette score for a given number of clusters with subsampling.
    :param:
        k (int): Number of clusters.
        x_train (ndarray): Training data.
    :return:
        float: Silhouette score (0 if insufficient clusters are found).
    """
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(x_train)

    sample_size = min(10000, x_train.shape[0])
    sample_indices = np.random.choice(x_train.shape[0], sample_size, replace=False)

    x_sample = x_train[sample_indices]
    labels_sample = kmeans.labels_[sample_indices]

    if len(np.unique(labels_sample)) < 2:
        print(f"Warning: only {len(np.unique(labels_sample))} clusters found for k={k}")
        return 0

    return np.mean(silhouette_samples(x_sample, labels_sample))


def analyze_kmeans(x_train, dataset_name):
    """
    Analyzes K-Means clustering for different values of k and visualizes the results.
    :param:
        x_train (ndarray): Training data.
        dataset_name (str): Identifier for the dataset (used in output file naming).
    :return:
        int: Optimal number of clusters based on silhouette score.
    """
    k_range = range(2, 11)

    print("Dataset statistics:")
    print("- Shape:", x_train.shape)
    print(
        "- Unique values:", np.unique(x_train, axis=0).shape[0], "/", x_train.shape[0]
    )
    print("- Feature variance:", np.var(x_train, axis=0))
    print("- NaN values present:", np.any(np.isnan(x_train)))
    print("- Inf values present:", np.any(np.isinf(x_train)))

    inertia = Parallel(n_jobs=-1)(
        delayed(compute_inertia)(k, x_train)
        for k in tqdm(k_range, desc="Calculating inertia")
    )

    try:
        silhouette_scores = Parallel(n_jobs=-1)(
            delayed(compute_silhouette_score)(k, x_train)
            for k in tqdm(k_range, desc="Calculating silhouette scores")
        )
    except (ValueError, IndexError, RuntimeError) as e:
        print(f"Error during silhouette score calculation: {e}")
        silhouette_scores = [0] * len(k_range)

    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    ax[0].plot(k_range, inertia, marker="o")
    ax[0].set_title("Elbow Method")
    ax[0].set_xlabel("Number of clusters")
    ax[0].set_ylabel("Inertia")

    ax[1].plot(k_range, silhouette_scores, marker="o")
    ax[1].set_title("Silhouette Scores")
    ax[1].set_xlabel("Number of clusters")
    ax[1].set_ylabel("Silhouette Score")

    fig.savefig(
        f"docs/graphics/kmeans/kmeans_{dataset_name}_scores.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.show()

    return k_range[np.argmax(silhouette_scores)]


def objective(x, trial):
    """
    Objective function for Optuna hyperparameter optimization of MiniBatchKMeans.
    :param:
        x (ndarray): Training data.
        trial (optuna.Trial): Optuna trial instance.
    :return:
        float: Silhouette score of the clustering result.
    """
    n_clusters = trial.suggest_int("n_clusters", 2, 10)
    init = trial.suggest_categorical("init", ["k-means++", "random"])
    batch_size = trial.suggest_int("batch_size", 50, 500, step=50)
    max_iter = trial.suggest_int("max_iter", 100, 500)
    tol = trial.suggest_float("tol", 1e-6, 1e-2, log=True)

    kmeans = MiniBatchKMeans(
        n_clusters=n_clusters,
        init=init,
        batch_size=batch_size,
        max_iter=max_iter,
        tol=tol,
        random_state=42,
    )
    labels = kmeans.fit_predict(x)

    sample_size = min(10000, x.shape[0])
    sample_indices = np.random.choice(x.shape[0], sample_size, replace=False)
    x_sample = x[sample_indices]
    labels_sample = labels[sample_indices]

    if len(np.unique(labels_sample)) < 2:
        return 0

    return np.mean(silhouette_samples(x_sample, labels_sample))


def optimize_hyperparams(
    x, n_trials=50, save_path="models/kmeans/optuna_kmeans_results.json"
):
    """
    Optimizes MiniBatchKMeans hyperparameters using Optuna and saves the results.
    :param:
        x (ndarray): Training data.
        n_trials (int, optional): Number of optimization trials. Defaults to 50.
        save_path (str, optional): Path to save optimization results. Defaults to "models/kmeans/optuna_kmeans_results.json".
    :return:
        dict: Best parameters and corresponding silhouette score.
    """
    best_params, best_value = {}, float("-inf")

    if os.path.exists(save_path):
        try:
            with open(save_path, "r") as f:
                saved_results = json.load(f)
                best_params = saved_results.get("best_params", {})
                best_value = saved_results.get("best_value", float("-inf"))
                print("Loaded previous optimization results...")
        except Exception as e:
            print(f"Error loading results: {e}")

    study = optuna.create_study(
        direction="maximize", study_name="minibatch_kmeans_optimization"
    )

    if best_params:
        study.enqueue_trial(best_params)

    try:
        study.optimize(lambda trial: objective(x, trial), n_trials=n_trials)
        best_params = study.best_params
        best_value = study.best_value
    except Exception as e:
        print(f"Optimization error: {e}")

    results = {"best_params": best_params, "best_value": best_value}

    try:
        with open(save_path, "w") as f:
            json.dump(results, f, indent=4)
        print(f"Results saved to {save_path}")
    except Exception as e:
        print(f"Error saving results: {e}")

    return results
