import streamlit as st
import streamlit.components.v1 as components

COLOR_KEY = {
    "curve_dao_count": "#FF6347",
    "aave_count": "#4e000b",
    "uniswap_count": "#1e8b22",
    "maker_count": "#ffc909",
    "tether_count": "#DC143C",
    "yearn_finance_count": "#c24ee2",
    "usdc_count": "#00CED1",
    "dai_count": "#FFFFFF",
    "balancer_count": "#7FFF00",
    "harvest_finance_count": "#efef24",
    "nftfi_count": "#FF1493",
}

def page_0():
    st.markdown(
        '<div class="header">Introduction_</div>',
        unsafe_allow_html=True,
    )
    st.write("""
This project aims to analyze and cluster user behavior in decentralized finance (DeFi) platforms using open-source data. By examining user interactions, transaction patterns, and other relevant metrics, the goal is to uncover meaningful insights into how users engage with DeFi applications. These insights can help to improve platform designs, identify emerging trends, and provide valuable information for both developers and users within the DeFi ecosystem.

---
## Scope of Analysis_

The scope of this analysis encompasses various decentralized finance (DeFi) protocols and platforms.   
Specifically, the study focuses on the following types of DeFi protocols on the `Ethereum blockchain`:

- **Decentralized Exchanges (DEX)**: *`Uniswap`, `Curve DAO`, `Balancer`*
- **Lending Platforms**: *`Aave`, `Maker`*
- **Stablecoins**: *`Tether`, `USD Coin (USDC)`, `Dai`*
- **Yield Farming**: *`Yearn Finance`, `Harvest Finance`*
- **Non-Fungible Token (NFT)**: *`NFTfi`*

---
## Data Collection_
The data used in this analysis is sourced from the Ethereum blockchain and all the process is detailed in the section `Data Collection_`.  
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
All data are stored in Parquet format and are available in the [Hugging Face hub](https://huggingface.co/datasets/mriusero/DeFi-Protocol-Data-on-Ethereum-2023-2024/tree/main/dataset/data).

    ├── contracts.parquet         # Contains contract details for selected DeFi protocols.
    ├── transactions.parquet      # Contains transaction data for Ethereum-based contracts.
    ├── market.parquet            # Contains enriched market data with aggregated transaction metrics.
    └── users.parquet             # User profiles based on transaction data.

---

## Features Engineering_
The features generated for each user address are detailed in the section `Feature Engineering_`.  
Process include the following steps and allows to obtain a total of `62 features` for each user address: 
1. Loading & Processing Data *(from .parquet files)*
2. Aggregating User Metrics, Transactions Data, Market Data
3. Standardizing Features *(with a specific method described in step 6)*

##### Storage
The features files are also available in the [Hugging Face Hub](https://huggingface.co/datasets/mriusero/DeFi-Protocol-Data-on-Ethereum-2023-2024/tree/main/dataset/data).

    ├── features.arrow                   # Contains the 62 features generated for each user address.
    └── features_standardised.arrow      # Contains the 62 features standardized following the process detailed in step 6.

##### Raw features
    """)
    iframe_features = '''
    <iframe
      src="https://huggingface.co/datasets/mriusero/DeFi-Protocol-Data-on-Ethereum-2023-2024/embed/viewer/default/train"
      frameborder="0"
      width="100%"
      height="560px"
    ></iframe>
    '''
    components.html(iframe_features, height=600)
    st.write("""
---

## Network Analysis_
The network analysis provides an abstract vision of relationships between user addresses and DeFi protocols. By visualizing the connections between users and protocols, we can identify patterns in user behavior and protocol interactions.   

#### Protocols Network_
    
This graph represents the network of user addresses and the protocols they interact with.  
Each node represents a user address and each edge represents a transaction between a user and a protocol.  

> **Note:** This graph contains only 100 000 users against 6 876 845 in the real dataset.  
> Image available [here](https://github.com/mriusero/defi-user-behavior-clustering/blob/main/docs/graphics/network/address_protocol_nx_plot.png).

        """)
    col1, col2 = st.columns([1, 5])
    with col1:
        st.write("""
        """)
        st.write("**Legend:**")
        for protocol, color in COLOR_KEY.items():
            st.markdown(f"<span style='color: {color};'>■</span> {protocol.replace('_', ' ').title()}",
                        unsafe_allow_html=True)
    with col2:
        st.image("src/frontend/layouts/pictures/address_protocol_nx_plot.png", caption="")

    st.write("""
## Clustering_
By identifying distinct clusters, we can gain insights into different user profiles and behaviors within the DeFi ecosystem.
To perform the clustering analysis, K-means algorithm is used to group users into clusters based on their features and transactional activities.
    """)
    col1, col2 = st.columns(2)
    with col1:
        st.write("""
#### PCA Analysis_
The PCA reduction allow to determine the number of dimensions required to keep a certain rate of variance. Here, 6 sigmas of the variance is explained by 28 dimensions against 62 initially.")
        """)
        st.image("docs/graphics/pca/pca_variance.png", caption="", width=500)
    with col2:
        st.write("""
#### Elbow Method_
The Elbow Method is used to identify visually the optimal number of clusters for the K-means algorithm. The inertia value is plotted against the number of clusters, and the "elbow" point indicates the optimal number of clusters to use. Here the optimal number of clusters can be determined visually as 4.
        """)
        st.image("docs/graphics/kmeans/kmeans_test_scores.png", caption="", width=600)
    st.write("""
#### Hyperparameters Optimization_
Thanks to Optuna, an hyperparameter optimization framework, best parameters for the K-means algorithm can be empirically identified.
The goal is to find the best set of hyperparameters that maximize the clustering performance based on a combined score of multiple metrics. 

```python
# Objective function
n_clusters = trial.suggest_int("n_clusters", 2, 10)                 # Suggest an integer between 2 and 10 for the number of clusters
init = trial.suggest_categorical("init", ["k-means++", "random"])   # Suggest a categorical value for the initialization method: either "k-means++" or "random"
batch_size = trial.suggest_int("batch_size", 50, 500, step=50)      # Suggest an integer between 50 and 500 (in steps of 50) for the batch size
max_iter = trial.suggest_int("max_iter", 100, 500)                  # Suggest an integer between 100 and 500 for the maximum number of iterations
tol = trial.suggest_float("tol", 1e-6, 1e-2, log=True)              # Suggest a floating-point number between 1e-6 and 1e-2 for the convergence tolerance, using a log scale

# Weighting
x = trial.suggest_float("silhouette_weight", 0.1, 1.0)
y = trial.suggest_float("ch_weight", 0.1, 1.0)
z = trial.suggest_float("db_weight", 0.1, 1.0)

# Combined score maximisation based on silhouette score, Calinski-Harabasz index, and Davies-Bouldin index
combined_score = (x * silhouette_avg) + (y * ch_index) - (z * db_index)
```
#### Performances obtained_
```python
{
    "Davies-Bouldin Index": 0.3619108287721344      # Measures the average similarity ratio of each cluster with the cluster most similar to it. Lower values indicate better clustering.
    "Calinski-Harabasz Index": 20025853.87041033    # Also known as the Variance Ratio Criterion, evaluates the ratio of between-cluster dispersion to within-cluster dispersion. Higher values indicate better-defined clusters.
    "Silhouette Avg": 0.7608796914931638            # Measures how similar a data point is to its own cluster compared to other clusters. The score ranges from -1 to 1, with higher values indicating better clustering.
}
```

#### Results_
The analysis of main differences between each clusters is available in the section `Clustering_`. The clusters are described with their characteristics, interactions types, correlation matrix, transactions activity, diversity and influence, sent and received transactions statistics, exposure metrics and timing behavior.

---
    """)


    st.write("""
## Recommandations_

---
    """)



