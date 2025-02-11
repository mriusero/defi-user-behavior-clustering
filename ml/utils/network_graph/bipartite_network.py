from tqdm import tqdm
import networkx as nx

def build_bipartite_graph(df, address_col, protocol_cols, graph_type='address-protocol'):
    """Build a bipartite graph between addresses and protocols."""
    print(f"\n===== Building {graph_type} graph ======\n")
    config = {
        'address_label_length': 6,
        'max_weight': 100,
        'address_cat': 'address'
    }
    G = nx.Graph()

    address_nodes = set(df[address_col].unique())
    protocol_nodes = set(protocol_cols)

    nodes = [
        (address, {'label': address[:config['address_label_length']], 'cat': config['address_cat']})
        for address in tqdm(address_nodes, desc="Adding addresses", unit="address")
    ]
    nodes.extend(
        (protocol, {'label': protocol, 'cat': protocol})
        for protocol in tqdm(protocol_nodes, desc="Adding protocols", unit="protocol")
    )
    G.add_nodes_from(nodes)

    edges = []
    for row in tqdm(df.itertuples(index=False), total=df.shape[0], desc="Adding edges", unit="row"):
        sender = getattr(row, address_col)
        for protocol in protocol_cols:
            if getattr(row, protocol) > 0:
                edges.append((sender, protocol, {'weight': min(getattr(row, protocol), config['max_weight'])}))
    G.add_edges_from(edges)

    return G