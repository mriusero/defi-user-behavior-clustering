import streamlit as st

from src.backend.core.utils import load_ranks, check_address
from src.frontend.recommendations import recommendations_board


def page_4():
    st.markdown('<div class="header">Who am I ?</div>', unsafe_allow_html=True)
    st.write("""
    Give me your ethereum address and I will tell who you are.    
    
    ---
    """)
    ranks = load_ranks()
    if ranks is not None:
        pass

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
        > `curve_dao_count`, `aave_count`, `uniswap_count`, `maker_count`, `tether_count`, `yearn_finance_count`,
        > `usdc_count`, `dai_count`, `balancer_count`, `harvest_finance_count`, `nftfi_count`.
    
        """)
        st.write("")

        selected_address = st.text_area("Enter an Ethereum Address here_", value='0x...', label_visibility='visible', height=68)
        submitted = st.button("Get report")

    with col2:
        st.write("")
        random_addresses = ranks['address'].sample(8).values
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

