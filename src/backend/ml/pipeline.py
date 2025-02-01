

from src.backend.ml.helper.splitting import splitting
from src.backend.ml.modeling.k_means import train_k_means

def ml_pipeline():
    """Pipeline de traitement ML"""
    print("\n ======= Running ML pipeline ======= \n")
    print("1. Splitting\n---------------------------------")
    dataset = splitting()

    print("\n2. Train\n---------------------------------")
    x_train, y_train = dataset['train'][0], dataset['train'][1]
    train_k_means(x_train, y_train)
