import time
import torch
import numpy as np
from tqdm import tqdm
import datashader as ds
import datashader.transfer_functions as tf
import networkx as nx
import pandas as pd
from datashader.utils import export_image
from datashader.bundling import connect_edges
from datashader.layout import random_layout, circular_layout, forceatlas2_layout

from build_networks import build_address_tx_graph

initial_start = time.time()

def time_taken(start, step_name):
    """Affiche le temps écoulé pour une étape donnée"""
    elapsed_time = time.time() - start
    print(f"{step_name} took {elapsed_time:.2f} seconds.\n")

GRAPH_TYPE = "address_tx_graph"             # PARAMS
BATCH_SIZE = 100000
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"\n--> device: {DEVICE} <--\n")

# Data loading
start = time.time()
print("-- Data loading --")
transactions = pd.read_parquet("data/raw/transactions.parquet", engine='pyarrow')       # Chargement des données
transactions = transactions.sample(100000, random_state=42)
time_taken(start, "Data loading")

# Network building
start = time.time()
G_address = build_address_tx_graph(transactions)                                            # Construction du graphe
time_taken(start, "Graph building")

# Mapping ethereum addresses to indexes
start = time.time()
print("-- Address mapping --")
address_to_idx = {address: idx for idx, address in enumerate(G_address.nodes())}
time_taken(start, "Address mapping")


# Nodes computing
start = time.time()
print("-- Nodes computing --")
pos = nx.spring_layout(G_address, k=0.15, iterations=10, seed=42)
pos_array = np.array(list(pos.values()), dtype=np.float32)
pos_tensor = torch.tensor(pos_array, device=DEVICE)
all_positions = []
pbar = tqdm(range(0, len(pos), BATCH_SIZE), desc="Calcul des positions", ncols=100, dynamic_ncols=True, position=0)
for i in pbar:
    batch_positions = pos_tensor[i:i + BATCH_SIZE].cpu().numpy()
    all_positions.append(batch_positions)
    pbar.set_postfix({'batch': i})
    pbar.refresh()

pos = {n: pos_tensor[i].cpu().numpy() for i, n in enumerate(G_address.nodes())}     #Mapping nodes positions

nodes_tensor = torch.tensor(np.array(list(pos.values()), dtype=np.float32), device=DEVICE)      # Conversion des positions en DataFrame
nodes = pd.DataFrame(nodes_tensor.cpu().numpy(), index=pos.keys(), columns=['x', 'y'])
nodes["size"] = 0.5
time_taken(start, "Nodes computing")


# Edges computing
start = time.time()
print("-- Edges computing --")
edges = pd.DataFrame(G_address.edges(), columns=['source', 'target'])
all_edges = []
pbar = tqdm(range(0, len(edges), BATCH_SIZE), desc="Calcul des arêtes", ncols=100, dynamic_ncols=True, position=1)
for i in pbar:
    batch_edges = edges[i:i + BATCH_SIZE]
    src_idx = torch.tensor([address_to_idx[src] for src in batch_edges["source"]], dtype=torch.long, device=DEVICE)
    tgt_idx = torch.tensor([address_to_idx[tgt] for tgt in batch_edges["target"]], dtype=torch.long, device=DEVICE)
    edges_x = torch.stack((nodes_tensor[src_idx, 0], nodes_tensor[tgt_idx, 0]), dim=1)
    edges_y = torch.stack((nodes_tensor[src_idx, 1], nodes_tensor[tgt_idx, 1]), dim=1)
    all_edges.append(pd.DataFrame({'x': edges_x.cpu().numpy().flatten(), 'y': edges_y.cpu().numpy().flatten()}))
    pbar.set_postfix({'batch': i})
    pbar.refresh()

edges_df = pd.concat(all_edges, ignore_index=True)
time_taken(start, "Edges computing")


# Canvas computing
start = time.time()
print("-- Canvas computing --")
canvas_width = min(len(G_address.nodes) // 10, 5000)
canvas_height = canvas_width
canvas = ds.Canvas(plot_width=canvas_width, plot_height=canvas_height)
time_taken(start, "Canvas computing")


# Aggregating nodes and edges
start = time.time()
print("-- Aggregating nodes and edges --")
nodes_agg = canvas.points(nodes, 'x', 'y', ds.sum('size'))
edge_agg = canvas.line(edges_df, 'x', 'y', ds.count())
time_taken(start, "Aggregating nodes and edges")


# Exporting image
start = time.time()
print("-- Exporting image --")
img = tf.stack(
    tf.shade(
            edge_agg, cmap=["lightgray", "black"]
        ),
          tf.shade(
            nodes_agg, cmap=["red", "yellow"]
        )
)
export_image(img, f"docs/graphics/address-tx/{GRAPH_TYPE}_nx_plot")
time_taken(start, "Exporting image")

time_taken(initial_start, "TOTAL PROCESS")