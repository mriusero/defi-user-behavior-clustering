import streamlit as st
import pandas as pd

from src.backend.ml.processing.distribution_analysis import statistical_tests

def page_3():
    st.markdown('<div class="header">#3 Statistics_</div>', unsafe_allow_html=True)

    st.write("""
> Before perform statistical test, features engineering have to be done first.
---
The code implements a data analysis and standardization process in Python, utilizing several statistical tests and transformations to normalize the dataset. Below is an explanation of the logic of testing and standardization carried out:

### 1. **Normality Test (Shapiro-Wilk Test)**
   - For each numeric column, the function performs a normality test using the `normaltest` from the `scipy.stats` package. 
   - If the sample size is greater than 7, the p-value from the test is used to determine whether the data is normally distributed:
     - **Normal**: p-value ≥ 0.05
     - **Not-normal**: p-value < 0.05

### 2. **Skewness and Kurtosis**
   - The skewness of the data is calculated using the `skew` function, and kurtosis is calculated using the `kurtosis` function.
   - The descriptions of skewness are:
     - **Symmetric**: Skew value between -0.5 and 0.5.
     - **Positively skewed**: Skew value > 0.
     - **Negatively skewed**: Skew value < 0.
   - The descriptions of kurtosis are:
     - **Mesokurtic (Normal)**: Kurtosis value between 2.5 and 3.5.
     - **Leptokurtic**: Kurtosis value > 3.5.
     - **Platykurtic**: Kurtosis value < 2.5.

### 3. **Standardization Method Decision**
   - Based on the normality, skewness, and kurtosis results, the following standardization methods are applied to each numeric column:
     - **Z-score**: Applied to normal distributions.
     - **Min-Max**: Applied to data with low skewness and low kurtosis.
     - **Log Transformation**: Applied to columns with strong positive skewness (if all values are greater than 0).
     - **Log Inverse**: Applied to columns with strong negative skewness (if all values are greater than 0).
     - **Box-Cox Transformation**: Applied when the skewness is high or the data has high kurtosis and non-positive values are present.
     - **None**: No transformation is applied if no standardization is needed.

### 4. **Standardization Function**
   - It applies the corresponding transformation to each column in the dataset:
     - **Z-score**: Subtracts the mean and divides by the standard deviation.
     - **Min-Max**: Scales the data to a [0, 1] range.
     - **Log**: Applies the natural logarithm transformation (with the addition of 1 to avoid log(0)).
     - **Log Inverse**: Applies the natural logarithm transformation to the negative values.
     - **Box-Cox**: Applies the Box-Cox transformation to the column data.
---
    """)
    if st.button("Run Statistical Tests"):
        df_std = statistical_tests()
        st.write("#### Standardized Data")
        st.write(df_std.head(15))
        st.write(df_std.describe())

    st.write("#### Before Standardisation")
    st.write(pd.read_csv("config/to_standardize.csv"))

    st.write("#### After Standardisation")
    st.write(pd.read_csv("config/standardized.csv").drop(columns=["Standardization"]))
