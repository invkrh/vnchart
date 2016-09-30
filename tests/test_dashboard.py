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
        with self.assertRaises(ValueError):
            stats_data(None, 'unknown')

        def case(file_name, unit, nb):
            import os
            test_dir = os.path.dirname(__file__)
            vnstat_json = read_json(os.path.join(test_dir, file_name))
            ret_dict = stats_data(vnstat_json, unit)
            self.assertEqual(len(ret_dict['labels']), nb + 1)
            self.assertEqual(len(ret_dict['datasets']), 4)
            ts = [len(x['transfer']) == nb for x in ret_dict['datasets']]
            self.assertTrue(all(ts))
        case('hour.json', 'hours', 24)
        case('day.json', 'days', 18)

    def test_error_page(self):
        with app.app_context():
            msg = "test"
            self.assertTrue(msg in error_page(msg))

    def test_dashboard(self):
        with app.app_context():
            with self.assertRaises(ValueError):
                dashboard("unknow")
            self.assertTrue('1134.35' in dashboard("demo"))
            self.assertTrue('Error' not in dashboard(""))


if __name__ == '__main__':
    unittest.main()
