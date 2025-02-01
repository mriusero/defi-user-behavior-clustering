import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import kurtosis, skew, normaltest, boxcox


def analyze_df(df, csv_out):
    """ Analyze the distribution of numeric columns in a DataFrame, define a standardisation method associated and save the results to a CSV file."""
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input is not a DataFrame.")

    numeric_cols = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
    results = []
    progress_bar = st.progress(0)

    for idx, col in enumerate(numeric_cols):
        try:
            col_data = df[col].dropna()
            p_val = normaltest(col_data)[1] if len(col_data) > 7 else np.nan
            norm_status = "Not-normal" if p_val < 0.05 else "Normal"
            skew_val = skew(col_data) if len(col_data) > 1 else np.nan
            kurt_val = kurtosis(col_data) if len(col_data) > 1 else np.nan

            skew_desc = "Symmetric" if abs(skew_val) < 0.5 else (
                "Positively skewed" if skew_val > 0 else "Negatively skewed")
            kurt_desc = "Mesokurtic (Normal)" if 2.5 <= kurt_val <= 3.5 else (
                "Leptokurtic" if kurt_val > 3.5 else "Platykurtic")

            if norm_status == "Normal":
                standardization = "Z-score"
            elif abs(skew_val) < 0.5:                                                   # Faible asymétrie
                standardization = "Min-Max"
            elif skew_val > 1:                                                          # Asymétrie positive forte
                standardization = "Log" if (df[col] > 0).all() else "Box-Cox"
            elif skew_val < -1:                                                         # Asymétrie négative forte
                standardization = "Log Inverse" if (df[col] > 0).all() else "Box-Cox"
            elif kurt_val > 3.5:                                                        # Kurtosis élevée, queues épaisses
                standardization = "Box-Cox"
            elif kurt_val < 2.5:                                                        # Kurtosis faible, queues légères
                standardization = "Min-Max"
            else:
                standardization = "None"

            results.append([col, norm_status, p_val, skew_val, skew_desc, kurt_val, kurt_desc, standardization])

        except ValueError as e:
            print(f"Error on {col}: {e}")

        progress = (idx + 1) / len(numeric_cols)
        progress_bar.progress(progress)

    df_results = pd.DataFrame(results, columns=['Variable', 'Normality', 'p_value', 'Skewness', 'Skew_Desc', 'Kurtosis', 'Kurt_Desc', 'Standardization'])
    df_results.to_csv(csv_out, index=False, encoding="utf-8")


def standardize_df(df, csv_in):
    """Standardize the numeric columns in a DataFrame based on the standardization method defined in a CSV file."""
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input is not a DataFrame.")
    try:
        std_info = pd.read_csv(csv_in)
    except (FileNotFoundError, pd.errors.EmptyDataError) as e:
        raise ValueError(f"Error loading standardization file: {e}") from e

    df_transformed = df.copy()
    progress_bar = st.progress(0)
    total_rows = len(std_info)

    for idx, row in std_info.iterrows():
        col, method = row['Variable'], row['Standardization']
        if col in df_transformed.columns and pd.api.types.is_numeric_dtype(df_transformed[col]):
            if method == "Z-score":
                df_transformed[col] = (df_transformed[col] - df_transformed[col].mean()) / df_transformed[col].std()
            elif method == "Min-Max":
                df_transformed[col] = (df_transformed[col] - df_transformed[col].min()) / (
                        df_transformed[col].max() - df_transformed[col].min())
            elif method == "Log":
                df_transformed[col] = np.log1p(np.maximum(df_transformed[col], 0))
            elif method == "Log Inverse":
                df_transformed[col] = np.log1p(np.maximum(-df_transformed[col], 0))
            elif method == "Box-Cox":
                df_transformed[col], _ = boxcox(df_transformed[col] - df_transformed[col].min() + 1)

        progress = (idx + 1) / total_rows
        progress_bar.progress(progress)

    return df_transformed


def statistical_tests():
    """Main pipeline to analyze and normalize data."""
    if 'features' not in st.session_state.get('dataframes', {}):
        df = pd.read_parquet('data/features/features.parquet', engine='pyarrow')
    else:
        df = st.session_state['dataframes']['features']

    analyze_df(df, csv_out="config/to_standardize.csv")
    df_std = standardize_df(df, csv_in="config/to_standardize.csv")
    analyze_df(df_std, csv_out="config/standardized.csv")

    df_std.to_parquet('data/features/standardized.parquet', engine='pyarrow')

    return df_std