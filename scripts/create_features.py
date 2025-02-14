import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ml.processing.features_engineering import implement_features
from ml.utils.hf_hub import upload_dataset


if __name__ == "__main__":
    implement_features()

    upload_dataset(
        dataset_path="data/features/features.arrow",
        hub_path="dataset/data/features.arrow",
    )
