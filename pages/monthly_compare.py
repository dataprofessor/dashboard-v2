"""Comapre monthly data in a customized way"""

import streamlit as st
import pandas as pd

from pages.helper.query import Queries

from login import check_local_token, login
from request import vasahm_query
from slider import create_range_slider
from menu import add_menu


st.set_page_config(layout='wide',
                   page_title="وسهم - بررسی جامع گزارشهای ماهانه",
                    page_icon="./assets/favicon.ico",
                    initial_sidebar_state='expanded')

with open( "style.css", encoding='UTF-8') as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
add_menu()


st.sidebar.header(f'Vasahm DashBoard `{st.session_state.ver}`')

check_local_token()
if "token" not in st.session_state:
    login()
else:
    queries = Queries()
    has_error, data = vasahm_query(queries.QUERY_MONTHLY_COMPARE)
    if has_error:
        st.error(data, icon="🚨")
    else:
        stock_data_history = pd.DataFrame(data).fillna(0.0)

        col1_slider = create_range_slider(stock_data_history,
                                          "col1_slider",
                                          "M/M ratio",
                                          "result")
        col2_slider = create_range_slider(stock_data_history,
                                          "col2_slider",
                                          "2M/2M ratio",
                                          "result2")
        col3_slider = create_range_slider(stock_data_history,
                                          "col3_slider",
                                          "3M/3M ratio",
                                          "result3")

        filtered_df = stock_data_history[stock_data_history['result'].astype(
            "float").between(col1_slider[0], col1_slider[1])]
        filtered_df1 = filtered_df[filtered_df['result2'].astype(
            "float").between(col2_slider[0], col2_slider[1])]
        filtered_df2 = filtered_df1[filtered_df1['result3'].astype(
            "float").between(col3_slider[0], col3_slider[1])]

        st.dataframe(filtered_df2, use_container_width=True, height=600,
                     column_config={
        "result": st.column_config.NumberColumn(
            "M/M",
            help="Month to Month sell",
            format="%.2f",
        ),
        "result2": st.column_config.NumberColumn(
            "2M/2M",
            help="two Month to two Month sell",
            format="%.2f",
        ),
        "result3": st.column_config.NumberColumn(
            "3M/3M",
            help="three Month to three Month sell",
            format="%.2f",
        )
        })
