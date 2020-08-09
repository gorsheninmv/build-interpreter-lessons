from .visitor import NodeVisitor
from .token_type import TokenType
from .memory import CallStack, ActivationRecord, ARType
from .ast import *

SHOULD_LOG_STACK = False

def enable_log():
    global SHOULD_LOG_STACK
    SHOULD_LOG_STACK = True

class Interpreter(NodeVisitor):
    def __init__(self, ast):
        self.ast = ast
        self.call_stack = CallStack()

    def get_var_value(self, var_name):
        var_name = var_name.upper()
        ar = self.call_stack.peek()
        return self.ar.get(var_name)

    def log(self, msg):
        if SHOULD_LOG_STACK:
            print(msg)

    def visit_Program(self, node):
        program_name = node.variable.token.value

        ar = ActivationRecord(
                name=program_name,
                type=ARType.PROGRAM,
                nesting_level=1
                )
        self.call_stack.push(ar)

        self.log(f'ENTER: PROGRAM {program_name}')
        self.log(self.call_stack)

        self.visit(node.block)

        self.log(f'LEAVE: PROGRAM {program_name}')
        self.log(self.call_stack)

        self.call_stack.pop()

    def visit_Block(self, node):
        for decl in node.declarations:
            self.visit(decl)
        self.visit(node.compound_statement)

    def visit_VarDecl(self, node):
        pass

    def visit_ProcDecl(self, node):
        pass

    def visit_ProcCall(self, node: ProcCall):
        proc_name = node.name
        proc_symbol = node.symbol

        ar = ActivationRecord(
                name=proc_name,
                type = ARType.PROCEDURE,
                nesting_level=proc_symbol.scope_level+1,)

        formal_params = proc_symbol.params
        actual_params = node.actual_params

        for param_symbol, argument_node in zip(formal_params, actual_params):
            ar[param_symbol.name] = self.visit(argument_node)

        self.call_stack.push(ar)
        self.log(f'ENTER: PROCEDURE {proc_name}')
        self.log(self.call_stack)

        self.visit(proc_symbol.body)

        self.log(f'LEAVE: PROCEDURE {proc_name}')
        self.log(self.call_stack)
        self.call_stack.pop()

    def visit_Type(self, node):
        pass

    def visit_Compound(self, node):
        for leaf in node.leaves:
            self.visit(leaf)

    def visit_Assign(self, node):
        var_tok = node.left.token
        var_nam = var_tok.value
        var_val = self.visit(node.right)
        ar = self.call_stack.peek()
        ar[var_nam] = var_val

    def visit_Var(self, node):
        ar = self.call_stack.peek()
        var_nam = node.token.value
        var_val = ar.get(var_nam)

        if var_val is None:
            raise NameError(repr(var_nam))
        else:
            return var_val

    def visit_NoOp(self, node):
        pass

    def visit_BinOp(self, node):
        if node.token.type == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.token.type == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.token.type == TokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.token.type == TokenType.INTEGER_DIV:
            return self.visit(node.left) // self.visit(node.right)
        elif node.token.type == TokenType.FLOAT_DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def visit_UnOp(self, node):
        value = self.visit(node.factor)
        if node.token.type == TokenType.MINUS:
            return -value
        elif node.token.type == TokenType.PLUS:
            return value

    def interpret(self):
        self.visit(self.ast)
