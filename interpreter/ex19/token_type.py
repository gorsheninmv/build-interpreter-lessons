from enum import Enum, auto

class TokenType(Enum):
    """ Token types """

    INF = auto()

    # single-character token types
    PLUS = '+'
    MINUS = '-'
    MUL = '*'
    FLOAT_DIV = '/'
    LP = '('
    RP = ')'
    SEMI = ';'
    DOT = '.'
    COMMA = ','
    COLON = ':'

    # block of reserved words
    RESERVED_INF = auto()
    INTEGER = 'INTEGER'
    INTEGER_DIV = 'DIV'
    PROGRAM = 'PROGRAM'
    VAR = 'VAR'
    REAL = 'REAL'
    BEGIN = 'BEGIN'
    END = 'END'
    PROCEDURE = 'PROCEDURE'
    RESERVED_SUP = auto()

    # misc
    ID = 'ID'
    ASSIGN = ':='
    INTEGER_CONST = 'INTEGER_CONST'
    REAL_CONST = 'REAL_CONST'
    EOF = 'EOF'

    SUP = auto()
