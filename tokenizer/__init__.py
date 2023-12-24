from cursor import Cursor
from tokens import Token, TokenType, special_char_token_type

def _tokenize_alphabet(cursor):
    while cursor.can_move() and (ord('A') <= ord(cursor.peek()) <= ord('Z') or ord('a') <= ord(cursor.peek()) <= ord('z')):
        cursor.move()

def _tokenize_digit(cursor):
    while cursor.can_move() and ord('0') <= ord(cursor.peek()) <= ord('9'):
        cursor.move()

def _tokenize_special_char(cursor):
    if cursor.can_move():
        cursor.move()

def tokenize(text):
    cursor = Cursor(text)
    tokens = []
    while cursor.can_move():
        if value := cursor.attempt(_tokenize_alphabet):
            token = Token(value, cursor.location, TokenType.ALPHA)
        elif value := cursor.attempt(_tokenize_digit):
            token = Token(value, cursor.location, TokenType.INTEGER)
        elif value := cursor.attempt(_tokenize_special_char):
            token_type = special_char_token_type(value)
            token = Token(value, cursor.location, token_type)
        else:
            break

        tokens.append(token)
    return tokens or None
