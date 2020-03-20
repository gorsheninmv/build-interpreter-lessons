from .token import Token
from .token_type import TokenType

class Interpreter:
    def __init__(self, text):
        self.text = text        # client string input
        self.pos = 0            # is an index in self.text
        self.cur_token = None   # current token instance

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        """ Lexical analyzer """

        text = self.text

        if self.pos > len(text) - 1:
            return Token(TokenType.EOF, None)

        cur_char = text[self.pos]

        if cur_char.isdigit():
            token = Token(TokenType.INTEGER, int(cur_char))
            self.pos += 1
            return token

        if cur_char == '+':
            token = Token(TokenType.PLUS, cur_char)
            self.pos += 1
            return token

        self.error()

    def eat(self, token_type):
        if self.cur_token.type == token_type:
            self.cur_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """ expr -> INTEGER PLUS INTEGER """

        self.cur_token = self.get_next_token()

        left = self.cur_token
        self.eat(TokenType.INTEGER)

        op = self.cur_token
        self.eat(TokenType.PLUS)

        right = self.cur_token
        self.eat(TokenType.INTEGER)

        result = left.value + right.value
        return result
