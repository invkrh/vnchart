import unittest
import json

from vnschart.app import TrafficStat


class TestTrafficStat(unittest.TestCase):
    ts = TrafficStat()

    with open('hour.json') as data_file:
        raw_stat_hour = json.load(data_file)
    with open('day.json') as data_file:
        raw_stat_day = json.load(data_file)

    def test_vnstat(self):
        # Check unknown args exception
        with self.assertRaises(AssertionError):
            self.ts.vnstat('j', 'd')
        with self.assertRaises(AssertionError):
            self.ts.vnstat('json', 'a')

    def test_create_data_frame(self):
        df_hour = TrafficStat.create_data_frame(self.raw_stat_hour, 'hours')
        self.assertEqual(len(df_hour.index), 24)
        df_day = TrafficStat.create_data_frame(self.raw_stat_day, 'days')
        self.assertEqual(len(df_day.index), 18)

    def test_indexed_stat(self):
        df = TrafficStat.create_data_frame(self.raw_stat_hour, 'hours')
        stat = self.ts.indexed_stat(df)
        self.assertEqual(len(stat['xValues']), 24)
        self.assertEqual(len(stat['yValues']), 24)


if __name__ == '__main__':
    unittest.main()
