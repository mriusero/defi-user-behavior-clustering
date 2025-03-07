from typing import Any
import pandas as pd
import streamlit as st
import re
import os
import requests
from pyarrow import feather

@st.cache_data
def cache():
    """ Preload data in streamlit cache. """

    # Load Ranks
    url = 'https://huggingface.co/datasets/mriusero/DeFi-Protocol-Data-on-Ethereum-2023-2024/resolve/main/dataset/data/users_scored.arrow'
    local_file = 'users_scored.arrow'

    response = requests.get(url, timeout=10)
    with open(local_file, 'wb') as file:
        file.write(response.content)

    ranks = feather.read_table(local_file).to_pandas()
    os.remove(local_file)

    return ranks

@st.cache_data
def load_transactions():

    url = 'https://huggingface.co/datasets/mriusero/DeFi-Protocol-Data-on-Ethereum-2023-2024/resolve/main/dataset/data/transactions.parquet'
    local_file = 'transactions.parquet'

    response = requests.get(url, timeout=10)
    with open(local_file, 'wb') as file:
        file.write(response.content)

    tx = pd.read_parquet(local_file)
    os.remove(local_file)

    return tx


@st.cache_data
def load_market():

    url = 'https://huggingface.co/datasets/mriusero/DeFi-Protocol-Data-on-Ethereum-2023-2024/resolve/main/dataset/data/market.parquet'
    local_file = 'market.parquet'

    response = requests.get(url, timeout=10)
    with open(local_file, 'wb') as file:
        file.write(response.content)

    mkt = pd.read_parquet(local_file)
    os.remove(local_file)

    return mkt


def load_ranks():
    """ Load ranks into session state with error handling. """
    try:
        if 'ranks' not in st.session_state or st.session_state['ranks'] is None:
            ranks = cache()
            st.session_state['ranks'] = ranks
        else:
            ranks = st.session_state['ranks']
    except requests.RequestException as e:
        st.error(f"Error downloading file: {e}")
        ranks = None
    return ranks


def is_valid_ethereum_address(address: object) -> Any:
    """ Check if address is a valid ethereum address. """
    eth_address_regex = r'^0x[a-fA-F0-9]{40}$'
    return re.match(eth_address_regex, address) is not None


def check_address(address, ranks):
    """ Check if address is in the ranks. """
    if not is_valid_ethereum_address(address):
        st.error("The input provided is not a valid Ethereum address.")
        return False
    elif address not in ranks['address'].values:
        st.warning("This address is not in the study dataset.")
        return False
    return True