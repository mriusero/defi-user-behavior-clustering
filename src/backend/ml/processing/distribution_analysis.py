import streamlit as st
import pandas as pd
import json
from scipy.stats import kurtosis, skew, normaltest


def save_analysis_to_markdown(filename, content):
    """Saves the content to a Markdown file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


def analyse_features(df, output_file="docs/statistical_analysis.md", json_output_file="data/features/statistical_analysis.json"):
    """
    Analyzes the DataFrame, applies several statistical tests on numeric columns, then saves the results in Markdown and JSON.
    :param df: The DataFrame to be analyzed.  (pd.DataFrame)
    :param output_file: The file path for saving the statistical analysis report in Markdown format. (str, default is "docs/statistical_analysis.md")
    :param json_output_file: The file path for saving the statistical analysis results in JSON format. (str, default is "data/features/statistical_analysis.json")
    :raise ValueError: If the provided input is not a DataFrame.
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("The provided input is not a DataFrame.")

    report = "# Statistical Analysis of Numeric Variables\n\n"
    numeric_cols = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
    results_summary = []

    for col in numeric_cols:
        try:
            _, p_value = normaltest(df[col].dropna())            # Perform normality test
            threshold = 1e-4
            if p_value < threshold:
                result_message = "Not-normal"
            else:
                result_message = "Normal"

            skewness = skew(df[col].dropna())                                   # Calculate skewness
            kurt = kurtosis(df[col].dropna())                                   # Calculate kurtosis
            skewness_desc = "Symmetric" if abs(skewness) < 0.5 else (
                "Positively skewed" if skewness > 0 else "Negatively skewed")
            kurtosis_desc = "Mesokurtic (Normal)" if 2.5 <= kurt <= 3.5 else (
                "Leptokurtic" if kurt > 3.5 else "Platykurtic")

            if result_message == "Normal":                        # Determine the recommended standardization method
                standardization = "Z-score normalization"
            elif abs(skewness) < 0.5:
                standardization = "Min-Max normalization"
            elif skewness > 1 or skewness < -1:
                standardization = "Logarithmic transformation"
            elif kurt > 3.5:
                standardization = "Box-Cox transformation"
            else:
                standardization = "No transformation needed"

            results_summary.append({
                'Variable': col,
                'Normality Test': result_message,
                'Skewness': f"{skewness:.2f} → {skewness_desc}",
                'Kurtosis': f"{kurt:.2f} → {kurtosis_desc}",
                'Recommended Standardization': standardization
            })
        except ValueError as e:
            report += f"Error during statistical test on `{col}`: {e}\n\n"


    report += "## Summary of Results\n\n"
    report += "| Variable | Normality Test | Skewness | Kurtosis | Recommended Standardization |\n"
    report += "|----------|----------------|----------|----------|----------------------------|\n"
    for result in results_summary:
        report += f"| `{result['Variable']}` | {result['Normality Test']} | {result['Skewness']} | {result['Kurtosis']} | {result['Recommended Standardization']} |\n"

    save_analysis_to_markdown(output_file, report)                            # Save analysis report to markdown file

    with open(json_output_file, 'w', encoding="utf-8") as json_file:          # Save analysis results to json file
        json.dump(results_summary, json_file, indent=4)


def statistical_tests():
    """ Main processing pipeline for normalize and split data """
    if 'features' not in st.session_state.get('dataframes', {}):
        features = pd.read_parquet('data/features/features.parquet', engine='pyarrow')
    else:
        features = st.session_state['dataframes']['features']

    analyse_features(features)