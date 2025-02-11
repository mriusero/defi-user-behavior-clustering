import time
import networkx as nx
import pandas as pd
from pyarrow import feather
import datashader as ds
import datashader.transfer_functions as tf
from datashader.layout import forceatlas2_layout
from datashader.bundling import hammer_bundle
from datashader.utils import export_image

from bipartite_network import build_bipartite_graph

CVSOPTS = dict(plot_height=5000, plot_width=5000)

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

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Time for {func.__name__} : {end_time - start_time} sec\n")
        return result
    return wrapper


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
    return tf.spread(shaded_img, px=px_size, shape=shape, how=None, mask=None, name=name)

@timing_decorator
def nodesplot(nodes, name=None, canvas=None, cat=None):
    """Génère une image pour les nœuds."""
    print(f"--> Building nodesplot")
    assert not nodes.isnull().any().any(), "Nodes data contains NaN values"

    aggregator = None if cat is None else ds.count_cat(cat)
    agg = canvas.points(nodes, 'x', 'y', aggregator)
    images = []

    unique_categories = nodes[cat].unique()
    other_categories = [category for category in unique_categories if category != "address"]

    if "address" in unique_categories:
        agg_address = agg.sel(**{cat: "address"})
        contains_nan = agg_address.isnull().any()
        print("--> processing 'address' images : ( NaN=", contains_nan.item(), ")")
        images.append(process_image(agg_address, px_size=15, min_alpha=200, shape='circle', name=name,  color_key={"address": "#f4676c"}))

    if other_categories:
        agg_others = agg.sel(**{cat: other_categories})
        contains_nan = agg_others.isnull().any()
        print("--> processing 'protocols' images : ( NaN=", contains_nan.item(),")")
        images.append(process_image(agg_others, px_size=15, min_alpha=255, shape='square', name=name))

    return tf.stack(*images)

@timing_decorator
def edgesplot(edges, name=None, canvas=None):
    print(f"--> Building edgesplot")
    return tf.shade(canvas.line(edges, 'x', 'y', agg=ds.count()), name=name)

@timing_decorator
def graphplot(nodes, edges, name="", canvas=None, cat=None):
    print(f"--> Building graph_plot")
    np = nodesplot(nodes, name + " nodes", canvas, cat)
    ep = edgesplot(edges, name + " edges", canvas)
    return tf.stack(ep, np, how="over", name=name)


@timing_decorator
def nx_layout(graph):
    """Generate node positions using spring layout."""
    print(f"--> Building layout")
    layout = nx.fruchterman_reingold_layout(graph, iterations=1)
    nodes = pd.DataFrame(layout).T.rename(columns={0: 'x', 1: 'y'})
    nodes.set_index(nodes.index, inplace=True)
    nodes['cat'] = [graph.nodes[node].get('cat', 'unknown') for node in graph.nodes()]
    nodes['cat'] = nodes['cat'].astype('category')
    edges = pd.DataFrame(list(graph.edges), columns=['source', 'target'])
    return nodes, edges

@timing_decorator
def nx_plot(canvas=None, nodes=None, edges=None, cat=None):
    print(f"--> Building nx_plot")
    fd = forceatlas2_layout(nodes, edges)
    return graphplot(fd, hammer_bundle(fd, edges, initial_bandwidth=0.05), "Force-directed, bundled", canvas=canvas, cat=cat)

@timing_decorator
def visualize_graph(G, graph_type):
    """Efficient visualization of the graph using Datashader."""
    nodes, edges = nx_layout(G)
    print(f"--> Building canvas")
    canvas = ds.Canvas(
        x_range=(nodes.x.min(), nodes.x.max()),
        y_range=(nodes.y.min(), nodes.y.max()),
        **CVSOPTS
    )
    nx_img = nx_plot(canvas=canvas, nodes=nodes, edges=edges, cat="cat")
    export_image(nx_img, f"docs/graphics/address_protocol/{graph_type}_nx_plot")
    print(f"Image exported succesfully !")


if __name__ == "__main__":
    protocols = [
        'curve_dao_count', 'aave_count', 'uniswap_count', 'maker_count', 'tether_count', 'yearn_finance_count',
        'usdc_count', 'dai_count', 'balancer_count','harvest_finance_count', 'nftfi_count'
    ]
    table = feather.read_table("data/features/features.arrow")
    features = table.to_pandas()
    features = features#.sample(100000, random_state=42)

    G_protocol = build_bipartite_graph(features, 'address', protocols, 'address-to-protocol')
    visualize_graph(G_protocol, "address_protocol")
