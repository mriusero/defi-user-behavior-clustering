import time
import networkx as nx
import pandas as pd
from tqdm import tqdm
from pyarrow import feather
import datashader as ds
import datashader.transfer_functions as tf
from datashader.bundling import connect_edges, hammer_bundle
from datashader.utils import export_image


def build_bipartite_graph(df, address_col, protocol_cols, graph_type='address-protocol'):
    """Build a bipartite graph between addresses and protocols."""
    print(f"\n===== Building {graph_type} graph ======\n")
    config = {
        'address_color': 'blue',
        'address_label_length': 6,
        'address_node_size': 10,
        'protocol_color': 'red',
        'protocol_node_size': 25,
        'edge_color': 'silver',
        'edge_width': 1,
        'max_weight': 100
    }
    G = nx.Graph()

    nodes = []
    for address in tqdm(df[address_col].unique(), desc="Adding addresses", unit="address"):
        nodes.append((address, {'label': address[:config['address_label_length']],
                                'color': config['address_color'], 'size': config['address_node_size']}))
    for protocol in tqdm(protocol_cols, desc="Adding protocols", unit="protocol"):
        nodes.append(
            (protocol, {'label': protocol, 'color': config['protocol_color'], 'size': config['protocol_node_size']}))
    G.add_nodes_from(nodes)

    edges = []
    for _, row in tqdm(df.iterrows(), total=df.shape[0], desc="Adding edges", unit="row"):
        sender = row[address_col]
        for protocol in protocol_cols:
            if row[protocol] > 0:
                edges.append((sender, protocol, {'weight': min(row[protocol], config['max_weight']),
                                                 'width': config['edge_width'], 'color': config['edge_color']}))
    G.add_edges_from(edges)
    return G

cvsopts = dict(plot_height=5000, plot_width=5000)

def nodesplot(nodes, name=None, canvas=None, cat=None):
    aggregator = None if cat is None else ds.count_cat(cat)
    agg = canvas.points(nodes, 'x', 'y', aggregator)
    return tf.spread(tf.shade(agg, cmap=["#FF3333"]), px=1, name=name)

def edgesplot(edges, name=None, canvas=None):
    return tf.shade(canvas.line(edges, 'x', 'y', agg=ds.count()), name=name)

def graphplot(nodes, edges, name="", canvas=None, cat=None):
    np = nodesplot(nodes, name + " nodes", canvas, cat)
    ep = edgesplot(edges, name + " edges", canvas)
    return tf.stack(ep, np, how="over", name=name)

def nx_layout(graph):
    """Generate node positions using spring layout."""
    layout = nx.fruchterman_reingold_layout(graph, iterations=1)
    nodes = pd.DataFrame(layout).T.rename(columns={0: 'x', 1: 'y'})
    nodes.set_index(nodes.index, inplace=True)
    edges = pd.DataFrame(list(graph.edges), columns=['source', 'target'])
    return nodes, edges

def nx_plot(canvas=None, nodes=None, edges=None):
    bundled_bw005 = hammer_bundle(nodes, edges)
    return [
        graphplot(nodes, bundled_bw005, "Bundled bw=0.05", canvas=canvas),
    ]

def visualize_graph(G, graph_type):
    """Efficient visualization of the graph using Datashader."""
    print(f"--> Building visualization graph")

    nodes, edges = nx_layout(G)
    canvas = ds.Canvas(x_range=(nodes.x.min(), nodes.x.max()), y_range=(nodes.y.min(), nodes.y.max()), **cvsopts)
    nx_images = nx_plot(canvas=canvas, nodes=nodes, edges=edges)

    for i, img in enumerate(nx_images):
        export_image(img, f"docs/graphics/address_protocol/{graph_type}_nx_plot_{i}")
        print(f"--> Exported image {i} for {graph_type} graph")

if __name__ == "__main__":
    protocols_type = [
        'type_dex', 'type_lending', 'type_stablecoin',
        'type_yield_farming', 'type_nft_fi'
    ]
    protocols = [
        'curve_dao_count', 'aave_count', 'uniswap_count',
        'maker_count', 'tether_count', 'yearn_finance_count',
        'usdc_count', 'dai_count', 'balancer_count',
        'harvest_finance_count', 'nftfi_count'
    ]
    table = feather.read_table("data/features/features.arrow")
    features = table.to_pandas()
    features = features.sample(100000, random_state=42)

    G_protocol = build_bipartite_graph(features, 'address', protocols, 'address-to-protocol')

    start_time = time.time()
    visualize_graph(G_protocol, "address_protocol")
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Total time for 'visualize_graph': {execution_time:.2f} seconds")