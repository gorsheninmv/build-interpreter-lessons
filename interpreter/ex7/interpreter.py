from .visitor import NodeVisitor
from .token_type import TokenType

class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser

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
    
    def interpret(self):
        ast = self.parser.parse()
        return self.visit(ast)
