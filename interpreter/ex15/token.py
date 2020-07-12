from .token_type import TokenType

class Token:
    def __init__(self, type, value, lineno=None, column=None):
        self.type = type
        self.value = value
        self.lineno = lineno
        self.column = column

    def __eq__(self, other):
        return (self.type == other.type and
                self.value == other.value)

    def __repr__(self):
        return f'Token ({self.type}, {self.value}, position={self.lineno}:{self.column})'
