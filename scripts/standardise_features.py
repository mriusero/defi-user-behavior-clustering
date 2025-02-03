import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ml.processing.distribution_analysis import standardisation_process
from ml.utils.hf_hub import upload_dataset

if __name__ == "__main__":

    standardisation_process()

    upload_dataset(
        dataset_path='data/features/features_standardised.arrow',
        hub_path='dataset/data/features_standardised.arrow'
    )