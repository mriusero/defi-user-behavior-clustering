# DeFi Protocol Data on Ethereum
This section outlines the steps involved in preparing the dataset for analyzing decentralized finance (DeFi) protocols and transactions. The process includes selecting DeFi protocols, extracting relevant contract data, collecting transaction information, and analyzing market trends. 
The dataset enables a comprehensive analysis of user behavior, protocol usage, transaction dynamics, and market performance on ethereum blockchain.

## Dataset
```
    ├── protocols.parquet         # Contains protocols details for selected DeFi protocols.
    ├── contracts.parquet         # Contains contract details for selected DeFi protocols.
    ├── transactions.parquet      # Contains transaction data for Ethereum-based contracts.
    ├── market.parquet            # Contains enriched market data with aggregated transaction metrics.
    └── users.parquet             # User profiles based on transaction data.
```
---
## Table of Contents
1. [Selection of DeFi Protocols](#1-selection-of-defi-protocols)
2. [Collection of Contract Data for Selected DeFi Protocols *(CoinGecko API)*](#2-collection-of-contract-data-for-selected-defi-protocols-coingecko-api)
3. [Collection of Transactions for Ethereum-Based Contracts *(Etherscan API)*](#3-collection-of-transactions-for-ethereum-based-contracts-etherscan-api)
4. [Generation of User Profiles Based on Transaction Data](#4-generation-of-user-profiles-based-on-transaction-data)
5. [Collection of Market OHLC Data for Tokens *(YahooFinance API)*](#5-collection-of-market-ohlc-data-for-tokens-yahoofinance-api)
6. [Enrichment of Market Data via Transaction Aggregation](#6-enrichment-of-market-data-via-transaction-aggregation)
---
## 1. Selection of DeFi Protocols
In this first step, we select multiple DeFi protocols that represent different categories of financial services in the decentralized ecosystem. This includes protocols for decentralized exchanges (DEX), lending platforms, stablecoins, and NFT-based finance.
 
### Protocols type: `('DEX': 3, 'Lending': 2, 'Yield Farming': 2, 'Stablecoin': 3, 'NFT-Fi': 1)` 

```python
KEY_PROTOCOLS = [
      "uniswap",                  # DEX
      "curve-dao-token",          # DEX
      "balancer",                 # DEX
      "aave",                     # Lending
      "maker",                    # Lending
      "yearn-finance",            # Yield Farming
      "harvest-finance",          # Yield Farming
      "dai",                      # Stablecoin
      "usd-coin",                 # Stablecoin
      "tether",                   # Stablecoin
      "nftfi",                    # NFT-Fi (optionnel)
  ]
```
### Objective
To define a set of popular and diverse DeFi protocols that will serve as the basis for data collection and analysis.

---
## 2. Collection of Contract Data for Selected DeFi Protocols *(CoinGecko API)*
### Collection name: `protocols` - *(11 documents)*
For each selected protocol, we extract contract information from *CoinGecko’s API*. This data contains the contract addresses on the blockchain, the type of protocol, and additional details like market capitalization rank and protocol description.

### Fields
#### 1. `_id` *(ObjectId)* - The unique identifier for this document in the database.
#### 2. `protocol_id` *(String)* - A unique identifier for the protocol (in this case, for Uniswap).
#### 3. `blockchain_contracts` *(Array of Objects)* - Contains a list of blockchain contracts associated with the asset.
- `blockchain` *(String)* - The name of the blockchain.
- `contract` *(String)* - The address of the protocol contract on the blockchain.
#### 4. `description` *(String)* - A brief description of the protocol.
#### 5. `market_cap_rank` *(Integer)* - The rank of the protocol based on market capitalization.
#### 6. `name` *(String)* - The name of the protocol.
#### 7. `symbol` *(String)* - The symbol of the protocol.
#### 8. `type` *(String)* - The type of protocol (e.g., DEX, Lending).
#### 9. `website_url` *(String)* - The URL of the protocol's official website.

### Exemple 
```json
{
  "_id": {
    "$oid": "678a6dbb7824a40cf5948a3a"
  },
  "protocol_id": "a32977262a1f49ca460aa0f158e86b03",
  "blockchain_contracts": [
    {
      "blockchain": "ethereum",
      "contract": "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984"
    }
  ],
  "description": "UNI is the governance token for Uniswap, an Automated Market Marker DEX on the Ethereum blockchain. The UNI token allows token holders to participate in the governance of the protocol. Key decisions such as usage of the treasury or future upgrades ca",
  "market_cap_rank": 26,
  "name": "Uniswap",
  "symbol": "uni",
  "type": "DEX",
  "website_url": "https://uniswap.org/"
}
```
### Objective
To retrieve the smart contract details associated with each protocol, enabling further analysis of transactions and interactions with the protocol on the blockchain.

---
## 3. Collection of Transactions for Ethereum-Based Contracts *(Etherscan API)*
### Collection name: `transactions` - *(22 682 739 documents)*
We use an API such as Etherscan to gather transaction data related to the selected Ethereum-based contracts. The data includes transaction hashes, sender and receiver addresses, gas usage, and transaction values.

#### Timeframe:
* Start: `2022-12-31T22:59:59.000Z`   
* End: `2024-12-30T23:00:11.000Z`

### Fields
#### 1. `_id` *(ObjectId)* - The unique identifier for this document in the database.
#### 2. `transaction_hash` *(String)* - The hash of the transaction.
#### 3. `error_code` *(String)* - The error code for the transaction, if any.
#### 4. `from` *(String)* - The address of the sender.
#### 5. `gas` *(Integer)* - The amount of gas proposed for the transaction.
#### 6. `gas_used` *(Integer)* - The amount of gas actually used in the transaction.
#### 7. `is_error` *(String)* - Indicates if there was an error during the transaction ("0" for no error, "1" for error).
#### 8. `metadata` *(Object)* - Contains additional details about the protocol.
- `protocol_name` *(String)* - The name of the protocol associated with the transaction.
- `type` *(String)* - The type of the protocol (e.g., DEX, Lending).
- `blockchain` *(String)* - The name of the blockchain (in this case, Ethereum).
- `contract_id` *(String)* - The unique identifier of the contract involved in the transaction.
#### 9. `timestamp` *(Date)* - The timestamp when the transaction occurred.
#### 10. `to` *(String)* - The address of the recipient.
#### 11. `trace_id` *(String)* - The trace identifier for tracking the transaction.
#### 12. `tx_hash` *(String)* - A duplicate of the `transaction_hash` field.
#### 13. `value (ETH)` *(Float)* - The amount of ETH transferred in the transaction.

### Example
```json
{
  "_id": {
    "$oid": "678bf7cf9ebf7cf7c1a3a88e"
  },
  "transaction_hash": "0x50edd2873907a3454a9c8cc8d242b6d0e365ec71263e4fb8cb9e935e151fcbaa",
  "error_code": "",
  "from": "0xbe6e45661c633fd1a1825389dec680e62c1c7d51",
  "gas": 57218,
  "gas_used": 52418,
  "is_error": "0",
  "metadata": {
    "protocol_name": "Uniswap",
    "type": "DEX",
    "blockchain": "ethereum",
    "contract_id": "c944b5855a3b2d8cbe4367a3f7561854"
  },
  "timestamp": {
    "$date": "2023-12-31T23:00:23.000Z"
  },
  "to": "0x0231b537b8f1c46b6cb4f7d9ec6d56951a66ff41",
  "trace_id": "",
  "tx_hash": "0x50edd2873907a3454a9c8cc8d242b6d0e365ec71263e4fb8cb9e935e151fcbaa",
  "value (ETH)": 12.201526377331376
}
```
### Objective
To collect transaction data associated with the Ethereum smart contracts, allowing for an analysis of activity, user behavior, and protocol usage over time.

---
## 4. Generation of User Profiles Based on Transaction Data
### Collection name: `users` - *(6 876 845 documents)*
By analyzing transaction data, we identify and create user profiles based on the Ethereum addresses involved in transactions. This step allows for tracking users’ activities across different protocols and their total received and sent amounts.

### Fields
#### 1. `_id` *(ObjectId)* - The unique identifier for this document in the database.
#### 2. `address` *(String)* - The Ethereum address of the user.
#### 3. `first_seen` *(Date)* - The timestamp when the address was first observed in the dataset.
#### 4. `last_seen` *(Date)* - The timestamp when the address was last observed in the dataset.
#### 5. `protocol_types` *(Object)* - A count of the types of protocols the user has interacted with, grouped by protocol type (e.g., DEX, Lending).
#### 6. `protocols_used` *(Object)* - A breakdown of protocols the user interacted with, containing:
- **Protocol name** *(String)* - The name of the protocol (e.g., Curve DAO, Aave).
  - `count` *(Integer)* - The number of interactions with the protocol.
  - `blockchain` *(String)* - The blockchain on which the protocol operates.
  - `contract_id` *(String)* - The unique identifier of the protocol's contract.
#### 7. `received_count` *(Integer)* - The number of transactions in which the user received assets.
#### 8. `sent_count` *(Integer)* - The number of transactions in which the user sent assets.
#### 9. `total_received (ETH)` *(Float)* - The total amount of ETH received by the user.
#### 10. `total_sent (ETH)` *(Float)* - The total amount of ETH sent by the user.
#### 11. `transactions` *(Array of Objects)* - Details of individual transactions involving the user.
- `transaction_hash` *(String)* - The hash of the transaction.
- `timestamp` *(Date)* - The timestamp of the transaction.
- `value (ETH)` *(Float)* - The amount of ETH transferred in the transaction.
- `is_sender` *(Boolean)* - Indicates whether the user was the sender in the transaction.
- `gas_used` *(Integer)* - The amount of gas used in the transaction.
- `protocol_name` *(String)* - The name of the protocol associated with the transaction.
- `protocol_type` *(String)* - The type of protocol (e.g., DEX, Lending).
- `blockchain` *(String)* - The name of the blockchain (e.g., Ethereum).
- `contract_id` *(String)* - The unique identifier of the protocol's contract involved in the transaction.

### Example
```json
{
  "_id": {
    "$oid": "678cf88798ededf702ec1766"
  },
  "address": "0x2deacac3a34ace696d3fe214a07882949311e81b",
  "first_seen": {
    "$date": "2023-01-07T22:05:35.000Z"
  },
  "last_seen": {
    "$date": "2023-01-21T12:46:35.000Z"
  },
  "protocol_types": {
    "DEX": 1,
    "Lending": 1
  },
  "protocols_used": {
    "Curve DAO": {
      "count": 1,
      "blockchain": "ethereum",
      "contract_id": "6c78ebb89739952c2d1b03a051f79287"
    },
    "Aave": {
      "count": 1,
      "blockchain": "ethereum",
      "contract_id": "e82fc843c812403d08dca5ab89b772d5"
    }
  },
  "received_count": 2,
  "sent_count": 0,
  "total_received (ETH)": 23.00372511606387,
  "total_sent (ETH)": 0,
  "transactions": [
    {
      "transaction_hash": "0x7de2510bd9efdb0fcbb358aac92473361026ad6cc8a49cbfcef5d88856eb1fe5",
      "timestamp": {
        "$date": "2023-01-07T22:05:35.000Z"
      },
      "value (ETH)": 23,
      "is_sender": false,
      "gas_used": 34225,
      "protocol_name": "Curve DAO",
      "protocol_type": "DEX",
      "blockchain": "ethereum",
      "contract_id": "6c78ebb89739952c2d1b03a051f79287"
    },
    {
      "transaction_hash": "0xb355bdf9cf819810d09ed6041358d3dd4bfc45b0a55ea9555b5e8360f68c3a98",
      "timestamp": {
        "$date": "2023-01-21T12:46:35.000Z"
      },
      "value (ETH)": 0.003725116063867235,
      "is_sender": false,
      "gas_used": 237828,
      "protocol_name": "Aave",
      "protocol_type": "Lending",
      "blockchain": "ethereum",
      "contract_id": "e82fc843c812403d08dca5ab89b772d5"
    }
  ]
}
```
### Objective
To track user behavior across different DeFi protocols, focusing on received and sent transaction counts and totals. This will help in understanding user engagement with various protocols.

---
## 5. Collection of Market OHLC Data for Tokens *(YahooFinance API)*
### Collection name: `market` - *(177 955 documents)*
We then enrich the transaction data by extracting market data for the associated tokens using sources like YahooFinance API. This includes Open, High, Low, and Close (OHLC) values for the token in USD.

### Fields
#### 1. `_id` *(ObjectId)* - The unique identifier for this document in the database.
#### 2. `timestamp` *(Date)* - The date and time when the market data was recorded.
#### 3. `contract_address` *(String)* - The address of the token contract associated with the market data.
#### 4. `symbol` *(String)* - The symbol of the token (e.g., UNI for Uniswap).
#### 5. `blockchain` *(String)* - The blockchain where the token operates (e.g., Ethereum).
#### 6. `close (usd)` *(Float)* - The closing price of the token in USD for the specified timestamp.
#### 7. `high (usd)` *(Float)* - The highest price of the token in USD during the specified period.
#### 8. `low (usd)` *(Float)* - The lowest price of the token in USD during the specified period.
#### 9. `open (usd)` *(Float)* - The opening price of the token in USD for the specified timestamp.
#### 10. `protocol_name` *(String)* - The name of the protocol associated with the token (e.g., Uniswap).
#### 11. `type` *(String)* - The type of the protocol (e.g., DEX, Lending).
#### 12. `volume` *(Float)* - The trading volume for the token during the specified period.

### Example
```json
{
  "_id": {
    "$oid": "678e7d11a552daf8aeb188c3"
  },
  "timestamp": {
    "$date": "2023-01-22T00:00:00.000Z"
  },
  "contract_address": "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984",
  "symbol": "uni",
  "blockchain": "ethereum",
  "close (usd)": 0.0002288398682139814,
  "high (usd)": 0.00022923298820387572,
  "low (usd)": 0.00022784991597291082,
  "open (usd)": 0.00022784991597291082,
  "protocol_name": "Uniswap",
  "type": "DEX",
  "volume": 0
}
```
### Objective
To integrate market data into the transaction dataset, enabling the analysis of token price movements and their correlation with transaction activity over time.

---
## 6. Enrichment of Market Data via Transaction Aggregation
### Collection name: `market_enriched` - *(177 955 documents)*
We aggregate transaction data to calculate key metrics like average gas used, transaction value, and unique participants over specified time frames. This enriched data allows for better insights into transaction trends and protocol usage.

### Fields
#### 1. `_id` *(ObjectId)* - The unique identifier for this document in the database.
#### 2. `avg_gas_used` *(Float)* - The average gas used in transactions over the last hour and 24 hours.
#### 3. `avg_value_eth_per_tx` *(Float)* - The average transaction value in ETH over the last hour and 24 hours.
#### 4. `blockchain` *(String)* - The blockchain where the protocol operates (e.g., Ethereum).
#### 5. `close (usd)` *(Float)* - The closing price of the token in USD for the specified timestamp.
#### 6. `contract_address` *(String)* - The address of the token contract associated with the data.
#### 7. `error_rate` *(Float)* - The percentage of transactions with errors over the last hour and 24 hours.
#### 8. `high (usd)` *(Float)* - The highest price of the token in USD during the specified period.
#### 9. `low (usd)` *(Float)* - The lowest price of the token in USD during the specified period.
#### 10. `max_gas_used` *(Integer)* - The maximum gas used in a transaction over the last hour and 24 hours.
#### 11. `max_value_eth` *(Float)* - The maximum transaction value in ETH over the last hour and 24 hours.
#### 12. `median_value_eth` *(Float)* - The median transaction value in ETH over the last hour and 24 hours.
#### 13. `min_gas_used` *(Integer)* - The minimum gas used in a transaction over the last hour and 24 hours.
#### 14. `min_value_eth` *(Float)* - The minimum transaction value in ETH over the last hour and 24 hours.
#### 15. `nb_tx` *(Integer)* - The total number of transactions over the last hour and 24 hours.
#### 16. `nb_unique_receivers` *(Integer)* - The number of unique receiver addresses over the last hour and 24 hours.
#### 17. `nb_unique_senders` *(Integer)* - The number of unique sender addresses over the last hour and 24 hours.
#### 18. `num_errors` *(Integer)* - The total number of transactions with errors over the last hour and 24 hours.
#### 19. `open (usd)` *(Float)* - The opening price of the token in USD for the specified timestamp.
#### 20. `protocol_name` *(String)* - The name of the protocol associated with the token.
#### 21. `std_gas_used` *(Float)* - The standard deviation of gas used in transactions over the last hour and 24 hours.
#### 22. `std_value_eth` *(Float)* - The standard deviation of transaction values in ETH over the last hour and 24 hours.
#### 23. `symbol` *(String)* - The symbol of the token (e.g., NFTFI).
#### 24. `timestamp` *(Date)* - The date and time of the aggregated data.
#### 25. `total_gas_used` *(Integer)* - The total gas used in transactions over the last hour and 24 hours.
#### 26. `total_value_eth` *(Float)* - The total transaction value in ETH over the last hour and 24 hours.
#### 27. `type` *(String)* - The type of the protocol (e.g., NFT-Fi).
#### 28. `volume` *(Float)* - The trading volume for the token during the specified period.

### Example
```json
{
  "_id": {
    "$oid": "678e7d1ca552daf8aeb42f81"
  },
  "avg_gas_used_1h": 0,
  "avg_gas_used_24h": 88387.36363636363,
  "avg_value_eth_per_tx_1h": 0,
  "avg_value_eth_per_tx_24h": 98435.44979489372,
  "blockchain": "ethereum",
  "close (usd)": 0.0033522879239171743,
  "contract_address": "0x09d6f0f5a21f5be4f59e209747e2d07f50bc694c",
  "error_rate_1h": 0,
  "error_rate_24h": 0,
  "high (usd)": 0.003360767150297761,
  "low (usd)": 0.003341925796121359,
  "max_gas_used_1h": 0,
  "max_gas_used_24h": 128672,
  "max_value_eth_1h": 0,
  "max_value_eth_24h": 173027.368086,
  "median_value_eth_1h": 0,
  "median_value_eth_24h": 20308,
  "min_gas_used_1h": 0,
  "min_gas_used_24h": 46674,
  "min_value_eth_1h": 0,
  "min_value_eth_24h": 8627,
  "nb_tx_1h": 0,
  "nb_tx_24h": 11,
  "nb_unique_receivers_1h": 0,
  "nb_unique_receivers_24h": 6,
  "nb_unique_senders_1h": 0,
  "nb_unique_senders_24h": 6,
  "num_errors_1h": 0,
  "num_errors_24h": 0,
  "open (usd)": 0.003341925796121359,
  "protocol_name": "NFTFI",
  "std_gas_used_1h": 0,
  "std_gas_used_24h": 27197.175038036337,
  "std_value_eth_1h": 0,
  "std_value_eth_24h": 61448.22032504086,
  "symbol": "nftfi",
  "timestamp": {
    "$date": "2024-08-10T06:00:00.000Z"
  },
  "total_gas_used_1h": 0,
  "total_gas_used_24h": 972261,
  "total_value_eth_1h": 0,
  "total_value_eth_24h": 1082789.947743831,
  "type": "NFT-Fi",
  "volume": 0
}
```
### Objective
To aggregate transaction and market data into meaningful metrics that represent the overall health and activity of the protocols, facilitating trend analysis.

---
## Credits
This dataset preparation process establishes the foundation for analysis of user behavior, market trends, and protocol performance within the DeFi space. Each step builds upon the previous one, ensuring that the final dataset is rich and well-structured for deeper insights. It includes various technical steps for data extraction, user profiling, and market data aggregation, based on a combination of APIs and data sources. Special thanks to the following sources and tools used in this process:  
1.	**CoinGecko API** - For contract data related to DeFi protocols and their market details.
2.	**Etherscan API** - For transaction data extraction on Ethereum smart contracts.
3.	**Yahoo Finance API** - For market data including OHLC values of tokens and trading volume.  
4. **MongoDB** - For managing and storing large volumes of transaction and protocol data in a structured format.  
5. **Ethereum Blockchain** - For the decentralized financial infrastructure that powers these protocols and transactions.