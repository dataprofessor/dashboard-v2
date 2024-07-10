"""handle creating all queries"""
# from datetime import datetime

class Queries():
    """
    create and return all queries
    inputs:
        name = name of stock
    """
    def __init__(self, name=None):
        self.name = name

    def get_stock_data(self):
        """return query to get stock data"""
        string = f"""select
                        stock_data.id, \"estimatedEPS\", \"sectorPE\", pe, all_holder_percent, all_holder_share
                    from
                        stock_data
                        INNER JOIN stocks ON stock_data.stock_id = stocks.id
                    where
                        stocks.name = '{self.name}'
                    order by 
                        stock_data.id desc
            """
        return string

    def get_monthly_sell_value_data(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                        row_title,
                        sum(value) as value,
                        end_to_period
                    from
                        public.all_data
                        INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                        INNER JOIN report_list ON public.all_data.report_id = report_list.id
                    where
                        (
                        public.all_data.column_title = 'مبلغ فروش (میلیون ریال)'
                        or public.all_data.column_title = 'درآمد شناسایی شده'
                        or public.all_data.column_title = 'درآمد محقق شده طی دوره یک ماهه - لیزینگ'
                        )
                        and stocks.name = '{self.name}'
                        and (public.report_list.\"letterCode\" = 'ن-۳۰' or public.report_list.\"letterCode\" = 'ن-۳۱')
                    group by
                        public.all_data.row_title,
                        public.all_data.end_to_period
        """
        if dollar:
            string = self._dollar_query(string)
        return string

    def get_monthly_production_value_data(self):
        """return query to monthly sell value data"""
        string = f"""select
                        row_title,
                        sum(value) as value,
                        end_to_period
                    from
                        public.all_data
                        INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                        INNER JOIN report_list ON public.all_data.report_id = report_list.id
                    where
                        (
                        public.all_data.column_title = 'تعداد تولید'
                        )
                        and stocks.name = '{self.name}'
                        and (public.report_list.\"letterCode\" = 'ن-۳۰' or public.report_list.\"letterCode\" = 'ن-۳۱')
                    group by
                        public.all_data.row_title,
                        public.all_data.end_to_period
        """
        return string

    def get_monthly_sell_no_data(self):
        """return query to monthly sell value data"""
        string = f"""select
                        row_title,
                        sum(value) as value,
                        end_to_period
                    from
                        public.all_data
                        INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                        INNER JOIN report_list ON public.all_data.report_id = report_list.id
                    where
                        (
                        public.all_data.column_title = 'تعداد فروش'
                        )
                        and stocks.name = '{self.name}'
                        and (public.report_list.\"letterCode\" = 'ن-۳۰' or public.report_list.\"letterCode\" = 'ن-۳۱')
                    group by
                        public.all_data.row_title,
                        public.all_data.end_to_period
        """
        return string

    def get_quarterly_sell_and_profit(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                        row_title,
                        value,
                        end_to_period
                    from
                        public.all_data
                        INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                        INNER JOIN report_list ON public.all_data.report_id = report_list.id
                    where
                        (
                        public.all_data.column_title = 'درآمدهای عملیاتی'
                        or public.all_data.column_title = 'سود(زیان) ناخالص'
                        or public.all_data.column_title = 'سود(زیان) خالص'
                        )
                        and stocks.name = '{self.name}'
                        and (public.report_list.\"letterCode\" = 'ن-۱۰')
        """
        if dollar:
            string = self._dollar_query(string)
        return string

    def get_quarterly_profit_ratio(self, dollar = False):
        """return query to monthly sell value data"""
        string = f"""select
                        row_title,
                        value,
                        end_to_period
                    from
                        public.all_data
                        INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                        INNER JOIN report_list ON public.all_data.report_id = report_list.id
                    where
                        (
                        public.all_data.column_title = 'درآمدهای عملیاتی'
                        or public.all_data.column_title = 'سود(زیان) ناخالص'
                        or public.all_data.column_title = 'سود(زیان) خالص'
                        )
                        and stocks.name = '{self.name}'
                        and (public.report_list.\"letterCode\" = 'ن-۱۰')
        """
        if dollar:
            string = self._dollar_query(string)
        return string

    def _dollar_query(self, text):
        query_string = f"""WITH
        ranked_dates AS (
            {text}
        )
        select
            row_title,
            value::float / dollar.rate * 1000000 As dollar_value,
            end_to_period
        from
            ranked_dates
            INNER JOIN dollar ON ranked_dates.\"endToPeriod\"::varchar = dollar.\"Jalali\"
        """
        return query_string

    QUERY_MONTHLY_COMPARE = """WITH
                        ranked_dates AS (
                            SELECT
                            stocks.name,
                            end_to_period,
                            SUM(value) as sum_value,
                            ROW_NUMBER() OVER (
                                PARTITION BY
                                stocks.name
                                ORDER BY
                                end_to_period DESC
                            ) AS rnk
                            FROM
                                public.all_data
                                INNER JOIN stocks ON public.all_data.stock_id = stocks.id
                                INNER JOIN report_list ON public.all_data.report_id = report_list.id
                            where
                                (
                                    stocks.\"stockType\" = '300'
                                    OR stocks.\"stockType\" = '303'
                                    OR stocks.\"stockType\" = '309'
                                )
                                AND (
                                    public.all_data.column_title = 'مبلغ فروش (میلیون ریال)'
                                    OR public.all_data.column_title = 'درآمد شناسایی شده'
                                )
                                AND (public.report_list.\"letterCode\" = 'ن-۳۰' or public.report_list.\"letterCode\" = 'ن-۳۱')
                            group by
                                stocks.name,
                                public.all_data.end_to_period
                        )
                        select
                        name,
                        (
                            MAX(
                            CASE
                                WHEN rnk = 1 THEN sum_value
                                ELSE 0
                            END
                            ) / NULLIF(MAX(
                            CASE
                                WHEN rnk = 2 THEN sum_value
                            END
                            ),0)
                        ) AS result,
                        (
                            SUM(
                            CASE
                                WHEN rnk IN (1, 2) THEN sum_value
                                ELSE 0
                            END
                            ) / NULLIF(SUM(
                            CASE
                                WHEN rnk in (3, 4) THEN sum_value
                            END
                            ),0)
                        ) AS result2,
                        (
                            SUM(
                            CASE
                                WHEN rnk IN (1, 2, 3) THEN sum_value
                                ELSE 0
                            END
                            ) / NULLIF(SUM(
                            CASE
                                WHEN rnk in (4, 5, 6) THEN sum_value
                            END
                            ),0)
                        ) AS result3
                        from
                        ranked_dates
                        group by
                        name"""