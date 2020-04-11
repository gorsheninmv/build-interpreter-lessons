from .token_type import TokenType
from .token import Token

class Lexer:
    def __init__(self, text):
        self.text = text                                  # client string input
        self.len = len(self.text)                         # input length
        self.cur_pos = 0                                  # is an index in self.text
        self.cur_char = self.text[self.cur_pos] if self.len > 0 else None

    def error(self, ch):
        raise Exception(f'Invalid character "{ch}"')

    def advance(self):
        self.cur_pos += 1
        self.cur_char = self.text[self.cur_pos] if self.cur_pos < self.len else None

    def skip_whitespace(self):
        while self.cur_char is not None and self.cur_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.cur_char is not None and self.cur_char.isdigit():
            result += self.cur_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.cur_char is not None:

            if self.cur_char.isspace():
                self.skip_whitespace()
                continue

            if self.cur_char.isdigit():
                return Token(TokenType.INTEGER, self.integer())

            if self.cur_char == '*':
                self.advance()
                return Token(TokenType.MUL, '*')

            if self.cur_char == '/':
                self.advance()
                return Token(TokenType.DIV, '/')

            if self.cur_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+')

            if self.cur_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-')

            if self.cur_char == '(':
                self.advance()
                return Token(TokenType.LP, '(')

            if self.cur_char == ')':
                self.advance()
                return Token(TokenType.RP, ')')

            self.error(self.cur_char)

        return Token(TokenType.EOF, None)
