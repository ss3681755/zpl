from dataclasses import dataclass
from enum import Flag, auto

class TokenType(Flag):
    ALPHA = auto()
    INTEGER = auto()
    MINUS = auto()
    NEWLINE = auto()
    SPACE = auto()
    TAB = auto()
    UNDERSCORE = auto()

@dataclass
class Token:
    start: int
    value: int
    line: int
    offset: int
    token_type: TokenType

    def __init__(self, cursor, value, token_type):
        self.start = cursor.index
        self.line = cursor.line
        self.offset = cursor.offset
        self.value = value
        self.token_type = token_type

_SPECIAL_CHAR_TOKEN_TYPE_MAPPING = {
    ' ': TokenType.SPACE,
    '\n': TokenType.NEWLINE,
    '\t': TokenType.TAB,
    '-': TokenType.MINUS,
    '_': TokenType.UNDERSCORE
}

def special_char_token_type(value):
    return _SPECIAL_CHAR_TOKEN_TYPE_MAPPING[value]