import unittest
import json

from vnchart.dashboard import *


class TestApp(unittest.TestCase):

    def test_kb_to_mb(self):
        # with two digits
        result = kb_to_mb(1024)
        expected = '1.00'
        self.assertEqual(expected, result)

    def test_current_usage(self):
        fixture = {
            "interfaces": [
                {
                    'traffic': {
                        'months': [
                            {
                                "rx": 100,
                                "tx": 100,
                            }
                        ]
                    }
                }
            ]
        }
        result = current_usage(fixture)
        expected = '0.20'
        self.assertEqual(expected, result)

if __name__ == '__main__':
    unittest.main()
