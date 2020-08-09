from .visitor import NodeVisitor

class RPNTranslator(NodeVisitor):
    """
    Reverse Polish Notation visitor
    """

    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return ' '.join([left, right, node.token.value])

    def visit_Num(self, node):
        return str(node.token.value)

    def translate(self):
        ast = self.parser.parse()
        return self.visit(ast)
