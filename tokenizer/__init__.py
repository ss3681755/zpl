from copy import deepcopy as clone
from dataclasses import dataclass, field
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
    end: int
    typ: TokenType

SPECIAL_CHAR_TOKEN_TYPE_MAPPING = {
    ' ': TokenType.SPACE,
    '\n': TokenType.NEWLINE,
    '\t': TokenType.TAB,
    '-': TokenType.MINUS,
    '_': TokenType.UNDERSCORE
}

@dataclass
class Cursor:
    text: str
    index: int = field(default=0)
    line: int = field(default=1)
    offset: int = field(default=1)

    def can_advance(self):
        return self.index < len(self.text)

    def peek(self):
        assert self.can_advance()
        return self.text[self.index]

    def advance(self):
        assert self.can_advance()
        if self.text[self.index] == '\n':
            self.line += 1
            self.offset = 1
        self.index += 1

    def __eq__(self, other):
        return self.index == other.index

def _tokenize_alphabet(cursor):
    if not cursor.can_advance(): return None, cursor

    old_cursor = clone(cursor)
    while cursor.can_advance() and ord('A') <= ord(cursor.peek()) <= ord('z'):
        cursor.advance()

    if old_cursor == cursor: return None, old_cursor
    return Token(old_cursor.index, cursor.index, TokenType.ALPHA), cursor

def _tokenize_digits(cursor):
    if not cursor.can_advance(): return None, cursor

    old_cursor = clone(cursor)
    while cursor.can_advance() and ord('0') <= ord(cursor.peek()) <= ord('9'):
        cursor.advance()

    if old_cursor == cursor: return None, cursor
    return Token(old_cursor.index, cursor.index, TokenType.INTEGER), cursor

def _tokenize_special_char(cursor):
    if not cursor.can_advance(): return None, cursor
    token_type = SPECIAL_CHAR_TOKEN_TYPE_MAPPING.get(cursor.peek())
    if token_type is None: return None, cursor

    start = cursor.index
    cursor.advance()
    return Token(start, cursor.index, token_type), cursor


def tokenize(text):
    cursor = Cursor(text)
    tokens = []
    while cursor.can_advance():
        old_cursor = clone(cursor)
        token, cursor = _tokenize_alphabet(cursor)
        if token is not None: tokens.append(token)
        token, cursor = _tokenize_digits(cursor)
        if token is not None: tokens.append(token)
        token, cursor = _tokenize_special_char(cursor)
        if token is not None: tokens.append(token)

        # if index has not moved that means we have
        # encountered an unknown character at index.
        if old_cursor == cursor:
            raise Exception(f'Cannot tokenize input due to unsupported character with ascii code {ord(text[index])}')
    return tokens