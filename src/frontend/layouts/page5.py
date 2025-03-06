import streamlit as st

from src.backend.core.utils import load_market  , load_transactions
from src.backend.core.plot_trends import TransactionAnalyzer
from src.backend.core.visualise import DataVisualizer


def page_5():
    st.markdown('<div class="header">Trend Analysis_</div>', unsafe_allow_html=True)
    st.write("""
    This section provides an overview of the trends.
    
    ---
    """)
    base_path = 'src/frontend/layouts/pictures/trends_analysis/'

    st.write("## Correlation_")
    col1, col2 = st.columns(2)
    with col1:
        st.write("##### Transactions vs Users per Protocol_")
        st.image(base_path + 'protocol_tx_vs_users_scatter.png')
    with col2:
        st.write("##### Transactions vs Users per Type_")
        st.image(base_path + 'type_tx_vs_users_scatter.png')

    col1, col2 = st.columns(2)
    with col1:
        st.write("##### Senders vs Receivers per Protocol_")
        st.image(base_path + 'protocol_senders_vs_receivers_scatter.png')
    with col2:
        st.write("##### Senders vs Receivers per Type_")
        st.image(base_path + 'type_senders_vs_receivers_scatter.png')

    col1, col2 = st.columns(2)
    with col1:
        st.write("##### Users vs Value (ETH) per Protocol_")
        st.image(base_path + 'protocol_users_vs_value_scatter.png')
    with col2:
        st.write("##### Users vs Value (ETH) per Type_")
        st.image(base_path + 'type_users_vs_value_scatter.png')

    col1, col2 = st.columns(2)
    with col1:
        st.write("##### Gas vs Users per Protocol_")
        st.image(base_path + 'protocol_gas_vs_users_scatter.png')
    with col2:
        st.write("##### Gas vs Users per Type_")
        st.image(base_path + 'type_gas_vs_users_scatter.png')


    # --------------------------

    st.write("## Proportion Trends_")
    col1, col2 = st.columns(2)
    with col1:
        st.write("##### Unique Users by Protocol_")
        st.image(base_path + 'protocol_users_by_month.png')
    with col2:
        st.write("##### Unique Users by Type_")
        st.image(base_path + 'type_users_by_month.png')

    col1, col2 = st.columns(2)
    with col1:
        st.write("##### Unique Transactions by Protocol_")
        st.image(base_path + 'protocol_tx_by_month.png')
    with col2:
        st.write("##### Unique Transactions by Type_")
        st.image(base_path + 'type_tx_by_month.png')

    col1, col2 = st.columns(2)
    with col1:
        st.write("##### ETH Value by Protocol_")
        st.image(base_path + 'protocol_eth_value_by_month.png')
    with col2:
        st.write("##### ETH Value by Type_")
        st.image(base_path + 'type_eth_value_by_month.png')

    col1, col2 = st.columns(2)
    with col1:
        st.write("##### Gas Used by Protocol_")
        st.image(base_path + 'protocol_gas_value_by_month.png')
    with col2:
        st.write("##### Gas Used by Type_")
        st.image(base_path + 'type_gas_value_by_month.png')


    st.write("## OHLC Chart per Protocol_")
    df = load_market()
    visualizer = DataVisualizer(df)
    visualizer.plot_ohlc('timestamp', 'open (usd)', 'high (usd)', 'low (usd)', 'close (usd)')

    _, col2, _ = st.columns([1,2,1])
    with col2:
        st.write('## Heatmap_')
        st.write("")
        st.write("")
        st.image(base_path + 'correlation_heatmap.png')



    # --------------------------  LOAD TRANSACTIONS DATA
    #df = load_transactions()
    #st.write(df.columns.to_list())
    #df = df.sample(10000)

    # -- Analysis
    #df = df[df['protocol_name'] == 'Aave']
    #df = df.sort_values(by='value (ETH)', ascending=False)
    #st.write(df.head(100))
#
    #identical_rows = df[df['from'] == df['to']]
    #total_rows = len(df)
    #percentage_identical = (len(identical_rows) / total_rows) * 100
    #print(f"Nombre de lignes où 'from' et 'to' sont identiques : {len(identical_rows)}")
    #print(f"Pourcentage de lignes où 'from' et 'to' sont identiques : {percentage_identical:.2f}%")

    # --------------------------  PLOT CORRELATIONS
    #corr_df = df.copy()
    #plotter = TransactionAnalyzer(corr_df)

    #plotter.plot_correlation_heatmap(freq='1ME', filename='correlation_heatmap.png', base_path=base_path)

    #plotter.plot_tx_vs_users_scatter(freq = '1W', file_name='protocol_tx_vs_users_scatter.png', base_path=base_path, group='protocol_name')
    #plotter.plot_tx_vs_users_scatter(freq = '1W', file_name='type_tx_vs_users_scatter.png', base_path=base_path, group='type')


    #plotter.plot_senders_vs_receivers_scatter(freq = '1W', file_name='protocol_senders_vs_receivers_scatter.png', base_path=base_path, group='protocol_name')
    #plotter.plot_senders_vs_receivers_scatter(freq = '1W', file_name='type_senders_vs_receivers_scatter.png', base_path=base_path, group='type')

    #plotter.plot_users_vs_value_scatter(freq = '1h', file_name='protocol_users_vs_value_scatter.png', base_path=base_path, group='protocol_name')
    #plotter.plot_users_vs_value_scatter(freq = '1h', file_name='type_users_vs_value_scatter.png', base_path=base_path, group='type')

    #plotter.plot_gas_vs_users_scatter(freq = '1h', file_name='protocol_gas_vs_users_scatter.png', base_path=base_path, group='protocol_name')
    #plotter.plot_gas_vs_users_scatter(freq = '1h', file_name='type_gas_vs_users_scatter.png', base_path=base_path, group='type')

    # --------------------------  PLOT PROPORTION TRENDS

    # --- Nb Users
    #us_df = df.copy()
    #plotter = TransactionAnalyzer(us_df)
    #plotter.plot_users_by_freq(freq='1ME', file_name='protocol_users_by_month.png', base_path=base_path, group='protocol_name')
    #plotter.plot_users_by_freq(freq='1ME', file_name='type_users_by_month.png', base_path=base_path, group='type')

    # --- Transactions
    #tx_df = df.copy()
    #plotter = TransactionAnalyzer(tx_df)
    #plotter.plot_tx_by_freq(freq='1ME', file_name='protocol_tx_by_month.png', base_path=base_path, group='protocol_name')
    #plotter.plot_tx_by_freq(freq='1ME', file_name='type_tx_by_month.png', base_path=base_path, group='type')

    # --- ETH Value
    #eth_df = df.copy()
    #plotter = TransactionAnalyzer(eth_df)
    #plotter.plot_value_by_freq(freq='1ME', file_name='protocol_eth_value_by_month.png', base_path=base_path, group='protocol_name', value='value (ETH)')
    #plotter.plot_value_by_freq(freq='1ME', file_name='type_eth_value_by_month.png', base_path=base_path, group='type', value='value (ETH)')

    # --- Gas Value
    #gas_df = df.copy()
    #plotter = TransactionAnalyzer(gas_df)
    #plotter.plot_value_by_freq(freq='1ME', file_name='protocol_gas_value_by_month.png', base_path=base_path, group='protocol_name', value='gas_used')
    #plotter.plot_value_by_freq(freq='1ME', file_name='type_gas_value_by_month.png', base_path=base_path, group='type', value='gas_used')