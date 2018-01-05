import unittest
import poq


class ListTest(unittest.TestCase):
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

    def test_first_level_list(self):
        result = poq.query(".[]", ListTest.LIST)
        self.assertEqual(ListTest.LIST, result)

    def test_second_level_with_key(self):
        result = poq.query(".two[]", ListTest.DICT)
        self.assertEqual(ListTest.DICT["two"], result)

    def test_second_level(self):
        result = poq.query(".[].one", ListTest.LIST)
        self.assertEqual([ListTest.DICT["one"]] * 3, result)

    def test_second_level_list(self):
        result = poq.query(".[].two", ListTest.LIST)
        self.assertEqual([ListTest.DICT["two"]] * 3, result)

    def test_second_level_flatten_list(self):
        result = poq.query(".[].two[]", ListTest.LIST)
        self.assertEqual([x for y in ListTest.LIST for x in y["two"]], result)

    def test_list_index(self):
        result = poq.query(".[1].one", ListTest.LIST)
        self.assertEqual(ListTest.LIST[1]["one"], result)
