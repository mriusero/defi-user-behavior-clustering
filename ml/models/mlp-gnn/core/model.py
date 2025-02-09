import torch
import torch.nn as nn
import torch.nn.functional as F
import torch_geometric
from torch_geometric.nn import GCNConv, global_mean_pool

# MLP pour les caractéristiques utilisateurs
class MLP(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# GNN avec PyTorch Geometric
class GNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(GNN, self).__init__()
        self.conv1 = GCNConv(input_size, hidden_size)  # Convolution sur les noeuds du graphe
        self.conv2 = GCNConv(hidden_size, output_size)

    def forward(self, data):
        x, edge_index, edge_attr = data.x, data.edge_index, data.edge_attr  # x = features des noeuds, edge_index = arêtes
        x = self.conv1(x, edge_index, edge_attr)
        x = F.relu(x)
        x = self.conv2(x, edge_index, edge_attr)
        return x

# Modèle combiné (MLP + GNN)
class CombinedModel(nn.Module):
    def __init__(self, mlp_input_size, mlp_hidden_size, gnn_input_size, gnn_hidden_size, combined_size):
        super(CombinedModel, self).__init__()
        self.mlp = MLP(mlp_input_size, mlp_hidden_size, combined_size)
        self.gnn = GNN(gnn_input_size, gnn_hidden_size, combined_size)
        self.fc_final = nn.Linear(combined_size * 2, 1)  # 1 pour classification binaire ou ajuster pour multiclasse

    def forward(self, data, user_features):
        mlp_out = self.mlp(user_features)
        gnn_out = self.gnn(data)
        combined = torch.cat((mlp_out, gnn_out), dim=-1)
        out = self.fc_final(combined)
        return out