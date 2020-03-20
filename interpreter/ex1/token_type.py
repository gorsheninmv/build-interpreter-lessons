from enum import Enum, auto

class TokenType(Enum):
    """ Token types """

    NUL = auto()
    INTEGER = auto()
    PLUS = auto()
    EOF = auto()
    INF = auto()
