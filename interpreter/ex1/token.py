from .token_type import TokenType

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return 'Token ({type}, {value})'.format(
                type = self.type,
                value = repr(self.value)
        )
