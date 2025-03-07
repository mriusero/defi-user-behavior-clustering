# DeFi Protocol Data on Ethereum
Following the data collection, below is a detailed, step-by-step explanation of the features created and the processes involved.  
This pipeline enriches the users data with a variety of derived metrics, providing a comprehensive view of user behavior and market interactions.

## Table of Contents

1. [Loading & Processing Data](#1-loading--processing-data)
2. [Aggregating User Metrics](#2-aggregating-user-metrics)
3. [Aggregating Transactions Data](#3-aggregating-transactions-data)
4. [Aggregating Market Data](#4-aggregating-market-data)
5. [Features Obtained](#5-features-obtained)
6. [Standardization of Features](#6-standardization-of-features)
7. [Storage](#7-storage)

---
## 1. Loading & Processing Data

First, features are based on previously data collected:
- **Users Data** *from* `users.parquet`.
- **Transactions Data** *from* `transactions.parquet`.
- **Market Data** *from* `market.parquet`.

Secondly, data are processed as follows:
- **Names Normalization**: Column names are normalized to snake_case.
- **Removal of Special Characters**: Spaces, dashes, underscores, dots, slashes, and parentheses are replaced or removed.

---

## 2. Aggregating User Metrics
Existing users profiles data allows to create some interesting others features:

- **Protocol Diversity**:
  - `protocol_type_diversity`: *count of unique protocol types used by each user.*
  - `protocol_name_diversity`: *count of unique protocol names used by each user.*
- **Ethereum Flow**:
  - `net_flow_eth`: *net Ethereum flow calculated as the difference between total received and total sent Ethereum.*
- **Whale Score**:
  - `whale_score`: *aggregated score based on normalized Ethereum flow metrics sum: `net_flow_eth`, `total_received_eth`, `total_sent_eth`.*

---

## 3. Aggregating Transactions Data
By processing transactional data, we can enrich users profiles based on the Ethereum addresses involved in transactions.

1. **Fetching Transactions**: *retrieve all transactions associated with each user.*

2. **Calculating Metrics** *(for each user)*:
   - **Gas Efficiency**: *calculate the ratio of Ethereum value to gas used.*
   - **Transaction Statistics**: *compute the min, mean, median, max, and std for both Ethereum value and gas used, separately for sent and received transactions.*
   - **Peak Activity**: *identify the peak hour for transactions and count the number of transactions during that hour.*
   - **Transaction Frequency**: *determine how often transactions occur.*

3. **Merging Data**: *integrate the calculated transaction metrics with User Profile Data.*

---
## 4. Aggregating Market Data
By processing market data, we can evaluate the user's risk and influence based on his market metrics exposure.

1. **Calculating Protocol Statistics**:
    - Calculates mean and standard deviation for various market metrics (volume, close price, gas used, etc.) for a given protocol.
2. **Calculating Exposure Metrics**:
  - Computes exposure metrics for each user based on their interaction with protocols:  
  `volume exposure`, `volatility exposure`, `gas exposure`, `error exposure`, `liquidity exposure`, `activity exposure`,  
   `user adoption exposure`, `gas volatility exposure`, `error volatility exposure`, `high-value exposure`.

3. **Merging Data**: *integrate the calculated market exposure metrics with User Profile Data.*

---
## 5. Features obtained
This pipeline generates a variety of features that provide insights into user behavior, transaction patterns, and market interactions.

#### 1. General Information
- `address`: Unique address of the user on the blockchain.

#### 2. Transaction Activity
- `received_count`: Total number of transactions received.
- `total_received_eth`: Total amount of ETH received.
- `sent_count`: Total number of transactions sent.
- `total_sent_eth`: Total amount of ETH sent.

#### 3. Types of Interaction with Protocols
- `type_dex`: Indicates whether the user interacts with DEXs (Decentralized Exchanges).
- `type_lending`: Indicates whether the user interacts with lending protocols.
- `type_stablecoin`: Indicates whether the user interacts with stablecoins.
- `type_yield_farming`: Indicates whether the user participates in yield farming.
- `type_nft_fi`: Indicates whether the user interacts with NFT-Fi protocols.

#### 4. Engagement with Specific Protocols
(Number of transactions made on each protocol)
- `curve_dao_count`
- `aave_count`
- `tether_count`
- `uniswap_count`
- `maker_count`
- `yearn_finance_count`
- `usdc_count`
- `dai_count`
- `balancer_count`
- `harvest_finance_count`
- `nftfi_count`

#### 5. User Diversity and Influence
- `protocol_type_diversity`: Number of different protocol types used by the user.
- `protocol_name_diversity`: Number of unique protocols used by the user.
- `net_flow_eth`: Difference between ETH sent and ETH received.
- `whale_score`: A score indicating whether the user is a large fund holder.

#### 6. Sent Transaction Statistics
(Minimum, average, median, maximum values, and standard deviations)
- `min_sent_eth`, `avg_sent_eth`, `med_sent_eth`, `max_sent_eth`, `std_sent_eth`: Statistics on amounts sent in ETH.
- `min_sent_gas`, `avg_sent_gas`, `med_sent_gas`, `max_sent_gas`, `std_sent_gas`: Statistics on gas used for sent transactions.
- `avg_gas_efficiency_sent`: Average gas efficiency for sent transactions.
- `peak_hour_sent`: Time of day when the user sends the most transactions.
- `peak_count_sent`: Maximum number of transactions sent during a given hour.
- `tx_frequency_sent`: Average frequency of sent transactions.

#### 7. Received Transaction Statistics
(Same structure as for sent transactions)
- `min_received_eth`, `avg_received_eth`, `med_received_eth`, `max_received_eth`, `std_received_eth`: Statistics on amounts received in ETH.
- `min_received_gas`, `avg_received_gas`, `med_received_gas`, `max_received_gas`, `std_received_gas`: Statistics on gas used for received transactions.
- `avg_gas_efficiency_received`: Average gas efficiency for received transactions.
- `peak_hour_received`: Time of day when the user receives the most transactions.
- `peak_count_received`: Maximum number of transactions received during a given hour.
- `tx_frequency_received`: Average frequency of received transactions.

#### 8. Exposure to Market Protocols
(Evaluation of the user's risk and influence based on the market)
- `total_volume_exposure`: Total exposure to the transaction volume of protocols.
- `total_volatility_exposure`: Exposure to price volatility of protocols.
- `total_gas_exposure`: Exposure to the average gas costs on used protocols.
- `total_error_exposure`: Exposure to transaction errors of protocols.
- `total_liquidity_exposure`: Exposure to protocol liquidity.
- `total_activity_exposure`: Exposure to global transaction activity of protocols.
- `total_user_adoption_exposure`: Exposure to the number of active users on protocols.
- `total_gas_volatility_exposure`: Exposure to gas volatility used on protocols.
- `total_error_volatility_exposure`: Exposure to the variability of transaction errors.
- `total_high_value_exposure`: Exposure to high-value transactions on protocols.

---
## 6. Standardization of Features

The standardization of features is a crucial step in data preprocessing, ensuring that each feature contributes equally to the analysis or modeling process.  
The script employs several standardization methods based on the statistical properties of the data:
#### Execution

1. **Analyze Data**: Computes statistical properties with `scipy.stats` and determines standardization methods.
    - Normality p_value calculation with `normaltest`
    - Distribution shape calculation with `skewness` and `kurtosis` metrics.  
    
2. **Standardize Data**: Applies the chosen standardization methods to the data.
    - **Z-score**: *used for normally distributed data* `(p_value) > 0.05`.
    - **Min-Max**: *applied to data with low skewness `(skew_val) < 0.5` or low kurtosis*  `(kurt_val) < 2.5`.
    - **Log Transformation**: *used for data with high positive skewness `(skew_val) > 1`.*
    - **Log Inverse Transformation**: *applied to data with high negative skewness `(skew_val) < -1`.*
    - **Box-Cox Transformation**: *used for data with high kurtosis `(kurt_val) > 3.5` or when other methods are not applicable.*

---
## 7. Storage
The features files are also available in the [Hugging Face Hub](https://huggingface.co/datasets/mriusero/DeFi-Protocol-Data-on-Ethereum-2023-2024/tree/main/dataset/data).

    ├── features.arrow                   # Contains the 62 features generated for each user address.
    └── features_standardised.arrow      # Contains the 62 features standardized following the process detailed in step 6.
