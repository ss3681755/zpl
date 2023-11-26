from .token import Token, TokenType

_SPECIAL_CHAR_TOKEN_TYPE_MAPPING = {
    '#': TokenType.HASH,
    ' ': TokenType.SPACE,
    '\n': TokenType.NEWLINE,
    '\t': TokenType.TAB,
    '-': TokenType.MINUS,
    '_': TokenType.UNDERSCORE
}

TokenType.validate(_SPECIAL_CHAR_TOKEN_TYPE_MAPPING.values())

def special_char_token_type(value):
    return _SPECIAL_CHAR_TOKEN_TYPE_MAPPING[value]