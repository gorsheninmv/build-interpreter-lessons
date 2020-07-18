from .visitor import NodeVisitor

class LNTranslator(NodeVisitor):
    """
    LISP Notation visitor
    """

    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        ret = ' '.join([node.token.value, left, right])
        return ''.join(['(', ret, ')'])

    def visit_Num(self, node):
        return str(node.token.value)

    def translate(self):
        ast = self.parser.parse()
        return self.visit(ast)
