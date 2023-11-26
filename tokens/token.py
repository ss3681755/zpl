from dataclasses import dataclass
from .token_type import TokenType

@dataclass
class Token:
    start: int
    value: int
    line: int
    offset: int
    token_type: TokenType

    def __init__(self, cursor, value, token_type):
        self.start = cursor.index
        self.line = cursor.line
        self.offset = cursor.offset
        self.value = value
        self.token_type = token_type