import json
import hdbscan
import optuna
import numpy as np
from optuna.pruners import MedianPruner
from sklearn.metrics import silhouette_samples


def objective(trial, x_train):
    """
    Objective function for hyperparameter optimization using Optuna.

    This function evaluates the performance of a clustering model (HDBSCAN) with different hyperparameter settings.
    It uses silhouette score to assess the clustering quality. The goal is to maximize the silhouette score.

    Hyperparameters:
    - min_cluster_size (int): Minimum size of the clusters. The higher the value, the larger the clusters. (Range: 5-50)
    - min_samples (int): Minimum number of samples in a neighborhood for a point to be considered a core point. (Range: 1-10)
    - cluster_selection_epsilon (float): Controls the sensitivity of the cluster selection process. (Range: 0.0-1.0)
    - cluster_selection_method (str): Method for selecting the final clusters. Options: 'eom' (excess of mass) or 'leaf'.
    - alpha (float): Controls the relative importance of the core distance and the density of the cluster. (Range: 1e-10 to 1.0, log scale)
    - approx_min_span_tree (bool): Whether or not to use an approximation of the minimum spanning tree.
    - gen_min_span_tree (bool): Whether or not to generate the minimum spanning tree.
    - metric (str): The distance metric to use for clustering. Options: 'euclidean', 'manhattan'.
    """
    min_cluster_size = trial.suggest_int('min_cluster_size', 5, 50, step=5)
    min_samples = trial.suggest_int('min_samples', 1, 10)
    cluster_selection_epsilon = trial.suggest_float('cluster_selection_epsilon', 0.0, 1.0, step=0.05)
    cluster_selection_method = trial.suggest_categorical('cluster_selection_method', ['eom', 'leaf'])
    alpha = trial.suggest_float('alpha', 1e-10, 1.0, log=True)
    approx_min_span_tree = trial.suggest_categorical('approx_min_span_tree', [True, False])
    gen_min_span_tree = trial.suggest_categorical('gen_min_span_tree', [True, False])
    metric = trial.suggest_categorical('metric', ['euclidean', 'manhattan'])

    model = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        cluster_selection_epsilon=cluster_selection_epsilon,
        cluster_selection_method=cluster_selection_method,
        alpha=alpha,
        approx_min_span_tree=approx_min_span_tree,
        gen_min_span_tree=gen_min_span_tree,
        metric=metric,
        core_dist_n_jobs = -1
    )
    model.fit(x_train)

    sample_size = min(10000, x_train.shape[0])
    sample_indices = np.random.choice(x_train.shape[0], sample_size, replace=False)

    x_sample = x_train[sample_indices]
    labels_sample = model.labels_[sample_indices]

    if len(np.unique(labels_sample)) < 2:
        print(f"Warning: only {len(np.unique(labels_sample))} clusters found.")
        return 0

    return np.mean(silhouette_samples(x_sample, labels_sample))


def trials_to_dict(trials):
    """ Convert Optuna trials to a dictionary format. """
    return [
        {
            'params': trial.params,
            'value': trial.value,
            'state': trial.state,
            'datetime': str(trial.datetime_start)
        }
        for trial in trials
    ]

def optimize_hyperparams(x_all, n_trials, save_path="models/hdbscan/optuna_study_results.json"):
    """
    Optimize hyperparameters for HDBSCAN using Optuna.

    This function creates an Optuna study to optimize the hyperparameters of the HDBSCAN clustering model.
    The objective function used for optimization returns the silhouette score, and the goal is to maximize this score.
    """
    pruner = MedianPruner(n_startup_trials=5, n_warmup_steps=10, interval_steps=1)
    study = optuna.create_study(
        direction='maximize',
        study_name='hdbscan_optimization',
        pruner=pruner
    )
    study.optimize(lambda trial: objective(trial, x_all), n_trials=n_trials, n_jobs=-1)
    best_params = study.best_params

    if save_path:
        with open(save_path, 'w') as f:
            json.dump({'best_params': best_params, 'trials': trials_to_dict(study.trials)}, f, indent=4, sort_keys=True)
    return best_params