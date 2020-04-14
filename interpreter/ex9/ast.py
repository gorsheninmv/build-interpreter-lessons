class Ast():
    pass

class Compound(Ast):
    """
    Represents a 'BEGIN ... END' block
    """
    def __init__(self):
        self.leaves = list()

class Assign(Ast):
    def __init__(self, left, token, right):
        self.left = left
        self.right = right
        self.token = token

class Var(Ast):
    def __init__(self, token):
        self.token = token

class BinOp(Ast):
    def __init__(self, left, token, right):
        self.left = left
        self.token = token
        self.right = right

class UnOp(Ast):
    def __init__(self, token, leaf):
        self.token = token
        self.leaf = leaf

class Num(Ast):
    def __init__(self, token):
        self.token = token

class NoOp(Ast):
    pass
