import pandas as pd
from pyarrow import feather
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns


def load_data():
    """Load the data from the feather files."""
    users = feather.read_table('data/features/features.arrow').to_pandas()
    results = feather.read_table('data/clustering/kmeans/kmeans_predictions.arrow').to_pandas()
    df = pd.merge(users, results, on='address', how='left')
    return df


def plot_general_heatmap(df, base_path):
    """ Plot and save a general heatmap of the correlation between clusters and variables."""
    df2 = df.copy().drop(columns=['address'], errors='ignore')
    df_encoded = pd.get_dummies(df2, columns=['cluster'])

    correlation_matrix = df_encoded.corr()
    cluster_columns = [col for col in df_encoded.columns if col.startswith('cluster_')]
    cluster_correlation = correlation_matrix.loc[cluster_columns, :].drop(columns=cluster_columns)

    plt.figure(figsize=(15, 5))
    sns.heatmap(
        cluster_correlation,
        annot=False,
        cmap='viridis',
        cbar_kws={'label': 'Correlation'},
        linewidths=.5,
        linecolor='gray'
    )

    plt.title('Correlation heatmap by clusters by variables')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()

    try:
        plt.savefig(f'{base_path}/general_heatmap.png')
        print(f"--> general heatmap saved.")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"--> Error: {base_path} does not exist.") from exc



def plot_heatmap(base_path):
    """Plot and save a heatmap of the metrics for each cluster."""

    df = load_data()
    plot_general_heatmap(df, base_path)

    features = df.columns.drop(['address', 'cluster'])

    for cluster in df['cluster'].unique():
        cluster_data = df[df['cluster'] == cluster]
        correlation_matrix = cluster_data[features].corr()

        fig = px.imshow(correlation_matrix,
                        title=f'Heatmap de corrélation pour le cluster {cluster}',
                        labels=dict(color="Corrélation"),
                        x=features,
                        y=features,
                        color_continuous_scale="Viridis")
        try:
            fig.write_html(f'{base_path}/heatmap_{cluster}.html')
            print(f"--> heatmap {cluster} saved.")
        except FileNotFoundError as exc:
            raise FileNotFoundError(f"--> Error: {base_path} does not exist.") from exc