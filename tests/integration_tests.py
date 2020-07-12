import unittest
from interpreter import Lexer, Parser, Interpreter, SemanticAnalyzer, enable_log

def interpret(text):
    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    interpreter = Interpreter(tree)
    interpreter.interpret()
    return interpreter.get_var_value

class IntegrationTests(unittest.TestCase):
    def setUp(self):
        enable_log()

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
        semantic_analyzer = SemanticAnalyzer()
        with self.assertRaises(Exception) as context:
            semantic_analyzer.visit(tree)

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
        semantic_analyzer = SemanticAnalyzer()
        with self.assertRaises(Exception) as context:
            semantic_analyzer.visit(tree)

    def test_throws_exceptions_when_duplicate_declaration(self):
        print('run test')
        program_code = r'''
        PROGRAM NameError2;
            VAR a, b : INTEGER;
            VAR b : REAL;

        BEGIN
            a := a + b;
        END.
        '''

        lexer = Lexer(program_code)
        parser = Parser(lexer)
        tree = parser.parse()
        semantic_analyzer = SemanticAnalyzer()
        with self.assertRaises(Exception) as context:
            semantic_analyzer.visit(tree)

    def test_output_1(self):
        program_code = r'''
        PROGRAM Part10;
        VAR
           number     : INTEGER;
           a, b, c, x : INTEGER;
           y          : REAL;
        
        BEGIN {Part10}
           BEGIN
              number := 2;
              a := number;
              b := 10 * a + 10 * number DIV 4;
              c := a - - b
           END;
           x := 11;
           y := 20 / 7 + 3.14;
           { writeln('a = ', a); }
           { writeln('b = ', b); }
           { writeln('c = ', c); }
           { writeln('number = ', number); }
           { writeln('x = ', x); }
           { writeln('y = ', y); }
        END.  {Part10}
        '''

        lexer = Lexer(program_code)
        parser = Parser(lexer)
        tree = parser.parse()
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.visit(tree)
        interpreter = Interpreter(tree)
        interpreter.interpret()
        print(interpreter.get_var_value('a'))
        print(interpreter.get_var_value('b'))
        print(interpreter.get_var_value('c'))
        print(interpreter.get_var_value('number'))
        print(interpreter.get_var_value('x'))
        print(interpreter.get_var_value('y'))

    def test_proc_call(self):
        program_code = r'''
        program Main;

        procedure Alpha(a : integer; b : integer);
        var x : integer;
        begin
           x := (a + b ) * 2;
        end;

        begin { Main }

           Alpha(3 + 5, 7);  { procedure call }

        end.  { Main }
        '''
        lexer = Lexer(program_code)
        parser = Parser(lexer)
        tree = parser.parse()
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.visit(tree)
        interpreter = Interpreter(tree)
        interpreter.interpret()

    def test_proc_call_throws_error_when_params_count_mismatch(self):
        program_code = r'''
        program Main;

        procedure Alpha(a : integer; b : integer);
        var x : integer;
        begin
           x := (a + b ) * 2;
        end;

        begin { Main }

           Alpha(7);  { procedure call }

        end.  { Main }
        '''
        lexer = Lexer(program_code)
        parser = Parser(lexer)
        tree = parser.parse()
        semantic_analyzer = SemanticAnalyzer()

        with self.assertRaises(Exception) as context:
            semantic_analyzer.visit(tree)
