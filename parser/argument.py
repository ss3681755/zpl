from dataclasses import dataclass
from enum import Flag, auto
from tokens import TokenType

from .terminals import parse_atom, parse_literal

class ArgumentType(Flag):
    ATOM = auto()
    LITERAL = auto()

@dataclass
class Argument:
    value: str
    kind: ArgumentType

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    def __hash__(self):
        return hash(self.value)

def _parse_spaces(cursor):
    while cursor.can_move() and cursor.peek().token_type == TokenType.SPACE:
        cursor.move()

def _count_spaces(cursor):
    if spaces := cursor.attempt(_parse_spaces):
        return len(spaces)
    return 0

def _parse_argument(cursor):
    if atom := cursor.attempt(parse_atom):
        return Argument(atom, ArgumentType.ATOM)

    if literal := cursor.attempt(parse_literal):
        return Argument(literal, ArgumentType.LITERAL)

def parse_argument_list(cursor):
    arguments = []
    while cursor.can_move():
        # ignore spaces if any but there must be at least 1 space
        # if not that means we have reached the end of function call.
        if cursor.attempt(_count_spaces) == 0: break

        if arg := cursor.attempt(_parse_argument):
            arguments.append(arg)

    return arguments or None