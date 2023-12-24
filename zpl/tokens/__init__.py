from dataclasses import dataclass
from enum import Flag, auto

from zpl.cursor import Location

class TokenType(Flag):
    ALPHA = auto()
    INTEGER = auto()
    HASH = auto()
    MINUS = auto()
    NEWLINE = auto()
    SPACE = auto()
    TAB = auto()
    UNDERSCORE = auto()

# Reverse Mapping of TokenType enum
_SPECIAL_CHAR_TOKEN_TYPE_MAPPING = {
    '#': TokenType.HASH,
    ' ': TokenType.SPACE,
    '\n': TokenType.NEWLINE,
    '\t': TokenType.TAB,
    '-': TokenType.MINUS,
    '_': TokenType.UNDERSCORE
}

def special_char_token_type(value):
    return _SPECIAL_CHAR_TOKEN_TYPE_MAPPING[value]

@dataclass
class Token:
    value: int
    location: Location
    token_type: TokenType