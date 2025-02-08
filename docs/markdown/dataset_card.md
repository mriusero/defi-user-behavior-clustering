# DeFi Protocol Data on Ethereum 2023-2024

Decentralized finance (DeFi) has emerged as a significant sector within the blockchain and cryptocurrency space. DeFi protocols enable users to access financial services without traditional intermediaries, offering a wide range of applications such as lending, borrowing, trading, and yield farming. Understanding user behavior, protocol interactions, and market trends is crucial for analyzing the DeFi ecosystem's dynamics and identifying opportunities for innovation and growth.

---
# About Dataset
This dataset encompasses several steps involved in preparing data to analyze decentralized finance (DeFi) protocols and transactions. The process of building the dataset involves collecting data from various DeFi protocols, extracting relevant contract data, gathering transaction information, and aggregating market data. The final dataset, which contains 62 features, integrates data from four primary sources: `users.parquet`, `contracts.parquet`, `market.parquet`, and `transactions.parquet`. This combined dataset enables a comprehensive analysis of user behavior, protocol usage, transaction dynamics, and market performance within the Ethereum blockchain ecosystem.

Each of these four files serves a distinct purpose and is carefully structured to facilitate deeper insights into the DeFi landscape:

    ├── contracts.parquet         # Contains contract details for selected DeFi protocols.
    ├── transactions.parquet      # Contains transaction data for Ethereum-based contracts.
    ├── market.parquet            # Contains enriched market data with aggregated transaction metrics.
    └── users.parquet             # User profiles based on transaction data.

Together, these datasets are used to calculate 62 distinct features, which represent key aspects of user behavior, interaction with protocols, transaction volumes, market dynamics, and more.

---
#### Timeframe:
* Start: `2022-12-31T22:59:59.000Z`   
* End: `2024-12-30T23:00:11.000Z`

#### Splitting (random_state = 42)
- `train` : 0.7
- `test` : 0.15
- `validation` : 0.15

---
# Features
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
## Conclusion
This dataset preparation process establishes the foundation for analysis of user behavior, market trends, and protocol performance within the DeFi space. Each step builds upon the previous one, ensuring that the final dataset is rich and well-structured for deeper insights. It includes various technical steps for data extraction, user profiling, and market data aggregation, based on a combination of APIs and data sources.

---
## Source

Tools used in this process:  
1.	**CoinGecko API** - For contract data related to DeFi protocols and their market details.
2.	**Etherscan API** - For transaction data extraction on Ethereum smart contracts.
3.	**Yahoo Finance API** - For market data including OHLC values of tokens and trading volume.  
4. **MongoDB** - For managing and storing large volumes of transaction and protocol data in a structured format.  
5. **Ethereum Blockchain** - For the decentralized financial infrastructure that powers these protocols and transactions.

Code is available on [GitHub](https://github.com/mriusero/defi-user-behavior-clustering) and the ETL process is explained [here](https://github.com/mriusero/defi-user-behavior-clustering/blob/main/docs/etl_pipeline_flow.md).

---
## Subsets

### `users.parquet`
This file focuses on user-level data and is aimed at answering questions related to user behavior, activity trends, and protocol interactions. Potential use cases include:
- Analyzing the lifecycle of user activity in DeFi.
- Identifying power users or dormant users.
- Mapping the interaction between users and various protocols.
---
- **`address`** *(string)*: The wallet address of the user.
- **`first_seen`** *(datetime)*: The first recorded activity of the user.
- **`last_seen`** *(datetime)*: The most recent activity of the user.
- **`protocol_types`** *(list/string)*: Types of protocols the user interacted with.
- **`protocols_used`** *(list/string)*: Specific protocols the user interacted with.
- **`received_count`** *(integer)*: The total number of transactions received by the user.
- **`total_received (ETH)`** *(float)*: The total amount of ETH received by the user.
- **`sent_count`** *(integer)*: The total number of transactions sent by the user.
- **`total_sent (ETH)`** *(float)*: The total amount of ETH sent by the user.
- **`transactions`** *(integer)*: The total number of transactions the user participated in.

---

### `market.parquet`
This file aggregates market-related data over time intervals, offering insights into protocol performance and market dynamics. Objectives include:
- Understanding market trends across DeFi protocols and tokens.
- Analyzing trading volumes, transaction activity, and price fluctuations.
- Identifying periods of high or low activity for specific tokens or protocols.
---
- **`timestamp`** *(datetime)*: The time when the data was recorded.
- **`blockchain`** *(string)*: The blockchain network (e.g., Ethereum, Binance Smart Chain).
- **`protocol_name`** *(string)*: The name of the protocol associated with the data.
- **`symbol`** *(string)*: The symbol of the cryptocurrency or token.
- **`type`** *(string)*: The type of asset (e.g., token, NFT).
- **`contract_address`** *(string)*: The contract address associated with the asset.
- **`open (usd)`** *(float)*: The opening price in USD during the interval.
- **`high (usd)`** *(float)*: The highest price in USD during the interval.
- **`low (usd)`** *(float)*: The lowest price in USD during the interval.
- **`close (usd)`** *(float)*: The closing price in USD during the interval.
- **`volume`** *(float)*: The total trading volume during the interval.
- **`nb_tx_1h`**, **`nb_tx_24h`** *(integer)*: The number of transactions in the last 1 hour and 24 hours, respectively.
- **`total_value_eth_1h`**, **`total_value_eth_24h`** *(float)*: The total value transferred in ETH in the last 1 hour and 24 hours.
- **`total_gas_used_1h`**, **`total_gas_used_24h`** *(float)*: The total gas used in the last 1 hour and 24 hours.
- **`nb_unique_receivers_1h`**, **`nb_unique_receivers_24h`** *(integer)*: The number of unique receiving addresses in the last 1 hour and 24 hours.
- **`nb_unique_senders_1h`**, **`nb_unique_senders_24h`** *(integer)*: The number of unique sending addresses in the last 1 hour and 24 hours.
- **`std_value_eth_1h`**, **`std_value_eth_24h`** *(float)*: The standard deviation of transaction values in ETH in the last 1 hour and 24 hours.
- **`std_gas_used_1h`**, **`std_gas_used_24h`** *(float)*: The standard deviation of gas used in the last 1 hour and 24 hours.
- **`avg_gas_used_1h`**, **`avg_gas_used_24h`** *(float)*: The average gas used in the last 1 hour and 24 hours.
- **`avg_value_eth_per_tx_1h`**, **`avg_value_eth_per_tx_24h`** *(float)*: The average ETH value per transaction in the last 1 hour and 24 hours.
- **`max_gas_used_1h`**, **`max_gas_used_24h`** *(float)*: The maximum gas used in the last 1 hour and 24 hours.
- **`max_value_eth_1h`**, **`max_value_eth_24h`** *(float)*: The maximum ETH value transferred in the last 1 hour and 24 hours.
- **`median_value_eth_1h`**, **`median_value_eth_24h`** *(float)*: The median transaction value in ETH in the last 1 hour and 24 hours.
- **`min_gas_used_1h`**, **`min_gas_used_24h`** *(float)*: The minimum gas used in the last 1 hour and 24 hours.
- **`min_value_eth_1h`**, **`min_value_eth_24h`** *(float)*: The minimum ETH value transferred in the last 1 hour and 24 hours.
- **`num_errors_1h`**, **`num_errors_24h`** *(integer)*: The number of errors in the last 1 hour and 24 hours.
- **`error_rate_1h`**, **`error_rate_24h`** *(float)*: The rate of errors in the last 1 hour and 24 hours.

---

### `transactions.parquet`
This file provides granular transaction-level data, which is crucial for understanding the flow of assets within the DeFi ecosystem. Applications include:
- Tracing the movement of funds between addresses.
- Analyzing transaction costs (gas) and failure rates.
- Identifying anomalous or fraudulent transactions.
---
- **`timestamp`** *(datetime)*: The time when the transaction occurred.
- **`transaction_hash`** *(string)*: The unique hash identifying the transaction.
- **`from`** *(string)*: The sender's wallet address.
- **`to`** *(string)*: The receiver's wallet address.
- **`value (ETH)`** *(float)*: The value transferred in ETH.
- **`gas`** *(integer)*: The gas limit specified for the transaction.
- **`gas_used`** *(integer)*: The actual gas used by the transaction.
- **`is_error`** *(boolean)*: Indicates if the transaction resulted in an error.
- **`error_code`** *(string)*: The error code, if applicable.
- **`metadata`** *(json/object)*: Additional metadata related to the transaction.

---

### `contracts.parquet`
This file documents details about the smart contracts associated with various DeFi protocols. It supports:
- Categorizing contracts by protocol, type, and use case.
- Analyzing the adoption of specific contract standards (e.g., ERC-20, ERC-721).
- Exploring the relationship between contract attributes and protocol performance.
---
- **`contract_address`** *(string)*: The unique address of the smart contract.
- **`blockchain`** *(string)*: The blockchain network where the contract is deployed.
- **`type`** *(string)*: The type of contract (e.g., ERC-20, ERC-721).
- **`protocol_name`** *(string)*: The name of the protocol the contract belongs to.
- **`protocol_symbol`** *(string)*: The symbol of the protocol or token.
- **`description`** *(string)*: A description of the contract's purpose or functionality.
- **`website_url`** *(string)*: The URL of the contract or protocol's official website.