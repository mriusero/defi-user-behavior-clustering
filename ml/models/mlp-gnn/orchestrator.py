import yaml
import torch
import mlflow
import mlflow.pytorch
from prefect import task, flow
from torchsummary import summary
from torch_geometric.data import Data
from ml.utils.splitting import splitting
from core.graph_builder import GraphBuilder
from core.embedder import MLXEmbedder
from core.model import CombinedModel
from training.train import train_model
from inference.inference import run_inference

with open("config/dl_config.yaml", "r") as f:
    CONFIG = yaml.safe_load(f)

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("DeFi_User_Classification")

@task
def load_data():
    """Charge et prétraite les données DeFi."""
    dataset = splitting()
    return dataset

@task
def build_graph(data):
    """Construit le graphe d'interaction utilisateur-protocole."""
    protocols = [
        'curve_dao_count', 'aave_count', 'uniswap_count',
        'maker_count', 'tether_count', 'yearn_finance_count',
        'usdc_count', 'dai_count', 'balancer_count',
        'harvest_finance_count', 'nftfi_count'
    ]
    graph = (
        GraphBuilder(data, address_col='address', protocol_cols=protocols)
        .build_graph()
    )
    print(f"Node features shape: {graph.x.shape}")
    print(f"Edge index shape: {graph.edge_index.shape}")
    print(f"Edge attributes shape: {graph.edge_attr.shape if graph.edge_attr is not None else 'None'}")

    return Data(x=graph.x, edge_index=graph.edge_index, edge_attr=graph.edge_attr)

@task
def compute_embeddings(data):
    """Calcule les embeddings MLX."""
    x_all = data['all'][0]
    embedder = MLXEmbedder(input_dim=x_all.shape[1], output_dim=32)
    embeddings = embedder.compute_embeddings(x_all)
    return torch.tensor(embeddings, dtype=torch.float)

@task
def train_model_task(graph, embeddings):
    """Entraîne un modèle GNN + MLP et enregistre les résultats avec MLflow."""
    with mlflow.start_run():
        model = CombinedModel(
            mlp_input_size=embeddings.shape[1],
            mlp_hidden_size=CONFIG["model"]["hidden_dim"],
            gnn_input_size=graph.x.shape[1],
            gnn_hidden_size=CONFIG["model"]["hidden_dim"],
            combined_size=CONFIG["model"]["hidden_dim"] * 2
        )
        summary(
            model,
            input_size=[
                (graph.num_nodes, graph.x.shape[1]),  # Nombre de nœuds et caractéristiques des nœuds pour le GNN
                (embeddings.shape[0], embeddings.shape[1])  # Batch size et taille des embeddings pour le MLP
            ]
        )
        summary(model.mlp, input_size=(embeddings.shape[1],))
        summary(model.gnn, input_size=(graph.x.shape[1],))

        trained_model = train_model(
            model, graph, embeddings.y,
            epochs=CONFIG["model"]["epochs"],
            lr=CONFIG["model"]["learning_rate"],
            device='mps' if CONFIG["gpu"]["use_mlx"] and torch.mps.is_available() else 'cpu'
        )
    return trained_model

@task
def inference_task(model, graph):
    """Exécute l'inférence avec le modèle entraîné."""
    return run_inference(model, graph)

@flow
def my_flow():
    data = load_data()
    graph = build_graph(data)
    embeddings = compute_embeddings(data)
    trained_model = train_model_task(graph, embeddings)
    predictions = inference_task(trained_model, graph)

if __name__ == "__main__":
    print(my_flow())

