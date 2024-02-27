"""Comapre monthly data in a customized way"""

import streamlit as st
import pandas as pd
import altair as alt


from request import get_stock_monthly
# from slider import create_range_slider
from menu import add_menu



st.set_page_config(layout='wide',
                   page_title="وسهم - نمودار ماهانه",
                    page_icon="./assets/favicon.ico",
                    initial_sidebar_state='collapsed')

with open( "style.css", encoding='UTF-8') as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
add_menu()


# st.sidebar.image(image="./assets/logo.png")
if "ver" in st.session_state:
    st.sidebar.header(f'Vasahm DashBoard `{st.session_state.ver}`')

df = pd.read_csv("data.csv").dropna()
list_of_name = df['name'].to_list()
if "stock" in st.query_params:
    STOCK_INDEX = list_of_name.index(st.query_params.stock)
else:
    STOCK_INDEX = 0

name = st.selectbox("لیست سهام", options = list_of_name, index=STOCK_INDEX)

dfg = get_stock_monthly(name)

stock_data_history = pd.DataFrame(dfg[name], columns=["period",
          "value"])

chart = alt.Chart(stock_data_history).mark_bar().encode(
                alt.Y('value:Q', title="مبلغ (میلیون ریال)"),
                alt.X('period:N',title="تاریخ")
            )
st.altair_chart(chart, use_container_width=True)
