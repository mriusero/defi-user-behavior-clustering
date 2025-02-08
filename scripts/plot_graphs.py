import pandas as pd
import networkx as nx
from tqdm import tqdm
from pyarrow import feather
from pyvis.network import Network
import matplotlib
import seaborn as sns

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
    addresses = set(df[address_col])
    protocols = set(protocol_cols)
    for address in tqdm(addresses, desc="Adding addresses", unit="address"):
        G.add_node(
            address,
            label=address[:config['address_label_length']],
            color=config['address_color'],
            size=config['address_node_size']
        )
    for protocol in tqdm(protocols, desc="Adding protocols", unit="protocol"):
        G.add_node(
            protocol,
            label=protocol,
            color=config['protocol_color'],
            size=config['protocol_node_size']
        )
    for _, row in tqdm(df.iterrows(), total=df.shape[0], desc="Adding edges", unit="row"):
        sender = row[address_col]
        for protocol in protocol_cols:
            if row[protocol] > 0:
                G.add_edge(
                    sender,
                    protocol,
                    weight=min(row[protocol], config['max_weight']),
                    width=config['edge_width'],
                    color=config['edge_color']
                )
    return G

def build_address_address_graph(df):
    """Build a transaction graph between addresses."""
    print(f"===== Building address-to-address graph ======\n")
    config = {
        'edge_color': 'silver',
        'edge_width': 1,
        'node_size': 200,
        'max_weight': 10
    }
    G = nx.DiGraph()
    df['value (ETH)'] = pd.to_numeric(df['value (ETH)'], errors='coerce')
    tx = df[['from', 'to', 'value (ETH)']]
    tx = tx[tx['value (ETH)'] > 0]
    total_transactions = pd.Series(0, index=pd.concat([tx['from'], tx['to']]).unique())

    for _, row in tqdm(tx.iterrows(), total=tx.shape[0], desc="Adding transaction edges", unit="transaction"):
        sender = row['from']
        receiver = row['to']
        value = row['value (ETH)']

        total_transactions[sender] += value
        total_transactions[receiver] += value

        if G.has_edge(sender, receiver):
            G[sender][receiver]['weight'] += min(value, config['max_weight'])
        else:
            G.add_edge(
                sender,
                receiver,
                weight=min(value, config['max_weight']),
                color=config['edge_color'],
                width=config['edge_width']
            )
    cmap = sns.color_palette("viridis", as_cmap=True)
    for node in G.nodes:
        G.nodes[node]['color'] = matplotlib.colors.rgb2hex(cmap((total_transactions[node])))

    return G

def visualize_graph(G, filename):
    """Visualize the graph with a progress bar for nodes and edges."""
    print(f"--> Building visualization graph")
    net = Network(height="800px", width="100%", notebook=False)
    net.from_nx(G)
    net.save_graph(filename)
    print(f"--> Graph successfully saved to {filename}")

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
    transactions = pd.read_parquet("data/raw/transactions.parquet", engine='pyarrow')

    features = features.sample(10000, random_state=42)
    transactions = transactions.sample(10000, random_state=42)

    G_protocol_type = build_bipartite_graph(features, 'address', protocols_type, 'address-to-protocol_type')
    visualize_graph(G_protocol_type, "docs/graphics/network/address_protocol_type_graph.html")

    G_protocol = build_bipartite_graph(features, 'address', protocols, 'address-to-protocol')
    visualize_graph(G_protocol, "docs/graphics/network/address_protocol_graph.html")

    G_address = build_address_address_graph(transactions)
    visualize_graph(G_address, "docs/graphics/network/address_address_graph.html")
