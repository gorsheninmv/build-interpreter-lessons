import unittest
from interpreter.ex7 import Lexer, Parser, LNTranslator

def infix2lisp(text):
    lexer = Lexer(text)
    parser = Parser(lexer)
    translator = LNTranslator(parser)
    return translator.translate()

class LNTranslatorTests(unittest.TestCase):
    def test_1(self):
        self.assertEqual(infix2lisp('1 + 2'), '(+ 1 2)')

    def test_2(self):
        self.assertEqual(infix2lisp('2 * 7'), '(* 2 7)')

    def test_3(self):
        self.assertEqual(infix2lisp('2 * 7 + 3'), '(+ (* 2 7) 3)')

    def test_4(self):
        self.assertEqual(infix2lisp('2 + 3 * 5'), '(+ 2 (* 3 5))')

    def test_5(self):
        self.assertEqual(infix2lisp('7 + 5 * 2 - 3'), '(- (+ 7 (* 5 2)) 3)')

    def test_6(self):
        self.assertEqual(
            infix2lisp('1 + 2 + 3 + 4 + 5'),
            '(+ (+ (+ (+ 1 2) 3) 4) 5)'
        )
