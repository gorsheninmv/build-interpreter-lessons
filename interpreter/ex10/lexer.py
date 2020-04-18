from .token_type import TokenType
from .token import Token

class Lexer:
    RESERVED_ID_TOKENS = {
            'PROGRAM': Token(TokenType.PROGRAM, 'PROGRAM'),
            'VAR': Token(TokenType.VAR, 'VAR'),
            'INTEGER': Token(TokenType.INTEGER, 'INTEGER'),
            'REAL': Token(TokenType.REAL, 'REAL'),
            'BEGIN': Token(TokenType.BEGIN, 'BEGIN'),
            'END': Token(TokenType.END, 'END'),
            'DIV': Token(TokenType.INTEGER_DIV, 'INTEGER_DIV')
                      }.get

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

    def skip_comment(self):
        while self.cur_char != '}':
            self.advance()
        self.advance()

    def number(self):
        result = ''
        while self.cur_char is not None and self.cur_char.isdigit():
            result += self.cur_char
            self.advance()

        if self.cur_char == '.':
            result += self.cur_char
            self.advance()

            while (
                self.cur_char is not None and
                self.cur_char.isdigit()
                ):
                result += self.cur_char
                self.advance()

            token = Token(TokenType.REAL_CONST, float(result))
        else:
            token = Token(TokenType.INTEGER_CONST, int(result))

        return token

    def peek(self):
        peek_pos = self.cur_pos + 1
        if peek_pos > self.len - 1:
            return None
        else:
            return self.text[peek_pos]

    def id(self):
        keyword = ''
        while (self.cur_char is not None and
                (self.cur_char.isalnum() or
                    self.cur_char == '_')):
            keyword += self.cur_char
            self.advance()

        keyword = keyword.upper()
        reserved_token = self.RESERVED_ID_TOKENS(keyword)
        token = reserved_token if reserved_token is not None else Token(TokenType.ID, keyword)
        return token

    def get_next_token(self):
        while self.cur_char is not None:

            if self.cur_char.isspace():
                self.skip_whitespace()
                continue

            if self.cur_char == '{':
                self.skip_comment()
                continue

            if self.cur_char.isdigit():
                return self.number()

            if (self.cur_char.isalpha() or
                self.cur_char == '_'):
                return self.id()

            if self.cur_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.ASSIGN, ':=')

            if self.cur_char == ':':
                self.advance()
                return Token(TokenType.COLON, ':')

            if self.cur_char == ';':
                self.advance()
                return Token(TokenType.SEMI, ';')

            if self.cur_char == ',':
                self.advance()
                return Token(TokenType.COMMA, ',')

            if self.cur_char == '.':
                self.advance()
                return Token(TokenType.DOT, '.')

            if self.cur_char == '*':
                self.advance()
                return Token(TokenType.MUL, '*')

            if self.cur_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+')

            if self.cur_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-')

            if self.cur_char == '/':
                self.advance()
                return Token(TokenType.FLOAT_DIV, '/')

            if self.cur_char == '(':
                self.advance()
                return Token(TokenType.LP, '(')

            if self.cur_char == ')':
                self.advance()
                return Token(TokenType.RP, ')')

            if (self.cur_char == '.'):
                self.advance()
                return Token(TokenType.DOT, '.')

            
            self.error(self.cur_char)

        return Token(TokenType.EOF, None)
