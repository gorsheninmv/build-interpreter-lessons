from .token import Token
from .token_type import TokenType
from .ast import BinOp, Num

class Parser():
    def __init__(self, lexer):
        self.lexer = lexer
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
            node = Num(token)
        else:
            self.eat(TokenType.LP)
            node = self.expr()
            self.eat(TokenType.RP)

        return node

    def term(self):
        """
        term: factor((MUL|DIV)factor)*
        """
        node = self.factor()

        while True:
            token = self.cur_token

            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
                node = BinOp(left=node, token=token, right=self.factor())
            elif self.cur_token.type == TokenType.DIV:
                self.eat(TokenType.DIV)
                node = BinOp(left=node, token=token, right=self.factor())
            else:
                break

        return node

    def expr(self):
        """
        expr: term((PLUS|MINUS)term)*
        term: factor((MUL|DIV)factor)*
        factor: INTEGER | LP expr RP
        """
        node = self.term()

        while True:
            token = self.cur_token

            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
                node = BinOp(left=node, token=token, right=self.term())
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
                node = BinOp(left=node, token=token, right=self.term())
            else:
                break

        return node

    def parse(self):
        return self.expr()
