import os
import sys
import numpy as np
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.decomposition import PCA
import logging

logging.basicConfig(level=logging.INFO)
matplotlib.use('Agg')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ml.utils.splitting import splitting


def apply_pca(x_all, variance_threshold=0.9999966):
    """Applies PCA and visualizes the principal components with a variance threshold."""
    print("\nApplying PCA...\n")
    pca = PCA()
    x_pca = pca.fit_transform(x_all)

    explained_variance_cumsum = np.cumsum(pca.explained_variance_ratio_)

    n_components = np.argmax(explained_variance_cumsum >= variance_threshold) + 1
    print(f"Optimal number of components to reach {variance_threshold * 100}% explained variance: {n_components}")

    plt.figure(figsize=(8, 5))
    plt.plot(explained_variance_cumsum)
    plt.axvline(x=n_components - 1, color='r', linestyle='--', label=f'({variance_threshold * 100}%) {n_components} components')
    plt.xlabel('Number of components')
    plt.ylabel('Cumulative explained variance')
    plt.title('PCA - Cumulative Explained Variance')
    plt.legend()
    plt.grid(True)
    plt.savefig(f"docs/graphics/pca/pca_variance.png", dpi=300, bbox_inches="tight")
    logging.info(f"Graphic saved in docs/graphics/pca/pca_variance.png")
    plt.close()

    pca = PCA(n_components=n_components)
    x_pca = pca.fit_transform(x_all)

    if n_components >= 3:

        max_points = 100_000
        if x_pca.shape[0] > max_points:
            idx = np.random.choice(x_pca.shape[0], max_points, replace=False)
            x_pca_sampled = x_pca[idx]
            colors = np.arange(max_points)
        else:
            x_pca_sampled = x_pca
            colors = np.arange(x_pca.shape[0])

        fig = px.scatter_3d(
            x=x_pca_sampled[:, 0],
            y=x_pca_sampled[:, 1],
            z=x_pca_sampled[:, 2],
            color=colors,
            labels={'x': 'PC1', 'y': 'PC2', 'z': 'PC3'},
            title="PCA Projection (3D)",
            opacity=0.7,
            color_continuous_scale="Viridis"
        )

        fig.write_html("docs/graphics/pca/pca_projection_3D_interactive.html")
        logging.info("Interactive 3D PCA plot saved as pca_projection_3D_interactive.html")

    logging.info(f"PCA applied successfully: {x_pca.shape[1]} components obtained in `x_pca`")
    return x_pca, n_components


def reduce_dimensions():
    """Pipeline de traitement ML"""
    print("\n ======= Analyse dimensions ======= \n")
    print("1. Splitting\n---------------------------------")
    dataset = splitting()

    print("\n2. Analyse\n---------------------------------")
    x_all, y_all = dataset['all'][0], dataset['all'][1]
    x_pca, n_components = apply_pca(x_all)

    return {"pca": x_pca}


if __name__ == "__main__":
    reduce_dimensions()
