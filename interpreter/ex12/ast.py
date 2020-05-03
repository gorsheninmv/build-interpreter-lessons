class Ast():
    pass

class Program(Ast):
    def __init__(self, variable, block):
        self.variable = variable
        self.block = block
        
class Block(Ast):
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement

class VarDecl(Ast):
    def __init__(self, ids, type):
        self.ids = ids
        self.type = type

class ProcDecl(Ast):
    """
    A procedure node

    id -- procedure identifier
    body -- procedure`s body
    """
    def __init__(self, id, body):
        self.id = id
        self.body = body

class Type(Ast):
    def __init__(self, token):
        self.token = token

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
    def __init__(self, token, factor):
        self.token = token
        self.factor = factor

class Num(Ast):
    def __init__(self, value):
        self.value = value

class NoOp(Ast):
    pass
