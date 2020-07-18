from enum import Enum
from .token import Token

class ErrorCode(Enum):
    UNEXPECTED_TOKEN = 'Unexpected token'
    ID_NOT_FOUND = 'Identifier not found'
    DUPLICATE_ID = 'Duplicate id found'
    PARAMS_COUNT_MISMATCH = 'Number of actual and formal parameters are not equal'

class Error(Exception):
    def __init__(self, error_code: ErrorCode=None, token: Token=None, message: str=None):
        super().__init__(f'{self.__class__.__name__}: {message}')
        self.error_code = error_code
        self.token = token

class LexerError(Error):
    pass

class ParserError(Error):
    pass

class SemanticError(Error):
    pass
