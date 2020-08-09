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
    def __init__(self, name, type):
        self.name = name
        self.type = type

class ProcDecl(Ast):
    """
    A procedure node

    name    -- procedure`s identifier
    params  -- procedure`s params
    body    -- procedure`s body
    """

    def __init__(self, name, body, params=[]):
        self.name = name
        self.params = params
        self.body = body

class ProcCall(Ast):
    """
    A procedure call node

    name    -- procedure`s identifier
    params  -- procedure`s actual params list
    token   -- associated token
    symbol  -- associated procedure symbol
    """
    def __init__(self, name, actual_params, token):
        self.name = name
        self.actual_params = actual_params
        self.token = token
        self.symbol = None

class Param(Ast):
    """
    Procedure param node

    var_node    -- node that represents variable
    type_node   -- node that represents variable type
    """

    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node

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
