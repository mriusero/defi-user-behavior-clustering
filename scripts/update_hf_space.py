import os
from huggingface_hub import login, upload_file

def update_dockerfile(docker_user, repo_name, date):
    dockerfile_content = f"""FROM docker.io/{docker_user}/{repo_name}:{date}
USER user
ENV PATH=$PATH:/home/user/.local/bin
WORKDIR /app
COPY --chown=user . /app/
EXPOSE 8501
CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
"""
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)


def commit_and_push_on_space(hf_user, hf_space_name, hf_token):
    try:
        login(token=hf_token)
        upload_file(
            path_or_fileobj="Dockerfile",
            path_in_repo="Dockerfile",
            repo_id=f"{hf_user}/{hf_space_name}"
        )
        print("Docker file updated successfully.")
    except Exception as e:
        print(f"Error during Dockerfile update: {e}")


if __name__ == "__main__":
    DOCKER_USER = os.getenv("DOCKER_USER", "default_user")
    REPO_NAME = os.getenv("REPO_NAME", "default_repo")
    DATE = os.getenv("DATE", "latest")
    HF_USER = os.getenv("HF_USER", "default_hf_user")
    HF_SPACE_NAME = os.getenv("HF_SPACE_NAME", "default_hf_space")
    HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")

    if not HF_API_TOKEN:
        print("HF token not defined !")
    else:
        update_dockerfile(DOCKER_USER, REPO_NAME, DATE)
        commit_and_push_on_space(HF_USER, HF_SPACE_NAME, HF_API_TOKEN)
