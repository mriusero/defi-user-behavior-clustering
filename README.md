# DeFi Users Behavior Clustering

---
## Project Description
This project aims to analyze and cluster user behavior in decentralized finance (DeFi) platforms using open-source data. By examining user interactions, transaction patterns, and other relevant metrics, the goal is to uncover meaningful insights into how users engage with DeFi applications. These insights can help to improve platform designs, identify emerging trends, and provide valuable information for both developers and users within the DeFi ecosystem.

---
## Step 1 : Data Collection
The first step in this project is to collect data from various DeFi protocols. This includes transaction data, user interactions, smart contract events, and other relevant information. By aggregating this data, we can create a comprehensive dataset that captures user behavior across different DeFi applications.

See documentation for more details: [DeFi Protocol Data on Ethereum (doc)](docs/etl_pipeline_flow.md)  

Dataset available on :
* Kaggle: [DeFi Protocol Data on Ethereum 2023-2024](https://www.kaggle.com/datasets/mariusayrault/defi-protocol-data-on-ethereum-2yr-23-to-24)
* Hugging Face: [DeFi Protocol Data on Ethereum 2023-2024](https://huggingface.co/datasets/mriusero/DeFi-Protocol-Data-on-Ethereum-2023-2024)

To trigger pipeline:
```bash
uv run src/back-end/etl/main.py
```

---
## Step 2 : Data Preprocessing


 ```bash
 streamlit run src/front-end/app.py
 ```
> CI test


> Work in progress