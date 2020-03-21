from .ex2 import Interpreter

def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            print("EOF Detected")
            break

        if not text:
            continue

        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)
