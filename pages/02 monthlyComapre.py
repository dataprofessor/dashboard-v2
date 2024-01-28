import streamlit as st
import pandas as pd
import plotly.express as px
import plost
from request import vasahm_query
from slider import create_range_slider, create_slider
from request import get_nonce
from request import get_key
import altair as alt

st.set_page_config(layout='wide',
                   page_title="Vasahm Dashboard",
                    page_icon="./assets/favicon.ico",
                    initial_sidebar_state='expanded')

# st.markdown(
#     """
#     <style>
#     #MainMenu {visibility: hidden;}
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# st.markdown(
#     """
#     <style>
#     .stDeployButton {
#             visibility: hidden;
#         }
#     </style>
#     """, unsafe_allow_html=True
# )
with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)


# st.sidebar.image(image="./assets/logo.png")
st.sidebar.header(f'Vasahm DashBoard `{st.session_state.ver}`')

def get_email_callback():
    hasError, message = get_nonce(st.session_state.email)
    if hasError:
        st.error(message, icon="🚨")
    else:
        submit_nonce = st.form("submit_nonce")
        submit_nonce.write("Inside the submit_nonce")
        nonce = submit_nonce.text_input('please enter your mail', placeholder='example@mail.com', key="nonce")
        # Every form must have a submit button.
        submitted = submit_nonce.form_submit_button("Submit", on_click = get_nonce_callback )

def get_nonce_callback():
    hasError, message = get_key(st.session_state.email, st.session_state.nonce)
    if hasError:
        st.error(message, icon="🚨")
        del st.session_state["nonce"]
    else:
        st.session_state["token"] = message


if "token" not in st .session_state:
    get_email = st.form("get_email")
    get_email.write("Inside the get_email")
    email = get_email.text_input('please enter your mail', placeholder='example@mail.com', key="email")
    # Every form must have a submit button.
    submitted = get_email.form_submit_button("Submit", on_click = get_email_callback )
else:

    txt = """WITH
  ranked_dates AS (
    SELECT
      stocks.name,
      endToPeriod,
      SUM(value) as sum_value,
      ROW_NUMBER() OVER (
        PARTITION BY
          stocks.name
        ORDER BY
          endToPeriod DESC
      ) AS rnk
    FROM
      MonthlyData
      join stocks on MonthlyData.stock_id = stocks.id
    where
      (
        stocks.stockType = '300'
        OR stocks.stockType = '303'
        OR stocks.stockType = '309'
      )
      AND (
        MonthlyData.columnTitle = 'مبلغ فروش (میلیون ریال)'
        OR MonthlyData.columnTitle = 'درآمد شناسایی شده'
      )
    group by
      stocks.name,
      MonthlyData.endToPeriod
  )
select
  name,
  (
    MAX(
      CASE
        WHEN rnk = 1 THEN sum_value
        ELSE 0
      END
    ) / MAX(
      CASE
        WHEN rnk = 2 THEN sum_value
      END
    )
  ) AS result,
  (
    SUM(
      CASE
        WHEN rnk IN (1, 2) THEN sum_value
        ELSE 0
      END
    ) / SUM(
      CASE
        WHEN rnk in (3, 4) THEN sum_value
      END
    )
  ) AS result2,
  (
    SUM(
      CASE
        WHEN rnk IN (1, 2, 3) THEN sum_value
        ELSE 0
      END
    ) / SUM(
      CASE
        WHEN rnk in (4, 5, 6) THEN sum_value
      END
    )
  ) AS result3
from
  ranked_dates
group by
  name"""

    hasError, data = vasahm_query(txt)
    if hasError:
        st.error(data, icon="🚨")
    else:
        stock_data_history = pd.DataFrame(data).fillna(0.0)

        col1_slider = create_range_slider(stock_data_history, "col1_slider", "M/M ratio", "result")
        col2_slider = create_range_slider(stock_data_history, "col2_slider", "2M/2M ratio", "result2")
        col3_slider = create_range_slider(stock_data_history, "col3_slider", "3M/3M ratio", "result3")

        filtered_df = stock_data_history[stock_data_history['result'].astype("float").between(col1_slider[0], col1_slider[1])]
        filtered_df1 = filtered_df[filtered_df['result2'].astype("float").between(col2_slider[0], col2_slider[1])]
        filtered_df2 = filtered_df1[filtered_df1['result3'].astype("float").between(col3_slider[0], col3_slider[1])]
        
        st.dataframe(filtered_df2, use_container_width=True, height=600,
                     column_config={
        "result": st.column_config.NumberColumn(
            "M/M",
            help="Month to Month sell",
            format="%.2f",
        ),
        "result2": st.column_config.NumberColumn(
            "2M/2M",
            help="two Month to two Month sell",
            format="%.2f",
        ),
        "result3": st.column_config.NumberColumn(
            "3M/3M",
            help="three Month to three Month sell",
            format="%.2f",
        )
        })