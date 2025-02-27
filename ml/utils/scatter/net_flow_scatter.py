import pandas as pd
import numpy as np
import pyarrow.feather as feather
import datashader as ds
import datashader.transfer_functions as tf
from datashader.utils import export_image
import matplotlib.pyplot as plt


def load_data(users_path, clusters_path):
    """ Load the predictions and features dataframes and merge them """
    users = feather.read_table(users_path).to_pandas()
    clusters = feather.read_table(clusters_path).to_pandas()
    return pd.merge(users, clusters, on='address', how='left')


def generate_coordinates(df, seed=0, with_cluster=False):
    """  Génère des coordonnées aléatoires autour des centres des clusters.   """
    if with_cluster:
        cluster_centers = {
            0: [0.2, 0.2],
            1: [0.8, 0.2],
            2: [0.2, 0.8],
            3: [0.8, 0.8]
        }
        np.random.seed(seed)
        df['x'] = df['cluster'].apply(lambda cluster: np.random.normal(loc=cluster_centers[cluster][0], scale=0.15))
        df['y'] = df['cluster'].apply(lambda cluster: np.random.normal(loc=cluster_centers[cluster][1], scale=0.15))
    else:
        np.random.seed(0)
        df['x'] = np.random.normal(loc=0.5, scale=0.1, size=len(df))
        df['y'] = np.random.normal(loc=0.5, scale=0.1, size=len(df))
    return df


def define_size(df, column_name='net_flow_eth'):
    """  Normalise la taille en fonction de la colonne spécifiée et applique une transformation exponentielle. """
    df['size'] = np.abs(df[column_name])
    size_range = df['size'].max() - df['size'].min()
    if size_range != 0:
        df['size'] = (df['size'] - df['size'].min()) / size_range
    else:
        df['size'] = 1
    df['size'] = np.log1p(df['size'])
    df['size'] *= 1000
    return df


def plot_aggregates(agg_positive, agg_negative):
    """  Visualise aggregats  """
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.title('Aggregate Positive')
    plt.imshow(agg_positive, cmap='viridis')
    plt.colorbar()

    plt.subplot(1, 2, 2)
    plt.title('Aggregate Negative')
    plt.imshow(agg_negative, cmap='viridis')
    plt.colorbar()

    plt.savefig('docs/graphics/network/color_range.png')
    plt.close()


def create_canvas(df):
    """ Create Canvas """
    x_min, x_max = df['x'].min(), df['x'].max()
    y_min, y_max = df['y'].min(), df['y'].max()

    cvs = ds.Canvas(plot_width=3000, plot_height=3000, x_range=(x_min, x_max), y_range=(y_min, y_max))

    positive_flow = df[df['net_flow_eth'] > 0]
    negative_flow = df[df['net_flow_eth'] < 0]

    agg_positive = cvs.points(positive_flow, 'x', 'y', ds.sum('size'))
    agg_negative = cvs.points(negative_flow, 'x', 'y', ds.sum('size'))

    return agg_positive, agg_negative


def save_image(agg_positive, agg_negative, output_path):
    """ Shade, Stack and Save the final Image """
    img_positive = tf.shade(agg_positive, cmap=['green', 'lightgreen'], how='log', alpha=180)
    img_negative = tf.shade(agg_negative, cmap=['red', 'lightcoral'], how='log', alpha=180)

    img = tf.stack(img_positive, img_negative)
   # img = tf.set_background(img, color='white')
    img = tf.Image(img)

    export_image(img, output_path)
    print(f"Image saved at: {output_path}")


def main():

    df = load_data(
        users_path='data/features/features.arrow',
        clusters_path="data/clustering/kmeans/kmeans_predictions.arrow"
    )

    df = generate_coordinates(df,
        seed=0,
        with_cluster=True
    )

    df = define_size(df,
        column_name='net_flow_eth'
    )

    agg_positive, agg_negative = create_canvas(df)
    plot_aggregates(agg_positive, agg_negative)

    save_image(
        agg_positive, agg_negative,
        output_path='docs/graphics/network/net_flow_scatter'
    )

if __name__ == "__main__":
    main()