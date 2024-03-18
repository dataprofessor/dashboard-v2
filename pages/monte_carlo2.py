"""Module provide monte Carlo charts."""
import math

import streamlit as st
import pandas as pd
import altair as alt

import requests
import numpy as np

from scipy.stats import norm

# from menu import add_menu



st.set_page_config(layout='wide',
                   page_title="وسهم - نمودار ماهانه",
                    page_icon="./assets/favicon.ico",
                    initial_sidebar_state='collapsed')

with open( "style.css", encoding='UTF-8') as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
# add_menu()

# st.sidebar.image(image="./assets/logo.png")
if "ver" in st.session_state:
    st.sidebar.header(f'Vasahm DashBoard `{st.session_state.ver}`')

def probs_find(predicted, higherthan, on = 'value'):
    "find predictions"
    if on == 'return':
        predicted0 = predicted.iloc[0,0]
        predicted = predicted.iloc[-1]
        pred_list = list(predicted)
        over = [(i*100)/predicted0 for i in pred_list if ((i-predicted0
                                                           )*100)/predicted0 >= higherthan]
        less = [(i*100)/predicted0 for i in pred_list if ((i-predicted0
                                                           )*100)/predicted0 < higherthan]
    elif on == 'value':
        predicted = predicted.iloc[-1]
        pred_list = list(predicted)
        over = [i for i in pred_list if i >= higherthan]
        less = [i for i in pred_list if i < higherthan]
    else:
        print("'on' must be either value or return")
    return (len(over)/(len(over)+len(less)))
#Example use (probability our investment will return at least 20% over the days specified in our prediction
#probs_find(predicted, 0.2, on = 'return')

name = st.sidebar.selectbox("لیست شاخصها", options = ["شاخص کل", "طلا"])
if name == "شاخص کل":
    URL = "http://cdn.tsetmc.com/api/Index/GetIndexB2History/32097828799138957"
    header = {"User-Agent": "PostmanRuntime/7.29.0"}
    s = requests.Session()
    isfahan = s.get(URL, headers=header, timeout= 10)
    data = isfahan.json()["indexB2"]
else:
    pass

# total index
df = pd.DataFrame(data)
df['open'] = df['xNivInuClMresIbs'].shift(1)
df.at[0, 'open'] = 0
df.drop("insCode", axis=1, inplace=True)
df.rename(columns={'dEven': 'date',
                   'xNivInuClMresIbs': 'close',
                   'xNivInuPbMresIbs': 'low',
                   'xNivInuPhMresIbs': 'high'}, inplace=True)
df.set_index('date', inplace=True)


log_returns = pd.DataFrame(np.log(1 + df["close"].pct_change()))
log_returns.fillna(0, inplace=True)

u = log_returns.mean()['close']
var = log_returns.var()['close']
drift = u - (0.5*var)

stdev = log_returns.std()['close']
DAYS = 150
TRIALS = 10000
z = norm.ppf(np.random.rand(DAYS, TRIALS)) #DAYS, TRIALS
daily_returns = np.exp(drift + stdev * z)

price_paths = np.zeros_like(daily_returns)
price_paths[0] = df["close"].iloc[-1]
for t in range(1, DAYS):
    price_paths[t] = price_paths[t-1]*daily_returns[t]
cols = []
for index in range(TRIALS):
    cols.append("F"+str(index))                   #rename the column name based on index
x = pd.DataFrame(price_paths, columns = cols).iloc[-1]
xx = pd.DataFrame(x)
xx.rename(columns={149: 'forcasts'}, inplace=True)


col1, col2, col3, col4 = st.columns(4)
col1.metric("پیش بینی برای روز آینده", f"{DAYS}")
col2.metric("مقدار مورد انتظار", f"{format(round(pd.DataFrame(price_paths).iloc[-1].mean(),2), '.2f')}")
col3.metric("بازده", f"{format((round(100*(pd.DataFrame(price_paths).iloc[-1].mean()-price_paths[0,1]
                                         )/pd.DataFrame(price_paths
                                                        ).iloc[-1].mean(),2)), '.2f')}")
col4.metric("احتمال شکست", f"{format(round(
    100*probs_find(pd.DataFrame(price_paths),1936771, on='value')), '.2f')}")


chart = alt.Chart(log_returns.iloc[1:]).mark_bar().encode(
                alt.Y('count()', title="Frequency"),
                alt.X('close', bin=alt.Bin(step=0.001), title="Returns")
            )
st.altair_chart(chart, use_container_width=True)

s = 10**(int(math.log10(xx["forcasts"][0])) -3)

chart = alt.Chart(xx).mark_bar().encode(
                alt.Y('count()', title="Frequency"),
                alt.X('forcasts', bin=alt.Bin(step=s), title="Target")
            )
st.altair_chart(chart, use_container_width=True)

