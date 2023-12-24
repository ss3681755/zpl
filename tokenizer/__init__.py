from cursor import Cursor
from tokens import Token, TokenType, special_char_token_type

from .alphabet import tokenize as _tokenize_alphabet
from .digit import tokenize as _tokenize_digit
from .special_char import tokenize as _tokenize_special_char

def tokenize(text):
    cursor = Cursor(text)
    tokens = []
    while cursor.can_move():
        old_token_count = len(tokens)
        if value := cursor.attempt(_tokenize_alphabet):
            token = Token(value, cursor.location, TokenType.ALPHA)
            tokens.append(token)
        if value := cursor.attempt(_tokenize_digit):
            token = Token(value, cursor.location, TokenType.INTEGER)
            tokens.append(token)
        if value := cursor.attempt(_tokenize_special_char):
            token_type = special_char_token_type(value)
            token = Token(value, cursor.location, token_type)
            tokens.append(token)

        # if no tokens were extracted that mean we
        # have encountered unsupported characters.
        if len(tokens) == old_token_count:
            raise Exception(f'Cannot tokenize input due to unsupported character with ascii code {ord(text[index])}')
    return tokens
