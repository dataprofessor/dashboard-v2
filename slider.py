import streamlit as st
import datetime

def create_slider(df, key, title):
    min_value  = df['date_column'].min()
    max_value  = df['date_column'].max()
    date_slider = st.sidebar.slider(
        title,
        min_value=min_value - datetime.timedelta(days=1),
        max_value=max_value + datetime.timedelta(days=1),
        value=[min_value, max_value],
        format="MM/DD/YY",
        key=key)
    return date_slider