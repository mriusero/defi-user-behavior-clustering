import pandas as pd
import streamlit as st
import kagglehub


@st.cache_data
def data_loading(
    files_list, base_path="mariusayrault/defi-protocol-data-on-ethereum-2yr-23-to-24"
):
    """
    Load data from parquet files
    :param files_list: list of files to load (list)
    :param base_path: the base path to the files (str)
    :return: a dictionary of dataframes loaded from kaggle and stored in session state (dict)
    """
    if "dataframes" not in st.session_state:
        dataframes = {}
        progress_bar = st.progress(0)
        total_files = len(files_list)

        for index, file in enumerate(files_list):
            if file == "users":
                path = "processed/users_processed.parquet"
            else:
                path = "dataset/data/" + file + ".parquet"

            endpoint = kagglehub.dataset_download(base_path, path=path)
            df = pd.read_parquet(endpoint, engine="pyarrow")
            dataframes[file] = df
            progress_bar.progress((index + 1) / total_files)

        ## ====== Data cast ====== ##
        for _, df in dataframes.items():
            ## ====== Timestamp conversion ====== ##
            if "timestamp" in df.columns:
                df["timestamp"] = pd.to_datetime(
                    df["timestamp"], errors="coerce", unit="s"
                )

            elif "first_seen" in df.columns:
                df["first_seen"] = pd.to_datetime(df["first_seen"], errors="coerce")

            elif "last_seen" in df.columns:
                df["last_seen"] = pd.to_datetime(df["last_seen"], errors="coerce")

            ## ====== Address conversion ====== ##
            elif "contract_address" in df.columns:
                df["contract_address"] = df["contract_address"].astype(str)

            elif "address" in df.columns:
                df["address"] = df["address"].astype(str)

            st.session_state["dataframes"] = dataframes
