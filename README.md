# DeFi Users Behavior Clustering

## Project Description
This project aims to analyze and cluster user behavior in decentralized finance (DeFi) platforms using open-source data. By examining user interactions, transaction patterns, and other relevant metrics, the goal is to uncover meaningful insights into how users engage with DeFi applications. These insights can help to improve platform designs, identify emerging trends, and provide valuable information for both developers and users within the DeFi ecosystem.

---

## Prerequisites
Before you begin, ensure you have the following software installed on your system:
- **Python 3.11+**: This project uses Python, so you'll need to have Python installed. You can download it from [python.org](https://www.python.org/).
- **uv**: This project uses `uv` for dependency management. Install it by following the instructions at [docs.astral.sh/uv](https://docs.astral.sh/uv/).
- **Docker** (Optional): If you prefer to run the project in a Docker container, ensure Docker is installed. Instructions can be found at [docker.com](https://www.docker.com/).

---
## Installation
Follow these steps to install and set up the project:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/mriusero/defi-user-behavior-clustering
   cd defi-user-behavior-clustering
   ```
   
2. **Install Dependencies:**
   ```bash
   pip install --upgrade pip    # Ensure pip is up-to-date
   python -m venv .venv         # Create a virtual environment
   source .venv/bin/activate    # Activate the virtual environment
   uv sync                      # Install dependencies with uv
   ```
    This will create a virtual environment and install all dependencies listed in `pyproject.toml`.


3. **Activate the Virtual Environment:**
   If uv does not automatically activate the virtual environment, you can activate it manually:
   ```bash
   source .venv/bin/activate
   ```
---
## Usage
You can run the application locally or inside a Docker container.

### Running Locally
To run the application locally, execute the following command:

```bash
 uv run streamlit run app.py
```

### Running with Docker
1. **Build the Docker Image:**
   ```bash
   docker build -t streamlit .
   ```
2. **Run the Docker Container:**
   ```bash
   docker run -p 8501:8501 streamlit
   ```
This will start the application, and you can access it in your web browser at [http://localhost:8501](http://localhost:8501).

---
## Step 1 : Data Collection
The first step in this project is to collect data from various DeFi protocols. This includes transaction data, user interactions, smart contract events, and other relevant information. By aggregating this data, we can create a comprehensive dataset that captures user behavior across different DeFi applications.

See documentation for more details: [DeFi Protocol Data on Ethereum (doc)](docs/etl_pipeline_flow.md)  

Dataset available on :
* Kaggle: [DeFi Protocol Data on Ethereum 2023-2024](https://www.kaggle.com/datasets/mariusayrault/defi-protocol-data-on-ethereum-2yr-23-to-24)
* Hugging Face: [DeFi Protocol Data on Ethereum 2023-2024](https://huggingface.co/datasets/mriusero/DeFi-Protocol-Data-on-Ethereum-2023-2024)

To trigger pipeline:
```bash
uv run etl/main.py
```
---
## Step 2 : Data Preprocessing

> Work in progress

---
## License
This project is licensed under the terms of the [MIT License](LICENSE).