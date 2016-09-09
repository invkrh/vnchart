from datetime import datetime, timedelta
import json
import pandas
import unittest

from app import traffic


class TestTraffic(unittest.TestCase):
    def test_create_df(self):
        with open('day.json') as data_file:
            data = json.load(data_file)
        df = traffic.create_df(data)
        self.assertEqual(len(df.index), 4)

    df = pandas.DataFrame(
        [
            {"year": 2000, "month": 3, "day": 3, "in": 5, "out": 5},
            {"year": 2000, "month": 3, "day": 4, "in": 5, "out": 5},
            {"year": 2000, "month": 4, "day": 3, "in": 5, "out": 5},
            {"year": 2005, "month": 7, "day": 3, "in": 5, "out": 5},
            {"year": 2005, "month": 4, "day": 3, "in": 5, "out": 5},
            {"year": 2005, "month": 5, "day": 3, "in": 5, "out": 5},
            {"year": 2001, "month": 6, "day": 3, "in": 5, "out": 5},
            {"year": 2001, "month": 5, "day": 3, "in": 5, "out": 5},
            {"year": 2001, "month": 6, "day": 3, "in": 5, "out": 5},
            {"year": 2016, "month": 9, "day": 1, "in": 5, "out": 500000},
            {"year": 2016, "month": 9, "day": 2, "in": 5, "out": 500000},
            {"year": 2016, "month": 9, "day": 3, "in": 5, "out": 500000},
        ]
    )

    def test_daily_traffic_in_current_month(self):
        dt = datetime.date(2016, 9, 5)
        res, cur = traffic.traffic_in_month(self.df, dt)
        print(res)
        print(cur)
        self.assertEqual(len(res['xValues']), traffic.day_num_in_month(dt))
        self.assertEqual(len(res['yValues']), traffic.day_num_in_month(dt))

    def test_monthly_traffic_in_last_year(self):
        res = traffic.traffic_in_last_year(self.df)
        print(res)
        self.assertEqual(len(res['xValues']), 12)
        self.assertEqual(len(res['yValues']), 12)

    def test_result_in_text(self):
        res = traffic.result_in_html(self.df)
        print(res)


if __name__ == '__main__':
    unittest.main()
