import unittest
from interpreter.ex7 import Lexer, Parser, RPNTranslator

def infix2postfix(text):
    lexer = Lexer(text)
    parser = Parser(lexer)
    translator = RPNTranslator(parser)
    return translator.translate()

class RPNTranslatorTests(unittest.TestCase):
    def test_1(self):
            self.assertEqual(infix2postfix('2 + 3'), '2 3 +')

    def test_2(self):
        self.assertEqual(infix2postfix('2 + 3 * 5'), '2 3 5 * +')

    def test_3(self):
        self.assertEqual(
            infix2postfix('5 + ((1 + 2) * 4) - 3'),
            '5 1 2 + 4 * + 3 -',
        )

    def test_4(self):
        self.assertEqual(
            infix2postfix('(5 + 3) * 12 / 3'),
            '5 3 + 12 * 3 /',
        )
