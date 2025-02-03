import os
import sys
from dotenv import load_dotenv
from huggingface_hub import login, upload_file

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ml.processing.distribution_analysis import standardisation_process

def commit_and_push_dataset(hf_user, hf_dataset_name, hf_token):
    """ Commit and push the dataset file to the Hugging Face Hub repository."""
    try:
        login(token=hf_token)
        upload_file(
            path_or_fileobj="data/features/features_standardised.arrow",
            path_in_repo="dataset/data/features_standardised.arrow",
            repo_id=f"{hf_user}/{hf_dataset_name}",
            repo_type="dataset"
        )
        print("Dataset file uploaded successfully.")
    except Exception as e:
        print(f"Error during dataset file uploading: {e}")


if __name__ == "__main__":

    standardisation_process()

    load_dotenv()
    HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")
    HF_USER = os.getenv("HF_USER", "")
    HF_DATASET_NAME = os.getenv("HF_DATASET_NAME", "")

    commit_and_push_dataset(HF_USER, HF_DATASET_NAME, HF_API_TOKEN)