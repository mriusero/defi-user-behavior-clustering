import streamlit as st

def page_1():
    st.markdown(
        '<div class="header">Data Collection_</div>',
        unsafe_allow_html=True,
    )
    st.write("""
The data used in this analysis is sourced from the `Ethereum blockchain` and dataset was obtained with the following steps:

#### 1. **Fetching Contracts Addresses**: 
*The addresses of smart contracts for each selected DeFi protocols were obtained with the CoinGecko API.*

```json
# Example of a contract address for Uniswap
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
#### 2. **Extracting Users Transactions**:
*The transactions associated to contracts on Ethereum blockchain were obtained with the Etherscan API.  
The data includes transaction hashes, sender and receiver addresses, gas usage, and transaction values.*

##### Timeframe:
* Start: `2022-12-31T22:59:59.000Z`   
* End: `2024-12-30T23:00:11.000Z`

```json
# Example of a user transaction
{
  "_id": {
    "$oid": "678bf7cf9ebf7cf7c1a3a88e"
  },
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

#### 3. **Generation of Users profiles**:
*By processing transactional data, we can create user profiles based on the Ethereum addresses involved in transactions.  
This step allows to aggregate users activities across different protocols and their total received and sent amounts with associated metadata.*

```json
# Example of a user profile
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

#### 4. **Fetching Market Behavior**:
*By extracting market data with the Yahoo Finance API, transactional data are enrich by associating the market behavior of a given token over the time.*

```json
# Example of market data for Uniswap token
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

#### 5. **Enrichment of Market Metrics**:

*Market metrics for a given protocol are enrich by aggregation of transactional data, like average gas used, transaction value, and unique participants over specified time frames.*

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
#### 6. **Data Storage**:
All data are stored in Parquet format and are available in the [Hugging Face hub](https://huggingface.co/datasets/mriusero/DeFi-Protocol-Data-on-Ethereum-2023-2024/tree/main/dataset/data).

    ├── contracts.parquet         # Contains contract details for selected DeFi protocols.
    ├── transactions.parquet      # Contains transaction data for Ethereum-based contracts.
    ├── market.parquet            # Contains enriched market data with aggregated transaction metrics.
    └── users.parquet             # User profiles based on transaction data.

    """)
