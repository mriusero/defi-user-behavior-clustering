import os
import hashlib
import pickle
import torch
from torch_geometric.data import Data
import pandas as pd

class GraphBuilder:
    """Creates a graph structure from user-protocol interactions with caching."""

    def __init__(self, data, address_col, protocol_cols, cache_dir="tmp/"):
        self.data = data
        self.address_col = address_col
        self.protocol_cols = protocol_cols
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def _get_cache_path(self):
        """Generates a unique cache filename based on data hash before processing."""
        hash_input = pickle.dumps(self.data)  # Hash the input data
        hash_digest = hashlib.md5(hash_input).hexdigest()
        return os.path.join(self.cache_dir, f"graph_{hash_digest}.pkl")

    def build_graph(self):
        """Loads graph from cache or builds it if not cached."""
        cache_path = self._get_cache_path()

        if os.path.exists(cache_path):
            print(f"Loading graph from cache: {cache_path}")
            with open(cache_path, "rb") as f:
                return pickle.load(f)

        print("Cache not found, building graph...")
        graph = self._compute_graph()

        with open(cache_path, "wb") as f:
            pickle.dump(graph, f)

        return graph

    def _compute_graph(self):
        """Compute the graph only if needed."""
        x_all = self.data['all'][0]
        y_all = self.data['all'][1]
        df = pd.concat([x_all, y_all], axis=1)

        addresses = list(set(df[self.address_col]))
        address_to_idx = {address: idx for idx, address in enumerate(addresses)}
        protocol_to_idx = {protocol: idx + len(addresses) for idx, protocol in enumerate(self.protocol_cols)}

        edge_index, edge_attr = self._get_edges(df, address_to_idx, protocol_to_idx)
        node_features = self._get_features(df)

        print(f"Node features shape: {node_features.shape}")
        print(f"Edge index shape: {edge_index.shape}")
        print(f"Edge attributes shape: {edge_attr.shape if edge_attr is not None else 'None'}")

        return Data(x=node_features, edge_index=edge_index, edge_attr=edge_attr)

    def _get_edges(self, df, address_to_idx, protocol_to_idx):
        """Constructs edges between users and protocols."""
        edges = []
        edge_weights = []
        for _, row in df.iterrows():
            sender = row[self.address_col]
            sender_idx = address_to_idx[sender]

            for protocol in self.protocol_cols:
                if row[protocol] > 0:
                    protocol_idx = protocol_to_idx[protocol]
                    weight = row[protocol]
                    edges.append((sender_idx, protocol_idx))
                    edge_weights.append(weight)

        edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()
        edge_attr = torch.tensor(edge_weights, dtype=torch.float).view(-1, 1)
        return edge_index, edge_attr

    def _get_features(self, df):
        """Extracts numerical features for nodes."""
        features = df.drop(columns=[self.address_col]).values
        return torch.tensor(features, dtype=torch.float)