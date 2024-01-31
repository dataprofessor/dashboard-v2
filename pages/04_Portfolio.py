import requests

import streamlit as st
import pandas as pd
import plotly.express as px
import plost
from request import vasahm_query
from slider import create_slider
from request import get_nonce
from request import get_key
import altair as alt

st.session_state.ver = '0.1.2'

st.set_page_config(layout='wide',
                   page_title="Vasahm Dashboard",
                    page_icon="./assets/favicon.ico",
                    initial_sidebar_state='expanded')

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

def index_price_history(insCode):
    url = f"https://cdn.tsetmc.com/api/ClosingPrice/GetChartData/{insCode}/D"
    header = {"User-Agent": "PostmanRuntime/7.29.0"}
    response = requests.get(url, headers=header).json()
    shiraz = pd.json_normalize(response['closingPriceChartData'])
    shiraz['datetime'] = pd.to_datetime(shiraz["dEven"]+19603987200, unit='s').dt.strftime("%Y%m%d").astype(int)
    return shiraz

def index_price_history2(insCode):
    url = f"https://cdn.tsetmc.com/api/Index/GetIndexB2History/{insCode}"
    header = {"User-Agent": "PostmanRuntime/7.29.0"}
    response = requests.get(url, headers=header).json()
    return pd.json_normalize(response['indexB2'])


df = pd.read_csv("data.csv").dropna()
list_of_name = df['name'].to_list()
# st.sidebar.image(image="./assets/logo.png")
def del_porto_submition_variable():
    del st.session_state.porto_submition
    if "portfolio_analyzer" in locals():
        del portfolio_analyzer

st.sidebar.header(f'Vasahm DashBoard `{st.session_state.ver}`')
 
def add_submit_state():
    st.session_state["porto_submition"] = True

def create_query_String():
    string = ""
    for i in range(st.session_state.portfo_number - 1):
        stro = f"stock_name_{i}"
        string = string + f"stocks.name = '{st.session_state[stro]}' OR "
    stro = f"stock_name_{st.session_state.portfo_number - 1}"
    string = string + f"stocks.name = '{st.session_state[stro]}'"
    return string

def create_form():
    
    portfolio_analyzer = st.form("portfolio_analyzer")

    cols2 = portfolio_analyzer.columns(2, gap="small")
    cols2[0].text_input('تاریخ شروع', placeholder='14010130', key=f"portfolio_month_start")
    cols2[1].text_input('تاریخ شروع', placeholder='14010130', key=f"portfolio_month_finish")
    cols = portfolio_analyzer.columns(3, gap="small")
    for i in range(st.session_state.portfo_number):
      cols[0].selectbox("لیست سهام", options = list_of_name, key=f"stock_name_{i}")
      cols[1].text_input('قیمت خرید', placeholder='12345', key=f"stock_number_{i}")
      cols[2].text_input('سهم از کل پورتفو (درصد)', placeholder='20', key=f"stock_percent_{i}")
    # Every form must have a submit button.
    options = portfolio_analyzer.multiselect(
    'شاخصهای مورد نظر خود برای مقایسه را انتخاب کنید',
    ['شاخص کل', 'شاخص همزون', 'طلا', 'زعفران (نهال)'],
    ['شاخص کل'], key="indexes")
    portfolio_analyzer.form_submit_button("بررسی عملکرد سبد", on_click=add_submit_state)

def get_email_callback():
    hasError, message = get_nonce(st.session_state.email)
    if hasError:
        st.error(message, icon="🚨")
    else:
        submit_nonce = st.form("submit_nonce")
        nonce = submit_nonce.text_input('کد تایید خود را وارد کنید', placeholder='XXXX', key="nonce")
        submitted = submit_nonce.form_submit_button("ارسال", on_click = get_nonce_callback )

def get_nonce_callback():
    hasError, message = get_key(st.session_state.email, st.session_state.nonce)
    if hasError:
        st.error(message, icon="🚨")
        del st.session_state["nonce"]
    else:
        st.session_state["token"] = message


if "token" not in st .session_state:
    get_email = st.form("get_email")
    email = get_email.text_input('ایمیل خود را وارد کنید', placeholder='example@mail.com', key="email")
    # Every form must have a submit button.
    submitted = get_email.form_submit_button("دریافت کد", on_click = get_email_callback )
else:

    if "porto_submition" not in st.session_state:
        st.number_input('تعداد سهام موجود در سبد خود را وارد کنید',
                        min_value=1,
                        max_value=10,
                        on_change=create_form,
                        value=1,
                        key="portfo_number")
    else:
        st.button("ثبت مجدد سبد سرمایه گذاری",
                  key="resubmmition_portfo",
                  help=None,
                  on_click=del_porto_submition_variable,
                  args=None,
                  kwargs=None,
                  type="secondary",
                  disabled=False,
                  use_container_width=True)
        string = create_query_String()
        st.write(st.session_state.stock_name_1)
        i = 1
        stro = f"stock_name_{i}"
        st.write(stro)
        st.write(st.session_state[stro])
        queryString = f"""
        SELECT stocks.name as name, "tradeDate", "lastAdjPrice"
        FROM public."stockPrice"
        INNER JOIN stocks ON "stockPrice".stock_id = stocks.id
        where 
        ({string})
        and "tradeDate" > '{st.session_state.portfolio_month_start}'
        and "tradeDate" < '{st.session_state.portfolio_month_finish}'
        order by "tradeDate";"""
        st.write(queryString)
        error, stock_data = vasahm_query(queryString)
        if error:
            st.error(stock_data, icon="🚨")
        else:
            stock_data_history = pd.DataFrame(stock_data, columns=["name",
                "tradeDate",
                "lastAdjPrice"])
            # st.dataframe(stock_data_history)
            pivot_df = stock_data_history.pivot_table(index='tradeDate',
                                                    columns='name',
                                                    values='lastAdjPrice',
                                                    aggfunc='sum').reset_index()
            pivot_df.fillna(method='ffill')
            ind = {}
            for i in st.session_state.indexes:
                if i == "طلا":
                    ind["tala"] = index_price_history(46700660505281786)
                elif i == 'زعفران (نهال)':
                    ind["nahal"] = index_price_history(12913156843322499)
                elif i == 'شاخص همزون':
                    ind["kol"] = index_price_history2(67130298613737946)
                elif i == 'شاخص کل':
                    ind["ham"] = index_price_history2(32097828799138957)
            st.dataframe(pivot_df)


