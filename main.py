"""Plot Some main monthly and quarterly charts"""
from pathlib import Path
import shutil

import streamlit as st
import pandas as pd
import altair as alt

from login import check_local_token, login
from request import vasahm_query
from menu import add_menu
from text_constant import MAIN_PAGE

from pages.helper.query import Queries

st.set_page_config(layout='wide',
                    page_title="وسهم",
                    page_icon="./assets/favicon.ico",
                    initial_sidebar_state='expanded')
st.session_state.ver = '0.1.7'

STREAMLIT_STATIC_PATH = Path(st.__path__[0]) / "static/static"
CSS_PATH = STREAMLIT_STATIC_PATH / "media/"
if not CSS_PATH.is_dir():
    CSS_PATH.mkdir()

css_file = CSS_PATH / "IRANSansWeb.ttf"
if not css_file.exists():
    shutil.copy("assets/font/IRANSansWeb.ttf", css_file)

with open( "style.css", encoding="utf-8") as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

def sfmono():
    """alrair chart theme"""
    font = "iransans"
    return {
        "config" : {
            "font": font
        }
    }

alt.themes.register('sfmono', sfmono)
alt.themes.enable('sfmono')

add_menu()
st.components.v1.html(MAIN_PAGE, height=60, scrolling=False)
# st.sidebar.image(image="./assets/logo.png")
st.sidebar.header(f'Vasahm DashBoard `{st.session_state.ver}`')

check_local_token()
if "token" not in st.session_state:
    login()
else:
    df = pd.read_csv("data.csv").dropna()
    list_of_name = df['name'].to_list()
    name = st.sidebar.selectbox("لیست سهام", options = list_of_name)

    queries = Queries(name)

    error, stock_data = vasahm_query(queries.get_stock_data())
    if error:
        st.error(stock_data, icon="🚨")
    else:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("سود سهم", f"{stock_data[0]['estimatedEPS']}")
        col2.metric("نسبت سود به قیمت", f"{format(float(stock_data[0]['pe']), '.2f')}")
        col3.metric("P/E صنعت", f"{format(float(stock_data[0]['sectorPE']), '.2f')}")
        col4.metric("درصد سهامداران عمده", f"{format(stock_data[0]['all_holder_percent'], '.2f')}")

    tab1, tab2 = st.tabs(["بر اساس ریال", "بر اساس دلار"])

    with tab1:

        st.header('گزارش ماهانه فروش', divider='rainbow')

        error, stock_data = vasahm_query(queries.get_monthly_sell_value_data())
        if error:
            st.error(stock_data, icon="🚨")
        else:
            stock_data_history = pd.DataFrame(stock_data, columns=["rowTitle",
                "value",
                "endToPeriod"])
            stock_data_history["endToPeriod"] = stock_data_history["endToPeriod"].astype(str)
            # specify the type of selection, here single selection is used
            selector = alt.selection_single(encodings=['x', 'color'])

            chart = alt.Chart(stock_data_history).mark_bar().encode(
                alt.Color('rowTitle:N', title="سرفصلها"),
                alt.Y('sum(value):Q', title="مبلغ (میلیون ریال)"),
                alt.X('endToPeriod:N',title="تاریخ")
            )
            st.altair_chart(chart, use_container_width=True)


        st.header('گزارش تعداد تولید', divider='rainbow')

        error, stock_data = vasahm_query(queries.get_monthly_production_value_data())
        if error:
            st.error(stock_data, icon="🚨")
        else:
            stock_data_history = pd.DataFrame(stock_data, columns=["rowTitle",
                "value",
                "endToPeriod"])
            stock_data_history["endToPeriod"] = stock_data_history["endToPeriod"].astype(str)
            # specify the type of selection, here single selection is used
            selector = alt.selection_single(encodings=['x', 'color'])

            chart_product = alt.Chart(stock_data_history).mark_bar().encode(
                alt.Color('rowTitle:N', title="سرفصلها"),
                alt.Y('sum(value):Q', title="تعداد"),
                alt.X('endToPeriod:N',title="تاریخ")
            )
            st.altair_chart(chart_product, use_container_width=True)

        st.header('گزارش تعداد فروش', divider='rainbow')

        error, stock_data = vasahm_query(queries.get_monthly_sell_no_data())
        if error:
            st.error(stock_data, icon="🚨")
        else:
            stock_data_history = pd.DataFrame(stock_data, columns=["rowTitle",
                "value",
                "endToPeriod"])
            stock_data_history["endToPeriod"] = stock_data_history["endToPeriod"].astype(str)
            # specify the type of selection, here single selection is used
            selector = alt.selection_single(encodings=['x', 'color'])

            chart_product = alt.Chart(stock_data_history).mark_bar().encode(
                alt.Color('rowTitle:N', title="سرفصلها"),
                alt.Y('sum(value):Q', title="تعداد"),
                alt.X('endToPeriod:N',title="تاریخ")
            )
            st.altair_chart(chart_product, use_container_width=True)


        st.header('درآمدهای عملیاتی و سود', divider='rainbow')

        error, stock_data = vasahm_query(queries.get_quarterly_sell_and_profit())
        if error:
            st.error(stock_data, icon="🚨")
        else:
            stock_data_history = pd.DataFrame(stock_data, columns=["rowTitle",
                "value",
                "endToPeriod"])
            stock_data_history["endToPeriod"] = stock_data_history["endToPeriod"].astype(str)
            # specify the type of selection, here single selection is used
            chart2 = alt.Chart(stock_data_history).mark_area(opacity=0.3).encode(
                alt.Color('rowTitle:N', title="سرفصلها"),
                alt.Y('value:Q', title="مبلغ (میلیون ریال)").stack(None),
                alt.X('endToPeriod:N',title="تاریخ")
            )
            st.altair_chart(chart2, use_container_width=True)


        st.header('حاشیه سود خالص', divider='rainbow')

        error, stock_data = vasahm_query(queries.get_quarterly_profit_ratio())
        if error:
            st.error(stock_data, icon="🚨")
        else:
            stock_data_history = pd.DataFrame(stock_data, columns=["rowTitle",
                "value",
                "endToPeriod"])
            stock_data_history["endToPeriod"] = stock_data_history["endToPeriod"].astype(str)
            stock_data_history["value"] = stock_data_history["value"].astype(float)
            pivot_df = stock_data_history.pivot_table(index='endToPeriod',
                                                    columns='rowTitle',
                                                    values='value',
                                                    aggfunc='sum').reset_index()

            pivot_df["profit_ratio"] = (pivot_df["سود(زیان) خالص"].astype(float)
                                        /pivot_df["درآمدهای عملیاتی"].astype(float))
            pe_df=pivot_df[["profit_ratio", "endToPeriod"]]

            chart_product = alt.Chart(pivot_df).mark_line().encode(
                    alt.X('endToPeriod:N', title='تاریخ'),
                    alt.Y('profit_ratio:Q', title="میزان عمکرد").axis(format='%'),
                    # alt.Color('column_name:N', title='دسته ها'),

                )
            chart_product.configure_title(
                        fontSize=20,
                        font='Vazirmatn',
                    )

            chart_product.configure(
                font='Vazirmatn'
            )
            st.altair_chart(chart_product, use_container_width=True)

    with tab2:

        st.header('گزارش ماهانه فروش - دلاری', divider='rainbow')

        error, stock_data = vasahm_query(queries.get_monthly_sell_value_data(dollar=True))
        if error:
            st.error(stock_data, icon="🚨")
        else:
            stock_data_history = pd.DataFrame(stock_data, columns=["rowTitle",
            "dollar_value",
            "endToPeriod"])
            stock_data_history["endToPeriod"] = stock_data_history["endToPeriod"].astype(str)
            # specify the type of selection, here single selection is used
            selector = alt.selection_single(encodings=['x', 'color'])

            chart = alt.Chart(stock_data_history).mark_bar().encode(
                alt.Color('rowTitle:N', title="سرفصلها"),
                alt.Y('sum(dollar_value):Q', title="مبلغ (میلیون دلار)"),
                alt.X('endToPeriod:N',title="تاریخ")
            )
            st.altair_chart(chart, use_container_width=True)


        st.header('گزارش تعداد تولید', divider='rainbow')

        error, stock_data = vasahm_query(queries.get_monthly_production_value_data())
        if error:
            st.error(stock_data, icon="🚨")
        else:
            stock_data_history = pd.DataFrame(stock_data, columns=["rowTitle",
            "value",
            "endToPeriod"])
            stock_data_history["endToPeriod"] = stock_data_history["endToPeriod"].astype(str)
            # specify the type of selection, here single selection is used
            selector = alt.selection_single(encodings=['x', 'color'])

            chart_product = alt.Chart(stock_data_history).mark_bar().encode(
                alt.Color('rowTitle:N', title="سرفصلها"),
                alt.Y('sum(value):Q', title="تعداد"),
                alt.X('endToPeriod:N',title="تاریخ")
            )
            st.altair_chart(chart_product, use_container_width=True)

        st.header('گزارش تعداد فروش', divider='rainbow')

        error, stock_data = vasahm_query(queries.get_monthly_sell_no_data())
        if error:
            st.error(stock_data, icon="🚨")
        else:
            stock_data_history = pd.DataFrame(stock_data, columns=["rowTitle",
            "value",
            "endToPeriod"])
            stock_data_history["endToPeriod"] = stock_data_history["endToPeriod"].astype(str)
            # specify the type of selection, here single selection is used
            selector = alt.selection_single(encodings=['x', 'color'])

            chart_product = alt.Chart(stock_data_history).mark_bar().encode(
                alt.Color('rowTitle:N', title="سرفصلها"),
                alt.Y('sum(value):Q', title="تعداد"),
                alt.X('endToPeriod:N',title="تاریخ")
            )
            st.altair_chart(chart_product, use_container_width=True)


        st.header('درآمدهای عملیاتی و سود - دلاری', divider='rainbow')

        error, stock_data = vasahm_query(queries.get_quarterly_sell_and_profit(dollar=True))
        if error:
            st.error(stock_data, icon="🚨")
        else:
            stock_data_history = pd.DataFrame(stock_data, columns=["rowTitle",
            "dollar_value",
            "endToPeriod"])

            stock_data_history["endToPeriod"] = stock_data_history["endToPeriod"].astype(str)
            # specify the type of selection, here single selection is used
            chart2 = alt.Chart(stock_data_history).mark_area(opacity=0.3).encode(
                alt.Color('rowTitle:N', title="سرفصلها"),
                alt.Y('dollar_value:Q', title="مبلغ (میلیون دلار)").stack(None),
                alt.X('endToPeriod:N',title="تاریخ")
            )

            st.altair_chart(chart2, use_container_width=True)

        st.header('حاشیه سود خالص - دلاری', divider='rainbow')

        error, stock_data = vasahm_query(queries.get_quarterly_profit_ratio(dollar=True))
        if error:
            st.error(stock_data, icon="🚨")
        else:
            stock_data_history = pd.DataFrame(stock_data, columns=["rowTitle",
            "dollar_value",
            "endToPeriod"])
            stock_data_history["endToPeriod"] = stock_data_history["endToPeriod"].astype(str)
            pivot_df = stock_data_history.pivot_table(index='endToPeriod',
                                                    columns='rowTitle',
                                                    values='dollar_value',
                                                    aggfunc='sum').reset_index()
            pivot_df["profit_ratio"] = (pivot_df["سود(زیان) خالص"].astype(float)
                                        /pivot_df["درآمدهای عملیاتی"].astype(float))

            chart_product = alt.Chart(pivot_df,
                                    height=600).mark_line().encode(
                            alt.X('endToPeriod:N', title='تاریخ'),
                            alt.Y('profit_ratio:Q', title="میزان عمکرد").axis(format='%'),
                            # alt.Color('column_name:N', title='دسته ها'),
                        )
            chart_product.configure_title(
                        fontSize=20,
                        font='Vazirmatn',
                    )

            chart_product.configure(
                font='Vazirmatn'
            )
            st.altair_chart(chart_product, use_container_width=True)
