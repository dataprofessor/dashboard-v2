"""handle logining of a user in vasahm"""

import streamlit as st
from streamlit_local_storage import LocalStorage


from request import is_authenticate, get_nonce, get_key


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
    local_storage = LocalStorage()
    has_error, message = get_key(st.session_state.email, st.session_state.nonce)
    if has_error:
        st.error(message, icon="🚨")
        del st.session_state["nonce"]
    else:
        st.session_state["token"] = message
        local_storage.setItem("saved_token", message)

def check_local_token():
    """check user login is in local storage or not"""
    local_storage = LocalStorage()
    local_storage.getItem("saved_token", key='temp1')
    if st.session_state.temp1 is not None:
        if "storage" in st.session_state.temp1:
            if st.session_state.temp1['storage'] is not None:
                saved_token = st.session_state.temp1['storage']['value']
                if is_authenticate(saved_token):
                    st.session_state["token"] = saved_token
                else:
                    local_storage.deleteItem("saved_token")

def login():
    """start login process of a user"""
    get_email = st.form("get_email")
    get_email.text_input('ایمیل خود را وارد کنید',
                                 placeholder='example@mail.com',
                                 key="email")
    # Every form must have a submit button.
    get_email.form_submit_button("دریافت کد", on_click = get_email_callback )
