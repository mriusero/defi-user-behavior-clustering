import pandas as pd
import numpy as np
import joblib
from matplotlib import pyplot as plt
from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics import silhouette_samples
from tqdm import tqdm
from joblib import Parallel, delayed


def compute_inertia(k, x_train):
    """Computes the inertia for a given number of clusters."""
    kmeans = MiniBatchKMeans(n_clusters=k, random_state=42, batch_size=100)
    kmeans.fit(x_train)
    return kmeans.inertia_


def compute_silhouette_score(k, x_train):
    """Computes the silhouette score with subsampling."""
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(x_train)

    sample_size = min(10000, x_train.shape[0])                                       # Maximum 10000 examples
    sample_indices = np.random.choice(x_train.shape[0], sample_size, replace=False)  # Random indices

    x_sample = np.array(x_train)[sample_indices]
    labels_sample = kmeans.labels_[sample_indices]

    if len(np.unique(labels_sample)) < 2:
        print(f"Warning: only {len(np.unique(labels_sample))} clusters found for k={k}")
        return 0

    return np.mean(silhouette_samples(x_sample, labels_sample))


def analyze_kmeans(x_train, set):
    """Trains the K-Means model, assigns clusters, and displays the results."""
    k_range = range(2, 11)

    print("Shape:", x_train.shape)
    print("Nb unique values:", np.unique(x_train, axis=0).shape[0], "/", x_train.shape[0])
    print("Features variance:\n", np.var(x_train, axis=0))
    print("NaN values:", np.any(np.isnan(x_train)))
    print("Inf values:", np.any(np.isinf(x_train)))

    inertia = Parallel(n_jobs=-1)(
        delayed(compute_inertia)(k, x_train) for k in tqdm(k_range, desc="Calculating inertia")
    )
    silhouette_scores = []
    try:
        silhouette_scores = Parallel(n_jobs=-1)(
            delayed(compute_silhouette_score)(k, x_train) for k in tqdm(k_range, desc="Calculating silhouette scores")
        )
    except (ValueError, IndexError, RuntimeError) as e:
        print(f"Error during silhouette score calculation: {e}")
        silhouette_scores = [0] * len(k_range)

    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    ax[0].plot(k_range, inertia, marker='o')
    ax[0].set_title("Elbow Method")
    ax[0].set_xlabel("Number of clusters")
    ax[0].set_ylabel("Inertia")

    ax[1].plot(k_range, silhouette_scores, marker='o')
    ax[1].set_title("Silhouette Scores")
    ax[1].set_xlabel("Number of clusters")
    ax[1].set_ylabel("Silhouette Score")

    fig.savefig(f"docs/graphics/kmeans/kmeans_{set}_scores.png", dpi=300, bbox_inches="tight")
    plt.show()

    return k_range[np.argmax(silhouette_scores)]

def train(best_k, x_train):
    """Trains a KMeans model with a defined number of clusters."""
    kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    kmeans.fit(x_train)
    return kmeans

def save_model(model, filename):
    """Saves the trained model to a file."""
    return joblib.dump(model, filename)

def load_model(filename):
    """Loads a saved KMeans model from a file."""
    return joblib.load(filename)

def predict(model, x_, y_):
    """Predicts clusters for new data using a trained model."""
    clusters = model.predict(x_)
    return pd.DataFrame({"address": y_, "cluster": clusters})