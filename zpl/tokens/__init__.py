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

@dataclass
class Token:
    value: int
    location: Location
    token_type: TokenType

    @staticmethod
    def alphabet(value: str, location: Location):
        return Token(value, location, TokenType.ALPHA)

    def integer(value: str, location: Location):
        return Token(value, location, TokenType.INTEGER)

    def special_char(value: str, location: Location):
        token_type = _SPECIAL_CHAR_TOKEN_TYPE_MAPPING[value]
        return Token(value, location, token_type)