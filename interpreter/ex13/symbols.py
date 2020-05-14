# Symbols region {{{
class Symbol:
    def __init__(self, name, type=None):
        self.name = name
        self.type = type


class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __repr__(self):
        return self.name


class VarSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type)

    def __repr__(self):
        return f'<{self.name}:{self.type}>'
# }}}


# SymbolTable region {{{
from collections import OrderedDict

class SymbolTable():
    def __init__(self):
        self.symbols = OrderedDict()

        self.define(BuiltinTypeSymbol('INTEGER'))
        self.define(BuiltinTypeSymbol('REAL'))

    def __repr__(self):
        symbols = [value for value in self.symbols.values()]
        return f'Symbols: {symbols}'

    def define(self, symbol):
        print(f'Define: {symbol}')
        self.symbols[symbol.name] = symbol

    def lookup(self, name):
        print(f'Lookup: {name}')
        symbol = self.symbols.get(name)
        return symbol
# }}}


# SemanticAnalyzer region {{{
from .visitor import NodeVisitor

class SemanticAnalyzer(NodeVisitor):
    def __init__(self):
        self.symtab = SymbolTable()

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_Block(self, node):
        for decl in node.declarations:
            self.visit(decl)
        self.visit(node.compound_statement)

    def visit_VarDecl(self, node):
        type_name = node.type.token.value
        type_symbol = self.symtab.lookup(type_name)
        var_name = node.id.token.value
        var_symbol = VarSymbol(var_name, type_name)

        if self.symtab.lookup(var_name) is None:
            self.symtab.define(var_symbol)
        else:
            raise Exception(f'Duplicate identifier {var_name}')

    def visit_ProcDecl(self, node):
        pass

    def visit_Type(self, node):
        pass

    def visit_Compound(self, node):
        for leaf in node.leaves:
            self.visit(leaf)

    def visit_Assign(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Var(self, node):
        var_name = node.token.value
        var_symbol = self.symtab.lookup(var_name)

        if var_symbol is None:
            raise Exception(f'Symbol not found {var_name}')

    def visit_NoOp(self, node):
        pass

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)
        
    def visit_Num(self, node):
        pass

    def visit_UnOp(self, node):
        self.visit(node.factor)
# }}}
