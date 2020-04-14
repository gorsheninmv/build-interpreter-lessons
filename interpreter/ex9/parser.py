from .token import Token
from .token_type import TokenType
from .ast import Compound, Assign, Var, BinOp, UnOp, Num, NoOp

class Parser():
    """
    program : compound_statement DOT

    compound_statement : BEGIN statement_list END

    statement_list : statement
                   | statement SEMI statement_list

    statement : compound_statement
              | assignment_statement
              | empty

    assignment_statement : variable ASSIGN expr

    empty:

    expr: term ((PLUS | MINUS) term)*

    term: factor ((MUL | DIV) factor)*

    factor : PLUS factor
           | MINUS factor
           | INTEGER
           | LP expr RP
           | variable

    variable : ID
    """
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

    def program(self):
        """
        program : compound_statement DOT
        """
        node = self.compound_statement()
        self.eat(TokenType.DOT)
        return node

    def compound_statement(self):
        """
        compound_statement: BEGIN statement_list END
        """
        self.eat(TokenType.BEGIN)
        nodes = self.statement_list()
        self.eat(TokenType.END)

        root = Compound()
        for node in nodes:
            root.leaves.append(node)

        return root

    def statement_list(self):
        """
        statement_list : statement
                       | statement SEMI statement_list
        """

        node = self.statement()
        nodes = [node]

        while self.cur_token.type == TokenType.SEMI:
            self.eat(TokenType.SEMI)
            nodes.append(self.statement())

        return nodes

    def statement(self):
        """
        statement : compound_statement
                  | assignment_statement
                  | empty
        """
        if self.cur_token.type == TokenType.BEGIN:
            node = self.compound_statement()
        elif self.cur_token.type == TokenType.ID:
            node = self.assignment_statement()
        else:
            node = self.empty()

        return node

    def assignment_statement(self):
        """
        assignment_statement : variable ASSIGN expr
        """
        left = self.variable()
        self.eat(TokenType.ASSIGN)
        right = self.expr()
        token = self.cur_token
        node = Assign(left=left, token=token, right=right)

        return node

    def empty(self):
        node = NoOp()
        return node

    def variable(self):
        node = Var(self.cur_token)
        self.eat(TokenType.ID)
        return node

    def factor(self):
        """
        factor : PLUS factor
               | MINUS factor
               | INTEGER
               | LP expr RP
               | variable
        """
        token = self.cur_token
        if token.type in (TokenType.PLUS, TokenType.MINUS):
            self.eat(token.type)
            node = UnOp(token=token, leaf=self.factor())
        elif token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            node = Num(token)
        elif token.type == TokenType.LP:
            self.eat(TokenType.LP)
            node = self.expr()
            self.eat(TokenType.RP)
        else:
            node = self.variable()

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
        root = self.program()
        if self.cur_token.type != TokenType.EOF:
            self.error()

        return root
