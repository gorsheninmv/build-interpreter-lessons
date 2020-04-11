from .ex8 import Interpreter, Lexer, Parser

def main():
    while True:
        try:
            text = input('spi> ')
        except EOFError:
            print("EOF Detected")
            break

        if not text:
            continue

        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)
