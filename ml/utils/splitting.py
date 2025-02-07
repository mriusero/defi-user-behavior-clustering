import pandas as pd
from sklearn.model_selection import train_test_split
from typing import Dict, Tuple
import pyarrow.feather as feather
from joblib import dump, load


def split_dataframe(df: pd.DataFrame, train_size: float = 0.7, validation_size: float = 0.15, random_state: int = None) -> Dict[str, Tuple[pd.DataFrame, pd.Series]]:
    """Split DataFrame into train/validation/test sets while preserving the 'address' column in separate tuples."""
    if not abs((train_size + validation_size) - 0.85) < 1e-6:
        raise ValueError("Train + validation sizes must sum to 0.85 (test size fixed at 0.15)")

    address = df['address']
    df = df.drop(columns=['address'])

    train_df, temp_df = train_test_split(
        df, train_size=train_size, random_state=random_state
    )
    val_test_ratio = validation_size / (1 - train_size)
    val_df, test_df = train_test_split(
        temp_df, train_size=val_test_ratio, random_state=random_state
    )

    return {
        'all': (df, address),
        'train': (train_df, address.loc[train_df.index]),
        'validation': (val_df, address.loc[val_df.index]),
        'test': (test_df, address.loc[test_df.index])
    }


def splitting():
    """Step 1 of pipeline : split the dataset into train, validation, and test sets."""

    cache_file = 'tmp/cached_dataset.joblib'
    try:
        dataset = load(cache_file)
        print("Dataset loaded from cache")
        return dataset
    except FileNotFoundError:
        print("No cached dataset found, creating a new one...")

    table = feather.read_table('data/features/features_standardised.arrow')
    df = table.to_pandas()

    df.fillna(0, inplace=True)

    dataset = split_dataframe(df=df, train_size=0.7, validation_size=0.15, random_state=42)
    datasets = ['all', 'train', 'validation', 'test']

    for data in datasets:
        x_data, y_data = dataset[data]
        print(f"- x_{data} shape:", x_data.shape)
        print(f"- y_{data} shape:", y_data.shape)
        missing_x = x_data.isnull().sum()
        missing_x = missing_x[missing_x > 0]

        if not missing_x.empty:
            print(f"- Missing values in x_{data}:")
            print(missing_x)

    dump(dataset, cache_file)

    return dataset