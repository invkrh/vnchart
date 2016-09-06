import json
import unittest

from app import traffic


class TestTraffic(unittest.TestCase):
    def test_create_df(self):
        with open('day.json') as data_file:
            data = json.load(data_file)
        df = traffic.create_df(data)
        self.assertEqual(len(df.index), 4)

if __name__ == '__main__':
    unittest.main()
