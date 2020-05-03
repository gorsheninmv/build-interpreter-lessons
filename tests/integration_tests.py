import unittest
from interpreter import Lexer, Parser, Interpreter, SymbolTableBuilder

def interpret(text):
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()
    return interpreter.get_var_value

class IntegrationTests(unittest.TestCase):
    def test_1(self):
        program_code = r'''
        PROGRAM Part10AST;
        VAR
            a,b : INTEGER;
            y   : REAL;

        BEGIN {Part10AST}
            a := 2;
            b := 10 * a + 10 * a DIV 4;
            y := 20 / 8 + 3.14;
        END. {Part10AST}
        '''

        get_var_value = interpret(program_code)
        self.assertEqual(get_var_value('a'), 2)
        self.assertEqual(get_var_value('b'), 25)
        self.assertEqual(format(get_var_value('y'), '.2f'), str(5.64))

    def test_throws_exceptions_when_var_not_declared(self):
        program_code = r'''
        PROGRAM NameError1;
        VAR
            a : INTEGER;

        BEGIN
            a := 2 + b;
        END.
        '''

        lexer = Lexer(program_code)
        parser = Parser(lexer)
        tree = parser.parse()
        symtab_builder = SymbolTableBuilder()
        with self.assertRaises(NameError) as context:
            symtab_builder.visit(tree)

    def test_throws_exceptions_when_var_not_declared_2(self):
        program_code = r'''
        PROGRAM NameError2;
        VAR
            b : INTEGER;

        BEGIN
            b := 1;
            a := b + 2;
        END.
        '''

        lexer = Lexer(program_code)
        parser = Parser(lexer)
        tree = parser.parse()
        symtab_builder = SymbolTableBuilder()
        with self.assertRaises(NameError) as context:
            symtab_builder.visit(tree)
