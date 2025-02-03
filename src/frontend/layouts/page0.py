import streamlit as st


def page_0():
    st.markdown(
        '<div class="header">Introduction_</div>',
        unsafe_allow_html=True,
    )
    st.write("## Features_")

    st.write("""
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
        """)