import streamlit as st
import pandas as pd
import plotly.express as px
import plost
from request import areon_query
from slider import create_slider
import altair as alt

st.set_page_config(layout='wide',
                   page_title="وسهم",
                    # page_icon="./assets/favicon.ico",
                    initial_sidebar_state='expanded')



# with open('style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
# st.sidebar.image(image="./assets/logo.png")
st.sidebar.header('vasahm DashBoard `version 1`')

df = pd.read_csv("data.csv").dropna()
rslt_df = df[df['type'] == "contract"] 
list_of_name = df['name'].to_list()

name = st.sidebar.selectbox("google", options = list_of_name)

st.header('گزارش ماهانه فروش', divider='rainbow')

queryString = queryString = """select
  rowTitle,
  sum(value) as value,
  endToPeriod
from
  MonthlyData
  INNER JOIN stocks ON MonthlyData.stock_id = stocks.id
where
  (
    MonthlyData.columnTitle = 'مبلغ فروش (میلیون ریال)'
    or MonthlyData.columnTitle = 'درآمد شناسایی شده'
    or MonthlyData.columnTitle = 'درآمد محقق شده طی دوره یک ماهه - لیزینگ'
  )
  and stocks.name = '{}'
group by
  MonthlyData.rowTitle,
  MonthlyData.endToPeriod
""".format(name)

stock_data = areon_query(queryString)
stock_data_history = pd.DataFrame(stock_data, columns=["rowTitle",
  "value",
  "endToPeriod"])
stock_data_history["endToPeriod"] = stock_data_history["endToPeriod"].astype(str)
# specify the type of selection, here single selection is used 
selector = alt.selection_single(encodings=['x', 'color']) 

chart = alt.Chart(stock_data_history).mark_bar().encode(
    color='rowTitle:N',
    y='sum(value):Q',
    x='endToPeriod:N'
)
st.altair_chart(chart, use_container_width=True)


st.header('گزارش تعداد تولید', divider='rainbow')
queryString = queryString = """select
  rowTitle,
  sum(value) as value,
  endToPeriod
from
  MonthlyData
  INNER JOIN stocks ON MonthlyData.stock_id = stocks.id
where
  (
    MonthlyData.columnTitle = 'تعداد تولید'
  )
  and stocks.name = '{}'
group by
  MonthlyData.rowTitle,
  MonthlyData.endToPeriod
""".format(name)

stock_data = areon_query(queryString)
stock_data_history = pd.DataFrame(stock_data, columns=["rowTitle",
  "value",
  "endToPeriod"])
stock_data_history["endToPeriod"] = stock_data_history["endToPeriod"].astype(str)
# specify the type of selection, here single selection is used 
selector = alt.selection_single(encodings=['x', 'color']) 

chart_product = alt.Chart(stock_data_history).mark_bar().encode(
    color='rowTitle:N',
    y='sum(value):Q',
    x='endToPeriod:N'
)
st.altair_chart(chart_product, use_container_width=True)

st.header('گزارش تعداد فروش', divider='rainbow')
queryString = queryString = """select
  rowTitle,
  sum(value) as value,
  endToPeriod
from
  MonthlyData
  INNER JOIN stocks ON MonthlyData.stock_id = stocks.id
where
  (
    MonthlyData.columnTitle = 'تعداد فروش'
  )
  and stocks.name = '{}'
group by
  MonthlyData.rowTitle,
  MonthlyData.endToPeriod
""".format(name)

stock_data = areon_query(queryString)
stock_data_history = pd.DataFrame(stock_data, columns=["rowTitle",
  "value",
  "endToPeriod"])
stock_data_history["endToPeriod"] = stock_data_history["endToPeriod"].astype(str)
# specify the type of selection, here single selection is used 
selector = alt.selection_single(encodings=['x', 'color']) 

chart_product = alt.Chart(stock_data_history).mark_bar().encode(
    color='rowTitle:N',
    y='sum(value):Q',
    x='endToPeriod:N'
)
st.altair_chart(chart_product, use_container_width=True)




st.header('درآمدهای عملیاتی و سود', divider='rainbow')
queryString = """select
  rowTitle,
  value,
  endToPeriod
from
  QuarterlyData
  INNER JOIN stocks ON QuarterlyData.stock_id = stocks.id
where
  (
    QuarterlyData.rowTitle = 'درآمدهای عملیاتی'
    or QuarterlyData.rowTitle = 'سود(زیان) ناخالص'
    or QuarterlyData.rowTitle = 'سود(زیان) خالص'
  )
  and stocks.name = '{}'
""".format(name)

stock_data = areon_query(queryString)
stock_data_history = pd.DataFrame(stock_data, columns=["rowTitle",
  "value",
  "endToPeriod"])
stock_data_history["endToPeriod"] = stock_data_history["endToPeriod"].astype(str)
# specify the type of selection, here single selection is used 
chart2 = alt.Chart(stock_data_history).mark_area(opacity=0.3).encode(
    color='rowTitle:N',
    y=alt.Y('value:Q').stack(None),
    x='endToPeriod:N'
)

st.altair_chart(chart2, use_container_width=True)