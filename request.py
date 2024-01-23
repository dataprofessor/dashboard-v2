import requests
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

authtoken = os.getenv('authtoken')


@st.cache_data
def areon_query(queryString):
    url = 'https://back.vasahm.com/user/runQuery'
    myobj = {'queryString': queryString}
    header = {
        "accept": "*/*",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,fa;q=0.7",
        "authtoken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7IkVtYWlsIjoibW9oc2VuYmFyZWthdGlAZ21haWwuY29tIiwiaWQiOjJ9LCJpYXQiOjE3MDU5OTIwMTQsImV4cCI6MTcwNjA3ODQxNH0.VAPqwRdxppc61npNWsBQtgBJLKDyJA_W4PXwDx5rZzo",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "pragma": "no-cache",
        "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Microsoft Edge\";v=\"120\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }
    x = requests.post(url, json = myobj, headers=header).json()
    return x["data"]["result"]


