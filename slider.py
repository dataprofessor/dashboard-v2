"""A helper for creating sliders"""

import datetime

import streamlit as st

def create_slider(df, key, title):
    """Creates a date slider"""
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

def create_range_slider(df, key, title, column):
    """Creates a range slider"""
    min_value  = df[column].astype(float).min()
    max_value  = df[column].astype(float).max()
    range_slider = st.sidebar.slider(
        title,
        min_value=min_value,
        max_value=max_value,
        value=[min_value, max_value],
        format="%.2f",
        step=0.01,
        key=key)
    return range_slider
