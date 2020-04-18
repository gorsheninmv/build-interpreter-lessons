import unittest
from interpreter import Lexer, Parser, Interpreter

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
