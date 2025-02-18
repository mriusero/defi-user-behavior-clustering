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
    """)




