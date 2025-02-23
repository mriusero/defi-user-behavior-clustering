import streamlit as st
import os
import requests
from pyarrow import feather

@st.cache_data
def preload_ranks():
    """ Preload data in streamlit cache. """
    url = 'https://huggingface.co/datasets/mriusero/DeFi-Protocol-Data-on-Ethereum-2023-2024/resolve/main/dataset/data/users_scored.arrow'
    local_file = 'users_scored.arrow'

    response = requests.get(url, timeout=10)
    with open(local_file, 'wb') as file:
        file.write(response.content)

    ranks = feather.read_table(local_file).to_pandas()
    os.remove(local_file)

    return ranks
