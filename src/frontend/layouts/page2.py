import pandas as pd
import streamlit as st

from src.backend.ml.features.preprocessing import implement_features

def page_2():
    st.markdown(
        '<div class="header">#2 Feature Engineering_</div>', unsafe_allow_html=True
    )

    if st.button("Launch feature engineering"):
        implement_features()

    if st.session_state.get('features') is None:
        features = pd.read_parquet('data/features.parquet', engine='pyarrow')
        st.session_state['features'] = features

    features = st.session_state['features']

    train_df = features['train']

    col1, col2 = st.columns([1, 2])
    with col1:
        st.write('Train set columns:', train_df.columns.tolist())
    with col2:
        st.write('Train set :', train_df.sample(10000))
        st.write('Train set description :', train_df.describe())