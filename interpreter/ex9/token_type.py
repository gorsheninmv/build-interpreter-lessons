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
    DOT = auto()
    BEGIN = auto()
    END = auto()
    ID = auto()
    ASSIGN = auto()
    SEMI = auto()
    EOF = auto()
    INF = auto()
