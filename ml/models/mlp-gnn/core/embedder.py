import mlx.core as mx
import mlx.nn as nn
from sklearn.decomposition import PCA
import plotly.express as px
import numpy as np

class MLXEmbedder:
    """Computes embeddings using MLX for Apple Silicon GPUs."""

    def __init__(self, input_dim, output_dim):
        self.model = nn.Linear(input_dim, output_dim)

    def compute_embeddings(self, features):
        """Converts tabular features into MLX-processed embeddings."""
        x = mx.array(features.to_numpy())
        print(f"Input shape: {x.shape}")
        return self.model(x)

    @staticmethod
    def plot_embeddings(embeddings):
        """Visualizes embeddings using PCA."""
        embeddings = np.random.choice(embeddings, size=1000, replace=False)
        pca = PCA(n_components=3)
        reduced_embeddings = pca.fit_transform(embeddings)
        colors = np.arange(reduced_embeddings.shape[0])
        fig = px.scatter_3d(
            x=reduced_embeddings[:, 0],
            y=reduced_embeddings[:, 1],
            z=reduced_embeddings[:, 2],
            color=colors,
            title="PCA of Embeddings in 3D",
            labels={"x": "PCA Component 1", "y": "PCA Component 2", "z": "PCA Component 3"},
            opacity=0.7,
            color_continuous_scale="Viridis",
        )
        fig.update_traces(marker=dict(size=5, opacity=0.6))
        fig.write_html('docs/graphics/embeddings/embeddings_plot.html')
        print(f"Embedding plot saved to 'docs/graphics/embeddings/embeddings_plot.html'")