import torch
from torch_geometric.data import Data
import pandas as pd


class GraphBuilder:
    """Creates a graph structure from user-protocol interactions."""

    def __init__(self, data, address_col, protocol_cols):
        self.x_all = data['all'][0]
        self.y_all = data['all'][1]
        self.df = pd.concat([self.x_all, self.y_all], axis=1)
        self.address_col = address_col
        self.protocol_cols = protocol_cols
        self.addresses = list(set(self.df[address_col]))
        self.protocols = protocol_cols

        self.address_to_idx = {address: idx for idx, address in enumerate(self.addresses)}
        self.protocol_to_idx = {protocol: idx + len(self.addresses) for idx, protocol in enumerate(self.protocols)}

    def build_graph(self):
        """Constructs edge list and node features for GNN."""
        edge_index, edge_attr = self._get_edges()
        node_features = self._get_features()
        return Data(x=node_features, edge_index=edge_index, edge_attr=edge_attr)

    def _get_edges(self):
        """Constructs edges between users and protocols."""
        edges = []
        edge_weights = []
        for idx, row in self.df.iterrows():
            sender = row[self.address_col]
            sender_idx = self.address_to_idx[sender]

            for protocol in self.protocol_cols:
                if row[protocol] > 0:
                    protocol_idx = self.protocol_to_idx[protocol]
                    weight = row[protocol]
                    edges.append((sender_idx, protocol_idx))
                    edge_weights.append(weight)

        edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()
        edge_attr = torch.tensor(edge_weights, dtype=torch.float).view(-1, 1)
        return edge_index, edge_attr

    def _get_features(self):
        """Extracts numerical features for nodes."""
        features = self.df.drop(columns=[self.address_col]).values
        return torch.tensor(features, dtype=torch.float)