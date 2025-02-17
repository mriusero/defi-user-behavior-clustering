# DeFi Users Behavior Clustering

This project aims to analyze and cluster user behavior in decentralized finance (DeFi) platforms using open-source data. By examining user interactions, transaction patterns, and other relevant metrics, the goal is to uncover meaningful insights into how users engage with DeFi applications. These insights can help to improve platform designs, identify emerging trends, and provide valuable information for both developers and users within the DeFi ecosystem.

[![HuggingFace](https://img.shields.io/badge/%20COLLECTION-FFD700?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/collections/mriusero/defi-behavior-analysis-67a0d6d132ccecdff8068369)
[![HuggingFace](https://img.shields.io/badge/DATASET-FFD700?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/datasets/mriusero/DeFi-Protocol-Data-on-Ethereum-2023-2024)
[![HuggingFace](https://img.shields.io/badge/SPACE-FFD700?style=for-the-badge&logo=huggingface&logoColor=black)](https://mriusero-defi-behavior.hf.space)
[![HuggingFace](https://img.shields.io/badge/MODELS-FFD700?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/mriusero/DeFI-Behavior-Models)

---
## Scope of Analysis_

The scope of this analysis encompasses various decentralized finance (DeFi) protocols and platforms.   
Specifically, the study focuses on the following types of DeFi protocols on the `Ethereum blockchain`:

- **Decentralized Exchanges (DEX)**: *`Uniswap`, `Curve DAO`, `Balancer`*
- **Lending Platforms**: *`Aave`, `Maker`*
- **Stablecoins**: *`Tether`, `USD Coin (USDC)`, `Dai`*
- **Yield Farming**: *`Yearn Finance`, `Harvest Finance`*
- **Non-Fungible Token (NFT)**: *`NFTfi`*

![Logo](docs/graphics/network/protocols_network_with_legend.png)

---
## Data Collection_
The data used in this analysis is sourced from the Ethereum blockchain and all the process is detailed in the section `Data Collection_` of the [HF Space](https://mriusero-defi-behavior.hf.space).  
Process include information on protocols, user transactions and average usages, protocol interactions or market metrics.

##### Timeframe *(2 years: 2023-2024)*
* Start  -  `31th of December 2022, 22:59:59 UTC`
* End  -  `30th of December 2024, 23:00:11 UTC`

##### Metrics
- Total protocols (see scope above): `11` 
- Total unique transactions : `22 682 739` 
- Total unique users/addresses : `6 876 845` 
- Total market hours covered : `177 955`

##### Storage
All data are stored in Parquet format and are available in the [HF Dataset](https://huggingface.co/datasets/mriusero/DeFi-Protocol-Data-on-Ethereum-2023-2024/tree/main/dataset/data).  

    ├── contracts.parquet         # Contains contract details for selected DeFi protocols.
    ├── transactions.parquet      # Contains transaction data for Ethereum-based contracts.
    ├── market.parquet            # Contains enriched market data with aggregated transaction metrics.
    └── users.parquet             # User profiles based on transaction data.

---
## Features Engineering_
The features generated for each user address are detailed in the section `Feature Engineering_` of the [HF Space](https://mriusero-defi-behavior.hf.space).  
Process include the following steps and allows to obtain a total of `62 features` for each user address: 
1. Loading & Processing Data *(from .parquet files)*
2. Aggregating User Metrics, Transactions Data, Market Data
3. Standardizing Features *(with a specific method described in step 6)*

##### Storage
The features files are saved in arrow format and are also available in the [HF Dataset](https://huggingface.co/datasets/mriusero/DeFi-Protocol-Data-on-Ethereum-2023-2024/tree/main/dataset/data).

    ├── features.arrow                   # Contains the 62 features generated for each user address.
    └── features_standardised.arrow      # Contains the 62 features standardized following the process detailed in step 6.

---
## Clustering Analysis_

> Work in progress...

---
# Run the app locally
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
   git clone https://github.com/mriusero/defi-user-behavior-clustering    # Clone the repository
   cd defi-user-behavior-clustering                                       # Access the project directory
   ```
   
2. **Create Virtual Environment:**
   ```bash
   python -m venv .venv         # Create a virtual environment
   source .venv/bin/activate    # Activate the virtual environment
   ```

3. **Install Dependencies:**
   ```bash
   pip install uv               # Install uv for dependency management
   uv sync                      # Install dependencies with uv
   ```
    This will install dependencies listed in `pyproject.toml`.
---

## Run the app
You can run the application locally or inside a Docker container.

### Running Locally
To run the application locally, execute the following command:

```bash
 uv run streamlit run app.py
```
This will start the application, and you can access it in your web browser at [http://localhost:8501](http://localhost:8501).

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
## License
This project is licensed under the terms of the [MIT License](LICENSE).