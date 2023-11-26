from .token import Token, TokenType, special_char_token_type
from .cursor import Cursor

def _tokenize_alphabet(cursor):
    while cursor.can_advance() and (ord('A') <= ord(cursor.peek()) <= ord('Z') or ord('a') <= ord(cursor.peek()) <= ord('z')):
        cursor.advance()

    if value := cursor.extract():
        return Token(cursor, value, TokenType.ALPHA)

def _tokenize_digits(cursor):
    while cursor.can_advance() and ord('0') <= ord(cursor.peek()) <= ord('9'):
        cursor.advance()

    if value := cursor.extract():
        return Token(cursor, value, TokenType.INTEGER)

def _tokenize_special_char(cursor):
    cursor.advance()

    if value := cursor.extract():
        token_type = special_char_token_type(value)
        return Token(cursor, value, token_type)

def tokenize(text):
    cursor = Cursor(text)
    tokens = []
    while cursor.can_advance():
        old_token_count = len(tokens)
        if token := cursor.try_advance(_tokenize_alphabet):
            tokens.append(token)
        if token := cursor.try_advance(_tokenize_digits):
            tokens.append(token)
        if token := cursor.try_advance(_tokenize_special_char):
            tokens.append(token)

        # if no tokens were extracted that mean we
        # have encountered unsupported characters.
        if len(tokens) == old_token_count:
            raise Exception(f'Cannot tokenize input due to unsupported character with ascii code {ord(text[index])}')
    return tokens
