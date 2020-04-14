from .visitor import NodeVisitor
from .token_type import TokenType

class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.__global_scope = {}

    def get_var_value(self, var_name):
        var_name = var_name.upper()
        return self.__global_scope.get(var_name)
            
    def visit_Compound(self, node):
        for leaf in node.leaves:
            self.visit(leaf)

    def visit_Assign(self, node):
        var_token = node.left.token
        var_name = var_token.value
        self.__global_scope[var_name] = self.visit(node.right)

    def visit_Var(self, node):
        var_name = node.token.value
        var_value = self.__global_scope.get(var_name)

        if var_value is None:
            raise NameError(repr(var_name))
        else:
            return var_value
    
    def visit_NoOp(self, node):
        pass

    def visit_BinOp(self, node):
        if node.token.type == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.token.type == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.token.type == TokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.token.type == TokenType.DIV:
            return self.visit(node.left) // self.visit(node.right)
        
    def visit_Num(self, node):
        return node.token.value

    def visit_UnOp(self, node):
        value = self.visit(node.leaf)
        if node.token.type == TokenType.MINUS:
            return -value
        elif node.token.type == TokenType.PLUS:
            return value
        
    def interpret(self):
        ast = self.parser.parse()
        self.visit(ast)
