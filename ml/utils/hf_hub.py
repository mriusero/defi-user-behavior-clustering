import os
from dotenv import load_dotenv
from huggingface_hub import login, upload_file

load_dotenv()
HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")
HF_USER = os.getenv("HF_USER", "")
HF_DATASET_NAME = os.getenv("HF_DATASET_NAME", "")
HF_MODEL_NAME = os.getenv("HF_MODEL_NAME", "")


def upload_dataset(dataset_path, hub_path):
    """Commit and push a Dataset to the Hugging Face Hub repository."""
    try:
        login(token=HF_API_TOKEN)
        upload_file(
            path_or_fileobj=dataset_path,
            path_in_repo=hub_path,
            repo_id=f"{HF_USER}/{HF_DATASET_NAME}",
            repo_type="dataset",
        )
        print("Dataset uploaded successfully to the hub")
    except Exception as e:
        print(f"Error during dataset uploading: {e}")


def upload_model(model_path, hub_path):
    """Commit and push a Model to the Hugging Face Hub repository."""
    try:
        login(token=HF_API_TOKEN)
        upload_file(
            path_or_fileobj=model_path,
            path_in_repo=hub_path,
            repo_id=f"{HF_USER}/{HF_MODEL_NAME}",
            repo_type="model",
        )
        print("Model uploaded successfully to the the hub.")
    except Exception as e:
        print(f"Error during model uploading: {e}")
