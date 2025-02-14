from tqdm import tqdm
import pandas as pd
import networkx as nx
from collections import defaultdict


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


def build_address_tx_graph(df):
    """Build a transaction graph between addresses."""
    print(f"===== Building address-tx graph ======\n")
    config = {
        'max_weight': 10
    }
    G = nx.DiGraph()
    df['value (ETH)'] = pd.to_numeric(df['value (ETH)'], errors='coerce').fillna(0).astype(int)
    tx = df[['from', 'to', 'value (ETH)']]
    tx = tx[tx['value (ETH)'] > 0]

    total_transactions = defaultdict(int)
    grouped = tx.groupby(['from', 'to'])['value (ETH)'].sum().reset_index()

    for _, row in tqdm(grouped.iterrows(), total=grouped.shape[0], desc="Adding transaction edges", unit="transaction"):
        sender = row['from']
        receiver = row['to']
        value = row['value (ETH)']

        total_transactions[sender] += value
        total_transactions[receiver] += value

        G.add_edge(
            sender,
            receiver,
            weight=min(value, config['max_weight']),
        )

    return G