import argparse
from .interpreter import Interpreter, enable_log as interp_enable_log
from .lexer import Lexer
from .parser import Parser
from .symbols import SemanticAnalyzer, enable_log as symbols_enable_log
from .error import *
import sys

def main():
    argparser = argparse.ArgumentParser(
            description='Simple Pascal Interpreter')
    argparser.add_argument(
            'inputfile',
            help='Pascal source file')
    argparser.add_argument(
            '--scope',
            help='Print scope information',
            action='store_true')
    argparser.add_argument(
            '--stack',
            help='Print call stack',
            action='store_true')

    args = argparser.parse_args()

    if args.scope: symbols_enable_log()
    if args.stack: interp_enable_log()

    source_code = open(args.inputfile, 'r').read()

    lexer = Lexer(source_code)

    try:
        parser = Parser(lexer)
        tree = parser.parse()
    except (LexerError, ParserError) as e:
        print(e.message)
        sys.exit(1)

    semantic_analyzer = SemanticAnalyzer()

    try:
        semantic_analyzer.visit(tree)
    except SemanticError as e:
        print(e)
        sys.exit(1)

    interpreter = Interpreter(tree)
    interpreter.interpret()
