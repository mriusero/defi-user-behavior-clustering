import torch
import torch.optim as optim


def train_model(model, data, labels, epochs=100, lr=0.001, device='mps'):
    """
    Entraîne un modèle GNN + MLP en utilisant les données et les labels fournis.
    """
    model.to(device)            # Déplacer le modèle sur le dispositif (GPU ou CPU)
    data = data.to(device)      # Déplacer les données sur le même dispositif que le modèle

    optimizer = optim.Adam(model.parameters(), lr=lr)
    loss_fn = torch.nn.CrossEntropyLoss()

    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        out = model(data, data.x)  # Data contient data.x et data.edge_index, tu peux aussi passer data.edge_attr si nécessaire
        loss = loss_fn(out, labels.to(device))
        loss.backward()
        optimizer.step()

        if epoch % 10 == 0:
            print(f"Epoch {epoch}, Loss: {loss.item():.4f}")

    return model