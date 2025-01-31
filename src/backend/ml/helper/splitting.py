import pandas as pd
from sklearn.model_selection import train_test_split
from typing import Dict


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