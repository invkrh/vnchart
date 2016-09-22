import unittest
import json

from vnschart.app import TrafficStat


class TestTrafficStat(unittest.TestCase):

    with open('tests/hour.json') as data_file:
        raw_stat_hour = json.load(data_file)
    with open('tests/day.json') as data_file:
        raw_stat_day = json.load(data_file)

    ts = TrafficStat(raw_stat_hour, raw_stat_day)

    def test_vnstat(self):
        # Check unknown args exception
        with self.assertRaises(AssertionError):
            self.ts.vnstat('j', 'd')
        with self.assertRaises(AssertionError):
            self.ts.vnstat('json', 'a')

    def test_create_data_frame(self):
        self.assertEqual(len(self.ts.hour_df.index), 24)
        self.assertEqual(len(self.ts.day_df.index), 18)

    def test_indexed_stat(self):
        hour_stat = self.ts.stat_by_hour()
        self.assertEqual(len(hour_stat['xValues']), 24)
        self.assertEqual(len(hour_stat['yValues']), 24)
        day_stat = self.ts.stat_by_day()
        self.assertEqual(len(day_stat['xValues']), 18)
        self.assertEqual(len(day_stat['yValues']), 18)

    def test_current_usage(self):
        self.ts.current_usage()


if __name__ == '__main__':
    unittest.main()
