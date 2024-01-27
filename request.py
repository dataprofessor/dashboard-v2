import requests
import streamlit as st


@st.cache_data(ttl=600)
def vasahm_query(queryString):
    url = 'https://back.vasahm.com/user/runQuery'
    myobj = {'queryString': queryString}
    headers = {
        "accept": "*/*",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,fa;q=0.7",
        "authtoken": st.session_state.token,
        "content-type": "application/json",
        "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Microsoft Edge\";v=\"120\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }
    x = requests.post(url, json = myobj, headers=headers).json()
    if x["hasError"]:
        x["hasError"], x["error"]["message"]
    else:
        return x["hasError"], x["data"]["result"]

def get_nonce(email):
    url = "https://back.vasahm.com/user/getNonce"
    myobj = {'Email': email}

    x = requests.post(url, json = myobj).json()
    if x["hasError"]:
        x["hasError"], x["error"]["message"]
    else:
        return x["hasError"], x["message"]

def get_key(email, nonce):
    url = "https://back.vasahm.com/user/login"
    myobj = {'Email': email, "Nonce": nonce}
    x = requests.post(url, json = myobj).json()
    if x["hasError"]:
        x["hasError"], x["error"]["message"]
    else:
        return x["hasError"], x["data"]["Token"]


