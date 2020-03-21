from .token import Token
from .token_type import TokenType

class Interpreter:
    def __init__(self, text):
        self.text = text                                  # client string input
        self.len = len(self.text)                         # input length
        self.cur_pos = 0                                  # is an index in self.text
        self.cur_token = Token(TokenType.NUL, None)       # current token instance
        self.cur_char = self.text[self.cur_pos] if self.len > 0 else None

    def error(self):
        raise Exception('Error parsing input')

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
        """ Lexical analyzer """

        while self.cur_char is not None:

            if self.cur_char.isspace():
                self.skip_whitespace()
                continue

            if self.cur_char.isdigit():
                return Token(TokenType.INTEGER, self.integer())

            if self.cur_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+')

            if self.cur_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-')

            self.error()

        return Token(TokenType.EOF, None)

    def eat(self, token_type):
        if self.cur_token.type == token_type:
            self.cur_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """
        expr -> INTEGER PLUS INTEGER
        expr -> INTEGER MINUS INTEGER
        """

        self.eat(TokenType.NUL)

        left = self.cur_token
        self.eat(TokenType.INTEGER)

        op = self.cur_token

        if op.type == TokenType.PLUS:
            self.eat(TokenType.PLUS)
        else:
            self.eat(TokenType.MINUS)

        right = self.cur_token
        self.eat(TokenType.INTEGER)

        if op.type == TokenType.PLUS:
            result = left.value + right.value
        else:
            result = left.value - right.value

        return result
