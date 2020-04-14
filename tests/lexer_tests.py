import unittest
from interpreter.ex9.lexer import Lexer
from interpreter.ex9.token_type import TokenType
from interpreter.ex9.token import Token

class LexerTests(unittest.TestCase):
    def test_1(self):
        text = 'BEGIN a := 2; END.'
        lexer = Lexer(text)

        token = lexer.get_next_token()
        self.assertEqual(token, Token(TokenType.BEGIN, 'BEGIN'))

        token = lexer.get_next_token()
        self.assertEqual(token, Token(TokenType.ID, 'A'))

        token = lexer.get_next_token()
        self.assertEqual(token, Token(TokenType.ASSIGN, ':='))

        token = lexer.get_next_token()
        self.assertEqual(token, Token(TokenType.INTEGER, 2))

        token = lexer.get_next_token()
        self.assertEqual(token, Token(TokenType.SEMI, ';'))

        token = lexer.get_next_token()
        self.assertEqual(token, Token(TokenType.END, 'END'))
        
        token = lexer.get_next_token()
        self.assertEqual(token, Token(TokenType.DOT, '.'))

        token = lexer.get_next_token()
        self.assertEqual(token, Token(TokenType.EOF, None))
