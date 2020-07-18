class NodeVisitor:
    def generic_visit(self, node):
        node_type = type(node).__name__
        raise Exception(f'No visit_{node_type} method')

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
