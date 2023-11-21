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
    end: int
    typ: TokenType

def _tokenize_alphabet(index, text):
    if index >= len(text): return None, index

    start = index
    while index < len(text) and ord('A') <= ord(text[index]) <= ord('z'):
        index += 1

    if start == index: return None, start
    return Token(start, index, TokenType.ALPHA), index

def _tokenize_digits(index, text):
    if index >= len(text): return None, index

    start = index
    while index < len(text) and ord('0') <= ord(text[index]) <= ord('9'):
        index += 1

    if start == index: return None, start
    return Token(start, index, TokenType.INTEGER), index

def _tokenize_space(index, text):
    if index >= len(text): return None, index

    match text[index]:
        case ' ':
            return Token(index, index + 1, TokenType.SPACE), index + 1
        case '\n':
            return Token(index, index + 1, TokenType.NEWLINE), index + 1
        case '\t':
            return Token(index, index + 1, TokenType.TAB), index + 1
        case '-':
            return Token(index, index + 1, TokenType.MINUS), index + 1
        case '_':
            return Token(index, index + 1, TokenType.UNDERSCORE), index + 1
        case _:
            return None, index


def tokenize(text):
    index = 0
    tokens = []
    while index < len(text):
        oindex = index
        token, index = _tokenize_alphabet(index, text)
        if token is not None: tokens.append(token)
        token, index = _tokenize_digits(index, text)
        if token is not None: tokens.append(token)
        token, index = _tokenize_space(index, text)
        if token is not None: tokens.append(token)

        # if index has not moved that means we have
        # encountered an unknown character at index.
        if index == oindex:
            raise Exception(f'Cannot tokenize input due to unsupported character with ascii code {ord(text[index])}')
    return tokens