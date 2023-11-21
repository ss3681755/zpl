from .token import Token, TokenType
from .cursor import Cursor

_SPECIAL_CHAR_TOKEN_TYPE_MAPPING = {
    ' ': TokenType.SPACE,
    '\n': TokenType.NEWLINE,
    '\t': TokenType.TAB,
    '-': TokenType.MINUS,
    '_': TokenType.UNDERSCORE
}

def _tokenize_alphabet(cursor):
    token = None
    with cursor.locked():
        while cursor.can_advance() and (ord('A') <= ord(cursor.peek()) <= ord('Z') or ord('a') <= ord(cursor.peek()) <= ord('z')):
            cursor.advance()

        value = cursor.extract()
        if value is None: raise Exception('Could not extract alphabet.')
        token = Token(cursor, value, TokenType.ALPHA)
    return token


def _tokenize_digits(cursor):
    token = None
    with cursor.locked():
        while cursor.can_advance() and ord('0') <= ord(cursor.peek()) <= ord('9'):
            cursor.advance()

        value = cursor.extract()
        if value is None: raise Exception('Could not extract alphabet.')
        token = Token(cursor, value, TokenType.INTEGER)
    return token

def _tokenize_special_char(cursor):
    token = None
    with cursor.locked():
        cursor.advance()

        value = cursor.extract()
        if value is None: raise Exception('Could not extract alphabet.')
        token_type = _SPECIAL_CHAR_TOKEN_TYPE_MAPPING.get(value)
        token = Token(cursor, value, token_type)
    return token

def tokenize(text):
    cursor = Cursor(text)
    tokens = []
    while cursor.can_advance():
        old_token_count = len(tokens)
        if token := _tokenize_alphabet(cursor):
            tokens.append(token)
        if token := _tokenize_digits(cursor):
            tokens.append(token)
        if token := _tokenize_special_char(cursor):
            tokens.append(token)

        # if no tokens were extracted that mean we
        # have encountered unsupported characters.
        if len(tokens) == old_token_count:
            raise Exception(f'Cannot tokenize input due to unsupported character with ascii code {ord(text[index])}')
    return tokens
