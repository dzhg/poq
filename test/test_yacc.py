import unittest
from poq.ast import PoqParser


class YaccTest(unittest.TestCase):
    def test_1(self):
        parser = PoqParser()
        parser.build()
        result = parser.test_yacc(".one.test_1")
        self.assertIsNotNone(result)
