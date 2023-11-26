from cursor import Cursor
from tokens import Token, TokenType, special_char_token_type

def _tokenize_alphabet(cursor):
    while cursor.can_move() and (ord('A') <= ord(cursor.peek()) <= ord('Z') or ord('a') <= ord(cursor.peek()) <= ord('z')):
        cursor.move()

def _tokenize_digits(cursor):
    while cursor.can_move() and ord('0') <= ord(cursor.peek()) <= ord('9'):
        cursor.move()

def _tokenize_special_char(cursor):
    cursor.move()

def tokenize(text):
    cursor = Cursor(text)
    tokens = []
    while cursor.can_move():
        old_token_count = len(tokens)
        if value := cursor.attempt(_tokenize_alphabet):
            token = Token(cursor, value, TokenType.ALPHA)
            tokens.append(token)
        if value := cursor.attempt(_tokenize_digits):
            token = Token(cursor, value, TokenType.INTEGER)
            tokens.append(token)
        if value := cursor.attempt(_tokenize_special_char):
            token_type = special_char_token_type(value)
            token = Token(cursor, value, token_type)
            tokens.append(token)

        # if no tokens were extracted that mean we
        # have encountered unsupported characters.
        if len(tokens) == old_token_count:
            raise Exception(f'Cannot tokenize input due to unsupported character with ascii code {ord(text[index])}')
    return tokens
