from dataclasses import dataclass
from cursor import Location
from .token_type import TokenType


@dataclass
class Token:
    value: int
    location: Location
    token_type: TokenType