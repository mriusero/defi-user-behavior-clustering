import os
import sys
import pyarrow as pa
import pyarrow.feather as feather

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ml.utils.splitting import splitting
from ml.kmeans.k_means import analyze_kmeans, train, save_model, load_model, predict
from ml.utils.hf_hub import upload_model

def kmeans_pipeline(analyse=False):
    """Pipeline de traitement ML"""
    print("\n ======= Running ML pipeline ======= \n")
    print("1. Splitting\n---------------------------------")
    dataset = splitting()

    if analyse:
        print("\n2. Analyse\n---------------------------------")
        x_train, y_train = dataset['train'][0], dataset['train'][1]
        best_k = analyze_kmeans(x_train, set='train')
        print(f"Optimal number of clusters (train): {best_k}")
        x_test, y_test = dataset['test'][0], dataset['test'][1]
        best_k_test = analyze_kmeans(x_test, set='test')
        print(f"Optimal number of clusters (test): {best_k_test}")
    else:
        best_k = 4

    x_all, y_all = dataset['all'][0], dataset['all'][1]

    print("\n3. Train\n---------------------------------")
    kmeans = train(best_k, x_all)
    print("Model trained successfully")

    model_path = "models/DeFI-Kmeans.pkl"

    print("\n4. Save model\n---------------------------------")
    save_model(kmeans, model_path)
    print(f"Model saved to {model_path}")

    print("\n5. Load Model\n---------------------------------")
    model = load_model(model_path)
    print(f"Model loaded successfully from {model_path}")

    print("\n6. Predict\n---------------------------------")
    predictions = predict(model, x_all, y_all)

    predictions_path = "data/results/kmeans_predictions.arrow"

    print("\n7. Save predictions\n---------------------------------")
    table = pa.Table.from_pandas(predictions)
    feather.write_feather(table, predictions_path)
    print(f'Data saved successfully to {predictions_path}\n')

    print("\n8. Upload model to HF\n---------------------------------")
    upload_model(
        model_path=model_path,
        hub_path="DeFI-Kmeans.pkl"
    )

    print("\n ======= Kmeans pipeline completed ======= \n")

if __name__ == "__main__":
    kmeans_pipeline(analyse=False)