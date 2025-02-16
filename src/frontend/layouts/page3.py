import streamlit as st

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

def page_3():
    st.markdown('<div class="header">Exploratory Analysis_</div>', unsafe_allow_html=True)
    st.write(""" 
    
Following the feature engineering process, the exploratory analysis provides first draw of insights into user behavior and protocol interactions within the DeFi ecosystem. A variety of visualizations are used to illustrate the relationships between users, protocols, and market metrics.
    
---

## Transactions Volumes and Values_  /!\ To review

    """)

    st.image("docs/graphics/exploratory_analysis/tx_volumes_and_values.png", caption="")
    col1, col2 = st.columns(2)
    with col1:
        st.write("""
        ### Transactions Volumes_
        This graph shows the number of transactions sent and received by users.
        #### Distribution :
        Il y a une concentration notable de points le long de la diagonale, ce qui suggère que pour de nombreux utilisateurs, le nombre de transactions envoyées est similaire au nombre de transactions reçues.
        
        #### Observations :
        La densité des points diminue à mesure que l'on s'éloigne de l'origine, indiquant que les transactions élevées (envoi ou réception) sont moins fréquentes.
        """)
    with col2:
        st.write("""
        ### Transactions Values_
        This graph shows the total value of transactions sent and received by users.
        #### Distribution :
        Les points sont largement dispersés, mais il y a une concentration le long de la diagonale, indiquant que pour de nombreux utilisateurs, la valeur totale de l'ETH envoyé est proche de la valeur totale de l'ETH reçu.

        #### Observations :
        La concentration le long de la diagonale suggère un équilibre entre les valeurs envoyées et reçues pour de nombreux utilisateurs.
        Les points en dehors de la diagonale indiquent des utilisateurs avec des déséquilibres significatifs, on constate notamment que les valeurs totales envoyées sont généralement plus élevées que les totales reçues.
        
        """)


    st.write("""
## Network Analysis_
The network analysis provides an abstract vision of relationships between user addresses and DeFi protocols. By visualizing the connections between users and protocols, we can identify patterns in user behavior and protocol interactions.   

#### Protocols Network_
    
This graph represents the network of user addresses and the protocols they interact with.  
Each node represents a user address and each edge represents a transaction between a user and a protocol.  

> **Note:** This graph contains only 100 000 users against 6 876 845 in the real dataset.

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
        st.image("docs/graphics/network/address_protocol_nx_plot.png", caption="")

