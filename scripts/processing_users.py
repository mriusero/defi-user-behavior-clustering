import pandas as pd
import json
from tqdm.auto import tqdm


def load_data(file_list, base_path):
    """Load data with progress tracking"""
    dataframes = {}
    for file in tqdm(file_list, desc="Loading files"):
        file_path = f"{base_path}/{file}.parquet"
        df = pd.read_parquet(file_path)
        dataframes[file] = df
        tqdm.write(f"\nDataFrame '{file}' columns:\n{df.columns.tolist()}")
    return dataframes


def clean_column_names(df):
    """Normalize column names to snake_case"""
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r"[\s\-_/.]+", "_", regex=True)
        .str.replace(r"_{2,}", "_", regex=True)
        .str.strip("_")
    )
    return df


def parse_protocols(protocol_str):
    """Parse JSON protocol strings"""
    try:
        protocols = json.loads(protocol_str)
        return protocols if isinstance(protocols, dict) else {}
    except json.JSONDecodeError:
        return {}


def process_user_protocols(users_df):
    """Process user protocol types"""
    protocol_columns = [
        "type_" + k for k in ["DEX", "Lending", "Stablecoin", "Yield Farming", "NFT-Fi"]
    ]
    users_df = users_df.assign(**{col: 0 for col in protocol_columns})

    with tqdm(total=2, desc="Processing protocols") as pbar:
        users_df["parsed_protocols"] = users_df["protocol_types"].apply(parse_protocols)
        pbar.update(1)

        for protocol in tqdm(
            ["DEX", "Lending", "Stablecoin", "Yield Farming", "NFT-Fi"],
            desc="Protocol types",
        ):
            column_name = f"type_{protocol}"
            users_df[column_name] = users_df["parsed_protocols"].apply(
                lambda x: x.get(protocol, 0)
            )
        pbar.update(1)

    return users_df.drop(columns=["protocol_types", "parsed_protocols"])


def transform_protocols_column(df, column_name="protocols_used"):
    """Transform protocols used column into count features"""
    df[column_name] = df[column_name].apply(
        lambda x: eval(x) if isinstance(x, str) else x
    )

    with tqdm(total=len(df), desc="Protocol details") as pbar:
        for index, row in df.iterrows():
            protocols = row[column_name]
            for protocol_name, protocol_data in protocols.items():
                df.at[index, f"{protocol_name}_count"] = int(
                    protocol_data.get("count", 0)
                )
            pbar.update(1)

    return df.drop(columns=[column_name])


def main():
    dataframes = load_data(["users"], "../data/raw")

    with tqdm(total=4, desc="Overall processing") as main_pbar:
        users = dataframes["users"].copy()

        users = process_user_protocols(users)
        main_pbar.update(1)

        users = transform_protocols_column(users)
        main_pbar.update(1)

        users = clean_column_names(users)
        main_pbar.update(1)

        users.fillna(0, inplace=True)
        protocols_counts = [
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
        ]
        users[protocols_counts] = users[protocols_counts].astype(int)
        users.to_parquet("../data/processed/users_processed.parquet", engine="pyarrow")
        main_pbar.update(1)

    print("\nFinal columns:")
    print(users.columns.tolist())
    print("\nData preview:")
    print(users.head(5))


if __name__ == "__main__":
    main()
