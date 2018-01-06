import unittest
from poq.ast import PoqParser


class LexerTest(unittest.TestCase):
    def test_1(self):
        parser = PoqParser()
        parser.build()
        result = parser.test_lexer(".one.test_1")
        self.assertEqual(2, len(result))
