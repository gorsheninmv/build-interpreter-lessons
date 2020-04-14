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
        begin
            BEGIN
                number := 2;
                __a := NumBer;
                B := 10 * __a + 10 * NUMBER DiV 4;
                c := __a - - b
            end;

            x := 11
        END.
        '''

        get_var_value = interpret(program_code)
        self.assertEqual(get_var_value('__a'), 2)
        self.assertEqual(get_var_value('x'), 11)
        self.assertEqual(get_var_value('c'), 27)
        self.assertEqual(get_var_value('b'), 25)
        self.assertEqual(get_var_value('number'), 2)
