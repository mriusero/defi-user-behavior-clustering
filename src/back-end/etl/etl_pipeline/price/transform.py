import pandas as pd


def transform_ohlc_data(contract_metadata: dict, symbol: str, raw_data: pd.DataFrame) -> list:
    """
    Transforms the extracted OHLC data into a format suitable for MongoDB.

    :param contract_metadata: Metadata related to the contract, including blockchain, protocol name, contract address, and type. (dict)
    :param symbol: The symbol for the contract (e.g., 'ETH'). (str)
    :param raw_data: The raw OHLC data as a pandas DataFrame. (pd.DataFrame)
    :return: A list of dictionaries where each dictionary represents a transformed data row. (list)
    :rtype: list
    """
    raw_data.reset_index(inplace=True)
    raw_data['Datetime'] = pd.to_datetime(raw_data['Datetime'], errors='coerce')
    raw_data.fillna({'Open': 0, 'High': 0, 'Low': 0, 'Close': 0, 'Volume': 0}, inplace=True)

    blockchain = contract_metadata.get('blockchain')
    protocol_name = contract_metadata.get('protocol_name')
    contract_address = contract_metadata.get('contract_address')
    contract_type = contract_metadata.get('type')

    transformed_data = raw_data[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']].apply(
        lambda row: {
            "timestamp": row['Datetime'],
            "blockchain": blockchain,
            "protocol_name": protocol_name,
            "contract_address": contract_address,
            "type": contract_type,
            "symbol": symbol,
            "open (usd)": row['Open'],
            "high (usd)": row['High'],
            "low (usd)": row['Low'],
            "close (usd)": row['Close'],
            "volume": row['Volume']
        },
        axis=1
    ).tolist()

    return transformed_data