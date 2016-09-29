import unittest

from vnchart.dashboard import *


class TestApp(unittest.TestCase):

    def test_kb_to_mb(self):
        # with two digits
        result = kb_to_mb(1024)
        expected = '1.00'
        self.assertEqual(expected, result)

    def test_last_two_month_trans(self):
        def case(fixture, expected):
            result = last_two_month_trans(fixture)
            self.assertEqual(expected, result)
        only_current = {
            "interfaces": [
                {
                    'traffic': {
                        'months': [
                            {"rx": 100, "tx": 100}
                        ]
                    }
                }
            ]
        }
        with_last = {
            "interfaces": [
                {
                    'traffic': {
                        'months': [
                            {"rx": 100, "tx": 100},
                            {"rx": 100, "tx": 100}
                        ]
                    }
                }
            ]
        }
        case(only_current, {'curr': '0.20', 'last': None})
        case(with_last, {'curr': '0.20', 'last': '0.20'})

    def test_month_name(self):
        import calendar
        m = datetime.now().month
        expected = calendar.month_name[m]
        result = month_name()
        self.assertEqual(expected, result)

    def test_last_month_name(self):
        import calendar
        m = (datetime.now().month - 2) % 12 + 1
        expected = calendar.month_name[m]
        result = last_month_name()
        self.assertEqual(expected, result)

    def test_vnstat(self):
        with self.assertRaises(AssertionError):
            vnstat(unit='a')
        with self.assertRaises(AssertionError):
            vnstat(unit='h', fmt='js')
        # Test only vnstat >= 1.4 is installed
        # self.assertTrue(vnstat(unit='h'))

    def test_stats_data(self):
        def case(file_name, unit, nb):
            import os
            test_dir = os.path.dirname(__file__)
            json = read_json(os.path.join(test_dir, file_name))
            dict = stats_data(json, unit)
            self.assertEqual(len(dict['labels']), nb)
            self.assertEqual(len(dict['datasets']), 4)
            ts = [len(x['transfer']) == nb for x in dict['datasets']]
            self.assertTrue(all(ts))
        case('hour.json', 'hours', 24)
        case('day.json', 'days', 18)


if __name__ == '__main__':
    unittest.main()
