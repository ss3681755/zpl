from enum import Flag, auto

class TokenType(Flag):
    ALPHA = auto()
    INTEGER = auto()
    HASH = auto()
    MINUS = auto()
    NEWLINE = auto()
    SPACE = auto()
    TAB = auto()
    UNDERSCORE = auto()

    @classmethod
    def validate(cls, values):
        uniq_values = set(values)
        assert len(values) == len(uniq_values), 'All reverse mapped values must be unique.'
        for member in cls:
            if member in [TokenType.ALPHA, TokenType.INTEGER]: continue
            assert member in uniq_values, 'Make sure all the special character token types are uniquely reverse mapped to a token type.'