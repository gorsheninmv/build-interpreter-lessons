SHOULD_LOG_SCOPE = False

def enable_log():
    global SHOULD_LOG_SCOPE
    SHOULD_LOG_SCOPE = True


# Symbols region {{{
class Symbol:
    def __init__(self, name, type=None):
        self.name = name
        self.type = type


class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<{self.__class__.__name__}(name="{self.name}")>'


class VarSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type)

    def __str__(self):
        return f'{self.name}: <{self.type}>'

    def __repr__(self):
        return f'<{self.__class__.__name__}(name="{self.name}", type="{self.type}")>'


class ProcSymbol(Symbol):
    def __init__(self, name, params=[]):
        super().__init__(name)
        self.params = params

    def __repr__(self):
        return f'<{self.__class__.__name__}(name="{self.name}", params="{self.params}")>'

# }}}


# ScopedSymbolTable region {{{
from collections import OrderedDict

class ScopedSymbolTable:
    def __init__(self, scope_name, scope_level, enclosing_scope=None):
        self.__symbols = OrderedDict()
        self.scope_name = scope_name
        self.scope_level = scope_level
        self.enclosing_scope = enclosing_scope

        self.insert(BuiltinTypeSymbol('INTEGER'))
        self.insert(BuiltinTypeSymbol('REAL'))

    def __repr__(self):
        h1 = 'SCOPE (SCOPED SYMBOL TABLE)'
        lines = ['\n', h1, '='*len(h1)]
        encl_scope_name = self.enclosing_scope.scope_name if self.enclosing_scope else None
        headers = (('Scope name', self.scope_name),
                   ('Scope level', self.scope_level),
                   ('Enclosing scope', encl_scope_name))

        for header_name, header_value in headers:
            lines.append(f'{header_name:15}: {header_value}')

        h2 = 'Scope (Scoped symbol table contents)'
        lines.extend((h2, '-'*len(h2)))
        lines.extend((f'{key:>7}: {value!r}') for key, value in self.__symbols.items())
        lines.append('\n')
        s = '\n'.join(lines)
        return s

    def insert(self, symbol):
        self.__symbols[symbol.name] = symbol

    def try_lookup(self, name, current_scope_only=False):
        symbol = self.__symbols.get(name)

        if symbol is not None or current_scope_only:
            return symbol
        else:
            if self.enclosing_scope is not None:
                return self.enclosing_scope.try_lookup(name)
            else:
                return None

    def log(self, msg):
        if SHOULD_LOG_SCOPE:
            print(msg)
# }}}


# SemanticAnalyzer region {{{
from .visitor import NodeVisitor
from . import ast
from .error import SemanticError, ErrorCode
from .token import Token

class SemanticAnalyzer(NodeVisitor):
    def __init__(self):
        self.current_scope = None

    def error(self, error_code: ErrorCode, token: Token):
        raise SemanticError(
                error_code=error_code,
                token=token,
                message=f'{error_code.value} -> {token}',
                )

    def visit_Program(self, node):
        self.log('Enter scope: global')
        global_scope = ScopedSymbolTable(
                scope_name='global',
                scope_level=1,
                enclosing_scope=self.current_scope,
        )
        self.current_scope = global_scope
        self.visit(node.block)
        self.log(global_scope)
        self.current_scope = self.current_scope.enclosing_scope
        self.log('Leave scope: global')

    def visit_Block(self, node):
        for decl in node.declarations:
            self.visit(decl)
        self.visit(node.compound_statement)

    def visit_VarDecl(self, node: ast.VarDecl):
        type_name = node.type.token.value
        type_symbol = self.current_scope.try_lookup(type_name)
        var_name = node.name.token.value
        var_symbol = VarSymbol(var_name, type_name)

        if self.current_scope.try_lookup(var_name, current_scope_only=True) is None:
            self.current_scope.insert(var_symbol)
        else:
            self.error(
                    error_code=ErrorCode.DUPLICATE_ID,
                    token=node.name,
                    )

    def visit_ProcDecl(self, node: ast.ProcDecl):
        proc_name = node.name
        proc_symbol = ProcSymbol(proc_name)
        self.current_scope.insert(proc_symbol)

        self.log(f'Enter scope {proc_name}')
        proc_scope = ScopedSymbolTable(
                scope_name=proc_name,
                scope_level=2,
                enclosing_scope=self.current_scope,)
        self.current_scope = proc_scope
        
        for param in node.params:
            type_name = param.type_node.token.value
            type_symbol = self.current_scope.try_lookup(type_name)
            var_name = param.var_node.token.value
            var_symbol = VarSymbol(var_name, type_name)
            proc_symbol.params.append(var_symbol)
            self.current_scope.insert(var_symbol)

        self.visit(node.body)
        self.log(proc_scope)
        self.current_scope = self.current_scope.enclosing_scope
        self.log(f'Leave scope {proc_name}')

    def visit_ProcCall(self, node: ast.ProcCall):
        proc_symbol = self.current_scope.try_lookup(node.name)

        if proc_symbol is not None:
            if len(proc_symbol.params) == len(node.actual_params):
                # All right, do nothing
                pass
            else:
                self.error(
                        error_code=ErrorCode.PARAMS_COUNT_MISMATCH,
                        token=node.token
                        )
        else:
            self.error(
                    error_code=ErrorCode.ID_NOT_FOUND,
                    token=node.token,
                    )

        for param_node in node.actual_params:
            self.visit(param_node)

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
        var_symbol = self.current_scope.try_lookup(var_name)

        if var_symbol is None:
            self.error(
                    error_code=ErrorCode.ID_NOT_FOUND,
                    token=node.token,
                    )

    def visit_NoOp(self, node):
        pass

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Num(self, node):
        pass

    def visit_UnOp(self, node):
        self.visit(node.factor)

    def log(self, msg):
        if SHOULD_LOG_SCOPE:
            print(msg)
# }}}
