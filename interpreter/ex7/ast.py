class Ast():
    pass

class BinOp(Ast):
    def __init__(self, left, token, right):
        self.left = left
        self.token = token
        self.right = right

class Num(Ast):
    def __init__(self, token):
        self.token = token
