import pandas as pd
import pyarrow as pa
import pyarrow.feather as feather

def load_data(path) -> pd.DataFrame:
    """Load data from a parquet file."""
    return pd.read_parquet(path, engine='pyarrow')


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names to snake_case and remove parentheses."""
    df.columns = (
        df.columns.str.strip()                              # Delete leading/trailing spaces
        .str.lower()                                        # Convert to lowercase
        .str.replace(r'[\s\-_/.]+', '_', regex=True)        # Replace spaces, dashes, underscores, dots, and slashes with underscores
        .str.replace(r'[()]+', '', regex=True)              # Delete parentheses
        .str.strip('_')                                     # Delete leading/trailing underscores
    )
    return df


def aggregate_users(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate and enrich users data with derived metrics."""
    df = df.drop(columns=['first_seen', 'last_seen'])
    protocol_types = ["type_dex", "type_lending", "type_stablecoin", "type_yield_farming", "type_nft_fi"]
    protocol_names = [
        "curve_dao_count", "aave_count", "tether_count", "uniswap_count",
        "maker_count", "yearn_finance_count", "usdc_count", "dai_count",
        "balancer_count", "harvest_finance_count", "nftfi_count"
    ]
    df['protocol_type_diversity'] = (df[protocol_types] != 0).sum(axis=1)
    df['protocol_name_diversity'] = (df[protocol_names] != 0).sum(axis=1)
    df['net_flow_eth'] = df['total_received_eth'] - df['total_sent_eth']
    for col in ['net_flow_eth', 'total_received_eth', 'total_sent_eth']:
        df[f'{col}_norm'] = df[col] / df[col].max()
    df['whale_score'] = df[[f'{col}_norm' for col in ['net_flow_eth', 'total_received_eth', 'total_sent_eth']]].sum(axis=1)

    return df.drop(columns=[f'{col}_norm' for col in ['net_flow_eth', 'total_received_eth', 'total_sent_eth']])


def aggregation_metrics(df, total_days, group_col, prefix):
    """ Aggregation metrics calculation for transaction"""
    agg_df = df.groupby(group_col).agg(
        **{
            f'min_{prefix}_eth': ('value_eth', 'min'),
            f'avg_{prefix}_eth': ('value_eth', 'mean'),
            f'med_{prefix}_eth': ('value_eth', 'median'),
            f'max_{prefix}_eth': ('value_eth', 'max'),
            f'std_{prefix}_eth': ('value_eth', 'std'),
            f'min_{prefix}_gas': ('gas_used', 'min'),
            f'avg_{prefix}_gas': ('gas_used', 'mean'),
            f'med_{prefix}_gas': ('gas_used', 'median'),
            f'max_{prefix}_gas': ('gas_used', 'max'),
            f'std_{prefix}_gas': ('gas_used', 'std'),
            f'date_nunique_{prefix}': ('date', 'nunique'),
            f'avg_gas_efficiency_{prefix}': ('gas_efficiency', 'mean')
        }
    ).reset_index()
    hour_counts = df.groupby([group_col, 'hour']).size().reset_index(name='count')
    peak = hour_counts.loc[hour_counts.groupby(group_col)['count'].idxmax()]
    peak = peak.rename(columns={
        'hour': f'peak_hour_{prefix}',
        'count': f'peak_count_{prefix}'
    })[[group_col, f'peak_hour_{prefix}', f'peak_count_{prefix}']]

    agg_df = agg_df.merge(peak, on=group_col, how='left')                               # Merge peak hour and count
    agg_df[f'tx_frequency_{prefix}'] = agg_df[f'date_nunique_{prefix}'] / total_days
    agg_df.drop(columns=[f'date_nunique_{prefix}'], inplace=True)
    return agg_df


def aggregate_transactions(users: pd.DataFrame, transactions: pd.DataFrame) -> pd.DataFrame:
    """Aggregate and enrich users with transactions metrics."""
    if transactions.empty:
        return users            # Make sure to return the users DataFrame if no transactions are available

    transactions['timestamp'] = pd.to_datetime(transactions['timestamp'])               # Preprocessing
    transactions['date'] = transactions['timestamp'].dt.date
    transactions['hour'] = transactions['timestamp'].dt.hour
    transactions['gas_efficiency'] = transactions['value_eth'] / transactions['gas_used']

    max_ts = transactions['timestamp'].max()            # Calculating total days
    min_ts = transactions['timestamp'].min()
    total_days = (max_ts - min_ts).days or 1            # Avoid division by zero

    tx_sent_agg = aggregation_metrics(transactions, total_days, 'from', 'sent')           # Calculate metrics for sent transactions
    tx_received_agg = aggregation_metrics(transactions, total_days,'to', 'received')      # Calculate metrics for received transactions

    merged_df = (                               # Merge aggregated data with users
        users
        .merge(tx_sent_agg, left_on='address', right_on='from', how='left')
        .merge(tx_received_agg, left_on='address', right_on='to', how='left')
    )
    return merged_df


def aggregate_market(merged_df: pd.DataFrame, market: pd.DataFrame) -> pd.DataFrame:
    """Aggregate and enrich users with market metrics"""
    market['protocol_name'] = (
        market['protocol_name']
        .str.strip()
        .str.lower()
        .str.replace(r'[\s\-_/.]+', '_', regex=True)
        .str.replace(r'[()]+', '', regex=True)
        .str.strip('_')
    )

    market_protocol_stats = market.groupby('protocol_name').agg({
        'volume': ['mean', 'std'],
        'close_usd': ['mean', 'std'],
        'avg_gas_used_24h': 'mean',
        'error_rate_24h': 'mean',
        'total_value_eth_24h': 'mean',
        'nb_tx_24h': 'mean',
        'nb_unique_receivers_24h': 'mean',
        'nb_unique_senders_24h': 'mean',
        'std_gas_used_24h': 'mean',
        'std_value_eth_24h': 'mean',
        'max_value_eth_24h': 'mean'
    }).reset_index()

    market_protocol_stats.columns = [
        'protocol_name',
        'avg_volume', 'std_volume',
        'avg_close_price', 'std_close_price',
        'avg_gas_used', 'avg_error_rate',
        'avg_total_value_eth', 'avg_nb_tx',
        'avg_nb_unique_receivers', 'avg_nb_unique_senders',
        'std_gas_used', 'std_value_eth',
        'max_value_eth'
    ]

    protocols = ['curve_dao', 'aave', 'tether', 'uniswap', 'maker', 'yearn_finance', 'usdc', 'dai', 'balancer',
                 'harvest_finance', 'nftfi']

    exposure_metrics = {
        'total_volume_exposure': 'avg_volume',
        'total_volatility_exposure': 'std_close_price',
        'total_gas_exposure': 'avg_gas_used',
        'total_error_exposure': 'avg_error_rate',
        'total_liquidity_exposure': 'avg_total_value_eth',
        'total_activity_exposure': 'avg_nb_tx',
        'total_user_adoption_exposure': ['avg_nb_unique_receivers', 'avg_nb_unique_senders'],
        'total_gas_volatility_exposure': 'std_gas_used',
        'total_error_volatility_exposure': 'std_value_eth',
        'total_high_value_exposure': 'max_value_eth'
    }

    for metric in exposure_metrics.keys():
        merged_df[metric] = 0.0

    for protocol in protocols:
        count_col = f'{protocol}_count'
        stats = market_protocol_stats[market_protocol_stats['protocol_name'] == protocol]

        if not stats.empty:
            for metric, market_col in exposure_metrics.items():
                if isinstance(market_col, list):
                    merged_df[metric] += merged_df[count_col] * sum(stats[col].values[0] for col in market_col)
                else:
                    merged_df[metric] += merged_df[count_col] * stats[market_col].values[0]

    return merged_df


def implement_features() -> None:
    """Main processing pipeline for feature engineering and data splitting."""
    print('\n ====== Implementing features ====== \n')

    print('1. Loading data\n----------------------------------------')
    users = load_data(path='data/processed/users_processed.parquet')
    transactions = load_data(path='data/raw/transactions.parquet')
    market = load_data(path='data/raw/market.parquet')
    print('Data loaded successfully\n')

    print('2. Processing users\n----------------------------------------')
    users = clean_column_names(users)
    users = aggregate_users(users)
    print('Users processed successfully\n')

    print('3. Processing transactions\n----------------------------------------')
    transactions = clean_column_names(transactions)
    merged_df = aggregate_transactions(users, transactions)
    print('Transactions processed successfully\n')

    print('4. Processing market\n----------------------------------------')
    market = clean_column_names(market)
    merged_df = aggregate_market(merged_df, market)
    print('Market processed successfully\n')

    print('5. Cleaning data\n----------------------------------------')
    merged_df.drop(columns=['from', 'to', 'transactions'], inplace=True)
    merged_df = merged_df.map(lambda x: pd.NA if x is None else x)
    merged_df = merged_df.fillna(0)
    print('Data cleaned successfully\n')

    print('6. Saving data\n----------------------------------------')
    table = pa.Table.from_pandas(merged_df)
    feather.write_feather(table, 'data/features/features.arrow')
    print('Data saved successfully\n')