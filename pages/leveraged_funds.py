"""Module compares leveraged funds."""

import streamlit as st
import pandas as pd
import altair as alt

from menu import add_menu

from funds.fund import Fund
from funds.metrics import Metrics

st.set_page_config(layout='wide',
                   page_title="وسهم - بررسی صندوق های اهرمی",
                    page_icon="./assets/favicon.ico",
                    initial_sidebar_state='expanded')

with open( "style.css", encoding='UTF-8') as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
add_menu()

# st.sidebar.image(image="./assets/logo.png")
if "ver" in st.session_state:
    st.sidebar.header(f'Vasahm DashBoard `{st.session_state.ver}`')

FILE_PATH = "./funds/fund_data.csv"
df = pd.read_csv(FILE_PATH, header=0)
metrics = Metrics()
funds = []
for index, row  in df.iterrows():
    try:
        funds.append(Fund(row["name"], row["url"], row["code"], metrics))
    except:
        pass

funds_df = pd.DataFrame([vars(obj) for obj in funds])
# funds_df["name"] = funds_df["name"].apply(lambda x: correctPersianText(x))
funds_df["leverage"] = funds_df["BaseUnitsTotalSubscription"]/\
    funds_df["SuperUnitsTotalSubscription"]+1
funds_df['leverage'] = funds_df['leverage'].round(decimals=2)
funds_df["bubble"] = (funds_df["last"]-funds_df["SuperUnitsCancelNAV"])/funds_df["last"]

col1, col2 = st.columns(2)
with col1:
    st.header('اهرم صندوق های اهرمی', divider='rainbow')
    chart = alt.Chart(funds_df).mark_bar().encode(
                    alt.X('name:N', title='نام صندوق'),
                    alt.Y('leverage:Q', title="میزان اهرم"),
                    alt.Color('name:N', title='نام صندوق'),
                )
    labels = alt.Chart(funds_df).mark_text(align='center', dy=-10, fontSize=20).encode(
                        alt.X('name:N', title='نام صندوق'),
                        alt.Y('leverage:Q', title="میزان اهرم"),
                        alt.Color('name:N', title='نام صندوق', legend=None),
                        alt.Text('leverage:Q'),
                    )
    chart_product = alt.layer(chart, labels).resolve_scale(color='independent')
    st.altair_chart(chart_product, use_container_width=True)
with col2:
    st.header('حباب صندوق ها', divider='rainbow')
    chart = alt.Chart(funds_df).mark_bar().encode(
                        alt.X('name:N', title='نام صندوق'),
                        alt.Y('bubble:Q', title="میزان حباب").axis(format='%'),
                        alt.Color('name:N', title='نام صندوق'),
                    )
    labels = alt.Chart(funds_df).mark_text(align='center', dy=-10, fontSize=20).encode(
                        alt.X('name:N', title='نام صندوق'),
                        alt.Y('bubble:Q', title="میزان حباب").axis(format='%'),
                        alt.Color('name:N', title='نام صندوق', legend=None),
                        alt.Text('bubble:Q').format('0.2%'),
                    )
    chart_product = alt.layer(chart, labels).resolve_scale(color='independent')
    st.altair_chart(chart_product, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.header('میزان دارایی نقد و اوراق', divider='rainbow')
    chart = alt.Chart(funds_df).mark_bar().encode(
                        alt.X('name:N', title='نام صندوق'),
                        alt.Y('CashAsset:Q', title="میزان دارایی نقد و اوراق").axis(format='%'),
                        alt.Color('name:N', title='نام صندوق'),
                        alt.Text('CashAsset:Q'),
                    )
    labels = alt.Chart(funds_df).mark_text(align='center', dy=-10, fontSize=20).encode(
                        alt.X('name:N', title='نام صندوق'),
                        alt.Y('CashAsset:Q', title="میزان دارایی نقد و اوراق").axis(format='%'),
                        alt.Color('name:N', title='نام صندوق', legend=None),
                        alt.Text('CashAsset:Q').format('0.2%'),
                    )
    chart_product = alt.layer(chart, labels).resolve_scale(color='independent')
    st.altair_chart(chart_product, use_container_width=True)

# with col2:
#     st.header('میزان دارایی نقد و اوراق', divider='rainbow')
#     chart = alt.Chart(funds_df).mark_bar().encode(
#                         alt.X('name:N', title='نام صندوق'),
#                         alt.Y('performance:Q', title="میزان دارایی نقد و اوراق").axis(format='%'),
#                         alt.Color('name:N', title='نام صندوق'),
#                     )
#     st.altair_chart(chart, use_container_width=True)
