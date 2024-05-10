from datetime import datetime
import requests
import json
import pandas as pd
from funds.helper.helper import persianNumberToEnglish

class Fund():
    def __init__(self, name, fund_address, code, metrics):
        self.name = name
        self.fund_address = fund_address
        self.code = code
        self.update_fund_data()
        self.update_closing_price()
        self.metric = metrics

    def update_fund_data(self):
        response = requests.get(self.fund_address+"/Fund/GetLeveragedNAV", timeout=60)
        json_object = json.loads(response.text)
        json_object = json.loads(json_object)

        self.BaseUnitsCancelNAV = persianNumberToEnglish(json_object["BaseUnitsCancelNAV"])
        self.BaseUnitsTotalNetAssetValue = persianNumberToEnglish(json_object["BaseUnitsTotalNetAssetValue"])
        self.BaseUnitsTotalSubscription = persianNumberToEnglish(json_object["BaseUnitsTotalSubscription"])
        self.SuperUnitsCancelNAV = persianNumberToEnglish(json_object["SuperUnitsCancelNAV"])
        self.SuperUnitsSubscriptionNAV = persianNumberToEnglish(json_object["SuperUnitsSubscriptionNAV"])
        self.SuperUnitsTotalSubscription = persianNumberToEnglish(json_object["SuperUnitsTotalSubscription"])
        self.SuperUnitsTotalNetAssetValue = persianNumberToEnglish(json_object["SuperUnitsTotalNetAssetValue"])

        response = requests.get(self.fund_address+"/Chart/AssetCompositions?type=getnavtotal", timeout=60)
        json_object = json.loads(response.text)
        self.CashAsset = 0
        for x in json_object['List']:
            if x["x"] == 'اوراق مشارکت' or x["x"] == 'نقد و بانک (سپرده)':
                self.CashAsset = self.CashAsset + x["y"]/100
        self.Asset = 1 - self.CashAsset
        
        response = requests.get(self.fund_address+"/Chart/TotalNAV?type=getnavtotal", timeout=60)
        json_object = json.loads(response.text)
        self.performance = []
        self.performance.append((json_object[2]['List'][6]["y"]-json_object[2]['List'][0]["y"])/json_object[2]['List'][0]["y"])
        self.performance.append((json_object[2]['List'][22]["y"]-json_object[2]['List'][0]["y"])/json_object[2]['List'][0]["y"])
        self.performance.append((json_object[2]['List'][66]["y"]-json_object[2]['List'][0]["y"])/json_object[2]['List'][0]["y"])
    def update_closing_price(self):

        url = "https://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceInfo/{}".format(self.code)
        header = {"User-Agent": "PostmanRuntime/7.29.0"}
        response = requests.get(url, headers=header, timeout=60).json()
        self.pClosing = response["closingPriceInfo"]["pClosing"]
        self.last = response["closingPriceInfo"]["pDrCotVal"]

    def get_price_history(self):
        url = "https://cdn.tsetmc.com/api/ClosingPrice/GetChartData/{}/D".format(self.code)
        header = {"User-Agent": "PostmanRuntime/7.29.0"}
        response = requests.get(url, headers=header, timeout=60).json()
        shiraz = pd.json_normalize(response['closingPriceChartData'])
        shiraz['datetime'] = pd.to_datetime(shiraz["dEven"]+19603987200, unit='s').dt.strftime("%Y%m%d").astype(int)
        self.history = shiraz

    def sharpe_ratio(self):
        return self.metric.sharpe_ratio(self)
    def sortino_ratio(self):
        return self.metric.sortino_ratio(self)
    def alpha(self, benchmark):
        return self.metric.alpha(self, benchmark)
    def r_squared(self, benchmark):
        return self.metric.r_squared(self, benchmark)
    def treynor_ratio(self, risk_free_rate):
        return self.metric.treynor_ratio(self, risk_free_rate)
    def jensens_alpha(self, benchmark):
        return self.metric.jensens_alpha(self, benchmark)
    def capture_ratio(self, benchmark):
        return self.metric.capture_ratio(self, benchmark)
    def drawdown_analysis(self):
        return self.metric.drawdown_analysis(self)

