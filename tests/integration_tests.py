import unittest
from interpreter import Lexer, Parser, Interpreter

def interpret(text):
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    return interpreter.interpret()

class IntegrationTests(unittest.TestCase):
    def test_1(self):
        self.assertEqual(interpret('-5'), -5)

    def test_2(self):
        self.assertEqual(interpret('---5'), -5)

    def test_3(self):
        self.assertEqual(interpret('5---5'), 0)
