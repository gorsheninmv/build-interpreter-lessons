from .token import Token
from .token_type import TokenType
from .lexer import Lexer

class Interpreter:
    def __init__(self, text):
        self.lexer = Lexer(text)
        self.cur_token = self.lexer.get_next_token()

    def error(self, msg):
        raise Exception('\n'.join(['Invalid syntax', msg]))

    def eat(self, token_type):
        if self.cur_token.type == token_type:
            self.cur_token = self.lexer.get_next_token()
        else:
            self.error(f'expected {token_type}, but {self.cur_token.type} received.')

    def factor(self):
        """
        factor: INTEGER | LP expr RP
        """
        token = self.cur_token
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return token.value
        else:
            self.eat(TokenType.LP)
            result = self.expr()
            self.eat(TokenType.RP)
            return result

    def term(self):
        """
        term: factor((MUL|DIV)factor)*
        """
        result = self.factor()

        while True:
            if self.cur_token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
                result *= self.factor()
            elif self.cur_token.type == TokenType.DIV:
                self.eat(TokenType.DIV)
                result //= self.factor()
            else:
                break

        return result

    def expr(self):
        """
        expr: term((PLUS|MINUS)term)*
        term: factor((MUL|DIV)factor)*
        factor: INTEGER | LP expr RP
        """
        result = self.term()

        while True:
            if self.cur_token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
                result += self.term()
            elif self.cur_token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
                result -= self.term()
            else:
                break

        return result
