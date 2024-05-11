"""index class use for calculating index parameters"""
import requests
# import json
import pandas as pd
# from helper.helper import persianNumberToEnglish

class Index():
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.history = self._get_price_history()

    def _get_price_history(self):
        url = f"https://cdn.tsetmc.com/api/Index/GetIndexB2History/{self.code}"
        header = {"User-Agent": "PostmanRuntime/7.29.0"}
        response = requests.get(url, headers=header, timeout=60).json()
        return pd.json_normalize(response['indexB2'])
