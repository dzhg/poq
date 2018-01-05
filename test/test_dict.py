import unittest
import poq


class DictTest(unittest.TestCase):
    DICT = {
        "one": {
            "test_1": "test_1_v",
            "test_2": "test_2_v"
        },
        "two": [
            1, 2, 3, 4, 5
        ]
    }

    def test_get_root(self):
        result = poq.query(".", DictTest.DICT)
        self.assertEqual(DictTest.DICT, result)

    def test_get_first_level_child_dict(self):
        result = poq.query(".one", DictTest.DICT)
        self.assertEqual(DictTest.DICT["one"], result)

    def test_get_first_level_child_none(self):
        result = poq.query(".zero", DictTest.DICT)
        self.assertIsNone(result)

    def test_get_first_level_child_list(self):
        result = poq.query(".two", DictTest.DICT)
        self.assertEqual(DictTest.DICT["two"], result)

    def test_get_second_level_child_dict(self):
        result = poq.query(".one.test_1", DictTest.DICT)
        self.assertEqual(DictTest.DICT["one"]["test_1"], result)

    def test_get_second_level_child_pipe(self):
        result = poq.query(".one | .test_2", DictTest.DICT)
        self.assertEqual(DictTest.DICT["one"]["test_2"], result)

    def test_get_second_level_child_none(self):
        result = poq.query(".one.test_0", DictTest.DICT)
        self.assertIsNone(result)
