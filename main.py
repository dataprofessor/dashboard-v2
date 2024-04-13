"""Plot Some main monthly and quarterly charts"""


import streamlit as st
import pandas as pd
import altair as alt

from login import check_local_token, login
from request import vasahm_query
from menu import add_menu

st.set_page_config(layout='wide',
                    page_title="وسهم",
                    page_icon="./assets/favicon.ico",
                    initial_sidebar_state='expanded')
st.session_state.ver = '0.1.5'

with open( "style.css", encoding="utf-8") as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

add_menu()
HTML = """<!DOCTYPE html>
<html lang="fa" dir="rtl">

<head>
  <meta charset="UTF-8">
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
    <p>وبسایت در مرحله آزمایشی است، از اطلاعات با احتیاط استفاده کنید. در صورت مشاهده ایراد میتوانید به تست<a href="https://t.me/Khiaboon_Hafez_Admin" target="_blank">@Khiaboon_Hafez_Admin</a> پیام دهید.</p>
  </div>
</body>

</html>
"""
st.components.v1.html(HTML, height=60, scrolling=False)
# st.sidebar.image(image="./assets/logo.png")
st.sidebar.header(f'Vasahm DashBoard `{st.session_state.ver}`')

check_local_token()
if "token" not in st.session_state:
    login()
else:
    df = pd.read_csv("data.csv").dropna()
    list_of_name = df['name'].to_list()
    name = st.sidebar.selectbox("لیست سهام", options = list_of_name)

    query_string = f"""select
                \"stockData\".id, \"estimatedEPS\", \"sectorPE\", pe, all_holder_percent, all_holder_share
            from
                \"stockData\"
                INNER JOIN stocks ON \"stockData\".stock_id = stocks.id
            where
                stocks.name = '{name}'
            order by 
                "stockData".id desc
            """

    error, stock_data = vasahm_query(query_string)
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

        query_string = f"""select
        \"rowTitle\",
        sum(value) as value,
        \"endToPeriod\"
    from
        public.\"MonthlyData\"
        INNER JOIN stocks ON public.\"MonthlyData\".stock_id = stocks.id
    where
        (
        public.\"MonthlyData\".\"columnTitle\" = 'مبلغ فروش (میلیون ریال)'
        or public.\"MonthlyData\".\"columnTitle\" = 'درآمد شناسایی شده'
        or public.\"MonthlyData\".\"columnTitle\" = 'درآمد محقق شده طی دوره یک ماهه - لیزینگ'
        )
        and stocks.name = '{name}'
    group by
        public.\"MonthlyData\".\"rowTitle\",
        public.\"MonthlyData\".\"endToPeriod\"
        """
        error, stock_data = vasahm_query(query_string)
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
        query_string = f"""select
        \"rowTitle\",
        sum(value) as value,
        \"endToPeriod\"
    from
        \"MonthlyData\"
        INNER JOIN stocks ON \"MonthlyData\".stock_id = stocks.id
    where
        (
        \"MonthlyData\".\"columnTitle\" = 'تعداد تولید'
        )
        and stocks.name = '{name}'
    group by
        \"MonthlyData\".\"rowTitle\",
        \"MonthlyData\".\"endToPeriod\"
        """
        error, stock_data = vasahm_query(query_string)
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
        query_string = f"""select
        \"rowTitle\",
        sum(value) as value,
        \"endToPeriod\"
    from
        \"MonthlyData\"
        INNER JOIN stocks ON \"MonthlyData\".stock_id = stocks.id
    where
        (
        \"MonthlyData\".\"columnTitle\" = 'تعداد فروش'
        )
        and stocks.name = '{name}'
    group by
        \"MonthlyData\".\"rowTitle\",
        \"MonthlyData\".\"endToPeriod\"
        """
        error, stock_data = vasahm_query(query_string)
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
        query_string = f"""select
        \"rowTitle\",
        \"value\",
        \"endToPeriod\"
    from
        \"QuarterlyData\"
        INNER JOIN stocks ON \"QuarterlyData\".stock_id = stocks.id
    where
        (
        \"QuarterlyData\".\"rowTitle\" = 'درآمدهای عملیاتی'
        or \"QuarterlyData\".\"rowTitle\" = 'سود(زیان) ناخالص'
        or \"QuarterlyData\".\"rowTitle\" = 'سود(زیان) خالص'
        )
        and stocks.name = '{name}'
        """
        error, stock_data = vasahm_query(query_string)
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
        query_string = f"""select
        \"rowTitle\",
        \"value\",
        \"endToPeriod\"
    from
        \"QuarterlyData\"
        INNER JOIN stocks ON \"QuarterlyData\".stock_id = stocks.id
    where
        (
        \"QuarterlyData\".\"rowTitle\" = 'درآمدهای عملیاتی'
        or \"QuarterlyData\".\"rowTitle\" = 'سود(زیان) ناخالص'
        or \"QuarterlyData\".\"rowTitle\" = 'سود(زیان) خالص'
        )
        and stocks.name = '{name}'
        """
        error, stock_data = vasahm_query(query_string)
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

        query_string = f"""WITH
        ranked_dates AS (
            select
            \"rowTitle\",
            sum(value) as value,
            \"endToPeriod\"
            from
            \"MonthlyData\"
            INNER JOIN stocks ON \"MonthlyData\".stock_id = stocks.id
            where
            (
            \"MonthlyData\".\"columnTitle\" = 'مبلغ فروش (میلیون ریال)'
            or \"MonthlyData\".\"columnTitle\" = 'درآمد شناسایی شده'
            or \"MonthlyData\".\"columnTitle\" = 'درآمد محقق شده طی دوره یک ماهه - لیزینگ'
            )
            and stocks.name = '{name}'
            group by
            \"MonthlyData\".\"rowTitle\",
            \"MonthlyData\".\"endToPeriod\"
        )
        select
        \"rowTitle\",
        value / dollar.rate * 1000000 As dollar_value,
        \"endToPeriod\"
        from
        ranked_dates
        INNER JOIN dollar ON ranked_dates.\"endToPeriod\"::varchar = dollar.\"Jalali\"
        """

        error, stock_data = vasahm_query(query_string)
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
        query_string = f"""select
            \"rowTitle\",
            sum(value) as value,
            \"endToPeriod\"
        from
            \"MonthlyData\"
            INNER JOIN stocks ON \"MonthlyData\".stock_id = stocks.id
        where
            (
            \"MonthlyData\".\"columnTitle\" = 'تعداد تولید'
            )
            and stocks.name = '{name}'
        group by
            \"MonthlyData\".\"rowTitle\",
            \"MonthlyData\".\"endToPeriod\"
        """
        error, stock_data = vasahm_query(query_string)
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
        query_string = f"""select
            \"rowTitle\",
            sum(value) as value,
            \"endToPeriod\"
        from
            \"MonthlyData\"
            INNER JOIN stocks ON \"MonthlyData\".stock_id = stocks.id
        where
            (
            \"MonthlyData\".\"columnTitle\" = 'تعداد فروش'
            )
            and stocks.name = '{name}'
        group by
            \"MonthlyData\".\"rowTitle\",
            \"MonthlyData\".\"endToPeriod\"
        """
        error, stock_data = vasahm_query(query_string)
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
        query_string = f"""WITH
        ranked_dates AS (
            select
            \"rowTitle\",
            value,
            \"endToPeriod\"
            from
            \"QuarterlyData\"
            INNER JOIN stocks ON \"QuarterlyData\".stock_id = stocks.id
            where
            (
                \"QuarterlyData\".\"rowTitle\" = 'درآمدهای عملیاتی'
                or \"QuarterlyData\".\"rowTitle\" = 'سود(زیان) ناخالص'
                or \"QuarterlyData\".\"rowTitle\" = 'سود(زیان) خالص'
            )
            and stocks.name = '{name}'
        )
        select
        \"rowTitle\",
        value::float / dollar.rate * 1000000 As dollar_value,
        \"endToPeriod\"
        from
        ranked_dates
        INNER JOIN dollar ON ranked_dates.\"endToPeriod\"::varchar = dollar.\"Jalali\"
        """
        error, stock_data = vasahm_query(query_string)
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
        query_string = f"""WITH
        ranked_dates AS (
            select
            \"rowTitle\",
            value,
            \"endToPeriod\"
            from
            \"QuarterlyData\"
            INNER JOIN stocks ON \"QuarterlyData\".stock_id = stocks.id
            where
            (
                \"QuarterlyData\".\"rowTitle\" = 'درآمدهای عملیاتی'
                or \"QuarterlyData\".\"rowTitle\" = 'سود(زیان) ناخالص'
                or \"QuarterlyData\".\"rowTitle\" = 'سود(زیان) خالص'
            )
            and stocks.name = '{name}'
        )
        select
        \"rowTitle\",
        value::float / dollar.rate * 1000000 As dollar_value,
        \"endToPeriod\"
        from
        ranked_dates
        INNER JOIN dollar ON ranked_dates.\"endToPeriod\"::varchar = dollar.\"Jalali\"
        """
        error, stock_data = vasahm_query(query_string)
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
