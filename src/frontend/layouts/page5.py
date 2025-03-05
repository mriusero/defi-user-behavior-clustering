import streamlit as st

from src.backend.core.utils import load_market#, load_transactions,
#from src.backend.core.plot_trends import TransactionAnalyzer
from src.backend.core.visualise import DataVisualizer

def page_5():
    st.markdown('<div class="header">Trend Analysis_</div>', unsafe_allow_html=True)
    st.write("""
    This section provides an overview of the trends.
    
    ---
    """)
    # PLOT MARKET OHLC
    st.write("## OHLC Chart_")

    df = load_market()
    visualizer = DataVisualizer(df)
    visualizer.plot_ohlc('timestamp', 'open (usd)', 'high (usd)', 'low (usd)', 'close (usd)')

    # PLOT TRANSACTIONS TRENDS
    st.write("## Transactions Trends_")
    base_path = 'src/frontend/layouts/pictures/trends_analysis/'
    #df = load_transactions()
    #df = df.sample(100000)

    # -------------------------------------------- V2
    #tx_df = df.copy()
    #plotter = TransactionAnalyzer(tx_df)
    #plotter.plot_tx_by_freq(freq='1ME', file_name='protocol_tx_by_month.png', base_path=base_path, group='protocol_name')
    #plotter.plot_tx_by_freq(freq='ME', file_name='type_tx_by_month.png', base_path=base_path, group='type')

    st.write("#### Unique Transactions by Protocol and Type_")
    col1, col2 = st.columns(2)
    with col1:
        st.image(base_path + 'protocol_tx_by_month.png')
    with col2:
        st.image(base_path + 'type_tx_by_month.png')

    # ---

    #eth_df = df.copy()
    #plotter = TransactionAnalyzer(eth_df)
    #plotter.plot_value_by_freq(freq='1ME', file_name='protocol_eth_value_by_month.png', base_path=base_path, group='protocol_name', value='value (ETH)')
    #plotter.plot_value_by_freq(freq='1ME', file_name='type_eth_value_by_month.png', base_path=base_path, group='type', value='value (ETH)')

    st.write("#### ETH Value by Protocol and Type_")
    col1, col2 = st.columns(2)
    with col1:
        st.image(base_path + 'protocol_eth_value_by_month.png')
    with col2:
        st.image(base_path + 'type_eth_value_by_month.png')

    # ---

    #gas_df = df.copy()
    #plotter = TransactionAnalyzer(gas_df)
    #plotter.plot_value_by_freq(freq='1ME', file_name='protocol_gas_value_by_month.png', base_path=base_path, group='protocol_name', value='gas_used')
    #plotter.plot_value_by_freq(freq='1ME', file_name='type_gas_value_by_month.png', base_path=base_path, group='type', value='gas_used')

    st.write("#### Gas Value by Protocol and Type_")
    col1, col2 = st.columns(2)
    with col1:
        st.image(base_path + 'protocol_gas_value_by_month.png')
    with col2:
        st.image(base_path + 'type_gas_value_by_month.png')


