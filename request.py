"""A helper for requesting different data"""

import configparser
import requests

import streamlit as st
import pandas as pd

config = configparser.ConfigParser()
config.read('config.ini')

@st.cache_data(ttl=int(config["server"]["cache_time"]))
def vasahm_query(query_string):
    """Query query_string on database and retrieve the results."""
    url = 'https://back.vasahm.com/user/runQuery'
    myobj = {'queryString': query_string}
    headers = {
        "accept": "*/*",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,fa;q=0.7",
        "authtoken": st.session_state.token,
        "content-type": "application/json",
        "sec-ch-ua": "\"Not_A Brand\";v=\"8\",\"Chromium\";v=\"120\", \"Microsoft Edge\";v=\"120\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }
    x = requests.post(url, json = myobj, headers=headers, timeout=60)
    if x.status_code != 200:
        return False, False
    else:
        x=x.json()
        if x["hasError"]:
            return x["hasError"], x["error"]
        else:
            return x["hasError"], x["data"]["result"]

def get_nonce(email):
    """get nonce to entered email."""
    url = "https://back.vasahm.com/user/getNonce"
    myobj = {'Email': email}

    x = requests.post(url, json = myobj, timeout=60).json()
    if x["hasError"]:
        return x["hasError"], x["error"]["message"]
    else:
        return x["hasError"], x["message"]

def get_key(email, nonce):
    """Confirm nonce for login."""
    url = "https://back.vasahm.com/user/login"
    myobj = {'Email': email, "Nonce": nonce}
    x = requests.post(url, json = myobj, timeout=60).json()
    if x["hasError"]:
        return x["hasError"], x["error"]["message"]
    else:
        return x["hasError"], x["data"]["Token"]

def is_authenticate(saved_token):
    """Query query_string on database and retrieve the results."""
    url = 'https://back.vasahm.com/user/getUserInfo'
    headers = {
        "accept": "*/*",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,fa;q=0.7",
        "authtoken": saved_token,
        "content-type": "application/json",
        "sec-ch-ua": "\"Not_A Brand\";v=\"8\",\"Chromium\";v=\"120\", \"Microsoft Edge\";v=\"120\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }
    x = requests.get(url, headers=headers, timeout=60)
    if x.status_code != 200:
        return False
    else:
        x=x.json()
        if x["hasError"]:
            return False
        else:
            return True

def index_price_history(ins_code, name):
    """Get history price of a tehran exchange Fund."""
    url = f"https://cdn.tsetmc.com/api/ClosingPrice/GetChartData/{ins_code}/D"
    header = {"User-Agent": "PostmanRuntime/7.29.0"}
    response = requests.get(url, headers=header, timeout=60).json()
    shiraz = pd.json_normalize(response['closingPriceChartData'])
    shiraz['datetime'] = pd.to_datetime(
        shiraz["dEven"]+19603987200, unit='s'
        ).dt.strftime("%Y%m%d").astype(str)
    shiraz = shiraz.rename(columns={'pDrCotVal': name})
    return shiraz[["datetime", name]]

def index_price_history2(ins_code, name):
    """Get history price of a tehran exchange index."""
    url = f"https://cdn.tsetmc.com/api/Index/GetIndexB2History/{ins_code}"
    header = {"User-Agent": "PostmanRuntime/7.29.0"}
    response = requests.get(url, headers=header, timeout=60).json()
    shiraz = pd.json_normalize(response['indexB2']).rename(
        columns={'dEven': 'datetime', 'xNivInuClMresIbs': name})
    shiraz['datetime'] = shiraz['datetime'].astype(str)
    return shiraz[["datetime", name]]


def get_stock_monthly(stock_name):
    """Get history monthly data for free users."""
    url = f"https://api.vasahm.ir/api/monthlyChart/{stock_name}"
    response = requests.get(url, timeout=60).json()
    return response
