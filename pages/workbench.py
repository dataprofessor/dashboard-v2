"""Query Workbench."""

import streamlit as st
import pandas as pd

from login import check_local_token, login
from request import vasahm_query
from menu import add_menu



st.set_page_config(layout='wide',
                   page_title="وسهم - میزکار، دسترسی آزاد اطلاعات",
                    page_icon="./assets/favicon.ico",
                    initial_sidebar_state='expanded')

with open( "style.css", encoding="UTF-8") as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)


add_menu()
st.sidebar.header(f'Vasahm DashBoard `{st.session_state.ver}`')

check_local_token()
if "token" not in st.session_state:
    login()
else:

    txt = st.text_area(
        "Text to analyze",
        """SELECT * FROM stocks""",
        key = "query_text",
        height=400,
    )
    print(txt)
    if st.button("Query", type="primary", disabled=False, use_container_width=True):
        has_error, data = vasahm_query(txt)
        if has_error:
            st.error(data, icon="🚨")
        else:
            stock_data_history = pd.DataFrame(data)
            st.dataframe(data, use_container_width=True)
