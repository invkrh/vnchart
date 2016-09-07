import json
import unittest
import pandas

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
            {"year": 2016, "month": 9, "day": 1, "in": 5, "out": 5},
            {"year": 2016, "month": 9, "day": 2, "in": 5, "out": 5},
            {"year": 2016, "month": 9, "day": 3, "in": 5, "out": 5},
        ]
    )

    def test_monthly_traffic_in_last_year(self):
        res = traffic.traffic_in_last_year(self.df)
        self.assertEqual(len(res.index), 7)

    def test_daily_traffic_in_current_month(self):
        res, cur = traffic.traffic_in_current_month(self.df)
        self.assertEqual(len(res.index), 3)


if __name__ == '__main__':
    unittest.main()
