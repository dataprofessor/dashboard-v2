"""Module provide monte Carlo charts."""
import math

import streamlit as st
import pandas as pd
import altair as alt

import numpy as np

from scipy.stats import norm

from request import index_price_history,index_price_history2
from menu import add_menu

st.set_page_config(layout='wide',
                   page_title="وسهم - تحلیل احتمالاتی ( مونته کارلو)",
                    page_icon="./assets/favicon.ico",
                    initial_sidebar_state='expanded')

with open( "style.css", encoding='UTF-8') as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
add_menu()

# st.sidebar.image(image="./assets/logo.png")
if "ver" in st.session_state:
    st.sidebar.header(f'Vasahm DashBoard `{st.session_state.ver}`')

def probs_find(predicted, less_than, on = 'value'):
    "find predictions"
    if on == 'return':
        predicted0 = predicted.iloc[0,0]
        predicted = predicted.iloc[-1]
        pred_list = list(predicted)
        over = [(i*100)/predicted0 for i in pred_list if ((i-predicted0
                                                           )*100)/predicted0 >= less_than]
        less = [(i*100)/predicted0 for i in pred_list if ((i-predicted0
                                                           )*100)/predicted0 < less_than]
    elif on == 'value':
        predicted = predicted.iloc[-1]
        pred_list = list(predicted)
        over = [i for i in pred_list if i >= less_than]
        less = [i for i in pred_list if i < less_than]
    else:
        print("'on' must be either value or return")
    return (len(less)/(len(over)+len(less)))
# Example use (probability our investment will return
# at least 20% over the days specified in our prediction
# probs_find(predicted, 0.2, on = 'return')

name = st.sidebar.selectbox("لیست شاخصها", options = ["شاخص کل",
                                                      "طلا",
                                                      "شاخص هموزن",
                                                      "زعفران (نهال)"])
data = None
if name == "طلا":
    data = index_price_history(46700660505281786, name)
elif name == 'زعفران (نهال)':
    data = index_price_history(12913156843322499, name)
elif name == 'شاخص هموزن':
    data = index_price_history2(67130298613737946, name)
elif name == 'شاخص کل':
    data = index_price_history2(32097828799138957, name)


if data is not None:
    data.rename(columns={'datetime': 'date',
                    name: 'close'}, inplace=True)
    data.set_index('date', inplace=True)

    log_returns = pd.DataFrame(np.log(1 + data["close"].pct_change()))
    log_returns.fillna(0, inplace=True)

    u = log_returns.mean()['close']
    var = log_returns.var()['close']
    drift = u - (0.5*var)

    stdev = log_returns.std()['close']
    DAYS = 150
    TRIALS = 100000
    z = norm.ppf(np.random.rand(DAYS, TRIALS)) #DAYS, TRIALS
    daily_returns = np.exp(drift + stdev * z)

    price_paths = np.zeros_like(daily_returns)
    price_paths[0] = data["close"].iloc[-1]
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
    col2.metric("مقدار مورد انتظار", f"{format(
        round(pd.DataFrame(price_paths).iloc[-1].mean(),2), '.2f')}")
    col3.metric("میانگین بازدهی سناریوها", f"{format(
        (round(100*(pd.DataFrame(
            price_paths).iloc[-1].mean()-price_paths[0,1])/pd.DataFrame(
                price_paths).iloc[-1].mean(),2)), '.2f')}")
    col4.metric("احتمال ریزش 10 درصدی", f"{format(round(
        100*probs_find(pd.DataFrame(price_paths),0.9*data["close"].iloc[-1], on='value')), '.2f')}")


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
