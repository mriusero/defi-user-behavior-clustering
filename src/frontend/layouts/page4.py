import streamlit as st

from src.backend.core.utils import load_ranks, check_address, wait_message
from src.backend.reporting.recommendations import recommendations_board


def page_4():
    st.markdown('<div class="header">Performance Report_</div>', unsafe_allow_html=True)
    st.write("""
As the final step of the project, the performance report delivers insights into a user's behavioral analysis. It includes a summary of the cluster analysis associated with the user, an evaluation of strengths and weaknesses within the DeFi ecosystem, and offers recommendations to enhance performance.

>To see the step-by-step analysis, please visit the `Study Overview_` section.

---
    """)
    message_placeholder = wait_message()

    ranks = load_ranks()
    if ranks is not None:
        message_placeholder.empty()

    col1, col2 = st.columns([8, 5])
    with col1:
        st.write("""
        #### Disclaimer_
                
        > This project is for educational and research purposes only.
        > - Not intended for real trading or investment.
        > - No warranties or guarantees provided.
        > - Past performance does not indicate future results.
        > - Creator assumes no liability for financial losses.
        > - Consult a financial advisor for investment decisions.
        > - By using this software, you agree to use it solely for learning purposes.
        
        #### Get a report_
        > **Note:**  This feature is exclusively compatible with Ethereum addresses that have interacted with the following DeFi protocols during 2023 and 2024:
        > - **Decentralized Exchanges (DEX)**: *`Uniswap`, `Curve DAO`, `Balancer`*
        > - **Lending Platforms**: *`Aave`, `Maker`*
        > - **Stablecoins**: *`Tether`, `USD Coin (USDC)`, `Dai`*
        > - **Yield Farming**: *`Yearn Finance`, `Harvest Finance`*
        > - **Non-Fungible Token (NFT)**: *`NFTfi`*
    
        """)
        st.write("")

        selected_address = st.text_area("Enter an Ethereum Address here_", value='0x...', label_visibility='visible', height=68)
        submitted = st.button("Get report")

    with col2:
        st.write("")
        random_addresses = ranks['address'].sample(10).values
        st.markdown("#### Pick an address_\n")
        for address in random_addresses:
            st.markdown(f"```\n{address}\n```")

    if submitted:
        try:
            check = check_address(selected_address, ranks)
            if check:
                st.write(f"""
                ---
                ### Requests_
                 Address: `{selected_address}`
                """)
                recommendations_board(ranks, selected_address)
        except ValueError as ve:
            st.error(f"Value Error: {ve}")

