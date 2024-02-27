"""Module providing a logic that let user understand his portfolio performance
in compare to other indexes or funds."""

import streamlit as st
import pandas as pd
import altair as alt

from request import vasahm_query, get_nonce, get_key, index_price_history, index_price_history2
from menu import add_menu


st.set_page_config(layout='wide',
                   page_title="وسهم - بررسی عملکرد پورتفو",
                    page_icon="./assets/favicon.ico",
                    initial_sidebar_state='expanded')

with open("style.css", encoding="utf-8") as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
add_menu()


df = pd.read_csv("data.csv").dropna()
list_of_name = df['name'].to_list()
# st.sidebar.image(image="./assets/logo.png")
def del_porto_submition_variable():
    """Deletes portfolio_analyzer form that let user to
    fill a new form again."""
    del st.session_state.porto_submition
    if "portfolio_analyzer" in locals():
        del portfolio_analyzer
html = """<!DOCTYPE html>
<html lang="fa" dir="rtl">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/fontsource-vazir-matin@2.0.0-alpha.8">
  <style>
    body {
      font-family: 'Vazir Matn', sans-serif;
      margin: 1px;
    }

    #content {
      max-width: 100%; /* Adjust this value based on your design */
      width: auto;
      display: inline-block;
    }
  </style>
</head>

<body>
  <div id="content">
    <p>میتوانید برای مشاوره از طریق <a href="https://t.me/milad_mousavi_trader" target="_blank">@milad_mousavi_trader</a>با ما در تماس باشید.</p>
  </div>
</body>

</html>
"""
st.components.v1.html(html, height=60, scrolling=False)

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


if "token" not in st .session_state:
    get_email = st.form("get_email")
    email = get_email.text_input('ایمیل خود را وارد کنید',
                                 placeholder='example@mail.com',
                                 key="email")
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
        string = create_query_string()
        queryString = f"""
        SELECT stocks.name as name, "tradeDate", "lastAdjPrice","tradeDateGre"
        FROM public."stockPrice"
        INNER JOIN stocks ON "stockPrice".stock_id = stocks.id
        where 
        ({string})
        and "tradeDate" > '{st.session_state.portfolio_month_start}'
        and "tradeDate" < '{st.session_state.portfolio_month_finish}'
        order by "tradeDate";"""

        error, stock_data = vasahm_query(queryString)
        if error:
            st.error(stock_data, icon="🚨")
        else:
            stock_data_history = pd.DataFrame(stock_data, columns=["name",
                "tradeDate",
                "lastAdjPrice",
                "tradeDateGre"])
            pivot_df = stock_data_history.pivot_table(index='tradeDateGre',
                                                    columns='name',
                                                    values='lastAdjPrice',
                                                    aggfunc='sum').reset_index()
            pivot_df['date'] = pd.to_datetime(pivot_df['tradeDateGre'], format="%Y-%m-%dT%H:%M:%S")
            pivot_df['datetime'] = pivot_df["date"].dt.strftime("%Y%m%d").astype(str)
            pivot_df = pivot_df.drop(columns=['date', 'tradeDateGre'])
            pivot_df.fillna(method='ffill', inplace=True)
            pivot_df['پورتفو'] = 0
            for i in range(st.session_state.portfo_number):
                stro = f"stock_name_{i}"
                stro1 = f"stock_percent_{i}"
                pivot_df['پورتفو'] = pivot_df['پورتفو'] + (
                    pivot_df[st.session_state[stro]].astype(int)*st.session_state[stro1]/100
                    )
                pivot_df = pivot_df.drop(columns=[st.session_state[stro]])
            ind = {}
            for i in st.session_state.indexes:
                if i == "طلا":
                    ind["طلا"] = index_price_history(46700660505281786, "طلا")
                    pivot_df = pivot_df.merge(ind["طلا"], how='left',on='datetime')
                elif i == 'زعفران (نهال)':
                    ind["زعفران (نهال)"] = index_price_history(12913156843322499, "زعفران (نهال)")
                    pivot_df = pivot_df.merge(ind["زعفران (نهال)"], how='left',on='datetime')
                elif i == 'شاخص همزون':
                    ind["شاخص هموزن"] = index_price_history2(67130298613737946, "شاخص هموزن")
                    pivot_df = pivot_df.merge(ind["شاخص هموزن"], how='left',on='datetime')
                elif i == 'شاخص کل':
                    ind["شاخص کل"] = index_price_history2(32097828799138957, "شاخص کل")
                    pivot_df = pivot_df.merge(ind["شاخص کل"], how='left',on='datetime')

            pivot_df.fillna(method='ffill', inplace=True)
            pivot_df['datetime'] = pd.to_datetime(
                pivot_df['datetime'],
                format='%Y%m%d',
                errors='coerce')
            pivot_df.sort_values('datetime', inplace=True)
            change_df = pivot_df[['datetime']]
            my_list = pivot_df.columns.values.tolist()
            my_list.remove('datetime')
            for i in my_list:
                change_df[i] = pivot_df[i].pct_change().fillna(0).cumsum()
                # change_df[i] = change_df[i].map('{:.2%}'.format)

            p2 = change_df.melt(id_vars=['datetime'], var_name='column_name', value_name='value')
            p2.fillna(0, inplace=True)
            # st.line_chart(p2,x="datetime", y="value", color="column_name", height=500)

            chart_product = alt.Chart(p2, height=600).mark_line().encode(
                alt.X('datetime:T', title='تاریخ'),
                alt.Y('value:Q', title="میزان عمکرد").axis(format='%'),
                alt.Color('column_name:N', title='دسته ها'),

            )
            chart_product.configure_title(
                    fontSize=20,
                    font='Vazirmatn',
                )

            chart_product.configure(
                font='Vazirmatn'
            )
            st.altair_chart(chart_product, use_container_width=True)
