# 1. General information
general_info = [
    "address"
]

# 2. Transaction Activity
transaction_activity = [
    "received_count",
    "total_received_eth",
    "sent_count",
    "total_sent_eth"
]

# 3. Types of Interaction with Protocols
interaction_protocols = [
    "type_dex",
    "type_lending",
    "type_stablecoin",
    "type_yield_farming",
    "type_nft_fi"
]

# 4. Engagement with Specific Protocols
engagement_protocols = [
    "curve_dao_count",
    "aave_count",
    "tether_count",
    "uniswap_count",
    "maker_count",
    "yearn_finance_count",
    "usdc_count",
    "dai_count",
    "balancer_count",
    "harvest_finance_count",
    "nftfi_count"
]

# 5. User Diversity and Influence
user_diversity_influence = [
    "protocol_type_diversity",
    "protocol_name_diversity",
    "net_flow_eth",
    "whale_score"
]

# 6. Sent Transaction Statistics
sent_tx_stats = [
    "min_sent_eth",
    "avg_sent_eth",
    "med_sent_eth",
    "max_sent_eth",
    "std_sent_eth",
    "min_sent_gas",
    "avg_sent_gas",
    "med_sent_gas",
    "max_sent_gas",
    "std_sent_gas",
    "avg_gas_efficiency_sent",
    "peak_hour_sent",
    "peak_count_sent",
    "tx_frequency_sent"
]

# 7. Received Transaction Statistics
received_tx_stats = [
    "min_received_eth",
    "avg_received_eth",
    "med_received_eth",
    "max_received_eth",
    "std_received_eth",
    "min_received_gas",
    "avg_received_gas",
    "med_received_gas",
    "max_received_gas",
    "std_received_gas",
    "avg_gas_efficiency_received",
    "peak_hour_received",
    "peak_count_received",
    "tx_frequency_received"
]

# 8. Exposure to Market Protocols
market_protocols_exposure = [
    "total_volume_exposure",
    "total_volatility_exposure",
    "total_gas_exposure",
    "total_error_exposure",
    "total_liquidity_exposure",
    "total_activity_exposure",
    "total_user_adoption_exposure",
    "total_gas_volatility_exposure",
    "total_error_volatility_exposure",
    "total_high_value_exposure"
]

SELECTED_FEATURES = (general_info
        + transaction_activity
        + interaction_protocols
        + engagement_protocols
        + user_diversity_influence
        + sent_tx_stats
        + received_tx_stats
        + market_protocols_exposure
)