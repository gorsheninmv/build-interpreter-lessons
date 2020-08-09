from .token_type import TokenType
from .token import Token
from . import error

def build_reserved_keywords() -> dict:
    tok_list = list(TokenType)
    begin = tok_list.index(TokenType.RESERVED_INF) + 1
    end = tok_list.index(TokenType.RESERVED_SUP)
    reserved_keywords = {tok_type.value: tok_type
            for tok_type in tok_list[begin:end]}
    return reserved_keywords


class Lexer:
    RESERVED_ID_TOKENS = build_reserved_keywords().get

    def __init__(self, text):
        self.text = text                                  # client string input
        self.len = len(self.text)                         # input length
        self.cur_pos = 0                                  # is an index in self.text
        self.cur_char = self.text[self.cur_pos] if self.len > 0 else None
        self.lineno = 1                                   # curent line
        self.column = 1                                   # curent column

    def error(self):
        s = f"Lexer error on '{self.cur_char}' line: {self.lineno} column: {self.column}"
        raise error.LexerError(message=s)

    def advance(self):
        if self.cur_char == '\n':
            self.lineno += 1
            self.column = 0
            
        self.cur_pos += 1

        if self.cur_pos < self.len:
            self.cur_char = self.text[self.cur_pos]
            self.column += 1
        else:
            self.cur_char = None

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
        ret = Token(type=None, value=None, lineno=self.lineno, column= self.column)
        keyword = ''
        while (self.cur_char is not None and
                (self.cur_char.isalnum() or
                    self.cur_char == '_')):
            keyword += self.cur_char
            self.advance()

        keyword = keyword.upper()
        token_type = self.RESERVED_ID_TOKENS(keyword)
        
        if token_type is None:
            ret.type = TokenType.ID
            ret.value = keyword
        else:
            ret.type = token_type
            ret.value = token_type.value

        return ret

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

            try:
                token_type = TokenType(self.cur_char)
            except ValueError:
                self.error()
            else:
                token = Token(
                        type=token_type,
                        value=token_type.value,
                        lineno=self.lineno,
                        column=self.column,)
                self.advance()
                return token

        return Token(TokenType.EOF, None)
