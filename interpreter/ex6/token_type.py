from enum import Enum, auto

class TokenType(Enum):
    """ Token types """

    NUL = auto()
    INTEGER = auto()
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    LP = auto()
    RP = auto()
    EOF = auto()
    INF = auto()
