"""Module provide monte Carlo charts."""

import streamlit as st
import pandas as pd
import altair as alt
from streamlit_local_storage import LocalStorage


from request import is_authenticate, vasahm_query, get_nonce
from request import get_key, index_price_history, index_price_history2

from menu import add_menu

import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

st.set_page_config(layout='wide',
                   page_title="وسهم - تحلیل احتمالاتی (مونته کارلو)",
                    page_icon="./assets/favicon.ico",
                    initial_sidebar_state='expanded')
sessionBrowserS = LocalStorage()


with open("style.css", encoding="utf-8") as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
add_menu()



list_of_name = ["شاخص کل", "شاخص همزون", "طلا"]
# st.sidebar.image(image="./assets/logo.png")
def del_porto_submition_variable():
    """Deletes portfolio_analyzer form that let user to
    fill a new form again."""
    del st.session_state.porto_submition
    if "portfolio_analyzer" in locals():
        del portfolio_analyzer

def probs_find(predicted, higherthan, on = 'value'):
    if on == 'return':
        predicted0 = predicted.iloc[0,0]
        predicted = predicted.iloc[-1]
        predList = list(predicted)
        over = [(i*100)/predicted0 for i in predList if ((i-predicted0)*100)/predicted0 >= higherthan]
        less = [(i*100)/predicted0 for i in predList if ((i-predicted0)*100)/predicted0 < higherthan]
    elif on == 'value':
        predicted = predicted.iloc[-1]
        predList = list(predicted)
        over = [i for i in predList if i >= higherthan]
        less = [i for i in predList if i < higherthan]
    else:
        print("'on' must be either value or return")
    return (len(over)/(len(over)+len(less)))
#Example use (probability our investment will return at least 20% over the days specified in our prediction
#probs_find(predicted, 0.2, on = 'return')


st.sidebar.header(f'Vasahm DashBoard `{st.session_state.ver}`')

def add_submit_state():
    """Create st.session_state['porto_submition'] that help logic
    whether user submit his portfolio or not."""
    st.session_state["porto_submition"] = True

def create_query_string():
    """Create a query string for retrieving all portfolio prices."""
    temp_str = ""
    for _ in range(st.session_state.portfo_number):
        stock_name_i = f"stock_name_{_}"
        temp_str = temp_str + f"stocks.name = '{st.session_state[stock_name_i]}' OR "
    return temp_str[:-4]

def create_form():
    """Create a form that let user enter his portfolio."""
    portfolio_analyzer = st.form("portfolio_analyzer")

    cols2 = portfolio_analyzer.columns(2, gap="small")
    cols2[0].text_input('تاریخ شروع', placeholder='14010130', key="portfolio_month_start")
    cols2[1].text_input('تاریخ پایان', placeholder='14010130', key="portfolio_month_finish")
    cols = portfolio_analyzer.columns(2, gap="small")
    for _ in range(st.session_state.portfo_number):
        cols[0].selectbox("لیست سهام", options = list_of_name, key=f"stock_name_{_}")
        cols[1].number_input('سهم از کل پورتفو (درصد)',
                             min_value=1,
                             max_value=100,
                             step=1,
                             placeholder='20',
                             key=f"stock_percent_{_}"
                             )
    portfolio_analyzer.multiselect(
    'شاخصهای مورد نظر خود برای مقایسه را انتخاب کنید',
    ['شاخص کل', 'شاخص همزون', 'طلا', 'زعفران (نهال)'],
    ['شاخص کل'], key="indexes")
    portfolio_analyzer.form_submit_button("بررسی عملکرد سبد", on_click=add_submit_state)

def get_email_callback():
    """Send nonce to entered email."""
    has_error, message = get_nonce(st.session_state.email)
    if has_error:
        st.error(message, icon="🚨")
    else:
        submit_nonce = st.form("submit_nonce")
        submit_nonce.text_input('کد تایید خود را وارد کنید', placeholder='XXXX', key="nonce")
        submit_nonce.form_submit_button("ارسال", on_click = get_nonce_callback )

def get_nonce_callback():
    """Confirm nonce for login."""
    has_error, message = get_key(st.session_state.email, st.session_state.nonce)
    if has_error:
        st.error(message, icon="🚨")
        del st.session_state["nonce"]
    else:
        st.session_state["token"] = message
        sessionBrowserS.setItem("saved_token", message)

sessionBrowserS.getItem("saved_token", key='temp1')
if st.session_state.temp1 is not None:
    if "storage" in st.session_state.temp1:
        if st.session_state.temp1['storage'] is not None:
            saved_token = st.session_state.temp1['storage']['value']
            if is_authenticate(saved_token):
                st.session_state["token"] = saved_token
            else:
                sessionBrowserS.deleteItem("saved_token")

if "token" not in st .session_state:
    get_email = st.form("get_email")
    email = get_email.text_input('ایمیل خود را وارد کنید',
                                 placeholder='example@mail.com',
                                 key="email")
    submitted = get_email.form_submit_button("دریافت کد", on_click = get_email_callback )
else:
    name = st.sidebar.selectbox("لیست شاخصها", options = list_of_name)

    requestedURL = "http://cdn.tsetmc.com/api/Index/GetIndexB2History/32097828799138957"

    header = {"User-Agent": "PostmanRuntime/7.29.0"}

    s = requests.Session()
    isfahan = s.get(requestedURL, headers=header, timeout= 10)
    data = isfahan.json()["indexB2"]

    # total index
    df = pd.DataFrame(data)
    df['open'] = df['xNivInuClMresIbs'].shift(1)
    df.at[0, 'open'] = 0
    df.drop("insCode", axis=1, inplace=True)
    df.rename(columns={'dEven': 'date', 'xNivInuClMresIbs': 'close', 'xNivInuPbMresIbs': 'low', 'xNivInuPhMresIbs': 'high'}, inplace=True)
    df.set_index('date', inplace=True)


    log_returns = np.log(1 + df["close"].pct_change())

    u = log_returns.mean()
    var = log_returns.var()
    drift = u - (0.5*var)

    stdev = log_returns.std()
    days = 150
    trials = 1000000
    z = norm.ppf(np.random.rand(days, trials)) #days, trials
    daily_returns = np.exp(drift + stdev * z)

    price_paths = np.zeros_like(daily_returns)
    price_paths[0] = df["close"].iloc[-1]
    for t in range(1, days):
        price_paths[t] = price_paths[t-1]*daily_returns[t]

    x = pd.DataFrame(price_paths).iloc[-1]
    fig, ax = plt.subplots(1,2, figsize=(14,4))
    selector = alt.selection_single(encodings=['x', 'color'])

    chart_product = alt.Chart(x).mark_bar().encode(
        alt.Color('rowTitle:N', title="سرفصلها"),
        alt.Y('sum(value):Q', title="تعداد"),
        alt.X('endToPeriod:N',title="تاریخ")
    )
    st.altair_chart(chart_product, use_container_width=True)
    sns.histplot(x, ax=ax[0])
    sns.histplot(x, cumulative=True,ax=ax[1])
    plt.xlabel("Stock Price")
    plt.show()

    print("index")
    print(f"Days: {days-1}")
    print(f"Expected Value: ${round(pd.DataFrame(price_paths).iloc[-1].mean(),2)}")
    print(f"Return: {round(100*(pd.DataFrame(price_paths).iloc[-1].mean()-price_paths[0,1])/pd.DataFrame(price_paths).iloc[-1].mean(),2)}%")
    print(f"Probability of Breakeven: {round(100*probs_find(pd.DataFrame(price_paths),1936771, on='value'))}%")
