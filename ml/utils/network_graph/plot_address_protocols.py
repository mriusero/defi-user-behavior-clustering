import time
import pandas as pd
import networkx as nx
from pyarrow import feather
import multiprocessing as mp
import datashader as ds
import datashader.transfer_functions as tf
from datashader.layout import forceatlas2_layout
from datashader.bundling import hammer_bundle
from datashader.utils import export_image
import dask.array as da
import dask.dataframe as dd

from bipartite_network import build_bipartite_graph

CVSOPTS = dict(plot_height=4000, plot_width=4000)
NUM_P = mp.cpu_count()

COLOR_KEY = {
    "curve_dao_count":       "#FF6347",
    "aave_count":            "#4e000b",
    "uniswap_count":         "#1e8b22",
    "maker_count":           "#ffc909",
    "tether_count":          "#DC143C",
    "yearn_finance_count":   "#c24ee2",
    "usdc_count":            "#00CED1",
    "dai_count":             "#FFFFFF",
    "balancer_count":        "#7FFF00",
    "harvest_finance_count": "#efef24",
    "nftfi_count":           "#FF1493",
    "address":               "#12a7bb",
}

def time_taken(start, step_name):
    """Affiche le temps écoulé pour une étape donnée"""
    elapsed_time = time.time() - start
    print(f"{step_name} took {elapsed_time:.2f} seconds.")


def process_image(agg, px_size, min_alpha, shape, name, color_key=None, color_baseline=None):
    """Génère une image pour la catégorie 'address' et une image pour les autres catégories."""
    if color_key is None:
        color_key = COLOR_KEY
    if color_baseline is None:
        color_baseline = agg.min().item()
    shaded_img = tf.shade(
        agg,
        cmap=list(color_key.values()),
        color_key=COLOR_KEY,
        how='eq_hist',
        alpha=255,
        min_alpha=min_alpha,
        span=None,
        name=name,
        color_baseline=color_baseline,
        rescale_discrete_levels=True
    )
    return tf.spread(
        shaded_img,
        px=px_size,
        shape=shape,
        how=None,
        mask=None,
        name=name
    )

def visualize_graph(graph, graph_type):
    """Efficient visualization of the graph using Datashader, with Dask for parallel computing."""

    start = time.time()
    print(f"\n1. -- Building layout --")

    def process_nodes_layout(layout):
        """Transforme le layout calculé sur le CPU en DataFrame Dask pour traitement parallèle"""
        nodes = pd.DataFrame(layout).T.rename(columns={0: 'x', 1: 'y'})
        nodes['cat'] = [graph.nodes[node].get('cat', 'unknown') for node in graph.nodes()]
        nodes['cat'] = nodes['cat'].astype('category')
        return dd.from_pandas(nodes, npartitions=NUM_P)

    layout = nx.fruchterman_reingold_layout(graph, iterations=1)
    nodes = process_nodes_layout(layout)
    edges = dd.from_pandas(pd.DataFrame(list(graph.edges), columns=['source', 'target']), npartitions=NUM_P*2)

    time_taken(start, "Building layout")

    start = time.time()
    print(f"\n2. -- Computing Canvas --")

    nodes_x = da.asarray(nodes['x'].values, chunks=(10000))
    nodes_y = da.asarray(nodes['y'].values, chunks=(10000))
    x_min, x_max = nodes_x.min().compute_chunk_sizes(), nodes_x.max().compute_chunk_sizes()
    y_min, y_max = nodes_y.min().compute_chunk_sizes(), nodes_y.max().compute_chunk_sizes()
    canvas = ds.Canvas(
        x_range=(x_min, x_max),
        y_range=(y_min, y_max),
        **CVSOPTS
    )
    time_taken(start, "Computing Canvas")


    start = time.time()
    print(f"\n3. -- Computing plot --")
    name = "Force-directed, bundled"
    cat = "cat"
    fd_nodes = forceatlas2_layout(nodes.compute(), edges.compute())
    bd_edges = hammer_bundle(fd_nodes, edges.compute(), initial_bandwidth=0.05)
    time_taken(start, "Computing plot")

    start = time.time()
    print(f"\n3.1 -- Processing nodesplot --")
    assert not fd_nodes.isnull().any().any(), "Nodes data contains NaN values"
    aggregator = None if cat is None else ds.count_cat(cat)
    agg = canvas.points(dd.from_pandas(fd_nodes, npartitions=NUM_P), 'x', 'y', aggregator)

    images = []

    unique_categories = fd_nodes[cat].unique()
    other_categories = [category for category in unique_categories if category != "address"]

    if "address" in unique_categories:
        agg_address = agg.sel(**{cat: "address"})
        contains_nan = agg_address.isnull().any()
        print("\n3.1.1 -- 'address' images : ( NaN=", contains_nan.item(), ")")
        images.append(process_image(agg_address, px_size=15, min_alpha=200, shape='circle', name=name, color_key={"address": "#f4676c"}))
        time_taken(start, "Processing Address")

    if other_categories:
        agg_others = agg.sel(**{cat: other_categories})
        contains_nan = agg_others.isnull().any()
        start = time.time()
        print("\n3.1.2 -- processing 'protocols' images : ( NaN=", contains_nan.item(), ")")
        images.append(process_image(agg_others, px_size=15, min_alpha=255, shape='square', name=name))
        time_taken(start, "Processing Categories")

    np = tf.stack(*images)
    time_taken(start, "Total processing nodesplot")

    start = time.time()
    print(f"\n3.2 -- Processing edgesplot --")
    ep = tf.shade(
        canvas.line(
            dd.from_pandas(bd_edges, npartitions=NUM_P),
            'x', 'y',
            agg=ds.count()
        ), name=name
    )
    time_taken(start, "Processing edgesplot")

    start = time.time()
    print(f"\n4. -- Stacking edgesplot & nodesplot --")
    nx_img = tf.stack(ep, np, how="over", name=name)
    time_taken(start, "Stacking edgesplot & nodesplot")

    start = time.time()
    print(f"\n5. -- Exporting image --")
    export_image(nx_img, f"docs/graphics/address_protocol/{graph_type}_nx_plot")
    time_taken(start, "Exporting image")

    print(f"\nImage exported succesfully!\n")
# -----------------------------------------------


if __name__ == "__main__":
    protocols = [
        'curve_dao_count', 'aave_count', 'uniswap_count', 'maker_count', 'tether_count', 'yearn_finance_count',
        'usdc_count', 'dai_count', 'balancer_count','harvest_finance_count', 'nftfi_count'
    ]
    table = feather.read_table("data/features/features.arrow")
    features = table.to_pandas()
    features = features.sample(100000, random_state=42)

    start = time.time()
    G_protocol = build_bipartite_graph(features, 'address', protocols, 'address-to-protocol')
    time_taken(start, "Total network building")

    start = time.time()
    visualize_graph(G_protocol, "address_protocol")
    time_taken(start, "Total graph building")