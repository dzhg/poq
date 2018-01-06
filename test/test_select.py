import unittest
import poq


class SelectTest(unittest.TestCase):
    DICT = {
        "one": {
            "test_1": "test_1_v",
            "test_2": "test_2_v"
        },
        "two": [
            1, 2, 3, 4, 5
        ]
    }

    LIST = [
        DICT, DICT, DICT
    ]

    def test_select_first_level(self):
        result = poq.query('.[] | select(.one.test_1 == "test_1_v")', SelectTest.LIST)
        self.assertEqual(SelectTest.LIST, result)
