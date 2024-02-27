"""Query Workbench."""

import streamlit as st
import pandas as pd

from request import vasahm_query, get_nonce, get_key
from menu import add_menu



st.set_page_config(layout='wide',
                   page_title="وسهم - میزکار، دسترسی آزاد اطلاعات",
                    page_icon="./assets/favicon.ico",
                    initial_sidebar_state='expanded')

# st.markdown(
#     """
#     <style>
#     #MainMenu {visibility: hidden;}
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# st.markdown(
#     """
#     <style>
#     .stDeployButton {
#             visibility: hidden;
#         }
#     </style>
#     """, unsafe_allow_html=True
# )
with open( "style.css", encoding="UTF-8") as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)


# st.sidebar.image(image="./assets/logo.png")
add_menu()
st.sidebar.header(f'Vasahm DashBoard `{st.session_state.ver}`')

def get_email_callback():
    """Send nonce to entered email."""
    has_error, message = get_nonce(st.session_state.email)
    if has_error:
        st.error(message, icon="🚨")
    else:
        submit_nonce = st.form("submit_nonce")
        submit_nonce.text_input('کد تایید خود را وارد کنید',
                                placeholder='XXXX',
                                key="nonce")
        submit_nonce.form_submit_button("ارسال", on_click = get_nonce_callback )

def get_nonce_callback():
    """Confirm nonce for login."""
    has_error, message = get_key(st.session_state.email, st.session_state.nonce)
    if has_error:
        st.error(message, icon="🚨")
        del st.session_state["nonce"]
    else:
        st.session_state["token"] = message


if "token" not in st .session_state:
    get_email = st.form("get_email")
    email = get_email.text_input('ایمیل خود را وارد کنید',
                                 placeholder='example@mail.com',
                                 key="email")
    # Every form must have a submit button.
    submitted = get_email.form_submit_button("دریافت کد", on_click = get_email_callback )
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
