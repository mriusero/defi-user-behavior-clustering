import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from typing import Dict


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names to snake_case and remove parentheses."""
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r'[\s\-_/.]+', '_', regex=True)
        .str.replace(r'[()]+', '', regex=True)
        .str.strip('_')
    )
    return df


def load_data() -> Dict[str, pd.DataFrame]:
    """Load raw data from the cache storage."""
    return st.session_state.get('dataframes', {})


def aggregate_users(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate and enrich users data with derived metrics."""
    with st.spinner("Users aggregation..."):
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

        df['whale_score'] = df[[f'{col}_norm' for col in ['net_flow_eth', 'total_received_eth', 'total_sent_eth']]].sum(
            axis=1)
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

    agg_df = agg_df.merge(peak, on=group_col, how='left')                               # Fusion et calcul de la fréquence
    agg_df[f'tx_frequency_{prefix}'] = agg_df[f'date_nunique_{prefix}'] / total_days
    agg_df.drop(columns=[f'date_nunique_{prefix}'], inplace=True)
    return agg_df


def aggregate_transactions(users: pd.DataFrame, transactions: pd.DataFrame) -> pd.DataFrame:
    """Aggregate and enrich users with transactions metrics."""
    with st.spinner("Transactions aggregation..."):
        if transactions.empty:
            return users            # Gérer le cas des transactions vides si nécessaire

        transactions['timestamp'] = pd.to_datetime(transactions['timestamp'])               # Préparation des données en une seule passe
        transactions['date'] = transactions['timestamp'].dt.date
        transactions['hour'] = transactions['timestamp'].dt.hour
        transactions['gas_efficiency'] = transactions['value_eth'] / transactions['gas_used']

        max_ts = transactions['timestamp'].max()            # Calcul des dates globales une seule fois
        min_ts = transactions['timestamp'].min()
        total_days = (max_ts - min_ts).days or 1            # Éviter la division par zéro

        tx_sent_agg = aggregation_metrics(transactions, total_days, 'from', 'sent')           # Calcul des agrégations pour les transactions envoyées/reçues
        tx_received_agg = aggregation_metrics(transactions, total_days,'to', 'received')

        merged_df = (           # Fusion finale avec les utilisateurs
            users
            .merge(tx_sent_agg, left_on='address', right_on='from', how='left')
            .merge(tx_received_agg, left_on='address', right_on='to', how='left')
        )
    return merged_df


def aggregate_market(merged_df: pd.DataFrame, market: pd.DataFrame) -> pd.DataFrame:
    """Aggregate and enrich users with market metrics"""

    market_protocol_stats = market.groupby('protocol_name').agg({        # Étape 1: Agréger les données de marché par protocole
        'volume': ['mean', 'std'],
        'close_usd': ['mean', 'std'],
        'avg_gas_used_24h': 'mean',
        'error_rate_24h': 'mean'
    }).reset_index()
    market_protocol_stats.columns = [
        'protocol_name',
        'avg_volume', 'std_volume',
        'avg_close_price', 'std_close_price',
        'avg_gas_used', 'avg_error_rate'
    ]
    protocols = ['curve_dao', 'aave', 'tether', 'uniswap', 'maker', 'yearn_finance', 'usdc', 'dai', 'balancer', 'harvest_finance', 'nftfi']  # Étape 2: Calculer l'exposition des utilisateurs
    exposure_metrics = ['total_volume_exposure', 'total_volatility_exposure', 'total_gas_exposure',  'total_error_exposure']

    for metric in exposure_metrics:
        merged_df[metric] = 0.0

    for protocol in protocols:
        count_col = f'{protocol}_count'
        stats = market_protocol_stats[market_protocol_stats['protocol_name'] == protocol]

        if not stats.empty:
            merged_df['total_volume_exposure'] += merged_df[count_col] * stats['avg_volume'].values[0]
            merged_df['total_volatility_exposure'] += merged_df[count_col] * stats['std_close_price'].values[0]
            merged_df['total_gas_exposure'] += merged_df[count_col] * stats['avg_gas_used'].values[0]
            merged_df['total_error_exposure'] += merged_df[count_col] * stats['avg_error_rate'].values[0]

  # eth_price_avg = market[market['symbol'] == 'ETH']['close (usd)'].mean()         # Étape 3: Ajouter des métriques globales
  # merged_df['global_avg_eth_price'] = eth_price_avg
    return merged_df


def split_dataframe(df: pd.DataFrame, train_size: float = 0.7, validation_size: float = 0.15, random_state: int = None) -> Dict[str, pd.DataFrame]:
    """Split DataFrame into train/validation/test sets without stratification."""
    if not abs((train_size + validation_size) - 0.85) < 1e-6:
        raise ValueError("Train + validation sizes must sum to 0.85 (test size fixed at 0.15)")
    train_df, temp_df = train_test_split(
        df, train_size=train_size, random_state=random_state
    )
    val_test_ratio = validation_size / (1 - train_size)
    val_df, test_df = train_test_split(
        temp_df, train_size=val_test_ratio, random_state=random_state
    )
    return {
        'train': train_df,
        'validation': val_df,
        'test': test_df
    }


def implement_features() -> None:
    """Main processing pipeline for feature engineering and data splitting."""
    if 'dataframes' not in st.session_state:
        raise ValueError("No data loaded in session state")

    progress_bar = st.progress(0)

    users = clean_column_names(st.session_state['dataframes']['users'])
    users = aggregate_users(users)
    progress_bar.progress(16)

    transactions = clean_column_names(st.session_state['dataframes']['transactions'])
    merged_df = aggregate_transactions(users, transactions)
    progress_bar.progress(48)

    market = clean_column_names(st.session_state['dataframes']['market'])
    merged_df = aggregate_market(merged_df, market)
    progress_bar.progress(64)

    merged_df.drop(columns=['from', 'to', 'transactions'], inplace=True)
    merged_df.fillna(0)

    st.session_state['features'] = split_dataframe(
        merged_df,
        random_state=42
    )
    progress_bar.progress(80)

    with st.spinner("Saving results..."):
        merged_df.to_parquet('data/features/features.parquet')
        progress_bar.progress(100)

    st.success('Features processed successfully!')