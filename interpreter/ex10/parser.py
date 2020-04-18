from .token import Token
from .token_type import TokenType
from .ast import *

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

    def program(self):
        """
        program : PROGRAM variable SEMI block DOT
        """

        self.eat(TokenType.PROGRAM)
        var_node = self.variable()
        self.eat(TokenType.SEMI)
        block_node = self.block()
        node = Program(variable=var_node, block=block_node)
        self.eat(TokenType.DOT)
        return node

    def block(self):
        """
        block : declarations compound_statement
        """

        decl_nodes = self.declarations()
        compound_statement_node = self.compound_statement()
        node = Block(declarations=decl_nodes, compound_statement=compound_statement_node)
        return node

    def declarations(self):
        """
        declarations : VAR (variable_declaration SEMI)+
                     | empty
        """

        declarations = []

        if self.cur_token.type == TokenType.VAR:
            self.eat(TokenType.VAR)

            while self.cur_token.type == TokenType.ID:
                var_decl = self.variable_declaration()
                self.eat(TokenType.SEMI)
                declarations.extend(var_decl)

        return declarations

    def variable_declaration(self):
        """
        variable_declaration : ID (COMMA ID)* COLON type_spec
        """

        token = self.cur_token
        self.eat(TokenType.ID)

        var_nodes = [Var(token)]

        while self.cur_token.type == TokenType.COMMA:
           self.eat(TokenType.COMMA)
           var_nodes.append(self.cur_token)
           self.eat(TokenType.ID)

        self.eat(TokenType.COLON)

        type_node = self.type_spec()

        decl_nodes = [VarDecl(var_node, type_node) for var_node in var_nodes]
        return decl_nodes

    def type_spec(self):
        """
        type_spec : INTEGER | REAL
        """

        token = self.cur_token

        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
        else:
            self.eat(TokenType.REAL)

        node = Type(token)
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
        """
        empty :
        """
        node = NoOp()
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

    def term(self):
       """
       term: factor ((MUL | INTEGER_DIV | FLOAT_DIV) factor)*
       """
       node = self.factor()

       while True:
           token = self.cur_token

           if token.type == TokenType.MUL:
               self.eat(TokenType.MUL)
               node = BinOp(left=node, token=token, right=self.factor())
           elif self.cur_token.type == TokenType.INTEGER_DIV:
               self.eat(TokenType.INTEGER_DIV)
               node = BinOp(left=node, token=token, right=self.factor())
           elif self.cur_token.type == TokenType.FLOAT_DIV:
               self.eat(TokenType.FLOAT_DIV)
               node = BinOp(left=node, token=token, right=self.factor())
           else:
               break

       return node

    def factor(self):
        """
        factor : PLUS factor
               | MINUS factor
               | INTEGER_CONST
               | REAL_CONST
               | LP expr RP
               | variable
        """
        token = self.cur_token
        if token.type in (TokenType.PLUS, TokenType.MINUS):
            self.eat(token.type)
            node = UnOp(token=token, factor=self.factor())
        elif token.type in (TokenType.INTEGER_CONST, TokenType.REAL_CONST):
            self.eat(token.type)
            node = Num(value=token.value)
        elif token.type == TokenType.LP:
            self.eat(TokenType.LP)
            node = self.expr()
            self.eat(TokenType.RP)
        else:
            node = self.variable()

        return node

    def variable(self):
        """
        variable : ID
        """
        node = Var(self.cur_token)
        self.eat(TokenType.ID)
        return node

    def parse(self):
        root = self.program()
        if self.cur_token.type != TokenType.EOF:
            self.error()

        return root
